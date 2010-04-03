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

import os
import sys
from memory import MemoryMap
from opcode import OpcodeType
from opcodes import OPCODES
from parser_record import ParserRecord
from symbol_table import SymbolTable

class Assembler:
    """Class defining an AGC assembler."""

    class Context:
        def __init__(self, arch, listfile, binfile, verbose=False):
            self.verbose = verbose
            self.arch = arch
            self.listfile = listfile
            self.binfile = binfile
            self.srcfile = None
            self.opcodes = OPCODES[self.arch]
            self.symtab = SymbolTable(self)
            self.linenum = 0
            self.global_linenum = 0
            self.mode = OpcodeType.BASIC
            self.memmap = MemoryMap(arch, verbose)
            self.checklist = []
            self.loc = 0
            self.passnum = 1
            self.ebank = 0
            self.fbank = 0
            self.bankloc = {}
            self.code = []
            for bank in range(len(self.memmap.memmap)):
                self.bankloc[bank] = 0
            self.records = []
            self.srcline = None

    def __init__(self, arch, listfile, binfile, verbose=False):
        self.verbose = verbose
        self.context = Assembler.Context(arch, listfile, binfile, verbose)
        self.context.verbose = verbose
        self.context.error = self.error
        self.context.warn = self.warn
        self.context.info = self.info
        
    def _makeNewRecord(self, line, label, pseudolabel, opcode, operands, comment):
        srcfile = self.context.srcfile
        linenum = self.context.linenum
        srcline = line
        address = self.context.loc
        code = self.context.code
        if label == None and pseudolabel == None and opcode == None and operands == None:
            address = None
            code = None
        return ParserRecord(srcfile, linenum, srcline, label, pseudolabel, opcode, operands, comment, address, code)

    def assemble(self, srcfile):
        print "Assembling", srcfile
        self.context.srcfile = srcfile
        self.context.linenum = 0
        lines = open(srcfile).readlines()
        for line in lines:
            if line.endswith('\n'):
                line = line[:-1]
            srcline = line.expandtabs(8)
            self.context.srcline = srcline
            self.context.linenum += 1
            self.context.global_linenum += 1
            self.context.code = None
            label = None
            pseudolabel = None
            opcode = None
            operands = None
            comment = None
            if line.startswith('$'):
                modname = line[1:].split()[0]
                if not os.path.isfile(modname):
                    print >>sys.stderr, "File \"%s\" does not exist" % modname
                    sys.exit(1)
                self.context.records.append(self._makeNewRecord(srcline, None, None, None, None, comment))
                self.assemble(modname)
                continue
            if len(line.strip()) == 0:
                self.context.records.append(self._makeNewRecord(srcline, None, None, None, None, None))
                continue
            if line.strip().startswith('#'):
                comment = line
                self.context.records.append(self._makeNewRecord(srcline, None, None, None, None, comment))
            else:
                # Real parsing starts here.
                if '#' in line:
                    comment = line[line.index('#'):]
                    line = line[:line.index('#')]
                fields = line.split()
                if not line.startswith(' ') and not line.startswith('\t'):
                    label = fields[0]
                    if len(fields) == 1:
                        # Label only.
                        self.context.symtab.add(label, None, self.context.loc)
                        self.context.records.append(self._makeNewRecord(srcline, label, None, None, None, comment))
                        continue
                    fields = fields[1:]
                else:
                    if line[1] == '+' or line[1] == '-':
                        pseudolabel = fields[0]
                        fields = fields[1:]
                # TODO: how to handle interpretive code?
                try:
                    opcode = fields[0]
                except:
                    print line
                    print fields
                    raise
                operands = " " .join(fields[1:])
                if operands == "":
                    operands = None
                else:
                    operands = operands.strip().split()
                if self.context.mode == OpcodeType.EXTENDED and opcode not in self.context.opcodes[OpcodeType.EXTENDED]:
                    self.context.error("missing EXTEND before extended instruction")
                else:
                    self.parse(label, opcode, operands)
                    self.context.records.append(self._makeNewRecord(srcline, label, pseudolabel, opcode, operands, comment))

    def parse(self, label, opcode, operands):
        try:
            if opcode in self.context.opcodes[OpcodeType.INTERPRETIVE]:
                self.context.opcodes[OpcodeType.INTERPRETIVE][opcode].parse(self.context, label, operands)
            if opcode in self.context.opcodes[OpcodeType.DIRECTIVE]:
                self.context.opcodes[OpcodeType.DIRECTIVE][opcode].parse(self.context, label, operands)
            if opcode in self.context.opcodes[self.context.mode]:
                self.context.opcodes[self.context.mode][opcode].parse(self.context, operands)
                if opcode != "EXTEND" and self.context.mode == OpcodeType.EXTENDED:
                    self.context.mode = OpcodeType.BASIC
        except:
            self.error("Exception processing line:")
            raise
        
    def error(self, text):
        print >>sys.stderr, "%s, line %d, error: %s" % (self.context.srcfile, self.context.linenum, text) 
        print >>sys.stderr, self.context.srcline
        
    def warn(self, text):
        print >>sys.stderr, "%s, line %d, warning: %s" % (self.context.srcfile, self.context.linenum, text)

    def info(self, text):
        if self.verbose:
            print >>sys.stderr, "%s, line %d, %s" % (self.context.srcfile, self.context.linenum, text)
