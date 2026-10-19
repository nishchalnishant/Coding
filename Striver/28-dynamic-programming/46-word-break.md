---
module: striver/28-dynamic-programming
lesson: 46
topic: Word break
difficulty: Medium
source: https://takeuforward.org/learning/dsa/word-break?category=dp-on-strings&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, strings, hashing]
---
# 46. Word break

← [Wildcard matching](45-wildcard-matching.md) · [Part 28 index](README.md) · Next → [Count palindromic subsequences](47-count-palindromic-subsequences.md)

> [!abstract] Problem at a glance
> **Task:** Can `s` be segmented into a sequence of dictionary words (reuse allowed)?
> **Key insight:** `dp[i]` = can the prefix `s[0..i)` be segmented? `dp[i] = OR over j < i of dp[j] ∧ s[j..i) ∈ dict`. Bound `i − j` by the maximum word length to cut the inner loop. This is unbounded-knapsack-shaped: positions are capacities and words are items.
> **Difficulty:** Medium · **Pattern:** Prefix boolean DP · **Also on:** LC 139
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/word-break?category=dp-on-strings&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized on start index](#3-memoized-on-start-index) · [4. Prefix DP with hash set](#4-prefix-dp-with-hash-set) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `s` and a list `wordDict`, return `true` if `s` can be split into one or more dictionary words (words may repeat).

| Input | Output | Why |
|---|---|---|
| `s = "leetcode", dict = ["leet","code"]` | `true` |  |
| `s = "applepenapple", dict = ["apple","pen"]` | `true` | reuse |
| `s = "catsandog", dict = ["cats","dog","sand","and","cat"]` | `false` |  |

**Constraints:** `1 ≤ |s| ≤ 300`, `1 ≤ |dict| ≤ 1000`, `1 ≤ |word| ≤ 20`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized on start index | f(i) = any word w at i with f(i + |w|) | O(n·D·L) | O(n) |
| Prefix DP with hash set | dp[i] |= dp[j] ∧ s[j..i) ∈ set | O(n·L²) | O(n + D·L) |

> [!tip] Interview angle
> Plain recursion is exponential on inputs like `"aaaa…ab"` with `["a","aa",…]`. Memoise on the start index. Mention the trie-based inner loop if the dictionary is large.

---

## 3. Memoized on start index

**Intuition.** Try each dictionary word as the next piece.

```python
def wb_memo(s, words):
    from functools import lru_cache
    @lru_cache(None)
    def f(i):
        if i == len(s):
            return True
        return any(s.startswith(w, i) and f(i + len(w)) for w in words)
    return f(0)
```

**Complexity:** time **O(n·D·L)**, space **O(n)**.

---

## 4. Prefix DP with hash set

**Intuition.** Only `j ≥ i − maxLen` can work, so the inner loop is bounded by the longest word.

**Algorithm**

1. `dp[0] = true`; `maxLen = max |w|`.
2. For `i = 1..n`: for `j = i−1` down to `max(0, i − maxLen)`: if `dp[j]` and `s[j..i)` in the set → `dp[i] = true`, break.
3. Return `dp[n]`.

**Dry run** — "leetcode": dp[4] via "leet", dp[8] via dp[4] + "code" → true.

**C++**
```cpp
bool wordBreak(string s, vector<string>& wordDict) {
    unordered_set<string> dict(wordDict.begin(), wordDict.end());
    int n = s.size(), maxLen = 0;
    for (auto& w : wordDict) maxLen = max(maxLen, (int)w.size());
    vector<bool> dp(n + 1, false);
    dp[0] = true;
    for (int i = 1; i <= n; i++)
        for (int j = i - 1; j >= max(0, i - maxLen); j--)
            if (dp[j] && dict.count(s.substr(j, i - j))) { dp[i] = true; break; }
    return dp[n];
}
```

**Java**
```java
static boolean wordBreak(String s, String[] wordDict) {
    Set<String> dict = new HashSet<>(Arrays.asList(wordDict));
    int n = s.length(), maxLen = 0;
    for (String w : wordDict) maxLen = Math.max(maxLen, w.length());
    boolean[] dp = new boolean[n + 1];
    dp[0] = true;
    for (int i = 1; i <= n; i++)
        for (int j = i - 1; j >= Math.max(0, i - maxLen); j--)
            if (dp[j] && dict.contains(s.substring(j, i))) { dp[i] = true; break; }
    return dp[n];
}
```

**Python**
```python
def word_break(s, words):
    d = set(words)
    L = max(map(len, words))
    dp = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        for j in range(i - 1, max(0, i - L) - 1, -1):
            if dp[j] and s[j:i] in d:
                dp[i] = True
                break
    return dp[-1]
```

**Complexity:** time **O(n·L²)**, space **O(n + D·L)** — n positions × L lengths × O(L) hashing.

---

## Edge cases

- Word reuse is allowed.
- A long run of the same character: memoisation is required.

---

## Common mistakes

1. Unmemoised recursion (exponential).
2. Greedy longest-match first ("cars" with car/ca/rs).

---

## Follow-ups

1. Return all sentences (LC 140)?
2. Huge dictionary?

<details><summary>Answer sketches</summary>

**#1:** Memoised DFS returning lists; output-sensitive (exponential output possible).

**#2:** Walk a trie from each `j` with `dp[j]` true, marking `dp[end]`.
</details>

---

## Flashcards

**Word break state?** #flashcard
dp[i] = prefix of length i is segmentable.

**Inner-loop bound?** #flashcard
Longest dictionary word.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
