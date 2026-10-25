---
module: striver-a2z/04-patterns
lesson: 6
topic: Pattern 6 — Inverted Number Triangle
source: https://takeuforward.org/learning/dsa/pattern-6?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 6. Pattern 6: Inverted Number Triangle

← [Pattern 5: Inverted Right Triangle](05-pattern-5.md) · [Part 4 index](README.md) · Next → [Pattern 7: Star Pyramid](07-pattern-7.md)

> [!abstract] What this covers
> **Core idea:** Pattern 5's shape with pattern 3's content.
> **Shape:** row i prints 1 … n − i + 1.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-6?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
1 2 3 4 5
1 2 3 4
1 2 3
1 2
1
```

n = 3 (use this for dry runs):
```text
1 2 3
1 2
1
```

Cells are separated by a space, as in Striver's reference output.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Cells | Content |
|---|---|---|
| 1 | 5 | 1 2 3 4 5 |
| 2 | 4 | 1 2 3 4 |
| 3 | 3 | 1 2 3 |
| 4 | 2 | 1 2 |
| 5 | 1 | 1 |
| **Formula** | **n − i + 1** | **j** |

---

## 3. Derivation

Shape = pattern 5 (bound `n − i + 1`), content = pattern 3 (`j`). Composition of two solved pieces — the habit Striver is building.

---

## 4. Code

**C++**
```cpp
void pattern6(int n) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n - i + 1; j++) cout << j << " ";
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern6(int n) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n - i + 1; j++) System.out.print(j + " ");
        System.out.println();
    }
}
```

**Python**
```python
def pattern6(n):
    for i in range(n, 0, -1):
        print(" ".join(str(j) for j in range(1, i + 1)))
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

1. Printing `n − j + 1` → rows read 5 4 3 …, a different pattern.

---

## Practice

Rows count down: 5 4 3 2 1, 5 4 3 2, …

<details><summary>Answer sketch</summary>

Content `n − j + 1`.
</details>

---

## Flashcards

**Pattern 6 = which shape + which content?** #flashcard
Pattern 5's shape (n − i + 1 cells) + pattern 3's content (j).

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
