module templatized_alu (
  input  logic                  clk,
  input  logic [16-1:0]  A,
  input  logic [16-1:0]  B,
  input  logic [3-1:0] op,
  output logic [16-1:0]  out
);

  logic [16-1:0] temp [3-1:0];
  logic [2:0] en;

  // Registered inputs
  logic [16-1:0] A_data;
  logic [16-1:0] B_data;

  // Optional ready-controlled input sampling (for future multi-cycle ops)
  always_ff @(posedge clk) begin
    // if (ready) begin (for future multi-cycle ops)
      A_data <= A;
      B_data <= B;
    // end
  end

  // Instantiate control module
  templatized_alu_control control_inst (
    .op_code (op),
    .en      (en)
  );

  // ALU group instantiations
  alu_add alu_add_inst_0 (
    .A     (A_data),
    .B     (B_data),
    .op    (op),
    .en    (en[0]),
    .result(temp[0])
  );
  alu_bool alu_bool_inst_1 (
    .A     (A_data),
    .B     (B_data),
    .op    (op),
    .en    (en[1]),
    .result(temp[1])
  );
  alu_shift alu_shift_inst_2 (
    .A     (A_data),
    .B     (B_data),
    .op    (op),
    .en    (en[2]),
    .result(temp[2])
  );

  // Output mux
  mux_generic mux_generic_inst (
    .in  (temp),
    .en  (en),
    .out (out)
  );

endmodule