---
module: striver/04-patterns
lesson: 14
topic: Pattern 14 — Letter Triangle
source: https://takeuforward.org/learning/dsa/pattern-14?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 14. Pattern 14: Letter Triangle

← [Pattern 13: Increasing Number Triangle](13-pattern-13.md) · [Part 4 index](README.md) · Next → [Pattern 15: Reverse Letter Triangle](15-pattern-15.md)

> [!abstract] What this covers
> **Core idea:** Pattern 3 with letters: cell j prints 'A' + j.
> **Shape:** A / A B / A B C.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-14?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
A
A B
A B C
A B C D
A B C D E
```

n = 3 (use this for dry runs):
```text
A
A B
A B C
```

Cells are separated by a space, as in Striver's reference output.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Cells | Letters |
|---|---|---|
| 1 | 1 | A |
| 2 | 2 | A B |
| 3 | 3 | A B C |
| 4 | 4 | A B C D |
| 5 | 5 | A B C D E |
| **Formula** | **i** | **'A' … 'A' + i − 1** |

---

## 3. Derivation

Characters are small integers (`'A'` = 65), so a `char` can be the loop variable itself. In C++/Java `'A' + j` is an **int**; loop over a `char` (as above) or cast `(char)('A' + j)`. Python needs `chr(ord('A') + j)`.

---

## 4. Code

**C++**
```cpp
void pattern14(int n) {
    for (int i = 1; i <= n; i++) {
        for (char ch = 'A'; ch < 'A' + i; ch++) cout << ch << " ";
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern14(int n) {
    for (int i = 1; i <= n; i++) {
        for (char ch = 'A'; ch < 'A' + i; ch++) System.out.print(ch + " ");
        System.out.println();
    }
}
```

**Python**
```python
def pattern14(n):
    for i in range(1, n + 1):
        print(" ".join(chr(ord("A") + j) for j in range(i)))
```

---

## 5. Complexity

| | |
|---|---|
| Time | O(n²) — proportional to the O(n²) characters printed |
| Extra space | O(1) in C++/Java; O(n) per row in Python (the row string is built before printing) |

**Edge cases:** n ≤ 26 for single letters; beyond that you run into `[`, `\`, … (ASCII 91+).

---

## Common mistakes

1. `cout << 'A' + j` prints 65, 66 … (int arithmetic).
2. Java: `ch + ' '` adds two chars → an int. Use `ch + " "`.

---

## Practice

Lowercase letters.

<details><summary>Answer sketch</summary>

Start from `'a'` (97).
</details>

---

## Flashcards

**Why does `cout << 'A' + 1` print 66?** #flashcard
char + int promotes to int. Cast back with `(char)`.

**Python: next letter after c?** #flashcard
`chr(ord(c) + 1)`.

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
