# cx Compiler

A complete compiler + virtual machine for **cx**, a small statically-typed language, written entirely in Python. The pipeline takes `.cx` source all the way through to execution with no external dependencies.

```
.cx source
   │
   ▼  Lexer          → token stream
   ▼  Parser         → AST
   ▼  Semantic Analyzer → type / scope checks
   ▼  Optimizer      → constant folding
   ▼  IR Generator   → Three-Address Code (TAC)
   ▼  Code Generator → pseudo-assembly
   ▼  VM / Interpreter → actual output
```

---

## Requirements

- **Python 3.10+** (uses `match`-free code; works on 3.8+ in practice)
- No third-party packages required to compile or run `.cx` files
- `pytest` is optional — only needed to run the test suite

---

## Installation

```bash
# 1. Clone or unzip the project
git clone <repo-url> cx-fixed
cd cx-fixed

# 2. (Optional) create a virtual environment
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# 3. (Optional) install pytest for running tests
pip install pytest
```

That's it. There are no other dependencies.

---

## The cx Language

### Types

| Keyword  | Example                    |
|----------|----------------------------|
| `int`    | `int x = 42;`              |
| `float`  | `float pi = 3.14;`         |
| `string` | `string name = "Alice";`   |
| `bool`   | — (true / false literals)  |

### Operators

`+`  `-`  `*`  `/`  `==`  `!=`  `<`  `>`  `<=`  `>=`

### Control flow

```cx
// if / else
if (x > 10) {
    print(x);
} else {
    print(0);
}

// while
while (i < 5) {
    i = i + 1;
}
```

### Functions

```cx
func add(a, b) {
    return a + b;
}

int result = add(3, 7);
print(result);           // prints 10
```

### Comments

```cx
// this is a single-line comment
```

### Full example

```cx
func factorial(n) {
    if (n <= 1) {
        return 1;
    }
    int rest = factorial(n - 1);
    return n * rest;
}

int r = factorial(5);
print(r);   // 120
```

---

## Usage

All commands are run from the **project root** (`cx-fixed/`).

### Compile and execute a file

```bash
python3 main.py --run examples/hello.cx
```

### Show the full compilation pipeline (TAC + assembly)

```bash
python3 main.py examples/hello.cx
```

Output:
```
THREE ADDRESS CODE
========================================
x = 10
y = 20
t1 = x + y
z = t1
PRINT z

ASSEMBLY
========================================
MOV x, 10
MOV y, 20
LOAD x
ADD y
STORE t1
MOV z, t1
LOAD z
PRINT
```

### Show TAC only

```bash
python3 main.py --tac examples/hello.cx
```

### Show assembly only

```bash
python3 main.py --asm examples/hello.cx
```

### Execute with a step-by-step trace

```bash
python3 main.py --run --verbose examples/hello.cx
```

Output (indented by call depth):
```
EXECUTION TRACE
========================================
[pc=  0] MOV x, 10  | ACC=None
[pc=  1] MOV y, 20  | ACC=None
[pc=  2] LOAD x     | ACC=None
[pc=  3] ADD y      | ACC=10
[pc=  4] STORE t1   | ACC=30
...
30
```

### Interactive mode

```bash
python3 main.py --run
# Enter cx code, finish with two blank lines
```

---

## Running the tests

Each test file is a standalone script. Run them from the project root:

```bash
# Run a single test
python3 -m tests.test_lexer
python3 -m tests.test_parser
python3 -m tests.test_codegen

# Run all tests at once
for mod in tests/test_*.py; do
    python3 -m "${mod%.py}" | tr '/' '.'
done
```

Or with pytest (auto-discovers any `pytest`-style tests added in future):

```bash
pip install pytest
python3 -m pytest tests/ -v
```

### What each test covers

| File | What it tests |
|------|--------------|
| `test_lexer.py` | Tokenizes a mixed program; checks token count and EOF |
| `test_parser.py` | Parses `x = x + 1` and pretty-prints the AST |
| `test_full.py` | Parses a program with funcs, if, and while; asserts no crash |
| `test_function.py` | Parses a two-parameter function; checks name + param list |
| `test_function_call.py` | Parses a function call expression |
| `test_assignment.py` | Parses a variable assignment statement |
| `test_if.py` | Parses an if statement |
| `test_if_else.py` | Generates TAC + ASM for if/else; checks label output |
| `test_while.py` | Parses a while statement |
| `test_ir.py` | Generates TAC for a function call; checks CALL instruction |
| `test_ir_assignment.py` | Generates TAC for `x = x + 1` |
| `test_if_ir.py` | Generates TAC for an if; checks JMP/label shape |
| `test_while_ir.py` | Generates TAC for a while; checks loop labels |
| `test_codegen.py` | Generates ASM for `int x = 10 + 20`; checks instructions |
| `test_comparison.py` | Parses a comparison expression |
| `test_semantic.py` | Runs semantic analysis on valid code; asserts no error |
| `test_semantic_if.py` | Semantic analysis on an if statement |
| `test_semantic_while.py` | Semantic analysis on a while loop |
| `test_optimizer.py` | Constant-folds `10 + 20` → `IntegerLiteral(30)` |

---

## Project structure

```
cx-fixed/
├── main.py                   # Entry point — CLI flags, pipeline wiring
│
├── examples/
│   ├── hello.cx              # int arithmetic + print
│   ├── fibonacci.cx          # function call (n + 1)
│   └── lang.cx               # variables + if/else
│
├── src/
│   ├── lexer/
│   │   ├── lexer.py          # Converts source text → token list
│   │   ├── token.py          # Token and TokenType definitions
│   │   └── errors.py         # LexerError
│   │
│   ├── parser/
│   │   ├── parser.py         # Recursive-descent parser → AST
│   │   ├── ast_nodes.py      # AST node classes (Program, IfStatement, …)
│   │   └── errors.py         # ParseError
│   │
│   ├── semantic/
│   │   ├── analyzer.py       # Type checking + scope validation (visitor)
│   │   ├── symbol_table.py   # Scoped symbol table (stack of dicts)
│   │   ├── type_checker.py   # (reserved for future type rules)
│   │   └── errors.py         # SemanticError
│   │
│   ├── optimizer/
│   │   ├── optimizer.py      # Runs all optimization passes in order
│   │   ├── constant_fold.py  # Folds int literal expressions at compile time
│   │   ├── cse.py            # (reserved — common subexpression elimination)
│   │   └── dead_code.py      # (reserved — dead code elimination)
│   │
│   ├── ir/
│   │   ├── generator.py      # AST → Three-Address Code instructions
│   │   └── tac.py            # TACInstruction data class + __str__
│   │
│   ├── codegen/
│   │   ├── generator.py      # TAC → pseudo-assembly Instruction list
│   │   └── instructions.py   # Instruction(opcode, operand) data class
│   │
│   └── vm/
│       └── interpreter.py    # Executes the pseudo-assembly instruction list
│
└── tests/
    └── test_*.py             # Per-stage test scripts (see table above)
```

---

## How each stage works

### 1 · Lexer (`src/lexer/lexer.py`)

Reads the source character by character, skipping whitespace and `//` comments, and emits a flat list of `Token(type, value, line, col)` objects. Keywords (`int`, `while`, `func`, …) are matched from a dict; everything else is classified as `IDENTIFIER`, `INTEGER`, `FLOAT`, `STRING`, or a punctuation token.

### 2 · Parser (`src/parser/parser.py`)

A hand-written recursive-descent parser. Each grammar rule is a method (`parse_statement`, `parse_expression`, `parse_if`, …). It consumes the token list and builds an AST made of the node types in `ast_nodes.py`. Operator precedence for arithmetic is handled by splitting expression parsing into `parse_expression` → `parse_comparison` → `parse_additive` → `parse_multiplicative` → `parse_primary`.

### 3 · Semantic Analyzer (`src/semantic/analyzer.py`)

A visitor that walks the AST. It checks:
- Variables are declared before use
- Function names are declared before call sites
- Types match in binary expressions (`any` is used for parameters, which can match anything)
- No double-declaration in the same scope

Uses a `SymbolTable` that is a stack of dicts — each function body gets a fresh scope pushed on entry and popped on exit.

### 4 · Optimizer (`src/optimizer/`)

Currently runs one pass: **constant folding**. If both sides of a `BinaryExpression` are `IntegerLiteral` nodes, the expression is replaced with a single `IntegerLiteral` at compile time. For example, `int x = 10 + 20` becomes `MOV x, 30` in the output with no addition at runtime.

Two further passes — CSE and dead-code elimination — are stubbed out for future work.

### 5 · IR Generator (`src/ir/generator.py`)

Converts the (possibly optimized) AST into **Three-Address Code** (TAC). Each TAC instruction has four fields: `result`, `arg1`, `operator`, `arg2`. Temporaries (`t1`, `t2`, …) and labels (`L1`, `L2`, …) are generated with monotonically increasing counters.

Key conventions:
- `ARG val` — emitted once per argument before every `CALL`, in order
- `CALL func n` — calls `func` with `n` arguments; result lands in a fresh temporary
- `FUNC name(p1,p2)` — marks the start of a function definition with its parameter list encoded directly in the instruction

### 6 · Code Generator (`src/codegen/generator.py`)

A straight-line TAC → assembly lowering. Each TAC instruction maps to one or a few assembly `Instruction(opcode, operand)` objects. The key translation rules:

| TAC | Assembly |
|-----|----------|
| `t1 = a + b` | `LOAD a` / `ADD b` / `STORE t1` |
| `PRINT x` | `LOAD x` / `PRINT` |
| `IF_FALSE t1 GOTO L1` | `LOAD t1` / `JZ L1` |
| `FUNC add(a,b)` | `FUNC_BEGIN add:a,b` |
| `ARG 10` | `PUSH_ARG 10` |
| `CALL add 2` | `CALL add 2` / `STORE result` |
| `RETURN t1` | `LOAD t1` / `RET` |

Parameter names are encoded into the `FUNC_BEGIN` operand as `"funcname:p1,p2"` so the VM can bind arguments to names without heuristics.

### 7 · VM (`src/vm/interpreter.py`)

A fetch-decode-execute loop over the instruction list. It maintains:

| Register | Purpose |
|----------|---------|
| `ACC` | Current working value (accumulator) |
| `memory` | Global variable store (dict) |
| `call_stack` | Stack of `CallFrame` objects |
| `arg_queue` | Staging area for `PUSH_ARG` values before a `CALL` |
| `pc` | Program counter |

Each `CallFrame` holds `local_memory` (parameters + locals), `return_pc` (where to resume after `RET`), and `saved_acc` (caller's ACC value, which is restored on function exit).

When the VM hits a `FUNC_BEGIN` during normal execution (not via `CALL`), it scans forward to the matching `FUNC_END` and skips past it — function bodies only execute when explicitly called.

When a `CALL` executes, the VM reads the parameter list from the `FUNC_BEGIN` operand (e.g. `add:a,b`), pops the right number of values from `arg_queue`, and binds them positionally into a new `CallFrame`. Recursive calls work naturally because each invocation gets its own frame.

Variable resolution always checks the innermost `CallFrame.local_memory` first, then falls back to `memory` (globals) — so function locals and parameters correctly shadow global names.
