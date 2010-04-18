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
import sys

class Number:
    
    OCTAL   = 0
    DECIMAL = 1
    
    OCTAL_RE   = re.compile("^[+-]*[0-7]+$")
    DECIMAL_RE = re.compile("^[+-]*[0-9]+[D]$")
    FLOAT_RE   = re.compile("^[+-]*[0-9]*\.[0-9]+[ ]*(E[+-]*[0-9]+)* *(B[+-]*[0-9]+)*[*]*$")
    
    def __init__(self, text, forcetype=None, size=1):
        self.valid = False
        self.text = text
        self.type = None
        self.size = size

        if self.size == 1:
            self.value = None
        else:
            self.value = ()

        # Trim trailing asterisk, if any.
        if text.endswith('*'):
            text = text[:-1]
            
        if forcetype != None:
            if forcetype == Number.OCTAL:
                self._getOctal(text)
            elif forcetype == Number.DECIMAL:
                self._getDecimal(text)
        else:
            if self.OCTAL_RE.search(text):
                self._getOctal(text)
            elif self.DECIMAL_RE.search(text) or self.FLOAT_RE.search(text):
                self._getDecimal(text)

    def scaleFactor(self, text):
        retval = 1.0
        if text.startswith('E'):
            retval = pow(10.0, int(text[1:]))
        elif text.startswith('B'):
            retval = pow(2.0, int(text[1:]))
        return retval

    def _getOctal(self, text):
        negate = False
        self.type = Number.OCTAL
        if text.startswith('-'):
            negate = True
        if text.startswith('-') or text.startswith('+'):
            text = text[1:]
        value = int(text, 8)
        if self.size == 1:
            self.value = value
            if negate:
                self.value = ~self.value & 077777
        else:
            textval = "%010o" % value
            tval1 = textval[:5]
            tval2 = textval[5:]
            self.value = [ int(tval1, 8), int(tval2, 8) ]
            if negate:
                self.value[0] = ~self.value[0] & 077777
                self.value[1] = ~self.value[1] & 077777
        self.valid = True

    def _getDecimal(self, text):
        negate = False
        self.type = Number.DECIMAL
        fields = text.split()
        bscale = 0
        escale = 0
        mantissa = text
        skip = False
        if len(fields) > 1:
            mantissa = None
            # Handle E and B scaling.
            for i in range(len(fields)):
                if skip:
                    skip = False
                    continue
                field = fields[i] 
                if field.startswith('B'):
                    bfield = field
                    if field == 'B':
                        bfield += fields[i+1]
                        skip = True
                    bscale = self.scaleFactor(bfield)
                elif field.startswith('E'):
                    efield = field
                    if field == 'E':
                        efield += fields[i+1]
                        skip = True
                    escale = self.scaleFactor(efield)
                else:
                    mantissa = field
        else:
            if not '.' in mantissa:
                if self.size == 1:
                    bscale = self.scaleFactor("B-14")
                else:
                    bscale = self.scaleFactor("B-28")
        if mantissa.endswith('D'):
            mantissa = mantissa[:-1]
        if mantissa.startswith('-'):
            negate = True
        if mantissa.startswith('-') or mantissa.startswith('+'):
            mantissa = mantissa[1:]
        realval = float(mantissa)
        if bscale != 0:
            realval *= bscale
        if escale != 0:
            realval *= escale
        if realval > 1.0:
            print >>sys.stderr, "Error, invalid number, greater than 1.0 (%s)" % (text)
            sys.exit()
        value = 0
        if self.size == 1:
            rangeval = 14
        else:
            rangeval = 28
        for i in range(rangeval):
            value = value << 1
            if realval >= 0.5:
                value += 1
                realval -= 0.5
            realval *= 2
        if self.size == 1:
            limitval = 0x3fff
        else:
            limitval = 0xfffffff
        if realval >= 0.5 and value < limitval:
            value += 1
        if self.size == 2:
            i = value & 0x3fff
            value = (value >> 14) & 0x3fff
        if negate:
            if self.size == 2:
                value = ~value
                i = ~i
                i &= 0x7fff
                value &= 0x7fff
            else:
                value = ~value & 0x7fff
        if self.size == 1:
            self.value = value
        else:
            self.value = [ value, i ]
        self.valid = True

    def isValid(self):
        return self.valid

    def complement(self):
        return ~self.value

    def __str__(self):
        text = " ".join([ "%05o" % x for x in self.values ])
        return text

class Octal(Number):
    def __init__(self, text):
        Number.__init__(self, text, Number.OCTAL)

class Decimal(Number):
    def __init__(self, text):
        Number.__init__(self, text, Number.DECIMAL)

class SingleNumber(Number):
    def __init__(self, text):
        Number.__init__(self, text, forcetype=None)

class SingleOctal(SingleNumber):
    def __init__(self, text):
        SingleNumber.__init__(self, text, forcetype=Number.OCTAL)

class SingleDecimal(SingleNumber):
    def __init__(self, text):
        SingleNumber.__init__(self, text, forcetype=Number.DECIMAL)

class DoubleNumber(Number):
    def __init__(self, text, forcetype=None):
        Number.__init__(self, text, forcetype, size=2)

class DoubleOctal(DoubleNumber):
    def __init__(self, text):
        DoubleNumber.__init__(self, text, forcetype=Number.OCTAL)

class DoubleDecimal(DoubleNumber):
    def __init__(self, text):
        DoubleNumber.__init__(self, text, forcetype=Number.DECIMAL)

def test(numtype, size, data):
    passed = 0
    failed = 0
    text = ""
    if size == 1:
        text += "SP "
        if numtype == Number.OCTAL:
            text += "Octal"
        elif numtype == Number.DECIMAL:
            text += "Decimal"
        elif numtype == Number.FLOAT:
            text += "Float"
    else:
        text += "DP "
        if numtype == Number.OCTAL:
            text += "Octal"
        elif numtype == Number.DECIMAL:
            text += "Decimal"
        elif numtype == Number.FLOAT:
            text += "Float"

    print "Testing %s..." % text
    
    for value in data:
        if size == 1:
            if numtype == Number.OCTAL:
                testval = Octal(value)
            elif numtype == Number.DECIMAL:
                testval = Decimal(value)
        else:
            if numtype == Number.OCTAL:
                testval = DoubleOctal(value)
            elif numtype == Number.DECIMAL:
                testval = DoubleDecimal(value)
  
        if testval.isValid():
            if size == 1:
                if testval.value != data[value]:
                    print "FAIL: \"%s\", %06o != %06o" % (value, testval.value, data[value])
                    failed += 1
                else:
                    print "PASS: \"%s\", %06o == %06o" % (value, testval.value, data[value])
                    passed += 1
            else:
                if testval.value[0] != data[value][0] or testval.value[1] != data[value][1]:
                    print "FAIL: \"%s\", (%06o,%06o) != (%06o,%06o)" % (value, testval.value[0], testval.value[1], data[value][0], data[value][1])
                    failed += 1
                else:
                    print "PASS: \"%s\", (%06o,%06o) == (%06o,%06o)" % (value, testval.value[0], testval.value[1], data[value][0], data[value][1])
                    passed += 1
        else:
            print "FAIL: \"%s\" failed to parse" % (value)
            failed += 1

    print "%s: %d passed, %d failed of %d total" % (text, passed, failed, passed+failed)
    print
    return (passed, failed)

def test_sp_oct():
    testdata = {
        "0":                000000,
        "+0":               000000,
        "-0":               077777,
        "1":                000001,
        "-1":               077776,
        "10000":            010000,
        "22000":            022000,
        "77777":            077777,
        "1400":             001400
    }
    return test(Number.OCTAL, 1, testdata)

def test_sp_dec():
    testdata = {
        "16372":            037764,
        "16372  B-14":      037764,
        "-.38888":          063434,
        "-83":              077654,
        "-83 B-14":         077654,
        "-79":              077660,
        "-79 B-14":         077660,
        "41":               000051,
        "41 B-14":          000051,
        "76":               000114,
        "76 B-14":          000114,
        "52":               000064,
        "52 B-14":          000064,
        "-30":              077741,
        "-30 B-14":         077741,
        "120":              000170,
        "120 B-14":         000170,
        "120D":             000170,
        "+120D":            000170,
        "+120":             000170,
        "+120D*":           000170,
        "+120*":            000170,
        "-0 B-14":          077777,
        "-0":               077777,
        "1000":             001750,  
        "1000 B-14":        001750,  
        "-71 B-14":         077670,
        "-71":              077670,
        "2":                000002,
        "2 B-14":           000002,
        "9000":             021450,
        "7199":             016037,
        "-07199":           061740,
        "-0000":            077777
    }
    return test(Number.DECIMAL, 1, testdata)
            
def test_dp_oct():
    testdata = {
        "0106505603":       (001065, 005603),
        "7776600011":       (077766, 000011),
        "1663106755":       (016631, 006755),
        "0777700000":       (007777, 000000),
        "3777737777":       (037777, 037777),
        "3777737700":       (037777, 037700),
        "0000000100":       (000000, 000100)
    }
    return test(Number.OCTAL, 2, testdata)

def test_dp_dec():
    testdata = {
        ".021336 B-7":              (000002, 027311),
        "2538.09 E3 B-27":          (000465, 032324),
        "7178165 B-29":             (000333, 001733),
        "30480 B-19":               (001670, 020000),
        "30.48 B-7":                (007475, 016051),
        "17.2010499 B-7":           (004231, 027400),
        ".032808399":               (001031, 021032),
        "0 B-28":                   (000000, 000000),
        ".031335467":               (001001, 014636),
        "8616410 B-28":             (001015, 034732),
        "+.8431756920 B-1":         (015373, 011346),
        "-.5376381241 B-1":         (067313, 065307),
        "+.5376381241 B-1":         (010464, 012470),
        ".5":                       (020000, 000000),
        "1 E-5 B14":                (005174, 013261),
        "1.666666666 E-4 B12":      (025660, 031742),
        ".16384":                   (005174, 013261),
        "-1.703706128 E-11 B28":    (077665, 042175),
        "+4.253263471 E-9 B27":     (022211, 000636),
        "-1.145531390 E-16 B28":    (077777, 077767),
        "+8.788308600 E-1 B 0":     (034076, 030363),
        "+6.552737750 E-1  B 0":    (024760, 000133),
        "+6.511941688 E-2  B 0":    (002052, 035250),
        "+1.160576171 E-7  B23":    (037116, 032631),
        "+7.733314844 E-1  B 0":    (030576, 010326),
        "3.986032 E 10 B-36":       (022437, 016067),
        ".25087606 E-10 B+34":      (015625, 021042),
        "1.99650495 E5 B-18":       (030276, 004773),
        ".50087529 E-5 B+17":       (025004, 006702),
        "4.902778 E8 B-30":         (016471, 001352),
        ".203966 E-8 B+28":         (021412, 020500),
        "2.21422176 E4 B-15":       (025477, 003367),
        ".45162595 E-4 B+14":       (027533, 007571),
        "2538.09 E3 B-27":          (000465, 032324),
    }
    return test(Number.DECIMAL, 2, testdata)

if __name__=="__main__":
    print "AGC Number classes tester..."

    passed = failed = 0
    
    (passed, failed) = test_sp_oct()

    (pass2, fail2) = test_sp_dec()
    passed += pass2
    failed += fail2

    (pass3, fail3) = test_dp_oct()
    passed += pass3
    failed += fail3

    (pass4, fail4) = test_dp_dec()
    passed += pass4
    failed += fail4
    
    print "Overall: %d passed, %d failed of %d total" % (passed, failed, passed+failed)
     
    sys.exit()
