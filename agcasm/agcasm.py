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

class Architecture:
    AGC1    = 0    # Mod1
    AGC2C   = 1    # Mod2C
    AGC3    = 2    # AGC3
    AGC4_B1 = 3    # AGC4 Block I
    AGC4_B2 = 4    # AGC4 Block II

class OpcodeType:
    BASIC = 0
    EXTENDED = 1
    BOTH = 2

class OperandType:
    NONE        = 0    # No operand.
    ERASABLE_10 = 1    # 10-bit erasable address.
    ERASABLE_12 = 2    # 12-bit erasable address.
    FIXED_9     = 3    # 9-bit fixed address. Only used by EDRUPT?
    FIXED_12    = 4    # 12-bit fixed address.
    GENERAL_12  = 5    # 12-bit general address (fixed or erasable).
    CHANNEL_9   = 6    # 9-bit I/O channel address.
    
class Instruction:
    def __init__(self, mnemonic, opcode, extend, operandType):
        self.mnemonic = mnemonic
        self.opcode = opcode
        self.extend = extend
        self.operandType = operandType
    
instructions = { 
    Architecture.AGC4_B2 : { 
        Instruction("AD",     060000,  OpcodeType.BASIC,     OperandType.ERASABLE_12), 
        Instruction("ADS",    026000,  OpcodeType.EXTENDED,  OperandType.ERASABLE_10),
        Instruction("AUG",    024000,  OpcodeType.EXTENDED,  OperandType.ERASABLE_10), 
        Instruction("BZF",    010000,  OpcodeType.EXTENDED,  OperandType.FIXED_12),  
        Instruction("BZMF",   060000,  OpcodeType.EXTENDED,  OperandType.FIXED_12),
        Instruction("CA",     030000,  OpcodeType.BASIC,     OperandType.GENERAL_12),
        Instruction("CAE",    030000,  OpcodeType.BASIC,     OperandType.ERASABLE_12),
        Instruction("CAF",    030000,  OpcodeType.BASIC,     OperandType.FIXED_12),
        Instruction("CCS",    010000,  OpcodeType.BASIC,     OperandType.ERASABLE_10),
        Instruction("COM",    040000,  OpcodeType.BASIC,     OperandType.NONE),
        Instruction("CS",     040000,  OpcodeType.BASIC,     OperandType.GENERAL_12),
        Instruction("DAS",    020001,  OpcodeType.BASIC,     OperandType.ERASABLE_10),
        Instruction("DCA",    030001,  OpcodeType.EXTENDED,  OperandType.GENERAL_12),
        Instruction("DCOM",   040001,  OpcodeType.EXTENDED,  OperandType.NONE),
        Instruction("DDOUBL", 020001,  OpcodeType.BASIC,     OperandType.NONE),
        Instruction("DIM",    026000,  OpcodeType.EXTENDED,  OperandType.ERASABLE_10),
        Instruction("DOUBLE", 060000,  OpcodeType.BASIC,     OperandType.NONE),
        Instruction("DTCB",   052006,  OpcodeType.BASIC,     OperandType.NONE),
        Instruction("DTCF",   052005,  OpcodeType.BASIC,     OperandType.NONE),
        Instruction("DV",     010000,  OpcodeType.BASIC,     OperandType.GENERAL_12),
        Instruction("DXCH",   050001,  OpcodeType.BASIC,     OperandType.ERASABLE_10
        Instruction("EDRUPT", 007000,  OpcodeType.EXTENDED,  OperandType.FIXED_9),
        Instruction("EXTEND", 000006,  OpcodeType.BASIC,     OperandType.NONE),
        Instruction("INCR",   024000,  OpcodeType.BASIC,     OperandType.NONE),
        Instruction("INDEX",  050000,  OpcodeType.BASIC,     OperandType.ERASABLE_10),
        Instruction("INDEX",  050000,  OpcodeType.EXTENDED,  OperandType.GENERAL_12),
        Instruction("INHINT", 000004,  OpcodeType.BASIC,     OperandType.NONE),
        Instruction("LXCH",   022000,  OpcodeType.BASIC,     OperandType.ERASABLE_10),
        Instruction("MASK",   070000,  OpcodeType.BASIC,     OperandType.GENERAL_12),
        Instruction("MP",     070000,  OpcodeType.EXTENDED,  OperandType.GENERAL_12),
        Instruction("MSK",    070000,  OpcodeType.BASIC,     OperandType.GENERAL_12),    # Alias for MASK.
        Instruction("MSU",    020000,  OpcodeType.EXTENDED,  OperandType.ERASABLE_10),
        Instruction("NDX",    050000,  OpcodeType.BASIC,     OperandType.ERASABLE_10),
        Instruction("NDX",    050000,  OpcodeType.EXTENDED,  OperandType.GENERAL_12),
        Instruction("NOOP",   030000,  OpcodeType.BASIC,     OperandType.NONE),          # Erasable memory: CA A
        Instruction("NOOP",   010000,  OpcodeType.BASIC,     OperandType.NONE),          # Fixed memory: TCF nextaddr
        Instruction("OVSK",   054000,  OpcodeType.BASIC,     OperandType.NONE),
        Instruction("QXCH",   022000,  OpcodeType.EXTENDED,  OperandType.ERASABLE_10),
        Instruction("RAND",   002000,  OpcodeType.EXTENDED,  OperandType.CHANNEL),
        Instruction("READ",   000000,  OpcodeType.EXTENDED,  OperandType.CHANNEL),
        Instruction("RELINT", 000003,  OpcodeType.BASIC,     OperandType.NONE),
        Instruction("RESUME", 050017,  OpcodeType.BASIC,     OperandType.NONE),
        Instruction("RETURN", 000002,  OpcodeType.BASIC,     OperandType.NONE),
        Instruction("ROR",    004000,  OpcodeType.EXTENDED,  OperandType.CHANNEL),
        Instruction("RXOR",   006000,  OpcodeType.EXTENDED,  OperandType.CHANNEL),
        Instruction("SQUARE", 070000,  OpcodeType.EXTENDED,  OperandType.NONE),
        Instruction("SU",     060000,  OpcodeType.EXTENDED,  OperandType.ERASABLE_10),
        Instruction("TC",     000000,  OpcodeType.BASIC,     OperandType.GENERAL_12),
        Instruction("TCAA",   054005,  OpcodeType.BASIC,     OperandType.NONE),
        Instruction("TCF",    010000,  OpcodeType.BASIC,     OperandType.FIXED_12),
        Instruction("TCR",    000000,  OpcodeType.BASIC,     OperandType.GENERAL_12),
        Instruction("TS",     054000,  OpcodeType.BASIC,     OperandType.ERASABLE_10),
        Instruction("WAND",   003000,  OpcodeType.EXTENDED,  OperandType.CHANNEL),
        Instruction("WOR",    005000,  OpcodeType.EXTENDED,  OperandType.CHANNEL),
        Instruction("WRITE",  001000,  OpcodeType.EXTENDED,  OperandType.CHANNEL),
        Instruction("XCH",    056000,  OpcodeType.BASIC,     OperandType.ERASABLE_10),
        Instruction("XLQ",    000001,  OpcodeType.BASIC,     OperandType.NONE),
        Instruction("XXALQ",  000000,  OpcodeType.BASIC,     OperandType.NONE),
        Instruction("ZL",     022007,  OpcodeType.BASIC,     OperandType.NONE),
        Instruction("ZQ",     022007,  OpcodeType.EXTENDED,  OperandType.NONE)
    }
}

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
