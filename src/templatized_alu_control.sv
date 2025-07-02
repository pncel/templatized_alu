module templatized_alu_control (
    input  logic [3:0] op_code,
    output logic [2:0] en
);

    // define every opcode as a named constant
    localparam logic [3:0] OPCODE_ADD = 4'b0000;
    localparam logic [3:0] OPCODE_SUB = 4'b0001;
    localparam logic [3:0] OPCODE_LT = 4'b0010;
    localparam logic [3:0] OPCODE_GT = 4'b0011;
    localparam logic [3:0] OPCODE_XOR = 4'b0100;
    localparam logic [3:0] OPCODE_SLL = 4'b0101;
    localparam logic [3:0] OPCODE_SAR = 4'b0110;
    localparam logic [3:0] OPCODE_ROTATIONLEFT = 4'b0111;
    localparam logic [3:0] OPCODE_ROTATIONRIGHT = 4'b1000;

    always_comb begin
        // default: all groups disabled
        en = 3'b0;
        unique case (op_code)
            OPCODE_ADD: en = {1'b1, 1'b0, 1'b0};  // add
            OPCODE_SUB: en = {1'b1, 1'b0, 1'b0};  // sub
            OPCODE_LT: en = {1'b1, 1'b0, 1'b0};  // lt
            OPCODE_GT: en = {1'b1, 1'b0, 1'b0};  // gt
            OPCODE_XOR: en = {1'b0, 1'b1, 1'b0};  // xor
            OPCODE_SLL: en = {1'b0, 1'b0, 1'b1};  // sll
            OPCODE_SAR: en = {1'b0, 1'b0, 1'b1};  // sar
            OPCODE_ROTATIONLEFT: en = {1'b0, 1'b0, 1'b1};  // rotationleft
            OPCODE_ROTATIONRIGHT: en = {1'b0, 1'b0, 1'b1};  // rotationright
            default: en = 3'b0;
        endcase
    end

endmodule