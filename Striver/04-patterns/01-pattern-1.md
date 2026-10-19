---
module: striver/04-patterns
lesson: 1
topic: Pattern 1 — Square of Stars
source: https://takeuforward.org/learning/dsa/pattern-1?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 1. Pattern 1: Square of Stars

← [Part 4 index](README.md) · Next → [Pattern 2: Right-Angled Triangle](02-pattern-2.md)

> [!abstract] What this covers
> **Core idea:** Both loops run a fixed n times — the inner bound does not depend on i.
> **Shape:** n × n grid of stars.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-1?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
* * * * *
* * * * *
* * * * *
* * * * *
* * * * *
```

n = 3 (use this for dry runs):
```text
* * *
* * *
* * *
```

Cells are separated by a space, as in Striver's reference output.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Stars |
|---|---|
| 1 | 5 |
| 2 | 5 |
| 3 | 5 |
| 4 | 5 |
| 5 | 5 |
| **Formula** | **n** |

---

## 3. Derivation

The outer loop prints one row per iteration; the inner loop prints that row's n stars; `newline` ends the row. Nothing depends on i, which is why this is the warm-up: it isolates the **loop-inside-a-loop** structure from any formula.

---

## 4. Code

**C++**
```cpp
void pattern1(int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) cout << "* ";
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern1(int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) System.out.print("* ");
        System.out.println();
    }
}
```

**Python**
```python
def pattern1(n):
    for i in range(n):
        print("* " * n)
```

---

## 5. Complexity

| | |
|---|---|
| Time | O(n²) — proportional to the O(n²) characters printed |
| Extra space | O(1) in C++/Java; O(n) per row in Python (the row string is built before printing) |

**Edge cases:** n = 1 → a single `*`. n = 0 → no output (both loops skip).

---

## Common mistakes

1. Newline inside the inner loop → n² lines of one star.
2. Forgetting the newline → one line of n² stars.

---

## Practice

Print an n × m rectangle.

<details><summary>Answer sketch</summary>

Inner bound becomes `m`; the outer stays `n`.
</details>

---

## Flashcards

**What does the inner loop of pattern 1 depend on?** #flashcard
Nothing — it always runs n times. Total work n² prints.

**Where does the newline go?** #flashcard
After the inner loop, inside the outer loop — once per row.

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
