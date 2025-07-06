# from lib import ALUConfig, generate_alu
from lib.alu_config import ALUConfig
from lib.alu_generator import ALUGenerator

# SUPPORTED_OPCODES:
#    add   group: "add", "sub", "lt", "gt", "le", "ge"
#    bool  group: "le", "ge", "xor", "eq", "ne", "and", "or", "not", "nand", "nor", "xnor"
#    shift group: "sll", "slr", "sar", "rotationleft", "rotationright"

def main():
    # 1. Initialize datatype width
    config = ALUConfig(
        width=32
    )

    # 2. Declare operations you need (validatated against SUPPORTED_OPCODES)
    #    Anything added not in SUPPORTED_OPCODES will raise an error.
    config.user_opcodes = [
        "add", "sub", "lt", "gt",  # Arithmetic operations
        "xor", "eq", "ne", "and",  # Boolean operations
        "sll", "slr", "rotationleft"  # Shift operations
    ]

    # 3. (Optional) Define input constraints for testing
    # If omitted, A and B defaults to [0, 2**width - 1]
    config.range('A', 0, 100)
    config.range('B', 0, 100)

    # # 4. Export constrains to JSON for generation.
    # json_path = "constraints.json"
    # config.to_json(json_path)

    # # 5) Now call generate_alu, pointing at that JSON
    #     # By default it’ll write .sv files into ./src/
    # try:
    #     generate_alu(json_path, output_dir="src")
    # except FileNotFoundError as e:
    #     print(f"❌ {e}")
    #     return
    # except ValueError as e:
    #     print(f"❌ {e}")
    #     return

    generator = ALUGenerator(config)
    try:
        generator.generate()
    except ValueError as e:
        print(f"❌ {e}")

    print("🎉 All .sv files have been generated into ./src/")

if __name__ == "__main__":
    main()
