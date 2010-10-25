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
import time
from opcode import OpcodeType
from parser_record import ParserRecord
from record_type import RecordType
from interpretive import Interpretive

class Assembler:
    """Class defining an AGC assembler."""

    def __init__(self, context):
        self.context = context
        self.context.fatal = self.fatal
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
        sfile = open(srcfile)
        lines = sfile.readlines()
        self.context.log(7, "assemble: file %s, lines %d" % (srcfile, len(lines)))
        sfile.close()
        for line in lines:
            if line.endswith('\n'):
                line = line[:-1]
            srcline = line.expandtabs(8)
            self.context.srcline = srcline
            self.context.linenum += 1
            self.context.global_linenum += 1
            self.context.code = None
            self.context.addSymbol = True
            self.context.messages = []
            label = None
            pseudolabel = None
            opcode = None
            operands = None
            comment = None

            self.context.log(7, "assemble: %d/%d (%d) \"%s\"" % (self.context.linenum, len(lines), self.context.global_linenum, self.context.srcline))

            if line.startswith('$'):
                modname = line[1:].split()[0]
                if not os.path.isfile(modname):
                    self.fatal("File \"%s\" does not exist" % modname, source=False)
                record = self._makeNewRecord(srcline, RecordType.INCLUDE, None, None, None, None, comment)
                record.complete = True
                self.context.records.append(record)
                self.context.log(7, "assemble: added record %d" % (len(self.context.records) - 1))
                self.assemble(modname)
                continue

            if len(line.strip()) == 0:
                record = self._makeNewRecord(srcline, RecordType.BLANK, None, None, None, None, None)
                record.complete = True
                self.context.records.append(record)
                self.context.log(7, "assemble: added record %d" % (len(self.context.records) - 1))
                continue

            if line.strip().startswith('#'):
                comment = line
                record = self._makeNewRecord(srcline, RecordType.COMMENT, None, None, None, None, comment)
                record.complete = True
                self.context.records.append(record)
                self.context.log(7, "assemble: added record %d" % (len(self.context.records) - 1))
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
                    self.context.symtab.add(label, None, self.context.loc, 0, RecordType.LABEL)
                    record = self._makeNewRecord(srcline, RecordType.LABEL, label, None, None, None, comment)
                    record.complete = True
                    self.context.records.append(record)
                    self.context.log(7, "assemble: added record %d" % (len(self.context.records) - 1))
                    continue
                fields = fields[1:]
            else:
                if line.startswith(' +') or line.startswith('\t+') or line.startswith(' \t+') or \
                   line.startswith(' -') or line.startswith('\t-') or line.startswith(' \t-'):
                    # It's a pseudo-label.
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
                if opindex == 24:
                    newoperands = [ opcode ]
                    if operands != None:
                        newoperands.extend(operands)
                    if opcode not in self.context.opcodes[OpcodeType.DIRECTIVE] and \
                       (opcode not in self.context.opcodes[self.context.mode] or \
                       (opcode in self.context.opcodes[self.context.mode] and opcode != self.context.opcodes[self.context.mode][opcode].mnemonic)) or \
                       opcode == "TC":
                        # Handle stand-alone interpretive operands.
                        operands = newoperands
                        opcode = None

            self.context.log(7, "assemble: label=%s opcode=%s operands=%s [%d]" % (label, opcode, operands, opindex))

            self.context.previousRecord = self.context.currentRecord
            self.context.currentRecord = self._makeNewRecord(srcline, RecordType.NONE, label, pseudolabel, opcode, operands, comment)
            if line.startswith('\t+') or line.startswith(' \t+') or \
               line.startswith('\t-') or line.startswith(' \t-'):
                # It's a pseudo-label.
                self.context.warn("bad indentation")
            if opindex != -1:
                if opindex != 16 and opindex != 24:
                    self.context.error("bad indentation")
                if opindex == 24:
                    # TC is also used as an interpretive label.
                    if opcode != None:
                        self.context.warn("bad indentation")
            self.parse(label, opcode, operands)
            self.context.currentRecord.update()
            self.context.records.append(self.context.currentRecord)
            self.context.log(7, "assemble: added record %d" % (len(self.context.records) - 1))

    def parse(self, label, opcode, operands):
        try:
            self.context.log(7, "parse: label=%s opcode=%s operands=%s" % (label, opcode, operands))

            preloc = self.context.loc

            if opcode == None:
                Interpretive.parseOperand(self.context, operands)
            else:
                if opcode in self.context.opcodes[OpcodeType.INTERPRETIVE]:
                    self.context.opcodes[OpcodeType.INTERPRETIVE][opcode].parse(self.context, operands)
                elif opcode in self.context.opcodes[OpcodeType.DIRECTIVE]:
                    self.context.opcodes[OpcodeType.DIRECTIVE][opcode].parse(self.context, operands)
                elif opcode in self.context.opcodes[self.context.mode]:
                    if self.context.interpArgs > 0 or self.context.interpArgCount > 0:
                        self.context.log(5, "parse: resetting interpArgs, %d -> %d" % (self.context.interpArgs, 0))
                        self.context.interpArgs = 0
                        self.context.interpArgCount = 0
                        self.context.interpArgTypes = [ None, None, None, None ]
                        self.context.interpArgCodes = [ 0, 0, 0, 0 ]
                        self.context.interpArgIncrement = [ False, False, False, False ]
                    self.context.opcodes[self.context.mode][opcode].parse(self.context, operands)
                else:
                    self.error("invalid opcode")

            if label != None and self.context.addSymbol == True and self.context.passnum == 0:
                if not self.context.reparse:
                    numWords = self.context.loc - preloc
                    self.context.symtab.add(label, operands, preloc, length=numWords, type=self.context.currentRecord.type)
                else:
                    self.context.symtab.update(label, operands, preloc, length=numWords, type=self.context.currentRecord.type)
        except:
            self.error("Exception processing line:")
            raise

    def parseRecord(self, recordIndex):
        "Parse a ParserRecord, without affecting assembler state. Return the generated code words, if any."
        record = self.context.records[recordIndex]
        self.context.reparse = True
        saveRecord = self.context.currentRecord
        savePrevRecord = self.context.previousRecord
        self.context.currentRecord = record
        if recordIndex >= 1:
            self.context.previousRecord = self.context.records[recordIndex - 1]
        self.context.load(record, partial=False)
        self.context.currentRecord.errorMsg = None
        self.context.currentRecord.warningMsg = None
        self.parse(record.label, record.opcode, record.operands)
        self.context.records[recordIndex] = self.context.currentRecord
        self.context.currentRecord = saveRecord
        self.context.previousRecord = savePrevRecord
        self.context.reparse = False
        self.context.log(6, "updated record %06d: %s" % (recordIndex, self.context.records[recordIndex]))

    def resolve(self, maxPasses=10):
        startTime = time.time()
        self.context.symtab.resolve(maxPasses)
        if self.context.debug:
            endTime = time.time()
            delta = endTime - startTime
            print "Symbol resolution: %3.2f seconds" % delta

        startTime = time.time()
        numRecords = len(self.context.records)
        self.context.log(3, "updating %d parser records..." % (numRecords))
        nUndefs = nPrevUndefs = 0
        for i in range(maxPasses):
            self.context.passnum = i + 1
            self.context.reset()
            nPrevUndefs = nUndefs
            nUndefs = 0
            undefRecords = []
            for j in range(numRecords):
                record = self.context.records[j]
                if record.isParseable():
                    self.context.currentRecord = record
                    self.context.previousRecord = self.context.records[j-1]
                    self.context.load(record)
                    self.context.log(8, "resolve: %s" % (record.srcline))
                    self.parse(record.label, record.opcode, record.operands)
                    self.context.records[j] = self.context.currentRecord
                    if not record.isComplete():
                        nUndefs += 1
                        undefRecords.append(record)
            self.context.log(3, "%d incomplete parser records" % (nUndefs))
            if nUndefs == 0:
                self.context.log(3, "all parser records complete")
                break
            if nUndefs == nPrevUndefs:
                self.context.error("no progress resolving parser records, %d undefined records" % nUndefs, source=False)
                for urec in undefRecords:
                    #self.context.error("undefined symbol in line:\n%s" % urec, source=True)
                    urec.printMessages()
                break
        if self.context.debug:
            endTime = time.time()
            delta = endTime - startTime
            print "Pass 2: %3.2f seconds" % delta

    def fatal(self, text, source=True):
        self.error(text, source, fatal=True)
        sys.exit(1)

    def _error(self, prefix, text, source=True, fatal=False, count=True):
        msg = ""
        if source:
            msg = "%s, line %d (%d), " % (self.context.currentRecord.srcfile, self.context.linenum, self.context.global_linenum)
        msg += "%s %s" % (prefix, text)
        if source:
            msg += ':'
        self.context.currentRecord.errorMsg = msg
        if source:
            msg += "\n%s" % self.context.srcline
        if fatal:
            print >>sys.stderr, msg
        self.log(1, msg)
        if count:
            self.context.errors += 1

    def error(self, text, source=True, fatal=False, count=True):
        self._error("error:", text, source, fatal, count)

    def syntax(self, text, source=True, count=True):
        self._error("syntax error:", text, source, count)

    def warn(self, text, source=True, count=True):
        msg = ""
        if source:
            msg = "%s, line %d (%d), " % (self.context.currentRecord.srcfile, self.context.linenum, self.context.global_linenum)
        msg += "warning: %s" % (text)
        if source:
            msg += ':'
        self.context.currentRecord.warningMsg = msg
        if source:
            msg += "\n%s" % self.context.srcline
        self.log(2, msg)
        if count:
            self.context.warnings += 1

    def info(self, text, source=True):
        msg = ""
        if source:
            msg = "%s, line %d (%d), " % (self.context.currentRecord.srcfile, self.context.linenum, self.context.global_linenum)
        msg += "%s" % (text)
        if source:
            msg += "\n%s" % self.context.srcline
        if self.context.verbose:
            print msg
        self.log(3, msg)

    def log(self, level, text):
        if level <= self.context.logLevel:
            print >>self.context.logfile, "[Pass %03d] %s" % (self.context.passnum + 1, text)
