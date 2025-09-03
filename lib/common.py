from enum import Enum, auto
from collections import namedtuple
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Union
from dora.core.arch.isa.datatype import (
    ArchDataType, ArchVectorType, ArchUnionType, 
    ArchIntegerType, ArchFloatType, ArchFixedType
)
from dora.core.arch.isa import *
from dora.core.arch.isa.ops import ArchOpType, OpType
# shared information between generator and module.

# === Supported Opcodes Definition ===
# _SUPPORTED_OPCODE_GROUPS: Dict[str, List[str]] = {
#     "add": ["add", "sub", "lt", "gt", "le", "ge"],
#     "bool": ["le", "ge", "xor", "eq", "ne", "and", "or", "not", "nand", "nor", "xnor"],
#     "shift": ["sll", "slr", "sar", "rotationleft", "rotationright"],
# }

# === Tuple Approach ===
# ArchDataType vs. str for tuple definitions? 
Operation = namedtuple("Operation", ["op_type", "num_operands", "result_type", "lhs_type", "rhs_type"])

# operations are not groups here but renderer needs some classification to know which alus to generate or not generate
OPERATIONS_US: Dict[str, List[Operation]] = {
    "add": [
        Operation(OpType.ADD, 2, INT32, INT32, INT32),
        Operation(OpType.SUB, 2, INT32, INT32, INT32),
        Operation(OpType.LT, 2, BOOL, INT32, INT32),
        Operation(OpType.GT, 2, BOOL, INT32, INT32),
        Operation(OpType.LE, 2, BOOL, INT32, INT32),
        Operation(OpType.GE, 2, BOOL, INT32, INT32),
    ],

    "bool": [
        Operation(OpType.XOR, 2, BOOL, INT32, INT32),
        Operation(OpType.EQ, 2, BOOL, INT32, INT32),
        Operation(OpType.NE, 2, BOOL, INT32, INT32),
        Operation(OpType.AND, 2, BOOL, INT32, INT32),
        Operation(OpType.OR, 2, BOOL, INT32, INT32),
        Operation(OpType.NOT, 1, BOOL, INT32),
        Operation(OpType.NAND, 2, BOOL, INT32, INT32),
        Operation(OpType.NOR, 2, BOOL, INT32, INT32),
        Operation(OpType.XNOR, 2, BOOL, INT32, INT32),
    ],

    "shift": [
        Operation(OpType.LSL, 2, INT32, INT32, INT32),
        Operation(OpType.LSR, 2, INT32, INT32, INT32),
        Operation(OpType.ASR, 2, INT32, INT32, INT32),
        Operation(OpType.ROL, 2, INT32, INT32, INT32),
        Operation(OpType.ROR, 2, INT32, INT32, INT32),
    ],
}