module mux_generic (
    input  logic [31:0] in_bool,
    input  logic [31:0] in_shift,
    input  logic [1:0] en,
    input  logic        clk,
    output logic [31:0] out
);

    logic [31:0] out_comb;

    always_comb begin
        // default: nothing selected
        out_comb = 32'b0;
        if (en[0])
            out_comb |= in_bool;
        if (en[1])
            out_comb |= in_shift;
    end

    always_ff @(posedge clk) begin
        out <= out_comb;
    end

endmodule