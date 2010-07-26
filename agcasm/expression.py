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

from number import Number
from opcode import OperandType

class Expression:
    """Class that represents an AGC expression."""
    
    def __init__(self, context, operands, addressExpr=False):
        self.complete = False               # Expression complete, all references resolved.
        self.operands = operands            # List of operand fields.
        self.value = None                   # If complete, calculated result of the expression.
        self.addressExpr = addressExpr      # Indicates that the expression is an Address Expression.
        self.context = context
        
        self.context.log(5, "expression: operands=%s addressExpr=%s" % (operands, addressExpr))

        op1 = 0
        op2 = 0
        
        if operands != None and 1 <= len(operands) <= 3:
            if len(operands) >= 1:
                operand = operands[0]
                (op1, op1type) = self._parseOperand(operand)
                if op1 != None:
                    if len(operands) == 1:
                        if self.addressExpr and op1type == OperandType.DECIMAL:
                            if operands[0].startswith('+'): 
                                self.value = self.context.loc + op1
                            elif operands[0].startswith('-'):
                                self.value = self.context.loc - op1
                            else:
                                self.value = op1
                        else:
                            self.value = op1
                        self.complete = True
            if len(operands) >= 2:
                if len(operands) == 2:
                    if operands[1].startswith('+') or operands[1].startswith('-'):
                        # Split a +N or -N operand.
                        operands = [ operands[0], operands[1][0], operands[1][1:] ]
                    else:
                        self.context.syntax("second operand must be +number or -number")
                if operands[1] != '+' and operands[1] != '-':
                    self.context.syntax("expression must be either addition (+) or subtraction (-)")
            if len(operands) == 3:
                (op2, op2type) = self._parseOperand(operands[2])
                if op1 != None and op2 != None:
                    if operands[1] == '+':
                        self.value = op1 + op2
                    else:
                        self.value = op1 - op2
                    self.complete = True

        if self.complete == True:
            self.context.log(5, "expression: complete, value=%05o" % (self.value))
        else:
            self.context.log(5, "expression: incomplete")

    def _parseOperand(self, operand):
        retval = None
        rettype = OperandType.NONE
        
        # First try symbol lookup.
        entry = self.context.symtab.lookup(operand)
        if entry != None:
            retval = entry.value
            rettype = OperandType.SYMBOLIC
        else:
            tmpop = operand
            if self.addressExpr and (operand.startswith('+') or operand.startswith('-')):
                tmpop = operand[1:]
            try:
                # Next try number.
                op = Number(tmpop)
                if op.isValid():
                    retval = op.value
                    rettype = OperandType.DECIMAL
            except:
                # Assume it is a symbol as yet undefined.
                pass

        return (retval, rettype)

    def __str__(self):
        text = "Expression: complete=%s" % str(self.complete)
        text += ", operands=%s" % str(self.operands)
        if self.value:
            text += ", value=%06o" % self.value
        else:
            text += ", value=%s" % self.value
        return text

class AddressExpression(Expression):
    "Class that represents an address expression."
    
    def __init__(self, context, operands):
        Expression.__init__(self, context, operands, True)
