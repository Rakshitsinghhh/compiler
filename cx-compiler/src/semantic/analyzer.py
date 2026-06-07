from src.semantic.symbol_table import SymbolTable
from src.semantic.errors import SemanticError
from src.parser.ast_nodes import Assignment

from src.parser.ast_nodes import (
    Program,
    VariableDeclaration,
    IntegerLiteral,
    FloatLiteral,
    StringLiteral,
    Identifier,
    BinaryExpression,
    WhileStatement,
)


class SemanticAnalyzer:

    def __init__(self):
        self.symbol_table = SymbolTable()
        
    def visit(self, node):

        method_name = (
            f"visit_{type(node).__name__}"
        )

        visitor = getattr(
            self,
            method_name,
            self.generic_visit
        )

        return visitor(node)
    
    def visit_Assignment(self, node):

        symbol = self.symbol_table.lookup(
            node.name
        )

        if symbol is None:
            raise SemanticError(
                f"Undefined variable '{node.name}'"
            )

        self.visit(node.value)
        
    def visit_WhileStatement(self, node):

        self.visit(node.condition)

        for stmt in node.body:
            self.visit(stmt)

    def generic_visit(self, node):
        raise Exception(
            f"No visit method for {type(node).__name__}"
        )
        
    def visit_Program(self, node):

        for stmt in node.statements:
            self.visit(stmt)
            
    def visit_VariableDeclaration(self, node):

        self.symbol_table.define(
            node.name,
            node.var_type
        )

        self.visit(node.value)
        
    def visit_IfStatement(self, node):

        self.visit(node.condition)

        for stmt in node.then_body:
            self.visit(stmt)

        if node.else_body:

            for stmt in node.else_body:
                self.visit(stmt)
        
    def visit_PrintStatement(self, node):
        self.visit(node.expression)
        
    def visit_IntegerLiteral(self, node):
        return "int"

    def visit_FloatLiteral(self, node):
        return "float"

    def visit_StringLiteral(self, node):
        return "string"
    
    def visit_Identifier(self, node):

        symbol = self.symbol_table.lookup(
            node.name
        )

        if symbol is None:
            raise SemanticError(
                f"Undefined variable '{node.name}'"
            )

        return symbol.symbol_type
    
    def visit_BinaryExpression(self, node):

        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type != right_type:
            raise SemanticError(
                "Type mismatch in expression"
            )

        return left_type