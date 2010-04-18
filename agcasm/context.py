#!/usr/bin/env python

# Copyright 2010 Jim Lawton <jim dot lawton at gmail dot com>
# 
# This file is part of pyagc. 
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from memory import MemoryMap, MemoryType
from opcode import OpcodeType
from opcodes import OPCODES
from symbol_table import SymbolTable

class Context:
    def __init__(self, arch, listfile, binfile, verbose=False, logging=False, logfile=None):
        self.verbose = verbose
        self.logging = logging
        self.logfile = logfile
        self.assembler = None
        self.arch = arch
        self.listfile = listfile
        self.binfile = binfile
        self.srcfile = None
        self.opcodes = OPCODES[self.arch]
        self.symtab = SymbolTable(self)
        self.linenum = 0
        self.global_linenum = 0
        self.mode = OpcodeType.BASIC
        self.memmap = MemoryMap(arch, verbose)
        self.lastEbank = 0
        self.lastEbankEquals = False
        self.code = []
        self.records = []
        self.srcline = None
        self.interpMode = False
        self.interpArgs = 0
        self.indexed = False
        self.currentRecord = None
        self.addSymbol = True
        self.reparse = False

        self.loc = 0        # Assembler PC, i.e. current position in erasable or fixed memory.
        self.sbank = 0      # Current S-Bank.
        self.ebank = 0      # Current E-Bank.
        self.fbank = 0      # Current F-Bank.

        self.ebankloc = {}  # Saved current location for each erasable bank.
        self.fbankloc = {}  # Saved current location for each fixed bank.

        for bank in range(len(self.memmap.banks[MemoryType.ERASABLE])):
            self.ebankloc[bank] = 0
        for bank in range(len(self.memmap.banks[MemoryType.FIXED])):
            self.fbankloc[bank] = 0
        
    def setLoc(self, loc):
        if not self.reparse:
            self.loc = loc

    def incrLoc(self, delta):
        if not self.reparse:
            self.loc += delta

    def setSBank(self, bank):
        if not self.reparse:
            self.sbank = bank

    def switchEBank(self, bank):
        if not self.reparse:
            self.lastEbank = self.ebank
            if self.memmap.isErasable(self.loc):
                self.ebankloc[self.ebank] = self.memmap.pseudoToBankOffset(self.loc)
            self.ebank = bank
            if self.memmap.isErasable(self.loc):
                self.loc = self.memmap.segmentedToPseudo(MemoryType.ERASABLE, bank, self.ebankloc[bank])
            self.lastEbankEquals = True
            self.log("switched EB to %s [%s:%d]" % (self.memmap.pseudoToSegmentedString(self.loc), self.srcfile, self.linenum))

    def revertEbank(self):
        if not self.reparse:
            if self.lastEbankEquals:
                if self.memmap.isErasable(self.loc):
                    self.ebankloc[self.ebank] = self.memmap.pseudoToBankOffset(self.loc)
                self.ebank = self.lastEbank
                if self.memmap.isErasable(self.loc):
                    self.loc = self.memmap.segmentedToPseudo(MemoryType.ERASABLE, self.lastEbank, self.ebankloc[self.lastEbank])
                self.lastEbankEquals = False

    def switchFBank(self, bank=None):
        if not self.reparse:
            if bank:
                offset = self.memmap.pseudoToBankOffset(self.loc)
                if offset != None:
                    self.fbankloc[self.fbank] = offset
                    self.fbank = bank
                    self.loc = self.memmap.segmentedToPseudo(MemoryType.FIXED, bank, self.fbankloc[self.fbank])
                    self.log("switched FB to %s [%s:%d]" % (self.memmap.pseudoToSegmentedString(self.loc), self.srcfile, self.linenum))
                else:
                    self.error("invalid address %06o" % self.loc)
            else:
                self.loc = self.memmap.segmentedToPseudo(MemoryType.FIXED, self.fbank, self.fbankloc[self.fbank])
                self.log("switched FB to %s [%s:%d]" % (self.memmap.pseudoToSegmentedString(self.loc), self.srcfile, self.linenum))
