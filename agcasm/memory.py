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

from architecture import Architecture

class MemoryType:
    ERASABLE    = 0
    FIXED       = 1
    NONEXISTENT = 2

class BankType:
    UNSWITCHED  = 0
    SWITCHED    = 1
    NONEXISTENT = 2

class BankDescriptor:
    def __init__(self, startaddr, memtype, banktype=None, banknum=None, size=0, name=None, superbank=None):
        self.startaddr = startaddr
        self.memtype = memtype
        self.banktype = banktype
        self.banknum = banknum
        self.size = size
        self.name = None
        if name:
            self.name = name
        else:
            if banknum:
                self.name = "%03o" % banknum
        self.superbank = superbank

    def __str__(self):
        return "%06o %d %d %03o %05o" % (self.startaddr, self.memtype, self.banktype, self.banknum, self.size)
        
# Memory Map
MAPS = {
    # Each entry contains (start_address, size, number)
    Architecture.AGC4_B1: {
    }, 
    Architecture.AGC4_B2: {
        0000000: BankDescriptor(0000000, MemoryType.ERASABLE, BankType.UNSWITCHED, 00,  0400, "E0"),
        0000400: BankDescriptor(0000400, MemoryType.ERASABLE, BankType.UNSWITCHED, 01,  0400, "E1"),
        0001000: BankDescriptor(0001000, MemoryType.ERASABLE, BankType.UNSWITCHED, 02,  0400, "E2"),
        0001400: BankDescriptor(0001400, MemoryType.ERASABLE, BankType.SWITCHED,   03,  0400, "E3"),
        0002000: BankDescriptor(0002000, MemoryType.ERASABLE, BankType.SWITCHED,   04,  0400, "E4"),
        0002400: BankDescriptor(0002400, MemoryType.ERASABLE, BankType.SWITCHED,   05,  0400, "E5"),
        0003000: BankDescriptor(0003000, MemoryType.ERASABLE, BankType.SWITCHED,   06,  0400, "E6"),
        0003400: BankDescriptor(0003400, MemoryType.ERASABLE, BankType.SWITCHED,   07,  0400, "E7"),
        0004000: BankDescriptor(0004000, MemoryType.FIXED,    BankType.UNSWITCHED, 002, 02000),
        0006000: BankDescriptor(0006000, MemoryType.FIXED,    BankType.UNSWITCHED, 003, 02000),
        0010000: BankDescriptor(0010000, MemoryType.FIXED,    BankType.SWITCHED,   000, 02000),
        0012000: BankDescriptor(0012000, MemoryType.FIXED,    BankType.SWITCHED,   001, 02000),
        0014000: BankDescriptor(0014000, MemoryType.NONEXISTENT),        
        0016000: BankDescriptor(0016000, MemoryType.NONEXISTENT),        
        0020000: BankDescriptor(0020000, MemoryType.FIXED,    BankType.SWITCHED,   004, 02000),
        0022000: BankDescriptor(0022000, MemoryType.FIXED,    BankType.SWITCHED,   005, 02000),
        0024000: BankDescriptor(0024000, MemoryType.FIXED,    BankType.SWITCHED,   006, 02000),
        0026000: BankDescriptor(0026000, MemoryType.FIXED,    BankType.SWITCHED,   007, 02000),
        0030000: BankDescriptor(0030000, MemoryType.FIXED,    BankType.SWITCHED,   010, 02000),
        0032000: BankDescriptor(0032000, MemoryType.FIXED,    BankType.SWITCHED,   011, 02000),
        0034000: BankDescriptor(0034000, MemoryType.FIXED,    BankType.SWITCHED,   012, 02000),
        0036000: BankDescriptor(0036000, MemoryType.FIXED,    BankType.SWITCHED,   013, 02000),
        0040000: BankDescriptor(0040000, MemoryType.FIXED,    BankType.SWITCHED,   014, 02000),
        0042000: BankDescriptor(0042000, MemoryType.FIXED,    BankType.SWITCHED,   015, 02000),
        0044000: BankDescriptor(0044000, MemoryType.FIXED,    BankType.SWITCHED,   016, 02000),
        0046000: BankDescriptor(0046000, MemoryType.FIXED,    BankType.SWITCHED,   017, 02000),
        0050000: BankDescriptor(0050000, MemoryType.FIXED,    BankType.SWITCHED,   020, 02000),
        0052000: BankDescriptor(0052000, MemoryType.FIXED,    BankType.SWITCHED,   021, 02000),
        0054000: BankDescriptor(0054000, MemoryType.FIXED,    BankType.SWITCHED,   022, 02000),
        0056000: BankDescriptor(0056000, MemoryType.FIXED,    BankType.SWITCHED,   023, 02000),
        0060000: BankDescriptor(0060000, MemoryType.FIXED,    BankType.SWITCHED,   024, 02000),
        0062000: BankDescriptor(0062000, MemoryType.FIXED,    BankType.SWITCHED,   025, 02000),
        0064000: BankDescriptor(0064000, MemoryType.FIXED,    BankType.SWITCHED,   026, 02000),
        0066000: BankDescriptor(0066000, MemoryType.FIXED,    BankType.SWITCHED,   027, 02000),
        0070000: BankDescriptor(0070000, MemoryType.FIXED,    BankType.SWITCHED,   030, 02000, 0),
        0072000: BankDescriptor(0072000, MemoryType.FIXED,    BankType.SWITCHED,   031, 02000, 0),
        0074000: BankDescriptor(0074000, MemoryType.FIXED,    BankType.SWITCHED,   032, 02000, 0),
        0076000: BankDescriptor(0076000, MemoryType.FIXED,    BankType.SWITCHED,   033, 02000, 0),
        0100000: BankDescriptor(0100000, MemoryType.FIXED,    BankType.SWITCHED,   034, 02000, 0),
        0102000: BankDescriptor(0102000, MemoryType.FIXED,    BankType.SWITCHED,   035, 02000, 0),
        0104000: BankDescriptor(0104000, MemoryType.FIXED,    BankType.SWITCHED,   036, 02000, 0),
        0106000: BankDescriptor(0106000, MemoryType.FIXED,    BankType.SWITCHED,   037, 02000, 0),
        0110000: BankDescriptor(0110000, MemoryType.FIXED,    BankType.SWITCHED,   040, 02000, 1),
        0112000: BankDescriptor(0112000, MemoryType.FIXED,    BankType.SWITCHED,   041, 02000, 1),
        0114000: BankDescriptor(0114000, MemoryType.FIXED,    BankType.SWITCHED,   042, 02000, 1),
        0116000: BankDescriptor(0116000, MemoryType.FIXED,    BankType.SWITCHED,   043, 02000, 1)
    } 
}


class MemoryMap:
    def __init__(self, arch, verbose=False):
        self.verbose = verbose
        self.arch = arch
        self.memmap = MAPS[arch]
        self.banks = { MemoryType.ERASABLE: {}, MemoryType.FIXED: {} }
        for startaddr in self.memmap:
            if self.memmap[startaddr].memtype == MemoryType.ERASABLE:
                self.banks[MemoryType.ERASABLE][self.memmap[startaddr].banknum] = self.memmap[startaddr]
            elif self.memmap[startaddr].memtype == MemoryType.FIXED:
                self.banks[MemoryType.FIXED][self.memmap[startaddr].banknum] = self.memmap[startaddr]

    def __str__(self):
        text = ""
        for bank in self.memmap:
            if bank.memtype == MemoryType.NONEXISTENT:
                continue
            text += "%s"  % str(bank)
        return text
            
    def _findBank(self, pa):
        bank = None
        found = False
        addrs = self.memmap.keys()
        addrs.sort()
        for startaddr in addrs:
            if pa < startaddr + self.memmap[startaddr].size:
                found = True
                break
        
        if found:
            bank = self.memmap[startaddr]
       
        return bank
        
    def segmentedToPseudo(self, banktype, bank, address=0):
        pa = self.banks[banktype][bank].startaddr + address
        return pa
    
    def segmentedToString(self, bank, address=0):
        return "%02o,%04o" % (bank, address)
        
    def pseudoToSegmented(self, pa):
        retval = (None, 0)
        if pa != None:
            bank = self._findBank(pa)
            if bank:
                offset = pa - bank.startaddr
                retval = (bank.banknum, offset)
        return retval
    
    def pseudoToString(self, pa):
        if pa != None:
            return "%06o" % (pa)
        else:
            return "undef "
    
    def getBankNumber(self, pa):
        banknum = None
        bank = self._findBank(pa)
        if bank:
            banknum = bank.banknum
        return banknum
    
    def getBankType(self, pa):
        memtype = None
        bank = self._findBank(pa)
        if bank:
            memtype = bank.memtype
        return memtype
    
    def getBankSize(self, pa):
        size = None
        bank = self._findBank(pa)
        if bank:
            size = bank.size
        return size

    def isFixed(self, pa):
        memtype = None
        bank = self._findBank(pa)
        if bank:
            memtype = bank.memtype
        return (memtype == MemoryType.FIXED)
    
    def isErasable(self, pa):
        memtype = None
        bank = self._findBank(pa)
        if bank:
            memtype = bank.memtype
        return (memtype == MemoryType.ERASABLE)
    
    def isChannel(self, pa):
        retval = False
        if 0 <= pa <= 0777:
            retval = True
        return retval
