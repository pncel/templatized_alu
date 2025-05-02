// top_level_alu_template_v1.sv.j2
module templatized_alu (
  input logic [32-1:0]    A,
  input logic [32-1:0]    B,
  input logic [3-1:0] op,

  input logic [$clog2(3)-1:0] sel,
  output logic [32-1:0]   out
);

  logic [32-1:0] temp [3-1:0];

  alu_add alu_add_inst_0 (
    .A     (A),
    .B     (B),
    .op    (op),
    .result(temp[0])
  );
  alu_bool alu_bool_inst_1 (
    .A     (A),
    .B     (B),
    .op    (op),
    .result(temp[1])
  );
  alu_shift alu_shift_inst_2 (
    .A     (A),
    .B     (B),
    .op    (op),
    .result(temp[2])
  );

  mux_generic #(.NUM_INPUTS(3)) mux_generic_inst (
    .in  (temp),
    .sel (sel),
    .out (out)
  );

endmodule