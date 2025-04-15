from jinja2 import Environment, FileSystemLoader
from itertools import chain, combinations
import os

# Initialize Jinja2 with whitespace trimming
env = Environment(
    loader=FileSystemLoader("templates"),
    trim_blocks=True,
    lstrip_blocks=True
)
template = env.get_template("alu_template.sv.j2")

# All possible operations
all_ops = ["add", "sub", "lt", "gt"]

# Get all non-empty subsets of ops
def all_nonempty_subsets(ops):
    return chain.from_iterable(combinations(ops, r) for r in range(1, len(ops) + 1))

# Create output dir
output_dir = "src/generated"
os.makedirs(output_dir, exist_ok=True)

# Width of the ALU
width = 32

# Generate all combinations
for ops_combo in all_nonempty_subsets(all_ops):
    ops_list = list(ops_combo)
    ops_suffix = "_".join(ops_list)
    module_name = f"alu_{width}bit_{ops_suffix}"

    rendered = template.render(
        module_name=module_name,
        width=width,
        ops=ops_list
    )

    output_path = os.path.join(output_dir, f"{module_name}.sv")
    with open(output_path, "w") as f:
        f.write(rendered)

    print(f"✅ Generated {output_path}")
