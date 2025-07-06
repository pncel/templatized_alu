from jinja2 import Environment, FileSystemLoader
import os
import math
from .common import SUPPORTED_GROUPS, OpcodeGroupInfo

class ALUGenerator:
    """
    ALUGenerator is responsible for generating SystemVerilog files for an ALU based on a given configuration.
    Configuration includes the width of the ALU, user-defined opcodes, and input constraints and comes from
    an instance of ALUConfig class from the `alu_config` module.
    """
    def __init__(self, config: common, output_dir: str = "src"):
        """
        Initialize the ALUGenerator with a configuration and output directory.
        """
        self.config = config
        self.output_dir = output_dir
        # === Jinja2 Rendering === #
        self.env = Environment(
            loader=FileSystemLoader("templates"),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        # add enumerate() as a filter:
        self.env.filters['enumerate'] = enumerate

        self.module_name = "templatized_alu"
        self.group_map = {
            group_info.group.value: [op.name for op in group_info.opcodes]
            for group_info in SUPPORTED_GROUPS
        }

    def generate(self):
        """
        Generate the ALU SystemVerilog files based on the configuration.
        """
        # === Set Configuration Variables === #
        width = self.config.width
        user_ops = self.config.user_opcodes
        # === Output File Directory === #
        os.makedirs(self.output_dir, exist_ok=True)

        # === Filter active groups === #
        # Determine which groups have at least one selected operation and appends it to active_groups
        # active_groups is then flattened to a list of operations
        active_groups = {}
        for group, members in self.group_map.items():
            # Build a list of operations from this group that the user selected
            selected_ops = []
            for op in members:
                if op in user_ops:
                    selected_ops.append(op)
            if selected_ops:
                active_groups[group] = selected_ops

        if not any(active_groups.values()):
            raise ValueError("No operations selected.")

        group_list = list(active_groups.keys())

        # === Flatten Operations Dynamically === #
        # Iterate in the defined order of group_map to support any number of categories
        flattened_ops = []
        for group in self.group_map:
            # Extend by any selected operations in this group, or skip if none
            flattened_ops.extend(active_groups.get(group, []))

        # Minimum 1 bit, else ceil(log2(count))
        op_width = max(1, math.ceil(math.log2(len(flattened_ops))))

        # === Assign Default Opcodes === #
        default_opcodes = {}
        for i, op in enumerate(flattened_ops):
            code = format(i, f'0{op_width}b')
            default_opcodes[op] = code
        
        # Determine the number of bits needed to select a group
        sel_width = max(1, math.ceil(math.log2(len(group_list))))

        # === Generate group-specific ALUs === #
        for group in active_groups:
            template = self.env.get_template(f"{group}_group_template.sv.j2")
            rendered = template.render(
                module_name=f"alu_{group}",
                width=width,
                op_width=op_width,
                ops=active_groups[group],
                op_code={op: default_opcodes[op] for op in active_groups[group]},
            )
            self._write_file(f"alu_{group}.sv", rendered)

        # === Control Module === #
        control_template = self.env.get_template("control_module_template.sv.j2")
        control_rendered = control_template.render(
            module_name=self.module_name,
            op_width=op_width,
            sel_width=sel_width,
            groups=active_groups,
            group_list=group_list,
            op_code=default_opcodes
        )
        self._write_file(f"{self.module_name}_control.sv", control_rendered)

        # === Top-Level ALU === #
        top_template = self.env.get_template("top_level_alu_template_v1.sv.j2")
        top_rendered = top_template.render(
            module_name=self.module_name,
            width=width,
            ops=flattened_ops,
            op_width=op_width,
            groups=active_groups,
            group_list=group_list,
            active_group_count=len(active_groups),
            sel_width=sel_width
        )
        self._write_file(f"{self.module_name}.sv", top_rendered)

        # === Mux === #
        mux_template = self.env.get_template("Mux_template.sv.j2")
        mux_rendered = mux_template.render(
            group_list=group_list,
            num_inputs=len(group_list),
            width=width
        )
        self._write_file("mux_generic.sv", mux_rendered)

    def _write_file(self, filename: str, content: str):
        path = os.path.join(self.output_dir, filename)
        with open(path, "w") as f:
            f.write(content)
        print(f"✅ Generated {path}")