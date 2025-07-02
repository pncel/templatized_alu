<<<<<<< HEAD
// alu_32bit_add_sub_lt_gt.sv
module alu_add (
    input  logic [31:0] A,
    input  logic [31:0] B,
    input  logic [3:0] opcode,
    input  logic en,
    output logic [31:0] result
=======
// alu_16bit_add_sub_gt_le.sv
module alu_add (
    input  logic [15:0] A,
    input  logic [15:0] B,
    input  logic [3:0] opcode,
    input  logic en,
    output logic [15:0] result
>>>>>>> origin/Ayush
);

    // Opcode constants
    localparam [3:0] OPCODE_ADD = 4'b0000;
    localparam [3:0] OPCODE_SUB = 4'b0001;
<<<<<<< HEAD
    localparam [3:0] OPCODE_LT = 4'b0010;
    localparam [3:0] OPCODE_GT = 4'b0011;

    // Internal signals
    logic [31:0] result_internal;
    logic [31:0] _a, _b;

    logic [31:0] add_sub_result;
    
    logic [31:0] _b_mod;
    logic is_sub;
    logic carry_in;

    logic [32:0] sub_result_ext;
    logic sign_flag, overflow_flag, zero_flag;

 logic lt_result;  logic gt_result; 
    always_comb begin
        _a              = A;
        _b              = B;
        result_internal = 32'b0;

        is_sub         = 1'b0;
        _b_mod         = 32'b0;
        carry_in       = 1'b0;
        add_sub_result = 32'b0;

        sub_result_ext  = 33'b0;
        sign_flag       = 1'b0;
        overflow_flag   = 1'b0;
        zero_flag       = 1'b0;
 lt_result = 1'b0;  gt_result = 1'b0; 
=======
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
>>>>>>> origin/Ayush

        if (en) begin
            is_sub = (opcode == OPCODE_SUB);
            _b_mod = is_sub ? ~_b : _b;
            carry_in = is_sub ? 1'b1 : 1'b0;
<<<<<<< HEAD
            add_sub_result = _a + _b_mod + { 31'b0, carry_in };

            sub_result_ext = {1'b0, _a} - {1'b0, _b};
            sign_flag = sub_result_ext[32];
            overflow_flag = (_a[31] != _b[31]) && (sub_result_ext[31] != _a[31]);
            zero_flag = (sub_result_ext[31:0] == 0);

 lt_result = (sign_flag ^ overflow_flag);  gt_result = !(sign_flag ^ overflow_flag || zero_flag); 
            case (opcode)
                OPCODE_ADD: result_internal = add_sub_result;
                OPCODE_SUB: result_internal = add_sub_result;
                OPCODE_LT: result_internal = { 31'b0, lt_result };
                OPCODE_GT: result_internal = { 31'b0, gt_result };
                default: result_internal = 32'b0;
=======
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
>>>>>>> origin/Ayush
            endcase
        end else begin
            result_internal = '0;
        end
    end

    assign result = result_internal;

endmodule