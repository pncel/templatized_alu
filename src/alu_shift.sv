// alu_32bit_shift_sll.sv
module alu_32bit_shift_sll (
    input  logic [31:0] A,
    input  logic [31:0] B, // B used for shift amount
    input  logic [2:0] opcode,
    output logic [31:0] result
);

    // Localparam opcodes
    localparam [2:0] OPCODE_SLL = 101;

    always_comb begin
        case (opcode)
            OPCODE_SLL:        result = A << B;
            default:           result = 0;
        endcase
    end

endmodule