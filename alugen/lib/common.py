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

# === namedtuple ===
Operation = namedtuple("Operation", ["op_type", "num_operands", "operand_types"])

# op_type field is now a mnemonic string matching SemanticOperation.mnemonic
# operand_types tuple: (input_0, input_1, ..., output)

# --- type groups ---
_INT_TYPES   = [INT8,   INT16,   INT32,   INT64  ]
_UINT_TYPES  = [UINT8,  UINT16,  UINT32,  UINT64 ]
_FLOAT_TYPES = [FLOAT16, FLOAT32, FLOAT64        ]

_INT_UINT_TYPES = _INT_TYPES + _UINT_TYPES           # integer bitwise/shift ops
_ALL_NUM_TYPES  = _INT_TYPES + _UINT_TYPES + _FLOAT_TYPES  # arithmetic + fma

# --- add group op lists ---
_ADD_SUB_OPS = ["add", "sub"]            # numeric output, all numeric types
_CMP_OPS     = ["lt", "gt", "le", "ge"]  # bool output, all numeric types

# --- bool group op lists ---
_BOOL_UNARY_OPS  = ["not"]                                               # 1-input, bool output
_BOOL_BINARY_OPS = ["xor", "eq", "ne", "and", "or", "nand", "nor", "xnor"]  # 2-input, bool output

# --- shift group op list ---
_SHIFT_OPS = ["lsl", "lsr", "asr", "rol", "ror"]  # int/uint only (undefined for floats)

# operations are not groups here but renderer needs some classification to know which alus to generate or not generate
OPERATIONS_US: Dict[str, List[Operation]] = {
    "add": [
        # numeric output: all numeric types
        Operation(op, 2, (t, t, t))
        for op in _ADD_SUB_OPS
        for t in _ALL_NUM_TYPES
    ] + [
        # bool output: all numeric types
        Operation(op, 2, (t, t, BOOL))
        for op in _CMP_OPS
        for t in _ALL_NUM_TYPES
    ],
    "bool": [
        # unary bool output: int/uint only (bitwise ops undefined for floats)
        Operation(op, 1, (t, BOOL))
        for op in _BOOL_UNARY_OPS
        for t in _INT_UINT_TYPES
    ] + [
        # binary bool output: int/uint only
        Operation(op, 2, (t, t, BOOL))
        for op in _BOOL_BINARY_OPS
        for t in _INT_UINT_TYPES
    ],
    "shift": [
        # numeric output: int/uint only (shifts undefined for floats)
        Operation(op, 2, (t, t, t))
        for op in _SHIFT_OPS
        for t in _INT_UINT_TYPES
    ],
    "mul": [
        # numeric output: all numeric types (result truncated to input width for integers)
        Operation("mul", 2, (t, t, t))
        for t in _ALL_NUM_TYPES
    ],
    "fma": [
        # A*B+C: 3 inputs, numeric output, all numeric types
        Operation("fma", 3, (t, t, t, t))
        for t in _ALL_NUM_TYPES
    ],
}
