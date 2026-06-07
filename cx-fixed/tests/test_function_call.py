from src.lexer.lexer import Lexer
from src.parser.parser import Parser

source = """
int x = add(10, 20);
"""

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

print("Function call parsed successfully!")
print(ast)