// alu_16bit_le_xor.sv
module alu_16bit_le_xor (
    input  logic [15:0] A,
    input  logic [15:0] B,
    input  logic [3:0] opcode,
    output logic [15:0] result
);

    // Localparam opcodes
    localparam [3:0] OPCODE_LE   = 0100;
    localparam [3:0] OPCODE_XOR  = 0101;

    // Result logic
    always_comb begin
        result = '0;

        if (opcode == OPCODE_LE)
            result = (A <= B);
        if (opcode == OPCODE_XOR)
            result = A ^ B;
    end

endmodule