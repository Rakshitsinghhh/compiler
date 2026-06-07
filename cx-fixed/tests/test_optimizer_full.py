"""
test_optimizer_full.py — optimizer / constant folding tests
"""
from src.parser.ast_nodes import IntegerLiteral, BinaryExpression, Identifier
from src.optimizer.constant_fold import ConstantFolder


def fold(node):
    return ConstantFolder().optimize(node)


def binop(left, op, right):
    return BinaryExpression(IntegerLiteral(left), op, IntegerLiteral(right))


def check(name, node, expected_type, expected_value=None):
    result = fold(node)
    type_ok = isinstance(result, expected_type)
    val_ok = (expected_value is None) or (result.value == expected_value)
    ok = type_ok and val_ok
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}]  {name}")
    if not ok:
        print(f"         expected type={expected_type.__name__} val={expected_value}")
        print(f"         got     type={type(result).__name__} val={getattr(result,'value',None)}")
    return ok


def main():
    print("\nOPTIMIZER / CONSTANT FOLDING TESTS")
    print("=" * 50)

    passed = 0
    total = 0

    def run(name, node, etype, evalue=None):
        nonlocal passed, total
        total += 1
        if check(name, node, etype, evalue): passed += 1

    run("fold 10 + 20",      binop(10,"+",20), IntegerLiteral, 30)
    run("fold 50 - 8",       binop(50,"-",8),  IntegerLiteral, 42)
    run("fold 6 * 7",        binop(6,"*",7),   IntegerLiteral, 42)
    run("fold 84 / 2",       binop(84,"/",2),  IntegerLiteral, 42)
    run("fold 0 + 0",        binop(0,"+",0),   IntegerLiteral, 0)
    run("fold nested (2+3)*4",
        BinaryExpression(binop(2,"+",3), "*", IntegerLiteral(4)),
        IntegerLiteral, 20)

    # Non-constant — should stay as BinaryExpression
    mixed = BinaryExpression(Identifier("x"), "+", IntegerLiteral(1))
    result = fold(mixed)
    ok = isinstance(result, BinaryExpression)
    total += 1
    if ok:
        passed += 1
    print(f"  {'[PASS]' if ok else '[FAIL]'}  non-constant stays as BinaryExpression")

    # Identifier — unchanged
    ident = Identifier("x")
    result = fold(ident)
    ok = isinstance(result, Identifier)
    total += 1
    if ok:
        passed += 1
    print(f"  {'[PASS]' if ok else '[FAIL]'}  identifier passes through unchanged")

    print(f"\n  {'=' * 40}")
    print(f"  Result: {passed}/{total} tests passed")
    if passed == total:
        print("  [ALL PASSED]")


if __name__ == "__main__":
    main()
