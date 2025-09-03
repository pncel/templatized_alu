from jinja2 import Environment, FileSystemLoader
import os
import math
<<<<<<< HEAD:alugen/lib/alu_generator.py
from .common import SUPPORTED_GROUPS, OpcodeGroupInfo
from dora.core.arch.netlist.module import ArchModule
=======
from common import OPERATIONS_US

from dora.core.arch.netlist.module import ArchModule

>>>>>>> 22bfbb5 (dora RTL generation draft):lib/alu_generator.py

class ALUGenerator:
    """
    ALUGenerator is responsible for generating SystemVerilog files for an ALU based on a given configuration.
    Configuration includes the width of the ALU, user-defined opcodes, and input constraints and comes from
    an instance of ALUConfig class from the `alu_config` module.
    """
<<<<<<< HEAD:alugen/lib/alu_generator.py

    __slots__ = ("_config", "_output_dir", "_env", "_module_name", "_group_map")
    
    def __init__(self, config: ArchModule, output_dir: str = "src"):
=======
    def __init__(self, config: "ArchModule", output_dir: str = "src"):
>>>>>>> 22bfbb5 (dora RTL generation draft):lib/alu_generator.py
        """
        Initialize the ALUGenerator with a configuration and output directory.
        """
        self._config = config
        self._output_dir = output_dir
        # === Jinja2 Rendering === #
        self._env = Environment(
            loader=FileSystemLoader("templates"),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        # add enumerate() as a filter:
        self._env.filters['enumerate'] = enumerate

<<<<<<< HEAD:alugen/lib/alu_generator.py
        self._module_name = "templatized_alu"
        self._group_map = {
            group_info.group.value: [op.name for op in group_info.opcodes]
            for group_info in SUPPORTED_GROUPS
        }
=======
        self.module_name = "templatized_alu"
        # self.group_map = {
        #     group_info.group.value: [op.name for op in group_info.opcodes]
        #     for group_info in SUPPORTED_GROUPS
        # }

        self.group_map = {}
        for group, ops in OPERATIONS_US.items():
            op_names = []
            for op in ops:
                op_names.append(op.op_type.name)
            self.group_map[group] = op_names
>>>>>>> 22bfbb5 (dora RTL generation draft):lib/alu_generator.py

    def generate(self):
        """
        Generate the ALU SystemVerilog files based on the configuration.
        """
<<<<<<< HEAD:alugen/lib/alu_generator.py
        # === Set Configuration Variables === #

        # Width of the ALU ports must be derived from the module ports
        width = self._config.width

        # Operations must be derived from the module operations
        user_ops = self._config.operations
        # input_A = self._config.input_a_name
        # input_B = self._config.input_b_name
        # input_C = self._config.input_c_name
        # result = self._config.result_name
=======
        # === Collect ports_info per operation === #
        # NOTE: In the future, if groups require distinct bit-widths/ports,
        #       create ports_info_add / ports_info_bool / ports_info_shift here.
        ports_info = {}
        user_ops = self.config.operations
        first_op = True

        for op_name, op_type in user_ops.items():
            ports = op_type.ports

            result_port = ports[-1]  # Last port is always the result
            input_ports = ports[:-1]  # All but last are inputs

            # === Handle inputs ===
            for i, port in enumerate(input_ports):
                key = make_internal_key(i)
                port_info = {
                    "name": port.name,
                    "bit_width": port.datatype.bit_width,
                    "datatype": port.datatype
                }

                if first_op:
                    ports_info[key] = port_info
                else:
                    expected = ports_info[key]
                    if (expected["bit_width"] != port.datatype.bit_width or
                        expected["datatype"] != port.datatype):
                        raise TypeError(
                            f"Port mismatch for {key} in {op_name}: "
                            f"expected {expected}, got {port_info}"
                        )

            # === Handle result ===
            result_info = {
                "name": result_port.name,
                "bit_width": result_port.datatype.bit_width,
                "datatype": result_port.datatype
            }

            if first_op:
                ports_info["dora_result"] = result_info
                first_op = False
            else:
                expected = ports_info["dora_result"]
                if (expected["bit_width"] != result_port.datatype.bit_width or
                    expected["datatype"] != result_port.datatype):
                    raise TypeError(
                        f"Result mismatch in {op_name}: "
                        f"expected {expected}, got {result_info}"
                    )


        input_A = ports_info_by_op.get("input_A")
        # input_B = self.config.input_b_name
        # input_C = self.config.input_c_name
        # result = self.config.result_name
>>>>>>> 22bfbb5 (dora RTL generation draft):lib/alu_generator.py
        # === Output File Directory === #
        os.makedirs(self._output_dir, exist_ok=True)

        # === Filter active groups === #
        # Determine which groups have at least one selected operation and appends it to active_groups
        # active_groups is then flattened to a list of operations
        active_groups = {}
<<<<<<< HEAD:alugen/lib/alu_generator.py
        for group, members in self._group_map.items():
            # Build a list of operations from this group that the user selected
            selected_ops = []
            for op in members:
                if op in user_ops:
                    selected_ops.append(op)
=======
        for group, members in self.group_map.items():
            # Keep only the operations that the user explicitly selected
            selected_ops = [op for op in members if op in user_ops]
>>>>>>> 22bfbb5 (dora RTL generation draft):lib/alu_generator.py
            if selected_ops:
                active_groups[group] = selected_ops

        if not active_groups:
            raise ValueError("No operations selected.")

        group_list = list(active_groups.keys())

        # === Flatten Operations Dynamically === #
        # Iterate in the defined order of group_map to support any number of categories
        flattened_ops = []
        for group in self._group_map:
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
            template = self._env.get_template(f"{group}_group_template.sv.j2")
            rendered = template.render(
<<<<<<< HEAD:alugen/lib/alu_generator.py
                module_name=f"alu_{group}",
                width=width,
                op_width=op_width,
                ops=active_groups[group],
                op_code={op: default_opcodes[op] for op in active_groups[group]},
                # input_A=input_A
=======
                module_name = f"alu_{group}",
                width       = width,
                log2_width  = math.ceil(math.log2(width)),
                op_width    = op_width,
                ops         = active_groups[group],
                op_code     = {op: default_opcodes[op] for op in active_groups[group]},
                input_A=input_a_port
>>>>>>> 22bfbb5 (dora RTL generation draft):lib/alu_generator.py
                # input_B=input_B,
                # input_C=input_C,
                # result=result,
                # signed=is_signed,
                # unsigned=is_unsigned
            )
            self._write_file(f"alu_{group}.sv", rendered)

        # === Control Module === #
        control_template = self._env.get_template("control_module_template.sv.j2")
        control_rendered = control_template.render(
            module_name=self._module_name,
            op_width=op_width,
            sel_width=sel_width,
            groups=active_groups,
            group_list=group_list,
            op_code=default_opcodes
        )
        self._write_file(f"{self._module_name}_control.sv", control_rendered)

        # === Top-Level ALU === #
        top_template = self._env.get_template("top_level_alu_template_v1.sv.j2")
        top_rendered = top_template.render(
            module_name=self._module_name,
            width=width,
            ops=flattened_ops,
            op_width=op_width,
            groups=active_groups,
            group_list=group_list,
            active_group_count=len(active_groups),
            sel_width=sel_width
        )
        self._write_file(f"{self._module_name}.sv", top_rendered)

        # === Mux === #
        mux_template = self._env.get_template("Mux_template.sv.j2")
        mux_rendered = mux_template.render(
            group_list=group_list,
            num_inputs=len(group_list),
            width=width
        )
        self._write_file("mux_generic.sv", mux_rendered)

    def _write_file(self, filename: str, content: str):
        path = os.path.join(self._output_dir, filename)
        with open(path, "w") as f:
            f.write(content)
        print(f"✅ Generated {path}")

def make_internal_key(idx: int) -> str:
    if idx == 0:
        return "dora_input_a"
    elif idx == 1:
        return "dora_input_b"
    elif idx == 2:
        return "dora_input_c"