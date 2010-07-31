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
        self.complement = True          # Default is to complement the generated code.

    def parse(self, context, operands):
        # Case 1: One interpretive opcode.
        # Case 2: Two packed interpretive opcodes.
        # Case 3: Interpretive opcode, simple operand.
        # Case 4: Interpretive opcode, operand expression with 2 components (e.g. ['A', '+1']).
        # Case 5: Interpretive opcode, operand expression with 3 components (e.g. ['A', '-', '1']).

        # TODO: Handle interpretive operands.
        # TODO: Handle store opcodes separately.
        # TODO: Handle interpretive operands ending in ,x. What does it mean?

        exitInterp = False

        if self.mnemonic == "EXIT":
            exitInterp = True

        mnemonic2 = None

        if operands != None:
            oplen = len(operands)
        else:
            oplen = 0
        opcodes = [ self.opcode ]

        if oplen == 0:
            context.log(5, "interpretive: %s (%03o)" % (self.mnemonic, self.opcode))
            # Case 1
            if self.numOperands > 0:
                context.log(5, "incrementing interpArgs: %d -> %d" % (context.interpArgs, context.interpArgs + self.numOperands))
                context.interpArgs += self.numOperands
        elif oplen == 1:
            if operands[0] in context.opcodes[OpcodeType.INTERPRETIVE]:
                # Case 2
                mnemonic2 = operands[0]
                opobj = context.opcodes[OpcodeType.INTERPRETIVE][operands[0]]
                context.log(5, "interpretive: %s (%03o), %s (%03o)" % (self.mnemonic, self.opcode, opobj.mnemonic, opobj.opcode))
                opcodes.append(opobj.opcode)
        elif oplen == 2 or oplen == 3:
            pass
        else:
            context.syntax("invalid operand expression")

        if self.methodName.endswith('*'):
            context.indexed = True

        context.currentRecord.code = None

        gotone = False
        if oplen == 2 or oplen == 3:
            gotone = Interpretive.parseOperand(context, operands)

        try:
            method = self.__getattribute__("parse_" + self.methodName)
        except:
            method = None
        if method:
            method(context, operands)

        if mnemonic2 != None:
            try:
                method = self.__getattribute__("parse_" + opobj.methodName)
            except:
                method = None
            if method:
                operands = operands[1:]
                method(context, operands)
            if mnemonic2 == "EXIT":
                exitInterp = True

        code = opcodes[0] + 1
        if len(opcodes) == 2:
            code += (opcodes[1] + 1) * 0200
            context.log(5, "interpretive: opcodes %03o %03o" % (opcodes[0], opcodes[1]))
        else:
            context.log(5, "interpretive: opcode %03o" % (opcodes[0]))
            if gotone:
                operandcode = context.currentRecord.code[0]
                context.log(5, "interpretive: operand %05o" % (operandcode))
                code += operandcode & 077777

        context.log(5, "interpretive: generated %05o (%03o,%03o)" % (~code & 077777, (code / 0200) & 0177, code & 0177))

        if self.complement:
            code = ~code & 077777

        context.currentRecord.code = [ code ]
        context.currentRecord.complete = True
        context.currentRecord.type = self.type

        if oplen != 2 and oplen != 3:
            # If any operands found, parseOperand will already have done this.
            context.incrLoc(self.numwords)

        if exitInterp == True:
            context.interpMode = False
            context.interpArgs = 0
        else:
            context.interpMode = True

    @classmethod
    def parseOperand(cls, context, operands):
        context.log(5, "interpretive: trying to parse operand %s" % operands)
        newoperands = []
        indexreg = 0
        for operand in operands:
            if operand.endswith(',1') or operand.endswith(',2'):
                context.log(5, "interpretive: indexed operand %s" % operand)
                if operand.endswith(',1'):
                    indexreg = 1
                else:
                    indexreg = 2
                newoperands.append(operand[:-2])
            else:
                newoperands.append(operand)
        operand = AddressExpression(context, newoperands)
        if operand.complete:
            code = context.memmap.pseudoToInterpretiveAddress(operand.value)
            if indexreg > 0:
                code += 1
                if indexreg == 2:
                    code = ~code & 077777
            context.currentRecord.code = [ code ]
            context.currentRecord.complete = True
            context.log(5, "interpretive: generated operand %05o" % code)
        else:
            context.log(5, "interpretive: operand undefined")
        context.incrLoc(1)
        context.interpArgs -= 1

    def parse_EXIT(self, context, operands):
        context.interpMode = False

    def parse_Store(self, context, operands):
        self.complement = False
