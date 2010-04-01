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
from opcodes import *

# NOTE: Must be a new-style class.
class Instruction(Opcode):
    
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

