from jinja2 import Environment, FileSystemLoader
import os
import math
from alugen.lib.common import OPERATIONS_US

from dora.core.arch.netlist.module import ArchModule


class ALUGenerator:
    """
    ALUGenerator is responsible for generating SystemVerilog files for an ALU based on a given configuration.
    Configuration includes the width of the ALU, user-defined opcodes, and input constraints and comes from
    an instance of ALUConfig class from the `alu_config` module.
    """

    def __init__(self, config: "ArchModule", output_dir: str = "src"):
        """
        Initialize the ALUGenerator with a configuration and output directory.
        """
        self.config = config
        self.output_dir = output_dir
        # === Jinja2 Rendering === #
        # Get the directory where this file is located and find templates relative to it
        current_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(current_dir, "..", "templates")
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        # add enumerate() as a filter:
        self.env.filters["enumerate"] = enumerate

        self.module_name = config.name

        self.group_map = OPERATIONS_US
        # for group, ops in OPERATIONS_US.items():
        #     op_names = []
        #     for op in ops:
        #         op_names.append(op.op_type.name)
        #     self.group_map[group] = op_names

    def generate(self):
        """
        Generate the ALU SystemVerilog files based on the configuration.
        """
        # === Collect ports_info per operation === #
        # NOTE: In the future, if groups require distinct bit-widths/ports,
        #       create ports_info_add / ports_info_bool / ports_info_shift here.
        ports_info = {}
        user_ops = self.config.operations
        first_op = True
        dora_width = None

        for op_name, op_type in user_ops.items():
            ports = op_type.ports

            result_port = ports[-1]  # Last port is always the result
            input_ports = ports[:-1]  # All but last are inputs

            # === Handle inputs ===
            for key, port in enumerate(input_ports):
                port_info = {
                    "name": port.name,
                    "bit_width": port.datatype.bit_width,
                    "datatype": port.datatype,
                }

                if first_op:
                    ports_info[key] = port_info
                else:
                    expected = ports_info[key]
                    if (
                        expected["bit_width"] != port.datatype.bit_width
                        or expected["datatype"] != port.datatype
                    ):
                        raise TypeError(
                            f"Port mismatch for {key} in {op_name}: "
                            f"expected {expected}, got {port_info}"
                        )

            # === Handle result ===
            result_info = {
                "name": result_port.name,
                "bit_width": result_port.datatype.bit_width,
                "datatype": result_port.datatype,
            }

            if first_op:
                ports_info["dora_result"] = result_info
                dora_width = result_port.datatype.bit_width
                first_op = False
            else:
                expected = ports_info["dora_result"]
                if (
                    expected["bit_width"] != result_port.datatype.bit_width
                    or expected["datatype"] != result_port.datatype
                ):
                    raise TypeError(
                        f"Result mismatch in {op_name}: "
                        f"expected {expected}, got {result_info}"
                    )

        # === Output File Directory === #
        os.makedirs(self.output_dir, exist_ok=True)

        # === Filter active groups === #
        # Determine which groups have at least one selected operation and appends it to active_groups
        # active_groups is then flattened to a list of operations
        active_groups = {}
        for group, members in self.group_map.items():
            # Keep only the operations that the user explicitly selected
            selected_ops = []
            for op in members:
                for user_op in user_ops.values():
                    if (
                        op.op_type == user_op.optype
                        and op.num_operands == user_op.num_inputs
                        and tuple(op.operand_types) == tuple(user_op.datatypes)
                    ):
                        selected_ops.append(op)
                        break
            if selected_ops:
                active_groups[group] = selected_ops

        if not active_groups:
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
            code = format(i, f"0{op_width}b")
            default_opcodes[op] = code

        # Determine the number of bits needed to select a group
        sel_width = max(1, math.ceil(math.log2(len(group_list))))

        # depeneding on what port.datatype is, generate specific ALUs.

        # === Generate group-specific ALUs === #

        # Print flattened_ops
        print(f"Flattened ops: {flattened_ops}")

        for group in active_groups:
            template = self.env.get_template(f"{group}_group_template.sv.j2")
            rendered = template.render(
                module_name=f"alu_{group}",
                width=dora_width,
                log2_width=math.ceil(math.log2(dora_width)),
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
            op_code=default_opcodes,
        )
        self._write_file(f"{self.module_name}_control.sv", control_rendered)

        # === Top-Level ALU === #
        top_template = self.env.get_template("top_level_alu_template_v1.sv.j2")

        top_rendered = top_template.render(
            module_name=self.module_name,
            width=dora_width,
            ops=flattened_ops,
            op_width=op_width,
            groups=active_groups,
            group_list=group_list,
            active_group_count=len(active_groups),
            sel_width=sel_width,
        )
        self._write_file(f"{self.module_name}.sv", top_rendered)

        # === Mux === #
        mux_template = self.env.get_template("Mux_template.sv.j2")
        mux_rendered = mux_template.render(
            group_list=group_list, num_inputs=len(group_list), width=dora_width
        )
        self._write_file("mux_generic.sv", mux_rendered)

    def _write_file(self, filename: str, content: str):
        path = os.path.join(self.output_dir, filename)
        with open(path, "w") as f:
            f.write(content)
        print(f"✅ Generated {path}")
