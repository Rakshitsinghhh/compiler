from src.lexer.lexer import Lexer
from src.parser.parser import Parser

source = """
func add(a, b) {
    return a + b;
}
"""

lexer = Lexer(source)
tokens = lexer.tokenize()

print("TOKENS")
print("=" * 40)

for token in tokens:
    print(token)

print("\nPARSING...")
print("=" * 40)

parser = Parser(tokens)
ast = parser.parse()

print("Function parsed successfully!")
func = ast.statements[0]

print("Function Name:", func.name)
print("Parameters:", func.parameters)
print("Body Statements:", len(func.body))