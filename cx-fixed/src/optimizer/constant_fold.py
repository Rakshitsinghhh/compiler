from src.parser.ast_nodes import (
    IntegerLiteral,
    BinaryExpression,
)


class ConstantFolder:

    def optimize(self, node):

        method = getattr(
            self,
            f"optimize_{type(node).__name__}",
            self.generic
        )

        return method(node)

    def generic(self, node):
        return node

    def optimize_IntegerLiteral(
        self,
        node
    ):
        return node

    def optimize_BinaryExpression(
        self,
        node
    ):

        left = self.optimize(node.left)
        right = self.optimize(node.right)

        if (
            isinstance(left, IntegerLiteral)
            and isinstance(right, IntegerLiteral)
        ):

            if node.operator == "+":
                return IntegerLiteral(
                    left.value + right.value
                )

            if node.operator == "-":
                return IntegerLiteral(
                    left.value - right.value
                )

            if node.operator == "*":
                return IntegerLiteral(
                    left.value * right.value
                )

            if node.operator == "/":
                return IntegerLiteral(
                    left.value // right.value
                )

        node.left = left
        node.right = right

        return node