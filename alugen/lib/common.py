from enum import Enum, auto
from collections import namedtuple
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Union
from dora.core.arch.isa.datatype import (
    ArchDataType, ArchVectorType, ArchUnionType, 
    ArchIntegerType, ArchFloatType, ArchFixedType
)
from dora.core.arch.isa.ops import ArchOpType, OpType
from dora.core.arch.isa import INT32, BOOL
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

OPERATIONS_US : List[OperationTuple] = [
    (OpType.ADD, 2, INT32, INT32, INT32),
    (OpType.SUB, 2, INT32, INT32, INT32),
    (OpType.LT, 2, BOOL, INT32, INT32),
    (OpType.GT, 2, BOOL, INT32, INT32),
    (OpType.LE, 2, BOOL, INT32, INT32),
    (OpType.GE, 2, BOOL, INT32, INT32),
    
    # Bool group operations
    (OpType.XOR, 2, BOOL, INT32, INT32),
    (OpType.EQ, 2, BOOL, INT32, INT32), 
    (OpType.NE, 2, BOOL, INT32, INT32), 
    (OpType.AND, 2, BOOL, INT32, INT32),
    (OpType.OR, 2, BOOL, INT32, INT32),
    (OpType.NOT, 1, BOOL, INT32, INT32),
    (OpType.NAND, 2, BOOL, INT32, INT32),
    (OpType.NOR, 2, BOOL, INT32, INT32),
    (OpType.XNOR, 2, BOOL, INT32, INT32),
    
    # Shift group operations
    (OpType.SLL, 2, INT32, INT32, INT32),      # Shift logical left / SLL
    (OpType.SLR, 2, INT32, INT32, INT32),      # Shift logical right / SRL
    (OpType.SAR, 2, INT32, INT32, INT32),      # Shift arithmetic right / SRA
    (OpType.ROTATIONLEFT, 2, INT32, INT32, INT32),
    (OpType.ROTATIONRIGHT, 2, INT32, INT32, INT32),
]