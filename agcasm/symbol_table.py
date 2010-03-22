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

from architecture import *

class SymbolTableEntry:
    
    def __init__(self, context, name, symbolic=None, value=-1):
        self.context = context
        self.name = name
        self.symbolic = symbolic
        self.value = value

    def __str__(self):
        text = "%-8s "  % (self.name)
        if self.value == -1:
            text += "%-20s" % "UNDEFINED"
        else:
            text += "%-10s" % self.context.memmap.pseudoToString(self.value)
            text += "(%02o,%04o) " % self.context.memmap.pseudoToSegmented(self.value)
            print self.context.memmap.pseudoToSegmented(self.value)
        if self.symbolic:
            text += " \"%s\""  % (self.symbolic)
        return text

class SymbolTable:
    def __init__(self, context):
        self.symbols = {}
        self.context = context
        
    def add(self, name=None, symbolic=None, value=-1):
        if name in self.symbols:
            print >>sys.stderr, "Error, symbol \"%s\" already defined!" % (name)
            sys.exit()
        else:
            self.symbols[name] = SymbolTableEntry(self.context, name, symbolic, value)

    def keys(self):
        return self.symbols.keys()

    def lookup(self, name):
        entry = None
        if name in self.symbols:
            entry = self.symbols[name]
        return entry

    def printTable(self):
        symbols = self.symbols.keys()
        symbols.sort()
        for symbol in symbols:
            print self.symbols[symbol]

