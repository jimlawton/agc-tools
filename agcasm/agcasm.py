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
from optparse import OptionParser
from architecture import Architecture
from assembler import Assembler

def main():
    parser = OptionParser("usage: %prog [options] src_file [src_file...]")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose output.")
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

    print "Simple AGC Assembler"
    print

    listfile = open(args[0].split('.')[0] + ".lst", 'w')
    symtabfile = open(args[0].split('.')[0] + ".symtab", 'w')
    binfile = open(args[0] + ".bin", 'wb')

    assembler = Assembler(Architecture.AGC4_B2, listfile, binfile, options.verbose)

    for arg in args:
        assembler.assemble(arg)

    print "Writing listing..."
    print >>listfile 
    print >>listfile, "Listing"
    print >>listfile, "-------"
    for record in assembler.context.records:
        print >>listfile, record

    print "Writing symbol table..."
    print >>symtabfile 
    print >>symtabfile, "Symbol Table"
    print >>symtabfile, "------------"
    assembler.context.symtab.printTable(symtabfile)
    
    print "Done."

if __name__=="__main__":
    sys.exit(main())
