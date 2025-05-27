// alu_16bit_le_nor.sv
module alu_bool (
    input  logic [15:0] A,
    input  logic [15:0] B,
    input  logic [3:0] opcode,
    input logic en,
    output logic [15:0] result
);

    // Localparam opcodes
    localparam [3:0] OPCODE_LE = 4'b0100;
    localparam [3:0] OPCODE_NOR = 4'b0101;

    // Result logic
    always_comb begin
        result = '0;
        if (en) begin
            case (opcode)
                OPCODE_LE:        result = (A == B); // changed from <= to ==
                OPCODE_NOR:       result = ~(A | B);
            endcase
            if (opcode == OPCODE_LE)
                result = (A == B); // changed from <= to ==
            if (opcode == OPCODE_NOR)
                result = ~(A | B);
        end
    end

endmodule