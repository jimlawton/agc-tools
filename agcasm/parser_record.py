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

from record_type import RecordType

class ParserRecord:
    """Class storing parser data."""
    
    def __init__(self, context, srcfile, linenum, srcline, type, label, pseudolabel, opcode, operands, comment, address, code):
        self.context = context              # Assembler context.
        self.srcfile = srcfile              # Source filename.
        self.linenum = linenum              # Source line number.
        self.srcline = srcline              # Source line.
        self.type = type                    # Record type.
        self.label = label                  # Label field [optional].
        self.pseudolabel = pseudolabel      # Pseudo-label field [optional].
        self.opcode = opcode                # Opcode or directive field.
        self.operands = operands            # Operands.
        self.comment = comment              # Comments.
        self.address = address              # Address of the first word in the code section.
        self.code = code                    # List of generated code words.
        self.numwords = 0                   # Number of code words generated.
        self.complete = False               # Assembly complete? i.e. all symbols resolved.
        self.target = None                  # Target address, if any, e.g. for = directive.
        self.mode = context.mode            # Mode.
        self.sbank = context.sbank          # S Bank.
        self.ebank = context.ebank          # E Bank.
        self.fbank = context.fbank          # F Bank.
        self.loc = context.loc
        self.lastEbank = context.lastEbank
        self.lastEbankEquals = context.lastEbankEquals
        self.global_linenum = context.global_linenum
        
    def isComplete(self):
        return self.complete

    def update(self):
        self.sbank = self.context.sbank
        self.ebank = self.context.ebank
        self.fbank = self.context.fbank
        self.loc = self.context.loc
        self.lastEbank = self.context.lastEbank
        self.lastEbankEquals = self.context.lastEbankEquals

    def __str__(self):
        text = ""
        text += "%06d " % self.linenum
        if RecordType.isIgnored(self.type):
            text += 38 * ' ' 
        else: 
            if RecordType.isAddressValid(self.type):
                text += self.context.memmap.pseudoToSegmentedString(self.address) + ' '
            else:
                text += 10 * ' '
            text += RecordType.toString(self.type) + "  "
            if self.target: 
                text += self.context.memmap.pseudoToSegmentedString(self.target) + ' '
            else:
                text += 10 * ' '
            if RecordType.isGenerative(self.type):
                if self.code != None and len(self.code) > 0:
                    if len(self.code) == 1 and self.code[0] != None:
                        text += " %05o %s " % (self.code[0] & 077777, 5 * ' ')
                    elif len(self.code) == 2 and self.code[0] != None and self.code[1] != None:
                        text += " %05o %05o " % (self.code[0] & 077777, self.code[1] & 077777)
                    else:
                        text += " ????? " + 6 * ' '
                else:
                    text += " ????? " + 6 * ' ' 
            else:
                text += 13 * ' '
        text += "   %s" % self.srcline
        return text
