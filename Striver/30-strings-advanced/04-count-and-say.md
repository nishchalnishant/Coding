---
module: striver/30-strings-advanced
lesson: 4
topic: Count and say
difficulty: Medium
source: https://takeuforward.org/learning/dsa/count-and-say?category=medium-problems&source=strivers-a2z-dsa-sheet
tags: [striver, strings--advanced-algo, string, simulation]
---
# 4. Count and say

← [Minimum number of bracket reversals to balance an expression](03-minimum-number-of-bracket-reversals-to-balance-an-expression.md) · [Part 30 index](README.md) · Next → [Rabin-Karp algorithm](05-rabin-karp-algorithm.md)

> [!abstract] Problem at a glance
> **Task:** Return the n-th term of the count-and-say sequence (`1, 11, 21, 1211, …`).
> **Key insight:** Each term is the **run-length encoding** of the previous one, read aloud: for every maximal block of equal digits, write its length, then the digit. Iterate `n − 1` times. Term lengths grow about 30% per step (Conway's constant ≈ 1.3036), so n stays small.
> **Difficulty:** Medium · **Pattern:** Simulation with run-length encoding · **Also on:** [LC 38](https://leetcode.com/problems/count-and-say/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-and-say?category=medium-problems&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursion](#3-recursion) · [4. Iterative run-length encoding](#4-iterative-run-length-encoding) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`countAndSay(1) = "1"`. `countAndSay(n)` is the run-length encoding of `countAndSay(n − 1)`: for each run of equal digits, append the run's count followed by the digit.

| Input | Output | Why |
|---|---|---|
| `1` | `"1"` |  |
| `4` | `"1211"` | 1 → 11 → 21 → 1211 |
| `5` | `"111221"` | 1211 = one 1, one 2, two 1s |

**Constraints:** `1 ≤ n ≤ 30`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursion | say(n) = encode(say(n − 1)) | O(Σ term lengths) | O(n) stack + term length |
| Iterative run-length encoding | repeat the encode step n − 1 times | O(Σ term lengths) | O(term length) |

> [!tip] Interview angle
> Write the run-length step as a helper and loop it. The only real bug risk is the last run: either flush it after the loop or use the inner-`while` form below, which has no flush. Use a builder, not string `+=`, in Java.

---

## 3. Recursion

**Intuition.** Directly follows the definition. Fine for n ≤ 30, but the iterative loop is just as short and has no stack.

```python
def count_and_say_rec(n):
    if n == 1:
        return "1"
    prev, out, i = count_and_say_rec(n - 1), [], 0
    while i < len(prev):
        j = i
        while j < len(prev) and prev[j] == prev[i]:
            j += 1
        out.append(str(j - i) + prev[i])
        i = j
    return "".join(out)
```

**Complexity:** time **O(Σ term lengths)**, space **O(n) stack + term length**.

---

## 4. Iterative run-length encoding

**Intuition.** Start from `"1"`. For each step, walk the current term with `i`, extend `j` over the run of `s[i]`, and append `(j − i)` and `s[i]`.

**Algorithm**

1. `s = "1"`.
2. Repeat `n − 1` times: `t = ""`; `i = 0`; while `i < |s|`: `j = i`; advance `j` while `s[j] == s[i]`; `t += str(j − i) + s[i]`; `i = j`.
3. `s = t`; finally return `s`.

**Dry run** — 21 → run '2' (1) → "12", run '1' (1) → "1211". 1211 → 11, 12, 21 → "111221".

**C++**
```cpp
string countAndSay(int n) {
    string s = "1";
    for (int k = 1; k < n; k++) {
        string t;
        for (int i = 0; i < (int)s.size(); ) {
            int j = i;
            while (j < (int)s.size() && s[j] == s[i]) j++;
            t += to_string(j - i);
            t += s[i];
            i = j;
        }
        s = t;
    }
    return s;
}
```

**Java**
```java
static String countAndSay(int n) {
    String s = "1";
    for (int k = 1; k < n; k++) {
        StringBuilder t = new StringBuilder();
        for (int i = 0; i < s.length(); ) {
            int j = i;
            while (j < s.length() && s.charAt(j) == s.charAt(i)) j++;
            t.append(j - i).append(s.charAt(i));
            i = j;
        }
        s = t.toString();
    }
    return s;
}
```

**Python**
```python
def count_and_say(n):
    s = "1"
    for _ in range(n - 1):
        t, i = [], 0
        while i < len(s):
            j = i
            while j < len(s) and s[j] == s[i]:
                j += 1
            t.append(str(j - i) + s[i])
            i = j
        s = "".join(t)
    return s
```

**Complexity:** time **O(Σ term lengths)**, space **O(term length)** — each term is produced in time linear in its length; the terms grow geometrically, so the last one dominates.

---

## Edge cases

- n = 1 returns "1" without looping.
- No digit above 3 ever appears (a known property).

---

## Common mistakes

1. Forgetting to emit the final run.
2. Appending the digit before the count.
3. Appending an int to a C++ string with `+=` (it appends a char code).

---

## Follow-ups

1. Run-length encode an arbitrary string (LC 443)?
2. Why don't digits above 3 appear?

<details><summary>Answer sketches</summary>

**#1:** Same scan, writing in place with a write pointer; counts can be multi-digit.

**#2:** A run of four equal digits `dddd` would require the previous term to contain `d d` read as two separate runs of the same digit, which run-length encoding never produces.
</details>

---

## Flashcards

**Count and say step?** #flashcard
Run-length encode the previous term: count then digit for each run.

**Count and say growth?** #flashcard
About ×1.30 per term (Conway's constant).

**Interview track →** [String algorithms deep-dive](../../02-algorithms/02-string-algorithms.md) · [String algorithm walkthroughs](../../coding/algorithms/02-string-algorithms.md)
