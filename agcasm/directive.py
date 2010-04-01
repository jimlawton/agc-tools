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
from architecture import *
from number import *
from memory import *
from symbol_table import *
from expression import *
from opcode import *

# NOTE: Must be a new-style class.
class Directive(Opcode):
    
    def __init__(self, methodName, mnemonic=None, numwords=0):
        Opcode.__init__(self, methodName, mnemonic, None, None, numwords)
        
    def parse(self, context, symbol, operands):
        retval = self.__getattribute__("parse_" + self.methodName)(context, symbol, operands)
        context.loc += self.numwords
        return retval

    def ignore(self, context):
        context.info("ignoring directive \"%s\"" % self.mnemonic)

    def parse_Minus1DNADR(self, context, symbol, operands):
        retval = self.parse_1DNADR(context, symbol, operands)
        context.code = ~ context.code
        return retval
    
    def parse_Minus2CADR(self, context, symbol, operands):
        retval = self.parse_2CADR(context, symbol, operands)
        context.code = ~ context.code
        return retval
    
    def parse_Minus2DNADR(self, context, symbol, operands):
        retval = self.parse_2DNADR(context, symbol, operands)
        context.code = ~ context.code
        return retval

    def parse_Minus3DNADR(self, context, symbol, operands):
        retval = self.parse_3DNADR(context, symbol, operands)
        context.code = ~ context.code
        return retval

    def parse_Minus4DNADR(self, context, symbol, operands):
        retval = self.parse_4DNADR(context, symbol, operands)
        context.code = ~ context.code
        return retval
    
    def parse_Minus5DNADR(self, context, symbol, operands):
        retval = self.parse_5DNADR(context, symbol, operands)
        context.code = ~ context.code
        return retval
    
    def parse_Minus6DNADR(self, context, symbol, operands):
        retval = self.parse_6DNADR(context, symbol, operands)
        context.code = ~ context.code
        return retval
    
    def parse_MinusDNCHAN(self, context, symbol, operands):
        retval = self.parse_DNCHAN(context, symbol, operands)
        context.code = ~ context.code
        return retval
    
    def parse_MinusDNPTR(self, context, symbol, operands):
        retval = self.parse_DNPTR(context, symbol, operands)
        context.code = ~ context.code
        return retval
    
    def parse_MinusGENADR(self, context, symbol, operands):
        retval = self.parse_GENADR(context, symbol, operands)
        context.code = ~ context.code
        return retval
    
    def parse_1DNADR(self, context, symbol, operands):
        retval = False
        pa = None
        if operands:
            expr = Expression(context, operands)
            if expr.complete:
                pa = expr.value
                if context.memmap.isErasable(pa):
                    context.code = pa
                    retval = True
                else:
                    context.error("1DNADR operand must be in erasable memory")
        return retval
    
    def parse_2BCADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def parse_2CADR(self, context, symbol, operands):
        retval = False
        word1 = word2 = None
        if operands:
            expr = Expression(context, operands)
            if expr.complete:
                word1 = expr.value
                (bank, offset) = context.memmap.pseudoToSegmented(expr.value)
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
                    word2 != (context.ebank & 07)
                else:
                    word2 = context.memmap.getBankNumber(word1)
            retval = True
        return retval

    def parse_2DEC(self, context, symbol, operands):
        retval = False
        if operands:
            op = DoubleDecimal(" ".join(operands))
            if op.isValid():
                context.code = op.value
                if symbol:
                    context.symtab.add(symbol, operands, context.loc)
                retval = True
            else:
                context.error("syntax error: %s %s" % (self.mnemonic, operands))
        return retval

    def parse_2DNADR(self, context, symbol, operands):
        retval = False
        pa = None
        if operands:
            expr = Expression(context, operands)
            if expr.complete:
                pa = expr.value
                if context.memmap.isErasable(pa):
                    context.code = pa + 04000
                else:
                    context.error("2DNADR operand must be in erasable memory")
            retval = True
        return retval
    
    def parse_2FCADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def parse_2OCT(self, context, symbol, operands):
        retval = False
        if operands:
            op = DoubleOctal(" ".join(operands))
            if op.isValid():
                context.code = op.value
                if symbol:
                    context.symtab.add(symbol, operands, context.loc)
            else:
                context.error("syntax error: %s %s" % (self.mnemonic, operands))
            retval = True
        return retval
    
    def parse_3DNADR(self, context, symbol, operands):
        retval = False
        pa = None
        if operands:
            expr = Expression(context, operands)
            if expr.complete:
                pa = expr.value
                if context.memmap.isErasable(pa):
                    context.code = pa + 010000
                else:
                    context.error("3DNADR operand must be in erasable memory")
            retval = True
        return retval
    
    def parse_4DNADR(self, context, symbol, operands):
        retval = False
        pa = None
        if operands:
            expr = Expression(context, operands)
            if expr.complete:
                pa = expr.value
                if context.memmap.isErasable(pa):
                    context.code = pa + 014000
                else:
                    context.error("4DNADR operand must be in erasable memory")
            retval = True
        return retval
    
    def parse_5DNADR(self, context, symbol, operands):
        retval = False
        pa = None
        if operands:
            expr = Expression(context, operands)
            if expr.complete:
                pa = expr.value
                if context.memmap.isErasable(pa):
                    context.code = pa + 020000
                else:
                    context.error("5DNADR operand must be in erasable memory")
            retval = True
        return retval
    
    def parse_6DNADR(self, context, symbol, operands):
        retval = False
        pa = None
        if operands:
            expr = Expression(context, operands)
            if expr.complete:
                pa = expr.value
                if context.memmap.isErasable(pa):
                    context.code = pa + 024000
                else:
                    context.error("6DNADR operand must be in erasable memory")
            retval = True
        return retval

    def parse_EqualsSign(self, context, symbol, operands):
        retval = False
        if symbol:
            if operands:
                expr = Expression(context, operands)
                if expr.valid:
                    context.symtab.add(symbol, operands, expr.value)
                else:
                    context.symtab.add(symbol, operands)
                retval = True
            else:
                context.symtab.add(symbol, operands[0], context.loc)
        return retval

    def parse_EqualsECADR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def parse_EqualsMINUS(self, context, symbol, operands):
        retval = self.parse_EqualsSign(context, symbol, operands)
        context.code = ~ context.code
        return retval
    
    def parse_ADRES(self, context, symbol, operands):
        retval = False
        if operands:
            expr = Expression(context, operands)
            if expr.valid:
                (bank, offset) = context.memmap.pseudoToSegmented(expr.value)
                if bank and (bank == context.fbank or bank == context.ebank):
                    aval = offset
            retval = True
        return retval

    def parse_BANK(self, context, symbol, operands):
        retval = False
        if operands:
            expr = Expression(context, operands)
            if expr.valid:
                context.fbank = expr.value
                context.loc = context.memmap.segmentedToPseudo(MemoryType.FIXED, expr.value, context.bankloc[expr.value])
        else:
            context.loc = context.memmap.segmentedToPseudo(MemoryType.FIXED, context.fbank, context.bankloc[context.fbank])
        retval = True
        return retval

    def parse_BBCON(self, context, symbol, operands):
        retval = False
        if operands:
            fbank = None
            expr = Expression(context, operands)
            if expr.valid:
                (fbank, offset) = context.memmap.pseudoToSegmented(entry.value)
            if fbank:
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
                bbval != (context.ebank & 07)
                # TODO: emit bbval to code stream.
            retval = True
        return retval
    
    def parse_BLOCK(self, context, symbol, operands):
        retval = False
        if operands:
            expr = Expression(context, operands)
            if expr.valid:
                bank = expr.value
                if bank == 0:
                    context.ebank = bank
                    context.loc = context.memmap.segmentedToPseudo(MemoryType.ERASABLE, bank, context.bankloc[bank])
                else:
                    context.fbank = bank
                    context.loc = context.memmap.segmentedToPseudo(MemoryType.FIXED, bank, context.bankloc[bank])
            else:
                context.error("invalid syntax")
            retval = True
        return retval

    def parse_BNKSUM(self, context, symbol, operands):
        self.ignore(context)
        return True
    
    def parse_CADR(self, context, symbol, operands):
        retval = False
        word = None
        if operands:
            expr = Expression(context, operands)
            if expr.complete:
                word = expr.value
                context.code = word - 010000
            retval = True
        return retval
    
    def parse_CHECKEquals(self, context, symbol, operands):
        retval = False
        if operands:
            fields = operands[0].split()
            defn = context.symtab.lookup(fields[0])
            if not defn:
                # Add to checklist and check at the end.
                context.checklist.append(SymbolTableEntry(context, symbol, operands[0]))
            else:
                pa = defn.value
                if len(fields) > 1:
                    op = Number(fields[1].strip())
                    if op.isValid():
                        pa += op.value
                    else:
                        context.error("invalid expression, \"%s\"" % operand)
            retval = False
        return retval
    
    def parse_COUNT(self, context, symbol, operands):
        self.ignore(context)
        return True
    
    def parse_DEC(self, context, symbol, operands):
        retval = False
        if operands:
            op = Decimal(" ".join(operands))
            if op.isValid():
                context.code = op.value
                if symbol:
                    context.symtab.add(symbol, operands, context.loc)
            else:
                context.error("syntax error: %s %s" % (self.mnemonic, operands))
            retval = True
        return retval
    
    def parse_DNCHAN(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def parse_DNPTR(self, context, symbol, operands):
        context.error("unsupported directive: %s %s" % (self.mnemonic, operands))
        sys.exit()
    
    def parse_EBANKEquals(self, context, symbol, operands):
        retval = False
        # TODO: handle one-shot EBANK=.
        if operands:
            op = Number(operands[0])
            if op.isValid():
                context.ebank = op.value
            else:
                entry = context.symtab.lookup(operands[0])
                if entry:
                    bank = context.memmap.pseudoToSegmented(entry.value)
                else:
                    if context.passnum > 1:
                        context.error("undefined symbol \"%s\"" % operands[0])
            retval = True
        return retval

    def parse_ECADR(self, context, symbol, operands):
        retval = False
        pa = None
        if operands:
            expr = Expression(context, operands)
            if expr.complete:
                pa = expr.value
                if context.memmap.isErasable(pa):
                    context.code = pa
                else:
                    context.error("ECADR operand must be in erasable memory")
            retval = True
        return retval

    def parse_EQUALS(self, context, symbol, operands):
        retval = False
        if symbol:
            if operands:
                if operands[0].isdigit():
                    context.symtab.add(symbol, operands[0], int(operands[0], 8))
                else:
                    context.symtab.add(symbol, operands[0])
            else:
                context.symtab.add(symbol, None, context.loc)
            retval = True
        return retval

    def parse_ERASE(self, context, symbol, operands):
        retval = False
        size = 0
        if not operands:
            size = 1
            operand = None
            op = Number("1")
        else:
            operand = operands[0]
            if '-' in operands[0]:
                op = Number(operands[0].strip())
                if op.isValid():
                    size = op.value
            else:
                op = Number(operands[0])
                if op.isValid():
                    size = op.value + 1
        if symbol and op.isValid():
            context.symtab.add(symbol, operand, op.value)
        context.loc += size
        retval = True
        return retval
        
    def parse_FCADR(self, context, symbol, operands):
        retval = False
        pa = None
        if operands:
            expr = Expression(context, operands)
            if expr.complete:
                pa = expr.value
                if context.memmap.isFixed(pa):
                    context.code = pa
                else:
                    context.error("FCADR operand must be in fixed memory")
            retval = True
        return retval

    def parse_GENADR(self, context, symbol, operands):
        retval = False
        bank = None
        if operands:
            op = Number(operands[0])
            if op.isValid():
                aval = op.value
            else:
                entry = context.symtab.lookup(operands[0])
                if entry:
                    (bank, offset) = context.memmap.pseudoToSegmented(entry.value)
                else:
                    if context.passnum > 1:
                        context.error("undefined symbol \"%s\"" % operands[0])
                if bank:
                    aval = offset
            retval = False
        return retval
    
    def parse_MEMORY(self, context, symbol, operands):
        #if '-' in operands:
        #    op1 = int(operands[0], 8)
        #    if symbol:
        #        context.symtab.add(symbol, operands[0], op1)
        #else:
        #    context.error("syntax error: %s %s" % (self.mnemonic, operand))
        self.ignore(context)
        return True
    
    def parse_MM(self, context, symbol, operands):
        return self.parse_DEC(context, symbol, operands)
    
    def parse_NV(self, context, symbol, operands):
        return self.parse_VN(context, symbol, operands)
    
    def parse_OCT(self, context, symbol, operands):
        retval = False
        if operands:
            op = Octal(operands[0])
            if op.isValid():
                context.code = op.value
                if symbol:
                    context.symtab.add(symbol, operands[0], op.value)
            else:
                context.error("syntax error: %s %s" % (self.mnemonic, operands[0]))
            retval = True
        return retval

    def parse_OCTAL(self, context, symbol, operands):
        return self.parse_OCT(context, symbol, operands)
    
    def parse_REMADR(self, context, symbol, operands):
        retval = False
        bank = None
        if operands:
            op = Number(operands[0])
            if op.isValid():
                aval = op.value
            else:
                entry = context.symtab.lookup(operands[0])
                if entry:
                    (bank, offset) = context.memmap.pseudoToSegmented(entry.value)
                else:
                    if context.passnum > 1:
                        context.error("undefined symbol \"%s\"" % operands[0])
                if bank and (bank != context.fbank and bank != context.ebank):
                    aval = offset
            retval = True
        return retval

    def parse_SBANKEquals(self, context, symbol, operands):
        context.warn("unsupported directive: %s %s" % (self.mnemonic, operands))
        return True
    
    def parse_SETLOC(self, context, symbol, operands):
        retval = False
        if operands:
            if operands[0].isdigit():
                context.loc = int(operands[0], 8)
            else:
                entry = context.symtab.lookup(operands[0])
                if entry:
                    context.loc = entry.value
            retval = True
        return retval

    def parse_SUBRO(self, context, symbol, operands):
        self.ignore(context)
        return True
    
    def parse_VN(self, context, symbol, operands):
        retval = False
        if operands:
            op = Decimal(operands[0])
            if op.isValid():
                lower = int(operands[0][-2:])
                upper = int(operands[0][:-2])
                context.code = upper * 128 + lower
                if symbol:
                    context.symtab.add(symbol, operands[0], context.loc)
            else:
                context.error("syntax error: %s %s" % (self.mnemonic, operands))
            retval = True
        return retval

