class Symbol:

    def __init__(self, name, symbol_type):
        self.name = name
        self.symbol_type = symbol_type

    def __repr__(self):
        return f"Symbol({self.name}, {self.symbol_type})"


class SymbolTable:

    def __init__(self):
        self.symbols = {}

    def define(self, name, symbol_type):

        if name in self.symbols:
            raise Exception(
                f"Variable '{name}' already declared"
            )

        self.symbols[name] = Symbol(
            name,
            symbol_type
        )

    def lookup(self, name):
        return self.symbols.get(name)