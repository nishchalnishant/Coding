---
module: striver-a2z/23-stack-and-queues
lesson: 28
topic: The Celebrity Problem
difficulty: Medium
source: https://takeuforward.org/learning/dsa/celebrity-problem?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, two-pointers, graph]
---
# 28. The Celebrity Problem

← [Stock span problem](27-stock-span-problem.md) · [Part 23 index](README.md) · Next → [LRU Cache](29-lru-cache.md)

> [!abstract] Problem at a glance
> **Task:** Find the person everyone knows but who knows nobody.
> **Key insight:** One query `knows(a, b)` **eliminates one person**: if `a` knows `b`, `a` isn't the celebrity; otherwise `b` isn't. So n − 1 queries leave one candidate. Then verify it with 2(n − 1) queries, because a celebrity might not exist.
> **Difficulty:** Medium · **Pattern:** Elimination (stack / two pointers) · **Also on:** [LC 277](https://leetcode.com/problems/find-the-celebrity/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/celebrity-problem?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. In-degree / out-degree](#3-in-degree--out-degree) · [4. Single-candidate elimination](#4-single-candidate-elimination) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `n × n` matrix `M` where `M[i][j] = 1` means person `i` knows `j`, return the celebrity's index (known by all others, knows no one else), or `-1`.

| Input | Output | Why |
|---|---|---|
| `M = [[0,1,0],[0,0,0],[0,1,0]]` | `1` | 0 and 2 know 1; 1 knows nobody |
| `M = [[0,1],[1,0]]` | `-1` |  |

**Constraints:** `1 ≤ n ≤ 3000`; diagonal entries are 0.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| In-degree / out-degree | count knows-me and I-know for everyone | O(n²) | O(n) |
| Single-candidate elimination | candidate = i whenever candidate knows i; then verify | O(n) | O(1) |

> [!tip] Interview angle
> The eliminate-one-per-query argument is what they want. The classic presentation pushes everyone onto a stack and pops two at a time; the single-candidate loop is the same idea without the stack. Don't skip verification.

---

## 3. In-degree / out-degree

**Intuition.** The celebrity has in-degree `n − 1` and out-degree 0.

```python
def celeb_brute(M):
    n = len(M)
    for c in range(n):
        if all(M[c][j] == 0 for j in range(n) if j != c) and all(M[i][c] == 1 for i in range(n) if i != c):
            return c
    return -1
```

**Complexity:** time **O(n²)**, space **O(n)**.

---

## 4. Single-candidate elimination

**Intuition.** Scan `i = 1…n−1`: if `cand` knows `i`, `cand` is out and `i` becomes the candidate. Otherwise `i` is out (someone doesn't know them). Everyone except the final `cand` was eliminated, so only `cand` can be the celebrity.

**Algorithm**

1. `cand = 0`. For `i = 1…n−1`: if `M[cand][i]`, `cand = i`.
2. Verify: for every `i ≠ cand`, `M[cand][i] == 0` and `M[i][cand] == 1`.
3. Return `cand` or −1.

**Dry run** — [[0,1,0],[0,0,0],[0,1,0]]: cand 0; 0 knows 1 → cand 1; 1 doesn't know 2 → stays 1. Verify: 1 knows nobody, 0 and 2 know 1 → 1.

**C++**
```cpp
int celebrity(vector<vector<int>> M) {
    int n = M.size(), cand = 0;
    for (int i = 1; i < n; i++)
        if (M[cand][i]) cand = i;
    for (int i = 0; i < n; i++)
        if (i != cand && (M[cand][i] || !M[i][cand])) return -1;
    return cand;
}
```

**Java**
```java
static int celebrity(int[][] M) {
    int n = M.length, cand = 0;
    for (int i = 1; i < n; i++)
        if (M[cand][i] == 1) cand = i;
    for (int i = 0; i < n; i++)
        if (i != cand && (M[cand][i] == 1 || M[i][cand] == 0)) return -1;
    return cand;
}
```

**Python**
```python
def celebrity(M):
    n, cand = len(M), 0
    for i in range(1, n):
        if M[cand][i]:
            cand = i
    for i in range(n):
        if i != cand and (M[cand][i] or not M[i][cand]):
            return -1
    return cand
```

**Complexity:** time **O(n)**, space **O(1)** — n − 1 elimination queries plus 2(n − 1) verification queries.

---

## Edge cases

- n = 1: that person is trivially the celebrity.
- No celebrity: verification catches it.
- Mutual acquaintances.

---

## Common mistakes

1. Returning the candidate without verifying.
2. Checking the diagonal (`M[c][c]`) during verification.
3. Assuming the loop's candidate never needs to be checked against people before it: those were eliminated by queries *from* earlier candidates, not by checking whether they know the final candidate.

---

## Follow-ups

1. Why is verification needed?
2. Stack version?

<details><summary>Answer sketches</summary>

**#1:** Elimination only proves nobody *else* can be the celebrity; it doesn't prove the candidate is.

**#2:** Push all; pop two, push back the one that survives `knows`; verify the last one. Same O(n), O(n) space.
</details>

---

## Flashcards

**Celebrity problem: what does one knows(a, b) query tell you?** #flashcard
If a knows b, a is out; otherwise b is out.

**Celebrity problem: total queries in the optimal approach?** #flashcard
≈ 3(n − 1): n − 1 to eliminate, 2(n − 1) to verify.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
