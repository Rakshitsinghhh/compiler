"""
test_codegen_full.py — code generation layer tests
"""
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.ir.generator import IRGenerator
from src.codegen.generator import CodeGenerator


def get_asm(source):
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    tac = IRGenerator().generate(ast)
    return CodeGenerator().generate(tac)


def opcodes(source):
    return [i.opcode for i in get_asm(source)]


def check(name, source, fn):
    try:
        asm = get_asm(source)
        ok = fn(asm)
        status = "PASS" if ok else "FAIL"
    except Exception as e:
        status = "FAIL"
        print(f"  [FAIL]  {name}  =>  {e}")
        return False
    print(f"  [{status}]  {name}")
    return status == "PASS"


def main():
    print("\nCODE GENERATION LAYER TESTS")
    print("=" * 50)

    passed = 0
    total = 0

    def run(name, src, fn):
        nonlocal passed, total
        total += 1
        if check(name, src, fn): passed += 1

    run("simple MOV for int decl",
        "int x = 10;",
        lambda a: a[0].opcode == "MOV" and "x" in a[0].operand)

    run("ADD instruction for +",
        "int z = 1 + 2;",
        lambda a: any(i.opcode == "ADD" for i in a))

    run("SUB instruction for -",
        "int z = 5 - 3;",
        lambda a: any(i.opcode == "SUB" for i in a))

    run("MUL instruction for *",
        "int z = 3 * 4;",
        lambda a: any(i.opcode == "MUL" for i in a))

    run("LOAD before arithmetic",
        "int z = 1 + 2;",
        lambda a: any(i.opcode == "LOAD" for i in a))

    run("STORE after arithmetic",
        "int z = 1 + 2;",
        lambda a: any(i.opcode == "STORE" for i in a))

    run("PRINT opcode generated",
        "int x = 5; print(x);",
        lambda a: any(i.opcode == "PRINT" for i in a))

    run("JZ for if condition",
        "int x = 5; if (x > 0) { print(x); }",
        lambda a: any(i.opcode == "JZ" for i in a))

    run("JMP for if end",
        "int x = 5; if (x > 0) { print(x); }",
        lambda a: any(i.opcode == "JMP" for i in a))

    run("LABEL opcode present",
        "int x = 5; if (x > 0) { print(x); }",
        lambda a: any(i.opcode == "LABEL" for i in a))

    run("FUNC_BEGIN for function",
        "func f(a) { return a; }",
        lambda a: any(i.opcode == "FUNC_BEGIN" for i in a))

    run("FUNC_END for function",
        "func f(a) { return a; }",
        lambda a: any(i.opcode == "FUNC_END" for i in a))

    run("RET for return",
        "func f(a) { return a; }",
        lambda a: any(i.opcode == "RET" for i in a))

    run("CALL opcode for function call",
        "func f(a) { return a; } int r = f(5);",
        lambda a: any(i.opcode == "CALL" for i in a))

    run("CMP_LT for less-than",
        "int x = 3; int y = 5; int r = x < y;",
        lambda a: any(i.opcode == "CMP_LT" for i in a))

    run("CMP_EQ for equality",
        "int x = 5; int y = 5; int r = x == y;",
        lambda a: any(i.opcode == "CMP_EQ" for i in a))

    print(f"\n  {'=' * 40}")
    print(f"  Result: {passed}/{total} tests passed")
    if passed == total:
        print("  [ALL PASSED]")


if __name__ == "__main__":
    main()
