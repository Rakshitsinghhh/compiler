"""
test_parser_full.py — parser layer tests
"""
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.parser.ast_nodes import (
    Program, VariableDeclaration, Assignment, PrintStatement,
    IfStatement, WhileStatement, FunctionDeclaration, ReturnStatement,
    FunctionCall, BinaryExpression, IntegerLiteral, Identifier,
)


def parse(source):
    return Parser(Lexer(source).tokenize()).parse()


def check(name, source, assertion_fn):
    try:
        ast = parse(source)
        ok = assertion_fn(ast)
        status = "PASS" if ok else "FAIL"
    except Exception as e:
        status = "FAIL"
        print(f"  [FAIL]  {name}  =>  Exception: {e}")
        return False
    print(f"  [{status}]  {name}")
    return status == "PASS"


def main():
    print("\nPARSER LAYER TESTS")
    print("=" * 50)

    passed = 0
    total = 0

    def run(name, src, fn):
        nonlocal passed, total
        total += 1
        if check(name, src, fn):
            passed += 1

    run("int decl",
        "int x = 10;",
        lambda a: isinstance(a.statements[0], VariableDeclaration)
                  and a.statements[0].name == "x"
                  and a.statements[0].var_type == "int")

    run("float decl",
        "float pi = 3.14;",
        lambda a: isinstance(a.statements[0], VariableDeclaration)
                  and a.statements[0].var_type == "float")

    run("assignment",
        "int x = 1; x = 2;",
        lambda a: isinstance(a.statements[1], Assignment)
                  and a.statements[1].name == "x")

    run("print statement",
        "int x = 1; print(x);",
        lambda a: isinstance(a.statements[1], PrintStatement))

    run("binary expr +",
        "int z = 1 + 2;",
        lambda a: isinstance(a.statements[0].value, BinaryExpression)
                  and a.statements[0].value.operator == "+")

    run("binary expr *",
        "int z = 3 * 4;",
        lambda a: a.statements[0].value.operator == "*")

    run("comparison <",
        "int x = 1; int y = 2; if (x < y) { print(x); }",
        lambda a: isinstance(a.statements[2], IfStatement))

    run("if no else",
        "int x = 5; if (x > 0) { print(x); }",
        lambda a: a.statements[1].else_body is None)

    run("if with else",
        "int x = 5; if (x > 0) { print(x); } else { print(0); }",
        lambda a: a.statements[1].else_body is not None)

    run("while statement",
        "int x = 0; while (x < 3) { x = x + 1; }",
        lambda a: isinstance(a.statements[1], WhileStatement))

    run("func declaration",
        "func add(a, b) { return a + b; }",
        lambda a: isinstance(a.statements[0], FunctionDeclaration)
                  and a.statements[0].name == "add"
                  and a.statements[0].parameters == ["a", "b"])

    run("func call in decl",
        "int r = add(1, 2);",
        lambda a: isinstance(a.statements[0].value, FunctionCall)
                  and a.statements[0].value.name == "add")

    run("nested expr",
        "int x = (2 + 3) * 4;",
        lambda a: isinstance(a.statements[0].value, BinaryExpression))

    run("multiple statements",
        "int a = 1; int b = 2; int c = 3;",
        lambda a: len(a.statements) == 3)

    print(f"\n  {'=' * 40}")
    print(f"  Result: {passed}/{total} tests passed")
    if passed == total:
        print("  [ALL PASSED]")


if __name__ == "__main__":
    main()
