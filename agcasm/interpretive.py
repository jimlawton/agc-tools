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

from opcode import Opcode, OpcodeType
from record_type import RecordType
from expression import AddressExpression

# NOTE: Must be a new-style class.
class Interpretive(Opcode):
    
    def __init__(self, methodName, mnemonic, opcode, numOperands=1, switchcode=None):
        Opcode.__init__(self, methodName, mnemonic, opcode, None, False, None, 1)
        self.numOperands = numOperands
        self.switchcode = switchcode
        self.type = RecordType.INTERP

    def parse(self, context, operands):
        # Case 1: One interpretive opcode.
        # Case 2: Two packed interpretive opcodes.
        # Case 3: Interpretive opcode, simple operand.
        # Case 4: Interpretive opcode, operand expression with 2 components (e.g. ['A', '+1']).
        # Case 5: Interpretive opcode, operand expression with 3 components (e.g. ['A', '-', '1']).
        
        # TODO: Handle interpretive operands.
        # TODO: Handle store opcodes separately.
        # TODO: Handle interpretive operands ending in ,x. What does it mean?
        
        if operands:
            oplen = len(operands)
        else:
            oplen = 0
        opcodes = [ self.opcode ]
        
        operand = None
        if oplen == 0:
            # Case 1
            if self.numOperands > 0:
                context.interpArgs += self.numOperands
            pass
        elif oplen == 1:
            if operands[0] in context.opcodes[OpcodeType.INTERPRETIVE]:
                # Case 2
                opobj = context.opcodes[OpcodeType.INTERPRETIVE][operands[0]]
                opcodes.append(opobj.opcode)
        elif oplen == 2 or oplen == 3:
            operand = AddressExpression(context, operands)
        else:
            context.syntax("invalid operand expression")

        code = opcodes[0] * 0200 + 1
        if len(opcodes) == 2:
            code += opcodes[1] + 1
        else:
            if operand != None:
                code += operand.value & 077777
        code = ~code & 077777

        try:
            method = self.__getattribute__("parse_" + self.methodName)
        except:
            method = None
        if method:
            method(context, operands)

        context.currentRecord.code = [ code ]
        context.currentRecord.complete = True
        context.currentRecord.type = self.type
        context.incrLoc(self.numwords)
        context.interpMode = True

    @classmethod
    def parseOperand(cls, context, operands):
        if context.interpMode and context.interpArgs > 0:
            operand = AddressExpression(context, operands)
            if operand.complete:
                context.currentRecord.code = [ operand.value ]
                context.currentRecord.complete = True
            context.incrLoc(1)
            context.interpArgs -= 1
            if context.interpArgs == 0:
                context.interpMode = False
            return True
        return False

    def parse_EXIT(self, context, operands):
        context.interpMode = False
