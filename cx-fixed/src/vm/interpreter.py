"""
cx VM — stack-based interpreter for pseudo-assembly.

Registers
---------
ACC          : current working value (accumulator)
memory       : flat dict of variable names → values (global frame)
call_stack   : list of CallFrame objects (for nested function calls)
arg_queue    : list of values accumulated by PUSH_ARG before a CALL
pc           : program counter (index into instruction list)

CallFrame holds:
  - return_pc          : where to resume after RET
  - local_memory       : parameter/local bindings for this call
  - saved_acc          : ACC value from the caller (restored on RET)

FUNC_BEGIN operand encoding
---------------------------
The code generator encodes function parameters directly into the
FUNC_BEGIN instruction operand using the format:

    "funcname:param1,param2,param3"

or just:

    "funcname"   (for zero-parameter functions)

This lets the VM bind call-site arguments to parameter names without
any heuristic scanning.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


# ── Frame ────────────────────────────────────────────────────────────────────

@dataclass
class CallFrame:
    func_name: str
    return_pc: int
    local_memory: dict = field(default_factory=dict)
    saved_acc: Any = None


# ── VM ───────────────────────────────────────────────────────────────────────

class VM:

    def __init__(self, instructions, verbose=False):
        self.instructions = instructions
        self.verbose      = verbose

        # Build label → pc  and  func_name → (pc, [params]) tables
        self.label_map: dict[str, int]         = {}
        self.func_map:  dict[str, tuple]       = {}   # name → (pc, params)

        for idx, instr in enumerate(instructions):
            if instr.opcode == "LABEL":
                label_name = instr.operand.rstrip(":")
                self.label_map[label_name] = idx

            elif instr.opcode == "FUNC_BEGIN":
                # operand: "name" or "name:p1,p2,p3"
                name, params = self._parse_func_operand(instr.operand)
                self.func_map[name] = (idx, params)

        # Runtime state
        self.acc        = None
        self.memory     = {}          # global / current scope
        self.call_stack = []          # list[CallFrame]
        self.arg_queue  = []          # args collected before CALL
        self.pc         = 0

    # ── operand parsing ───────────────────────────────────────────────────────

    @staticmethod
    def _parse_func_operand(operand: str):
        """
        Parse "funcname" or "funcname:p1,p2,p3" into (name, [params]).
        """
        if ":" in operand:
            name, rest = operand.split(":", 1)
            params = [p.strip() for p in rest.split(",") if p.strip()]
        else:
            name   = operand
            params = []
        return name, params

    # ── helpers ──────────────────────────────────────────────────────────────

    def _resolve(self, operand):
        """
        Turn an operand string (or already-typed value) into a Python value.
        Tries: int literal, float literal, quoted string, bool keyword,
        then memory lookup (local scope first, then global).
        """
        if operand is None:
            return None

        # Already a Python value (e.g. integer literal stored directly)
        if not isinstance(operand, str):
            return operand

        # Quoted string literal  "hello"
        if operand.startswith('"') and operand.endswith('"'):
            return operand[1:-1]

        # Boolean keywords
        if operand == "true":
            return True
        if operand == "false":
            return False

        # Integer literal
        try:
            return int(operand)
        except ValueError:
            pass

        # Float literal
        try:
            return float(operand)
        except ValueError:
            pass

        # Variable — search local frame first, then globals
        if self.call_stack:
            local = self.call_stack[-1].local_memory
            if operand in local:
                return local[operand]

        if operand in self.memory:
            return self.memory[operand]

        raise RuntimeError(f"VM: undefined variable '{operand}'")

    def _store(self, name, value):
        """Write a value to the innermost live scope."""
        if self.call_stack:
            self.call_stack[-1].local_memory[name] = value
        else:
            self.memory[name] = value

    def _log(self, instr):
        if self.verbose:
            scope = self.call_stack[-1].local_memory if self.call_stack else self.memory
            depth = "  " * len(self.call_stack)
            print(f"{depth}[pc={self.pc:3d}] {instr}  | ACC={self.acc!r}")

    # ── main execution loop ───────────────────────────────────────────────────

    def run(self):
        while self.pc < len(self.instructions):
            instr = self.instructions[self.pc]
            self._log(instr)
            op  = instr.opcode
            arg = instr.operand      # raw string operand (may be None)

            # ── Data movement ────────────────────────────────────────────────

            if op == "MOV":
                # MOV dest, src_or_literal
                dest, src = [s.strip() for s in arg.split(",", 1)]
                self._store(dest, self._resolve(src))

            elif op == "LOAD":
                self.acc = self._resolve(arg)

            elif op == "STORE":
                self._store(arg, self.acc)

            # ── Arithmetic ───────────────────────────────────────────────────

            elif op == "ADD":
                self.acc = self.acc + self._resolve(arg)

            elif op == "SUB":
                self.acc = self.acc - self._resolve(arg)

            elif op == "MUL":
                self.acc = self.acc * self._resolve(arg)

            elif op == "DIV":
                divisor = self._resolve(arg)
                if divisor == 0:
                    raise RuntimeError("VM: division by zero")
                # Integer division when both operands are ints
                if isinstance(self.acc, int) and isinstance(divisor, int):
                    self.acc = self.acc // divisor
                else:
                    self.acc = self.acc / divisor

            # ── Comparisons (result: 1 or 0) ─────────────────────────────────

            elif op == "CMP_EQ":
                self.acc = 1 if self.acc == self._resolve(arg) else 0

            elif op == "CMP_NEQ":
                self.acc = 1 if self.acc != self._resolve(arg) else 0

            elif op == "CMP_LT":
                self.acc = 1 if self.acc < self._resolve(arg) else 0

            elif op == "CMP_GT":
                self.acc = 1 if self.acc > self._resolve(arg) else 0

            elif op == "CMP_LTE":
                self.acc = 1 if self.acc <= self._resolve(arg) else 0

            elif op == "CMP_GTE":
                self.acc = 1 if self.acc >= self._resolve(arg) else 0

            # ── Control flow ─────────────────────────────────────────────────

            elif op == "JMP":
                self.pc = self.label_map[arg]
                continue

            elif op == "JZ":
                if not self.acc:          # 0, False, or falsy
                    self.pc = self.label_map[arg]
                    continue

            elif op == "LABEL":
                pass                      # labels are no-ops at runtime

            # ── I/O ──────────────────────────────────────────────────────────

            elif op == "PRINT":
                value = self._resolve(arg) if arg else self.acc
                print(value)

            # ── Functions ────────────────────────────────────────────────────

            elif op == "FUNC_BEGIN":
                # Skip over the function body when encountered in normal flow;
                # find the matching FUNC_END and jump past it.
                depth = 1
                skip_pc = self.pc + 1
                while skip_pc < len(self.instructions):
                    s = self.instructions[skip_pc]
                    if s.opcode == "FUNC_BEGIN":
                        depth += 1
                    elif s.opcode == "FUNC_END":
                        depth -= 1
                        if depth == 0:
                            self.pc = skip_pc + 1
                            break
                    skip_pc += 1
                continue

            elif op == "FUNC_END":
                # Implicit return (void function / missing explicit return)
                if self.call_stack:
                    frame = self.call_stack.pop()
                    self.acc = frame.saved_acc
                    self.pc  = frame.return_pc
                    continue
                # Top-level FUNC_END outside a call — just move on

            elif op == "PUSH_ARG":
                self.arg_queue.append(self._resolve(arg))

            elif op == "CALL":
                # arg format: "func_name num_args"
                parts     = arg.split()
                func_name = parts[0]
                num_args  = int(parts[1])

                if func_name not in self.func_map:
                    raise RuntimeError(f"VM: undefined function '{func_name}'")

                func_pc, params = self.func_map[func_name]

                # Grab the right number of evaluated args from the queue
                call_args      = self.arg_queue[-num_args:] if num_args else []
                self.arg_queue = self.arg_queue[:-num_args] if num_args else self.arg_queue

                # Build the new call frame
                frame = CallFrame(
                    func_name    = func_name,
                    return_pc    = self.pc + 1,
                    saved_acc    = self.acc,
                    local_memory = {},
                )

                # Bind positional arguments to parameter names
                for pname, pval in zip(params, call_args):
                    frame.local_memory[pname] = pval

                self.call_stack.append(frame)
                self.pc = func_pc + 1     # step into function body
                continue

            elif op == "RET":
                # ACC already holds the return value (set by preceding LOAD)
                return_value = self.acc
                if self.call_stack:
                    frame = self.call_stack.pop()
                    self.acc = return_value      # leave return value in ACC
                    self.pc  = frame.return_pc
                    continue
                else:
                    break   # RET at top level — stop

            else:
                raise RuntimeError(f"VM: unknown opcode '{op}'")

            self.pc += 1
