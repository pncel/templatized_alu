// alu_32bit_xor_eq_ne_and.sv
module alu_bool (
    input  logic [31:0] A,
    input  logic [31:0] B,
    input  logic [3:0] opcode,
    input logic en,
    output logic [31:0] result
);

    // Localparam opcodes
    localparam [3:0] OPCODE_XOR = 4'b0100;
    localparam [3:0] OPCODE_EQ = 4'b0101;
    localparam [3:0] OPCODE_NE = 4'b0110;
    localparam [3:0] OPCODE_AND = 4'b0111;

    // Result logic
    always_comb begin
        result = 32'b0; // Default result
        if (en) begin
            case (opcode)
                OPCODE_EQ:        result = (A == B);
                OPCODE_XOR:       result = A ^ B;
                OPCODE_NE:        result = (A != B);
                OPCODE_AND:       result = A & B;
                default:          result = 32'b0;
            endcase
        end
    end

endmodule