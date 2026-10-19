---
module: striver/29-tries
lesson: 7
topic: Maximum XOR with an element from the array
difficulty: Hard
source: https://takeuforward.org/learning/dsa/maximum-xor-with-an-element-from-an-array?category=problems&source=strivers-a2z-dsa-sheet
tags: [striver, tries, trie, bit-manipulation, offline-queries, sorting]
---
# 7. Maximum XOR with an element from the array

← [Maximum XOR of two numbers in an array](06-maximum-xor-of-two-numbers-in-an-array.md) · [Part 29 index](README.md) · Next → [Part 30: Strings (Advanced)](../30-strings-advanced/README.md)

> [!abstract] Problem at a glance
> **Task:** For each query `(x, m)`: max `x XOR a` over `a ≤ m` in `nums`, else −1.
> **Key insight:** The `a ≤ m` filter changes per query, so answer the queries **offline**. Sort `nums` ascending and the queries by `m`. Sweep: before each query, insert every `nums` value `≤ m` into the binary trie. The trie then holds exactly the allowed set, and a normal max-XOR query answers it.
> **Difficulty:** Hard · **Pattern:** Offline queries + binary trie · **Also on:** [LC 1707](https://leetcode.com/problems/maximum-xor-with-an-element-from-array/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/maximum-xor-with-an-element-from-an-array?category=problems&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Per-query scan](#3-per-query-scan) · [4. Offline sort + binary trie sweep](#4-offline-sort--binary-trie-sweep) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `nums` and `queries[i] = [x_i, m_i]`, answer each query with the maximum of `x_i XOR nums[j]` over all `j` with `nums[j] ≤ m_i`, or `-1` if every `nums[j] > m_i`.

| Input | Output | Why |
|---|---|---|
| `nums=[0,1,2,3,4], q=[[3,1],[1,3],[5,6]]` | `[3,3,7]` | 3^0, 1^2, 5^2 |
| `nums=[5,2,4,6,6,3], q=[[12,4],[8,1],[6,3]]` | `[15,-1,5]` | no a ≤ 1 |

**Constraints:** `1 ≤ n, q ≤ 10⁵`, `0 ≤ nums[j], x_i, m_i ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Per-query scan | for each query, loop all nums ≤ m | O(n·q) | O(1) |
| Offline sort + binary trie sweep | sort queries by m; insert nums ≤ m before answering | O((n + q) log + 31(n + q)) | O(31·n) |

> [!tip] Interview angle
> Say **offline** early: queries can be reordered as long as the answers go back to their original indices. Sort queries by `m` with their index, sweep a pointer over sorted `nums`, then run the max-XOR query. The online alternative (store the subtree minimum in each node and refuse children whose min `> m`) is a good follow-up.

---

## 3. Per-query scan

**Intuition.** For each query, scan all of `nums`, filter by `≤ m` and take the max XOR. 10¹⁰ operations at the limits.

```python
def maximize_xor_brute(nums, queries):
    return [max((x ^ a for a in nums if a <= m), default=-1) for x, m in queries]
```

**Complexity:** time **O(n·q)**, space **O(1)**.

---

## 4. Offline sort + binary trie sweep

**Intuition.** Sorting both lists means each `nums` value is inserted once, in order, and before any query whose limit admits it. If nothing has been inserted yet, the answer is −1.

**Algorithm**

1. Sort `nums`. Make `(m, x, idx)` for each query and sort by `m`.
2. Pointer `p = 0`. For each query: while `p < n` and `nums[p] ≤ m`, insert `nums[p++]`.
3. If `p == 0`, `ans[idx] = −1`; else `ans[idx] = maxXor(x)` (greedy opposite bit).
4. Return `ans` in the original order.

**Dry run** — nums [0,1,2,3,4]; queries sorted by m: (1,x=3) inserts 0,1 → 3^0 = 3; (3,x=1) inserts 2,3 → 1^2 = 3; (6,x=5) inserts 4 → 5^2 = 7.

**C++**
```cpp
vector<int> maximizeXor(vector<int>& nums, vector<vector<int>>& queries) {
    sort(nums.begin(), nums.end());
    int q = queries.size();
    vector<int> ord(q), ans(q, -1);
    iota(ord.begin(), ord.end(), 0);
    sort(ord.begin(), ord.end(), [&](int a, int b) { return queries[a][1] < queries[b][1]; });
    vector<array<int, 2>> t(1, {0, 0});
    int p = 0;
    for (int qi : ord) {
        int x = queries[qi][0], m = queries[qi][1];
        while (p < (int)nums.size() && nums[p] <= m) {
            int n = 0;
            for (int b = 30; b >= 0; b--) {
                int bit = (nums[p] >> b) & 1;
                if (!t[n][bit]) { t[n][bit] = t.size(); t.push_back({0, 0}); }
                n = t[n][bit];
            }
            p++;
        }
        if (p == 0) continue;
        int n = 0, cur = 0;
        for (int b = 30; b >= 0; b--) {
            int want = ((x >> b) & 1) ^ 1;
            if (t[n][want]) { cur |= 1 << b; n = t[n][want]; }
            else n = t[n][want ^ 1];
        }
        ans[qi] = cur;
    }
    return ans;
}
```

**Java**
```java
static int[] maximizeXor(int[] nums, int[][] queries) {
    Arrays.sort(nums);
    int q = queries.length;
    Integer[] ord = new Integer[q];
    for (int i = 0; i < q; i++) ord[i] = i;
    Arrays.sort(ord, (a, b) -> Integer.compare(queries[a][1], queries[b][1]));
    int[] ans = new int[q];
    Arrays.fill(ans, -1);
    int[][] t = new int[31 * nums.length + 1][2];
    int sz = 1, p = 0;
    for (int qi : ord) {
        int x = queries[qi][0], m = queries[qi][1];
        while (p < nums.length && nums[p] <= m) {
            int n = 0;
            for (int b = 30; b >= 0; b--) {
                int bit = (nums[p] >> b) & 1;
                if (t[n][bit] == 0) t[n][bit] = sz++;
                n = t[n][bit];
            }
            p++;
        }
        if (p == 0) continue;
        int n = 0, cur = 0;
        for (int b = 30; b >= 0; b--) {
            int want = ((x >> b) & 1) ^ 1;
            if (t[n][want] != 0) { cur |= 1 << b; n = t[n][want]; }
            else n = t[n][want ^ 1];
        }
        ans[qi] = cur;
    }
    return ans;
}
```

**Python**
```python
def maximize_xor(nums, queries):
    nums = sorted(nums)
    order = sorted(range(len(queries)), key=lambda i: queries[i][1])
    ans = [-1] * len(queries)
    t, p = [[0, 0]], 0
    for qi in order:
        x, m = queries[qi]
        while p < len(nums) and nums[p] <= m:
            n = 0
            for b in range(30, -1, -1):
                bit = (nums[p] >> b) & 1
                if not t[n][bit]:
                    t[n][bit] = len(t)
                    t.append([0, 0])
                n = t[n][bit]
            p += 1
        if p == 0:
            continue
        n = cur = 0
        for b in range(30, -1, -1):
            want = ((x >> b) & 1) ^ 1
            if t[n][want]:
                cur |= 1 << b
                n = t[n][want]
            else:
                n = t[n][want ^ 1]
        ans[qi] = cur
    return ans
```

**Complexity:** time **O((n + q) log + 31(n + q))**, space **O(31·n)** — two sorts plus 31 steps per insert and per query.

---

## Edge cases

- Every `nums[j] > m` → −1 (nothing inserted yet).
- Duplicate `m` values: the sweep handles them naturally.
- Answers must go back to the original query order.

---

## Common mistakes

1. Answering in sorted order and returning that order.
2. Rebuilding the trie per query.
3. Forgetting the −1 case when the trie is empty.

---

## Follow-ups

1. Online (queries arrive one at a time)?
2. Range constraint `l ≤ a ≤ r`?

<details><summary>Answer sketches</summary>

**#1:** Store the minimum value in each node's subtree. During the query, only follow a child whose min `≤ m`. O(31) per query.

**#2:** Persistent trie over the sorted values, or a merge-sort tree of tries.
</details>

---

## Flashcards

**Offline query trick?** #flashcard
Sort queries by their constraint, sweep data in the same order, store answers by original index.

**Max XOR with a ≤ m, online?** #flashcard
Keep the subtree minimum per trie node; skip children whose min exceeds m.

**Interview track →** [Trie deep-dive](../../01-data-structures/09-trie.md) · [Bit manipulation](../../02-algorithms/17-bit-manipulation.md) · [Trie walkthroughs](../../coding/data-structures/09-trie.md)
