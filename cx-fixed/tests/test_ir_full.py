"""
test_ir_full.py — IR / TAC generation layer tests
"""
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.ir.generator import IRGenerator


def get_tac(source):
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    return IRGenerator().generate(ast)


def opcodes(source):
    return [i.result for i in get_tac(source)]


def check(name, source, fn):
    try:
        tac = get_tac(source)
        ok = fn(tac)
        status = "PASS" if ok else "FAIL"
    except Exception as e:
        status = "FAIL"
        print(f"  [FAIL]  {name}  =>  {e}")
        return False
    print(f"  [{status}]  {name}")
    return status == "PASS"


def main():
    print("\nIR / TAC GENERATION LAYER TESTS")
    print("=" * 50)

    passed = 0
    total = 0

    def run(name, src, fn):
        nonlocal passed, total
        total += 1
        if check(name, src, fn): passed += 1

    run("simple assignment",
        "int x = 5;",
        lambda t: t[0].result == "x" and t[0].arg1 == 5)

    run("binary expr generates temp",
        "int z = 1 + 2;",
        lambda t: any(i.operator == "+" for i in t))

    run("print generates PRINT opcode",
        "int x = 1; print(x);",
        lambda t: any(i.result == "PRINT" for i in t))

    run("if generates IF_FALSE",
        "int x = 5; if (x > 0) { print(x); }",
        lambda t: any(i.result == "IF_FALSE" for i in t))

    run("if generates GOTO",
        "int x = 5; if (x > 0) { print(x); }",
        lambda t: any(i.result == "GOTO" for i in t))

    run("if generates two LABELs",
        "int x = 5; if (x > 0) { print(x); }",
        lambda t: sum(1 for i in t if i.result == "LABEL") == 2)

    run("while generates LABEL at start",
        "int x = 0; while (x < 3) { x = x + 1; }",
        lambda t: any(i.result == "LABEL" for i in t))

    run("while generates IF_FALSE",
        "int x = 0; while (x < 3) { x = x + 1; }",
        lambda t: any(i.result == "IF_FALSE" for i in t))

    run("func declaration generates FUNC",
        "func f(a) { return a; }",
        lambda t: t[0].result == "FUNC" and t[0].arg1 == "f")

    run("func declaration generates END_FUNC",
        "func f(a) { return a; }",
        lambda t: any(i.result == "END_FUNC" for i in t))

    run("return generates RETURN",
        "func f(a) { return a; }",
        lambda t: any(i.result == "RETURN" for i in t))

    run("function call generates CALL",
        "func f(a) { return a; } int r = f(1);",
        lambda t: any(i.result == "CALL" for i in t))

    run("string literal in TAC",
        'string s = "hello"; print(s);',
        lambda t: t[0].arg1 == '"hello"')

    print(f"\n  {'=' * 40}")
    print(f"  Result: {passed}/{total} tests passed")
    if passed == total:
        print("  [ALL PASSED]")


if __name__ == "__main__":
    main()
