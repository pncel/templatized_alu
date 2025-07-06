from enum import Enum
from dataclasses import dataclass
from typing import List, Dict
# shared information between generator and module.

# === Supported Opcodes Definition ===
# supported ops should be a named tuple
# make into enum instead of strings
# describe ISA by mapping each operation to a tuple (number of inputs, number of outputs, and datatype)
# ^ separate file to describe the classes for operations
# _SUPPORTED_OPCODE_GROUPS: Dict[str, List[str]] = {
#     "add": ["add", "sub", "lt", "gt", "le", "ge"],
#     "bool": ["le", "ge", "xor", "eq", "ne", "and", "or", "not", "nand", "nor", "xnor"],
#     "shift": ["sll", "slr", "sar", "rotationleft", "rotationright"],
# }

class DataType(Enum):
    #stuff

@dataclass(frozen=True)
class Opcode:
    name: str
    num_inputs: int
    num_outputs: int
    datatype: DataType

class OpcodeGroup(Enum):
    ADD = "add"
    BOOL = "bool"
    SHIFT = "shift"

@dataclass
class OpcodeGroupInfo:
    group: OpcodeGroup
    opcodes: List[Opcode]

# Define opcodes
ADD_OPS = [
    Opcode("add", 2, 1, DataType.),
    Opcode("sub", 2, 1, DataType.),
    Opcode("lt", 2, 1, DataType.),
    Opcode("gt", 2, 1, DataType.),
    Opcode("le", 2, 1, DataType.),
    Opcode("ge", 2, 1, DataType.),
]

BOOL_OPS = [
    Opcode("xor", 2, 1, DataType.),
    Opcode("eq", 2, 1, DataType.),
    Opcode("ne", 2, 1, DataType.),
    Opcode("and", 2, 1, DataType.),
    Opcode("or", 2, 1, DataType.),
    Opcode("not", 1, 1, DataType.),
    Opcode("nand", 2, 1, DataType.),
    Opcode("nor", 2, 1, DataType.),
    Opcode("xnor", 2, 1, DataType.),
    Opcode("le", 2, 1, DataType.),
    Opcode("ge", 2, 1, DataType.),
]

SHIFT_OPS = [
    Opcode("sll", 2, 1, DataType.),
    Opcode("slr", 2, 1, DataType.),
    Opcode("sar", 2, 1, DataType.),
    Opcode("rotationleft", 2, 1, DataType.),
    Opcode("rotationright", 2, 1, DataType.),
]

# Final registry
SUPPORTED_GROUPS: List[OpcodeGroupInfo] = [
    OpcodeGroupInfo(OpcodeGroup.ADD, ADD_OPS),
    OpcodeGroupInfo(OpcodeGroup.BOOL, BOOL_OPS),
    OpcodeGroupInfo(OpcodeGroup.SHIFT, SHIFT_OPS),
]