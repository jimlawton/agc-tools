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
from opcode import OpcodeType, OperandType
from memory import AddressType
from instruction import Instruction
from directive import Directive
from interpretive import Interpretive

OPCODES = { 
    Architecture.AGC4_B2 : {
        # In AGC4 architecture, all instructions are single-word.
        OpcodeType.BASIC: {
            # Name                Method    Opcode   Operand Type               Address Type 
            "AD":     Instruction("AD",     060000,  OperandType.EXPRESSION,    AddressType.ERASABLE_12), 
            "CA":     Instruction("CA",     030000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "CAE":    Instruction("CAE",    030000,  OperandType.EXPRESSION,    AddressType.ERASABLE_12),
            "CAF":    Instruction("CAF",    030000,  OperandType.EXPRESSION,    AddressType.FIXED_12),
            "CCS":    Instruction("CCS",    010000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "COM":    Instruction("COM",    040000),
            "CS":     Instruction("CS",     040000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "DAS":    Instruction("DAS",    020001,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "DDOUBL": Instruction("DDOUBL", 020001),
            "DOUBLE": Instruction("DOUBLE", 060000),
            "DTCB":   Instruction("DTCB",   052006),
            "DTCF":   Instruction("DTCF",   052005),
            "DV":     Instruction("DV",     010000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "DXCH":   Instruction("DXCH",   050001,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "EXTEND": Instruction("EXTEND", 000006),
            "INCR":   Instruction("INCR",   024000),
            "INDEX":  Instruction("INDEX",  050000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "INHINT": Instruction("INHINT", 000004),
            "LXCH":   Instruction("LXCH",   022000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "MASK":   Instruction("MASK",   070000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "MSK":    Instruction("MASK",   070000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "NDX":    Instruction("INDEX",  050000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "NOOP":   Instruction("NOOP",   010000),           # TODO: For fixed memory only. Handle erasable case.
            "OVSK":   Instruction("OVSK",   054000),
            "RELINT": Instruction("RELINT", 000003),
            "RESUME": Instruction("RESUME", 050017),
            "RETURN": Instruction("RETURN", 000002),
            "TC":     Instruction("TC",     000000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "TCAA":   Instruction("TCAA",   054005),
            "TCF":    Instruction("TCF",    010000,  OperandType.EXPRESSION,    AddressType.FIXED_12),
            "TCR":    Instruction("TC",     000000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "TS":     Instruction("TS",     054000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "XCH":    Instruction("XCH",    056000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "XLQ":    Instruction("XLQ",    000001),
            "XXALQ":  Instruction("XXALQ",  000000),
            "ZL":     Instruction("ZL",     022007)
        },
        OpcodeType.EXTENDED: {
            # Name                Method    Opcode   Operand
            "ADS":    Instruction("ADS",    026000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "AUG":    Instruction("AUG",    024000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10), 
            "BZF":    Instruction("BZF",    010000,  OperandType.EXPRESSION,    AddressType.FIXED_12),  
            "BZMF":   Instruction("BZMF",   060000,  OperandType.EXPRESSION,    AddressType.FIXED_12),
            "DCA":    Instruction("DCA",    030001,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "DCOM":   Instruction("DCOM",   040001),
            "DIM":    Instruction("DIM",    026000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "EDRUPT": Instruction("EDRUPT", 007000,  OperandType.EXPRESSION,    AddressType.FIXED_9),
            "INDEX":  Instruction("INDEX",  050000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "MP":     Instruction("MP",     070000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "MSU":    Instruction("MSU",    020000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "NDX":    Instruction("INDEX",  050000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "QXCH":   Instruction("QXCH",   022000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "RAND":   Instruction("RAND",   002000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "READ":   Instruction("READ",   000000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "ROR":    Instruction("ROR",    004000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "RXOR":   Instruction("RXOR",   006000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "SQUARE": Instruction("SQUARE", 070000),
            "SU":     Instruction("SU",     060000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "WAND":   Instruction("WAND",   003000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "WOR":    Instruction("WOR",    005000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "WRITE":  Instruction("WRITE",  001000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "ZQ":     Instruction("ZQ",     022007)
        },
        OpcodeType.DIRECTIVE: {
            # Name                Method            Mnemonic    Operand Type            Words
            "-1DNADR":  Directive("Minus1DNADR",    "-1DNADR",  OperandType.EXPRESSION, 1),
            "-2CADR":   Directive("Minus2CADR",     "-2CADR",   OperandType.EXPRESSION, 1),
            "-2DNADR":  Directive("Minus2DNADR",    "-2DNADR",  OperandType.EXPRESSION, 1),
            "-3DNADR":  Directive("Minus3DNADR",    "-3DNADR",  OperandType.EXPRESSION, 1),
            "-4DNADR":  Directive("Minus4DNADR",    "-4DNADR",  OperandType.EXPRESSION, 1),
            "-5DNADR":  Directive("Minus5DNADR",    "-5DNADR",  OperandType.EXPRESSION, 1),
            "-6DNADR":  Directive("Minus6DNADR",    "-6DNADR",  OperandType.EXPRESSION, 1),
            "-DNCHAN":  Directive("MinusDNCHAN",    "-DNCHAN",  1),
            "-DNPTR":   Directive("MinusDNPTR",     "-DNPTR",   1),
            "-GENADR":  Directive("MinusGENADR",    "-GENADR",  1),
            "1DNADR":   Directive("1DNADR",         None,       OperandType.EXPRESSION, 1),
            "2BCADR":   Directive("2BCADR",         None,       OperandType.EXPRESSION, 2),
            "2CADR":    Directive("2CADR",          None,       OperandType.EXPRESSION, 2),
            "2DEC":     Directive("2DEC",           None,       OperandType.DECIMAL,    2),
            "2DEC*":    Directive("2DEC",           "2DEC*",    OperandType.DECIMAL,    2),
            "2DNADR":   Directive("2DNADR",         None,       OperandType.EXPRESSION, 2),
            "2FCADR":   Directive("2FCADR",         None,       OperandType.EXPRESSION, 2), 
            "2OCT":     Directive("2OCT",           None,       OperandType.OCTAL,      2),
            "3DNADR":   Directive("3DNADR",         None,       OperandType.EXPRESSION, 1),
            "4DNADR":   Directive("4DNADR",         None,       OperandType.EXPRESSION, 1),
            "5DNADR":   Directive("5DNADR",         None,       OperandType.EXPRESSION, 1),
            "6DNADR":   Directive("6DNADR",         None,       OperandType.EXPRESSION, 1),
            "=":        Directive("EqualsSign",     "=",        OperandType.EXPRESSION, 0),
            "=ECADR":   Directive("EqualsECADR",    "=ECADR",   OperandType.EXPRESSION, 0),
            "=MINUS":   Directive("EqualsMINUS",    "=MINUS",   OperandType.EXPRESSION, 0),
            "ADRES":    Directive("ADRES",          None,       OperandType.EXPRESSION, 1),
            "BANK":     Directive("BANK",           None,       OperandType.OCTAL,      0),
            "BBCON":    Directive("BBCON",          None,       OperandType.EXPRESSION, 1),
            "BBCON*":   Directive("BBCON",          "BBCON*",   OperandType.EXPRESSION, 1),
            "BLOCK":    Directive("BLOCK",          None,       OperandType.OCTAL,      0),
            "BNKSUM":   Directive("BNKSUM",         None,       OperandType.NONE,       0),
            "CADR":     Directive("CADR",           None,       OperandType.EXPRESSION, 1),
            "CHECK=":   Directive("CHECKEquals",    "CHECK=",   OperandType.EXPRESSION, 0),
            "COUNT":    Directive("COUNT",          None,       OperandType.EXPRESSION, 0),
            "COUNT*":   Directive("COUNT",          "COUNT*",   OperandType.EXPRESSION, 0),
            "DEC":      Directive("DEC",            None,       OperandType.DECIMAL,    1),
            "DEC*":     Directive("DEC",            "DEC*",     OperandType.DECIMAL,    1),
            "DNCHAN":   Directive("DNCHAN",         None,       OperandType.OCTAL,      1),
            "DNPTR":    Directive("DNPTR",          None,       OperandType.EXPRESSION, 1),
            "EBANK=":   Directive("EBANKEquals",    "EBANK=",   OperandType.EXPRESSION, 0),
            "ECADR":    Directive("ECADR",          None,       OperandType.EXPRESSION, 1),
            "EQUALS":   Directive("EQUALS",         None,       OperandType.EXPRESSION, 0),
            "ERASE":    Directive("ERASE",          None,       OperandType.EXPRESSION, 0),
            "FCADR":    Directive("FCADR",          None,       OperandType.EXPRESSION, 1),
            "GENADR":   Directive("GENADR",         None,       OperandType.EXPRESSION, 1),
            "MEMORY":   Directive("MEMORY",         None,       OperandType.EXPRESSION, 0),
            "MM":       Directive("MM",             None,       OperandType.DECIMAL,    1),
            "NV":       Directive("NV",             None,       OperandType.DECIMAL,    1),
            "OCT":      Directive("OCT",            None,       OperandType.OCTAL,      1),
            "OCTAL":    Directive("OCTAL",          None,       OperandType.OCTAL,      1),
            "REMADR":   Directive("REMADR",         None,       OperandType.EXPRESSION, 1),
            "SBANK=":   Directive("SBANKEquals",    "SBANK=",   OperandType.EXPRESSION, 0),
            "SETLOC":   Directive("SETLOC",         None,       OperandType.EXPRESSION, 0),
            "SUBRO":    Directive("SUBRO",          None,       OperandType.SYMBOLIC,   0),
            "VN":       Directive("VN",             None,       OperandType.DECIMAL,    1)
        },
        OpcodeType.INTERPRETIVE: {
            # Name                 Method           Mnemonic    Opcode	Operands	Switch	  NNNN
            "ABS":    Interpretive("ABS",           "ABS",      0130,   0),
            "ABVAL":  Interpretive("ABVAL",         "ABVAL",    0130,   0),
            "ACOS":   Interpretive("ACOS",          "ACOS",     0050,   0),
            "ARCCOS": Interpretive("ACOS",          "ARCCOS",   0050,   0),
            "ARCSIN": Interpretive("ASIN",          "ARCSIN",   0040,   0),
            "ASIN":   Interpretive("ASIN",          "ASIN",     0040,   0),
            "AXC,1":  Interpretive("AXC",           "AXC,1",    0016,   1),
            "AXC,2":  Interpretive("AXC",           "AXC,2",    0012,   1),
            "AXT,1":  Interpretive("AXT",           "AXT,1",    0006,   1),
            "AXT,2":  Interpretive("AXT",           "AXT,2",    0002,   1),
            "BDDV":   Interpretive("BDDV",          "BDDV",     0111,   1,          0,        000000),
            "BDDV*":  Interpretive("BDDV",          "BDDV*",    0113,   1,          0,        000000),
            "BDSU":   Interpretive("BDSU",          "BDSU",     0155,   1,  		0,        000000),
            "BDSU*":  Interpretive("BDSU",          "BDSU*",    0157,   1,  		0,        000000),
            "BHIZ":   Interpretive("BHIZ",          "BHIZ",     0146,   1),
            "BMN":    Interpretive("BMN",           "BMN",      0136,   1),
            "BOF":    Interpretive("BOF",           "BOF",      0162,   2,  		1,        000341),
            "BOFCLR": Interpretive("BOFCLR",        "BOFCLR",   0162,   2,  		1,        000241),
            "BOFF":   Interpretive("BOFF",          "BOFF",     0162,   2,  		1,        000341),
            "BOFINV": Interpretive("BOFINV",        "BOFINV",   0162,   2,  		1,        000141),
            "BOFSET": Interpretive("BOFSET",        "BOFSET",   0162,   2,  		1,        000041),
            "BON":    Interpretive("BON",           "BON",      0162,   2,  		1,        000301),
            "BONCLR": Interpretive("BONCLR",        "BONCLR",   0162,   2,  		1,        000201),
            "BONINV": Interpretive("BONINV",        "BONINV",   0162,   2,  		1,        000101),
            "BONSET": Interpretive("BONSET",        "BONSET",   0162,   2,  		1,        000001),
            "BOV":    Interpretive("BOV",           "BOV",      0176,   1),
            "BOVB":   Interpretive("BOVB",          "BOVB",     0172,   1),
            "BPL":    Interpretive("BPL",           "BPL",      0132,   1),
            "BVSU":   Interpretive("BVSU",          "BVSU",     0131,   1,  		0,        000000),
            "BVSU*":  Interpretive("BVSU",          "BVSU*",    0133,   1,  		0,        000000),
            "BZE":    Interpretive("BZE",           "BZE",      0122,   1),
            "CALL":   Interpretive("CALL",          "CALL",     0152,   1),
            "CALRB":  Interpretive("CALRB",         "CALRB",    0152,   1),
            "CCALL":  Interpretive("CCALL",         "CCALL",    0065,   2,  		0,        000000),
            "CCALL*": Interpretive("CCALL",         "CCALL*",   0067,   2,  		0,        000000),
            "CGOTO":  Interpretive("CGOTO",         "CGOTO",    0021,   2,  		0,        000000),
            "CGOTO*": Interpretive("CGOTO",         "CGOTO*",   0023,   2,  		0,        000000),
            "CLEAR":  Interpretive("CLEAR",         "CLEAR",    0162,   1,  		1,        000261),
            "CLR":    Interpretive("CLR",           "CLR",      0162,   1,  		1,        000261),
            "CLRGO":  Interpretive("CLRGO",         "CLRGO",    0162,   2,  		1,        000221),
            "COS":    Interpretive("COS",           "COS",      0030,   0),
            "COSINE": Interpretive("COS",           "COSINE",   0030,   0),
            "DAD":    Interpretive("DAD",           "DAD",      0161,   1,  		0,        000000),
            "DAD*":   Interpretive("DAD",           "DAD*",     0163,   1,  		0,        000000),
            "DCOMP":  Interpretive("DCOMP",         "DCOMP",    0100,   0),
            "DDV":    Interpretive("DDV",           "DDV",      0105,   1,  		0,        000000),
            "DDV*":   Interpretive("DDV",           "DDV*",     0107,   1,  		0,        000000),
            "DLOAD":  Interpretive("DLOAD",         "DLOAD",    0031,   1,  		0,        000000),
            "DLOAD*": Interpretive("DLOAD",         "DLOAD*",   0033,   1,  		0,        000000),
            "DMP":    Interpretive("DMP",           "DMP",      0171,   1,  		0,        000000),
            "DMP*":   Interpretive("DMP",           "DMP*",     0173,   1,  		0,        000000),
            "DMPR":   Interpretive("DMPR",          "DMPR",     0101,   1,  		0,        000000),
            "DMPR*":  Interpretive("DMPR",          "DMPR*",    0103,   1,  		0,        000000),
            "DOT":    Interpretive("DOT",           "DOT",      0135,   1,  		0,        000000),
            "DOT*":   Interpretive("DOT",           "DOT*",     0137,   1,  		0,        000000),
            "DSQ":    Interpretive("DSQ",           "DSQ",      0060,   0),
            "DSU":    Interpretive("DSU",           "DSU",      0151,   1,  		0,        000000),
            "DSU*":   Interpretive("DSU",           "DSU*",     0153,   1,  		0,        000000),
            "EXIT":   Interpretive("EXIT",          "EXIT",     0000,   0),
            "GOTO":   Interpretive("GOTO",          "GOTO",     0126,   1),
            "INCR,1": Interpretive("INCR",          "INCR,1",   0066,   1),
            "INCR,2": Interpretive("INCR",          "INCR,2",   0062,   1),
            "INVERT": Interpretive("INVERT",        "INVERT",   0162,   1,  		1,        000161),
            "INVGO":  Interpretive("INVGO",         "INVGO",    0162,   2,  		1,        000121),
            "ITA":    Interpretive("ITA",           "ITA",      0156,   1),
            "LXA,1":  Interpretive("LXA",           "LXA,1",    0026,   1),
            "LXA,2":  Interpretive("LXA",           "LXA,2",    0022,   1),
            "LXC,1":  Interpretive("LXC",           "LXC,1",    0036,   1),
            "LXC,2":  Interpretive("LXC",           "LXC,2",    0032,   1),
            "MXV":    Interpretive("MXV",           "MXV",      0055,   1,  		0,        000000),
            "MXV*":   Interpretive("MXV",           "MXV*",     0057,   1,  		0,        000000),
            "NORM":   Interpretive("NORM",          "NORM",     0075,   1,  		0,        000000),
            "NORM*":  Interpretive("NORM",          "NORM*",    0077,   1,  		0,        000000),
            "PDDL":   Interpretive("PDDL",          "PDDL",     0051,   1,  		0,        000000),
            "PDDL*":  Interpretive("PDDL",          "PDDL*",    0053,   1,  		0,        000000),
            "PDVL":   Interpretive("PDVL",          "PDVL",     0061,   1,  		0,        000000),
            "PDVL*":  Interpretive("PDVL",          "PDVL*",    0063,   1,  		0,        000000),
            "PUSH":   Interpretive("PUSH",          "PUSH",     0170,   0),
            "ROUND":  Interpretive("ROUND",         "ROUND",    0070,   0),
            "RTB":    Interpretive("RTB",           "RTB",      0142,   1),
            "RVQ":    Interpretive("RVQ",           "RVQ",      0160,   0),
            "SET":    Interpretive("SET",           "SET",      0162,   1,  		1,        000061),
            "SETGO":  Interpretive("SETGO",         "SETGO",    0162,   2,  		1,        000021),
            "SETPD":  Interpretive("SETPD",         "SETPD",    0175,   1,  		0,        000000),
            "SIGN":   Interpretive("SIGN",          "SIGN",     0011,   1,  		0,        000000),
            "SIGN*":  Interpretive("SIGN",          "SIGN*",    0013,   1,  		0,        000000),
            "SIN":    Interpretive("SIN",           "SIN",      0020,   0),
            "SINE":   Interpretive("SIN",           "SINE",     0020,   0),
            "SL":     Interpretive("SL",            "SL",       0115,   1,  		2,        020202),
            "SL*":    Interpretive("SL",            "SL*",      0117,   1,  		2,        020202),
            "SL1":    Interpretive("SL",            "SL1",      0024,   0,  		0,        000000),
            "SL1R":   Interpretive("SL",            "SL1R",     0004,   0,  		0,        000000),
            "SL2":    Interpretive("SL",            "SL2",      0064,   0,  		0,        000000),
            "SL2R":   Interpretive("SL",            "SL2R",     0044,   0,  		0,        000000),
            "SL3":    Interpretive("SL",            "SL3",      0124,   0,  		0,        000000),
            "SL3R":   Interpretive("SL",            "SL3R",     0104,   0,  		0,        000000),
            "SL4":    Interpretive("SL",            "SL4",      0164,   0,  		0,        000000),
            "SL4R":   Interpretive("SL",            "SL4R",     0144,   0,  		0,        000000),
            "SLOAD":  Interpretive("SLOAD",         "SLOAD",    0041,   1,  		0,        000000),
            "SLOAD*": Interpretive("SLOAD",         "SLOAD*",   0043,   1,  		0,        000000),
            "SLR":    Interpretive("SLR",           "SLR",      0115,   1,  		2,        021202),
            "SLR*":   Interpretive("SLR",           "SLR*",     0117,   1,  		2,        021202),
            "SQRT":   Interpretive("SQRT",          "SQRT",     0010,   0),
            "SR":     Interpretive("SR",            "SR",       0115,   1,  		2,        020602),
            "SR*":    Interpretive("SR",            "SR*",      0117,   1,  		2,        020602),
            "SR1":    Interpretive("SR",            "SR1",      0034,   0,  		0,        000000),
            "SR1R":   Interpretive("SR",            "SR1R",     0014,   0,  		0,        000000),
            "SR2":    Interpretive("SR",            "SR2",      0074,   0,  		0,        000000),
            "SR2R":   Interpretive("SR",            "SR2R",     0054,   0,  		0,        000000),
            "SR3":    Interpretive("SR",            "SR3",      0134,   0,  		0,        000000),
            "SR3R":   Interpretive("SR",            "SR3R",     0114,   0,  		0,        000000),
            "SR4":    Interpretive("SR",            "SR4",      0174,   0,  		0,        000000),
            "SR4R":   Interpretive("SR",            "SR4R",     0154,   0,  		0,        000000),
            "SRR":    Interpretive("SRR",           "SRR",      0115,   1,  		2,        021602),
            "SRR*":   Interpretive("SRR",           "SRR*",     0117,   1,  		2,        021602),
            "SSP":    Interpretive("SSP",           "SSP",      0045,   2,  		0,        000000),
            "SSP*":   Interpretive("SSP",           "SSP*",     0047,   1,  		0,        000000),
            "STADR":  Interpretive("STADR",         "STADR",    0150,   0),
            "STCALL": Interpretive("STCALL",        "STCALL",   0000    ),                      # FIXME: opcode
            "STODL":  Interpretive("STODL",         "STODL",    0000    ),                      # FIXME: opcode
            "STODL*": Interpretive("STODL",         "STODL*",   0000    ),                      # FIXME: opcode
            "STORE":  Interpretive("STORE",         "STORE",    0000    ),                      # FIXME: opcode
            "STOVL":  Interpretive("STOVL",         "STOVL",    0000    ),                      # FIXME: opcode
            "STOVL*": Interpretive("STOVL",         "STOVL*",   0000    ),                      # FIXME: opcode
            "STQ":    Interpretive("STQ",           "STQ",      0156,   1),
            "SXA,1":  Interpretive("SXA",           "SXA,1",    0046,   1),
            "SXA,2":  Interpretive("SXA",           "SXA,2",    0042,   1),
            "TAD":    Interpretive("TAD",           "TAD",      0005,   1,  		0,        000000),
            "TAD*":   Interpretive("TAD",           "TAD*",     0007,   1,  		0,        000000),
            "TIX,1":  Interpretive("TIX",           "TIX,1",    0076,   1),
            "TIX,2":  Interpretive("TIX",           "TIX,2",    0072,   1),
            "TLOAD":  Interpretive("TLOAD",         "TLOAD",    0025,   1,  		0,        000000),
            "TLOAD*": Interpretive("TLOAD",         "TLOAD*",   0027,   1,  		0,        000000),
            "UNIT":   Interpretive("UNIT",          "UNIT",     0120,   0),
            "UNIT*":  Interpretive("UNIT",          "UNIT*",    0000    ),                      # FIXME: opcode
            "V/SC":   Interpretive("VSC",           "V/SC",     0035,   1,  		0,        000000),
            "V/SC*":  Interpretive("VSC",           "V/SC*",    0037,   1,  		0,        000000),
            "VAD":    Interpretive("VAD",           "VAD",      0121,   1,  		0,        000000),
            "VAD*":   Interpretive("VAD",           "VAD*",     0123,   1,  		0,        000000),
            "VCOMP":  Interpretive("VCOMP",         "VCOMP",    0100,   0),
            "VDEF":   Interpretive("VDEF",          "VDEF",     0110,   0),
            "VLOAD":  Interpretive("VLOAD",         "VLOAD",    0001,   1,  		0,        000000),
            "VLOAD*": Interpretive("VLOAD",         "VLOAD*",   0003,   1,  		0,        000000),
            "VPROJ":  Interpretive("VPROJ",         "VPROJ",    0145,   1,  		0,        000000),
            "VPROJ*": Interpretive("VPROJ",         "VPROJ*",   0147,   1,  		0,        000000),
            "VSL":    Interpretive("VSL",           "VSL",      0115,   1,  		2,        020202),
            "VSL*":   Interpretive("VSL",           "VSL*",     0117,   1,  		2,        020202),
            "VSL1":   Interpretive("VSL",           "VSL1",     0004,   0,  		0,        000000),
            "VSL2":   Interpretive("VSL",           "VSL2",     0024,   0,  		0,        000000),
            "VSL3":   Interpretive("VSL",           "VSL3",     0044,   0,  		0,        000000),
            "VSL4":   Interpretive("VSL",           "VSL4",     0064,   0,  		0,        000000),
            "VSL5":   Interpretive("VSL",           "VSL5",     0104,   0,  		0,        000000),
            "VSL6":   Interpretive("VSL",           "VSL6",     0124,   0,  		0,        000000),
            "VSL7":   Interpretive("VSL",           "VSL7",     0144,   0,  		0,        000000),
            "VSL8":   Interpretive("VSL",           "VSL8",     0164,   0,  		0,        000000),
            "VSQ":    Interpretive("VSQ",           "VSQ",      0140,   0),
            "VSR":    Interpretive("VSR",           "VSR",      0115,   1,  		2,        020602),
            "VSR*":   Interpretive("VSR",           "VSR*",     0117,   1,  		2,        020602),
            "VSR1":   Interpretive("VSR",           "VSR1",     0014,   0,  		0,        000000),
            "VSR2":   Interpretive("VSR",           "VSR2",     0034,   0,  		0,        000000),
            "VSR3":   Interpretive("VSR",           "VSR3",     0054,   0,  		0,        000000),
            "VSR4":   Interpretive("VSR",           "VSR4",     0074,   0,  		0,        000000),
            "VSR5":   Interpretive("VSR",           "VSR5",     0114,   0,  		0,        000000),
            "VSR6":   Interpretive("VSR",           "VSR6",     0134,   0,  		0,        000000),
            "VSR7":   Interpretive("VSR",           "VSR7",     0154,   0,  		0,        000000),
            "VSR8":   Interpretive("VSR",           "VSR8",     0174,   0,  		0,        000000),
            "VXM":    Interpretive("VXM",           "VXM",      0071,   1,  		0,        000000),
            "VXM*":   Interpretive("VXM",           "VXM*",     0073,   1,  		0,        000000),
            "VXSC":   Interpretive("VXSC",          "VXSC",     0015,   1,  		0,        000000),
            "VXSC*":  Interpretive("VXSC",          "VXSC*",    0017,   1,  		0,        000000),
            "VXV":    Interpretive("VXV",           "VXV",      0141,   1,  		0,        000000),
            "VXV*":   Interpretive("VXV",           "VXV*",     0143,   1,  		0,        000000),
            "XAD,1":  Interpretive("XAD",           "XAD,1",    0106,   1),
            "XAD,2":  Interpretive("XAD",           "XAD,2",    0102,   1),
            "XCHX,1": Interpretive("XCHX",          "XCHX,1",   0056,   1),
            "XCHX,2": Interpretive("XCHX",          "XCHX,2",   0052,   1),
            "XSU,1":  Interpretive("XSU",           "XSU,1",    0116,   1),
            "XSU,2":  Interpretive("XSU",           "XSU,2",    0112,   1)
        }
    }
}
