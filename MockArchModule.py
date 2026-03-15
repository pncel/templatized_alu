from dora.core.arch.netlist.net import ArchPort
from dora.utils.proxy import ReadonlySequenceProxy
from dora.core.common.types import ModuleType, PlaneType
from dora.core.arch.netlist.module import ArchModule


# helper to wrap datatypes into ArchPorts consistently
def make_ports(datatypes):
    """
    datatypes = [result, input0, input1, ...]
    """
    ports = []
    for i, dt in enumerate(datatypes[1:]):  # inputs
        ports.append(ArchPort(f"dora_input_{i}", dt))
    ports.append(ArchPort("dora_result", datatypes[0]))  # output last
    return ReadonlySequenceProxy(ports)


USER_OPS = {
    "ADD": ArchOpType(
        optype=OpType.ADD,
        name="ADD",
        num_inputs=2,
        datatypes=ReadonlySequenceProxy([INT32, INT32, INT32]),
        ports=make_ports([INT32, INT32, INT32]),
    ),
    "SUB": ArchOpType(
        optype=OpType.SUB,
        name="SUB",
        num_inputs=2,
        datatypes=ReadonlySequenceProxy([INT32, INT32, INT32]),
        ports=make_ports([INT32, INT32, INT32]),
    ),
    "AND": ArchOpType(
        optype=OpType.AND,
        name="AND",
        num_inputs=2,
        datatypes=ReadonlySequenceProxy([BOOL, INT32, INT32]),
        ports=make_ports([BOOL, INT32, INT32]),
    ),
    "OR": ArchOpType(
        optype=OpType.OR,
        name="OR",
        num_inputs=2,
        datatypes=ReadonlySequenceProxy([BOOL, INT32, INT32]),
        ports=make_ports([BOOL, INT32, INT32]),
    ),
    "LSL": ArchOpType(
        optype=OpType.LSL,
        name="LSL",
        num_inputs=2,
        datatypes=ReadonlySequenceProxy([INT32, INT32, INT32]),
        ports=make_ports([INT32, INT32, INT32]),
    ),
    "LSR": ArchOpType(
        optype=OpType.LSR,
        name="LSR",
        num_inputs=2,
        datatypes=ReadonlySequenceProxy([INT32, INT32, INT32]),
        ports=make_ports([INT32, INT32, INT32]),
    ),
}

mock_module = ArchModule(
    name="mock_alu",
    module_type=ModuleType.tile,
    committed_planes=PlaneType.logic,
    ports={},
    instances={},
    instantiations=[],
    nets=[],
    connections={},
    operations=USER_OPS,
)
