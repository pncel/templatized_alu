from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any
import json

# === Supported Opcodes Definition ===
_SUPPORTED_OPCODE_GROUPS: Dict[str, List[str]] = {
    "add": ["add", "sub", "lt", "gt", "le", "ge"],
    "bool": ["le", "ge", "xor", "eq", "ne", "and", "or", "not", "nand", "nor", "xnor"],
    "shift": ["sll", "slr", "sar", "rotationleft", "rotationright"],
}
SUPPORTED_OPCODES: List[str] = [
    opcode for group in _SUPPORTED_OPCODE_GROUPS.values() for opcode in group
]

"""
Core ALU configuration class.
User can define the ALU's behavior by importing this class and 
script their constraints.

width: data-path width in bits
user_opcodes: user-declared list of opcodes that alu should generate
input_constraints: range of input values for each input port for testing. Defaults to [0, 2**width - 1]
"""
@dataclass
class ALUConfig:

    """
    Declares one ore more opcodes. 
    If not supported(not in SUPPORTED_OPCODES), an error will be raised.
    """
    width: int
    user_opcodes: List[str] = field(default_factory=list)
    input_constraints: Dict[str, Tuple[int, int]] = field(default_factory=dict)
    
    def __post_init__(self):
        """
        Set default input ranges for signal 'A' and 'B' to [0, 2**width - 1]
        if not specified by the user.
        """
        default_low = 0
        default_high = 2**self.width - 1
        for sig in ("A", "B"):
            self.input_constraints.setdefault(sig, (default_low, default_high))

    def opcodes(self, *ops: str) -> 'ALUConfig':
        """
        Add user-defined opcodes to the configuration.
        Validates against SUPPORTED_OPCODES.
        """
        return self

    def width_bits(self, bits: int) -> 'ALUConfig':
        """
        Set ALU data-path width in bits.
        """
        self.width = bits
        # Update default ranges based on new width
        return self
    
    def range(self, signal: str, low: int, high: int) -> 'ALUConfig':
        """
        Override default input range for a signal.
        """
        self.input_constraints[signal] = (low, high)
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the configuration to a dictionary.
        """
        return {
            "width": self.width,
            "user_opcodes": list(self.user_opcodes),
            "input_constraints": {sig: [low, high] for sig, (low, high) in self.input_constraints.items()}
            }
    
    def to_json(self, path: str) -> None:
        """
        Export the configuration to a JSON file.
        """
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
