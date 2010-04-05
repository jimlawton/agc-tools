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

from opcode import Opcode, OpcodeType, OperandType
from expression import Expression, AddressExpression

# NOTE: Must be a new-style class.
class Instruction(Opcode):
    
    def __init__(self, methodName, opcode, operandType=OperandType.NONE, addressType=None, numwords=1):
        Opcode.__init__(self, methodName, methodName, opcode, operandType, addressType, numwords)

    def parse(self, context, operands):
        retval = True
        if self.operandType == OperandType.NONE:
            if operands != None:
                context.error("instruction takes no operand")
            else:
                context.currentRecord.code = [ self.opcode ]
                context.currentRecord.complete = True
        else:
            if operands == None:
                context.error("missing operand")
            else:
                pa = None
                if operands:
                    expr = AddressExpression(context, operands)
                    if expr.complete:
                        pa = expr.value
                        (bank, offset) = context.memmap.pseudoToSegmented(pa)
                        context.currentRecord.code = [ self.opcode + offset ]
                        context.currentRecord.complete = True
                else:
                    context.error("missing operand")
                parser = self.__getattribute__("parse_" + self.mnemonic)
                if parser:
                    parser(context, operands)
        context.loc += self.numwords
        return retval
    
    def parse_AD(self, context, operands):
        pass

    def parse_ADS(self, context, operands):
        pass
    
    def parse_AUG(self, context, operands):
        pass
    
    def parse_BZF(self, context, operands):
        pass
    
    def parse_BZMF(self, context, operands):
        pass
    
    def parse_CA(self, context, operands):
        pass
    
    def parse_CAE(self, context, operands):
        pass
    
    def parse_CAF(self, context, operands):
        pass
    
    def parse_CCS(self, context, operands):
        pass
    
    def parse_CS(self, context, operands):
        pass
    
    def parse_DAS(self, context, operands):
        pass
    
    def parse_DCA(self, context, operands):
        pass
    
    def parse_DIM(self, context, operands):
        pass
    
    def parse_DV(self, context, operands):
        pass
    
    def parse_DXCH(self, context, operands):
        pass
    
    def parse_EDRUPT(self, context, operands):
        pass
    
    def parse_EXTEND(self, context, operands):
        context.mode = OpcodeType.EXTENDED
    
    def parse_INCR(self, context, operands):
        pass
    
    def parse_INDEX(self, context, operands):
        pass
    
    def parse_LXCH(self, context, operands):
        pass
    
    def parse_MASK(self, context, operands):
        pass
    
    def parse_MP(self, context, operands):
        pass
    
    def parse_MSU(self, context, operands):
        pass
    
    def parse_NDX(self, context, operands):
        pass
    
    def parse_QXCH(self, context, operands):
        pass
    
    def parse_RAND(self, context, operands):
        pass
    
    def parse_READ(self, context, operands):
        pass
    
    def parse_ROR(self, context, operands):
        pass
    
    def parse_RXOR(self, context, operands):
        pass
    
    def parse_SU(self, context, operands):
        pass
    
    def parse_TC(self, context, operands):
        pass
    
    def parse_TCF(self, context, operands):
        pass
    
    def parse_TS(self, context, operands):
        pass
    
    def parse_WAND(self, context, operands):
        pass
    
    def parse_WOR(self, context, operands):
        pass
    
    def parse_WRITE(self, context, operands):
        pass
    
    def parse_XCH(self, context, operands):
        pass
