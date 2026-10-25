---
module: striver-a2z/28-dynamic-programming
lesson: 34
topic: Longest string chain
difficulty: Medium
source: https://takeuforward.org/learning/dsa/longest-string-chain?category=lis-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, lis, string, hashing]
---
# 34. Longest string chain

← [Largest divisible subset](33-largest-divisible-subset.md) · [Part 28 index](README.md) · Next → [Longest bitonic subsequence](35-longest-bitonic-subsequence.md)

> [!abstract] Problem at a glance
> **Task:** Longest chain of words where each is the previous plus exactly one inserted character.
> **Key insight:** Sort by length, then LIS where "`a` can precede `b`" means `len(b) = len(a) + 1` and `a` is `b` with one character removed (a two-pointer check). The faster hash version: `dp[w] = 1 + max dp[w minus char i]` over all deletion positions.
> **Difficulty:** Medium · **Pattern:** LIS variant (custom compare) · **Also on:** LC 1048
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/longest-string-chain?category=lis-dp&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Sort + LIS with predecessor check](#3-sort--lis-with-predecessor-check) · [4. Sort + hash of deletions](#4-sort--hash-of-deletions) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Word `a` is a predecessor of `b` if you can insert exactly one letter anywhere in `a` (without reordering) to get `b`. Return the length of the longest word chain `w1 → w2 → …` from `words`.

| Input | Output | Why |
|---|---|---|
| `["a","b","ba","bca","bda","bdca"]` | `4` | a → ba → bda → bdca |
| `["xbc","pcxbcf","xb","cxbc","pcxbc"]` | `5` |  |
| `["abcd","dbqca"]` | `1` |  |

**Constraints:** `1 ≤ n ≤ 1000`, `1 ≤ |word| ≤ 16`, lowercase.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Sort + LIS with predecessor check | two-pointer one-insert test | O(n²·L) | O(n) |
| Sort + hash of deletions | dp[w] = 1 + max dp[w without char i] | O(n·L²) | O(n·L) |

> [!tip] Interview angle
> Present both. The LIS + `isPredecessor` form is O(n²·L) and reuses LIS directly. The hash-of-deletions form is O(n·L²) and better when n is large. Mention that sorting by length makes every predecessor appear earlier.

---

## 3. Sort + LIS with predecessor check

**Intuition.** `dp[i] = 1 + max dp[j]` over `j < i` with `isPred(words[j], words[i])`.

```python
def chain_lis(words):
    w = sorted(words, key=len)
    def is_pred(a, b):
        if len(b) != len(a) + 1:
            return False
        i = j = 0
        while j < len(b):
            if i < len(a) and a[i] == b[j]:
                i += 1
            j += 1
        return i == len(a)
    dp = [1] * len(w)
    for i in range(len(w)):
        for j in range(i):
            if is_pred(w[j], w[i]):
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

**Complexity:** time **O(n²·L)**, space **O(n)**.

---

## 4. Sort + hash of deletions

**Intuition.** Process words by length. For each, try deleting each character and look the result up in the map of already-processed words.

**Algorithm**

1. Sort by length.
2. For each `w`: `best = 1`; for each `i`: `p = w[:i] + w[i+1:]`; if `p` in `dp`, `best = max(best, dp[p] + 1)`.
3. `dp[w] = best`; track the max.

**Dry run** — a:1, b:1, ba: from a/b → 2, bca: from ba → 3, bda → 3, bdca: from bca/bda → 4.

**C++**
```cpp
int longestStrChain(vector<string>& words) {
    vector<string> w = words;
    sort(w.begin(), w.end(), [](const string& x, const string& y) { return x.size() < y.size(); });
    unordered_map<string, int> dp;
    int ans = 0;
    for (const string& s : w) {
        int best = 1;
        for (size_t i = 0; i < s.size(); i++) {
            string p = s.substr(0, i) + s.substr(i + 1);
            auto it = dp.find(p);
            if (it != dp.end()) best = max(best, it->second + 1);
        }
        dp[s] = max(dp[s], best);
        ans = max(ans, best);
    }
    return ans;
}
```

**Java**
```java
static int longestStrChain(String[] words) {
    String[] w = words.clone();
    Arrays.sort(w, (x, y) -> x.length() - y.length());
    Map<String, Integer> dp = new HashMap<>();
    int ans = 0;
    for (String s : w) {
        int best = 1;
        for (int i = 0; i < s.length(); i++) {
            String p = s.substring(0, i) + s.substring(i + 1);
            if (dp.containsKey(p)) best = Math.max(best, dp.get(p) + 1);
        }
        dp.merge(s, best, Math::max);
        ans = Math.max(ans, best);
    }
    return ans;
}
```

**Python**
```python
def longest_str_chain(words):
    dp = {}
    for w in sorted(words, key=len):
        dp[w] = max(dp.get(w, 0), 1 + max((dp.get(w[:i] + w[i + 1:], 0) for i in range(len(w))), default=0))
    return max(dp.values())
```

**Complexity:** time **O(n·L²)**, space **O(n·L)** — n words × L deletions × O(L) substring/hash.

---

## Edge cases

- Duplicates in the input: harmless with `max`.
- No chains: 1.

---

## Common mistakes

1. Not sorting by length (predecessors may appear later).
2. An `isPred` that allows reordering or more than one extra character.

---

## Follow-ups

1. Return the chain.
2. Chains where a character may be inserted or replaced?

<details><summary>Answer sketches</summary>

**#1:** Store the best predecessor per word.

**#2:** Change the predecessor test; same DP.
</details>

---

## Flashcards

**String chain = ?** #flashcard
LIS after sorting by length, with a one-insert predecessor check.

**Faster string chain?** #flashcard
Hash map; try all L deletions of each word.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
