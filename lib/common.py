# shared information between generator and module.

# === Supported Opcodes Definition ===
# supported ops should be a named tuple
# make into enum instead of strings
# describe ISA by mapping each operation to a tuple (number of inputs, number of outputs, and datatype)
# ^ separate file to describe the classes for operations
_SUPPORTED_OPCODE_GROUPS: Dict[str, List[str]] = {
    "add": ["add", "sub", "lt", "gt", "le", "ge"],
    "bool": ["le", "ge", "xor", "eq", "ne", "and", "or", "not", "nand", "nor", "xnor"],
    "shift": ["sll", "slr", "sar", "rotationleft", "rotationright"],
}

# operation type could be common()
