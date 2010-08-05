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
    def __init__(self, arch, listfile, binfile, verbose=False, logLevel=0, logfile=None):
        self.verbose = verbose
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
        self.previousWasEbankEquals = False
        self.code = []
        self.records = []
        self.srcline = None
        self.interpMode = False
        self.interpArgs = 0
        self.interpArgTypes = [ None, None, None, None ]
        self.interpArgCodes = [ 0, 0, 0, 0 ]
        self.previousWasInterpOperand = False
        self.indexed = False
        self.currentRecord = None
        self.previousRecord = None
        self.addSymbol = True
        self.reparse = False
        self.passnum = 0
        self.complementNext = False     # STADR complements the following instruction(s).

        # Log level:
        #  0 - None.
        #  1 - Errors.
        #  2 - Warnings.
        #  3 - Info messages.
        #  4 - Bank changes, binary generation.
        #  5 - LOC changes, detailed interpretive logging.
        #  6 - Symbol information, address conversion.
        #  7 - Parser operation.
        #  8 - Symbol resolution.
        self.logLevel = logLevel

        self.loc = 0        # Assembler PC, i.e. current position in erasable or fixed memory.
        self.ebank = 0      # Current E-Bank.
        self.fbank = 0      # Current F-Bank.
        self.super = 0      # Superbank bit (0/1).

        self.ebankloc = {}  # Saved current location for each erasable bank.
        self.fbankloc = {}  # Saved current location for each fixed bank.

        for bank in range(len(self.memmap.banks[MemoryType.ERASABLE])):
            self.ebankloc[bank] = 0
        for bank in range(len(self.memmap.banks[MemoryType.FIXED])):
            self.fbankloc[bank] = 0

        self.errors = 0
        self.warnings = 0

    def reset(self):
        self.linenum = 0
        self.global_linenum = 0
        self.mode = OpcodeType.BASIC
        self.lastEbank = 0
        self.previousWasEbankEquals = False
        self.code = []
        self.srcline = None
        self.interpMode = False
        self.interpArgs = 0
        self.interpArgTypes = [ None, None, None, None ]
        self.interpArgCodes = [ 0, 0, 0, 0 ]
        self.previousWasInterpOperand = False
        self.indexed = False
        self.currentRecord = None
        self.previousRecord = None
        self.addSymbol = True
        self.reparse = False
        self.loc = 0
        self.super = 0
        self.ebank = 0
        self.fbank = 0
        self.complementNext = False

    def load(self, record, partial=True):
        self.linenum = record.linenum
        self.global_linenum = record.global_linenum
        self.code = record.code
        self.srcline = record.srcline
        self.loc = record.loc
        if partial == False:
            self.mode = record.mode
            self.lastEbank = record.lastEbank
            self.previousWasEbankEquals = record.previousWasEbankEquals
            self.super = record.super
            self.ebank = record.ebank
            self.fbank = record.fbank

    def save(self, record, partial=True):
        record.linenum = self.linenum
        record.global_linenum = self.global_linenum
        record.code = self.code
        record.srcline = self.srcline
        if partial == False:
            record.lastEbank = self.lastEbank
            record.previousWasEbankEquals = self.previousWasEbankEquals
            record.mode = self.mode
            record.loc = self.loc
            record.super = self.super
            record.ebank = self.ebank
            record.fbank = self.fbank

    def setLoc(self, loc):
        if not self.memmap.isValid(loc):
            self.error("trying to set loc to an invalid address (%06o)" % loc)
        if not self.reparse:
            self.log(5, "changing loc from %06o to %06o" % (self.loc, loc))
            self.loc = loc

    def incrLoc(self, delta):
        if not self.memmap.isValid(self.loc + delta):
            self.error("trying to set loc to an invalid address (%06o)" % (self.loc + delta))
        if not self.reparse:
            self.log(5, "incrementing loc from %06o to %06o (delta=%04o)" % (self.loc, self.loc + delta, delta))
            self.loc += delta

    def switchEBank(self, bank):
        pa = self.ebankloc[bank]
        self.printBanks()
        self.switchEBankPA(pa)

    def saveCurrentBank(self):
        (bank, offset) = self.memmap.pseudoToBankOffset(self.loc)
        if bank != None and offset != None:
            if self.memmap.isErasable(self.loc):
                if offset > self.ebankloc[bank]:
                    self.log(4, "saving EB %02o: %04o -> %04o" % (bank, self.ebankloc[bank], offset))
                    self.ebankloc[bank] = offset
            else:
                if offset > self.fbankloc[bank]:
                    self.log(4, "saving FB %02o: %04o -> %04o" % (bank, self.fbankloc[bank], offset))
                    self.fbankloc[bank] = offset
        else:
            self.error("invalid address %06o" % self.loc)

    def switchEBankPA(self, pa):
        if not self.reparse:
            self.lastEbank = self.ebank
            self.saveCurrentBank()
            self.ebank = self.memmap.pseudoToBank(pa)
            self.log(4, "switched EB: %02o -> %02o" % (self.lastEbank, self.ebank))
            if self.memmap.isErasable(self.loc):
                # Only change LOC if it is currently erasable. This allows us to move LOC up through the various
                # erasable banks at the start as symbols are defined. Later, in fixed banks, you do not want an
                # EBANK= to affect LOC.
                self.setLoc(self.memmap.segmentedToPseudo(MemoryType.ERASABLE, self.ebank, self.ebankloc[self.ebank]))
            self.previousWasEbankEquals = True
            self.printBanks()

    def revertEbank(self):
        if not self.reparse:
            self.printBanks()
            if self.previousWasEbankEquals == True:
                self.saveCurrentBank()
                self.ebank = self.lastEbank
                self.log(4, "reverted EB: %02o -> %02o" % (self.lastEbank, self.ebank))
                if self.memmap.isErasable(self.loc):
                    self.setLoc(self.memmap.segmentedToPseudo(MemoryType.ERASABLE, self.lastEbank, self.ebankloc[self.lastEbank]))
                self.previousWasEbankEquals = False

    def switchFBank(self, bank=None):
        if not self.reparse:
            if bank != None:
                self.saveCurrentBank()
                oldbank = self.fbank
                self.fbank = bank
                self.log(4, "switched FB: %02o -> %02o" % (oldbank, self.fbank))
            self.setLoc(self.memmap.segmentedToPseudo(MemoryType.FIXED, self.fbank, self.fbankloc[self.fbank]))
            self.log(4, "switched FB to %s" % (self.memmap.pseudoToSegmentedString(self.loc)))

    def getBankCount(self, memtype, bank):
        if memtype == MemoryType.ERASABLE:
            return self.ebankloc[bank]
        else:
            return self.fbankloc[bank]

    def getBankSize(self, memtype, bank):
        return self.memmap.banks[memtype][bank].size

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
        self.log(4, text)
