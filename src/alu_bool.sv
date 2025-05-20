// alu_32bit_xor.sv
// module alu_32bit_xor (
module alu_bool (
    input  logic [31:0] A,
    input  logic [31:0] B,
    input  logic [2:0] opcode,
    input logic en,
    output logic [31:0] result
);

    // Localparam opcodes
    localparam [2:0] OPCODE_XOR = 3'b000;

    // Result logic
    always_comb begin
        result = '0;

        if (opcode == OPCODE_XOR)
            result = A ^ B;
    end

endmodule