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

from architecture import *
from memory import *

class Code:
    """Class storing generated object code."""
    
    def __init__(self, context):
        self.code = {}
        for bank in context.memmap.banks[MemoryType.FIXED]:
            self.code[bank] = {}
    
    def emit(self, context, data):
        """Emit generated code. 'data' must be a list."""
        for value in data:
            address = context.bankloc[context.fbank]
            self.code[context.fbank][address] = value
            address += 1
        context.bankloc[context.fbank] = address
        
