// alu_16bit_nor.sv
module alu_16bit_nor (
    input  logic [15:0] A,
    input  logic [15:0] B,
    input  logic [2:0] opcode,
    input logic en,
    output logic [15:0] result
);

    // Localparam opcodes
    localparam [2:0] OPCODE_NOR = 3'b010;

    // Result logic
    always_comb begin
        result = '0;

        if (opcode == OPCODE_NOR)
            result = ~(A | B);
    end

endmodule