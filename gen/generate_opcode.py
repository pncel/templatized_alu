from jinja2 import Environment, FileSystemLoader

# dictionary to check which operations the user has selected
user_checklist = {
    "add": True,
    "sub": True,
    "gt": True,
    "lt": True,
}

# dictionary for custom opcodes of user
custom_opcodes = {
    "add": None, 
    "sub": None, 
    "gt": None,
    "lt": None,
}

port_size = 32

module_name = "Add ALU"

# Create some sort of check to see how many operations the user has selected and scale the op_width accordingly
# Count how many operations are enabled
enabled_ops_count = sum(user_checklist.values())

# Determine op_width based on the number of operations
# 1-2 ops: 1 bit, 3-4 ops: 2 bits
if enabled_ops_count <= 2:
    op_width = 1
elif enabled_ops_count <= 4:
    op_width = 2
else:
    raise ValueError("Unexpected number of operations selected.")

# Build the default opcodes in the case no user custom opcodes are provided
if op_width == 1:
    # Go through enabled operations and assign opcodes in order of the operations in the user_checklist
    enabled_ops = [op for op in ['add', 'sub', 'gt', 'lt'] if user_checklist.get(op)]
    # Assign opcodes sequentially (as strings) starting from 0.
    default_opcodes = {op: str(i) for i, op in enumerate(enabled_ops)}
elif op_width == 2:
    # Constand, fixed opcodes
    default_opcodes = {
        "add": '00',
        "sub": '01',
        "gt": '10',
        "lt": '11',
    }

# Incorporate any user custom opcodes into the default opcodes
for op in default_opcodes:
    if custom_opcodes[op] is not None:
        # If the user has provided a custom opcode, use it
        default_opcodes[op] = custom_opcodes[op]
    else:
        # Otherwise, use the default opcode
        default_opcodes[op] = default_opcodes[op]

env = Environment(loader=FileSystemLoader("templates"))
# trim_blocks true
# lstrip_blocks true
template = env.get_template("add_alu.tmpl.v")

rendered_template = template.render(
    ops=user_checklist, 
    port_size=port_size, 
    module_name=module_name, 
    op_width=op_width,
    op_code=default_opcodes,
)

with open("generated_add_alu.v", "w") as f:
    f.write(rendered_template)
print("✅ Generated add_alu.v")