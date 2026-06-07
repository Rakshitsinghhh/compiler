cx-compiler/
│
├── README.md
├── requirements.txt
│
├── src/
│   ├── __init__.py
│   │
│   ├── lexer/
│   │   ├── lexer.py          # Tokenizer
│   │   ├── token.py          # Token class & TokenType enum
│   │   └── errors.py         # Lexical error types
│   │
│   ├── parser/
│   │   ├── parser.py         # Recursive descent parser
│   │   ├── ast_nodes.py      # All AST node classes
│   │   └── errors.py         # Syntax error types
│   │
│   ├── semantic/
│   │   ├── analyzer.py       # Semantic analysis visitor
│   │   ├── symbol_table.py   # Symbol table + scope manager
│   │   └── type_checker.py   # Type inference & checking
│   │
│   ├── ir/
│   │   ├── generator.py      # TAC / quad generator
│   │   ├── tac.py            # Three Address Code structures
│   │   └── quadruples.py     # Quad/triple representations
│   │
│   ├── optimizer/
│   │   ├── optimizer.py      # Optimization pipeline
│   │   ├── constant_fold.py  # Constant folding & propagation
│   │   ├── dead_code.py      # Dead code elimination
│   │   └── cse.py            # Common subexpression elimination
│   │
│   ├── codegen/
│   │   ├── generator.py      # Final code emitter
│   │   └── instructions.py   # Instruction set definition
│   │
│   └── utils/
│       ├── error_handler.py  # Unified error reporting
│       └── ast_printer.py    # Pretty-print the AST
│
├── tests/
│   ├── valid/                # .cx programs that should compile
│   ├── invalid/              # .cx programs that should error
│   └── test_*.py             # Unit tests per phase
│
├── examples/
│   ├── hello.cx
│   ├── factorial.cx
│   └── fibonacci.cx
│
└── main.py                   # Driver: glues all phases together