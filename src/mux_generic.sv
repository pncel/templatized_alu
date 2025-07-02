<<<<<<< HEAD
module mux_generic (
    input  logic [31:0] in_add,
    input  logic [31:0] in_bool,
    input  logic [31:0] in_shift,
    input  logic [2:0] en,
    input  logic        clk,
    output logic [31:0] out
);

    logic [31:0] out_comb;

    always_comb begin
        // default: nothing selected
        out_comb = 32'b0;
        if (en[0])
            out_comb = out_comb | in_add;
        if (en[1])
            out_comb = out_comb | in_bool;
        if (en[2])
            out_comb = out_comb | in_shift;
=======
// one hot mux
module mux_generic (
    input logic  [16-1:0] in [3-1:0],
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
>>>>>>> origin/Ayush
    end

    always_ff @(posedge clk) begin
        out <= out_comb;
    end

endmodule