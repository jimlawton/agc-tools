#!/usr/bin/env python

# Copyright 2010 Jim lawton <jim dot lawton at gmail dot com>
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
    AGC2C   = 1    # Mod2C
    AGC3    = 2    # AGC3
    AGC4_B1 = 3    # AGC4 Block I
    AGC4_B2 = 4    # AGC4 Block II

class MemoryType:
    ERASABLE = 0
    FIXED    = 1

class ErasableMemoryType:
    UNSWITCHED = 0
    SWITCHED   = 1


BANKS = {
    # Each entry contains (start_address, size, number)
    MemoryType.ERASABLE: {
        Architecture.AGC4_B1: (0, 0400, 0),    # TODO: number of erasable banks in Block I 
        Architecture.AGC4_B2: (0, 0400, 8)
    },
    MemoryType.FIXED: {
        Architecture.AGC4_B1: (02000, 02000, 24), 
        Architecture.AGC4_B2: (02000, 02000, 36)
    }    
}


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
    def __init__(self, name=None, symbolic=None, value=-1):
        self.name = name
        self.symbolic = symbolic
        self.value = value

    def __str__(self):
        text = "(%8s, "  % (self.name)
        if self.symbolic:
            text += "\"%-30s\", "  % (self.symbolic)
        else:
            text += "%-32s, " % ("None")
        if self.value == -1:
            text += "UNDEFINED)"
        else:
            text += "%06o)" % (self.value)
        return text


def parseNumber(text):
    # TODO: make sure it's a number
    
    if text.endswith('D'):
        number = int(text[:-1])
    else:
        number = int(text, 8)
    return number


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
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_Minus2_CADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_Minus2_DNADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_Minus3_DNADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_Minus4_DNADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_Minus5_DNADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_Minus6_DNADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_Minus_DNCHAN(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_Minus_DNPTR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_Minus_GENADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_1DNADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_2BCADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_2CADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_2DEC(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_2DEC_Star(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_2DNADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_2FCADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_2OCT(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_3DNADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_4DNADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_5DNADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_6DNADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_Equals_Sign(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_Equals_ECADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_Equals_MINUS(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_ADRES(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_BANK(self, context, symbol, operand):
        if operand:
            if operand.isdigit():
                bank = int(operand, 8)            
                context.fbank = bank
                context.loc = (bank * 02000) + context.fbankloc[bank]
            else:
                context.error("Invalid syntax")
        else:
            context.loc = (context.fbank * 02000) + context.fbankloc[context.fbank]
    
    def process_BBCON(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_BBCON_Star(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_BLOCK(self, context, symbol, operand):
        if operand:
            if operand.isdigit():
                bank = int(operand, 8)
                if bank == 0:
                    context.ebank = bank
                    context.loc = (bank * 0400) + context.ebankloc[bank]
                else:
                    context.fbank = bank
                    context.loc = (bank * 02000) + context.fbankloc[bank]
            else:
                context.error("Invalid syntax")
        else:
            context.error("Invalid syntax")
    
    def process_BNKSUM(self, context, symbol, operand):
        context.info("ignoring BNKSUM directive")
    
    def process_CADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_CHECK_Equals(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_COUNT(self, context, symbol, operand):
        context.info("ignoring COUNT directive")
    
    def process_COUNT_Star(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_DEC(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_DEC_Star(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_DNCHAN(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_DNPTR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_EBANK_Equals(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_ECADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_EQUALS(self, context, symbol, operand):
        if operand:
            if operand.isdigit():
                context.symtab[symbol] = SymbolTableEntry(symbol, operand, int(operand, 8))
            else:
                context.symtab[symbol] = SymbolTableEntry(symbol, operand)
        else:
            context.symtab[symbol] = SymbolTableEntry(symbol, operand, context.loc)
            context.loc += 1
    
    def process_ERASE(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_FCADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_GENADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_MEMORY(self, context, symbol, operand):
        if '-' in operand:
            op1 = int(operand.split('-')[0], 8)
            op2 = int(operand.split('-')[1], 8)
            if symbol:
                context.symtab[symbol] = SymbolTableEntry(symbol, operand, op1)
        else:
            context.error("syntax error: %s %s" % (self.mnemonic, self.operand))
    
    def process_MM(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_NV(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_OCT(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_OCTAL(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_REMADR(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_SBANK_Equals(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_SETLOC(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_SUBRO(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)
    
    def process_VN(self, context, symbol, operand):
        sys.exit("Unsupported directive: %s" % self.mnemonic)


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
        def __init__(self, arch, listfile, binfile):
            self.arch = arch
            self.listfile = listfile
            self.binfile = binfile
            self.srcfile = None
            self.source = []
            self.symtab = {}
            self.code = {}
            self.linenum = 0
            self.global_linenum = 0
            self.mode = OpcodeType.BASIC
            self.loc = 0
            self.bank = 0
            self.ebankloc = {}
            for bank in range(BANKS[MemoryType.ERASABLE][arch][2]):
                self.ebankloc[bank] = 0
            self.fbankloc = {}
            for bank in range(BANKS[MemoryType.FIXED][arch][2]):
                self.fbankloc[bank] = 0

    def __init__(self, arch, listfile, binfile):
        self.context = Assembler.Context(arch, listfile, binfile)
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
                        self.context.symtab[label] = SymbolTableEntry(label, None, loc)
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
                        operand += field
                    if operand == "":
                            operand = None
                    if opcode == "EXTEND":
                        self.context.mode = OpcodeType.EXTENDED
                    if opcode in DIRECTIVES[self.context.arch]:
                        DIRECTIVES[self.context.arch][opcode].process(self.context, label, operand)
                    if opcode in INSTRUCTIONS[self.context.arch]:
                        INSTRUCTIONS[self.context.arch][opcode][self.context.mode].process(self.context, operand)
                except:
                    symbols = self.context.symtab.keys()
                    symbols.sort()
                    for symbol in symbols:
                        print self.context.symtab[symbol]
                    raise

    def error(self, text):
        print >>sys.stderr, "%s, line %d, error: %s" % (self.context.srcfile, self.context.linenum, text)

    def warn(self, text):
        print >>sys.stderr, "%s, line %d, warning: %s" % (self.context.srcfile, self.context.linenum, text)

    def info(self, text):
        print >>sys.stderr, "%s, line %d, %s" % (self.context.srcfile, self.context.linenum, text)


def main():

    parser = OptionParser("usage: %prog [options] src_file [src_file...]")
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

    assembler = Assembler(Architecture.AGC4_B2, listfile, binfile)

    for arg in args:
        assembler.assemble(arg)

    
if __name__=="__main__":
    sys.exit(main())
