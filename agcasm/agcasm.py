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
import traceback
from optparse import OptionParser
from architecture import Architecture
from assembler import Assembler
from context import Context
from binary import ObjectCode

def main():
    totalTime = 0.0
    startTime = time.time()

    parser = OptionParser("usage: %prog [options] src_file [src_file...]")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose output.")
    parser.add_option("-l", "--log", dest="logLevel", default=0, help="Print detailed log information.")
    parser.add_option("-t", "--test", action="store_true", dest="test", default=False, help="Run assembler test code.")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False, help="Turn on assembler debugging code.")
    parser.add_option("-s", "--syntax-only", action="store_true", dest="syntaxOnly", default=False, help="Exit after checking syntax.")
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("At least one source file must be supplied!")
        sys.exit(1)

    sources = []
    for arg in args:
        sources.append(arg)
        if not os.path.isfile(arg):
            parser.error("File \"%s\" does not exist" % arg)
            sys.exit(1)

    buildname = os.path.basename(os.getcwd())
    
    firstfile = args[0]
    firstfilename = args[0].split('.')[0]
    
    listfile = open(firstfilename + ".lst", 'w')
    symtabfile = open(firstfilename + ".symtab", 'w')
    binfile = open(firstfile + ".bin", 'wb')
    logfile = open(firstfilename + ".log", 'w')

    context = Context(Architecture.AGC4_B2, listfile, binfile, options, int(options.logLevel), logfile)
    assembler = Assembler(context)
    context.assembler = assembler

    if options.debug:
        print "Build:", buildname 
        endTime = time.time()
        delta = endTime - startTime
        totalTime += delta
        print "Initialisation: %3.2f seconds" % delta

    assembler.info("Simple AGC Assembler, v0.1", source=False)
    assembler.info("", source=False)

    startTime = time.time()
    for arg in args:
        try:
            assembler.assemble(arg)
        except:
            print >>sys.stderr
            print >>sys.stderr, "EXCEPTION:"
            traceback.print_exc(file=sys.stderr)
            print >>sys.stderr, "Context:"
            print >>sys.stderr, context
            raise
    if options.debug:
        endTime = time.time()
        delta = endTime - startTime
        totalTime += delta
        print "Pass 1: %3.2f seconds" % delta

    context.saveCurrentBank()

    if options.syntaxOnly == False and context.errors == 0:
        assembler.info("Resolving symbols...", source=False)
        startTime = time.time()
        try:
            assembler.resolve()
        except:
            assembler.log(1, "EXCEPTION:\n%s" % context)
            raise
        if options.debug:
            endTime = time.time()
            delta = endTime - startTime
            totalTime += delta

    for record in assembler.context.records:
        record.printMessages()

    assembler.info("Writing listing...", source=False)
    startTime = time.time()
    print >>listfile
    print >>listfile, "Listing"
    print >>listfile, "-------"
    for record in assembler.context.records:
        print >>listfile, record
    if options.debug:
        endTime = time.time()
        delta = endTime - startTime
        totalTime += delta
        print "Write listing: %3.2f seconds" % delta

    if not options.syntaxOnly:
        assembler.info("Writing symbol table listing...", source=False)
        startTime = time.time()
        print >>listfile
        print >>listfile, "Symbol Table"
        print >>listfile, "------------"
        assembler.context.symtab.printTable(listfile)
        if options.debug:
            endTime = time.time()
            delta = endTime - startTime
            totalTime += delta
            print "Write symbol table listing: %3.2f seconds" % delta

    if not options.syntaxOnly and context.errors == 0:
        assembler.info("Writing symbol table...", source=False)
        startTime = time.time()
        assembler.context.symtab.write(symtabfile)
        if options.debug:
            endTime = time.time()
            delta = endTime - startTime
            totalTime += delta
            print "Write symbol table: %3.2f seconds" % delta

    if context.errors == 1:
        msg = "1 error, "
    else:
        msg = "%d errors, " % (context.errors)
    if context.warnings == 1:
        msg += "1 warning, "
    else:
        msg += "%d warnings, " % (context.warnings)
    assembler.info(msg, source=False)
    print msg

    if not options.syntaxOnly:
        if options.test:
            startTime = time.time()

            # FIXME: Temporary hack
            # Check generated symbols against the symtab generated by yaYUL.

            assembler.info("Checking symbol table against yaYUL version...", source=False)
            from artemis072_symbols import ARTEMIS_SYMBOLS
            from memory import MemoryType

            nsyms = assembler.context.symtab.getNumSymbols()
            check_nsyms = len(ARTEMIS_SYMBOLS.keys())
            assembler.info("Number of symbols: yaYUL=%d pyagc=%d" % (check_nsyms, nsyms), source=False)

            my_syms = []
            other_syms = []
            common_syms = []

            for sym in assembler.context.symtab.keys():
                if sym in ARTEMIS_SYMBOLS.keys():
                    common_syms.append(sym)
                else:
                    if sym != "FIXED":
                        my_syms.append(sym)

            for sym in ARTEMIS_SYMBOLS.keys():
                if sym not in assembler.context.symtab.keys():
                    if not sym.startswith('$') and sym != "'":
                        other_syms.append(sym)

            if len(my_syms) != 0 or len(other_syms) != 0:
                assembler.error("incorrect number of symbols, expected %d, got %d" % (check_nsyms, nsyms), source=False)

            if len(my_syms) > 0:
                assembler.error("symbols defined that should not be defined: %s" % my_syms, source=False)

            if len(other_syms) > 0:
                assembler.error("symbols not defined that should be defined: %s" % other_syms, source=False)

            errcount = 0
            bad_syms = {}

            for sym in common_syms:
                entry = assembler.context.symtab.lookup(sym)
                if entry == None:
                    assembler.error("symbol %-8s not defined" % entry, source=False)
                pa = entry.value
                aval = ARTEMIS_SYMBOLS[sym]
                if ',' in aval:
                    bank = aval.split(',')[0]
                    type = MemoryType.FIXED
                    if bank.startswith('E'):
                        bank = bank[1:]
                        type = MemoryType.ERASABLE
                    bank = int(bank, 8)
                    offset = int(aval.split(',')[1], 8)
                    check_pa = context.memmap.segmentedToPseudo(type, bank, offset, absolute=True)
                else:
                    check_pa = int(aval, 8)
                if pa != check_pa:
                    errcount += 1
                    bad_syms[pa] = (sym, check_pa)

            if errcount > 0:
                bad_addrs = bad_syms.keys()
                bad_addrs.sort()
                for pa in bad_addrs:
                    sym = bad_syms[pa][0]
                    check_pa = bad_syms[pa][1]
                    assembler.error("symbol %-8s defined as %06o %s, expected %06o %s" % (sym, pa, context.memmap.pseudoToSegmentedString(pa), check_pa, context.memmap.pseudoToSegmentedString(check_pa)), source=False)
                assembler.error("%d/%d symbols incorrectly defined" % (errcount, len(common_syms)), source=False)

            if options.debug:
                endTime = time.time()
                delta = endTime - startTime
                totalTime += delta
                print "Symbol checking: %3.2f seconds" % delta

            # FIXME: End of temporary hack

    if not options.syntaxOnly and context.errors == 0:
        assembler.info("Writing binary output...", source=False)
        startTime = time.time()
        ocode = ObjectCode(context)
        ocode.generateBuggers()
        ocode.write(binfile)
        if options.debug:
            endTime = time.time()
            delta = endTime - startTime
            totalTime += delta
            print "Binary generation: %3.2f seconds" % delta

        assembler.info("Writing rope usage...", source=False)
        startTime = time.time()
        print >>listfile
        print >>listfile
        print >>listfile, "Bank Usage"
        print >>listfile, "----------"
        print >>listfile
        ocode.writeUsage(listfile)
        if options.debug:
            endTime = time.time()
            delta = endTime - startTime
            totalTime += delta
            print "Rope usage: %3.2f seconds" % delta

        assembler.info("Writing rope image listing...", source=False)
        startTime = time.time()
        print >>listfile
        print >>listfile
        print >>listfile, "Rope Image Listing"
        print >>listfile, "------------------"
        print >>listfile
        ocode.writeListing(listfile)
        if options.debug:
            endTime = time.time()
            delta = endTime - startTime
            totalTime += delta
            print "Rope image listing: %3.2f seconds" % delta

    assembler.info("Done.", source=False)
    listfile.close()
    symtabfile.close()
    binfile.close()
    logfile.close()

    if options.debug:
        print "Total time: %3.2f seconds" % totalTime

    print "Done."

if __name__=="__main__":
    sys.exit(main())
