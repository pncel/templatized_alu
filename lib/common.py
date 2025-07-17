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
OperationTuple = Tuple[OpType, int, ArchDataType, ArchDataType, ArchDataType]

OPERATIONS_T : List[OperationTuple] = [
    (OpType.ADD, 2, INT32, INT32, INT32),
    (OpType.SUB, 2, INT32, INT32, INT32),
    (OpType.LT, 2, INT32, INT32, BOOL),
    (OpType.GT, 2, INT32, INT32, BOOL),
    (OpType.LE, 2, INT32, INT32, BOOL),
    (OpType.GE, 2, INT32, INT32, BOOL),
    
    # Bool group operations
    (OpType.XOR, 2, INT32, INT32, BOOL),
    (OpType.EQ, 2, INT32, INT32, BOOL), 
    (OpType.NE, 2, INT32, INT32, BOOL), 
    (OpType.AND, 2, INT32, INT32, BOOL),
    (OpType.OR, 2, INT32, INT32, BOOL),
    (OpType.NOT, 1, INT32, INT32, BOOL),
    (OpType.NAND, 2, INT32, INT32, BOOL),
    (OpType.NOR, 2, INT32, INT32, BOOL),
    (OpType.XNOR, 2, INT32, INT32, BOOL),
    
    # Shift group operations
    (OpType.SLL, 2, INT32, INT32, INT32),      # Shift left logical
    (OpType.SLR, 2, INT32, INT32, INT32),      # Shift left right
    (OpType.SAR, 2, INT32, INT32, INT32),      # Shift arithmetic right
    (OpType.ROTATIONLEFT, 2, INT32, INT32, INT32),
    (OpType.ROTATIONRIGHT, 2, INT32, INT32, INT32),
]