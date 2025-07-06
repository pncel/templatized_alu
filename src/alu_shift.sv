// alu_32bit_shift_sll_slr_rotationleft.sv
module alu_shift (
    input  logic [31:0] A,
    input  logic [31:0] B, // B used for shift amount
    input  logic [3:0] opcode,
    input logic en,
    output logic [31:0] result
);

    // Localparam opcodes
    localparam [3:0] OPCODE_SLL = 4'b1000;
    localparam [3:0] OPCODE_SLR = 4'b1001;
    localparam [3:0] OPCODE_ROTATIONLEFT = 4'b1010;

    always_comb begin
        result = 32'b0; // Default result
        if (en) begin
            case (opcode)
                OPCODE_SLL:        result = A << B;
                OPCODE_ROTATIONLEFT:   result = (A << B) | (A >> (32 - B));
                default:           result = 0;
            endcase
        end
    end

endmodule