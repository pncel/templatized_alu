module mux_generic (
    input logic [3] [32-1:0] in,
    input logic [$clog2(3)-1:0] sel,
    output logic [32-1:0] out
);

always_comb begin
    case (sel)
        0: out = in[0];
        1: out = in[1];
        2: out = in[2];
        default: out = '0;
    endcase
end

endmodule