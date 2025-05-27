// alu_16bit_add_sub_gt_le.sv
module alu_add (
    input  logic [15:0] A,
    input  logic [15:0] B,
    input  logic [3:0] opcode,
    input  logic en,
    output logic [15:0] result
);

    // Opcode constants
    localparam [3:0] OPCODE_ADD = 4'b0000;
    localparam [3:0] OPCODE_SUB = 4'b0001;
    localparam [3:0] OPCODE_GT = 4'b0010;
    localparam [3:0] OPCODE_LE = 4'b0100;

    // Internal signals
    logic [15:0] result_internal;
    logic [15:0] _a, _b;

    logic [15:0] add_sub_result;
    
    logic [15:0] _b_mod;
    logic is_sub;
    logic carry_in;

    logic [16:0] sub_result_ext;
    logic sign_flag, overflow_flag, zero_flag;

    logic gt_result;  
    logic le_result; 
    
    always_comb begin
        _a = A;
        _b = B;
        result_internal = '0;

        if (en) begin
            is_sub = (opcode == OPCODE_SUB);
            _b_mod = is_sub ? ~_b : _b;
            carry_in = is_sub ? 1'b1 : 1'b0;
            add_sub_result = _a + _b_mod + carry_in;

            sub_result_ext = {1'b0, _a} - {1'b0, _b};
            sign_flag = sub_result_ext[16];
            overflow_flag = (_a[15] != _b[15]) && (sub_result_ext[15] != _a[15]);
            zero_flag = (sub_result_ext[15:0] == 0);

            gt_result = !(sign_flag ^ overflow_flag || zero_flag);  
            le_result = (sign_flag ^ overflow_flag) || zero_flag; 
            case (opcode)
                OPCODE_ADD: result_internal = add_sub_result;
                OPCODE_SUB: result_internal = add_sub_result;
                OPCODE_GT: result_internal = 16'(gt_result);
                OPCODE_LE: result_internal = 16'(le_result);
                default: result_internal = '0;
            endcase
        end else begin
            result_internal = '0;
        end
    end

    assign result = result_internal;

endmodule