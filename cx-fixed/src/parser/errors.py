class ParserError(Exception):
    def __init__(self, message, token):
        self.message = message
        self.token = token

        super().__init__(
            f"Parser Error: {message} "
            f"at line {token.line}, "
            f"column {token.column}"
        )