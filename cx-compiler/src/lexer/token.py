from enum import Enum, auto


class TokenType(Enum):

    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()

    # Identifiers
    IDENTIFIER = auto()

    # Keywords
    INT = auto()
    FLOAT_TYPE = auto()
    BOOL = auto()
    STRING_TYPE = auto()

    IF = auto()
    ELSE = auto()
    WHILE = auto()

    FUNC = auto()
    RETURN = auto()
    PRINT = auto()

    # Arithmetic Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()

    # Assignment
    ASSIGN = auto()      # =

    # Comparison Operators
    EQUAL = auto()       # ==
    NOT_EQUAL = auto()   # !=

    LESS_THAN = auto()      # <
    GREATER_THAN = auto()   # >

    LESS_EQUAL = auto()     # <=
    GREATER_EQUAL = auto()  # >=

    # Delimiters
    LPAREN = auto()
    RPAREN = auto()

    LBRACE = auto()
    RBRACE = auto()

    COMMA = auto()
    SEMICOLON = auto()

    # End of File
    EOF = auto()


class Token:

    def __init__(self, token_type, value, line, column):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return (
            f"type={self.type.name}, "
            f"value={self.value}, "
            f"line={self.line}, "
            f"column={self.column})"
        )