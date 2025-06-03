#!/bin/bash

set -e  # Exit on any error

echo "🧼 Step 1: Linting & synthesis checks..."
./scripts/check_design.sh

echo "🔧 Step 2: Generating RTL..."
python gen/generate_alu.py constraints/constraints.json

echo "🚀 Step 3: Running cocotb tests..."
cd testbench
make

echo "✅ Simulation completed."
