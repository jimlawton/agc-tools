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
from expression import AddressExpression
from record_type import RecordType

# NOTE: Must be a new-style class.
class Instruction(Opcode):
    
    def __init__(self, methodName, opcode, operandType=OperandType.NONE, addressType=None, numwords=1):
        Opcode.__init__(self, methodName, methodName, opcode, operandType, False, addressType, numwords)
        self.type = RecordType.EXEC

    def parse(self, context, operands):
        if context.mode == OpcodeType.EXTENDED and self.mnemonic not in context.opcodes[OpcodeType.EXTENDED]:
            self.context.error("missing EXTEND before extended instruction")
            return
        if self.operandType == OperandType.NONE:
            if operands != None:
                context.error("instruction takes no operand")
            else:
                context.currentRecord.code = [ self.opcode ]
                context.currentRecord.complete = True
        else:
            if operands == None:
                if self.mnemonic == "TC" or self.mnemonic == "DV":
                    # FIXME: remove this hack?
                    # HACK: TC and DV are also used as labels in interpretive code.
                    expr = AddressExpression(context, [ self.mnemonic ])
                    if expr.complete:
                        context.currentRecord.code = [ context.memmap.pseudoToAddress(expr.value) ]
                        context.currentRecord.complete = True
                        context.currentRecord.type = self.type
                        context.incrLoc(self.numwords)
                        return
                else:
                    context.error("missing operand")
            else:
                pa = None
                if operands:
                    expr = AddressExpression(context, operands)
                    if expr.complete:
                        address = context.memmap.pseudoToAddress(expr.value)
                        context.log(6, "converted pa %06o to address %05o" % (expr.value, address))
                        context.currentRecord.code = [ self.opcode + address ]
                        context.currentRecord.complete = True
                else:
                    context.error("missing operand")
                
        try:
            method = self.__getattribute__("parse_" + self.methodName)
        except:
            method = None
        if method:
            method(context, operands)

        context.currentRecord.type = self.type
        context.incrLoc(self.numwords)

        if context.mode == OpcodeType.EXTENDED:
            if self.mnemonic != "EXTEND" and self.mnemonic != "INDEX": 
                context.mode = OpcodeType.BASIC
    
    def parse_EXTEND(self, context, operands):
        context.mode = OpcodeType.EXTENDED
    
    def parse_MinusCCS(self, context, operands):
        words = []
        if context.currentRecord.code != None:
            for i in range(len(context.currentRecord.code)):
                words.append(~context.currentRecord.code[i] & 077777)
            context.currentRecord.code = words
            context.currentRecord.complete = True
        