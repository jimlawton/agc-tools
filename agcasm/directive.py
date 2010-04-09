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
from number import Decimal, DoubleDecimal, Octal, DoubleOctal
from expression import Expression, AddressExpression, Number
from opcode import Opcode, OperandType
from record_type import RecordType

# NOTE: Must be a new-style class.
class Directive(Opcode):
    
    def __init__(self, methodName, mnemonic=None, operandType=OperandType.NONE, operandOptional=False, numwords=0):
        Opcode.__init__(self, methodName, mnemonic, None, operandType, operandOptional, None, numwords)
        if numwords == 0:
            self.type = RecordType.ASMCONST
        else:
            self.type = RecordType.CONST
        
    def parse(self, context, operands):
        if self.operandType == OperandType.NONE:
            if operands != None:
                context.error("instruction takes no operand")
        else:
            if operands == None:
                if not self.operandOptional:
                    context.error("missing operand")
        try:
            self.__getattribute__("parse_" + self.methodName)(context, operands)
        except:
            pass
        context.currentRecord.type = self.type
        context.incrLoc(self.numwords)
        if self.numwords == 0:
            if self.methodName != "EQUALS":
                context.currentRecord.complete = True

    def ignore(self, context):
        self.type = RecordType.IGNORE
        context.info("ignoring directive \"%s\"" % self.mnemonic)

    def parse_MinusDNADR(self, context, operands):
        self.parse_DNADR(context, operands)
        words = []
        if context.currentRecord.code != None:
            for i in range(len(context.currentRecord.code)):
                words.append(~context.currentRecord.code[i])
            context.currentRecord.code = words
            context.currentRecord.complete = True
    
    def parse_Minus2CADR(self, context, operands):
        self.parse_2CADR(context, operands)
        words = []
        if context.currentRecord.code != None:
            for i in range(len(context.currentRecord.code)):
                words.append(~context.currentRecord.code[i])
            context.currentRecord.code = words
            context.currentRecord.complete = True
    
    def parse_MinusDNCHAN(self, context, operands):
        self.parse_DNCHAN(context, operands)
        words = []
        if context.currentRecord.code != None:
            for i in range(len(context.currentRecord.code)):
                words.append(~context.currentRecord.code[i])
            context.currentRecord.code = words
            context.currentRecord.complete = True
    
    def parse_MinusDNPTR(self, context, operands):
        self.parse_DNPTR(context, operands)
        words = []
        if context.currentRecord.code != None:
            for i in range(len(context.currentRecord.code)):
                words.append(~context.currentRecord.code[i])
            context.currentRecord.code = words
            context.currentRecord.complete = True
    
    def parse_MinusGENADR(self, context, operands):
        self.parse_GENADR(context, operands)
        words = []
        if context.currentRecord.code != None:
            for i in range(len(context.currentRecord.code)):
                words.append(~context.currentRecord.code[i])
            context.currentRecord.code = words
            context.currentRecord.complete = True
    
    def parse_DNADR(self, context, operands):
        pa = None
        opnum = int(self.opcode[0])
        dnadrConstants = { 1: 000000, 2: 004000, 3: 010000, 4: 014000, 5: 020000, 6: 024000 }
        expr = AddressExpression(context, operands)
        if expr.complete:
            pa = expr.value
            if context.memmap.isErasable(pa):
                context.currentRecord.code = [ pa + dnadrConstants[opnum] ]
                context.currentRecord.complete = True
            else:
                context.error("operand must be in erasable memory")
    
    def parse_2CADR(self, context, operands):
        word1 = word2 = None
        expr = AddressExpression(context, operands)
        if expr.complete:
            word1 = expr.value
            if context.memmap.isFixed(word1):
                word2 = 0
                # Bits 15-11 of the 2nd generated word contain the bank number.
                word2 |= ((context.fbank & 037) << 10) 
                # Bits 10-8 and 4 are zero. 
                # Bits 7-5 are 000 if F-Bank < 030, 011 if F-Bank is 030-037, or 100 if F-Bank is 040-043.
                if 030 <= context.fbank <= 037:
                    word2 |= (3 << 4)
                elif 040 <= context.fbank <= 043:
                    word2 |= (4 << 4)
                # Bits 3-1 equals the current EBANK= code.
                word2 |= (context.ebank & 07)
            else:
                word2 = context.memmap.getBankNumber(word1)
            context.currentRecord.code = [word1, word2]
            context.currentRecord.complete = True
        if context.lastEbankEquals:
            context.revertEBank()

    def parse_2DEC(self, context, operands):
        op = DoubleDecimal(" ".join(operands))
        if op.isValid():
            context.currentRecord.code = op.value
            context.currentRecord.complete = True
        else:
            context.error("syntax error: %s %s" % (self.mnemonic, operands))

    def parse_2FCADR(self, context, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def parse_2OCT(self, context, operands):
        op = DoubleOctal(" ".join(operands))
        if op.isValid():
            context.currentRecord.code = op.value
            context.currentRecord.complete = True
        else:
            context.error("syntax error: %s %s" % (self.mnemonic, operands))
    
    def parse_EqualsECADR(self, context, operands):
        self.ignore(context)
    
    def parse_EqualsMINUS(self, context, operands):
        self.parse_EQUALS(context, operands)
        if context.currentRecord.target != None:
            context.currentRecord.target = ~context.currentRecord.target
            context.currentRecord.complete = True
    
    def parse_ADRES(self, context, operands):
        expr = Expression(context, operands)
        if expr.complete:
            (bank, offset) = context.memmap.pseudoToSegmented(expr.value)
            if bank and (bank == context.fbank or bank == context.ebank):
                aval = offset
                context.currentRecord.code = [ aval ]
                context.currentRecord.complete = True

    def parse_BANK(self, context, operands):
        if operands:
            expr = Expression(context, operands)
            if expr.complete:
                context.switchFBank(expr.value)
                context.currentRecord.target = context.loc
                context.currentRecord.complete = True
        else:
            context.switchFBank()
            context.currentRecord.target = context.loc
            context.currentRecord.complete = True
        return True

    def parse_BBCON(self, context, operands):
        fbank = None
        expr = Expression(context, operands)
        if expr.complete:
            fbank = context.memmap.getBankNumber(expr.value)
        if fbank != None:
            bbval = 0
            # Bits 15-11 of the generated word contain the bank number.
            bbval |= ((fbank & 037) << 10) 
            # Bits 10-8 and 4 are zero. 
            # Bits 7-5 are 000 if F-Bank < 030, 011 if F-Bank is 030-037, or 100 if F-Bank is 040-043.
            if 030 <= fbank <= 037:
                bbval |= (3 << 4)
            elif 040 <= fbank <= 043:
                bbval |= (4 << 4)
            # Bits 3-1 equals the current EBANK= code.
            bbval |= (context.ebank & 07)
            context.currentRecord.code = [ bbval ]
            context.currentRecord.complete = True
        if context.lastEbankEquals:
            context.ebank = context.lastEbank
            context.lastEbankEquals = False
    
    def parse_BBCONstar(self, context, operands):
        context.currentRecord.code = [ 066100 ]
        context.currentRecord.complete = True
        if context.lastEbankEquals:
            context.ebank = context.lastEbank
            # TODO: recalculate sbank, based on superbit=1.
            context.lastEbankEquals = False
        return True
    
    def parse_BLOCK(self, context, operands):
        expr = Expression(context, operands)
        if expr.complete:
            bank = expr.value
            if bank == 0:
                context.switchEBank(bank)
                context.currentRecord.target = context.loc
                context.currentRecord.complete = True
            else:
                context.switchFBank(bank)
                context.currentRecord.target = context.loc
                context.currentRecord.complete = True
        else:
            context.error("invalid syntax")

    def parse_BNKSUM(self, context, operands):
        self.ignore(context)
    
    def parse_CADR(self, context, operands):
        word = None
        if operands:
            expr = Expression(context, operands)
            if expr.complete:
                word = expr.value
                context.currentRecord.code = [ word - 010000 ]
                context.currentRecord.complete = True
    
    def parse_CHECKEquals(self, context, operands):
        if context.currentRecord.label != None:
            lhs = Expression(context, [ context.currentRecord.label ])
            rhs = Expression(context, operands)
            if not lhs.complete or not rhs.complete:
                # Add to checklist and check at the end.
                context.checklist.append(context.currentRecord)
            else:
                lpa = lhs.value
                rpa = rhs.value
                if lpa != rpa:
                    context.error("CHECK= test failed, \"%s\" (%06o) != \"%s\" (%06o)" % (context.currentRecord.label, lpa, ' '.join(operands), rpa))
                context.currentRecord.target = lpa
        else:
            context.error("syntax error")
        context.addSymbol = False
    
    def parse_COUNT(self, context, operands):
        self.ignore(context)
    
    def parse_DEC(self, context, operands):
        op = Decimal(" ".join(operands))
        if op.isValid():
            context.currentRecord.code = [ op.value ]
            context.currentRecord.complete = True
        else:
            context.error("invalid syntax")
    
    def parse_DNCHAN(self, context, operands):
        op = Octal(" ".join(operands))
        if op.isValid():
            context.currentRecord.code = [ op.value + 034000 ]
            context.currentRecord.complete = True
        else:
            context.error("syntax error: %s %s" % (self.mnemonic, operands))
    
    def parse_DNPTR(self, context, operands):
        pa = None
        expr = Expression(context, operands)
        if expr.complete:
            channel = expr.value
            if context.memmap.isChannel(channel):
                context.currentRecord.code = [ pa + 030000 ]
                context.currentRecord.complete = True
            else:
                context.error("operand must be a channel number")
    
    def parse_EBANKEquals(self, context, operands):
        op = Number(operands[0])
        if op.isValid():
            context.lastEbank = context.ebank
            context.ebank = op.value
            context.lastEbankEquals = True
            context.currentRecord.target = op.value
        else:
            entry = context.symtab.lookup(operands[0])
            if entry != None:
                bank = context.memmap.getBankNumber(entry.value)
                if bank != None:
                    context.lastEbank = context.ebank
                    context.ebank = bank
                    context.lastEbankEquals = True
                    context.currentRecord.target = entry.value

    def parse_ECADR(self, context, operands):
        pa = None
        expr = Expression(context, operands)
        if expr.complete:
            pa = expr.value
            if context.memmap.isErasable(pa):
                context.currentRecord.code = [ pa ]
                context.currentRecord.complete = True
            else:
                context.error("operand must be in erasable memory")

    def parse_EQUALS(self, context, operands):
        if operands != None:
            expr = Expression(context, operands)
            if expr.complete:
                if not context.reparse:
                    context.symtab.add(context.currentRecord.label, operands, expr.value)
                else:
                    context.symtab.update(context.currentRecord.label, operands, expr.value)
                context.currentRecord.target = expr.value
                context.currentRecord.complete = True
            else:
                if not context.reparse:
                    context.symtab.add(context.currentRecord.label, operands)
        else:
            if not context.reparse:
                context.symtab.add(context.currentRecord.label, None, context.loc)
            else:
                context.symtab.update(context.currentRecord.label, None, context.loc)
            context.currentRecord.target = context.loc
            context.currentRecord.complete = True
        context.currentRecord.type = RecordType.ASMCONST
        context.addSymbol = False

    def parse_ERASE(self, context, operands):
        size = 0
        if operands == None:
            size = 1
            op = Number("1")
        else:
            # TODO: Change to use Expression.
            if '-' in operands[0]:
                op = Number(operands[0].strip())
                if op.isValid():
                    size = op.value
            else:
                op = Number(operands[0])
                if op.isValid():
                    size = op.value + 1
        if context.currentRecord.label != None and op.isValid():
            if not context.reparse:
                context.symtab.add(context.currentRecord.label, operands, context.loc)
            else:
                context.symtab.update(context.currentRecord.label, operands, context.loc)
        context.currentRecord.target = context.loc
        context.incrLoc(size)
        context.addSymbol = False
        
    def parse_FCADR(self, context, operands):
        pa = None
        expr = Expression(context, operands)
        if expr.complete:
            pa = expr.value
            if context.memmap.isFixed(pa):
                context.currentRecord.code = [ pa ]
                context.currentRecord.complete = True
            else:
                context.error("FCADR operand must be in fixed memory")

    def parse_GENADR(self, context, operands):
        bank = None
        aval = None
        op = Number(operands[0])
        if op.isValid():
            aval = op.value
        else:
            entry = context.symtab.lookup(operands[0])
            if entry != None:
                (bank, offset) = context.memmap.pseudoToSegmented(entry.value)
            if bank:
                aval = offset
        if aval != None:
            context.currentRecord.code = [ aval ]
            context.currentRecord.complete = True
    
    def parse_MEMORY(self, context, operands):
        #if '-' in operands:
        #    op1 = int(operands[0], 8)
        #    if symbol:
        #        context.symtab.add(symbol, operands[0], op1)
        #else:
        #    context.error("syntax error: %s %s" % (self.mnemonic, operand))
        self.ignore(context)
    
    def parse_OCT(self, context, operands):
        op = Octal(operands[0])
        if op.isValid():
            context.currentRecord.code = [ op.value ]
            context.currentRecord.complete = True
        else:
            context.error("syntax error: %s %s" % (self.mnemonic, operands[0]))

    def parse_REMADR(self, context, operands):
        bank = None
        aval = None
        op = Number(operands[0])
        if op.isValid():
            aval = op.value
        else:
            entry = context.symtab.lookup(operands[0])
            if entry:
                (bank, offset) = context.memmap.pseudoToSegmented(entry.value)
            if bank and (bank != context.fbank and bank != context.ebank):
                aval = offset
        if aval != None:
            context.currentRecord.code = [ aval ]
            context.currentRecord.complete = True

    def parse_SBANKEquals(self, context, operands):
        pa = None
        expr = Expression(context, operands)
        if expr.complete:
            pa = expr.value
            if context.memmap.isFixed(pa):
                context.currentRecord.target = pa
                context.currentRecord.complete = True
                context.sbank = pa
            else:
                context.error("operand must be in fixed memory")
    
    def parse_SETLOC(self, context, operands):
        expr = Expression(context, operands)
        if expr.complete:
            pa = expr.value
            context.currentRecord.target = pa
            context.currentRecord.complete = True
            context.setLoc(pa)

    def parse_SUBRO(self, context, operands):
        self.ignore(context)
    
    def parse_VN(self, context, operands):
        op = Decimal(operands[0])
        if op.isValid():
            lower = int(operands[0][-2:])
            upper = int(operands[0][:-2])
            context.currentRecord.code = [ upper * 128 + lower ]
            context.currentRecord.complete = True
        else:
            context.error("syntax error: %s %s" % (self.mnemonic, operands))

