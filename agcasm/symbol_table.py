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

class SymbolTableEntry:
    
    def __init__(self, context, name, symbolic=None, value=None):
        self.context = context
        self.name = name
        self.symbolic = symbolic
        self.value = value
        self.references = []
        self.recordIndex = None

    def isComplete(self):
        return (self.value != None)

    def addReference(self, ref):
        self.references.append(ref)

    def getReferences(self):
        return self.references

    def __str__(self):
        text = "%-8s "  % (self.name)
        if self.value == None:
            text += "%-20s" % "******"
        else:
            text += "%-10s" % self.context.memmap.pseudoToString(self.value)
            (bank, offset) = self.context.memmap.pseudoToSegmented(self.value)
            if bank != None:
                text += "(%02o,%04o) " % (bank, offset)
            else:
                text += 10 * ' ' 
        if self.symbolic:
            text += " \"%s\""  % (' '.join(self.symbolic))
        if len(self.references) > 0:
            text += self.references
        return text

class SymbolTable:
    def __init__(self, context):
        self.symbols = {}
        self.undefs = []
        self.context = context
        
    def add(self, name=None, symbolic=None, value=None):
        if name != None:
            if name in self.symbols.keys():
                self.context.error("symbol \"%s\" already defined!" % (name))
            else:
                self.symbols[name] = SymbolTableEntry(self.context, name, symbolic, value) 
                if value == None:
                    self.undefs.append(name)
                #else:
                #    tmpUndefs = []
                #    for symbol in self.undefs:
                #        record = self.symbols[symbol].record
                #        if name in record.operands:
                #            if name == "+ROLL1" or name == "FIVE":
                #                print "Reparsing symbol %s for %s" % (record.label, name)
                #            self.context.assembler.reparse(record)
                #            print record
                #        if not record.complete:
                #            tmpUndefs.append(name)
                #    self.undefs = tmpUndefs
                #    print "After reparse: undefs:", self.undefs

    def resolve(self, maxPasses=10):
        self.context.info("resolving symbols...")
        nPrevUndefs = nUndefs = len(self.undefs)
        for i in range(maxPasses):
            self.context.warn("pass %d: %d undefined symbols" % (i, nUndefs))
            if nUndefs == 0:
                self.context.info("all symbols resolved")
                break
            for symbol in self.undefs:
                self.context.assembler.reparse(self.symbols[symbol].recordIndex)
            self.pruneUndefines()
            nUndefs = len(self.undefs)
            if nUndefs == nPrevUndefs:
                self.context.error("aborting, no progress in resolving symbols")
                break
            nPrevUndefs = nUndefs

    def pruneUndefines(self):
        # Prune the undefs list.
        tmpUndefs =[]
        for symbol in self.undefs:
            record = self.context.records[self.symbols[symbol].recordIndex]
            if not record.complete:
                tmpUndefs.append(symbol)
        self.undefs = tmpUndefs
        
    def keys(self):
        return self.symbols.keys()

    def lookup(self, name):
        entry = None
        if name in self.symbols:
            entry = self.symbols[name]
        return entry

    def printTable(self, outfile=None):
        if outfile == None:
            out = sys.stdout
        else:
            out = outfile
        symbols = self.symbols.keys()
        symbols.sort()
        for symbol in symbols:
            print >>out, self.symbols[symbol]

        for symbol in self.undefs:
            print >>out, self.symbols[symbol]
