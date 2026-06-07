from src.ir.tac import TACInstruction

from src.parser.ast_nodes import (
    Program,
    VariableDeclaration,
    IntegerLiteral,
    FloatLiteral,
    StringLiteral,
    Identifier,
    BinaryExpression,
    Assignment,
    PrintStatement,
    IfStatement,
    WhileStatement,
)


class IRGenerator:

    def __init__(self):
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0

    # -------------------------
    # TEMP VARIABLES
    # -------------------------

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    # -------------------------
    # LABELS
    # -------------------------

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    # -------------------------
    # DISPATCH
    # -------------------------

    def generate(self, node):

        method_name = (
            f"generate_{type(node).__name__}"
        )

        method = getattr(
            self,
            method_name
        )

        return method(node)

    # -------------------------
    # PROGRAM
    # -------------------------

    def generate_Program(self, node):

        for stmt in node.statements:
            self.generate(stmt)

        return self.instructions

    # -------------------------
    # VARIABLE DECLARATION
    # -------------------------

    def generate_VariableDeclaration(
        self,
        node
    ):

        value = self.generate(
            node.value
        )

        self.instructions.append(
            TACInstruction(
                node.name,
                value
            )
        )

    # -------------------------
    # ASSIGNMENT
    # -------------------------

    def generate_Assignment(
        self,
        node
    ):

        value = self.generate(
            node.value
        )

        self.instructions.append(
            TACInstruction(
                node.name,
                value
            )
        )

    # -------------------------
    # PRINT
    # -------------------------

    def generate_PrintStatement(
        self,
        node
    ):

        value = self.generate(
            node.expression
        )

        self.instructions.append(
            TACInstruction(
                "PRINT",
                value
            )
        )

    # -------------------------
    # IF
    # -------------------------

    def generate_IfStatement(self, node):

        condition = self.generate(
            node.condition
        )

        else_label = self.new_label()
        end_label = self.new_label()

        self.instructions.append(
            TACInstruction(
                "IF_FALSE",
                condition,
                else_label
            )
        )

        for stmt in node.then_body:
            self.generate(stmt)

        self.instructions.append(
            TACInstruction(
                "GOTO",
                end_label
            )
        )

        self.instructions.append(
            TACInstruction(
                "LABEL",
                else_label
            )
        )

        if node.else_body:

            for stmt in node.else_body:
                self.generate(stmt)

        self.instructions.append(
            TACInstruction(
                "LABEL",
                end_label
            )
        )

    # -------------------------
    # LITERALS
    # -------------------------

    def generate_IntegerLiteral(
        self,
        node
    ):
        return node.value

    def generate_FloatLiteral(
        self,
        node
    ):
        return node.value

    def generate_StringLiteral(
        self,
        node
    ):
        return f'"{node.value}"'

    def generate_Identifier(
        self,
        node
    ):
        return node.name

    # -------------------------
    # BINARY EXPRESSIONS
    # -------------------------

    def generate_BinaryExpression(
        self,
        node
    ):

        left = self.generate(
            node.left
        )

        right = self.generate(
            node.right
        )

        temp = self.new_temp()

        self.instructions.append(
            TACInstruction(
                temp,
                left,
                node.operator,
                right
            )
        )

        return temp
    
    def generate_WhileStatement(self, node):

        start_label = self.new_label()
        end_label = self.new_label()

        self.instructions.append(
            TACInstruction(
                "LABEL",
                start_label
            )
        )

        condition = self.generate(
            node.condition
        )

        self.instructions.append(
            TACInstruction(
                "IF_FALSE",
                condition,
                end_label
            )
        )

        for stmt in node.body:
            self.generate(stmt)

        self.instructions.append(
            TACInstruction(
                "GOTO",
                start_label
            )
        )

        self.instructions.append(
            TACInstruction(
                "LABEL",
                end_label
            )
        )