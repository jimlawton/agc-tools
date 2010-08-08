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
from memory import MemoryType

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
        self.super = context.super          # Superbank bit (0/1).
        self.ebank = context.ebank          # E Bank.
        self.fbank = context.fbank          # F Bank.
        self.loc = context.loc
        self.lastEbank = context.lastEbank
        self.previousWasEbankEquals = context.previousWasEbankEquals
        self.global_linenum = context.global_linenum
        self.argcode = None
        self.interpArgs = 0
        self.interpArgCount = 0
        self.packingType = None

    def isGenerative(self):
        return RecordType.isGenerative(self.type)

    def isParseable(self):
        return RecordType.isParseable(self.type)

    def isComplete(self):
        return self.complete

    def update(self):
        self.super = self.context.super
        self.ebank = self.context.ebank
        self.fbank = self.context.fbank
        self.lastEbank = self.context.lastEbank
        self.previousWasEbankEquals = self.context.previousWasEbankEquals
        self.interpArgs = self.context.interpArgs
        self.interpArgCount = self.context.interpArgCount

    def __str__(self):
        text = ""
        if self.type == RecordType.INCLUDE:
            text += "\n\n"
        text += "%06d,%06d " % (self.global_linenum, self.linenum)
        if RecordType.isIgnored(self.type):
            if self.context.debug:
                text += 49 * ' '
            else:
                text += 29 * ' '
        else:
            if RecordType.isAddressValid(self.type):
                text += self.context.memmap.pseudoToSegmentedString(self.address) + ' '
            else:
                text += 8 * ' '
            if self.target:
                text += self.context.memmap.pseudoToSegmentedString(self.target) + ' '
            else:
                text += 8 * ' '
            if self.isGenerative():
                if self.context.debug:
                    text += self.context.memmap.bankToString(MemoryType.ERASABLE, self.context.ebank)
                    text += ' '
                    text += self.context.memmap.bankToString(MemoryType.FIXED, self.context.fbank)
                    text += ' '
                    text += "(%02d,%02d) " % (self.interpArgs, self.interpArgCount)
                    if self.argcode != None and self.argcode > 0:
                        text += "%05o " % (self.argcode)
                    else:
                        text += 6 * ' '
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
                if self.context.debug:
                    text += 33 * ' '
                else:
                    text += 13 * ' '
        text += "   %s" % self.srcline
        return text
