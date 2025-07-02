from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("alu_template.sv.j2")
output = template.render(width=32)

with open("src/alu_32bit.sv", "w") as f:
    f.write(output)

print("✅ Template rendered to src/alu_32bit.sv")
