#!/usr/bin/env python

# Copyright 2010 Jim lawton <jim dot lawton at gmail dot com>
# 
# This file is part of yaAGC. 
#
# yaAGC is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# yaAGC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with yaAGC; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import os
import sys
import glob
from optparse import OptionParser

class Assembler:
    """Class defining an AGC assembler."""

    def __init__(self, listfile, binfile):
        self.listfile = listfile
        self.binfile = binfile
    
    def assemble(self, srcfile, source=None, symtab=None, code=None):
        print "Assembling", srcfile
        if source == None:
            source = []
        if symtab == None:
            symtab = {}
        if code == None:
            code = {}
        lines = open(srcfile).readlines()
        for line in lines:
            source.append(line)
            if line.startswith('$'):
                modname = line[1:].split()[0]
                if not os.path.isfile(modname):
                    print >>sys.stderr, "File \"%s\" does not exist" % modname
                    sys.exit(1)
                self.assemble(modname, symtab, code)
            # Real parsing starts here.
    

def main():

    parser = OptionParser("usage: %prog [options] src_file [src_file...]")
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
    binfile = open(args[0] + ".bin", 'wb')

    assembler = Assembler(listfile, binfile)

    for arg in args:
        assembler.assemble(arg)

if __name__=="__main__":
    sys.exit(main())
