// alu_16bit_add_sub.sv
module alu_16bit_add_sub (
    input  logic [15:0] A,
    input  logic [15:0] B,
    input  logic [2:0] opcode,
    input logic en,
    output logic [15:0] result
);

    // Define local parameters for opcodes based on enabled operations 
    // avoid single line if statements here. Use for loops. 
    // using for loop to define local parameters for all operations
    localparam [2:0] OPCODE_ADD = 3'b000;
    localparam [2:0] OPCODE_SUB = 3'b001;

    logic [15:0] _a = A;
    logic [15:0] _b = B;
    logic [15:0] result_internal;

    logic [15:0] add_sub_result;
    logic carry_in = 1'b0;
    logic is_sub = (opcode == OPCODE_SUB);
    wire [15:0] _b_mod = is_sub ? ~_b : _b;
    carry_in = is_sub ? 1'b1 : 1'b0;
    add_sub_result = _a + _b_mod + carry_in;


    always_comb begin
        case (opcode)
            OPCODE_ADD: result_internal = add_sub_result;
            OPCODE_SUB: result_internal = add_sub_result;
            default: result_internal = 0;
        endcase
    end

    assign result = result_internal;

endmodule