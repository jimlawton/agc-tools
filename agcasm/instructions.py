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

from architecture import *

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

# NOTE: Must be a new-style class.
class Instruction(object):
    
    def __init__(self, mnemonic, opcode, operandType, numwords=1):
        self.mnemonic = mnemonic
        self.opcode = opcode
        self.operandType = operandType
        self.numwords = numwords

    def parse(self, context, operand):
        if context.mode == OpcodeType.EXTENDED and opcode not in INSTRUCTIONS[context.arch][OpcodeType.EXTENDED]:
            context.error("missing EXTEND before extended instruction")
            sys.exit()
        if self.operandType == OperandType.NONE:
            context.code = self.opcode
        else:
            self.__getattribute__("parse_" + self.mnemonic)(operand)
        context.loc += self.numwords
        
    def parse_AD(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_ADS(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_AUG(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_BZF(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_BZMF(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_CA(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_CAE(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_CAF(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_CCS(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_COM(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_CS(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_DAS(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_DCA(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_DCOM(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_DDOUBL(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_DIM(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_DOUBLE(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_DTCB(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_DTCF(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_DV(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_DXCH(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_EDRUPT(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_EXTEND(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_INCR(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_INDEX(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_INHINT(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_LXCH(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_MASK(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_MP(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_MSU(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_NDX(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_NOOP(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_OVSK(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_QXCH(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_RAND(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_READ(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_RELINT(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_RESUME(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_RETURN(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_ROR(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_RXOR(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_SQUARE(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_SU(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_TC(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_TCAA(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_TCF(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_TS(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_WAND(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_WOR(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_WRITE(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_XCH(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_XLQ(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_XXALQ(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_ZL(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)
    
    def parse_ZQ(self, context, operand):
        sys.exit("Unsupported opcode: %s" % self.mnemonic)

    
INSTRUCTIONS = { 
    Architecture.AGC4_B2 : {
        # In AGC4 architecture, all instructions are single-word.
        OpcodeType.BASIC: {
            # Name                Mnemonic  Opcode   Operand
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
            # Name                Mnemonic  Opcode   Operand
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

