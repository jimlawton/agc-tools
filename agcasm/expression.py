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
        self.operands = operands
        self.value = None
        
        if operands:
            if len(operands) == 1 or len(operands) == 3:
                op1 = self._parseOperand(context, operands[0])
                if op1:
                    self.value = op1
                    if len(operands) > 1:
                        if operands[1] == '+' or operands[1] == '-':
                            op2 = self._parseOperand(context, operands[2])
                            if op2:
                                if operands[1] == '+':
                                    self.value += op2
                                else:
                                    self.value -= op2
                                self.valid = True
                        else:
                            context.error("invalid syntax")
                    else:
                        self.valid = True
            else:
                context.error("invalid syntax")
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
            else:
                context.error("undefined symbol \"%s\"" % operand)
        return retval
