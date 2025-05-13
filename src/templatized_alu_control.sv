module templatized_alu_control (
    input  logic [2:0] op_code,
    output logic [2:0] en
);

always_comb begin
    en = 3'b0;
    unique case (op_code)
        3'b000: en = { 1, 0, 0 };
        3'b001: en = { 1, 0, 0 };
        3'b010: en = { 0, 1, 0 };
        3'b011: en = { 0, 0, 1 };
        3'b100: en = { 0, 0, 1 };
        3'b101: en = { 0, 0, 1 };
        3'b110: en = { 0, 0, 1 };
        default: en = 3'b0;
    endcase
end

endmodule