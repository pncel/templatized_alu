module templatized_alu (
  input  logic                  clk,
  input  logic [32-1:0]  A,
  input  logic [32-1:0]  B,
  input  logic [3-1:0] op,
  output logic [32-1:0]  out
);

  logic [32-1:0] temp [2-1:0];
  logic [1:0] en;

  // Registered inputs
  logic [32-1:0] A_data;
  logic [32-1:0] B_data;

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
  alu_bool alu_bool_inst_0 (
    .A     (A_data),
    .B     (B_data),
    .op    (op),
    .en    (en[0]),
    .result(temp[0])
  );
  alu_shift alu_shift_inst_1 (
    .A     (A_data),
    .B     (B_data),
    .op    (op),
    .en    (en[1]),
    .result(temp[1])
  );

  // Output mux
  mux_generic mux_generic_inst (
    .in_bool   ( temp[0] ),
    .in_shift   ( temp[1] ),
    .en           ( en ),
    .clk          ( clk ),
    .out          ( out )
  );

endmodule