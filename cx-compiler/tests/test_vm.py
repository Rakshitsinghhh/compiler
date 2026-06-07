"""
test_vm.py — VM execution tests
Tests that cx programs actually produce the correct output.
"""

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.generator import IRGenerator
from src.codegen.generator import CodeGenerator
from src.vm.interpreter import VM


def run(source):
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    SemanticAnalyzer().visit(ast)
    tac = IRGenerator().generate(ast)
    asm = CodeGenerator().generate(tac)
    vm = VM()
    vm.load(asm)
    return vm.run()


def test(name, source, expected):
    output = run(source)
    result = output[0] if output else ""
    status = "PASS" if str(result) == str(expected) else "FAIL"
    print(f"  [{status}]  {name}")
    if status == "FAIL":
        print(f"         expected={expected!r}  got={result!r}")
    return status == "PASS"


def main():
    print("\nVM EXECUTION TESTS")
    print("=" * 50)

    passed = 0
    total = 0

    def check(name, src, expected):
        nonlocal passed, total
        total += 1
        if test(name, src, expected):
            passed += 1

    # Basic arithmetic
    check("print integer",         'int x = 42; print(x);',                  "42")
    check("addition",              'int x = 10 + 20; print(x);',             "30")
    check("subtraction",           'int x = 50 - 8; print(x);',              "42")
    check("multiplication",        'int x = 6 * 7; print(x);',               "42")
    check("chained arithmetic",    'int x = 2 + 3; int y = x + 37; print(y);',"42")

    # Assignment
    check("reassignment",
        'int x = 10; x = x + 32; print(x);', "42")

    # If / else
    check("if true branch",
        'int x = 10; if (x > 5) { print(x); }', "10")
    check("if false skips",
        'int x = 3; if (x > 5) { print(x); }', "")
    check("if-else true",
        'int x = 10; if (x > 5) { print(1); } else { print(0); }', "1")
    check("if-else false",
        'int x = 1; if (x > 5) { print(1); } else { print(0); }', "0")

    # While loop
    check("while loop count",
        'int x = 0; int s = 0; while (x < 5) { s = s + x; x = x + 1; } print(s);',
        "10")

    # Functions
    check("function call",
        'func add(a, b) { return a + b; } int r = add(20, 22); print(r);', "42")
    check("function multiple calls",
        'func double(n) { return n + n; } int a = double(5); int b = double(a); print(b);',
        "20")

    # Comparisons
    check("equal true",
        'int x = 5; int y = 5; int r = x == y; print(r);', "1")
    check("equal false",
        'int x = 5; int y = 6; int r = x == y; print(r);', "0")
    check("less than true",
        'int x = 3; int y = 5; int r = x < y; print(r);', "1")

    print(f"\n  {'=' * 40}")
    print(f"  Result: {passed}/{total} tests passed")
    if passed == total:
        print("  [ALL PASSED]")
    else:
        print(f"  [{total - passed} FAILED]")


if __name__ == "__main__":
    main()
