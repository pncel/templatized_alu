// one hot mux
module mux_generic (
    input logic [3] [16-1:0] in,
    input logic [3-1:0] en,
    input logic clk,
    output logic [16-1:0] out
);

    logic [16-1:0] out_comb;

    always_comb begin
        if (en[0])
            out_comb |= in[0];
        if (en[1])
            out_comb |= in[1];
        if (en[2])
            out_comb |= in[2];
        out_comb = out;
    end

    always_ff @(posedge clk) begin
        out <= out_comb;
    end

endmodule