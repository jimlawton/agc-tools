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

class RecordType:
    """Class defining type of a parser record."""

    NONE        = 0     # Invalid.
    INCLUDE     = 1     # Include directive.
    BLANK       = 2     # Blank line.
    COMMENT     = 3     # Comment-only line.
    LABEL       = 4     # Label-only line.
    ASMCONST    = 5     # Assembler constant, no code generated.
    CONST       = 6     # Constant, code generated.
    EXEC        = 7     # Executable line, code generated.
    INTERP      = 8     # Interpretive line.
    IGNORE      = 9     # Ignored.`

    @classmethod
    def isGenerative(cls, rectype):
        """Return True if record type generates machine code."""
        isGenerative = {
            None:                 False,
            RecordType.NONE:      False,
            RecordType.INCLUDE:   False,
            RecordType.BLANK:     False,
            RecordType.COMMENT:   False,
            RecordType.LABEL:     False,
            RecordType.ASMCONST:  False,
            RecordType.CONST:     True,
            RecordType.EXEC:      True,
            RecordType.INTERP:    True,
            RecordType.IGNORE:    False
        }
        if rectype:
            return isGenerative[rectype]
        else:
            return False

    @classmethod
    def isAddressValid(cls, rectype):
        """Return True if record type is one in which the address field is valid."""
        isAddress = {
            None:                 False,
            RecordType.NONE:      False,
            RecordType.INCLUDE:   False,
            RecordType.BLANK:     False,
            RecordType.COMMENT:   False,
            RecordType.LABEL:     True,
            RecordType.ASMCONST:  False,
            RecordType.CONST:     True,
            RecordType.EXEC:      True,
            RecordType.INTERP:    True,
            RecordType.IGNORE:    False
        }
        if rectype:
            return isAddress[rectype]
        else:
            return False

    @classmethod
    def isParseable(cls, rectype):
        """Return True if record type is reparseable."""
        isParseable = {
            RecordType.NONE:      False,
            RecordType.INCLUDE:   False,
            RecordType.BLANK:     False,
            RecordType.COMMENT:   False,
            RecordType.LABEL:     False,
            RecordType.ASMCONST:  True,
            RecordType.CONST:     True,
            RecordType.EXEC:      True,
            RecordType.INTERP:    True,
            RecordType.IGNORE:    False
        }
        if rectype:
            return isParseable[rectype]
        else:
            return False

    @classmethod
    def isIgnored(cls, rectype):
        """Return True if record type should be ignored."""
        isIgnored = {
            RecordType.NONE:      True,
            RecordType.INCLUDE:   False,
            RecordType.BLANK:     True,
            RecordType.COMMENT:   True,
            RecordType.LABEL:     False,
            RecordType.ASMCONST:  False,
            RecordType.CONST:     False,
            RecordType.EXEC:      False,
            RecordType.INTERP:    False,
            RecordType.IGNORE:    True
        }
        if rectype:
            return isIgnored[rectype]
        else:
            return True

    @classmethod
    def isInterpretive(cls, rectype):
        """Return True if record type is interpretive."""
        if rectype == RecordType.INTERP:
            return True
        else:
            return False

    @classmethod
    def toString(cls, rectype):
        if rectype == None:
            rectype = RecordType.NONE
        textdict = {
            RecordType.NONE:      "   ",
            RecordType.INCLUDE:   "INC",
            RecordType.BLANK:     "   ",
            RecordType.COMMENT:   "   ",
            RecordType.LABEL:     "LBL",
            RecordType.ASMCONST:  "ASM",
            RecordType.CONST:     "CON",
            RecordType.EXEC:      "EXE",
            RecordType.INTERP:    "INT",
            RecordType.IGNORE:    "   "
        }
        return textdict[rectype]
