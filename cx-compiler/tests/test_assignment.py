# tests/test_assignment.py

from src.lexer.lexer import Lexer
from src.parser.parser import Parser

code = """
int x = 10;
x = x + 1;
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

print("✓ Assignment Parsing Successful")
print(ast)