import cocotb
import json
import random
from cocotb.triggers import RisingEdge, Timer
from cocotb_coverage.coverage import coverage_db, CoverPoint

# 1. Load constraints from json file
with open("constraints.json", "r") as f:
    constraints = json.load(f)

WIDTH = constraints["width"]
SUPPORTED_OPCODES = constraints["supported_opcodes"]
INPUT_CONSTRAINTS = constraints["input_constraints"]
A_min, A_max = INPUT_CONSTRAINTS["A_range"]
B_min, B_max = INPUT_CONSTRAINTS["B_range"]

# 2. Define expected‐result functions for each opcode (dynamic)
# All possible user‐selected operations
OP_FUNCS = {}
for op in SUPPORTED_OPCODES:
    if op == "add":
        OP_FUNCS[op] = lambda a, b: a + b
    elif op == "sub":
        OP_FUNCS[op] = lambda a, b: a - b
    elif op == "lt":
        OP_FUNCS[op] = lambda a, b: 1 if a < b else 0
    elif op == "gt":
        OP_FUNCS[op] = lambda a, b: 1 if a > b else 0
    elif op == "le":
        OP_FUNCS[op] = lambda a, b: 1 if a <= b else 0
    elif op == "ge":
        OP_FUNCS[op] = lambda a, b: 1 if a >= b else 0
    elif op == "xor":
        OP_FUNCS[op] = lambda a, b: a ^ b
    elif op == "and":
        OP_FUNCS[op] = lambda a, b: a & b
    elif op == "or":
        OP_FUNCS[op] = lambda a, b: a | b
    elif op == "not":
        OP_FUNCS[op] = lambda a, b: ~a
    elif op == "nand":
        OP_FUNCS[op] = lambda a, b: ~(a & b)
    elif op == "nor":
        OP_FUNCS[op] = lambda a, b: ~(a | b)
    elif op == "xnor":
        OP_FUNCS[op] = lambda a, b: ~(a ^ b)
    elif op == "sll":
        OP_FUNCS[op] = lambda a, b: (a << b) & ((1 << WIDTH) - 1)
    elif op == "slr":
        OP_FUNCS[op] = lambda a, b: (a % (1 << WIDTH)) >> b
    elif op == "sar":
        OP_FUNCS[op] = lambda a, b: (a >> b) if a < (1 << (WIDTH-1)) else ((a | ~((1 << WIDTH)-1)) >> b)
    elif op == "rotationleft":
        OP_FUNCS[op] = lambda a, b: ((a << b) | (a >> (WIDTH - b))) & ((1 << WIDTH) - 1)
    elif op == "rotationright":
        OP_FUNCS[op] = lambda a, b: ((a >> b) | (a << (WIDTH - b))) & ((1 << WIDTH) - 1)
    else:
        raise NotImplementedError(f"Expected-result function not defined for opcode '{op}'")

# 3. Functional coverage definitions
@CoverPoint(
    "top.opcode",
    xf=lambda op: op,
    bins=SUPPORTED_OPCODES,
    at_least=1
)
def cover_opcode(op):
    "Record which opcodes have been exercised."
    pass

@CoverPoint(
    "top.a_value",
    xf=lambda a: "min" if a==A_min else ("max" if a==A_max else "mid"),
    bins=["min","mid","max"],
    at_least=1
)
def cover_a(a):
    "Record A in three zones: min, mid, max."
    pass

@CoverPoint(
    "top.b_value",
    xf=lambda b: "min" if b==B_min else ("max" if b==B_max else "mid"),
    bins=["min","mid","max"],
    at_least=1
)
def cover_b(b):
    "Record B in three zones: min, mid, max."
    pass

# 4. Main test: apply stimulus, collect coverage, and check correctness
@cocotb.test()
async def test_templatized_alu(dut):
    """Constrained random testing, coverage, and output verification."""
    if hasattr(dut, 'reset'):
        dut.reset.value = 1
        await RisingEdge(dut.clk)
        dut.reset.value = 0
        await RisingEdge(dut.clk)

    # Generate a sequence of random tests
    for cycle in range(5000):
        await RisingEdge(dut.clk)
        # Choose random inputs
        opcode = random.choice(SUPPORTED_OPCODES)
        a_val  = random.randint(A_min, A_max)
        b_val  = random.randint(B_min, B_max)

        # Drive DUT signals
        dut.opcode.value = SUPPORTED_OPCODES.index(opcode)
        dut.a.value      = a_val
        dut.b.value      = b_val
        # Wait for output to stabilize
        await Timer(10, units="ns")

        # 4.a) Functional coverage sampling
        cover_opcode(opcode)
        cover_a(a_val)
        cover_b(b_val)

        # 4.b) Correctness check: compare DUT output to expected value
        actual = int(dut.out.value)
        expected = OP_FUNCS[opcode](a_val, b_val)
        if actual != expected:
            dut._log.error(
                f"Mismatch: op={opcode}, A={a_val}, B={b_val}, "
                f"expect={expected}, got={actual}"
            )
            assert False, (
                f"ALU output incorrect for {opcode}: "
                f"A={a_val}, B={b_val}, exp={expected}, got={actual}"
            )

    # 5. Report coverage and fail if any bin is missing
    coverage_db.report_coverage(dut._log.info, bins=True)
    missing_ops = coverage_db.get_missing_bins("top.opcode")
    if missing_ops:
        dut._log.error(f"❌ Missing opcode coverage: {missing_ops}")
        assert False, "Test failed: some opcodes not exercised"
    dut._log.info("✅ All opcodes exercised and outputs verified!")