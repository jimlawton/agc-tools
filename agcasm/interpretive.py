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
        nOpFields = oplen
        
        operand = None
        if nOpFields == 0:
            # Case 1
            pass
        elif nOpFields == 1:
            if operands[0] in context.opcodes[OpcodeType.INTERPRETIVE]:
                # Case 2
                opobj = context.opcodes[OpcodeType.INTERPRETIVE][operands[0]]
                opcodes.append(opobj.opcode)
        elif nOpFields == 2 or nOpFields == 3:
            operand = AddressExpression(context, operands)
        else:
            context.error("syntax error")

        code = opcodes[0] * 0200 + 1
        if len(opcodes) == 2:
            code += opcodes[1] + 1
        code = ~code & 077777

        try:
            self.__getattribute__("parse_" + self.methodName)(context, operands)
        except:
            pass

        context.currentRecord.code = [ code ]
        context.currentRecord.complete = True
        context.currentRecord.type = self.type
        context.incrLoc(self.numwords)
