from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.ir.generator import IRGenerator

code = """
int x = 10;

if (x > 5) {
    print(x);
}
else {
    print(0);
}
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

ir = IRGenerator().generate(ast)

print("\nIR")
print("=" * 40)

for instruction in ir:
    print(instruction)