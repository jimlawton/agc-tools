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

from memory import AddressType

class OpcodeType:
    BASIC        = 0
    EXTENDED     = 1
    DIRECTIVE    = 2
    INTERPRETIVE = 3

class OperandType:
    NONE         = 0    # No operand.
    OCTAL        = 1    # Octal constant.
    DECIMAL      = 2    # Decimal constant.
    SYMBOLIC     = 3    # Symbol.
    EXPRESSION   = 4    # Symbolic expression.

# NOTE: Must be a new-style class.
class Opcode(object):

    def __init__(self, methodName=None, mnemonic=None, opcode=0, operandType=None, operandOptional=False, addressType=AddressType.GENERAL_12, numwords=1):
        if mnemonic == None:
            self.mnemonic = methodName
        else:
            self.mnemonic = mnemonic
        self.methodName = methodName                # Parser method name.
        self.opcode = opcode                        # Opcode mnemonic string.
        self.operandType = operandType              # Operand type.
        self.operandOptional = operandOptional      # Operand is optional?
        self.addressType = addressType              # Operand address type, if applicable.
        self.numwords = numwords                    # Number of code words generated.
        self.type = None                            # Parser record type for this opcode.
