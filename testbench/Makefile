# testbench/Makefile

TOPLEVEL_LANG := verilog
VERILOG_SOURCES := $(wildcard ../src/*.sv)
TOPLEVEL := templatized_alu
MODULE := test_alu

SIM := icarus
WAVES := 0    # disable VCD generation

include $(shell cocotb-config --makefiles | sed 's/ /\\ /g')/Makefile.sim