from jinja2 import Environment, FileSystemLoader
import os

# === User Configuration ===
module_name = "alu32bit"
width = 32
ops = ["add", "lt"]
#ops = ["add", "sub", "lt", "gt"]  # Customize this list as needed

# === Jinja2 Setup ===
env = Environment(loader=FileSystemLoader("templates"),
                  trim_blocks=True,
                  lstrip_blocks=True)
template = env.get_template("adder_template.sv.j2")

# === Render Template ===
rendered = template.render(
    module_name=module_name,
    width=width,
    ops=ops
)

# === Write Output File ===
output_dir = "src"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, f"{module_name}.sv")

with open(output_path, "w") as f:
    f.write(rendered)

print(f"✅ Generated {output_path}")
