from src.lexer.lexer import Lexer
from src.parser.parser import Parser

code = """
print(10 > 5);
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

print("Comparison parsing successful!")