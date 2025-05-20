// alu_32bit_le.sv
module alu_32bit_le (
    input  logic [31:0] A,
    input  logic [31:0] B,
    input  logic [2:0] opcode,
    input logic en,
    output logic [31:0] result
);

    // Define local parameters for opcodes based on enabled operations 
    // avoid single line if statements here. Use for loops. 
    // using for loop to define local parameters for all operations
    localparam [2:0] OPCODE_LE = 3'b001;

    logic [31:0] _a = A;
    logic [31:0] _b = B;
    logic [31:0] result_internal;


    logic le_result = ($signed(_a) <= $signed(_b));

    always_comb begin
        case (opcode)
            OPCODE_LE: result_internal = 32'(le_result);
            default: result_internal = 0;
        endcase
    end

    assign result = result_internal;

endmodule