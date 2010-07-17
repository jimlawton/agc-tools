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
        self.info("Assembling %s" % srcfile, source=False)
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
                    self.fatal("File \"%s\" does not exist" % modname, source=False)
                record = self._makeNewRecord(srcline, RecordType.INCLUDE, None, None, None, None, comment)
                record.complete = True
                self.context.records.append(record)
                self.assemble(modname)
                continue
            
            if len(line.strip()) == 0:
                record = self._makeNewRecord(srcline, RecordType.BLANK, None, None, None, None, None)
                record.complete = True
                self.context.records.append(record)
                continue
            
            if line.strip().startswith('#'):
                comment = line
                record = self._makeNewRecord(srcline, RecordType.COMMENT, None, None, None, None, comment)
                record.complete = True
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
                    record.complete = True
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

            label_len = 0
            if label != None:
                label_len = len(label)

            if opcode != None:
                opindex = self.context.srcline.find(opcode, label_len)
            elif operands != None:
                opindex = self.context.srcline.find(operands[0], label_len)
            else:
                opindex = -1

            if opindex != -1:
                if opindex != 16 and opindex != 24:
                    self.context.error("bad indentation")
                if opindex == 24:
                    # Handle standalone interpretive operands.
                    newoperands = [ opcode ]
                    if operands != None:
                        newoperands.extend(operands)
                    operands = newoperands
                    opcode = None

            self.context.log(7, "assemble: label=%s opcode=%s operands=%s [%d]" % (label, opcode, operands, opindex))
            
            self.context.currentRecord = self._makeNewRecord(srcline, RecordType.NONE, label, pseudolabel, opcode, operands, comment)
            self.parse(label, opcode, operands)
            #self.context.currentRecord.update()
            self.context.records.append(self.context.currentRecord)

    def parse(self, label, opcode, operands):
        gotInterpArgs = False
        try:
            self.context.log(7, "parse: label=%s opcode=%s operands=%s" % (label, opcode, operands))
            
            if opcode == None:
                gotInterpArgs = Interpretive.parseOperand(self.context, operands)
            else:
                if opcode in self.context.opcodes[OpcodeType.INTERPRETIVE]:
                    self.context.opcodes[OpcodeType.INTERPRETIVE][opcode].parse(self.context, operands)
                elif opcode in self.context.opcodes[OpcodeType.DIRECTIVE]:
                    self.context.opcodes[OpcodeType.DIRECTIVE][opcode].parse(self.context, operands)
                elif opcode in self.context.opcodes[self.context.mode]:
                    self.context.opcodes[self.context.mode][opcode].parse(self.context, operands)
                else:
                    self.error("invalid opcode")

            if label != None and self.context.addSymbol == True and self.context.passnum == 0:
                if not self.context.reparse:
                    self.context.symtab.add(label, operands, self.context.loc)
                else:
                    self.context.symtab.update(label, operands, self.context.loc)
        except:
            self.error("Exception processing line:")
            raise

    def parseRecord(self, recordIndex):
        "Parse a ParserRecord, without affecting assembler state. Return the generated code words, if any."
        record = self.context.records[recordIndex]
        self.context.reparse = True
        saveRecord = self.context.currentRecord
        self.context.currentRecord = record
        self.context.load(record)
        self.parse(record.label, record.opcode, record.operands)
        self.context.records[recordIndex] = self.context.currentRecord
        self.context.currentRecord = saveRecord
        self.context.reparse = False
        self.context.log(6, "updated record %06d: %s" % (recordIndex, self.context.records[recordIndex]))
        
    def resolve(self, maxPasses=10):
        self.context.symtab.resolve(maxPasses)
        numRecords = len(self.context.records)
        self.context.log(3, "updating %d parser records..." % (numRecords))
        nUndefs = nPrevUndefs = 0
        for i in range(maxPasses):
            self.context.passnum = i + 1
            self.context.reset()
            nPrevUndefs = nUndefs
            nUndefs = 0
            for j in range(numRecords):
                record = self.context.records[j]
                if record.isParseable():
                    self.context.currentRecord = record
                    self.context.load(record)
                    self.context.log(8, "resolve: %s" % (record.srcline))
                    self.parse(record.label, record.opcode, record.operands)
                    self.context.records[j] = self.context.currentRecord
                    if not record.isComplete():
                        nUndefs += 1
            self.context.log(3, "%d incomplete parser records" % (nUndefs))
            if nUndefs == 0:
                self.context.log(3, "all parser records complete")
                break
            if nUndefs == nPrevUndefs:
                self.context.error("no progress resolving parser records", source=False)
                break

    def fatal(self, text, source=True):
        self.error(text, source)
        sys.exit(1)

    def error(self, text, source=True):
        msg = ""
        if source:
            msg = "%s, line %d (%d), " % (self.context.currentRecord.srcfile, self.context.currentRecord.linenum, self.context.global_linenum)
        msg += "error: %s" % (text) 
        if source:
            msg += "\n%s" % self.context.currentRecord.srcline
        print >>sys.stderr, msg
        self.log(1, msg)
        self.context.errors += 1

    def syntax(self, text, source=True):
        self.error("syntax error: %s" % text, source)

    def warn(self, text, source=True):
        msg = ""
        if source:
            msg = "%s, line %d (%d), " % (self.context.currentRecord.srcfile, self.context.currentRecord.linenum, self.context.global_linenum)
        msg += "warning: %s" % (text)
        if source:
            msg += "\n%s" % self.context.currentRecord.srcline
        print >>sys.stderr, msg
        self.log(2, msg)
        self.context.warnings += 1

    def info(self, text, source=True):
        msg = ""
        if source:
            msg = "%s, line %d (%d), " % (self.context.currentRecord.srcfile, self.context.currentRecord.linenum, self.context.global_linenum)
        msg += "%s" % (text)
        if source:
            msg += "\n%s" % self.context.currentRecord.srcline
        if self.context.verbose:
            print msg
        self.log(3, msg)

    def log(self, level, text):
        if level <= self.context.logLevel:
            print >>self.context.logfile, "[Pass %03d] %s" % (self.context.passnum + 1, text)
