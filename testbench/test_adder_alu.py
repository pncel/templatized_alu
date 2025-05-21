import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_basic_operations(dut):
    for _ in range(10):
        a = random.randint(0, 15)
        b = random.randint(0, 15)

        # Test ADD
        dut.a <= a
        dut.b <= b
        dut.opcode <= 0b000
        await Timer(1, units='ns')
        assert dut.result.value == a + b, f"ADD failed: {a}+{b} != {int(dut.result.value)}"

        # Test SUB
        dut.opcode <= 0b001
        await Timer(1, units='ns')
        assert dut.result.value == a - b, f"SUB failed: {a}-{b} != {int(dut.result.value)}"

        # Test GT
        dut.opcode <= 0b010
        await Timer(1, units='ns')
        expected = 1 if a > b else 0
        assert dut.result.value == expected, f"GT failed: {a}>{b} != {int(dut.result.value)}"

        # Test LT
        dut.opcode <= 0b011
        await Timer(1, units='ns')
        expected = 1 if a < b else 0
        assert dut.result.value == expected, f"LT failed: {a}<{b} != {int(dut.result.value)}"
