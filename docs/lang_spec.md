# CX Language Specification

## Overview

CX is a simple statically-typed programming language designed for learning compiler construction.

---

## Data Types

- int
- float
- bool
- string

---

## Keywords

- int
- float
- bool
- string
- if
- else
- while
- func
- return
- print

---

## Operators

Arithmetic:
+ - * /

Comparison:
== != < > <= >=

Assignment:
=

---

## Variable Declaration

Example:

int age = 19;
string name = "Rakshit";

---

## Print Statement

print(age);

---

## If Statement

if (age >= 18) {
    print("Adult");
}

---

## If Else Statement

if (age >= 18) {
    print("Adult");
} else {
    print("Minor");
}

---

## While Loop

while (age < 25) {
    age = age + 1;
}

---

## Function

func add(int a, int b) {
    return a + b;
}

---

## Program Example

int x = 10;
int y = 20;

print(x + y);