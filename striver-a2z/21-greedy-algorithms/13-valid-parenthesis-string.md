---
module: striver-a2z/21-greedy-algorithms
lesson: 13
topic: Valid Parenthesis String
difficulty: Medium
source: https://takeuforward.org/learning/dsa/valid-paranthesis-checker?category=hard&source=strivers-a2z-dsa-sheet
tags: [striver, greedy-algorithms, greedy, string, parentheses, dp]
---
# 13. Valid Parenthesis String

← [Minimum Number of Platforms](12-minimum-number-of-platforms.md) · [Part 21 index](README.md) · Next → [Candy](14-candy.md)

> [!abstract] Problem at a glance
> **Task:** String of `(`, `)` and `*` where `*` can be `(`, `)` or empty — can it be a valid parenthesis string?
> **Key insight:** Track the **range** `[lo, hi]` of possible open-bracket counts. `(` shifts both up, `)` both down, `*` widens it (`lo − 1`, `hi + 1`). Fail if `hi < 0`; clamp `lo` at 0; valid iff `lo == 0` at the end.
> **Difficulty:** Medium · **Pattern:** Range of possible balances · **Also on:** [LC 678](https://leetcode.com/problems/valid-parenthesis-string/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/valid-paranthesis-checker?category=hard&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursion: try all three for *](#3-recursion-try-all-three-for-) · [4. Memoised DP on (i, balance)](#4-memoised-dp-on-i-balance) · [5. Greedy balance range](#5-greedy-balance-range) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `s` containing only `(`, `)` and `*`, return `true` if `s` is valid, where each `*` may be treated as `(`, `)` or the empty string, and a valid string has every prefix balance ≥ 0 and final balance 0.

| Input | Output | Why |
|---|---|---|
| `s = "()"` | `true` |  |
| `s = "(*)"` | `true` | * = empty |
| `s = "(*))"` | `true` | * = ( |
| `s = ")*("` | `false` |  |

**Constraints:** `1 ≤ s.length ≤ 100`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursion: try all three for * | f(i, open) branching on * | O(3ⁿ) | O(n) |
| Memoised DP on (i, balance) | dp[i][bal] | O(n²) | O(n²) |
| Greedy balance range | lo/hi of possible open counts | O(n) | O(1) |

> [!tip] Interview angle
> Show recursion (3-way branch) → memoised DP on (index, balance) → O(n) greedy range. The greedy's correctness: every balance in `[lo, hi]` is achievable, and the set stays contiguous.

---

## 3. Recursion: try all three for *

**Intuition.** Walk the string carrying the current balance. A `*` branches into +1, −1 and 0. Prune when balance < 0.

```python
def check_rec(s):
    def f(i, bal):
        if bal < 0:
            return False
        if i == len(s):
            return bal == 0
        if s[i] == '(':
            return f(i + 1, bal + 1)
        if s[i] == ')':
            return f(i + 1, bal - 1)
        return f(i + 1, bal + 1) or f(i + 1, bal - 1) or f(i + 1, bal)
    return f(0, 0)
```

**Complexity:** time **O(3ⁿ)**, space **O(n)**.

---

## 4. Memoised DP on (i, balance)

**Intuition.** The recursion has only `n × (n + 1)` distinct states. Memoise them.

```python
from functools import lru_cache

def check_dp(s):
    n = len(s)
    @lru_cache(None)
    def f(i, bal):
        if bal < 0 or bal > n - i:
            return False
        if i == n:
            return bal == 0
        if s[i] == '(':
            return f(i + 1, bal + 1)
        if s[i] == ')':
            return f(i + 1, bal - 1)
        return f(i + 1, bal + 1) or f(i + 1, bal - 1) or f(i + 1, bal)
    return f(0, 0)
```

**Complexity:** time **O(n²)**, space **O(n²)**.

---

## 5. Greedy balance range

**Intuition.** Instead of one balance, keep the interval of balances some choice of `*`s could produce. `hi` treats every `*` as `(`, `lo` treats every `*` as `)` (but never below 0, since negative branches are dead). If even the optimistic `hi` drops below 0, nothing works. At the end, 0 must be achievable: `lo == 0`.

**Algorithm**

1. `lo = hi = 0`.
2. `(`: `lo++`, `hi++`. `)`: `lo−−`, `hi−−`. `*`: `lo−−`, `hi++`.
3. If `hi < 0` return false. `lo = max(lo, 0)`.
4. Return `lo == 0`.

**Dry run** — "(*))": ( → [1,1]; * → [0,2]; ) → [0,1] (lo −1 clamped); ) → [0,0]. lo = 0 → true.

**Two-pass alternative:** left→right treating `*` as `(` must never go negative; right→left treating `*` as `)` must never go negative.

**C++**
```cpp
bool checkValidString(string s) {
    int lo = 0, hi = 0;
    for (char c : s) {
        if (c == '(') { lo++; hi++; }
        else if (c == ')') { lo--; hi--; }
        else { lo--; hi++; }
        if (hi < 0) return false;
        lo = max(lo, 0);
    }
    return lo == 0;
}
```

**Java**
```java
static boolean checkValidString(String s) {
    int lo = 0, hi = 0;
    for (char c : s.toCharArray()) {
        if (c == '(') { lo++; hi++; }
        else if (c == ')') { lo--; hi--; }
        else { lo--; hi++; }
        if (hi < 0) return false;
        lo = Math.max(lo, 0);
    }
    return lo == 0;
}
```

**Python**
```python
def check_valid_string(s):
    lo = hi = 0
    for c in s:
        if c == '(':
            lo += 1; hi += 1
        elif c == ')':
            lo -= 1; hi -= 1
        else:
            lo -= 1; hi += 1
        if hi < 0:
            return False
        lo = max(lo, 0)
    return lo == 0
```

**Complexity:** time **O(n)**, space **O(1)** — one pass, two counters.

---

## Edge cases

- Only `*`s → true.
- Leading `)` → false.
- Trailing `(` with not enough `*` after it.

---

## Common mistakes

1. Not clamping `lo` at 0 (keeps impossible negative balances).
2. Checking only `hi ≥ 0` at the end, or only counts of `(` and `)`.
3. Treating `*` greedily as one fixed character.

---

## Follow-ups

1. Return one valid assignment.
2. Minimum insertions to make plain parentheses valid (LC 921).

<details><summary>Answer sketches</summary>

**#1:** Two stacks of indices (opens, stars): match `)` with an open, else a star; at the end match remaining opens with later stars.

**#2:** Track balance; count how often it would go negative, add the final balance.
</details>

---

## Flashcards

**Valid Parenthesis String greedy?** #flashcard
Keep `[lo, hi]` of possible open counts; `*` widens both ways; fail if `hi < 0`; clamp `lo ≥ 0`; valid iff `lo == 0`.

**Why clamp lo at 0?** #flashcard
Choices that make the balance negative are already invalid; the smallest valid balance is 0.

**Interview track →** [Greedy deep-dive](../../02-algorithms/16-greedy.md) · [Greedy walkthroughs](../../04-practice/algorithms/16-greedy.md)
