"""
run_all_tests.py
================
Runs every test module and gives a final summary.
Usage:  python3 -m tests.run_all_tests
"""

import importlib
import sys

# All test modules in pipeline order
SUITES = [
    ("LEXER          (original)",  "tests.test_lexer"),
    ("LEXER          (full)",      "tests.test_lexer_full"),
    ("PARSER         (original)",  "tests.test_parser"),
    ("PARSER         (full)",      "tests.test_parser_full"),
    ("SEMANTIC       (original)",  "tests.test_semantic"),
    ("SEMANTIC       (if)",        "tests.test_semantic_if"),
    ("SEMANTIC       (while)",     "tests.test_semantic_while"),
    ("SEMANTIC       (full)",      "tests.test_semantic_full"),
    ("OPTIMIZER      (original)",  "tests.test_optimizer"),
    ("OPTIMIZER      (full)",      "tests.test_optimizer_full"),
    ("IR / TAC       (original)",  "tests.test_ir"),
    ("IR / TAC       (assignment)","tests.test_ir_assignment"),
    ("IR / TAC       (if)",        "tests.test_if_ir"),
    ("IR / TAC       (while)",     "tests.test_while_ir"),
    ("IR / TAC       (if-else)",   "tests.test_if_else"),
    ("IR / TAC       (full)",      "tests.test_ir_full"),
    ("CODEGEN        (original)",  "tests.test_codegen"),
    ("CODEGEN        (full)",      "tests.test_codegen_full"),
    ("PARSER CASES   (assignment)","tests.test_assignment"),
    ("PARSER CASES   (comparison)","tests.test_comparison"),
    ("PARSER CASES   (if)",        "tests.test_if"),
    ("PARSER CASES   (while)",     "tests.test_while"),
    ("PARSER CASES   (function)",  "tests.test_function"),
    ("PARSER CASES   (func call)", "tests.test_function_call"),
    ("PARSER CASES   (full)",      "tests.test_full"),
    ("VM EXECUTION   (full)",      "tests.test_vm"),
]

WIDTH = 60

def banner(text, char="="):
    print(f"\n{char * (WIDTH + 4)}")
    pad = WIDTH - len(text)
    print(f"{char}{char}  {text}{' ' * pad}  {char}{char}")
    print(f"{char * (WIDTH + 4)}")


def run_suite(label, module_name):
    banner(label, char="#")
    try:
        mod = importlib.import_module(module_name)
        if hasattr(mod, "main"):
            mod.main()
        return True
    except Exception as e:
        print(f"  [ERROR] Could not run {module_name}: {e}")
        return False


def main():
    banner("cx COMPILER — FULL TEST SUITE", char="=")
    print(f"  Running {len(SUITES)} test suite(s)...\n")

    ok_count = 0
    fail_count = 0

    for label, mod in SUITES:
        if run_suite(label, mod):
            ok_count += 1
        else:
            fail_count += 1

    banner("FINAL SUMMARY", char="=")
    print(f"  Suites run    : {len(SUITES)}")
    print(f"  Suites OK     : {ok_count}")
    print(f"  Suites errored: {fail_count}")
    if fail_count == 0:
        print("\n  ALL SUITES COMPLETED SUCCESSFULLY")
    else:
        print(f"\n  {fail_count} SUITE(S) HAD ERRORS")
    print()


if __name__ == "__main__":
    main()
