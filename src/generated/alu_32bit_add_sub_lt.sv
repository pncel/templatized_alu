// alu_32bit.sv
module alu_32bit (
    input  logic [31:0] A,
    input  logic [31:0] B,
    input  logic [2:0] opcode,
    output logic [31:0] result
);

    logic [31:0] _a, _b;
    logic [31:0] add_sub_result;
    logic carry_in;

    // Shared input path
    _a = A;
    _b = B;
    carry_in = 1'b0;

    // Adjust B and carry_in if subtraction is enabled
    logic is_sub = (opcode == 3'b001);  // assume sub is opcode 001
    logic [31:0] _b_mod = is_sub ? ~B : B;
    logic _cin = is_sub ? 1'b1 : 1'b0;
    {_cout, add_sub_result} = _a + _b_mod + _cin;

    logic cmp_result;
    logic lt_result = (A < B);

    // Output mux
    always_comb begin
        result = '0;
        case (opcode)
            3'b000: result = add_sub_result;
            3'b001: result = add_sub_result;
            3'b011: result = 32'(lt_result);
            default: result = '0;
        endcase
    end

endmodule