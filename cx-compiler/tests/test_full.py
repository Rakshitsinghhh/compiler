from src.lexer.lexer import Lexer
from src.parser.parser import Parser

source = """
func add(a, b) {
    return a + b;
}

int x = 10;

if (x > 5) {
    print(x);
}

while (x < 20) {
    x = x + 1;
}
"""

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

print("FULL PROGRAM PARSED SUCCESSFULLY")