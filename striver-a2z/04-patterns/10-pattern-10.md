---
module: striver-a2z/04-patterns
lesson: 10
topic: Pattern 10 — Half Diamond
source: https://takeuforward.org/learning/dsa/pattern-10?category=patterns&source=strivers-a2z-dsa-sheet
tags: [striver, patterns, nested-loops]
---
# 10. Pattern 10: Half Diamond

← [Pattern 9: Diamond](09-pattern-9.md) · [Part 4 index](README.md) · Next → [Pattern 11: Binary Number Triangle](11-pattern-11.md)

> [!abstract] What this covers
> **Core idea:** One loop over 2n − 1 rows; stars = i ≤ n ? i : 2n − i (= n − |n − i|).
> **Shape:** stars rise 1 → n then fall back to 1.
> **Source:** [takeuforward lesson](https://takeuforward.org/learning/dsa/pattern-10?category=patterns&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Output](#1-output) · [2. Row table](#2-row-table) · [3. Derivation](#3-derivation) · [4. Code](#4-code) · [5. Complexity](#5-complexity) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Flashcards](#flashcards)

---

## 1. Output

n = 5:
```text
*
* *
* * *
* * * *
* * * * *
* * * *
* * *
* *
*
```

n = 3 (use this for dry runs):
```text
*
* *
* * *
* *
*
```

Cells are separated by a space, as in Striver's reference output.

---

## 2. Row table

Row table for n = 5 (1-based rows):

| Row i | Stars |
|---|---|
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 4 |
| 5 | 5 |
| 6 | 4 |
| 7 | 3 |
| 8 | 2 |
| 9 | 1 |
| **Formula** | **i ≤ n ? i : 2n − i** |

---

## 3. Derivation

You *could* write pattern 2 then pattern 5 minus its first row. The single-loop version is cleaner: a **piecewise bound**. The closed form `n − |n − i|` is the absolute-value trick from [Part 3 Hard §2](../03-logic-building-patterns/02-hard.md#2-composition-stacking-shapes).

---

## 4. Code

**C++**
```cpp
void pattern10(int n) {
    for (int i = 1; i <= 2 * n - 1; i++) {
        int stars = (i <= n) ? i : 2 * n - i;
        for (int j = 0; j < stars; j++) cout << "* ";
        cout << '\n';
    }
}
```

**Java**
```java
static void pattern10(int n) {
    for (int i = 1; i <= 2 * n - 1; i++) {
        int stars = (i <= n) ? i : 2 * n - i;
        for (int j = 0; j < stars; j++) System.out.print("* ");
        System.out.println();
    }
}
```

**Python**
```python
def pattern10(n):
    for i in range(1, 2 * n):
        stars = n - abs(n - i)
        print("* " * stars)
```

---

## 5. Complexity

| | |
|---|---|
| Time | O(n²) — proportional to the O(n²) characters printed |
| Extra space | O(1) in C++/Java; O(n) per row in Python (the row string is built before printing) |

**Edge cases:** n = 1 → one `*`.

---

## Common mistakes

1. Looping to 2n → an extra empty row (2n − 2n = 0 stars).
2. `2n − i + 1` in the bottom half → the widest row is printed twice.

---

## Practice

Centred half diamond (a full diamond of 2n − 1 rows).

<details><summary>Answer sketch</summary>

Spaces |n − i|, stars 2(n − |n − i|) − 1.
</details>

---

## Flashcards

**Stars in row i of the half diamond?** #flashcard
i ≤ n ? i : 2n − i, i.e. n − |n − i|.

**How many rows?** #flashcard
2n − 1.

**Interview track →** [How to Think](../../03-patterns/HOW_TO_THINK.md) · [Part 3: pattern method](../03-logic-building-patterns/README.md)
