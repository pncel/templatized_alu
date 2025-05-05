// alu_16bit_add_sub_le.sv
module alu_16bit_add_sub_le (
    input  logic [15:0] A,
    input  logic [15:0] B,
    input  logic [3:0] opcode,
    output logic [15:0] result
);

    // Define local parameters for opcodes based on enabled operations
    localparam [3:0] OPCODE_ADD = 0000;
    localparam [3:0] OPCODE_SUB = 0001;
    localparam [3:0] OPCODE_LE = 0011;

    logic [15:0] _a = A;
    logic [15:0] _b = B;
    logic [15:0] result_internal;

    logic [15:0] add_sub_result;
    logic carry_in = 1'b0;
    logic is_sub = (opcode == OPCODE_SUB);
    wire [15:0] _b_mod = is_sub ? ~_b : _b;
    carry_in = is_sub ? 1'b1 : 1'b0;
    add_sub_result = _a + _b_mod + carry_in;

    logic le_result = ($signed(_a) <= $signed(_b));

    always_comb begin
        case (opcode)
            OPCODE_ADD: result_internal = add_sub_result;
            OPCODE_SUB: result_internal = add_sub_result;
            OPCODE_LE: result_internal = 16'(le_result);
            default: result_internal = 0;
        endcase
    end

    assign result = result_internal;

endmodule