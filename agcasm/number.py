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

import re

class Number:
    OCTAL   = 0
    DECIMAL = 1
    FLOAT   = 2
    
    OCTAL_RE   = re.compile("^[+-]*[0-7]+$")
    DECIMAL_RE = re.compile("^[+-]*[0-9]+[D]$")
    FLOAT_RE   = re.compile("^[+-]*[0-9]*\.[0-9]+[ ]*(E[+-]*[0-9]+)* *(B[+-]*[0-9]+)*[*]*$")
    
    def __init__(self, text, forcetype=None, size=1):
        self.valid = False
        self.text = text
        self.value = None
        self.values = []
        self.type = None
        self.size = size
        
        # Trim trailing asterisk, if any.
        if text.endswith('*'):
            text = text[:-1]
            
        if forcetype:
            if forcetype == self.OCTAL:
                try:
                    self._getOctal(text)
                except:
                    pass
            elif forcetype == self.DECIMAL:
                try:
                    self._getDecimal(text)
                except:
                    pass
            elif forcetype == self.FLOAT:
                try:
                    self._getFloat(text)
                except:
                    pass
        else:
            if self.OCTAL_RE.search(text):
                self._getOctal(text)
            elif self.DECIMAL_RE.search(text):
                self._getDecimal(text)
            elif self.FLOAT_RE.search(text):
                self._getFloat(text)
                
    def _getOctal(self, text):
        negate = False
        self.type = self.OCTAL
        if text.startswith('-'):
            negate = True
        if text.startswith('-') or text.startswith('+'):
            text = text[1:]
        self.value = int(text, 8)
        if negate:
            self.value = -self.value
        self.valid = True

    def _getDecimal(self, text):
        negate = False
        self.type = self.DECIMAL
        if text.endswith('D'):
            text = text[:-1]
        if text.startswith('-'):
            negate = True
        if text.startswith('-') or text.startswith('+'):
            text = text[1:]
        self.value = int(text)
        if negate:
            self.value = -self.value
        self.valid = True
    
    def _getFloat(self, text):
        self.type = self.FLOAT
        # TODO: Figure out how to handle floats.
        print >>sys.stderr, "Float formats not yet supported! (%s)" % text
        self.valid = False
    
    def isValid(self):
        return self.valid

    def complement(self):
        return ~self.value

    def __str__(self):
        text = " ".join([ "%05o" % x for x in self.values ])
        return text

class Octal(Number):
    def __init__(self, text):
        Number.__init__(self, text, self.OCTAL)

class Decimal(Number):
    def __init__(self, text):
        Number.__init__(self, text, self.DECIMAL)

class Float(Number):
    def __init__(self, text):
        Number.__init__(self, text, self.FLOAT)

class SingleNumber(Number):
    def __init__(self, text):
        Number.__init__(self, text, forcetype=None)

class SingleOctal(SingleNumber):
    def __init__(self, text):
        SingleNumber.__init__(self, text, forcetype=self.OCTAL)

class SingleDecimal(SingleNumber):
    def __init__(self, text):
        SingleNumber.__init__(self, text, forcetype=self.DECIMAL)

class SingleFloat(SingleNumber):
    def __init__(self, text):
        SingleNumber.__init__(self, text, forcetype=self.FLOAT)

class DoubleNumber(Number):
    def __init__(self, text):
        Number.__init__(self, text, forcetype=None, size=2)

class DoubleOctal(DoubleNumber):
    def __init__(self, text):
        DoubleNumber.__init__(self, text, forcetype=self.OCTAL)

class DoubleDecimal(DoubleNumber):
    def __init__(self, text):
        DoubleNumber.__init__(self, text, forcetype=self.DECIMAL)

class DoubleFloat(DoubleNumber):
    def __init__(self, text):
        DoubleNumber.__init__(self, text, forcetype=self.FLOAT)

def test_sp_oct():
    testdata = {
        "10000":            010000,
    }

    for value in testdata:
        testval = Octal(value)
        if testval.isValid():
            if testval.value != testdata[value]:
                print "FAIL: \"%s\", %06o != %06o" % (value, testval.value, testdata[value])
            else:
                print "PASS: \"%s\", %06o == %06o" % (value, testval.value, testdata[value])
        else:
            print "FAIL: \"%s\" failed to parse" % (value)

def test_sp_dec():
    testdata = {
        "16372  B-14":      037764,
        "-.38888":          063434,
        "-83 B-14":         077654,
        "-79 B-14":         077660,
        "41 B-14":          000051,
        "76 B-14":          000114,
        "52 B-14":          000064,
        "-30 B-14":         077741,
    }

    for value in testdata:
        testval = Decimal(value)
        if testval.isValid():
            if testval.value != testdata[value]:
                print "FAIL: \"%s\", %06o != %06o" % (value, testval.value, testdata[value])
            else:
                print "PASS: \"%s\", %06o == %06o" % (value, testval.value, testdata[value])
        else:
            print "FAIL: \"%s\" failed to parse" % (value)
            
if __name__=="__main__":
    import sys

    print "AGC Number classes tester..."

    test_sp_oct()
    test_sp_dec()
    
    sys.exit()
