from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer

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

analyzer = SemanticAnalyzer()

analyzer.visit(ast)

print("Semantic Analysis Passed!")