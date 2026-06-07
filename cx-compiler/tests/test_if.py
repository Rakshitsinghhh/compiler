from src.lexer.lexer import Lexer
from src.parser.parser import Parser

code = """
int x = 10;

if (x > 5) {
    print(x);
}
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

print("IF statement parsed successfully!")
print(ast)