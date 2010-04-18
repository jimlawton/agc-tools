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
from opcode import OpcodeType
from parser_record import ParserRecord
from record_type import RecordType
from interpretive import Interpretive

class Assembler:
    """Class defining an AGC assembler."""

    def __init__(self, context):
        self.context = context
        self.context.error = self.error
        self.context.syntax = self.syntax
        self.context.warn = self.warn
        self.context.info = self.info
        self.context.log = self.log

    def _makeNewRecord(self, line, rectype, label, pseudolabel, opcode, operands, comment):
        srcfile = self.context.srcfile
        linenum = self.context.linenum
        srcline = line
        address = self.context.loc
        code = self.context.code
        if label == None and pseudolabel == None and opcode == None and operands == None:
            address = None
            code = None
        tmpType = rectype
        if rectype == None:
            tmpType = RecordType.NONE
        return ParserRecord(self.context, srcfile, linenum, srcline, tmpType, label, pseudolabel, opcode, operands, comment, address, code)

    def assemble(self, srcfile):
        self.info("Assembling %s" % srcfile)
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
            self.context.addSymbol = True
            label = None
            pseudolabel = None
            opcode = None
            operands = None
            comment = None

            if line.startswith('$'):
                modname = line[1:].split()[0]
                if not os.path.isfile(modname):
                    self.fatal("File \"%s\" does not exist" % modname)
                record = self._makeNewRecord(srcline, RecordType.INCLUDE, None, None, None, None, comment)
                self.context.records.append(record)
                self.assemble(modname)
                continue
            
            if len(line.strip()) == 0:
                self.context.records.append(self._makeNewRecord(srcline, RecordType.BLANK, None, None, None, None, None))
                continue
            
            if line.strip().startswith('#'):
                comment = line
                record = self._makeNewRecord(srcline, RecordType.COMMENT, None, None, None, None, comment)
                self.context.records.append(record)
                continue
            
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
                    record = self._makeNewRecord(srcline, RecordType.LABEL, label, None, None, None, comment)
                    self.context.records.append(record)
                    continue
                fields = fields[1:]
            else:
                if line.startswith(' ') and line.strip(' ').startswith('+') or line.strip(' ').startswith('-'):
                    pseudolabel = fields[0]
                    fields = fields[1:]
            try:
                opcode = fields[0]
            except:
                print self.context.srcfile, self.context.linenum
                print line
                print fields
                raise
            operands = " " .join(fields[1:])
            if operands == "":
                operands = None
            else:
                operands = operands.strip().split()

            self.context.currentRecord = self._makeNewRecord(srcline, RecordType.NONE, label, pseudolabel, opcode, operands, comment)
            if self.context.mode == OpcodeType.EXTENDED and opcode not in self.context.opcodes[OpcodeType.EXTENDED]:
                self.context.error("missing EXTEND before extended instruction")
            else:
                self.parse(label, opcode, operands)
            self.context.records.append(self.context.currentRecord)

    def parse(self, label, opcode, operands):
        try:
            # Check for any outstanding interpretive operands first, i.e. until interpArgs reaches zero.
            if opcode in self.context.opcodes[OpcodeType.INTERPRETIVE]:
                self.context.opcodes[OpcodeType.INTERPRETIVE][opcode].parse(self.context, operands)
            else:
                newoperands = [ opcode ]
                if operands:
                    newoperands.extend(operands)
                gotone = Interpretive.parseOperand(self.context, newoperands)
                if gotone:
                    return
            if opcode in self.context.opcodes[OpcodeType.DIRECTIVE]:
                self.context.opcodes[OpcodeType.DIRECTIVE][opcode].parse(self.context, operands)
            if opcode in self.context.opcodes[self.context.mode]:
                self.context.opcodes[self.context.mode][opcode].parse(self.context, operands)
            if label != None and self.context.addSymbol == True:
                if not self.context.reparse:
                    self.context.symtab.add(label, operands, self.context.loc)
                else:
                    self.context.symtab.update(label, operands, self.context.loc)
        except:
            self.error("Exception processing line:")
            raise

    def reparse(self, recordIndex):
        "Reparse a ParserRecord, without affecting assembler state. Return the generated code words, if any."
        record = self.context.records[recordIndex]
        self.context.reparse = True
        saveRecord = self.context.currentRecord
        self.context.currentRecord = record
        self.parse(record.label, record.opcode, record.operands)
        self.context.records[recordIndex] = self.context.currentRecord
        self.context.currentRecord = saveRecord
        self.context.log("updated record %d: %s" % (recordIndex, self.context.records[recordIndex]))
        self.context.reparse = False
        
    def resolve(self, maxPasses=10):
        self.context.symtab.resolve(maxPasses)
        numRecords = len(self.context.records)
        self.context.log("updating %d parser records..." % (numRecords))
        nUndefs = nPrevUndefs = 0
        for i in range(maxPasses):
            nPrevUndefs = nUndefs
            nUndefs = 0
            for j in range(numRecords):
                record = self.context.records[j]
                if not record.complete:
                    nUndefs += 1
                    if RecordType.isReparseable(record.type):
                        self.reparse(j)
            self.context.log("pass %d: %d incomplete parser records" % (i, nUndefs))
            if nUndefs == 0:
                self.context.log("all parser records complete")
                break
            if nUndefs == nPrevUndefs:
                self.context.error("no progress resolving parser records", True)
                break

    def fatal(self, text):
        self.error(text)
        sys.exit(1)

    def error(self, text, noSource=False):
        if noSource:
            msg = "error: %s" % (text) 
        else:
            msg = "%s, line %d, error: %s\n" % (self.context.currentRecord.srcfile, self.context.currentRecord.linenum, text) 
            msg += "%s" % self.context.currentRecord.srcline
        print >>sys.stderr, msg
        self.log(msg)

    def syntax(self, text):
        self.error("syntax error: %s" % text)

    def warn(self, text):
        msg = "%s, line %d, warning: %s" % (self.context.currentRecord.srcfile, self.context.currentRecord.linenum, text)
        print >>sys.stderr, msg
        self.log(msg)

    def info(self, text):
        if self.context.currentRecord:
            msg = "%s, line %d, %s" % (self.context.currentRecord.srcfile, self.context.currentRecord.linenum, text)
        else:
            msg = "%s" % (text)
        if self.context.verbose:
            print msg
        self.log(msg)

    def log(self, text):
        if self.context.logging:
            print >>self.context.logfile, "%s" % (text)
