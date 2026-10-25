---
module: striver-a2z/04-patterns
lesson: 4
topic: Pattern 4 — Row-Number Triangle
source: https://takeuforward.org/learning/dsa/pattern-4?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 4. Pattern 4: Row-Number Triangle

← [Pattern 3: Number Triangle](03-pattern-3.md) · [Part 4 index](README.md) · Next → [Pattern 5: Inverted Right Triangle](05-pattern-5.md)

> [!abstract] What this covers
> **Core idea:** Same shape as pattern 2; the cell content is the row index i.
> **Shape:** row i prints i, i times.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-4?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
1
2 2
3 3 3
4 4 4 4
5 5 5 5 5
```

n = 3 (use this for dry runs):
```text
1
2 2
3 3 3
```

Cells are separated by a space, as in Striver's reference output.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Cells | Content |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |
| 4 | 4 | 4 |
| 5 | 5 | 5 |
| **Formula** | **i** | **i** |

---

## 3. Derivation

Compare with pattern 3: identical loops, one character different (`i` vs `j`). Being able to say *which loop variable controls what* is the whole lesson.

---

## 4. Code

**C++**
```cpp
void pattern4(int n) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) cout << i << " ";
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern4(int n) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) System.out.print(i + " ");
        System.out.println();
    }
}
```

**Python**
```python
def pattern4(n):
    for i in range(1, n + 1):
        print(" ".join([str(i)] * i))
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

1. Printing `j` → pattern 3.

---

## Practice

Print row i with the value n − i + 1 (5, 4 4, 3 3 3 …).

<details><summary>Answer sketch</summary>

Content `n − i + 1`, bound unchanged.
</details>

---

## Flashcards

**Pattern 3 vs pattern 4 difference?** #flashcard
Cell content: column `j` (pattern 3) vs row `i` (pattern 4). Loops identical.

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
