#!/bin/bash
# Exit on any error
set -e

echo "🔍 Running Verilator lint..."
verilator --lint-only -sv src/*.sv

echo "✅ Verilator lint passed!"

echo "🏗️  Running Yosys synthesis..."
yosys -p "
  read_verilog -sv src/*.sv
  hierarchy -check -top templatized_alu
  synth -top templatized_alu
"

echo "✅ Yosys synthesis passed!"
