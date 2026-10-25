---
module: striver-a2z/21-greedy-algorithms
lesson: 2
topic: Assign Cookies
difficulty: Easy
source: https://takeuforward.org/learning/dsa/assign-cookies?category=easy&source=strivers-a2z-dsa-sheet
tags: [striver, greedy-algorithms, greedy, sorting, two-pointers]
---
# 2. Assign Cookies

← [Greedy Fundamentals](01-greedy-fundamentals.md) · [Part 21 index](README.md) · Next → [Lemonade Change](03-lemonade-change.md)

> [!abstract] Problem at a glance
> **Task:** Maximise the number of children whose greed `g[i]` is satisfied by a cookie of size `s[j] ≥ g[i]`, each cookie used once.
> **Key insight:** Sort both. Give each cookie, smallest first, to the least greedy unsatisfied child it can satisfy — a small cookie that fits the least greedy child is never better spent elsewhere.
> **Difficulty:** Easy · **Pattern:** Sort + two pointers (match smallest feasible) · **Also on:** [LC 455](https://leetcode.com/problems/assign-cookies/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/assign-cookies?category=easy&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force: best cookie per child](#3-brute-force-best-cookie-per-child) · [4. Sort + two pointers](#4-sort--two-pointers) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Child `i` has greed factor `g[i]`; cookie `j` has size `s[j]`. A child is content if given one cookie with `s[j] ≥ g[i]`. Each child gets at most one cookie. Return the maximum number of content children.

| Input | Output | Why |
|---|---|---|
| `g = [1,2,3], s = [1,1]` | `1` | only the child with greed 1 |
| `g = [1,2], s = [1,2,3]` | `2` |  |

**Constraints:** `1 ≤ g.length ≤ 3·10⁴`, `0 ≤ s.length ≤ 3·10⁴`, `1 ≤ g[i], s[j] ≤ 2³¹ − 1`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force: best cookie per child | for each child scan for smallest unused fitting cookie | O(n·m) | O(m) |
| Sort + two pointers | advance cookie always, child when fed | O(n log n + m log m) | O(1) extra |

> [!tip] Interview angle
> The opener for greedy: the interviewer wants the sort and a one-line **exchange argument** — if an optimal solution feeds the least greedy child a bigger cookie, swapping in the smallest feasible cookie keeps it optimal.

---

## 3. Brute force: best cookie per child

**Intuition.** Process children from least greedy; for each, scan all cookies for the smallest unused one that fits. Correct (same greedy choice) but the scan makes it quadratic.

```python
def assign_brute(g, s):
    used = [False] * len(s)
    count = 0
    for child in sorted(g):
        best = -1
        for j, c in enumerate(s):
            if not used[j] and c >= child and (best == -1 or c < s[best]):
                best = j
        if best != -1:
            used[best] = True
            count += 1
    return count
```

**Complexity:** time **O(n·m)**, space **O(m)**.

---

## 4. Sort + two pointers

**Intuition.** Sort greed and sizes. Pointer `l` on cookies, `r` on children. If cookie `s[l]` satisfies child `g[r]`, feed them and advance `r`. Either way advance `l` — a cookie too small for the least greedy remaining child is too small for everyone.

**Algorithm**

1. Sort `g` and `s`.
2. `l = r = 0`.
3. While `l < len(s)` and `r < len(g)`: if `s[l] ≥ g[r]`, `r += 1`; always `l += 1`.
4. Return `r`.

**Dry run** — g = [1,2,3], s = [1,1]: s[0]=1 ≥ g[0]=1 → r=1; s[1]=1 < g[1]=2 → skip. Answer 1.

**C++**
```cpp
int findContentChildren(vector<int>& g, vector<int>& s) {
    sort(g.begin(), g.end());
    sort(s.begin(), s.end());
    int r = 0;
    for (int l = 0; l < (int)s.size() && r < (int)g.size(); l++)
        if (s[l] >= g[r]) r++;
    return r;
}
```

**Java**
```java
static int findContentChildren(int[] g, int[] s) {
    Arrays.sort(g);
    Arrays.sort(s);
    int r = 0;
    for (int l = 0; l < s.length && r < g.length; l++)
        if (s[l] >= g[r]) r++;
    return r;
}
```

**Python**
```python
def find_content_children(g, s):
    g.sort(); s.sort()
    r = 0
    for c in s:
        if r < len(g) and c >= g[r]:
            r += 1
    return r
```

**Complexity:** time **O(n log n + m log m)**, space **O(1) extra** — sorting dominates; the merge-style scan is linear.

---

## Edge cases

- No cookies → 0.
- All cookies too small → 0.
- Duplicate greed values.

---

## Common mistakes

1. Advancing the child pointer when the cookie is too small (should discard the cookie).
2. Greedily giving the **largest** cookie to the least greedy child — wastes big cookies.
3. Forgetting to sort one of the arrays.

---

## Follow-ups

1. Each child can take several cookies until satisfied.
2. Maximise total satisfaction weight.

<details><summary>Answer sketches</summary>

**#1:** Becomes a bin-covering problem — no simple greedy; NP-hard in general.

**#2:** Weighted bipartite matching — greedy no longer optimal.
</details>

---

## Flashcards

**Assign Cookies greedy rule?** #flashcard
Sort both; give the smallest cookie that fits to the least greedy child; discard cookies that fit nobody.

**Exchange argument in one sentence?** #flashcard
Any optimal solution can be transformed, swap by swap, into the greedy one without getting worse.

**Interview track →** [Greedy deep-dive](../../02-algorithms/16-greedy.md) · [Greedy walkthroughs](../../04-practice/algorithms/16-greedy.md)
