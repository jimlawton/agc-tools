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
from expression import AddressExpression, ExpressionType

class InterpretiveType:
    NORMAL = 0
    SWITCH = 1
    SHIFT  = 2

class PackingType:
    "Specifies the packing type of a line of interpretive code, i.e. whether a left word only, right word only, or a packed pair (2 opcodes, or opcode/operand)."
    OPCODE_ONLY    = 0  # Left.
    OPERAND_ONLY   = 1  # Right.
    OPCODE_PAIR    = 2  # Pair.
    OPCODE_OPERAND = 3  # Pair.

# NOTE: Must be a new-style class.
class Interpretive(Opcode):

    def __init__(self, methodName, mnemonic, opcode, numOperands=1, interpType=InterpretiveType.NORMAL, switchcode=None):
        Opcode.__init__(self, methodName, mnemonic, opcode, None, False, None, 1)
        self.numOperands = numOperands
        self.switchcode = switchcode
        self.type = RecordType.INTERP
        self.interpType = interpType
        self.complement = True          # Default is to complement the generated code.

    def parse(self, context, operands):
        # Case 1: One interpretive opcode.
        # Case 2: Two packed interpretive opcodes.
        # Case 3: Interpretive opcode, simple operand.
        # Case 4: Interpretive opcode, operand expression with 2 components (e.g. ['A', '+1']).
        # Case 5: Interpretive opcode, operand expression with 3 components (e.g. ['A', '-', '1']).

        exitInterp = False
        numArgs = self.numOperands

        context.interpArgs = 0
        context.interpArgCount = 0
        context.interpArgTypes = [ None, None, None, None ]
        context.interpArgCodes = [ 0, 0, 0, 0 ]

        if self.mnemonic == "EXIT":
            exitInterp = True

        mnemonic2 = None

        if operands != None:
            oplen = len(operands)
        else:
            oplen = 0
        opcodes = [ self.opcode ]

        checkForOperand = False
        if oplen == 0:
            # Case 1
            context.currentRecord.packingType = PackingType.OPCODE_ONLY
            context.log(5, "interpretive: %s (%03o)" % (self.mnemonic, self.opcode))
        elif oplen == 1:
            if operands[0] in context.opcodes[OpcodeType.INTERPRETIVE]:
                # Case 2
                context.currentRecord.packingType = PackingType.OPCODE_PAIR
                mnemonic2 = operands[0]
                opobj = context.opcodes[OpcodeType.INTERPRETIVE][operands[0]]
                context.log(5, "interpretive: %s (%03o), %s (%03o)" % (self.mnemonic, self.opcode, opobj.mnemonic, opobj.opcode))
                opcodes.append(opobj.opcode)
                numArgs2 = opobj.numOperands
            else:
                context.currentRecord.packingType = PackingType.OPCODE_OPERAND
                checkForOperand = True
        elif oplen == 2 or oplen == 3:
            context.currentRecord.packingType = PackingType.OPCODE_OPERAND
            pass
        else:
            context.syntax("invalid operand expression")

        if self.methodName.endswith('*'):
            context.indexed = True

        context.currentRecord.code = None

        if numArgs > 0:
            if context.interpArgs < 4:
                if (context.interpArgs + numArgs) <= 4:
                    context.log(5, "interpretive: incrementing interpArgs, %d -> %d" % (context.interpArgs, context.interpArgs + numArgs))
                    context.interpArgs += numArgs
                else:
                    context.log(5, "interpretive: incrementing interpArgs, %d -> %d" % (context.interpArgs, 4))
                    context.interpArgs = 4

        if oplen == 2 or oplen == 3 or checkForOperand == True:
            Interpretive._parseOperand(context, operands, checkForOperand)

        try:
            method = self.__getattribute__("parse_" + self.methodName)
        except:
            method = None
        if method:
            method(context, operands)

        if mnemonic2 != None:
            if numArgs2 > 0:
                if context.interpArgs < 4:
                    if (context.interpArgs + numArgs2) <= 4:
                        context.log(5, "interpretive: incrementing interpArgs, %d -> %d" % (context.interpArgs, context.interpArgs + numArgs2))
                        context.interpArgs += numArgs2
                    else:
                        context.log(5, "interpretive: incrementing interpArgs, %d -> %d" % (context.interpArgs, 4))
                        context.interpArgs = 4
            try:
                method = opobj.__getattribute__("parse_" + opobj.methodName)
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
            if context.currentRecord.code:
                operandcode = context.currentRecord.code[0]
                context.log(5, "interpretive: operand %05o" % (operandcode))
                code = (opcodes[0] + operandcode) & 077777

        context.log(5, "interpretive: generated %05o (%03o,%03o)" % (code & 077777, (code / 0200) & 0177, code & 0177))

        if self.complement or (context.complementNext and checkForOperand):
            code = ~code & 077777
            context.log(5, "interpretive: complemented to %05o " % (code))
            if (context.complementNext and checkForOperand):
                context.complementNext = False

        context.currentRecord.code = [ code ]
        context.currentRecord.complete = True
        context.currentRecord.type = self.type

        if oplen != 2 and oplen != 3:
            # If any operands found, parseOperand will already have done this.
            context.incrLoc(self.numwords)

        if exitInterp == True:
            context.interpMode = False
        else:
            context.interpMode = True

    @classmethod
    def _parseOperand(cls, context, operands, store=False):
        context.log(5, "interpretive: trying to parse operand %d %s" % (context.interpArgCount, operands))
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
            context.currentRecord.target = operand.value
            code = context.memmap.pseudoToInterpretiveAddress(operand.value)
            acindex = context.interpArgCount
            if context.interpArgTypes[acindex] != None:
                # Switch or shift operand.
                if context.interpArgTypes[acindex] == InterpretiveType.SWITCH:
                    context.log(5, "interpretive: switch operand value=%05o [%d] %05o" % (code, acindex, context.interpArgCodes[acindex]))
                    context.currentRecord.argcode = context.interpArgCodes[acindex]
                    # Switch operands use the encoding 0WWWWWWNNNNBBBB, where:
                    #  WWWWWW (6 bits) is the quotient when the constant value is divided by 15.
                    #  BBBB (4 bits) is the remainder when the constant value is divided by 15.
                    #  NNNN is an operation-specific value (all switch operations share the same opcode).
                    flag = (code / 15) & 077
                    bit = (code % 15)
                    code = (flag << 8) | bit | (context.currentRecord.argcode << 4)
                    context.log(5, "interpretive: switch operand flag=%03o bit=%02o code=%05o" % (flag, bit, code))
                else:
                    context.log(5, "interpretive: shift operand value=%05o [%d] %05o" % (code, acindex, context.interpArgCodes[acindex]))
                    context.currentRecord.argcode = context.interpArgCodes[acindex]
                    code |= (context.interpArgCodes[acindex] << 2)
            else:
                if context.memmap.isErasable(operand.value):
                    code += 1
                if operand.length > 1:
                    code += operand.length - 1
                if indexreg == 2 or (context.complementNext and not store):
                    code = ~code & 077777
                    if (context.complementNext and not store):
                        context.complementNext = False
            context.currentRecord.code = [ code ]
            context.currentRecord.complete = True
            context.log(5, "interpretive: generated operand %05o" % code)
        else:
            context.log(5, "interpretive: operand undefined")
        if not store:
            context.incrLoc(1)

        if context.interpArgCount < 4:
            context.log(5, "interpretive: incrementing interpArgCount, %d -> %d" % (context.interpArgCount, context.interpArgCount + 1))
            context.interpArgCount += 1
        if context.interpArgCount == context.interpArgs:
            context.log(5, "interpretive: all args found, resetting interpArgs, %d -> %d" % (context.interpArgs, 0))
            context.interpArgs = 0
            context.interpArgCount = 0

    @classmethod
    def parseOperand(cls, context, operands, store=False):
        context.currentRecord.packingType = PackingType.OPERAND_ONLY
        cls._parseOperand(context, operands, store)
        context.currentRecord.type = RecordType.INTERP

    def parse_EXIT(self, context, operands):
        context.interpMode = False

    def parse_Store(self, context, operands):
        self.complement = False

    def parse_STADR(self, context, operands):
        context.complementNext = True
        context.log(5, "interpretive: STADR, decrementing interpArgs, %d -> %d" % (context.interpArgs, context.interpArgs - 1))

    def parse_Switch(self, context, operands):
        # Store argcode in appropriate slot in context.interpArgCodes.
        context.log(5, "interpretive: switch, %d operands" % (self.numOperands))
        if self.numOperands == 2:
            acindex = context.interpArgs - 2
        else:
            acindex = context.interpArgs - 1
        context.interpArgCodes[acindex] = self.switchcode
        context.interpArgTypes[acindex] = InterpretiveType.SWITCH
        context.log(5, "interpretive: switch detected, [%d]=%05o" % (acindex, context.interpArgCodes[acindex]))

    def parse_Shift(self, context, operands):
        # Store argcode in appropriate slot in context.interpArgCodes.
        acindex = context.interpArgs - 1
        context.interpArgCodes[acindex] = self.switchcode
        context.interpArgTypes[acindex] = InterpretiveType.SHIFT
        context.log(5, "interpretive: shift detected, [%d]=%05o" % (acindex, context.interpArgCodes[acindex]))

