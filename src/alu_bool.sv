// alu_32bit_xor_ne.sv
module alu_32bit_xor_ne (
    input  logic [31:0] A,
    input  logic [31:0] B,
    input  logic [2:0] opcode,
    output logic [31:0] result
);

    // Localparam opcodes
    localparam [2:0] OPCODE_XOR  = 011;
    localparam [2:0] OPCODE_NE   = 100;

    // Result logic
    always_comb begin
        result = '0;

        if (opcode == OPCODE_XOR)
            result = A ^ B;
        if (opcode == OPCODE_NE)
            result = (A != B);
    end

endmodule