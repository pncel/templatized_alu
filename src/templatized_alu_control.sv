    input  logic [3:0] op_code,
    output logic [2:0] en
);

    // define every opcode as a named constant
    localparam logic [3:0] OPCODE_ADD = 4'b0000;
    localparam logic [3:0] OPCODE_SUB = 4'b0001;
    localparam logic [3:0] OPCODE_LT = 4'b0010;
    localparam logic [3:0] OPCODE_GT = 4'b0011;
    localparam logic [3:0] OPCODE_XOR = 4'b0100;
    localparam logic [3:0] OPCODE_LSL = 4'b0101;
    localparam logic [3:0] OPCODE_ASR = 4'b0110;
    localparam logic [3:0] OPCODE_ROL = 4'b0111;
    localparam logic [3:0] OPCODE_ROR = 4'b1000;

    always_comb begin
        // default: all groups disabled
        en = 3'b0;
        unique case (op_code)
            OPCODE_ADD: en = {1'b0, 1'b0, 1'b1};  // add
            OPCODE_SUB: en = {1'b0, 1'b0, 1'b1};  // sub
            OPCODE_LT: en = {1'b0, 1'b0, 1'b1};  // lt
            OPCODE_GT: en = {1'b0, 1'b0, 1'b1};  // gt
            OPCODE_XOR: en = {1'b0, 1'b1, 1'b0};  // xor
            OPCODE_LSL: en = {1'b1, 1'b0, 1'b0};  // lsl
            OPCODE_ASR: en = {1'b1, 1'b0, 1'b0};  // asr
            OPCODE_ROL: en = {1'b1, 1'b0, 1'b0};  // rol
            OPCODE_ROR: en = {1'b1, 1'b0, 1'b0};  // ror
            default: en = 3'b0;
        endcase
    end

endmodule