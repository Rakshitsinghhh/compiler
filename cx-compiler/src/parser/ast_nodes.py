class ASTNode:
    pass


class Program(ASTNode):

    def __init__(self, statements):
        self.statements = statements


class IntegerLiteral(ASTNode):

    def __init__(self, value):
        self.value = value


class FloatLiteral(ASTNode):

    def __init__(self, value):
        self.value = value


class StringLiteral(ASTNode):

    def __init__(self, value):
        self.value = value


class Identifier(ASTNode):

    def __init__(self, name):
        self.name = name


class BinaryExpression(ASTNode):

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class VariableDeclaration(ASTNode):

    def __init__(self, var_type, name, value):
        self.var_type = var_type
        self.name = name
        self.value = value


class Assignment(ASTNode):

    def __init__(self, name, value):
        self.name = name
        self.value = value
        
class PrintStatement(ASTNode):

    def __init__(self, expression):
        self.expression = expression
        
class IfStatement(ASTNode):

    def __init__(
        self,
        condition,
        then_body,
        else_body=None
    ):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body
        
class WhileStatement(ASTNode):

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        