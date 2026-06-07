from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.ir.generator import IRGenerator

code = """
int x = 10 + 20;
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

generator = IRGenerator()

instructions = generator.generate(ast)

print("\nTHREE ADDRESS CODE")
print("=" * 40)

for instruction in instructions:
    print(instruction)