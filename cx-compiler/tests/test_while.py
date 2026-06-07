from src.lexer.lexer import Lexer
from src.parser.parser import Parser

code = """
int x = 0;

while (x < 5) {
    print(x);
    x = x + 1;
}
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

print("While parsing successful!")
print(ast)