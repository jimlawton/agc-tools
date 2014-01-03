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

import sys

# NOTE: Must be a new-style class.
class Word(object):

    def __init__(self, value=0, bits=15):
        self.bits = bits
        if bits == 15:
            self.maxval = 077777
        elif bits == 16:
            self.maxval = 0177777
        else:
            print >>sys.stderr, "Error, illegal word size (%d)" % (bits)

        self.value = (value & self.maxval)

    def set(self, value):
        self.value = (value & self.maxval)

    def get(self):
        return self.value

    def getSize(self):
        return self.bit

    def getMax(self):
        return self.maxval

    def isPositive(self):
        if self.value & 040000 == 040000:
            return False
        else:
            return True

    def isNegative(self):
        if self.value & 040000 == 040000:
            return True
        else:
            return False

    def add(self, value):
        self.value += value
        self.value &= self.maxval

    def subtract(self, value):
        self.value -= value
        self.value &= self.maxval

    def increment(self):
        self.value += 1
        self.value &= self.maxval

    def decrement(self):
        self.value -= 1
        self.value &= self.maxval

    def complement(self):
        self.value = (~self.value & self.maxval)

class Word15(Word):
    def __init__(self, value=0):
        super(Word15, self).__init__(value, 15)

class Word16(Word):
    def __init__(self, value=0):
        super(Word16, self).__init__(value, 16)

def test(data, size=15, methodName=None):
    passed = 0
    failed = 0
    text = ""

    NUM_OPERANDS = {
        "add":        1,
        "subtract":   1,
        "increment":  0,
        "decrement":  0,
        "complement": 0
    }

    print "Testing %s..." % text

    for value in data:
        for testdata in data[value]:
            word = Word(value, bits=size)
            precondition = testdata[0]
            operand = testdata[1]
            postcondition = testdata[2]

            if word.value != precondition:
                print "FAIL: %d, PRE actual %06o != expected %06o" % (value, word.value, precondition)
                failed += 1
            else:
                print "PASS: %d, PRE actual %06o == expected %06o" % (value, word.value, precondition)
                passed += 1

            if methodName != None:
                try:
                    method = word.__getattribute__(methodName)
                except:
                    method = None
                    print >>sys.stderr, "illegal method name '%s'" % (methodName)
            else:
                method = None

            if method:
                numOperands = NUM_OPERANDS[methodName]
                if numOperands == 0:
                    method()
                else:
                    method(operand)

                if word.value != postcondition:
                    print "FAIL: %d, POST actual %06o != expected %06o" % (value, word.value, postcondition)
                    failed += 1
                else:
                    print "PASS: %d, POST actual %06o == expected %06o" % (value, word.value, postcondition)
                    passed += 1


    if methodName == None:
        methodName = "numbers"
    print "%s: %d passed, %d failed of %d total" % (methodName, passed, failed, passed+failed)
    print
    return (passed, failed)

def test_15bit_numbers():
    testdata = {
         0:   [ (000000, 0, 0) ],
        -1:   [ (077777, 0, 0) ],
        1:    [ (000001, 0, 0) ],
        -2:   [ (077776, 0, 0) ],
        4096: [ (010000, 0, 0) ],
        9216: [ (022000, 0, 0) ],
        768:  [ (001400, 0, 0) ]
    }
    return test(testdata, 15)

def test_15bit_add():
    testdata = {
         0:   [ (000000, 1, 1) ],
        -1:   [ (077777, 1, 0), (077777, -1, 077776) ],
        1:    [ (000001, 1, 2), (000001, -1, 0) ],
        -2:   [ (077776, 1, 077777) ],
        4095: [ (007777, 1, 010000) ],
    }
    return test(testdata, 15, "add")

def test_15bit_subtract():
    testdata = {
         0:   [ (000000, 1, 077777) ],
        -1:   [ (077777, 1, 077776), (077777, -1, 0) ],
        1:    [ (000001, 1, 0), (000001, -1, 2) ],
        -2:   [ (077776, 1, 077775) ],
        4095: [ (007777, 1, 007776) ],
    }
    return test(testdata, 15, "subtract")

def test_15bit_increment():
    testdata = {
         0:   [ (000000, None, 1) ],
        -1:   [ (077777, None, 0) ],
        1:    [ (000001, None, 2) ],
        -2:   [ (077776, None, 077777) ],
        4095: [ (007777, None, 010000) ],
    }
    return test(testdata, 15, "increment")

def test_15bit_decrement():
    testdata = {
         0:   [ (000000, None, 077777) ],
        -1:   [ (077777, None, 077776) ],
        1:    [ (000001, None, 0) ],
        -2:   [ (077776, None, 077775) ],
        4095: [ (007777, None, 007776) ],
    }
    return test(testdata, 15, "decrement")

def test_15bit_complement():
    testdata = {
         0:   [ (000000, None, 077777) ],
        -1:   [ (077777, None, 0) ],
        1:    [ (000001, None, 077776) ],
        -2:   [ (077776, None, 1) ],
        4095: [ (007777, None, 070000) ],
    }
    return test(testdata, 15, "complement")

def test_16bit_numbers():
    testdata = {
         0:   [ (0000000, 0, 0) ],
        -1:   [ (0177777, 0, 0) ],
        1:    [ (0000001, 0, 0) ],
        -2:   [ (0177776, 0, 0) ],
        4096: [ (0010000, 0, 0) ],
        9216: [ (0022000, 0, 0) ],
        768:  [ (0001400, 0, 0) ]
    }
    return test(testdata, 16)

def test_16bit_add():
    testdata = {
         0:   [ (0000000, 1, 1) ],
        -1:   [ (0177777, 1, 0), (0177777, -1, 0177776) ],
        1:    [ (0000001, 1, 2), (0000001, -1, 0) ],
        -2:   [ (0177776, 1, 0177777) ],
        4095: [ (0007777, 1, 0010000) ],
    }
    return test(testdata, 16, "add")

def test_16bit_subtract():
    testdata = {
         0:   [ (0000000, 1, 0177777) ],
        -1:   [ (0177777, 1, 0177776), (0177777, -1, 0) ],
        1:    [ (0000001, 1, 0), (0000001, -1, 2) ],
        -2:   [ (0177776, 1, 0177775) ],
        4095: [ (0007777, 1, 0007776) ],
    }
    return test(testdata, 16, "subtract")

def test_16bit_increment():
    testdata = {
         0:   [ (0000000, None, 1) ],
        -1:   [ (0177777, None, 0) ],
        1:    [ (0000001, None, 2) ],
        -2:   [ (0177776, None, 0177777) ],
        4095: [ (0007777, None, 0010000) ],
    }
    return test(testdata, 16, "increment")

def test_16bit_decrement():
    testdata = {
         0:   [ (0000000, None, 0177777) ],
        -1:   [ (0177777, None, 0177776) ],
        1:    [ (0000001, None, 0) ],
        -2:   [ (0177776, None, 0177775) ],
        4095: [ (0007777, None, 0007776) ],
    }
    return test(testdata, 16, "decrement")

def test_16bit_complement():
    testdata = {
         0:   [ (0000000, None, 0177777) ],
        -1:   [ (0177777, None, 0) ],
        1:    [ (0000001, None, 0177776) ],
        -2:   [ (0177776, None, 1) ],
        4095: [ (0007777, None, 0170000) ],
    }
    return test(testdata, 16, "complement")

if __name__=="__main__":
    print "AGC Word class tester..."

    passed = failed = 0

    (passed, failed) = test_15bit_numbers()

    (pass2, fail2) = test_15bit_add()
    passed += pass2
    failed += fail2

    (pass2, fail2) = test_15bit_subtract()
    passed += pass2
    failed += fail2

    (pass2, fail2) = test_15bit_increment()
    passed += pass2
    failed += fail2

    (pass2, fail2) = test_15bit_decrement()
    passed += pass2
    failed += fail2

    (pass2, fail2) = test_15bit_complement()
    passed += pass2
    failed += fail2

    (pass2, fail2) = test_16bit_numbers()
    passed += pass2
    failed += fail2

    (pass2, fail2) = test_16bit_add()
    passed += pass2
    failed += fail2

    (pass2, fail2) = test_16bit_subtract()
    passed += pass2
    failed += fail2

    (pass2, fail2) = test_16bit_increment()
    passed += pass2
    failed += fail2

    (pass2, fail2) = test_16bit_decrement()
    passed += pass2
    failed += fail2

    (pass2, fail2) = test_16bit_complement()
    passed += pass2
    failed += fail2

    print "Overall: %d passed, %d failed of %d total" % (passed, failed, passed+failed)

    sys.exit()
