"""
test_lexer_full.py — comprehensive lexer layer tests
"""
from src.lexer.lexer import Lexer
from src.lexer.token import TokenType


def check(name, source, expected_types):
    tokens = Lexer(source).tokenize()
    actual = [t.type for t in tokens if t.type != TokenType.EOF]
    status = "PASS" if actual == expected_types else "FAIL"
    print(f"  [{status}]  {name}")
    if status == "FAIL":
        print(f"         expected: {[t.name for t in expected_types]}")
        print(f"         got:      {[t.name for t in actual]}")
    return status == "PASS"


def main():
    print("\nLEXER LAYER TESTS")
    print("=" * 50)

    passed = 0
    total = 0

    def run(name, src, types):
        nonlocal passed, total
        total += 1
        if check(name, src, types):
            passed += 1

    TT = TokenType

    run("integer literal",   "42;",      [TT.INTEGER, TT.SEMICOLON])
    run("float literal",     "3.14;",    [TT.FLOAT,   TT.SEMICOLON])
    run("string literal",    '"hi";',    [TT.STRING,  TT.SEMICOLON])
    run("bool true",         "true;",    [TT.BOOLEAN, TT.SEMICOLON])
    run("bool false",        "false;",   [TT.BOOLEAN, TT.SEMICOLON])
    run("identifier",        "myVar;",   [TT.IDENTIFIER, TT.SEMICOLON])
    run("int keyword",       "int x;",   [TT.INT, TT.IDENTIFIER, TT.SEMICOLON])
    run("float keyword",     "float f;", [TT.FLOAT_TYPE, TT.IDENTIFIER, TT.SEMICOLON])
    run("if keyword",        "if",       [TT.IF])
    run("else keyword",      "else",     [TT.ELSE])
    run("while keyword",     "while",    [TT.WHILE])
    run("func keyword",      "func",     [TT.FUNC])
    run("return keyword",    "return",   [TT.RETURN])
    run("print keyword",     "print",    [TT.PRINT])
    run("plus",              "a + b;",   [TT.IDENTIFIER, TT.PLUS, TT.IDENTIFIER, TT.SEMICOLON])
    run("minus",             "a - b;",   [TT.IDENTIFIER, TT.MINUS, TT.IDENTIFIER, TT.SEMICOLON])
    run("multiply",          "a * b;",   [TT.IDENTIFIER, TT.MULTIPLY, TT.IDENTIFIER, TT.SEMICOLON])
    run("divide",            "a / b;",   [TT.IDENTIFIER, TT.DIVIDE, TT.IDENTIFIER, TT.SEMICOLON])
    run("assign",            "x = 1;",   [TT.IDENTIFIER, TT.ASSIGN, TT.INTEGER, TT.SEMICOLON])
    run("equal ==",          "x == y;",  [TT.IDENTIFIER, TT.EQUAL, TT.IDENTIFIER, TT.SEMICOLON])
    run("not equal !=",      "x != y;",  [TT.IDENTIFIER, TT.NOT_EQUAL, TT.IDENTIFIER, TT.SEMICOLON])
    run("less than <",       "x < y;",   [TT.IDENTIFIER, TT.LESS_THAN, TT.IDENTIFIER, TT.SEMICOLON])
    run("greater than >",    "x > y;",   [TT.IDENTIFIER, TT.GREATER_THAN, TT.IDENTIFIER, TT.SEMICOLON])
    run("less equal <=",     "x <= y;",  [TT.IDENTIFIER, TT.LESS_EQUAL, TT.IDENTIFIER, TT.SEMICOLON])
    run("greater equal >=",  "x >= y;",  [TT.IDENTIFIER, TT.GREATER_EQUAL, TT.IDENTIFIER, TT.SEMICOLON])
    run("parens",            "(x)",      [TT.LPAREN, TT.IDENTIFIER, TT.RPAREN])
    run("braces",            "{x}",      [TT.LBRACE, TT.IDENTIFIER, TT.RBRACE])
    run("comma",             "a, b",     [TT.IDENTIFIER, TT.COMMA, TT.IDENTIFIER])
    run("comment skipped",   "// hi\nint x;", [TT.INT, TT.IDENTIFIER, TT.SEMICOLON])

    print(f"\n  {'=' * 40}")
    print(f"  Result: {passed}/{total} tests passed")
    if passed == total:
        print("  [ALL PASSED]")


if __name__ == "__main__":
    main()
