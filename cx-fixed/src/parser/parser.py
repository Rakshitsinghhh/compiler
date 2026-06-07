from src.lexer.token import TokenType
from src.parser.errors import ParserError

from src.parser.ast_nodes import (
    Program,
    IntegerLiteral,
    FloatLiteral,
    StringLiteral,
    Identifier,
    BinaryExpression,
    VariableDeclaration,
    Assignment,
    PrintStatement,
    IfStatement,
    WhileStatement,
    FunctionDeclaration,
    ReturnStatement,
    FunctionCall,
)


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):

        if self.position >= len(self.tokens):
            return self.tokens[-1]

        return self.tokens[self.position]

    def advance(self):
        self.position += 1

    def consume(self, expected_type):

        token = self.current_token()

        if token.type != expected_type:
            raise ParserError(
                f"Expected {expected_type.name}, got {token.type.name}",
                token,
            )

        self.advance()
        return token

    # =====================================
    # FACTOR
    # =====================================

    def parse_factor(self):

        token = self.current_token()

        if token.type == TokenType.INTEGER:
            self.advance()
            return IntegerLiteral(token.value)

        if token.type == TokenType.FLOAT:
            self.advance()
            return FloatLiteral(token.value)

        if token.type == TokenType.STRING:
            self.advance()
            return StringLiteral(token.value)

        if token.type == TokenType.IDENTIFIER:

            if (
                self.position + 1 < len(self.tokens)
                and self.tokens[self.position + 1].type
                == TokenType.LPAREN
            ):
                return self.parse_function_call()

            self.advance()
            return Identifier(token.value)

        if token.type == TokenType.LPAREN:

            self.consume(TokenType.LPAREN)

            expr = self.parse_comparison()

            self.consume(TokenType.RPAREN)

            return expr

        raise ParserError(
            "Unexpected token",
            token
        )

    # =====================================
    # TERM
    # =====================================

    def parse_term(self):

        left = self.parse_factor()

        while self.current_token().type in (
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
        ):

            operator = self.current_token()
            self.advance()

            right = self.parse_factor()

            left = BinaryExpression(
                left,
                operator.value,
                right
            )

        return left

    # =====================================
    # EXPRESSION
    # =====================================

    def parse_expression(self):

        left = self.parse_term()

        while self.current_token().type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):

            operator = self.current_token()
            self.advance()

            right = self.parse_term()

            left = BinaryExpression(
                left,
                operator.value,
                right
            )

        return left

    # =====================================
    # COMPARISON
    # =====================================

    def parse_comparison(self):

        left = self.parse_expression()

        while self.current_token().type in (
            TokenType.EQUAL,
            TokenType.NOT_EQUAL,
            TokenType.LESS_THAN,
            TokenType.GREATER_THAN,
            TokenType.LESS_EQUAL,
            TokenType.GREATER_EQUAL,
        ):

            operator = self.current_token()
            self.advance()

            right = self.parse_expression()

            left = BinaryExpression(
                left,
                operator.value,
                right
            )

        return left

    # =====================================
    # PRINT
    # =====================================

    def parse_print_statement(self):

        self.consume(TokenType.PRINT)

        self.consume(TokenType.LPAREN)

        expr = self.parse_comparison()

        self.consume(TokenType.RPAREN)

        self.consume(TokenType.SEMICOLON)

        return PrintStatement(expr)

    # =====================================
    # VARIABLE DECLARATION
    # =====================================

    def parse_variable_declaration(self):

        type_token = self.current_token()
        self.advance()

        name = self.consume(
            TokenType.IDENTIFIER
        )

        self.consume(
            TokenType.ASSIGN
        )

        value = self.parse_comparison()

        self.consume(
            TokenType.SEMICOLON
        )

        return VariableDeclaration(
            type_token.value,
            name.value,
            value,
        )

    # =====================================
    # ASSIGNMENT
    # =====================================

    def parse_assignment(self):

        name = self.consume(
            TokenType.IDENTIFIER
        )

        self.consume(
            TokenType.ASSIGN
        )

        value = self.parse_comparison()

        self.consume(
            TokenType.SEMICOLON
        )

        return Assignment(
            name.value,
            value
        )

    # =====================================
    # FUNCTION CALL
    # =====================================

    def parse_function_call(self):

        name = self.consume(
            TokenType.IDENTIFIER
        )

        self.consume(TokenType.LPAREN)

        arguments = []

        if self.current_token().type != TokenType.RPAREN:

            arguments.append(
                self.parse_comparison()
            )

            while (
                self.current_token().type
                == TokenType.COMMA
            ):

                self.consume(
                    TokenType.COMMA
                )

                arguments.append(
                    self.parse_comparison()
                )

        self.consume(TokenType.RPAREN)

        return FunctionCall(
            name.value,
            arguments
        )

    # =====================================
    # RETURN
    # =====================================

    def parse_return_statement(self):

        self.consume(TokenType.RETURN)

        value = self.parse_comparison()

        self.consume(TokenType.SEMICOLON)

        return ReturnStatement(value)

    # =====================================
    # FUNCTION DECLARATION
    # =====================================

    def parse_function_declaration(self):

        self.consume(TokenType.FUNC)

        name = self.consume(
            TokenType.IDENTIFIER
        )

        self.consume(TokenType.LPAREN)

        parameters = []

        if self.current_token().type != TokenType.RPAREN:

            param = self.consume(
                TokenType.IDENTIFIER
            )

            parameters.append(
                param.value
            )

            while (
                self.current_token().type
                == TokenType.COMMA
            ):

                self.consume(
                    TokenType.COMMA
                )

                param = self.consume(
                    TokenType.IDENTIFIER
                )

                parameters.append(
                    param.value
                )

        self.consume(TokenType.RPAREN)

        self.consume(TokenType.LBRACE)

        body = []

        while (
            self.current_token().type
            != TokenType.RBRACE
        ):
            body.append(
                self.parse_statement()
            )

        self.consume(TokenType.RBRACE)

        return FunctionDeclaration(
            name.value,
            parameters,
            body
        )

    # =====================================
    # IF
    # =====================================

    def parse_if_statement(self):

        self.consume(TokenType.IF)

        self.consume(TokenType.LPAREN)

        condition = self.parse_comparison()

        self.consume(TokenType.RPAREN)

        self.consume(TokenType.LBRACE)

        then_body = []

        while self.current_token().type != TokenType.RBRACE:
            then_body.append(
                self.parse_statement()
            )

        self.consume(TokenType.RBRACE)

        else_body = None

        if self.current_token().type == TokenType.ELSE:

            self.consume(TokenType.ELSE)

            self.consume(TokenType.LBRACE)

            else_body = []

            while self.current_token().type != TokenType.RBRACE:
                else_body.append(
                    self.parse_statement()
                )

            self.consume(TokenType.RBRACE)

        return IfStatement(
            condition,
            then_body,
            else_body
        )

    # =====================================
    # WHILE
    # =====================================

    def parse_while_statement(self):

        self.consume(TokenType.WHILE)

        self.consume(TokenType.LPAREN)

        condition = self.parse_comparison()

        self.consume(TokenType.RPAREN)

        self.consume(TokenType.LBRACE)

        body = []

        while self.current_token().type != TokenType.RBRACE:
            body.append(
                self.parse_statement()
            )

        self.consume(TokenType.RBRACE)

        return WhileStatement(
            condition,
            body
        )

    # =====================================
    # STATEMENT
    # =====================================

    def parse_statement(self):

        token = self.current_token()

        if token.type == TokenType.FUNC:
            return self.parse_function_declaration()

        if token.type == TokenType.RETURN:
            return self.parse_return_statement()

        if token.type in (
            TokenType.INT,
            TokenType.FLOAT_TYPE,
            TokenType.BOOL,
            TokenType.STRING_TYPE,
        ):
            return self.parse_variable_declaration()

        if token.type == TokenType.IF:
            return self.parse_if_statement()

        if token.type == TokenType.WHILE:
            return self.parse_while_statement()

        if token.type == TokenType.PRINT:
            return self.parse_print_statement()

        if (
            token.type == TokenType.IDENTIFIER
            and self.position + 1 < len(self.tokens)
            and self.tokens[self.position + 1].type
            == TokenType.ASSIGN
        ):
            return self.parse_assignment()

        raise ParserError(
            "Unknown statement",
            token
        )

    # =====================================
    # PROGRAM
    # =====================================

    def parse(self):

        statements = []

        while (
            self.current_token().type
            != TokenType.EOF
        ):
            statements.append(
                self.parse_statement()
            )

        return Program(
            statements
        )