// alu_16bit_shift_sll_sar_rotationleft_rotationright.sv
module alu_shift (
    input  logic [15:0] A,
    input  logic [15:0] B, // B used for shift amount
    input  logic [3:0] opcode,
    input logic en,
    output logic [15:0] result
);

    // Localparam opcodes
    localparam [3:0] OPCODE_SLL = 4'b0110;
    localparam [3:0] OPCODE_SAR = 4'b0111;
    localparam [3:0] OPCODE_ROTATIONLEFT = 4'b1000;
    localparam [3:0] OPCODE_ROTATIONRIGHT = 4'b1001;

    always_comb begin
        if (en) begin
            case (opcode)
                OPCODE_SLL:        result = A << B;
                OPCODE_SAR:        result = $signed(A) >>> B;
                OPCODE_ROTATIONLEFT:   result = (A << B) | (A >> (16 - B));
                OPCODE_ROTATIONRIGHT:  result = (A >> B) | (A << (16 - B));
                default:           result = 0;
            endcase
        end
    end

endmodule