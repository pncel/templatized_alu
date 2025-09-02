// Core logic:
module alu_shift (
    input logic [31:0] A,
    input logic [31:0] B,
    input logic [3:0] opcode,
    input logic en,
    output logic [31:0] result
);

    logic [4:0] shamt; // Shift amount
    assign shamt = B[4:0]; // Extracting the lower bits for shift amount

    // Localparam opcodes
    localparam [3:0] OPCODE_LSL = 4'b0101;
    localparam [3:0] OPCODE_ASR = 4'b0110;
    localparam [3:0] OPCODE_ROL = 4'b0111;
    localparam [3:0] OPCODE_ROR = 4'b1000;

    logic [31:0] stage0;

    logic [31:0] stage1;
    logic [31:0] stage2;
    logic [31:0] stage3;
    logic [31:0] stage4;
    logic [31:0] stage5;

    // Fill bit & control signal definition
    logic fill;
    logic shift_left;
    logic shift_right;
    logic rotate_right;
    logic rotate_left;

    always_comb begin
        stage0 = A; // Default stage0 value
        stage1 = 32'b0; // Default stage value;
        stage2 = 32'b0; // Default stage value;
        stage3 = 32'b0; // Default stage value;
        stage4 = 32'b0; // Default stage value;
        stage5 = 32'b0; // Default stage value;
        shift_left = 1'b0; // Default shift direction
        shift_right = 1'b0; // Default shift direction
        rotate_right = 1'b0; // Default rotation direction
        rotate_left = 1'b0; // Default rotation direction
        fill = 1'b0; // Default fill bit
        if (en) begin
            case (opcode) // asr, ror, rol, lsr
 
                OPCODE_LSL: begin
                    fill = 1'b0; // Fill bit for logical shift
                    shift_left = 1'b1; // Logical shift left
                end
                OPCODE_ASR: begin
                    fill = A[31]; // Fill bit for arithmetic shift
                    shift_right = 1'b1; // Logical shift right
                end
                OPCODE_ROR: begin
                    rotate_right = 1'b1; // Rotate right
                end
                OPCODE_ROL: begin
                    rotate_left = 1'b1; // Rotate left
                end
                default: result = 32'b0;
            endcase

            // Stage N
            stage0 = A; // Initialize stage0 with input
            if (shamt[0]) begin
                if (shift_left) begin
                    stage1 = {stage0[30:0],  {1{fill}}};
                end else
                if (shift_right) begin
                    stage1 = {{1{fill}}, stage0[31:1]};                
                end
                if (rotate_left) begin
                    stage1 = {stage0[30:0], stage0[31:31]};
                end else
                if (rotate_right) begin
                    stage1 = {stage0[0:0], stage0[31:1]};
                end
            end else begin
                stage1 = stage0;
            end
            if (shamt[1]) begin
                if (shift_left) begin
                    stage2 = {stage1[29:0],  {2{fill}}};
                end else
                if (shift_right) begin
                    stage2 = {{2{fill}}, stage1[31:2]};                
                end
                if (rotate_left) begin
                    stage2 = {stage1[29:0], stage1[31:30]};
                end else
                if (rotate_right) begin
                    stage2 = {stage1[1:0], stage1[31:2]};
                end
            end else begin
                stage2 = stage1;
            end
            if (shamt[2]) begin
                if (shift_left) begin
                    stage3 = {stage2[27:0],  {4{fill}}};
                end else
                if (shift_right) begin
                    stage3 = {{4{fill}}, stage2[31:4]};                
                end
                if (rotate_left) begin
                    stage3 = {stage2[27:0], stage2[31:28]};
                end else
                if (rotate_right) begin
                    stage3 = {stage2[3:0], stage2[31:4]};
                end
            end else begin
                stage3 = stage2;
            end
            if (shamt[3]) begin
                if (shift_left) begin
                    stage4 = {stage3[23:0],  {8{fill}}};
                end else
                if (shift_right) begin
                    stage4 = {{8{fill}}, stage3[31:8]};                
                end
                if (rotate_left) begin
                    stage4 = {stage3[23:0], stage3[31:24]};
                end else
                if (rotate_right) begin
                    stage4 = {stage3[7:0], stage3[31:8]};
                end
            end else begin
                stage4 = stage3;
            end
            if (shamt[4]) begin
                if (shift_left) begin
                    stage5 = {stage4[15:0],  {16{fill}}};
                end else
                if (shift_right) begin
                    stage5 = {{16{fill}}, stage4[31:16]};                
                end
                if (rotate_left) begin
                    stage5 = {stage4[15:0], stage4[31:16]};
                end else
                if (rotate_right) begin
                    stage5 = {stage4[15:0], stage4[31:16]};
                end
            end else begin
                stage5 = stage4;
            end

        end

        result = stage5;

    end

endmodule
