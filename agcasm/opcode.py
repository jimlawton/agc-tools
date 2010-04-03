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
from opcodes import OPCODES

class OpcodeType:
    BASIC        = 0
    EXTENDED     = 1
    DIRECTIVE    = 3
    INTERPRETIVE = 4

class OperandType:
    NONE        = 0    # No operand.
    ERASABLE_10 = 1    # 10-bit erasable address.
    ERASABLE_12 = 2    # 12-bit erasable address.
    FIXED_9     = 3    # 9-bit fixed address. Only used by EDRUPT?
    FIXED_12    = 4    # 12-bit fixed address.
    GENERAL_12  = 5    # 12-bit general address (fixed or erasable).
    CHANNEL     = 6    # 9-bit I/O channel address.

# NOTE: Must be a new-style class.
class Opcode(object):
    
    def __init__(self, methodName=None, mnemonic=None, opcode=0, operandType=None, numwords=1):
        if mnemonic == None:
            self.mnemonic = methodName
        else:
            self.mnemonic = mnemonic
        self.methodName = methodName
        self.opcode = opcode
        self.operandType = operandType
        self.numwords = numwords

    def parse(self, context, operand):
        if context.mode == OpcodeType.EXTENDED and self.opcode not in OPCODES[context.arch][OpcodeType.EXTENDED]:
            context.error("missing EXTEND before extended instruction")
            sys.exit()
        if self.operandType == OperandType.NONE:
            context.code = [ self.opcode ]
        else:
            self.__getattribute__("parse_" + self.methodName)(operand)
        context.loc += self.numwords
        
