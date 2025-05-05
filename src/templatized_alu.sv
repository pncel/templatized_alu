module templatized_alu (
  input logic [16-1:0]    A,
  input logic [16-1:0]    B,
  input logic [4-1:0] op,
  output logic [16-1:0]   out
);

  logic [16-1:0] temp [3-1:0];
  logic [1:0] sel;

  // Instantiate ALU groups
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

  // Instantiate control module
  templatized_alu_control control_inst (
    .op_code (op),
    .select  (sel)
  );

  // Instantiate mux
  mux_generic mux_generic_inst (
    .in  (temp),
    .sel (sel),
    .out (out)
  );

endmodule