from jinja2 import Environment, FileSystemLoader
<<<<<<< HEAD
import sys
import os
import math
import json

# === CLI Argument Parsing === #
if len(sys.argv) != 2:
    print("Usage: python gen/generate_alu.py <path/to/constraints.json>")
    sys.exit(1)
constraint_path = sys.argv[1]

# === Check if constraints file exists === #
if not os.path.isfile(constraint_path):
    print(f"Error: Constraints file '{constraint_path}' does not exist.")
    sys.exit(1)

# === Load User Constraints === #
with open(constraint_path, "r") as f:
    constraints = json.load(f)

# === User Configuration === #
module_name = "templatized_alu"
width = constraints.get("width", 32)  # Default to 32 bits if not specified

# List of user-selected operations
user_ops = constraints.get("supported_opcodes")

# === Define Operation Groups === #
=======
import os
import math

print("👀 Current Working Directory:", os.getcwd())

# === User Configuration ===
module_name = "templatized_alu"
width = 16
# List of user-selected operations
user_ops = ["add", "sub", "le", "gt", "nor", "sll", "sar", "rotationleft", "rotationright"]

# === Define Operation Groups ===
>>>>>>> origin/Ayush
group_map = {
    "add": ["add", "sub", "lt", "gt", "le", "ge"],
    "bool": ["le", "ge", "xor", "eq", "ne", "and", "or", "not", "nand", "nor", "xnor"],
    "shift": ["sll", "slr", "sar", "rotationleft", "rotationright"],
    
    # for later :)
    # "multiplication": [],
    # "division": []
    # "pop count 1"(number of 1s)
    # "pop count 0"(number of 0s)
    # "leading zero detection"
    # Add more groups here as needed
}

# === Filter Active Groups === #
# Determine which groups have at least one selected operation
active_groups = {}
for group_name, members in group_map.items():
    # Build a list of operations from this group that the user selected
    selected_ops = []
    for op in members:
        if op in user_ops:
            selected_ops.append(op)
    if selected_ops:
        active_groups[group_name] = selected_ops

group_list = list(active_groups.keys())
active_group_count = len(active_groups)

# === Flatten Operations Dynamically === #
# Iterate in the defined order of group_map to support any number of categories
flattened_ops = []
for group_name in group_map:
    # Extend by any selected operations in this group, or skip if none
    flattened_ops.extend(active_groups.get(group_name, []))

# === Compute op_width Dynamically === #
enabled_ops_count = len(flattened_ops)
if enabled_ops_count == 0:
    raise ValueError("No operations selected.")
# Minimum 1 bit, else ceil(log2(count))
op_width = max(1, math.ceil(math.log2(enabled_ops_count)))

# === Assign Default Opcodes === #
default_opcodes = {}
for index, op in enumerate(flattened_ops):
    code = format(index, f'0{op_width}b')
    default_opcodes[op] = code

# === Jinja2 Rendering === # 
env = Environment(
<<<<<<< HEAD
    loader        = FileSystemLoader("templates"),
    trim_blocks   = True,
    lstrip_blocks = True,
=======
    loader=FileSystemLoader("templates"),
    trim_blocks=True,
    lstrip_blocks=True,
>>>>>>> origin/Ayush
)

# add enumerate() as a filter:
env.filters['enumerate'] = enumerate

# === Output File Directory === #
output_dir = "src"
os.makedirs(output_dir, exist_ok=True)

# === Render each group‐ALU only if it’s active ===
for group in group_map.keys(): # ["addgroup", "boolgroup", "shiftgroup"]:
    if group in active_groups:
        tmpl        = env.get_template(f"{group}_group_template.sv.j2")
        # pass only that group’s ops & opcodes
        rendered    = tmpl.render(
            module_name   = f"alu_{group}",
            width         = width,
            op_width      = op_width,
            ops           = active_groups[group],
            op_code       = { op: default_opcodes[op] for op in active_groups[group] },
        )
        path = os.path.join(output_dir, f"alu_{group}.sv")
        with open(path, "w") as f:
            f.write(rendered)
        print(f"✅ Generated {path}")


# === Render control module === #

# Determine the number of bits needed to select a group
sel_width = max(1, math.ceil(math.log2(len(group_list))))


control_tmpl = env.get_template("control_module_template.sv.j2")
control_rendered = control_tmpl.render(
<<<<<<< HEAD
    module_name = module_name,
    op_width    = op_width,
    sel_width   = sel_width,
    groups      = active_groups,
    group_list  = group_list,
    op_code     = { op: default_opcodes[op] for op in flattened_ops }
=======
    module_name=module_name,
    op_width=op_width,
    sel_width=sel_width,
    groups=active_groups,
    group_list=group_list,
    op_code={ op: default_opcodes[op] for op in flattened_ops }
>>>>>>> origin/Ayush
)
control_path = os.path.join(output_dir, f"{module_name}_control.sv")
with open(control_path, "w") as f:
    f.write(control_rendered)
print(f"✅ Generated {control_path}")

# === Render top-level ALU Template === #
top_template = env.get_template("top_level_alu_template_v1.sv.j2")

# === Render Template === #
rendered = top_template.render(
    module_name="templatized_alu",
    width=width,
    ops=flattened_ops,
    op_width=op_width,
    groups=active_groups,
    group_list=group_list,
    active_group_count=active_group_count,
    sel_width=sel_width,
)

top_path = os.path.join(output_dir, f"{module_name}.sv")

with open(top_path, "w") as f:
    f.write(rendered)

print(f"✅ Generated {top_path}")

# === Generate Mux === #
mux_tmpl = env.get_template("Mux_template.sv.j2")
mux_rendered = mux_tmpl.render(
<<<<<<< HEAD
    group_list = group_list,
=======
>>>>>>> origin/Ayush
    num_inputs = active_group_count,
    width      = width
)
mux_path = os.path.join(output_dir, f"mux_generic.sv")
with open(mux_path, "w") as f:
    f.write(mux_rendered)
print(f"✅ Generated {mux_path}")
