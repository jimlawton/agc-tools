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

class ParserRecord:
    """Class storing parser data."""
    
    def __init__(self, context, label, pseudolabel, opcode, operands, comment):
        self.srcfile = context.srcfile      # Source filename.
        self.linenum = context.linenum      # Source line number.
        self.label = label                  # Label field [optional].
        self.pseudolabel = pseudolabel      # Pseudo-label field [optional].
        self.opcode = opcode                # Opcode or directive field.
        self.operands = operands            # Operands.
        self.comment = comment              # Comments.
        self.address = context.loc          # Address of the first word in the code section.
        self.numwords = 0                   # Number of code words generated.
        self.code = []                      # List of generated code words.
        self.ebank = None                   # Current E-Bank.
        self.complete = False               # Assembly complete? i.e. all symbols resolved.
        
    def generate(self, code):
        self.code = code

    def setEBank(self, ebank):
        self.ebank = ebank

    def isComplete(self):
        return self.complete
