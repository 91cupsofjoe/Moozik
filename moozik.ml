(* Top-level of the Moozik compiler: scan & parse the input,
   check the resulting AST and generate an SAST from it, generate LLVM IR,
   and dump the module *)

   type action = Ast | Sast | LLVM_IR

   let () =
     let action = ref LLVM_IR in
     let set_action a () = action := a in
     let speclist = [
       ("-a", Arg.Unit (set_action Ast), "Print the AST");
       ("-s", Arg.Unit (set_action Sast), "Print the SAST");
       ("-l", Arg.Unit (set_action LLVM_IR), "Print the generated LLVM IR");
     ] in
     let usage_msg = "usage: ./moozik.native [-a|-s|-l] [file.mz]" in
     let channel = ref stdin in
     let input_file = ref "" in
     Arg.parse speclist (fun filename -> 
       input_file := filename;
       channel := open_in filename
     ) usage_msg;
   
     let lexbuf = Lexing.from_channel !channel in
   
     let ast = Parser.program_rule Scanner.token lexbuf in
     let sast = Semant.check ast in
     match !action with
       LLVM_IR -> print_string (Llvm.string_of_llmodule (Irgen.translate sast !input_file))
     | Ast -> print_string (Ast.string_of_program ast)
     | Sast -> print_string (Sast.string_of_sprogram sast)
      