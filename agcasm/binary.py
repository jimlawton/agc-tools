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

import struct
from memory import MemoryType

class ObjectCode:
    """Class storing object code."""

    def __init__(self, context):
        self.context = context              # Assembler context.
        self.objectCode = {}
        for bank in self.context.memmap.getBanks(MemoryType.FIXED):
            self.objectCode[bank] = {}
            for offset in range(self.context.getBankSize(MemoryType.FIXED, bank)):
                self.objectCode[bank][offset] = 0

        for i in range(len(self.context.records)):
            record = self.context.records[i]
            if record.isGenerative():
                pa = record.address
                (bank, offset) = context.memmap.pseudoToBankOffset(pa)
                if record.code != None and len(record.code) > 0:
                    if len(record.code) >= 1:
                        self.objectCode[bank][offset] = record.code[0] & 077777
                        #context.log(4, "code for %06o (%02o,%04o): %05o" % (pa, bank, offset, self.objectCode[bank][offset]))
                    if len(record.code) == 2:
                        self.objectCode[bank][offset+1] = record.code[1] & 077777
                        #context.log(4, "code for %06o (%02o,%04o): %05o" % (pa, bank, offset+1, self.objectCode[bank][offset+1]))
                else:
                    context.error("missing object code at address %06s" % (pa), source=False)
                    return

    def generateBuggers(self):
        for bank in self.context.memmap.getBanks(MemoryType.FIXED):
            # Add bugger info to the bank.
            if bank == 2:
                offset = 04000
            elif bank == 3:
                offset = 06000
            else:
                offset = 02000

            count = self.context.getBankCount(MemoryType.FIXED, bank)

            if count < 01776:
                self.objectCode[bank][count] = count + offset
                count += 1
            if count < 01777:
                self.objectCode[bank][count] = count + offset
                count += 1
            if count < 02000:
                bugger = 0
                offset = 0
                for offset in range(count):
                    bugger = self.add(bugger, self.objectCode[bank][offset])
                if (bugger & 040000) == 0:
                    guess = self.add(bank, 077777 & ~bugger)
                else:
                    guess = self.add(077777 & ~bank, 077777 & ~bugger)
                self.objectCode[bank][count] = guess
                self.context.log(4, "bugger word %05o at (%02o,%04o)" % (guess, bank, count + 02000))

    # Convert AGC number to native format.
    @classmethod
    def convertToNative(cls, n):
        i = n
        if (n & 040000) != 0:
            i = -(077777 & ~i)
        return i

    # Add two AGC numbers.
    @classmethod
    def add(cls, n1, n2):
        # Convert from AGC 1's-complement format to the native integer.
        i1 = cls.convertToNative(n1)
        i2 = cls.convertToNative(n2)
        sum = i1 + i2

        if sum > 037777:
            sum -= 040000
            sum += 1
        elif sum < -037777:
            sum += 040000
            sum -= 1

        if sum > 037777 or sum < -037777:
            print "Arithmetic overflow."

        if sum < 0:
            sum = (077777 & ~(-sum))

        return sum

    def getBugger(self, data):
        """Return the bugger word in the supplied bank data. The bugger word is the last non-zero word."""

        index = 0
        for i in range(len(data)-1, -1, -1):
            if data[i] != 0:
                index = i
                if i == len(data)-1:
                    if data[i-1] == 0:
                        # Search farther back for bugger word.
                        for j in range(len(data)-2, -1, -1):
                            if data[j] != 0:
                                index = j
                                break
                break
        return data[index]

    def write(self, outputfile):
        count = 0
        for bank in self.context.memmap.getBanks(MemoryType.FIXED):
            self.context.log(4, "writing output for bank %02o (%d words)" % (bank, self.context.getBankSize(MemoryType.FIXED, bank)))
            count += self.context.getBankSize(MemoryType.FIXED, bank)
            for offset in range(self.context.getBankSize(MemoryType.FIXED, bank)):
                value = self.objectCode[bank][offset]
                value = value << 1
                wordval = struct.pack(">H", value)
                outputfile.write(wordval)
        self.context.log(4, "wrote %d words" % (count))
