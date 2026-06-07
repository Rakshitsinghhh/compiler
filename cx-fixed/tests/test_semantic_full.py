"""
test_semantic_full.py — semantic analysis layer tests
"""
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.semantic.errors import SemanticError


def analyze(source):
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    SemanticAnalyzer().visit(ast)


def check_ok(name, source):
    try:
        analyze(source)
        print(f"  [PASS]  {name}")
        return True
    except Exception as e:
        print(f"  [FAIL]  {name}  =>  {e}")
        return False


def check_err(name, source):
    try:
        analyze(source)
        print(f"  [FAIL]  {name}  =>  Expected error but got none")
        return False
    except (SemanticError, Exception):
        print(f"  [PASS]  {name}  (error correctly raised)")
        return True


def main():
    print("\nSEMANTIC ANALYSIS LAYER TESTS")
    print("=" * 50)

    passed = 0
    total = 0

    def ok(name, src):
        nonlocal passed, total
        total += 1
        if check_ok(name, src): passed += 1

    def err(name, src):
        nonlocal passed, total
        total += 1
        if check_err(name, src): passed += 1

    ok("int declaration",        "int x = 10;")
    ok("float declaration",      "float f = 3.14;")
    ok("string declaration",     'string s = "hello";')
    ok("var use after decl",     "int x = 1; int y = x + 1;")
    ok("assignment valid",       "int x = 0; x = 5;")
    ok("if with declared var",   "int x = 5; if (x > 0) { print(x); }")
    ok("while with declared var","int x = 0; while (x < 3) { x = x + 1; }")
    ok("function declaration",   "func add(a, b) { return a + b; }")
    ok("function call",          "func f(n) { return n; } int r = f(1);")
    ok("nested if",
       "int x = 5; if (x > 0) { int y = x + 1; print(y); }")

    err("undefined variable",    "print(z);")
    err("assign before decl",    "x = 5;")
    err("use before decl",       "int y = z + 1;")

    print(f"\n  {'=' * 40}")
    print(f"  Result: {passed}/{total} tests passed")
    if passed == total:
        print("  [ALL PASSED]")


if __name__ == "__main__":
    main()
