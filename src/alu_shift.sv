// alu_32bit_shift_sll_sar_rotationleft_rotationright.sv
// module alu_32bit_shift_sll_sar_rotationleft_rotationright (
module alu_shift (
    input  logic [31:0] A,
    input  logic [31:0] B, // B used for shift amount
    input  logic [2:0] opcode,
    input logic en,
    output logic [31:0] result
);

    // Localparam opcodes
    localparam [2:0] OPCODE_SLL = 3'b001;
    localparam [2:0] OPCODE_SAR = 3'b010;
    localparam [2:0] OPCODE_ROTATIONLEFT = 3'b011;
    localparam [2:0] OPCODE_ROTATIONRIGHT = 3'b100;

    always_comb begin
        case (opcode)
            OPCODE_SLL:        result = A << B;
            OPCODE_SAR:        result = $signed(A) >>> B;
            OPCODE_ROT_LEFT:   result = (A << B) | (A >> (32 - B));
            OPCODE_ROT_RIGHT:  result = (A >> B) | (A << (32 - B));
            default:           result = 0;
        endcase
    end

endmodule