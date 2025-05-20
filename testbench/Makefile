TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(wildcard ../src/*.sv)
TOPLEVEL = templatized_alu
MODULE = test_adder_alu

SIM = icarus
WAVES = 1

include $(shell cocotb-config --makefiles)/Makefile.sim
