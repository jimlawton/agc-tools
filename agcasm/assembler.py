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
#

import os
from architecture import *
from number import *
from memory import *
from symbol_table import *
from instructions import *
from directives import *
from code import *
from parser_record import *

class Assembler:
    """Class defining an AGC assembler."""

    class Context:
        def __init__(self, arch, listfile, binfile, verbose=False):
            self.verbose = verbose
            self.arch = arch
            self.listfile = listfile
            self.binfile = binfile
            self.srcfile = None
            self.source = []
            self.symtab = SymbolTable(self)
            self.linenum = 0
            self.global_linenum = 0
            self.mode = OpcodeType.BASIC
            self.memmap = MemoryMap(arch, verbose)
            self.checklist = []
            self.loc = 0
            self.bank = 0
            self.bankloc = {}
            for bank in range(len(self.memmap.memmap)):
                self.bankloc[bank] = 0
            self.records = []

    def __init__(self, arch, listfile, binfile, verbose=False):
        self.verbose = verbose
        self.context = Assembler.Context(arch, listfile, binfile, verbose)
        self.context.verbose = verbose
        self.context.error = self.error
        self.context.warn = self.warn
        self.context.info = self.info
        
    def assemble(self, srcfile):
        print "Assembling", srcfile
        self.context.srcfile = srcfile
        self.context.linenum = 0
        lines = open(srcfile).readlines()
        for line in lines:
            self.context.source.append(line.expandtabs(8))
            self.context.linenum += 1
            self.context.global_linenum += 1
            if line.startswith('$'):
                modname = line[1:].split()[0]
                if not os.path.isfile(modname):
                    print >>sys.stderr, "File \"%s\" does not exist" % modname
                    sys.exit(1)
                self.assemble(modname)
                continue
            if len(line.strip()) == 0:
                continue
            # Real parsing starts here.
            fields = line.split()
            label = None
            pseudolabel = None
            opcode = None
            operand = None
            comment = None
            if line.startswith('#'):
                comment = line
            else:
                if '#' in line:
                    comment = line[line.index('#'):]
                if not line.startswith(' ') and not line.startswith('\t'):
                    label = fields[0]
                    if len(fields) == 1:
                        # Label only.
                        self.context.symtab.add(label, None, self.context.loc)
                        continue
                    fields = fields[1:]
                else:
                    if line[1] == '+' or line[1] == '-':
                        pseudolabel = fields[0]
                        fields = fields[1:]
                # TODO: how to handle interpretive code?
                opcode = fields[0]
                operands = ""
                for field in fields[1:]:
                    if field.startswith('#'):
                        break
                    operands += " " + field
                if operands == "":
                    operands = None
                else:
                    operands = operands.strip().split()
                if opcode == "EXTEND":
                    self.context.mode = OpcodeType.EXTENDED
                self.context.records.append(ParserRecord(self.context, label, pseudolabel, opcode, operands, comment))
                try:
                    if opcode in DIRECTIVES[self.context.arch]:
                        DIRECTIVES[self.context.arch][opcode].process(self.context, label, operands)
                    if opcode in INSTRUCTIONS[self.context.arch]:
                        INSTRUCTIONS[self.context.arch][opcode][self.context.mode].process(self.context, operands)
                        self.context.mode = OpcodeType.BASIC
                except:
                    #self.context.symtab.printTable()
                    raise

    def error(self, text):
        print >>sys.stderr, "%s, line %d, error: %s" % (self.context.srcfile, self.context.linenum, text)

    def warn(self, text):
        print >>sys.stderr, "%s, line %d, warning: %s" % (self.context.srcfile, self.context.linenum, text)

    def info(self, text):
        if self.verbose:
            print >>sys.stderr, "%s, line %d, %s" % (self.context.srcfile, self.context.linenum, text)
