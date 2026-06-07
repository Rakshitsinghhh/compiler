class Symbol:

    def __init__(self, name, symbol_type):
        self.name = name
        self.symbol_type = symbol_type

    def __repr__(self):
        return f"Symbol({self.name}, {self.symbol_type})"


class SymbolTable:

    def __init__(self):
        # Stack of scopes; each scope is a dict
        self.scopes = [{}]

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()

    def define(self, name, symbol_type):
        current = self.scopes[-1]
        if name in current:
            raise Exception(f"Variable '{name}' already declared in this scope")
        current[name] = Symbol(name, symbol_type)

    def lookup(self, name):
        # Walk scopes from innermost to outermost
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
