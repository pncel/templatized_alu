module templatized_alu_control (
    input  logic [2:0] op_code,
    output logic [1:0] en
);

    // define every opcode as a named constant
    localparam logic [2:0] OPCODE_XOR = 3'b000;
    localparam logic [2:0] OPCODE_SLL = 3'b001;
    localparam logic [2:0] OPCODE_SAR = 3'b010;
    localparam logic [2:0] OPCODE_ROTATIONLEFT = 3'b011;
    localparam logic [2:0] OPCODE_ROTATIONRIGHT = 3'b100;

    always_comb begin
        // default: all groups disabled
        en = 2'b0;
        unique case (op_code)
            OPCODE_XOR: en = {1'b1, 1'b0};  // xor
            OPCODE_SLL: en = {1'b0, 1'b1};  // sll
            OPCODE_SAR: en = {1'b0, 1'b1};  // sar
            OPCODE_ROTATIONLEFT: en = {1'b0, 1'b1};  // rotationleft
            OPCODE_ROTATIONRIGHT: en = {1'b0, 1'b1};  // rotationright
            default: en = 2'b0;
        endcase
    end

endmodule