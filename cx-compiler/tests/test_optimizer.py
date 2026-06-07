from src.parser.ast_nodes import (
    IntegerLiteral,
    BinaryExpression,
)

from src.optimizer.constant_fold import (
    ConstantFolder
)

expr = BinaryExpression(
    IntegerLiteral(10),
    "+",
    IntegerLiteral(20)
)

result = ConstantFolder().optimize(expr)

print(type(result).__name__)
print(result.value)