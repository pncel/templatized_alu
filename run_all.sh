#!/bin/bash

set -e  # Exit on any error

echo "🧼 Step 1: Linting & synthesis checks..."
./check_design.sh

echo "🚀 Step 2: Running cocotb testbench with Icarus..."
cd testbench
make

echo "📼 Step 3: Simulation completed. VCD waveform generated at: $(pwd)/dump.vcd"
