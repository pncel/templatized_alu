// alu_16bit_shift_sll_sar_rotationleft_rotationright.sv
module alu_16bit_shift_sll_sar_rotationleft_rotationright (
    input  logic [15:0] A,
    input  logic [15:0] B, // B used for shift amount
    input  logic [3:0] opcode,
    output logic [15:0] result
);

    // Localparam opcodes
    localparam [3:0] OPCODE_SLL = 0101;
    localparam [3:0] OPCODE_SAR = 0110;
    localparam [3:0] OPCODE_ROT_LEFT = 0111;
    localparam [3:0] OPCODE_ROT_RIGHT = 1000;

    always_comb begin
        case (opcode)
            OPCODE_SLL:        result = A << B;
            OPCODE_SAR:        result = $signed(A) >>> B;
            OPCODE_ROT_LEFT:   result = (A << B) | (A >> (16 - B));
            OPCODE_ROT_RIGHT:  result = (A >> B) | (A << (16 - B));
            default:           result = 0;
        endcase
    end

endmodule