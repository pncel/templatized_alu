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

# === Named Tuple Approach ===
# === Opcode Structure Definition ===
Operation = namedtuple('Operation', [
    'optype', 'num_inputs', 'input_A', 'input_B', 'output',
])

# === Opcode Definitions ===
OPERATIONS_NT = [
    Operation(
        optype = OpType.ADD,
        num_inputs = 2,
        input_A = INT32,
        input_B = INT32,
        output = INT32,
    ),
    Operation(
        optype = OpType.SUB,
        num_inputs = 2,
        input_A = INT32,
        input_B = INT32,
        output = INT32,
    )
]

# Final registry
SUPPORTED_GROUPS = OPERATIONS_NT

# === Tuple Approach ===
# ArchDataType vs. str for tuple definitions? 
OperationTuple = Tuple[OpType, int, ArchDataType, ArchDataType, ArchDataType]

OPERATIONS_T : List[OperationTuple] = [
    (OpType.ADD, 2, INT32, INT32, INT32),
    (OpType.SUB, 2, INT32, INT32, INT32),
    (OpType.LT, 2, INT32, INT32, BOOL),
]