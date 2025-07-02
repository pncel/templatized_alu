from jinja2 import Environment, FileSystemLoader

# Load Jinja2 environment from current directory
env = Environment(loader=FileSystemLoader("templates"))
# Load the template file
template = env.get_template("Mux_template.sv.j2")

# Render the template with parameters
rendered = template.render(
    module_name="Mux32to1",
    width=64,
    num_inputs=32
)

# Output to file
with open("src/Mux32to1.sv", "w") as f:
    f.write(rendered)

print("Generated Mux32to1.sv")
