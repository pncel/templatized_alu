from enum import Enum, auto
from collections import namedtuple
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Union
from dora.core.arch.isa.datatype import (
    ArchDataType,
    ArchVectorType,
    ArchUnionType,
    ArchIntegerType,
    ArchFloatType,
    ArchFixedType,
)
from dora.core.arch.isa import *
from dora.core.arch.isa.ops import ArchOpType, OpType

# shared information between generator and module.

# === Supported Opcodes Definition ===
#     "add": ["add", "sub", "lt", "gt", "le", "ge"],
#     "bool": ["le", "ge", "xor", "eq", "ne", "and", "or", "not", "nand", "nor", "xnor"],
#     "shift": ["sll", "slr", "sar", "rotationleft", "rotationright"],

# === namedtuple ===
Operation = namedtuple("Operation", ["op_type", "num_operands", "operand_types"])

# operations are not groups here but renderer needs some classification to know which alus to generate or not generate
OPERATIONS_US: Dict[str, List[Operation]] = {
    "add": [
        Operation(OpType.ADD, 2, (INT32, INT32, INT32)),
        Operation(OpType.ADD, 2, (INT16, INT16, INT16)),
        Operation(OpType.ADD, 2, (INT8, INT8, INT8)),
        Operation(OpType.SUB, 2, (INT32, INT32, INT32)),
        Operation(OpType.SUB, 2, (INT8, INT8, INT8)),
        Operation(OpType.LT, 2, (INT32, INT32, BOOL)),
        Operation(OpType.GT, 2, (INT32, INT32, BOOL)),
        Operation(OpType.LE, 2, (INT32, INT32, BOOL)),
        Operation(OpType.GE, 2, (INT32, INT32, BOOL)),
    ],
    "bool": [
        Operation(OpType.XOR, 2, (INT32, INT32, BOOL)),
        Operation(OpType.EQ, 2, (INT32, INT32, BOOL)),
        Operation(OpType.NE, 2, (INT32, INT32, BOOL)),
        Operation(OpType.AND, 2, (INT32, INT32, BOOL)),
        Operation(OpType.OR, 2, (INT32, INT32, BOOL)),
        Operation(OpType.NOT, 1, (INT32, BOOL)),
        Operation(OpType.NAND, 2, (INT32, INT32, BOOL)),
        Operation(OpType.NOR, 2, (INT32, INT32, BOOL)),
        Operation(OpType.XNOR, 2, (INT32, INT32, BOOL)),
    ],
    "shift": [
        Operation(OpType.LSL, 2, (INT32, INT32, INT32)),
        Operation(OpType.LSR, 2, (INT32, INT32, INT32)),
        Operation(OpType.ASR, 2, (INT32, INT32, INT32)),
        Operation(OpType.ROL, 2, (INT32, INT32, INT32)),
        Operation(OpType.ROR, 2, (INT32, INT32, INT32)),
    ],
    "mul": [
        # multiplier: keep result width same as inputs (truncated) so it fits the existing ALU result conventions
        Operation(OpType.MUL, 2, (INT32, INT32, INT32)),
        Operation(OpType.MUL, 2, (INT8, INT8, INT8)),
    ],
}
