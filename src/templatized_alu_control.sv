module templatized_alu_control (
    input  logic [3:0] op_code,
    output logic [1:0] select
);

always_comb begin
    unique case (op_code)
            4'b0000: select = 2'd0;
            4'b0001: select = 2'd0;
            4'b0011: select = 2'd0;
            4'b0011: select = 2'd1;
            4'b0100: select = 2'd1;
            4'b0101: select = 2'd2;
            4'b0110: select = 2'd2;
            4'b0111: select = 2'd2;
            4'b1000: select = 2'd2;
    default: select = 2'd0; // fallback
    endcase
end

endmodule