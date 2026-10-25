---
module: striver-a2z/18-recursion
lesson: 3
topic: Generate Parentheses
difficulty: Medium
source: https://takeuforward.org/learning/dsa/generate-parentheses?category=implementation-problems&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, backtracking, string]
---
# 3. Generate Parentheses

← [Pow(x, n)](02-pow-x-n.md) · [Part 18 index](README.md) · Next → [Power Set](04-power-set.md)

> [!abstract] Problem at a glance
> **Task:** Generate every well-formed string of `n` pairs of parentheses.
> **Key insight:** Build left to right and only make legal moves: add `(` while `open < n`, add `)` while `close < open`. Every leaf is then valid — no filtering. The count is the n-th Catalan number.
> **Difficulty:** Medium · **Pattern:** Backtracking with constraints · **Also on:** [LC 22](https://leetcode.com/problems/generate-parentheses/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/generate-parentheses?category=implementation-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Generate all, then validate](#3-generate-all-then-validate) · [4. Backtracking on open/close counts](#4-backtracking-on-openclose-counts) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `n`, return all combinations of `n` pairs of well-formed parentheses, in any order.

| Input | Output | Why |
|---|---|---|
| `n = 3` | `["((()))", "(()())", "(())()", "()(())", "()()()"]` | C₃ = 5 |
| `n = 1` | `["()"]` |  |

**Constraints:** `1 ≤ n ≤ 8`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Generate all, then validate | 2^(2n) strings, keep balanced ones | O(2²ⁿ · n) | O(n) recursion |
| Backtracking on open/close counts | '(' if open < n; ')' if close < open | O(4ⁿ / √n) | O(n) recursion + output |

> [!tip] Interview angle
> Standard backtracking check. Start with the brute (generate 2²ⁿ, validate) to show you see the search space, then prune. Be ready to state the output size: Catalan Cₙ = (2n choose n)/(n + 1) ≈ 4ⁿ / (n^1.5 √π).

---

## 3. Generate all, then validate

**Intuition.** Recursively append either bracket until length 2n, then check balance with a counter. Explores many dead strings like `))((`.

```python
def gen_brute(n):
    out = []
    def valid(s):
        d = 0
        for c in s:
            d += 1 if c == '(' else -1
            if d < 0:
                return False
        return d == 0
    def go(cur):
        if len(cur) == 2 * n:
            if valid(cur):
                out.append(cur)
            return
        go(cur + '(')
        go(cur + ')')
    go("")
    return out
```

**Complexity:** time **O(2²ⁿ · n)**, space **O(n) recursion**.

---

## 4. Backtracking on open/close counts

**Intuition.** A prefix can be completed into a valid string iff `close ≤ open ≤ n`. Enforcing that at every step means every recursion path ends at a valid string, so work ≈ output size × n.

**Dry run** — n = 2: `(` → `((` → `(()` → `(())` ✓; back to `(` → `()` → `()(` → `()()` ✓.

**C++**
```cpp
void build(int n, int open, int close, string& cur, vector<string>& out) {
    if ((int)cur.size() == 2 * n) { out.push_back(cur); return; }
    if (open < n) { cur.push_back('('); build(n, open + 1, close, cur, out); cur.pop_back(); }
    if (close < open) { cur.push_back(')'); build(n, open, close + 1, cur, out); cur.pop_back(); }
}
vector<string> generateParenthesis(int n) {
    vector<string> out;
    string cur;
    build(n, 0, 0, cur, out);
    return out;
}
```

**Java**
```java
static void build(int n, int open, int close, StringBuilder cur, List<String> out) {
    if (cur.length() == 2 * n) { out.add(cur.toString()); return; }
    if (open < n) { cur.append('('); build(n, open + 1, close, cur, out); cur.deleteCharAt(cur.length() - 1); }
    if (close < open) { cur.append(')'); build(n, open, close + 1, cur, out); cur.deleteCharAt(cur.length() - 1); }
}
static List<String> generateParenthesis(int n) {
    List<String> out = new ArrayList<>();
    build(n, 0, 0, new StringBuilder(), out);
    return out;
}
```

**Python**
```python
def generate_parenthesis(n):
    out, cur = [], []
    def build(open_, close):
        if len(cur) == 2 * n:
            out.append("".join(cur))
            return
        if open_ < n:
            cur.append('(')
            build(open_ + 1, close)
            cur.pop()
        if close < open_:
            cur.append(')')
            build(open_, close + 1)
            cur.pop()
    build(0, 0)
    return out
```

**Complexity:** time **O(4ⁿ / √n)**, space **O(n) recursion + output** — Cₙ leaves, each copied in O(n); the bound is Catalan · n.

---

## Edge cases

- n = 1.
- Output grows as Catalan: 1, 2, 5, 14, 42, 132, 429, 1430.

---

## Common mistakes

1. Allowing `)` when `close == open` — produces invalid prefixes.
2. String concatenation in each call (fine in Python, O(n) copies in Java) vs one shared builder with backtracking.
3. Forgetting to undo (`pop_back`) after the recursive call.

---

## Follow-ups

1. Count only (no list).
2. Multiple bracket types.
3. Generate in lexicographic order.

<details><summary>Answer sketches</summary>

**#1:** Catalan number: `C(2n, n) / (n + 1)` or DP `C[i] = Σ C[j]·C[i−1−j]`.

**#2:** Track a stack of open types; a close must match the top.

**#3:** Try `(` before `)` — the backtracking above already does (since `(` < `)` in ASCII).
</details>

---

## Flashcards

**Generate parentheses pruning rule?** #flashcard
Add ( while open < n; add ) while close < open.

**Number of valid strings with n pairs?** #flashcard
Catalan Cₙ = C(2n, n)/(n + 1).

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../04-practice/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../04-practice/algorithms/12-backtracking.md)
