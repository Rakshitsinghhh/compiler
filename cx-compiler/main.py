#!/usr/bin/env python3
"""
cx-compiler — main entry point

Usage:
  python3 main.py <source_file.cx>               # show TAC + assembly
  python3 main.py --tac  <source_file.cx>         # TAC only
  python3 main.py --asm  <source_file.cx>         # assembly only
  python3 main.py --run  <source_file.cx>         # compile AND execute
  python3 main.py --run --verbose <source_file>   # execute with trace
"""

import sys

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.optimizer.optimizer import Optimizer
from src.ir.generator import IRGenerator
from src.codegen.generator import CodeGenerator
from src.vm.interpreter import VM


def compile_source(source: str, show_tac=True, show_asm=True):

    # ── 1. Lex ───────────────────────────────────────────
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    # ── 2. Parse ─────────────────────────────────────────
    parser = Parser(tokens)
    ast = parser.parse()

    # ── 3. Semantic analysis ─────────────────────────────
    analyzer = SemanticAnalyzer()
    analyzer.visit(ast)

    # ── 4. Optimize (constant folding) ───────────────────
    optimizer = Optimizer()
    ast = optimizer.optimize(ast)

    # ── 5. IR generation (TAC) ───────────────────────────
    ir_gen = IRGenerator()
    tac = ir_gen.generate(ast)

    if show_tac:
        print("\nTHREE ADDRESS CODE")
        print("=" * 40)
        for instr in tac:
            print(instr)

    # ── 6. Code generation ───────────────────────────────
    codegen = CodeGenerator()
    asm = codegen.generate(tac)

    if show_asm:
        print("\nASSEMBLY")
        print("=" * 40)
        for instr in asm:
            print(instr)

    return tac, asm


def run_source(source: str, verbose=False):
    """Full pipeline: compile then execute via VM."""

    # ── 1-4. Same front-end as compile_source ────────────
    lexer  = Lexer(source)
    tokens = lexer.tokenize()
    ast    = Parser(tokens).parse()
    SemanticAnalyzer().visit(ast)
    ast    = Optimizer().optimize(ast)

    # ── 5. IR ────────────────────────────────────────────
    tac = IRGenerator().generate(ast)

    # ── 6. Code gen ──────────────────────────────────────
    asm = CodeGenerator().generate(tac)

    # ── 7. Execute ───────────────────────────────────────
    if verbose:
        print("\nEXECUTION TRACE")
        print("=" * 40)

    vm = VM(asm, verbose=verbose)
    vm.run()


def main():
    args = sys.argv[1:]

    run_mode  = False
    verbose   = False
    show_tac  = True
    show_asm  = True

    if "--run" in args:
        args.remove("--run")
        run_mode = True

    if "--verbose" in args:
        args.remove("--verbose")
        verbose = True

    if "--tac" in args:
        args.remove("--tac")
        show_asm = False

    if "--asm" in args:
        args.remove("--asm")
        show_tac = False

    if not args:
        print("cx compiler — interactive mode (Ctrl-C to quit)")
        mode_hint = "execute" if run_mode else "compile"
        print(f"Enter your cx program to {mode_hint} (end with two blank lines):\n")
        lines = []
        blank = 0
        try:
            while True:
                line = input()
                if line == "":
                    blank += 1
                    if blank >= 2:
                        break
                else:
                    blank = 0
                lines.append(line)
        except (KeyboardInterrupt, EOFError):
            pass
        source = "\n".join(lines)
    else:
        filepath = args[0]
        try:
            with open(filepath) as f:
                source = f.read()
        except FileNotFoundError:
            print(f"Error: file '{filepath}' not found.")
            sys.exit(1)

    try:
        if run_mode:
            run_source(source, verbose=verbose)
        else:
            compile_source(source, show_tac=show_tac, show_asm=show_asm)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
