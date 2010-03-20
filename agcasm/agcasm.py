#!/usr/bin/env python

# Copyright 2010 Jim Lawton <jim dot lawton at gmail dot com>
# 
# This file is part of yaAGC. 
#
# yaAGC is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# yaAGC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with yaAGC; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import os
import sys
import glob
import re
from optparse import OptionParser

class Architecture:
    AGC1    = 0    # Mod1
    AGC2    = 1    # Mod2
    AGC3    = 2    # AGC3
    AGC4_B1 = 3    # AGC4 Block I
    AGC4_B2 = 4    # AGC4 Block II

class MemoryType:
    ERASABLE    = 0
    FIXED       = 1
    NONEXISTENT = 2

class BankType:
    UNSWITCHED  = 0
    SWITCHED    = 1
    NONEXISTENT = 2

class BankDescriptor:
    def __init__(self, startaddr, memtype, banktype=None, banknum=None, size=0, name=None, superbank=None):
        self.startaddr = startaddr
        self.memtype = memtype
        self.banktype = banktype
        self.banknum = banknum
        self.size = size
        self.name = None
        if name:
            self.name = name
        else:
            if banknum:
                self.name = "%03o" % banknum
        self.superbank = superbank

    def __str__(self):
        return "%06o %d %d %03o %05o" % (self.startaddr, self.memtype, self.banktype, self.banknum, self.size)
        
# Memory Map
MAPS = {
    # Each entry contains (start_address, size, number)
    Architecture.AGC4_B1: {
    }, 
    Architecture.AGC4_B2: {
        0000000: BankDescriptor(0000000, MemoryType.ERASABLE, BankType.UNSWITCHED, 00,  0400, "E0"),
        0000400: BankDescriptor(0000400, MemoryType.ERASABLE, BankType.UNSWITCHED, 01,  0400, "E1"),
        0001000: BankDescriptor(0001000, MemoryType.ERASABLE, BankType.UNSWITCHED, 02,  0400, "E2"),
        0001400: BankDescriptor(0001400, MemoryType.ERASABLE, BankType.SWITCHED,   03,  0400, "E3"),
        0002000: BankDescriptor(0002000, MemoryType.ERASABLE, BankType.SWITCHED,   04,  0400, "E4"),
        0002400: BankDescriptor(0002400, MemoryType.ERASABLE, BankType.SWITCHED,   05,  0400, "E5"),
        0003000: BankDescriptor(0003000, MemoryType.ERASABLE, BankType.SWITCHED,   06,  0400, "E6"),
        0003400: BankDescriptor(0003400, MemoryType.ERASABLE, BankType.SWITCHED,   07,  0400, "E7"),
        0004000: BankDescriptor(0004000, MemoryType.FIXED,    BankType.UNSWITCHED, 002, 02000),
        0006000: BankDescriptor(0006000, MemoryType.FIXED,    BankType.UNSWITCHED, 003, 02000),
        0010000: BankDescriptor(0010000, MemoryType.FIXED,    BankType.SWITCHED,   000, 02000),
        0012000: BankDescriptor(0012000, MemoryType.FIXED,    BankType.SWITCHED,   001, 02000),
        0014000: BankDescriptor(0014000, MemoryType.NONEXISTENT),        
        0016000: BankDescriptor(0016000, MemoryType.NONEXISTENT),        
        0020000: BankDescriptor(0020000, MemoryType.FIXED,    BankType.SWITCHED,   004, 02000),
        0022000: BankDescriptor(0022000, MemoryType.FIXED,    BankType.SWITCHED,   005, 02000),
        0024000: BankDescriptor(0024000, MemoryType.FIXED,    BankType.SWITCHED,   006, 02000),
        0026000: BankDescriptor(0026000, MemoryType.FIXED,    BankType.SWITCHED,   007, 02000),
        0030000: BankDescriptor(0030000, MemoryType.FIXED,    BankType.SWITCHED,   010, 02000),
        0032000: BankDescriptor(0032000, MemoryType.FIXED,    BankType.SWITCHED,   011, 02000),
        0034000: BankDescriptor(0034000, MemoryType.FIXED,    BankType.SWITCHED,   012, 02000),
        0036000: BankDescriptor(0036000, MemoryType.FIXED,    BankType.SWITCHED,   013, 02000),
        0040000: BankDescriptor(0040000, MemoryType.FIXED,    BankType.SWITCHED,   014, 02000),
        0042000: BankDescriptor(0042000, MemoryType.FIXED,    BankType.SWITCHED,   015, 02000),
        0044000: BankDescriptor(0044000, MemoryType.FIXED,    BankType.SWITCHED,   016, 02000),
        0046000: BankDescriptor(0046000, MemoryType.FIXED,    BankType.SWITCHED,   017, 02000),
        0050000: BankDescriptor(0050000, MemoryType.FIXED,    BankType.SWITCHED,   020, 02000),
        0052000: BankDescriptor(0052000, MemoryType.FIXED,    BankType.SWITCHED,   021, 02000),
        0054000: BankDescriptor(0054000, MemoryType.FIXED,    BankType.SWITCHED,   022, 02000),
        0056000: BankDescriptor(0056000, MemoryType.FIXED,    BankType.SWITCHED,   023, 02000),
        0060000: BankDescriptor(0060000, MemoryType.FIXED,    BankType.SWITCHED,   024, 02000),
        0062000: BankDescriptor(0062000, MemoryType.FIXED,    BankType.SWITCHED,   025, 02000),
        0064000: BankDescriptor(0064000, MemoryType.FIXED,    BankType.SWITCHED,   026, 02000),
        0066000: BankDescriptor(0066000, MemoryType.FIXED,    BankType.SWITCHED,   027, 02000),
        0070000: BankDescriptor(0070000, MemoryType.FIXED,    BankType.SWITCHED,   030, 02000, 0),
        0072000: BankDescriptor(0072000, MemoryType.FIXED,    BankType.SWITCHED,   031, 02000, 0),
        0074000: BankDescriptor(0074000, MemoryType.FIXED,    BankType.SWITCHED,   032, 02000, 0),
        0076000: BankDescriptor(0076000, MemoryType.FIXED,    BankType.SWITCHED,   033, 02000, 0),
        0100000: BankDescriptor(0100000, MemoryType.FIXED,    BankType.SWITCHED,   034, 02000, 0),
        0102000: BankDescriptor(0102000, MemoryType.FIXED,    BankType.SWITCHED,   035, 02000, 0),
        0104000: BankDescriptor(0104000, MemoryType.FIXED,    BankType.SWITCHED,   036, 02000, 0),
        0106000: BankDescriptor(0106000, MemoryType.FIXED,    BankType.SWITCHED,   037, 02000, 0),
        0110000: BankDescriptor(0110000, MemoryType.FIXED,    BankType.SWITCHED,   040, 02000, 1),
        0112000: BankDescriptor(0112000, MemoryType.FIXED,    BankType.SWITCHED,   041, 02000, 1),
        0114000: BankDescriptor(0114000, MemoryType.FIXED,    BankType.SWITCHED,   042, 02000, 1),
        0116000: BankDescriptor(0116000, MemoryType.FIXED,    BankType.SWITCHED,   043, 02000, 1)
    } 
}


class MemoryMap:
    def __init__(self, arch, verbose=False):
        self.verbose = verbose
        self.arch = arch
        self.memmap = MAPS[arch]
        self.banks = { MemoryType.ERASABLE: {}, MemoryType.FIXED: {} }
        for startaddr in self.memmap:
            if self.memmap[startaddr].memtype == MemoryType.ERASABLE:
                self.banks[MemoryType.ERASABLE][self.memmap[startaddr].banknum] = self.memmap[startaddr]
            elif self.memmap[startaddr].memtype == MemoryType.FIXED:
                self.banks[MemoryType.FIXED][self.memmap[startaddr].banknum] = self.memmap[startaddr]

    def __str__(self):
        text = ""
        for bank in self.memmap:
            text += "%s" % bank
            
    def findBank(self, pa):
        bank = None
        found = False
        addrs = self.memmap.keys()
        addrs.sort()
        for startaddr in addrs:
            if pa < startaddr + self.memmap[startaddr].size:
                found = True
                break
        
        if found:
            bank = self.memmap[startaddr]
        
        return bank
        
    def convertBankToPA(self, banktype, bank, address=0):
        pa = self.banks[banktype][bank].startaddr + address
        #print "(%02o,%04o) -> %06o" % (bank, address, pa)
        #testaddr = self.convertPAToBank(pa)
        #print "(%02o,%04o) -> %06o -> %s" % (bank, address, pa, self.convertBankToString(testaddr[0], testaddr[1]))
        return pa
    
    def convertBankToString(self, bank, address=0):
        return "%02o,%04o" % (bank, address)
        
    def convertPAToBank(self, pa):
        bank = self.findBank(pa)
        if bank:
            offset = pa - bank.startaddr
            #print "%06o -> (%02o,%04o)" % (pa, bank.banknum, offset)
            return (bank.banknum, offset)
        else:
            return (None, 0)
    
    def convertPAToString(self, pa):
        return "%06o" % (pa)
    

class OpcodeType:
    BASIC    = 0
    EXTENDED = 1
    BOTH     = 2


class OperandType:
    NONE        = 0    # No operand.
    ERASABLE_10 = 1    # 10-bit erasable address.
    ERASABLE_12 = 2    # 12-bit erasable address.
    FIXED_9     = 3    # 9-bit fixed address. Only used by EDRUPT?
    FIXED_12    = 4    # 12-bit fixed address.
    GENERAL_12  = 5    # 12-bit general address (fixed or erasable).
    CHANNEL     = 6    # 9-bit I/O channel address.


class SymbolTableEntry:
    
    def __init__(self, context, name, symbolic=None, value=-1):
        self.context = context
        self.name = name
        self.symbolic = symbolic
        self.value = value

    def __str__(self):
        text = "%-8s "  % (self.name)
        if self.value == -1:
            text += "%-20s" % "UNDEFINED"
        else:
            text += "%-10s" % self.context.memmap.convertPAToString(self.value)
            text += "(%02o,%04o) " % self.context.memmap.convertPAToBank(self.value)
            print self.context.memmap.convertPAToBank(self.value)
        if self.symbolic:
            text += " \"%s\""  % (self.symbolic)
        return text

class SymbolTable:
    def __init__(self, context):
        self.symbols = {}
        self.context = context
        
    def add(self, name=None, symbolic=None, value=-1):
        if name in self.symbols:
            print >>sys.stderr, "Error, symbol \"%s\" already defined!" % (name)
            sys.exit()
        else:
            self.symbols[name] = SymbolTableEntry(self.context, name, symbolic, value)

    def keys(self):
        return self.symbols.keys()

    def lookup(self, name):
        entry = None
        if name in self.symbols:
            entry = self.symbols[name]
        return entry

    def printTable(self):
        symbols = self.symbols.keys()
        symbols.sort()
        for symbol in symbols:
            print self.symbols[symbol]


class Number:
    OCTAL   = 0
    DECIMAL = 1
    FLOAT   = 2
    
    OCTAL_RE   = re.compile("^[+-]*[0-7]+$")
    DECIMAL_RE = re.compile("^[+-]*[0-9]+D$")
    FLOAT_RE   = re.compile("^[+-]*[0-9]*\.[0-9]+ *(E[+-]*[0-9]+)* *(B[+-]*[0-9]+)*[*]*$")
    
    def __init__(self, text):
        self.valid = False
        self.text = text
        self.value = 0
        if self.OCTAL_RE.search(text):
            self.type = self.OCTAL
            self.valid = True
            self.value = int(text, 8)
        elif self.DECIMAL_RE.search(text):
            self.type = self.DECIMAL
            self.valid = True
            self.value = int(text[:-1])
        elif self.FLOAT_RE.search(text):
            self.type = self.FLOAT
            self.valid = True
            # TODO: Figure out how to handle floats.
            print >>sys.stderr, "Float formats not yet supported! (%s)" % text
        else:
            print >>sys.stderr, "Syntax error in number format (%s)" % text
            raise

    def isValid(self):
        return self.valid


# NOTE: Must be a new-style class.
class Instruction(object):
    
    def __init__(self, mnemonic, opcode, operandType):
        self.mnemonic = mnemonic
        self.opcode = opcode
        self.operandType = operandType

    def process(self, context, operand):
        if context.mode == OpcodeType.EXTENDED and opcode not in INSTRUCTIONS[context.arch][OpcodeType.EXTENDED]:
            context.error("missing EXTEND before extended instruction")
            sys.exit()
        self.__getattribute__("process_" + self.mnemonic)(operand)
        
    def process_AD(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_ADS(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_AUG(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_BZF(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_BZMF(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_CA(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_CAE(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_CAF(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_CCS(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_COM(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_CS(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_DAS(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_DCA(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_DCOM(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_DDOUBL(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_DIM(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_DOUBLE(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_DTCB(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_DTCF(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_DV(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_DXCH(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_EDRUPT(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_EXTEND(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_INCR(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_INDEX(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_INHINT(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_LXCH(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_MASK(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_MP(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_MSU(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_NDX(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_NOOP(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_OVSK(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_QXCH(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_RAND(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_READ(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_RELINT(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_RESUME(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_RETURN(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_ROR(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_RXOR(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_SQUARE(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_SU(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_TC(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_TCAA(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_TCF(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_TS(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_WAND(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_WOR(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_WRITE(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_XCH(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_XLQ(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_XXALQ(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_ZL(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def process_ZQ(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
# NOTE: Must be a new-style class.
class Directive(object):
    
    def __init__(self, name, mnemonic=None):
        if mnemonic:
            self.mnemonic = mnemonic
        else:
            self.mnemonic = name
        self.name = name
        
    def process(self, context, symbol, operand):
        self.__getattribute__("process_" + self.name)(context, symbol, operand)
        
    def process_Minus1_DNADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_Minus2_CADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_Minus2_DNADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_Minus3_DNADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_Minus4_DNADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_Minus5_DNADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_Minus6_DNADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_Minus_DNCHAN(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_Minus_DNPTR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_Minus_GENADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_1DNADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_2BCADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_2CADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_2DEC(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_2DEC_Star(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_2DNADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_2FCADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_2OCT(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_3DNADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_4DNADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_5DNADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_6DNADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_Equals_Sign(self, context, symbol, operand):
        if symbol:
            if operand:
                if operand.isdigit():
                    context.symtab.add(symbol, operand, int(operand, 8))
                else:
                    context.symtab.add(symbol, operand)
            else:
                context.symtab.add(symbol, operand, context.loc)
    
    def process_Equals_ECADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_Equals_MINUS(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_ADRES(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_BANK(self, context, symbol, operand):
        if operand:
            if operand.isdigit():
                bank = int(operand, 8)            
                context.fbank = bank
                context.loc = context.memmap.convertBankToPA(MemoryType.FIXED, bank, context.bankloc[bank])
            else:
                context.error("invalid syntax, \"%s\"" % operand)
        else:
            context.loc = context.memmap.convertBanktoPA(MemoryType.FIXED, context.fbank, context.bankloc[context.fbank])
    
    def process_BBCON(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_BBCON_Star(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_BLOCK(self, context, symbol, operand):
        if operand:
            if operand.isdigit():
                bank = int(operand, 8)
                if bank == 0:
                    context.ebank = bank
                    context.loc = context.memmap.convertBankToPA(MemoryType.ERASABLE, bank, context.bankloc[bank])
                else:
                    context.fbank = bank
                    context.loc = context.memmap.convertBankToPA(MemoryType.FIXED, bank, context.bankloc[bank])
            else:
                context.error("invalid syntax")
        else:
            context.error("invalid syntax")
    
    def process_BNKSUM(self, context, symbol, operand):
        context.info("ignoring BNKSUM directive")
    
    def process_CADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_CHECK_Equals(self, context, symbol, operand):
        if operand:
            fields = operand.split()
            defn = context.symtab.lookup(fields[0])
            if not defn:
                # Add to checklist and check at the end.
                context.checklist.append(SymbolTableEntry(context, symbol, operand))
            else:
                pa = defn.value
                if len(fields) > 1:
                    op = Number(fields[1].strip())
                    if op.isValid():
                        pa += op.value
                    else:
                        context.error("invalid expression, \"%s\"" % operand)
    
    def process_COUNT(self, context, symbol, operand):
        context.info("ignoring COUNT directive")
    
    def process_COUNT_Star(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_DEC(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_DEC_Star(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_DNCHAN(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_DNPTR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_EBANK_Equals(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_ECADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_EQUALS(self, context, symbol, operand):
        if symbol:
            if operand:
                if operand.isdigit():
                    context.symtab.add(symbol, operand, int(operand, 8))
                else:
                    context.symtab.add(symbol, operand)
            else:
                context.symtab.add(symbol, operand, context.loc)
    
    def process_ERASE(self, context, symbol, operand):
        size = 0
        if not operand:
            size = 1
            op = Number("1")
        else:
            if '-' in operand:
                op = Number(operand.split('-')[0].strip())
                if op.isValid():
                    size = op.value
            else:
                op = Number(operand)
                if op.isValid():
                    size = op.value + 1
        if symbol and op.isValid():
            context.symtab.add(symbol, operand, op.value)
        context.loc += size
        
    def process_FCADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_GENADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_MEMORY(self, context, symbol, operand):
        if '-' in operand:
            op1 = int(operand.split('-')[0], 8)
            op2 = int(operand.split('-')[1], 8)
            if symbol:
                context.symtab.add(symbol, operand, op1)
        else:
            context.error("syntax error: %s %s" % (self.mnemonic, operand))
    
    def process_MM(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_NV(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_OCT(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_OCTAL(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_REMADR(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()
    
    def process_SBANK_Equals(self, context, symbol, operand):
        context.warn("unsupported directive: %s %s" % (self.mnemonic, operand))
    
    def process_SETLOC(self, context, symbol, operand):
        if operand:
            if operand.isdigit():
                context.loc = int(operand, 8)
            else:
                if context.symtab.lookup(operand):
                    context.loc = context.symtab.lookup(operand)
        else:
            context.error("invalid syntax")
    
    def process_SUBRO(self, context, symbol, operand):
        context.info("ignoring BNKSUM directive")
    
    def process_VN(self, context, symbol, operand):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operand))
        sys.exit()


INSTRUCTIONS = { 
    Architecture.AGC4_B2 : {
        OpcodeType.BASIC: {
            "AD":     Instruction("AD",     060000,  OperandType.ERASABLE_12), 
            "CA":     Instruction("CA",     030000,  OperandType.GENERAL_12),
            "CAE":    Instruction("CAE",    030000,  OperandType.ERASABLE_12),
            "CAF":    Instruction("CAF",    030000,  OperandType.FIXED_12),
            "CCS":    Instruction("CCS",    010000,  OperandType.ERASABLE_10),
            "COM":    Instruction("COM",    040000,  OperandType.NONE),
            "CS":     Instruction("CS",     040000,  OperandType.GENERAL_12),
            "DAS":    Instruction("DAS",    020001,  OperandType.ERASABLE_10),
            "DDOUBL": Instruction("DDOUBL", 020001,  OperandType.NONE),
            "DOUBLE": Instruction("DOUBLE", 060000,  OperandType.NONE),
            "DTCB":   Instruction("DTCB",   052006,  OperandType.NONE),
            "DTCF":   Instruction("DTCF",   052005,  OperandType.NONE),
            "DV":     Instruction("DV",     010000,  OperandType.GENERAL_12),
            "DXCH":   Instruction("DXCH",   050001,  OperandType.ERASABLE_10),
            "EXTEND": Instruction("EXTEND", 000006,  OperandType.NONE),
            "INCR":   Instruction("INCR",   024000,  OperandType.NONE),
            "INDEX":  Instruction("INDEX",  050000,  OperandType.ERASABLE_10),
            "INHINT": Instruction("INHINT", 000004,  OperandType.NONE),
            "LXCH":   Instruction("LXCH",   022000,  OperandType.ERASABLE_10),
            "MASK":   Instruction("MASK",   070000,  OperandType.GENERAL_12),
            "MSK":    Instruction("MASK",   070000,  OperandType.GENERAL_12),
            "NDX":    Instruction("INDEX",  050000,  OperandType.ERASABLE_10),
            "NOOP":   Instruction("NOOP",   010000,  OperandType.NONE),           # TODO: For fixed memory only. Handle erasable case.
            "OVSK":   Instruction("OVSK",   054000,  OperandType.NONE),
            "RELINT": Instruction("RELINT", 000003,  OperandType.NONE),
            "RESUME": Instruction("RESUME", 050017,  OperandType.NONE),
            "RETURN": Instruction("RETURN", 000002,  OperandType.NONE),
            "TC":     Instruction("TC",     000000,  OperandType.GENERAL_12),
            "TCAA":   Instruction("TCAA",   054005,  OperandType.NONE),
            "TCF":    Instruction("TCF",    010000,  OperandType.FIXED_12),
            "TCR":    Instruction("TC",     000000,  OperandType.GENERAL_12),
            "TS":     Instruction("TS",     054000,  OperandType.ERASABLE_10),
            "XCH":    Instruction("XCH",    056000,  OperandType.ERASABLE_10),
            "XLQ":    Instruction("XLQ",    000001,  OperandType.NONE),
            "XXALQ":  Instruction("XXALQ",  000000,  OperandType.NONE),
            "ZL":     Instruction("ZL",     022007,  OperandType.NONE)
        }, 
        OpcodeType.EXTENDED: {
            "ADS":    Instruction("ADS",    026000,  OperandType.ERASABLE_10),
            "AUG":    Instruction("AUG",    024000,  OperandType.ERASABLE_10), 
            "BZF":    Instruction("BZF",    010000,  OperandType.FIXED_12),  
            "BZMF":   Instruction("BZMF",   060000,  OperandType.FIXED_12),
            "DCA":    Instruction("DCA",    030001,  OperandType.GENERAL_12),
            "DCOM":   Instruction("DCOM",   040001,  OperandType.NONE),
            "DIM":    Instruction("DIM",    026000,  OperandType.ERASABLE_10),
            "EDRUPT": Instruction("EDRUPT", 007000,  OperandType.FIXED_9),
            "INDEX":  Instruction("INDEX",  050000,  OperandType.GENERAL_12),
            "MP":     Instruction("MP",     070000,  OperandType.GENERAL_12),
            "MSU":    Instruction("MSU",    020000,  OperandType.ERASABLE_10),
            "NDX":    Instruction("INDEX",  050000,  OperandType.GENERAL_12),
            "QXCH":   Instruction("QXCH",   022000,  OperandType.ERASABLE_10),
            "RAND":   Instruction("RAND",   002000,  OperandType.CHANNEL),
            "READ":   Instruction("READ",   000000,  OperandType.CHANNEL),
            "ROR":    Instruction("ROR",    004000,  OperandType.CHANNEL),
            "RXOR":   Instruction("RXOR",   006000,  OperandType.CHANNEL),
            "SQUARE": Instruction("SQUARE", 070000,  OperandType.NONE),
            "SU":     Instruction("SU",     060000,  OperandType.ERASABLE_10),
            "WAND":   Instruction("WAND",   003000,  OperandType.CHANNEL),
            "WOR":    Instruction("WOR",    005000,  OperandType.CHANNEL),
            "WRITE":  Instruction("WRITE",  001000,  OperandType.CHANNEL),
            "ZQ":     Instruction("ZQ",     022007,  OperandType.NONE)
        }
    }
}


DIRECTIVES = {
    Architecture.AGC4_B2 : {
        "-1DNADR":  Directive("Minus1_DNADR", "-1DNADR"),
        "-2CADR":   Directive("Minus2_CADR",  "-2CADR"),
        "-2DNADR":  Directive("Minus2_DNADR", "-2DNADR"),
        "-3DNADR":  Directive("Minus3_DNADR", "-3DNADR"),
        "-4DNADR":  Directive("Minus4_DNADR", "-4DNADR"),
        "-5DNADR":  Directive("Minus5_DNADR", "-5DNADR"),
        "-6DNADR":  Directive("Minus6_DNADR", "-6DNADR"),
        "-DNCHAN":  Directive("Minus_DNCHAN", "-DNCHAN"),
        "-DNPTR":   Directive("Minus_DNPTR",  "-DNPTR"),
        "-GENADR":  Directive("Minus_GENADR", "-GENADR"),
        "1DNADR":   Directive("1DNADR"),
        "2BCADR":   Directive("2BCADR"),
        "2CADR":    Directive("2CADR"),
        "2DEC":     Directive("2DEC"),
        "2DEC*":    Directive("2DEC_Star",    "2DEC*"),
        "2DNADR":   Directive("2DNADR"),
        "2FCADR":   Directive("2FCADR"), 
        "2OCT":     Directive("2OCT"),
        "3DNADR":   Directive("3DNADR"),
        "4DNADR":   Directive("4DNADR"),
        "5DNADR":   Directive("5DNADR"),
        "6DNADR":   Directive("6DNADR"),
        "=":        Directive("Equals_Sign",  "="),
        "=ECADR":   Directive("Equals_ECADR", "=ECADR"),
        "=MINUS":   Directive("Equals_MINUS"  "=MINUS"),
        "ADRES":    Directive("ADRES"),
        "BANK":     Directive("BANK"),
        "BBCON":    Directive("BBCON"),
        "BBCON*":   Directive("BBCON_Star",   "BBCON*"),
        "BLOCK":    Directive("BLOCK"),
        "BNKSUM":   Directive("BNKSUM"),
        "CADR":     Directive("CADR"),
        "CHECK=":   Directive("CHECK_Equals", "CHECK="),
        "COUNT":    Directive("COUNT"),
        "COUNT*":   Directive("COUNT_Star",   "COUNT*"),
        "DEC":      Directive("DEC"),
        "DEC*":     Directive("DEC_Star",     "DEC*"),
        "DNCHAN":   Directive("DNCHAN"),
        "DNPTR":    Directive("DNPTR"),
        "EBANK=":   Directive("EBANK_Equals", "EBANK="),
        "ECADR":    Directive("ECADR"),
        "EQUALS":   Directive("EQUALS"),
        "ERASE":    Directive("ERASE"),
        "FCADR":    Directive("FCADR"),
        "GENADR":   Directive("GENADR"),
        "MEMORY":   Directive("MEMORY"),
        "MM":       Directive("MM"),
        "NV":       Directive("NV"),
        "OCT":      Directive("OCT"),
        "OCTAL":    Directive("OCTAL"),
        "REMADR":   Directive("REMADR"),
        "SBANK=":   Directive("SBANK_Equals", "SBANK="),
        "SETLOC":   Directive("SETLOC"),
        "SUBRO":    Directive("SUBRO"),
        "VN":       Directive("VN")
    }
}


class Assembler:
    """Class defining an AGC assembler."""

    class Context:
        def __init__(self, arch, listfile, binfile, verbose=False):
            self.verbose = verbose
            self.arch = arch
            self.listfile = listfile
            self.binfile = binfile
            self.srcfile = None
            self.source = []
            self.symtab = SymbolTable(self)
            self.code = {}
            self.linenum = 0
            self.global_linenum = 0
            self.mode = OpcodeType.BASIC
            self.memmap = MemoryMap(arch, verbose)
            self.checklist = []
            self.loc = 0
            self.bank = 0
            self.bankloc = {}
            for bank in range(len(self.memmap.memmap)):
                self.bankloc[bank] = 0

    def __init__(self, arch, listfile, binfile, verbose=False):
        self.verbose = verbose
        self.context = Assembler.Context(arch, listfile, binfile, verbose)
        self.context.error = self.error
        self.context.warn = self.warn
        self.context.info = self.info
        
    def assemble(self, srcfile):
        print "Assembling", srcfile
        self.context.srcfile = srcfile
        self.context.linenum = 0
        lines = open(srcfile).readlines()
        for line in lines:
            self.context.source.append(line.expandtabs(8))
            self.context.linenum += 1
            self.context.global_linenum += 1
            if line.startswith('$'):
                modname = line[1:].split()[0]
                if not os.path.isfile(modname):
                    print >>sys.stderr, "File \"%s\" does not exist" % modname
                    sys.exit(1)
                self.assemble(modname)
                continue
            if len(line.strip()) == 0:
                continue
            # Real parsing starts here.
            fields = line.split()
            label = None
            pseudolabel = None
            opcode = None
            operand = None
            comment = None
            if line.startswith('#'):
                comment = line
            else:
                if '#' in line:
                    comment = line[line.index('#'):]
                if not line.startswith(' ') and not line.startswith('\t'):
                    label = fields[0]
                    if len(fields) == 1:
                        # Label only.
                        self.context.symtab.add(label, None, loc)
                        continue
                    fields = fields[1:]
                else:
                    if line[1] == '+' or line[1] == '-':
                        pseudolabel = fields[0]
                        fields = fields[1:]
                # TODO: how to handle interpretive code?
                try:
                    opcode = fields[0]
                    operand = ""
                    for field in fields[1:]:
                        if field.startswith('#'):
                            break
                        operand += " " + field
                    if operand == "":
                        operand = None
                    else:
                        operand = operand.strip()
                    if opcode == "EXTEND":
                        self.context.mode = OpcodeType.EXTENDED
                    if opcode in DIRECTIVES[self.context.arch]:
                        DIRECTIVES[self.context.arch][opcode].process(self.context, label, operand)
                    if opcode in INSTRUCTIONS[self.context.arch]:
                        INSTRUCTIONS[self.context.arch][opcode][self.context.mode].process(self.context, operand)
                        self.context.mode = OpcodeType.BASIC
                except:
                    #self.context.symtab.printTable()
                    raise

    def error(self, text):
        print >>sys.stderr, "%s, line %d, error: %s" % (self.context.srcfile, self.context.linenum, text)

    def warn(self, text):
        print >>sys.stderr, "%s, line %d, warning: %s" % (self.context.srcfile, self.context.linenum, text)

    def info(self, text):
        if self.verbose:
            print >>sys.stderr, "%s, line %d, %s" % (self.context.srcfile, self.context.linenum, text)


def main():

    parser = OptionParser("usage: %prog [options] src_file [src_file...]")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose output.")
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("At least one source file must be supplied!")
        sys.exit(1)

    sources = []
    for arg in args:
        sources.append(arg)
        if not os.path.isfile(arg):
            parser.error("File \"%s\" does not exist" % arg)
            sys.exit(1)

    print "Simple AGC Assembler"
    print

    listfile = open(args[0].split('.')[0] + ".lst", 'w')
    binfile = open(args[0] + ".bin", 'wb')

    assembler = Assembler(Architecture.AGC4_B2, listfile, binfile, options.verbose)

    for arg in args:
        assembler.assemble(arg)

    
if __name__=="__main__":
    sys.exit(main())
