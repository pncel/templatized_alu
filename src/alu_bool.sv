// alu_32bit_xor.sv
module alu_bool (
    input  logic [31:0] A,
    input  logic [31:0] B,
    input  logic [3:0] opcode,
    input logic en,
    output logic [31:0] result
);

    // Localparam opcodes
    localparam [3:0] OPCODE_XOR = 4'b0100;

    // Result logic
    always_comb begin
        result = 32'b0; // Default result
        if (en) begin
            case (opcode)
                OPCODE_XOR:       result = A ^ B;
                default:          result = 32'b0;
            endcase
        end
    end

endmodule