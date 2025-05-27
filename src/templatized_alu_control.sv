module templatized_alu_control (
    input  logic [3:0] op_code,
    output logic [2:0] en
);

always_comb begin
    en = 3'b0;
    unique case (op_code)
        4'b0000: en = { 1, 0, 0 };
        4'b0001: en = { 1, 0, 0 };
        4'b0010: en = { 1, 0, 0 };
        4'b0100: en = { 1, 1, 0 };
        4'b0101: en = { 0, 1, 0 };
        4'b0110: en = { 0, 0, 1 };
        4'b0111: en = { 0, 0, 1 };
        4'b1000: en = { 0, 0, 1 };
        4'b1001: en = { 0, 0, 1 };
        default: en = 3'b0;
    endcase
end

endmodule