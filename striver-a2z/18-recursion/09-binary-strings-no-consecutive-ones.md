---
module: striver-a2z/18-recursion
lesson: 9
topic: Generate Binary Strings Without Consecutive 1s
difficulty: Medium
source: https://takeuforward.org/learning/dsa/generate-binary-strings-without-consecutive-1s?category=subsequence-pattern-problems&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, backtracking, string]
---
# 9. Generate Binary Strings Without Consecutive 1s

← [Count All Subsequences with Sum K](08-count-subsequences-sum-k.md) · [Part 18 index](README.md) · Next → [Combination Sum](10-combination-sum.md)

> [!abstract] Problem at a glance
> **Task:** List all binary strings of length `n` with no two adjacent 1s, in lexicographic order.
> **Key insight:** At each position you can always place `0`; place `1` only if the previous char isn't `1`. Trying `0` before `1` yields lexicographic order for free. The count is Fib(n + 2).
> **Difficulty:** Medium · **Pattern:** Constrained generation (backtracking) · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/generate-all-binary-strings/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/generate-binary-strings-without-consecutive-1s?category=subsequence-pattern-problems&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. All 2ⁿ strings, filter](#3-all-2ⁿ-strings-filter) · [4. Backtracking with last-char check](#4-backtracking-with-last-char-check) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `n`, return all binary strings of length `n` that contain no two consecutive `1`s, in increasing (lexicographic) order.

| Input | Output | Why |
|---|---|---|
| `n = 3` | `["000", "001", "010", "100", "101"]` | Fib(5) = 5 |
| `n = 2` | `["00", "01", "10"]` |  |

**Constraints:** `1 ≤ n ≤ 20`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| All 2ⁿ strings, filter | enumerate masks, reject those containing 11 | O(n · 2ⁿ) | O(n) |
| Backtracking with last-char check | always try 0; try 1 only if the previous char is 0 | O(n · Fib(n)) | O(n) |

> [!tip] Interview angle
> Simple generation question that checks pruning at the branch (don't generate `11` then filter) and that you can state the output size: strings ending in 0 extend any string, strings ending in 1 extend only those ending in 0 → Fibonacci.

---

## 3. All 2ⁿ strings, filter

**Intuition.** `mask & (mask >> 1)` is non-zero exactly when two adjacent bits are both 1. Generate masks 0 … 2ⁿ − 1 in order — already lexicographic when printed MSB-first.

```python
def no11_mask(n):
    out = []
    for m in range(1 << n):
        if m & (m >> 1) == 0:
            out.append(format(m, "0%db" % n))
    return out
```

**Complexity:** time **O(n · 2ⁿ)**, space **O(n)**.

---

## 4. Backtracking with last-char check

**Intuition.** Only valid prefixes are extended, so the work is proportional to the output. Branch order 0 then 1 gives sorted output.

**Dry run** — n = 3: 0 → 00 → 000, 001; 01 → 010; 1 → 10 → 100, 101.

**C++**
```cpp
void gen(int n, string& cur, vector<string>& out) {
    if ((int)cur.size() == n) { out.push_back(cur); return; }
    cur.push_back('0'); gen(n, cur, out); cur.pop_back();
    if (cur.empty() || cur.back() == '0') { cur.push_back('1'); gen(n, cur, out); cur.pop_back(); }
}
vector<string> generateBinaryStrings(int n) {
    vector<string> out;
    string cur;
    gen(n, cur, out);
    return out;
}
```

**Java**
```java
static void gen(int n, StringBuilder cur, List<String> out) {
    if (cur.length() == n) { out.add(cur.toString()); return; }
    cur.append('0'); gen(n, cur, out); cur.deleteCharAt(cur.length() - 1);
    if (cur.length() == 0 || cur.charAt(cur.length() - 1) == '0') {
        cur.append('1'); gen(n, cur, out); cur.deleteCharAt(cur.length() - 1);
    }
}
static List<String> generateBinaryStrings(int n) {
    List<String> out = new ArrayList<>();
    gen(n, new StringBuilder(), out);
    return out;
}
```

**Python**
```python
def generate_binary_strings(n):
    out, cur = [], []
    def gen():
        if len(cur) == n:
            out.append("".join(cur))
            return
        cur.append('0'); gen(); cur.pop()
        if not cur or cur[-1] == '0':
            cur.append('1'); gen(); cur.pop()
    gen()
    return out
```

**Complexity:** time **O(n · Fib(n))**, space **O(n)** — Fib(n + 2) leaves × O(n) copy.

---

## Edge cases

- n = 1 → `["0", "1"]`.
- Output size grows like φⁿ — 17 711 strings at n = 20.

---

## Common mistakes

1. Checking the *next* char instead of the previous.
2. Generating then filtering — 2ⁿ instead of Fib(n).
3. Trying 1 before 0 — breaks the required order.

---

## Follow-ups

1. Count only.
2. No k consecutive 1s.
3. Integers ≤ N without consecutive 1s (LC 600).

<details><summary>Answer sketches</summary>

**#1:** Fib(n + 2) — DP `end0[i] = end0 + end1`, `end1[i] = end0` of i − 1.

**#2:** Carry the current run length; allow 1 while run < k − 1.

**#3:** Digit DP over the bits of N using the Fibonacci counts.
</details>

---

## Flashcards

**Number of length-n binary strings with no 11?** #flashcard
Fib(n + 2): 2, 3, 5, 8, …

**Bit test for adjacent ones in mask m?** #flashcard
m & (m >> 1) != 0.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../04-practice/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../04-practice/algorithms/12-backtracking.md)
