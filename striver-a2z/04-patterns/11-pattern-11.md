---
module: striver-a2z/04-patterns
lesson: 11
topic: Pattern 11 — Binary Number Triangle
source: https://takeuforward.org/learning/dsa/pattern-11?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 11. Pattern 11: Binary Number Triangle

← [Pattern 10: Half Diamond](10-pattern-10.md) · [Part 4 index](README.md) · Next → [Pattern 12: Number Crown](12-pattern-12.md)

> [!abstract] What this covers
> **Core idea:** Cell (i, j) prints 1 when i + j is even, else 0 — parity of the position.
> **Shape:** 1 / 0 1 / 1 0 1 — alternating bits.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-11?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
1
0 1
1 0 1
0 1 0 1
1 0 1 0 1
```

n = 3 (use this for dry runs):
```text
1
0 1
1 0 1
```

Cells are separated by a space, as in Striver's reference output.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Cells | Starts with | Row |
|---|---|---|---|
| 1 | 1 | 1 | 1 |
| 2 | 2 | 0 | 0 1 |
| 3 | 3 | 1 | 1 0 1 |
| 4 | 4 | 0 | 0 1 0 1 |
| 5 | 5 | 1 | 1 0 1 0 1 |
| **Formula** | **i** | **i odd ? 1 : 0** | **toggle each cell** |

---

## 3. Derivation

Two equivalent views. **Toggle** (Striver's): pick the row's first bit from i's parity, then flip it each column (`bit = 1 − bit`). **Formula** (Python above): `(i + j) % 2 == 0 ? 1 : 0` — the checkerboard colour of the cell. The formula view is stateless and generalises to any checkerboard.

---

## 4. Code

**C++**
```cpp
void pattern11(int n) {
    for (int i = 1; i <= n; i++) {
        int bit = (i % 2 == 1) ? 1 : 0;          // odd rows start with 1
        for (int j = 1; j <= i; j++) {
            cout << bit << " ";
            bit = 1 - bit;                       // toggle
        }
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern11(int n) {
    for (int i = 1; i <= n; i++) {
        int bit = (i % 2 == 1) ? 1 : 0;          // odd rows start with 1
        for (int j = 1; j <= i; j++) {
            System.out.print(bit + " ");
            bit = 1 - bit;                       // toggle
        }
        System.out.println();
    }
}
```

**Python**
```python
def pattern11(n):
    for i in range(1, n + 1):
        print(" ".join("1" if (i + j) % 2 == 0 else "0" for j in range(1, i + 1)))
```

---

## 5. Complexity

| | |
|---|---|
| Time | O(n²) — proportional to the O(n²) characters printed |
| Extra space | O(1) in C++/Java; O(n) per row in Python (the row string is built before printing) |

**Edge cases:** n = 1 → `1`.

---

## Common mistakes

1. Forgetting to reset `bit` at the start of each row.
2. 0-based i, j with the 1-based formula → every bit inverted.

---

## Practice

Print a full n × n checkerboard of 1/0.

<details><summary>Answer sketch</summary>

Same formula over all j in 1..n.
</details>

---

## Flashcards

**Cell formula for the binary triangle?** #flashcard
`(i + j) % 2 == 0 ? 1 : 0` (1-based).

**How do you toggle a 0/1 variable?** #flashcard
`b = 1 − b` (or `b ^= 1`).

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
