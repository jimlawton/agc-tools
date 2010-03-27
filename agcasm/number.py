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
    DECIMAL_RE = re.compile("^[+-]*[0-9]+D$")
    FLOAT_RE   = re.compile("^[+-]*[0-9]*\.[0-9]+[ ]*(E[+-]*[0-9]+)* *(B[+-]*[0-9]+)*[*]*$")
    
    def __init__(self, text, forcetype=None):
        self.valid = False
        self.text = text
        self.value = 0
        self.type = None
        if forcetype:
            if forcetype == self.OCTAL:
                try:
                    self.value = int(text, 8)
                    self.valid = True
                except:
                    pass
            elif forcetype == self.DECIMAL:
                try:
                    self.value = int(text[:-1])
                    self.valid = True
                except:
                    pass
            elif forcetype == self.FLOAT:
                # TODO: Figure out how to handle floats.
                print >>sys.stderr, "Float formats not yet supported! (%s)" % text
        else:
            if self.OCTAL_RE.search(text):
                self.type = self.OCTAL
                self.valid = True
                self.value = int(text, 8)
            elif self.DECIMAL_RE.search(text):
                self.type = self.DECIMAL
                self.valid = True
                self.value = int(text[:-1])
            elif self.FLOAT_RE.search(text):
                self.type = self.FLOAT
                self.valid = True
                # TODO: Figure out how to handle floats.
                print >>sys.stderr, "Float formats not yet supported! (%s)" % text

    def isValid(self):
        return self.valid

    def complement(self):
        return ~self.value

class Octal(Number):
    def __init__(self, text):
        return Number(self, text, forceType=Number.OCTAL)

class Decimal(Number):
    def __init__(self, text):
        return Number(self, text, forceType=Number.DECIMAL)

class Float(Number):
    def __init__(self, text):
        return Number(self, text, forceType=Number.FLOAT)
    