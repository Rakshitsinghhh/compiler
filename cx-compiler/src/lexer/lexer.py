from src.lexer.token import Token, TokenType
from src.lexer.errors import LexerError


class Lexer:

    KEYWORDS = {
        "int": TokenType.INT,
        "float": TokenType.FLOAT_TYPE,
        "bool": TokenType.BOOL,
        "string": TokenType.STRING_TYPE,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "func": TokenType.FUNC,
        "return": TokenType.RETURN,
        "print": TokenType.PRINT,
        "true": TokenType.BOOLEAN,
        "false": TokenType.BOOLEAN,
    }

    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def current_char(self):
        if self.position >= len(self.source):
            return None
        return self.source[self.position]

    def peek(self):
        if self.position + 1 >= len(self.source):
            return None
        return self.source[self.position + 1]

    def advance(self):
        if self.current_char() == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.position += 1

    def skip_whitespace(self):
        while (
            self.current_char() is not None
            and self.current_char().isspace()
        ):
            self.advance()

    def skip_comment(self):
        while (
            self.current_char() is not None
            and self.current_char() != "\n"
        ):
            self.advance()

    def number(self):
        start_column = self.column
        value = ""
        has_decimal = False

        while self.current_char() is not None and (
            self.current_char().isdigit()
            or self.current_char() == "."
        ):
            if self.current_char() == ".":
                if has_decimal:
                    raise LexerError(
                        "Invalid float literal",
                        self.line,
                        self.column,
                    )
                has_decimal = True

            value += self.current_char()
            self.advance()

        if has_decimal:
            return Token(
                TokenType.FLOAT,
                float(value),
                self.line,
                start_column,
            )

        return Token(
            TokenType.INTEGER,
            int(value),
            self.line,
            start_column,
        )

    def identifier(self):
        start_column = self.column
        value = ""

        while self.current_char() is not None and (
            self.current_char().isalnum()
            or self.current_char() == "_"
        ):
            value += self.current_char()
            self.advance()

        token_type = self.KEYWORDS.get(
            value,
            TokenType.IDENTIFIER
        )

        if value == "true":
            return Token(
                TokenType.BOOLEAN,
                True,
                self.line,
                start_column,
            )

        if value == "false":
            return Token(
                TokenType.BOOLEAN,
                False,
                self.line,
                start_column,
            )

        return Token(
            token_type,
            value,
            self.line,
            start_column,
        )

    def string(self):
        start_column = self.column

        self.advance()  # skip opening quote

        value = ""

        while (
            self.current_char() is not None
            and self.current_char() != '"'
        ):
            value += self.current_char()
            self.advance()

        if self.current_char() is None:
            raise LexerError(
                "Unterminated string literal",
                self.line,
                self.column,
            )

        self.advance()  # skip closing quote

        return Token(
            TokenType.STRING,
            value,
            self.line,
            start_column,
        )

    def get_next_token(self):

        while self.current_char() is not None:

            if self.current_char().isspace():
                self.skip_whitespace()
                continue

            if (
                self.current_char() == "/"
                and self.peek() == "/"
            ):
                self.skip_comment()
                continue

            if self.current_char().isdigit():
                return self.number()

            if (
                self.current_char().isalpha()
                or self.current_char() == "_"
            ):
                return self.identifier()

            if self.current_char() == '"':
                return self.string()

            # Two-character operators

            if (
                self.current_char() == "="
                and self.peek() == "="
            ):
                self.advance()
                self.advance()
                return Token(
                    TokenType.EQUAL,
                    "==",
                    self.line,
                    self.column,
                )

            if (
                self.current_char() == "!"
                and self.peek() == "="
            ):
                self.advance()
                self.advance()
                return Token(
                    TokenType.NOT_EQUAL,
                    "!=",
                    self.line,
                    self.column,
                )

            if (
                self.current_char() == "<"
                and self.peek() == "="
            ):
                self.advance()
                self.advance()
                return Token(
                    TokenType.LESS_EQUAL,
                    "<=",
                    self.line,
                    self.column,
                )

            if (
                self.current_char() == ">"
                and self.peek() == "="
            ):
                self.advance()
                self.advance()
                return Token(
                    TokenType.GREATER_EQUAL,
                    ">=",
                    self.line,
                    self.column,
                )

            # Single-character operators

            token_map = {
                "+": TokenType.PLUS,
                "-": TokenType.MINUS,
                "*": TokenType.MULTIPLY,
                "/": TokenType.DIVIDE,
                "=": TokenType.ASSIGN,
                "<": TokenType.LESS_THAN,
                ">": TokenType.GREATER_THAN,
                "(": TokenType.LPAREN,
                ")": TokenType.RPAREN,
                "{": TokenType.LBRACE,
                "}": TokenType.RBRACE,
                ",": TokenType.COMMA,
                ";": TokenType.SEMICOLON,
            }

            char = self.current_char()

            if char in token_map:
                token = Token(
                    token_map[char],
                    char,
                    self.line,
                    self.column,
                )
                self.advance()
                return token

            raise LexerError(
                f"Unexpected character '{char}'",
                self.line,
                self.column,
            )

        return Token(
            TokenType.EOF,
            None,
            self.line,
            self.column,
        )

    def tokenize(self):
        tokens = []

        while True:
            token = self.get_next_token()
            tokens.append(token)

            if token.type == TokenType.EOF:
                break

        return tokens