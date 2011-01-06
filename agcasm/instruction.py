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
from memory import AddressType

# NOTE: Must be a new-style class.
class Instruction(Opcode):

    def __init__(self, methodName, opcode, operandType=OperandType.NONE, addressType=None, numwords=1):
        Opcode.__init__(self, methodName, methodName, opcode, operandType, False, addressType, numwords)
        self.type = RecordType.EXEC

    def parse(self, context, operands):
        if context.mode == OpcodeType.EXTENDED and self.mnemonic not in context.opcodes[OpcodeType.EXTENDED]:
            context.error("missing EXTEND before extended instruction")
            return
        if self.operandType == OperandType.NONE:
            if operands != None:
                context.error("instruction takes no operand")
            else:
                context.currentRecord.code = [ self.opcode ]
                context.currentRecord.operandType = RecordType.NONE
                context.currentRecord.complete = True
        else:
            if operands == None:
                context.error("missing operand")
            else:
                if operands:
                    expr = AddressExpression(context, operands)
                    if expr.complete:
                        pa = expr.value
                        if pa < 0:
                            # Negative, relative address.
                            if self.mnemonic == "TC":
                                pa -= 1
                            context.currentRecord.code = [ (self.opcode + pa) & 077777 ]
                        else:
                            if context.debug:
                                context.currentRecord.target = expr.value
                            address = context.memmap.pseudoToAddress(pa)
                            if self.addressType == AddressType.FIXED_9:
                                if context.memmap.isFixed(expr.value) or context.previousWasIndex == True:
                                    address &= 0777
                                else:
                                    context.error("Address must be in fixed memory")
                            elif self.addressType == AddressType.FIXED_12:
                                if context.memmap.isFixed(expr.value) or context.previousWasIndex == True:
                                    address &= 07777
                                else:
                                    context.error("Address must be in fixed memory")
                            elif self.addressType == AddressType.ERASABLE_10:
                                if context.memmap.isErasable(expr.value) or context.previousWasIndex == True:
                                    address &= 01777
                                else:
                                    context.error("Address must be in erasable memory")
                            elif self.addressType == AddressType.ERASABLE_12:
                                if context.memmap.isErasable(expr.value) or context.previousWasIndex == True:
                                    address &= 07777
                                else:
                                    context.error("Address must be in erasable memory")
                            elif self.addressType == AddressType.GENERAL_12:
                                address &= 07777
                            elif self.addressType == AddressType.CHANNEL:
                                address &= 0777
                            else:
                                context.error("Invalid address type")
                            context.currentRecord.code = [ (self.opcode + address) & 077777 ]
                        context.currentRecord.operandType = expr.refType
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

        if self.mnemonic != "INDEX" and context.previousWasIndex:
            context.previousWasIndex = False

        if context.currentRecord.complete:
            if self.numwords == 1:
                context.log(5, "generated code %05o" % (context.currentRecord.code[0]))
            else:
                context.log(5, "generated code %05o %05o" % (context.currentRecord.code[0], context.currentRecord.code[1]))

    def parse_EXTEND(self, context, operands):
        context.mode = OpcodeType.EXTENDED

    def parse_INDEX(self, context, operands):
        context.previousWasIndex = True

    def parse_MinusCCS(self, context, operands):
        words = []
        if context.currentRecord.code != None:
            for i in range(len(context.currentRecord.code)):
                words.append(~context.currentRecord.code[i] & 077777)
            context.currentRecord.code = words
            context.currentRecord.complete = True

    def parse_NOOP(self, context, operands):
        if context.memmap.isErasable(context.loc):
            # Equivalent to "CA A".
            word = context.opcodes[OpcodeType.BASIC]["CA"].opcode
        else:
            # Equivalent to "TCF +1".
            word = context.memmap.pseudoToAddress(context.loc + 1)
        context.currentRecord.code = [ self.opcode + word ]
        context.currentRecord.complete = True
