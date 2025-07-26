
// alu_32bit_add_sub_lt_gt.sv
module alu_add (
    input  logic [31:0] A,
    input  logic [31:0] B,
    input  logic [3:0] opcode,
    input  logic en,
    output logic [31:0] result
);

    // Localparam opcodes
    localparam [3:0] OPCODE_ADD = 4'b0000;
    localparam [3:0] OPCODE_SUB = 4'b0001;
    localparam [3:0] OPCODE_LT = 4'b0010;
    localparam [3:0] OPCODE_GT = 4'b0011;

    // Internal computation signals
    logic [32:0] extended_sub;
    logic sign_flag, overflow_flag, zero_flag;

    // Compute flags for comparison operations
    always_comb begin
        extended_sub = {1'b0, A} - {1'b0, B};
        sign_flag = extended_sub[32];
        overflow_flag = (A[31] != B[31]) && (extended_sub[31] != A[31]);
        zero_flag = (extended_sub[31:0] == 0);
    end

    // Result logic
    always_comb begin
        result = 32'b0; // Default result
        if (en) begin
            case (opcode)
                OPCODE_ADD: result = A + B;
                OPCODE_SUB: result = A - B;
                OPCODE_LT:  result = (sign_flag ^ overflow_flag) ? { 32{1'b1}} : { 32{1'b0}};
                OPCODE_GT:  result = !(sign_flag ^ overflow_flag || zero_flag) ? { 32{1'b1}} : { 32{1'b0}};
                default:    result = 32'b0;
            endcase
        end
    end

endmodule