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
        if not self.memmap.isValid(loc):
            self.error("trying to set loc to an invalid address (%06o)" % loc)
        if not self.reparse:
            self.log("changing loc from %06o to %06o" % (self.loc, loc))
            self.loc = loc

    def incrLoc(self, delta):
        if not self.memmap.isValid(self.loc + delta):
            self.error("trying to set loc to an invalid address (%06o)" % (self.loc + delta))
        if not self.reparse:
            #self.log("incrementing loc from %06o to %06o (delta=%04o)" % (self.loc, self.loc + delta, delta))
            self.loc += delta

    def setSBank(self, bank):
        if not self.reparse:
            self.sbank = bank

    def switchEBank(self, bank):
        pa = self.ebankloc[bank]
        self.printBanks()
        self.switchEBankPA(pa)

    def saveCurrentBank(self):
        (bank, offset) = self.memmap.pseudoToBankOffset(self.loc)
        if bank!= None and offset != None:
            if self.memmap.isErasable(self.loc):
                self.log("saving EB %02o: %04o -> %04o" % (bank, self.ebankloc[bank], offset))
                self.ebankloc[bank] = offset
            else:
                self.log("saving FB %02o: %04o -> %04o" % (bank, self.fbankloc[bank], offset))
                self.fbankloc[bank] = offset
        else:
            self.error("invalid address %06o" % self.loc)
            
    def switchEBankPA(self, pa):
        if not self.reparse:
            self.lastEbank = self.ebank
            self.saveCurrentBank()
            self.ebank = self.memmap.pseudoToBank(pa)
            self.setLoc(self.memmap.segmentedToPseudo(MemoryType.ERASABLE, self.ebank, self.ebankloc[self.ebank]))
            self.lastEbankEquals = True
            self.log("switched EB to %s [%s:%d]" % (self.memmap.pseudoToSegmentedString(self.ebankloc[self.ebank]), self.srcfile, self.linenum))

    def revertEbank(self):
        if not self.reparse:
            self.printBanks()
            if self.lastEbankEquals:
                self.saveCurrentBank()
                self.ebank = self.lastEbank
                self.setLoc(self.memmap.segmentedToPseudo(MemoryType.ERASABLE, self.lastEbank, self.ebankloc[self.lastEbank]))
                self.log("reverted EB to %s [%s:%d]" % (self.memmap.pseudoToSegmentedString(self.ebankloc[self.ebank]), self.srcfile, self.linenum))
                self.lastEbankEquals = False

    def switchFBank(self, bank=None):
        if not self.reparse:
            if bank != None:
                self.log("switching to bank %02o" % bank)
                self.saveCurrentBank()
                self.fbank = bank
            self.setLoc(self.memmap.segmentedToPseudo(MemoryType.FIXED, self.fbank, self.fbankloc[self.fbank]))
            self.log("switched FB to %s [%s:%d]" % (self.memmap.pseudoToSegmentedString(self.loc), self.srcfile, self.linenum))

    def printBanks(self):
        text = "LOC=%06o EB=%02o FB=%02o " % (self.loc, self.ebank, self.fbank)
        text += "EBs: "
        for eb in self.ebankloc.keys():
            if self.ebankloc[eb] > 0:
                text += "%02o:%04o " % (eb, self.ebankloc[eb])
        text += "FBs: "
        for fb in self.fbankloc.keys():
            if self.fbankloc[fb] > 0:
                text += "%02o:%04o " % (fb, self.fbankloc[fb])
        self.log(text)
        