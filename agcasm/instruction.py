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

import sys
from architecture import *
from opcode import *

# NOTE: Must be a new-style class.
class Instruction(Opcode):
    
    def __init__(self, methodName, opcode, operandType, numwords=1):
        Opcode.__init__(self, methodName, methodName, opcode, operandType, numwords)

    def parse(self, context, operand):
        if self.operandType == OperandType.NONE:
            context.code = [ self.opcode ]
        else:
            self.__getattribute__("parse_" + self.mnemonic)(context, operand)
            pass
        context.loc += self.numwords
        
    def parse_AD(self, context, operand):
        pass
    
    def parse_ADS(self, context, operand):
        pass
    
    def parse_AUG(self, context, operand):
        pass
    
    def parse_BZF(self, context, operand):
        pass
    
    def parse_BZMF(self, context, operand):
        pass
    
    def parse_CA(self, context, operand):
        pass
    
    def parse_CAE(self, context, operand):
        pass
    
    def parse_CAF(self, context, operand):
        pass
    
    def parse_CCS(self, context, operand):
        pass
    
    def parse_COM(self, context, operand):
        pass
    
    def parse_CS(self, context, operand):
        pass
    
    def parse_DAS(self, context, operand):
        pass
    
    def parse_DCA(self, context, operand):
        pass
    
    def parse_DCOM(self, context, operand):
        pass
    
    def parse_DDOUBL(self, context, operand):
        pass
    
    def parse_DIM(self, context, operand):
        pass
    
    def parse_DOUBLE(self, context, operand):
        pass
    
    def parse_DTCB(self, context, operand):
        pass
    
    def parse_DTCF(self, context, operand):
        pass
    
    def parse_DV(self, context, operand):
        pass
    
    def parse_DXCH(self, context, operand):
        pass
    
    def parse_EDRUPT(self, context, operand):
        pass
    
    def parse_EXTEND(self, context, operand):
        context.mode = OpcodeType.EXTENDED
    
    def parse_INCR(self, context, operand):
        pass
    
    def parse_INDEX(self, context, operand):
        pass
    
    def parse_INHINT(self, context, operand):
        pass
    
    def parse_LXCH(self, context, operand):
        pass
    
    def parse_MASK(self, context, operand):
        pass
    
    def parse_MP(self, context, operand):
        pass
    
    def parse_MSU(self, context, operand):
        pass
    
    def parse_NDX(self, context, operand):
        pass
    
    def parse_NOOP(self, context, operand):
        pass
    
    def parse_OVSK(self, context, operand):
        pass
    
    def parse_QXCH(self, context, operand):
        pass
    
    def parse_RAND(self, context, operand):
        pass
    
    def parse_READ(self, context, operand):
        pass
    
    def parse_RELINT(self, context, operand):
        pass
    
    def parse_RESUME(self, context, operand):
        pass
    
    def parse_RETURN(self, context, operand):
        pass
    
    def parse_ROR(self, context, operand):
        pass
    
    def parse_RXOR(self, context, operand):
        pass
    
    def parse_SQUARE(self, context, operand):
        pass
    
    def parse_SU(self, context, operand):
        pass
    
    def parse_TC(self, context, operand):
        pass
    
    def parse_TCAA(self, context, operand):
        pass
    
    def parse_TCF(self, context, operand):
        pass
    
    def parse_TS(self, context, operand):
        pass
    
    def parse_WAND(self, context, operand):
        pass
    
    def parse_WOR(self, context, operand):
        pass
    
    def parse_WRITE(self, context, operand):
        pass
    
    def parse_XCH(self, context, operand):
        pass
    
    def parse_XLQ(self, context, operand):
        pass
    
    def parse_XXALQ(self, context, operand):
        pass
    
    def parse_ZL(self, context, operand):
        pass
    
    def parse_ZQ(self, context, operand):
        pass

