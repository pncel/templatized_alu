// alu_32bit_add_sub_lt.sv
module alu_32bit_add_sub_lt (
    input  logic [31:0] A,
    input  logic [31:0] B,
    input  logic [2:0] opcode,
    output logic [31:0] result
);

    // Define local parameters for opcodes based on enabled operations
    localparam [2:0] OPCODE_ADD = 000;
    localparam [2:0] OPCODE_SUB = 001;
    localparam [2:0] OPCODE_LT = 010;

    logic [31:0] _a = A;
    logic [31:0] _b = B;
    logic [31:0] result_internal;

    logic [31:0] add_sub_result;
    logic carry_in = 1'b0;
    logic is_sub = (opcode == OPCODE_SUB);
    wire [31:0] _b_mod = is_sub ? ~_b : _b;
    carry_in = is_sub ? 1'b1 : 1'b0;
    add_sub_result = _a + _b_mod + carry_in;

    logic lt_result = ($signed(_a) < $signed(_b));

    always_comb begin
        case (opcode)
            OPCODE_ADD: result_internal = add_sub_result;
            OPCODE_SUB: result_internal = add_sub_result;
            OPCODE_LT: result_internal = 32'(lt_result);
            default: result_internal = 0;
        endcase
    end

    assign result = result_internal;

endmodule