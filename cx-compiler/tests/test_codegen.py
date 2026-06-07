from src.lexer.lexer import Lexer
from src.parser.parser import Parser

from src.ir.generator import IRGenerator
from src.codegen.generator import CodeGenerator


code = """
int x = 10 + 20;
"""


lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

ir_generator = IRGenerator()
tac = ir_generator.generate(ast)

print("\nTHREE ADDRESS CODE")
print("=" * 40)

for instruction in tac:
    print(instruction)


codegen = CodeGenerator()

assembly = codegen.generate(tac)

print("\nASSEMBLY")
print("=" * 40)

for instruction in assembly:
    print(instruction)