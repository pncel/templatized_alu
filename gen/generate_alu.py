from jinja2 import Environment, FileSystemLoader
import os
import math

# === User Configuration ===
module_name = "alu32bit"
width = 32
# List of user-selected operations
user_ops = ["add", "sub", "le", "xor", "sll", "sar", "rotationleft", "rotationright"] # for loops tbd

# === Define Operation Groups ===
group_map = {
    "addgroup": ["add", "sub"],
    "boolgroup": ["lt", "gt"],
    "shiftgroup": ["sll", "srl"],
    # Add more groups here as needed
}

# === Filter Active Groups ===#
# Determine which groups have at least one selected operation
active_groups = {}
for group_name, members in group_map.items():
    # Build a list of operations from this group that the user selected
    selected_ops = []
    # Collecting 
    for op in members:
        if op in user_ops:
            selected_ops.append(op)
    if selected_ops:
        active_groups[group_name] = selected_ops

# === Flatten Operations Dynamically ===#
# Iterate in the defined order of group_map to support any number of categories
flattened_ops = []
for group_name in group_map:
    # Extend by any selected operations in this group, or skip if none
    flattened_ops.extend(active_groups.get(group_name, []))

# === Compute op_width Dynamically ===
enabled_ops_count = len(flattened_ops)
if enabled_ops_count == 0:
    raise ValueError("No operations selected.")
# Minimum 1 bit, else ceil(log2(count))
op_width = max(1, math.ceil(math.log2(enabled_ops_count)))

# === Assign Default Opcodes ===#
default_opcodes = {}
for index, op in enumerate(flattened_ops):
    code = format(index, f'0{op_width}b')
    default_opcodes[op] = code

# === Jinja2 Rendering ===#
env = Environment(
    loader=FileSystemLoader("templates"),
    trim_blocks=True,
    lstrip_blocks=True
)
template = env.get_template("alu_template.sv.j2")

# === Render Template ===
rendered = template.render(
    module_name=module_name,
    width=width,
    ops=flattened_ops,
    op_width=op_width,
    op_code=default_opcodes,
    groups=active_groups,
)

# === Write Output File ===#
output_dir = "src"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, f"{module_name}.sv")

with open(output_path, "w") as f:
    f.write(rendered)

print(f"✅ Generated {output_path}")
