from src.codegen.instructions import Instruction


class CodeGenerator:

    def __init__(self):
        self.instructions = []

    def generate(self, tac_instructions):

        for tac in tac_instructions:

            # x = 10
            if tac.operator is None:

                self.instructions.append(
                    Instruction(
                        "MOV",
                        f"{tac.result}, {tac.arg1}"
                    )
                )

            # t1 = a + b
            else:

                self.instructions.append(
                    Instruction(
                        "LOAD",
                        tac.arg1
                    )
                )

                if tac.operator == "+":
                    self.instructions.append(
                        Instruction(
                            "ADD",
                            tac.arg2
                        )
                    )

                elif tac.operator == "-":
                    self.instructions.append(
                        Instruction(
                            "SUB",
                            tac.arg2
                        )
                    )

                elif tac.operator == "*":
                    self.instructions.append(
                        Instruction(
                            "MUL",
                            tac.arg2
                        )
                    )

                elif tac.operator == "/":
                    self.instructions.append(
                        Instruction(
                            "DIV",
                            tac.arg2
                        )
                    )

                self.instructions.append(
                    Instruction(
                        "STORE",
                        tac.result
                    )
                )

        return self.instructions