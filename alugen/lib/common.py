from collections import namedtuple
from typing import List, Dict
from dora.core.arch.isa import (
    BOOL,
    INT8,
    INT16,
    INT32,
    INT64,
    UINT8,
    UINT16,
    UINT32,
    UINT64,
    FLOAT16,
    FLOAT32,
    FLOAT64,
)

# shared information between generator and module.

# === Supported Opcodes Definition ===
#     "add": ["add", "sub", "lt", "gt", "le", "ge"],
#     "bool": ["le", "ge", "xor", "eq", "ne", "and", "or", "not", "nand", "nor", "xnor"],
#     "shift": ["sll", "slr", "sar", "rotationleft", "rotationright"],

# === namedtuple ===
Operation = namedtuple("Operation", ["op_type", "num_operands", "operand_types"])

# operations are not groups here but renderer needs some classification to know which alus to generate or not generate
# op_type field is now a mnemonic string matching SemanticOperation.mnemonic
OPERATIONS_US: Dict[str, List[Operation]] = {
    "add": [
        Operation("add", 2, (INT32, INT32, INT32)),
        Operation("add", 2, (INT16, INT16, INT16)),
        Operation("add", 2, (INT8, INT8, INT8)),
        Operation("sub", 2, (INT32, INT32, INT32)),
        Operation("sub", 2, (INT8, INT8, INT8)),
        Operation("sub", 2, (INT16, INT16, INT16)),
        Operation("lt",  2, (INT32, INT32, BOOL)),
        Operation("gt",  2, (INT32, INT32, BOOL)),
        Operation("le",  2, (INT32, INT32, BOOL)),
        Operation("ge",  2, (INT32, INT32, BOOL)),
    ],
    "bool": [
        Operation("xor",  2, (INT32, INT32, BOOL)),
        Operation("eq",   2, (INT32, INT32, BOOL)),
        Operation("ne",   2, (INT32, INT32, BOOL)),
        Operation("and",  2, (INT32, INT32, BOOL)),
        Operation("or",   2, (INT32, INT32, BOOL)),
        Operation("not",  1, (INT32, BOOL)),
        Operation("nand", 2, (INT32, INT32, BOOL)),
        Operation("nor",  2, (INT32, INT32, BOOL)),
        Operation("xnor", 2, (INT32, INT32, BOOL)),
    ],
    "shift": [
        Operation("lsl", 2, (INT32, INT32, INT32)),
        Operation("lsr", 2, (INT32, INT32, INT32)),
        Operation("asr", 2, (INT32, INT32, INT32)),
        Operation("rol", 2, (INT32, INT32, INT32)),
        Operation("ror", 2, (INT32, INT32, INT32)),
    ],
    "mul": [
        # multiplier: keep result width same as inputs (truncated) so it fits the existing ALU result conventions
        Operation("mul", 2, (INT32, INT32, INT32)),
        Operation("mul", 2, (INT16, INT16, INT16)),
        Operation("mul", 2, (INT8, INT8, INT8)),
    ],
}
