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

from opcode import Opcode

# NOTE: Must be a new-style class.
class Interpretive(Opcode):
    
    def __init__(self, methodName, mnemonic, opcode, numOperands=1, switchcode=None):
        Opcode.__init__(self, methodName, mnemonic, opcode, None, 1)
        self.switchcode = switchcode

    def parse(self, context, operands):
        #retval = self.__getattribute__("parse_" + self.name)(context, operands)
        context.loc += self.numwords
        #return retval
        
