from src.codegen.instructions import Instruction


class CodeGenerator:

    def __init__(self):
        self.instructions = []

    def generate(self, tac_instructions):

        for tac in tac_instructions:

            opcode = tac.result

            # ---- Control flow & special opcodes ----

            if opcode == "LABEL":
                self.instructions.append(
                    Instruction("LABEL", f"{tac.arg1}:")
                )

            elif opcode == "GOTO":
                self.instructions.append(
                    Instruction("JMP", tac.arg1)
                )

            elif opcode == "IF_FALSE":
                # condition is in arg1, target label in operator
                self.instructions.append(
                    Instruction("LOAD", tac.arg1)
                )
                self.instructions.append(
                    Instruction("JZ", tac.operator)
                )

            elif opcode == "PRINT":
                self.instructions.append(
                    Instruction("LOAD", tac.arg1)
                )
                self.instructions.append(
                    Instruction("PRINT", None)
                )

            elif opcode == "FUNC":
                # Encode params as "name:p1,p2,p3" so the VM can bind args
                params_str = ",".join(tac.operator) if tac.operator else ""
                operand = f"{tac.arg1}:{params_str}" if params_str else tac.arg1
                self.instructions.append(
                    Instruction("FUNC_BEGIN", operand)
                )

            elif opcode == "ARG":
                # Push argument value onto the arg-passing stack
                self.instructions.append(
                    Instruction("PUSH_ARG", tac.arg1)
                )

            elif opcode == "END_FUNC":
                self.instructions.append(
                    Instruction("FUNC_END", tac.arg1)
                )

            elif opcode == "RETURN":
                self.instructions.append(
                    Instruction("LOAD", tac.arg1)
                )
                self.instructions.append(
                    Instruction("RET", None)
                )

            elif opcode == "CALL":
                # arg1=func_name, operator=num_args, arg2=result_temp
                self.instructions.append(
                    Instruction("CALL", f"{tac.arg1} {tac.operator}")
                )
                self.instructions.append(
                    Instruction("STORE", tac.arg2)
                )

            # ---- Assignments / arithmetic ----

            elif tac.operator is None:
                # Simple copy: result = arg1
                self.instructions.append(
                    Instruction("MOV", f"{tac.result}, {tac.arg1}")
                )

            else:
                # Binary expression: result = arg1 op arg2
                self.instructions.append(
                    Instruction("LOAD", tac.arg1)
                )

                op_map = {
                    "+":  "ADD",
                    "-":  "SUB",
                    "*":  "MUL",
                    "/":  "DIV",
                    "==": "CMP_EQ",
                    "!=": "CMP_NEQ",
                    "<":  "CMP_LT",
                    ">":  "CMP_GT",
                    "<=": "CMP_LTE",
                    ">=": "CMP_GTE",
                }

                asm_op = op_map.get(tac.operator, f"OP_{tac.operator}")
                self.instructions.append(
                    Instruction(asm_op, tac.arg2)
                )

                self.instructions.append(
                    Instruction("STORE", tac.result)
                )

        return self.instructions
