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

from number import *

class Expression:
    """Class that represents an AGC expression."""
    
    def __init__(self, context, operands):
        self.valid = False
        self.complete = False
        self.operands = operands
        self.value = None

        op1 = 0
        op2 = 0
        
        if operands and 1 <= len(operands) <= 3:
            if len(operands) >= 1:
                op1 = self._parseOperand(context, operands[0])
                if op1:
                    if len(operands) == 1:
                        self.value = op1
                        self.valid = True
            if len(operands) >= 2:
                if len(operands) == 2:
                    if operands[1].startswith('+') or operands[1].startswith('-'):
                        # Split a +N or -N operand.
                        operands = [ operands[0], operands[1][0], operands[1][1:] ]
                    else:
                        context.error("invalid syntax")
                if operands[1] != '+' and operands[1] != '-':
                    context.error("invalid syntax")
            if len(operands) == 3:
                op2 = self._parseOperand(context, operands[2])
                if op1 and op2:
                    if operands[1] == '+':
                        self.value = op1 + op2
                    else:
                        self.value = op1 - op2
                    self.valid = True
                    self.complete = True
        else:
            context.error("invalid syntax")

    def _parseOperand(self, context, operand):
        retval = None
        op = Number(operand)
        if op.isValid():
            retval = op.value
        else:
            entry = context.symtab.lookup(operand)
            if entry:
                retval = entry.value

        return retval
