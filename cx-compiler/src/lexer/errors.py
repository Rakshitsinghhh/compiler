class LexerError(Exception):
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column

        super().__init__(
            f"Lexer Error at line {line}, column {column}: {message}"
        )