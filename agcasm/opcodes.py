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
from interpretive import Interpretive, InterpretiveType

OPCODES = {
    Architecture.AGC4_B2: {
        # In AGC4 architecture, all instructions are single-word.
        OpcodeType.BASIC: {
            # Name                Method        Opcode   Operand Type               Address Type
            "0":      Instruction("TC",         000000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "3":      Instruction("TC",         030000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "7":      Instruction("TC",         070000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "AD":     Instruction("AD",         060000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "ADS":    Instruction("ADS",        026000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "CA":     Instruction("CA",         030000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "CAE":    Instruction("CAE",        030000,  OperandType.EXPRESSION,    AddressType.ERASABLE_12),
            "CAF":    Instruction("CAF",        030000,  OperandType.EXPRESSION,    AddressType.FIXED_12),
            "CCS":    Instruction("CCS",        010000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "-CCS":   Instruction("MinusCCS",   010000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "COM":    Instruction("COM",        040000),
            "CS":     Instruction("CS",         040000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "DAS":    Instruction("DAS",        020001,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "DDOUBL": Instruction("DDOUBL",     020001),
            "DOUBLE": Instruction("DOUBLE",     060000),
            "DTCB":   Instruction("DTCB",       052006),
            "DTCF":   Instruction("DTCF",       052005),
            "DXCH":   Instruction("DXCH",       052001,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "EXTEND": Instruction("EXTEND",     000006),
            "INCR":   Instruction("INCR",       024000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "INDEX":  Instruction("INDEX",      050000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "INHINT": Instruction("INHINT",     000004),
            "LXCH":   Instruction("LXCH",       022000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "MASK":   Instruction("MASK",       070000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "MSK":    Instruction("MASK",       070000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "NDX":    Instruction("INDEX",      050000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "NOOP":   Instruction("NOOP",       010000),           # TODO: For fixed memory only. Handle erasable case.
            "OVSK":   Instruction("OVSK",       054000),
            "RELINT": Instruction("RELINT",     000003),
            "RESUME": Instruction("RESUME",     050017),
            "RETURN": Instruction("RETURN",     000002),
            "TC":     Instruction("TC",         000000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "TCAA":   Instruction("TCAA",       054005),
            "TCF":    Instruction("TCF",        010000,  OperandType.EXPRESSION,    AddressType.FIXED_12,       optional=True),
            "TCR":    Instruction("TC",         000000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "TS":     Instruction("TS",         054000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "XCH":    Instruction("XCH",        056000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "XLQ":    Instruction("XLQ",        000001),
            "XXALQ":  Instruction("XXALQ",      000000),
            "ZL":     Instruction("ZL",         022007)
        },
        OpcodeType.EXTENDED: {
            # Name                Method        Opcode   Operand                    Address Type
            "AUG":    Instruction("AUG",        024000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "BZF":    Instruction("BZF",        010000,  OperandType.EXPRESSION,    AddressType.FIXED_12),
            "BZMF":   Instruction("BZMF",       060000,  OperandType.EXPRESSION,    AddressType.FIXED_12),
            "DCA":    Instruction("DCA",        030001,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "DCOM":   Instruction("DCOM",       040001),
            "DCS":    Instruction("DCS",        040001,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "DIM":    Instruction("DIM",        026000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "DV":     Instruction("DV",         010000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "EDRUPT": Instruction("EDRUPT",     007000,  OperandType.EXPRESSION,    AddressType.FIXED_9),
            "INDEX":  Instruction("INDEX",      050000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "MP":     Instruction("MP",         070000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "MSU":    Instruction("MSU",        020000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "NDX":    Instruction("INDEX",      050000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "QXCH":   Instruction("QXCH",       022000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "RAND":   Instruction("RAND",       002000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "READ":   Instruction("READ",       000000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "ROR":    Instruction("ROR",        004000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "RXOR":   Instruction("RXOR",       006000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "SQUARE": Instruction("SQUARE",     070000),
            "SU":     Instruction("SU",         060000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "WAND":   Instruction("WAND",       003000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "WOR":    Instruction("WOR",        005000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "WRITE":  Instruction("WRITE",      001000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "ZQ":     Instruction("ZQ",         022007)
        },
        OpcodeType.DIRECTIVE: {
            # Name                Method            Mnemonic    Operand Type            Optional?   Words
            "-1DNADR":  Directive("MinusDNADR",     "-1DNADR",  OperandType.EXPRESSION, False,      1),
            "-2CADR":   Directive("Minus2CADR",     "-2CADR",   OperandType.EXPRESSION, False,      2),
            "-2DNADR":  Directive("MinusDNADR",     "-2DNADR",  OperandType.EXPRESSION, False,      1),
            "-3DNADR":  Directive("MinusDNADR",     "-3DNADR",  OperandType.EXPRESSION, False,      1),
            "-4DNADR":  Directive("MinusDNADR",     "-4DNADR",  OperandType.EXPRESSION, False,      1),
            "-5DNADR":  Directive("MinusDNADR",     "-5DNADR",  OperandType.EXPRESSION, False,      1),
            "-6DNADR":  Directive("MinusDNADR",     "-6DNADR",  OperandType.EXPRESSION, False,      1),
            "-DNCHAN":  Directive("MinusDNCHAN",    "-DNCHAN",  OperandType.OCTAL,      False,      1),
            "-DNPTR":   Directive("MinusDNPTR",     "-DNPTR",   OperandType.EXPRESSION, False,      1),
            "-GENADR":  Directive("MinusGENADR",    "-GENADR",  OperandType.EXPRESSION, False,      1),
            "1DNADR":   Directive("DNADR",          "1DNADR",   OperandType.EXPRESSION, False,      1),
            "2BCADR":   Directive("2CADR",          "2BCADR",   OperandType.EXPRESSION, False,      2),
            "2CADR":    Directive("2CADR",          None,       OperandType.EXPRESSION, False,      2),
            "2DEC":     Directive("2DEC",           None,       OperandType.DECIMAL,    False,      2),
            "2DEC*":    Directive("2DEC",           "2DEC*",    OperandType.DECIMAL,    False,      2),
            "2DNADR":   Directive("DNADR",          "2DNADR",   OperandType.EXPRESSION, False,      1),
            "2FCADR":   Directive("2FCADR",         None,       OperandType.EXPRESSION, False,      2),
            "2OCT":     Directive("2OCT",           None,       OperandType.OCTAL,      False,      2),
            "3DNADR":   Directive("DNADR",          "3DNADR",   OperandType.EXPRESSION, False,      1),
            "4DNADR":   Directive("DNADR",          "4DNADR",   OperandType.EXPRESSION, False,      1),
            "5DNADR":   Directive("DNADR",          "5DNADR",   OperandType.EXPRESSION, False,      1),
            "6DNADR":   Directive("DNADR",          "6DNADR",   OperandType.EXPRESSION, False,      1),
            "=":        Directive("EQUALS",         "=",        OperandType.EXPRESSION, True,       0),
            "=ECADR":   Directive("EqualsECADR",    "=ECADR",   OperandType.EXPRESSION, False,      0),
            "=MINUS":   Directive("EqualsMINUS",    "=MINUS",   OperandType.EXPRESSION, True,       0),
            "ADRES":    Directive("ADRES",          None,       OperandType.EXPRESSION, False,      1),
            "BANK":     Directive("BANK",           None,       OperandType.OCTAL,      True,       0),
            "BBCON":    Directive("BBCON",          None,       OperandType.EXPRESSION, False,      1),
            "BBCON*":   Directive("BBCONstar",      "BBCON*",   OperandType.NONE,       False,      1),
            "BLOCK":    Directive("BLOCK",          None,       OperandType.OCTAL,      False,      0),
            "BNKSUM":   Directive("BNKSUM",         None,       OperandType.OCTAL,      True,       0),
            "CADR":     Directive("FCADR",          "CADR",     OperandType.EXPRESSION, False,      1),
            "CHECK=":   Directive("CHECKEquals",    "CHECK=",   OperandType.EXPRESSION, False,      0),
            "COUNT":    Directive("COUNT",          None,       OperandType.EXPRESSION, False,      0),
            "COUNT*":   Directive("COUNT",          "COUNT*",   OperandType.EXPRESSION, False,      0),
            "DEC":      Directive("DEC",            None,       OperandType.DECIMAL,    False,      1),
            "DEC*":     Directive("DEC",            "DEC*",     OperandType.DECIMAL,    False,      1),
            "DNCHAN":   Directive("DNCHAN",         None,       OperandType.OCTAL,      False,      1),
            "DNPTR":    Directive("DNPTR",          None,       OperandType.EXPRESSION, False,      1),
            "EBANK=":   Directive("EBANKEquals",    "EBANK=",   OperandType.EXPRESSION, False,      0),
            "ECADR":    Directive("ECADR",          None,       OperandType.EXPRESSION, False,      1),
            "EQUALS":   Directive("EQUALS",         None,       OperandType.EXPRESSION, True,       0),
            "ERASE":    Directive("ERASE",          None,       OperandType.EXPRESSION, True,       0),
            "FCADR":    Directive("FCADR",          None,       OperandType.EXPRESSION, False,      1),
            "GENADR":   Directive("GENADR",         None,       OperandType.EXPRESSION, False,      1),
            "MEMORY":   Directive("MEMORY",         None,       OperandType.EXPRESSION, False,      0),
            "MM":       Directive("DEC",            "MM",       OperandType.DECIMAL,    False,      1),
            "NV":       Directive("VN",             "NV",       OperandType.DECIMAL,    False,      1),
            "OCT":      Directive("OCT",            None,       OperandType.OCTAL,      False,      1),
            "OCTAL":    Directive("OCT",            "OCTAL",    OperandType.OCTAL,      False,      1),
            "REMADR":   Directive("REMADR",         None,       OperandType.EXPRESSION, False,      1),
            "SBANK=":   Directive("SBANKEquals",    "SBANK=",   OperandType.EXPRESSION, False,      0),
            "SETLOC":   Directive("SETLOC",         None,       OperandType.EXPRESSION, False,      0),
            "SUBRO":    Directive("SUBRO",          None,       OperandType.SYMBOLIC,   False,      0),
            "VN":       Directive("VN",             None,       OperandType.DECIMAL,    False,      1)
        },
        OpcodeType.INTERPRETIVE: {
            # Op   Instructions(s)
            # 0000 EXIT
            # 0001 VLOAD
            # 0002 AXT,2
            # 0003 VLOAD*
            # 0004 SL1R,VSL1
            # 0005 TAD
            # 0006 AXT,1
            # 0007 TAD*
            # 0010 SQRT
            # 0011 SIGN
            # 0012 AXC,2
            # 0013 SIGN*
            # 0014 SR1R,VSR1
            # 0015 VXSC
            # 0016 AXC,1
            # 0017 VXSC*
            # 0020 SIN,SINE
            # 0021 CGOTO
            # 0022 LXA,2
            # 0023 CGOTO*
            # 0024 SL1,VSL2
            # 0025 TLOAD
            # 0026 LXA,1
            # 0027 TLOAD*
            # 0030 COS,COSINE
            # 0031 DLOAD
            # 0032 LXC,2
            # 0033 DLOAD*
            # 0034 SR1,VSR2
            # 0035 V/SC
            # 0036 LXC,1
            # 0037 V/SC*
            # 0040 ARCSIN,ASIN
            # 0041 SLOAD
            # 0042 SXA,2
            # 0043 SLOAD*
            # 0044 SL2R,VSL3
            # 0045 SSP
            # 0046 SXA,1
            # 0047 SSP*
            # 0050 ACOS,ARCCOS
            # 0051 PDDL
            # 0052 XCHX,2
            # 0053 PDDL*
            # 0054 SR2R,VSR3
            # 0055 MXV
            # 0056 XCHX,1
            # 0057 MXV*
            # 0060 DSQ
            # 0061 PDVL
            # 0062 INCR,2
            # 0063 PDVL*
            # 0064 SL2,VSL4
            # 0065 CCALL
            # 0066 INCR,1
            # 0067 CCALL*
            # 0070 ROUND
            # 0071 VXM
            # 0072 TIX,2
            # 0073 VXM*
            # 0074 SR2,VSR4
            # 0075 NORM
            # 0076 TIX,1
            # 0077 NORM*
            # 0100 DCOMP,VCOMP
            # 0101 DMPR
            # 0102 XAD,2
            # 0103 DMPR*
            # 0104 SL3R,VSL5
            # 0105 DDV
            # 0106 XAD,1
            # 0107 DDV*
            # 0110 VDEF
            # 0111 BDDV
            # 0112 XSU,2
            # 0113 BDDV*
            # 0114 SR3R,VSR5
            # 0115 SL,SLR,SR,SRR,VSL,VSR
            # 0116 XSU,1
            # 0117 SL*,SLR*,SR*,SRR*,VSL*,VSR*
            # 0120 UNIT
            # 0121 VAD
            # 0122 BZE
            # 0123 VAD*
            # 0124 SL3,VSL6
            # 0125 VSU
            # 0126 GOTO
            # 0127 VSU*
            # 0130 ABS,ABVAL
            # 0131 BVSU
            # 0132 BPL
            # 0133 BVSU*
            # 0134 SR3,VSR6
            # 0135 DOT
            # 0136 BMN
            # 0137 DOT*
            # 0140 VSQ
            # 0141 VXV
            # 0142 RTB
            # 0143 VXV*
            # 0144 SL4R,VSL7
            # 0145 VPROJ
            # 0146 BHIZ
            # 0147 VPROJ*
            # 0150 STADR
            # 0151 DSU
            # 0152 CALL,CALRB
            # 0153 DSU*
            # 0154 SR4R,VSR7
            # 0155 BDSU
            # 0156 ITA,STQ
            # 0157 BDSU*
            # 0160 RVQ
            # 0161 DAD
            # 0162 BOF,BOFCLR,BOFF,BOFINV,BOFSET,BON,BONCLR,BONINV,BONSET,CLEAR,CLR,CLRGO,INVERT,INVGO,SET,SETGO
            # 0163 DAD*
            # 0164 SL4,VSL8
            # 0170 PUSH
            # 0171 DMP
            # 0172 BOVB
            # 0173 DMP*
            # 0174 SR4,VSR8
            # 0175 SETPD
            # 0176 BOV

            # Name                 Method           Mnemonic    Opcode	Operands	Increment     Type                        Argcode
            "ABS":    Interpretive("ABS",           "ABS",      0130,   0),
            "ABVAL":  Interpretive("ABVAL",         "ABVAL",    0130,   0),
            "ACOS":   Interpretive("ACOS",          "ACOS",     0050,   0),
            "ARCCOS": Interpretive("ACOS",          "ARCCOS",   0050,   0),
            "ARCSIN": Interpretive("ASIN",          "ARCSIN",   0040,   0),
            "ASIN":   Interpretive("ASIN",          "ASIN",     0040,   0),
            "AXC,1":  Interpretive("Index",         "AXC,1",    0016,   1),
            "AXC,2":  Interpretive("Index",         "AXC,2",    0012,   1),
            "AXT,1":  Interpretive("AXT",           "AXT,1",    0006,   1),
            "AXT,2":  Interpretive("AXT",           "AXT,2",    0002,   1),
            "BDDV":   Interpretive("BDDV",          "BDDV",     0111,   1,          True),
            "BDDV*":  Interpretive("BDDV",          "BDDV*",    0113,   1,          True),
            "BDSU":   Interpretive("BDSU",          "BDSU",     0155,   1,          True),
            "BDSU*":  Interpretive("BDSU",          "BDSU*",    0157,   1,          True),
            "BHIZ":   Interpretive("Branch",        "BHIZ",     0146,   1),
            "BMN":    Interpretive("Branch",        "BMN",      0136,   1),
            "BOF":    Interpretive("Switch",        "BOF",      0162,   2,  		False,        InterpretiveType.SWITCH,    016),
            "BOFCLR": Interpretive("Switch",        "BOFCLR",   0162,   2,  		False,        InterpretiveType.SWITCH,    012),
            "BOFF":   Interpretive("Switch",        "BOFF",     0162,   2,  		False,        InterpretiveType.SWITCH,    016),
            "BOFINV": Interpretive("Switch",        "BOFINV",   0162,   2,  		False,        InterpretiveType.SWITCH,    006),
            "BOFSET": Interpretive("Switch",        "BOFSET",   0162,   2,  		False,        InterpretiveType.SWITCH,    002),
            "BON":    Interpretive("Switch",        "BON",      0162,   2,  		False,        InterpretiveType.SWITCH,    014),
            "BONCLR": Interpretive("Switch",        "BONCLR",   0162,   2,  		False,        InterpretiveType.SWITCH,    010),
            "BONINV": Interpretive("Switch",        "BONINV",   0162,   2,  		False,        InterpretiveType.SWITCH,    004),
            "BONSET": Interpretive("Switch",        "BONSET",   0162,   2,  		False,        InterpretiveType.SWITCH,    000),
            "BOV":    Interpretive("Branch",        "BOV",      0176,   1),
            "BOVB":   Interpretive("Branch",        "BOVB",     0172,   1),
            "BPL":    Interpretive("Branch",        "BPL",      0132,   1),
            "BVSU":   Interpretive("BVSU",          "BVSU",     0131,   1,          True),
            "BVSU*":  Interpretive("BVSU",          "BVSU*",    0133,   1,          True),
            "BZE":    Interpretive("Branch",        "BZE",      0122,   1),
            "CALL":   Interpretive("Branch",        "CALL",     0152,   1),
            "CALRB":  Interpretive("Branch",        "CALRB",    0152,   1),
            "CCALL":  Interpretive("Branch",        "CCALL",    0065,   2,          True),
            "CCALL*": Interpretive("Branch",        "CCALL*",   0067,   2,          True),
            "CGOTO":  Interpretive("Branch",        "CGOTO",    0021,   2,          True),
            "CGOTO*": Interpretive("Branch",        "CGOTO*",   0023,   2,          True),
            "CLEAR":  Interpretive("Switch",        "CLEAR",    0162,   1,  		False,        InterpretiveType.SWITCH,    013),
            "CLR":    Interpretive("Switch",        "CLR",      0162,   1,  		False,        InterpretiveType.SWITCH,    013),
            "CLRGO":  Interpretive("Switch",        "CLRGO",    0162,   2,  		False,        InterpretiveType.SWITCH,    011),
            "COS":    Interpretive("COS",           "COS",      0030,   0),
            "COSINE": Interpretive("COS",           "COSINE",   0030,   0),
            "DAD":    Interpretive("DAD",           "DAD",      0161,   1,          True),
            "DAD*":   Interpretive("DAD",           "DAD*",     0163,   1,          True),
            "DCOMP":  Interpretive("DCOMP",         "DCOMP",    0100,   0),
            "DDV":    Interpretive("DDV",           "DDV",      0105,   1,          True),
            "DDV*":   Interpretive("DDV",           "DDV*",     0107,   1,          True),
            "DLOAD":  Interpretive("DLOAD",         "DLOAD",    0031,   1,          True),
            "DLOAD*": Interpretive("DLOAD",         "DLOAD*",   0033,   1,          True),
            "DMP":    Interpretive("DMP",           "DMP",      0171,   1,          True),
            "DMP*":   Interpretive("DMP",           "DMP*",     0173,   1,          True),
            "DMPR":   Interpretive("DMPR",          "DMPR",     0101,   1,          True),
            "DMPR*":  Interpretive("DMPR",          "DMPR*",    0103,   1,          True),
            "DOT":    Interpretive("DOT",           "DOT",      0135,   1,          True),
            "DOT*":   Interpretive("DOT",           "DOT*",     0137,   1,          True),
            "DSQ":    Interpretive("DSQ",           "DSQ",      0060,   0),
            "DSU":    Interpretive("DSU",           "DSU",      0151,   1,          True),
            "DSU*":   Interpretive("DSU",           "DSU*",     0153,   1,          True),
            "EXIT":   Interpretive("EXIT",          "EXIT",     0000,   0),
            "GOTO":   Interpretive("Branch",        "GOTO",     0126,   1),
            "INCR,1": Interpretive("Index",         "INCR,1",   0066,   1),
            "INCR,2": Interpretive("Index",         "INCR,2",   0062,   1),
            "INVERT": Interpretive("Switch",        "INVERT",   0162,   1,  		False,        InterpretiveType.SWITCH,    007),
            "INVGO":  Interpretive("Switch",        "INVGO",    0162,   2,  		False,        InterpretiveType.SWITCH,    005),
            "ITA":    Interpretive("ITA",           "ITA",      0156,   1),
            "LXA,1":  Interpretive("Index",         "LXA,1",    0026,   1),
            "LXA,2":  Interpretive("Index",         "LXA,2",    0022,   1),
            "LXC,1":  Interpretive("Index",         "LXC,1",    0036,   1),
            "LXC,2":  Interpretive("Index",         "LXC,2",    0032,   1),
            "MXV":    Interpretive("MXV",           "MXV",      0055,   1,          True),
            "MXV*":   Interpretive("MXV",           "MXV*",     0057,   1,          True),
            "NORM":   Interpretive("NORM",          "NORM",     0075,   1,          True),
            "NORM*":  Interpretive("NORM",          "NORM*",    0077,   1,          True),
            "PDDL":   Interpretive("PDDL",          "PDDL",     0051,   1,          True),
            "PDDL*":  Interpretive("PDDL",          "PDDL*",    0053,   1,          True),
            "PDVL":   Interpretive("PDVL",          "PDVL",     0061,   1,          True),
            "PDVL*":  Interpretive("PDVL",          "PDVL*",    0063,   1,          True),
            "PUSH":   Interpretive("PUSH",          "PUSH",     0170,   0),
            "ROUND":  Interpretive("ROUND",         "ROUND",    0070,   0),
            "RTB":    Interpretive("Branch",        "RTB",      0142,   1),
            "RVQ":    Interpretive("RVQ",           "RVQ",      0160,   0),
            "SET":    Interpretive("Switch",        "SET",      0162,   1,  		False,        InterpretiveType.SWITCH,    003),
            "SETGO":  Interpretive("Switch",        "SETGO",    0162,   2,  		False,        InterpretiveType.SWITCH,    001),
            "SETPD":  Interpretive("SETPD",         "SETPD",    0175,   1,          True),
            "SIGN":   Interpretive("SIGN",          "SIGN",     0011,   1,          True),
            "SIGN*":  Interpretive("SIGN",          "SIGN*",    0013,   1,          True),
            "SIN":    Interpretive("SIN",           "SIN",      0020,   0),
            "SINE":   Interpretive("SIN",           "SINE",     0020,   0),
            "SL":     Interpretive("Shift",         "SL",       0115,   1,  		True,         InterpretiveType.SHIFT,     0202),
            "SL*":    Interpretive("Shift",         "SL*",      0117,   1,  		True,         InterpretiveType.SHIFT,     0202),
            "SL1":    Interpretive("SL",            "SL1",      0024,   0,          True),
            "SL1R":   Interpretive("SL",            "SL1R",     0004,   0,          True),
            "SL2":    Interpretive("SL",            "SL2",      0064,   0,          True),
            "SL2R":   Interpretive("SL",            "SL2R",     0044,   0,          True),
            "SL3":    Interpretive("SL",            "SL3",      0124,   0,          True),
            "SL3R":   Interpretive("SL",            "SL3R",     0104,   0,          True),
            "SL4":    Interpretive("SL",            "SL4",      0164,   0,          True),
            "SL4R":   Interpretive("SL",            "SL4R",     0144,   0,          True),
            "SLOAD":  Interpretive("SLOAD",         "SLOAD",    0041,   1,          True),
            "SLOAD*": Interpretive("SLOAD",         "SLOAD*",   0043,   1,          True),
            "SLR":    Interpretive("Shift",         "SLR",      0115,   1,  		True,         InterpretiveType.SHIFT,     0212),
            "SLR*":   Interpretive("Shift",         "SLR*",     0117,   1,  		True,         InterpretiveType.SHIFT,     0212),
            "SQRT":   Interpretive("SQRT",          "SQRT",     0010,   0,          True),
            "SR":     Interpretive("Shift",         "SR",       0115,   1,  		True,         InterpretiveType.SHIFT,     0206),
            "SR*":    Interpretive("Shift",         "SR*",      0117,   1,  		True,         InterpretiveType.SHIFT,     0206),
            "SR1":    Interpretive("SR",            "SR1",      0034,   0,          True),
            "SR1R":   Interpretive("SR",            "SR1R",     0014,   0,          True),
            "SR2":    Interpretive("SR",            "SR2",      0074,   0,          True),
            "SR2R":   Interpretive("SR",            "SR2R",     0054,   0,          True),
            "SR3":    Interpretive("SR",            "SR3",      0134,   0,          True),
            "SR3R":   Interpretive("SR",            "SR3R",     0114,   0,          True),
            "SR4":    Interpretive("SR",            "SR4",      0174,   0,          True),
            "SR4R":   Interpretive("SR",            "SR4R",     0154,   0,          True),
            "SRR":    Interpretive("Shift",         "SRR",      0115,   1,  		True,         InterpretiveType.SHIFT,     0216),
            "SRR*":   Interpretive("Shift",         "SRR*",     0117,   1,  		True,         InterpretiveType.SHIFT,     0216),
            "SSP":    Interpretive("SSP",           "SSP",      0045,   2,          True),
            "SSP*":   Interpretive("SSP",           "SSP*",     0047,   1,          True),
            "STADR":  Interpretive("STADR",         "STADR",    0150,   0),
            "STCALL": Interpretive("STCALL",        "STCALL",   034000, 2,          True),
            "STODL":  Interpretive("StoreLoad",     "STODL",    014000, 2,          True),
            "STODL*": Interpretive("StoreLoad",     "STODL*",   020000, 2,          True),
            "STORE":  Interpretive("STORE",         "STORE",    000000, 1,          True),
            "STOVL":  Interpretive("StoreLoad",     "STOVL",    024000, 2,          True),
            "STOVL*": Interpretive("StoreLoad",     "STOVL*",   030000, 2,          True),
            "STQ":    Interpretive("STQ",           "STQ",      0156,   1),
            "SXA,1":  Interpretive("Index",         "SXA,1",    0046,   1),
            "SXA,2":  Interpretive("Index",         "SXA,2",    0042,   1),
            "TAD":    Interpretive("TAD",           "TAD",      0005,   1,          True),
            "TAD*":   Interpretive("TAD",           "TAD*",     0007,   1,          True),
            "TIX,1":  Interpretive("Branch",        "TIX,1",    0076,   1),
            "TIX,2":  Interpretive("Branch",        "TIX,2",    0072,   1),
            "TLOAD":  Interpretive("TLOAD",         "TLOAD",    0025,   1,          True),
            "TLOAD*": Interpretive("TLOAD",         "TLOAD*",   0027,   1,          True),
            "UNIT":   Interpretive("UNIT",          "UNIT",     0120,   0),
            "UNIT*":  Interpretive("UNIT",          "UNIT*",    0122,   0),
            "V/SC":   Interpretive("VSC",           "V/SC",     0035,   1,          True),
            "V/SC*":  Interpretive("VSC",           "V/SC*",    0037,   1,          True),
            "VAD":    Interpretive("VAD",           "VAD",      0121,   1,          True),
            "VAD*":   Interpretive("VAD",           "VAD*",     0123,   1,          True),
            "VCOMP":  Interpretive("VCOMP",         "VCOMP",    0100,   0),
            "VDEF":   Interpretive("VDEF",          "VDEF",     0110,   0),
            "VLOAD":  Interpretive("VLOAD",         "VLOAD",    0001,   1,          True),
            "VLOAD*": Interpretive("VLOAD",         "VLOAD*",   0003,   1,          True),
            "VPROJ":  Interpretive("VPROJ",         "VPROJ",    0145,   1,          True),
            "VPROJ*": Interpretive("VPROJ",         "VPROJ*",   0147,   1,          True),
            "VSL":    Interpretive("Shift",         "VSL",      0115,   1,  		True,         InterpretiveType.SHIFT,     0202),
            "VSL*":   Interpretive("Shift",         "VSL*",     0117,   1,  		True,         InterpretiveType.SHIFT,     0202),
            "VSL1":   Interpretive("VSL1",          "VSL1",     0004,   0,          True),
            "VSL2":   Interpretive("VSL2",          "VSL2",     0024,   0,          True),
            "VSL3":   Interpretive("VSL3",          "VSL3",     0044,   0,          True),
            "VSL4":   Interpretive("VSL4",          "VSL4",     0064,   0,          True),
            "VSL5":   Interpretive("VSL5",          "VSL5",     0104,   0,          True),
            "VSL6":   Interpretive("VSL6",          "VSL6",     0124,   0,          True),
            "VSL7":   Interpretive("VSL7",          "VSL7",     0144,   0,          True),
            "VSL8":   Interpretive("VSL8",          "VSL8",     0164,   0,          True),
            "VSQ":    Interpretive("VSQ",           "VSQ",      0140,   0),
            "VSR":    Interpretive("Shift",         "VSR",      0115,   1,  		True,         InterpretiveType.SHIFT,     0206),
            "VSR*":   Interpretive("Shift",         "VSR*",     0117,   1,  		True,         InterpretiveType.SHIFT,     0206),
            "VSR1":   Interpretive("VSR1",          "VSR1",     0014,   0,          True),
            "VSR2":   Interpretive("VSR2",          "VSR2",     0034,   0,          True),
            "VSR3":   Interpretive("VSR3",          "VSR3",     0054,   0,          True),
            "VSR4":   Interpretive("VSR4",          "VSR4",     0074,   0,          True),
            "VSR5":   Interpretive("VSR5",          "VSR5",     0114,   0,          True),
            "VSR6":   Interpretive("VSR6",          "VSR6",     0134,   0,          True),
            "VSR7":   Interpretive("VSR7",          "VSR7",     0154,   0,          True),
            "VSR8":   Interpretive("VSR8",          "VSR8",     0174,   0,          True),
            "VSU":    Interpretive("VSU",           "VSU",      0125,   1,          True),
            "VSU*":   Interpretive("VSU",           "VSU*",     0127,   1,          True),
            "VXM":    Interpretive("VXM",           "VXM",      0071,   1,          True),
            "VXM*":   Interpretive("VXM",           "VXM*",     0073,   1,          True),
            "VXSC":   Interpretive("VXSC",          "VXSC",     0015,   1,          True),
            "VXSC*":  Interpretive("VXSC",          "VXSC*",    0017,   1,          True),
            "VXV":    Interpretive("VXV",           "VXV",      0141,   1,          True),
            "VXV*":   Interpretive("VXV",           "VXV*",     0143,   1,          True),
            "XAD,1":  Interpretive("Index",         "XAD,1",    0106,   1),
            "XAD,2":  Interpretive("Index",         "XAD,2",    0102,   1),
            "XCHX,1": Interpretive("Index",         "XCHX,1",   0056,   1),
            "XCHX,2": Interpretive("Index",         "XCHX,2",   0052,   1),
            "XSU,1":  Interpretive("Index",         "XSU,1",    0116,   1),
            "XSU,2":  Interpretive("Index",         "XSU,2",    0112,   1)
        }
    }
}
