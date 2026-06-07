class Instruction:

    def __init__(self, opcode, operand=None):
        self.opcode = opcode
        self.operand = operand

    def __str__(self):

        if self.operand is None:
            return self.opcode

        return f"{self.opcode} {self.operand}"