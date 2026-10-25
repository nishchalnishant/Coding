---
module: striver-a2z/04-patterns
lesson: 17
topic: Pattern 17 — Alpha-Hill
source: https://takeuforward.org/learning/dsa/pattern-17?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 17. Pattern 17: Alpha-Hill

← [Pattern 16: Alpha-Ramp](16-pattern-16.md) · [Part 4 index](README.md) · Next → [Pattern 18: Alpha-Triangle](18-pattern-18.md)

> [!abstract] What this covers
> **Core idea:** Pyramid shape (n − i spaces, 2i − 1 cells) with mirrored letters: rise to the peak 'A' + i − 1, then fall.
> **Shape:** centred A / ABA / ABCBA.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-17?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
    A
   ABA
  ABCBA
 ABCDCBA
ABCDEDCBA
```

n = 3 (use this for dry runs):
```text
  A
 ABA
ABCBA
```

No separator between cells — the shape depends on exact column positions.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Spaces | Letters | Peak | Breakpoint (0-based j) |
|---|---|---|---|---|
| 1 | 4 | 1 | A | 0 |
| 2 | 3 | 3 | B | 1 |
| 3 | 2 | 5 | C | 2 |
| 4 | 1 | 7 | D | 3 |
| 5 | 0 | 9 | E | 4 |
| **Formula** | **n − i** | **2i − 1** | **'A' + i − 1** | **(2i − 1) / 2** |

---

## 3. Derivation

Shape is [pattern 7](07-pattern-7.md). Content is mirrored: increment the letter until the **breakpoint** (middle index), decrement after. Stateless alternative (Python): cell j = `'A' + (i − 1) − |i − 1 − j|`. See [Part 3 Hard §3](../03-logic-building-patterns/02-hard.md#3-mirroring-a-row).

---

## 4. Code

**C++**
```cpp
void pattern17(int n) {
    for (int i = 1; i <= n; i++) {
        for (int s = 0; s < n - i; s++) cout << ' ';
        char ch = 'A';
        int breakpoint = (2 * i - 1) / 2;
        for (int j = 0; j < 2 * i - 1; j++) {
            cout << ch;
            if (j < breakpoint) ch++; else ch--;
        }
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern17(int n) {
    for (int i = 1; i <= n; i++) {
        for (int s = 0; s < n - i; s++) System.out.print(' ');
        char ch = 'A';
        int breakpoint = (2 * i - 1) / 2;
        for (int j = 0; j < 2 * i - 1; j++) {
            System.out.print(ch);
            if (j < breakpoint) ch++; else ch--;
        }
        System.out.println();
    }
}
```

**Python**
```python
def pattern17(n):
    for i in range(1, n + 1):
        row = "".join(chr(ord("A") + (i - 1) - abs(i - 1 - j)) for j in range(2 * i - 1))
        print(" " * (n - i) + row)
```

---

## 5. Complexity

| | |
|---|---|
| Time | O(n²) — proportional to the O(n²) characters printed |
| Extra space | O(1) in C++/Java; O(n) per row in Python (the row string is built before printing) |

**Edge cases:** n = 1 → `A`.

---

## Common mistakes

1. Incrementing up to and including the breakpoint → peak printed twice (`ABCCBA`).
2. Resetting `ch` outside the outer loop → rows continue from the previous letter.

---

## Practice

Number hill: 1 / 121 / 12321.

<details><summary>Answer sketch</summary>

Same breakpoint logic with an int starting at 1.
</details>

---

## Flashcards

**Breakpoint in alpha-hill row i (0-based j)?** #flashcard
(2i − 1) / 2 — the middle index; increment before it, decrement after.

**Stateless formula for cell j?** #flashcard
'A' + (i − 1) − |i − 1 − j|.

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
