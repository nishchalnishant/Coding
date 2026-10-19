---
module: striver/23-stack-and-queues
lesson: 19
topic: Sum of Subarray Ranges
difficulty: Medium
source: https://takeuforward.org/learning/dsa/sum-of-subarray-ranges?category=monotonic-stack&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, monotonic-stack, contribution]
---
# 19. Sum of Subarray Ranges

← [Sum of Subarray Minimums](18-sum-of-subarray-minimums.md) · [Part 23 index](README.md) · Next → [Remove K Digits](20-remove-k-digits.md)

> [!abstract] Problem at a glance
> **Task:** Sum of `max − min` over all subarrays.
> **Key insight:** Linearity: Σ(max − min) = Σ max − Σ min. Each part is a contribution sum. `arr[i]` is the max of `(i − pge)·(nge − i)` subarrays and the min of `(i − pse)·(nse − i)`, with the same strict/non-strict tie split as in Sum of Subarray Minimums.
> **Difficulty:** Medium · **Pattern:** Contribution technique × 2 · **Also on:** [LC 2104](https://leetcode.com/problems/sum-of-subarray-ranges/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/sum-of-subarray-ranges?category=monotonic-stack&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Running max and min](#3-running-max-and-min) · [4. Σ max − Σ min via monotonic stacks](#4-σ-max--σ-min-via-monotonic-stacks) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `nums`, return the sum of `max(b) − min(b)` over all contiguous subarrays `b`.

| Input | Output | Why |
|---|---|---|
| `nums = [1,2,3]` | `4` | ranges 0,0,0,1,1,2 |
| `nums = [1,3,3]` | `4` |  |
| `nums = [4,-2,-3,4,1]` | `59` |  |

**Constraints:** `1 ≤ n ≤ 1000`; `−10⁹ ≤ nums[i] ≤ 10⁹`. Follow-up: O(n).

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Running max and min | fix l, extend r, add max − min | O(n²) | O(1) |
| Σ max − Σ min via monotonic stacks | contribution as max minus contribution as min | O(n) | O(n) |

> [!tip] Interview angle
> The O(n²) running max/min is acceptable at n = 1000. The follow-up asks for O(n), which is the contribution method run twice. Note there's no modulo here, so use 64-bit.

---

## 3. Running max and min

**Intuition.** For each `l`, extend `r` while tracking the running max and min; add their difference.

```python
def ranges_brute(nums):
    total = 0
    for i in range(len(nums)):
        lo = hi = nums[i]
        for j in range(i, len(nums)):
            lo, hi = min(lo, nums[j]), max(hi, nums[j])
            total += hi - lo
    return total
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Σ max − Σ min via monotonic stacks

**Intuition.** A single helper computes `Σ x·(i − prev)·(next − i)` where prev/next are the nearest elements that 'beat' `x`. Passing a comparator selects min or max. Each call is two stack passes.

**Algorithm**

1. `sumMins`: previous strictly smaller (pop while `>`), next smaller-or-equal (pop while `≥`).
2. `sumMaxs`: same with the comparisons reversed (pop while `<` / `≤`).
3. Return `sumMaxs − sumMins`.

**Dry run** — [1,2,3]: Σmax = 1·1·1 + 2·2·1 + 3·3·1 = 14; Σmin = 1·1·3 + 2·1·2 + 3·1·1 = 10; 14 − 10 = 4.

**C++**
```cpp
long long contrib(const vector<int>& a, bool mx) {
    int n = a.size();
    vector<int> prv(n), nxt(n), st;
    auto beats = [&](int x, int y) { return mx ? x > y : x < y; };   // x strictly beats y
    for (int i = 0; i < n; i++) {
        while (!st.empty() && !beats(a[st.back()], a[i]) && a[st.back()] != a[i]) st.pop_back();
        prv[i] = st.empty() ? -1 : st.back();
        st.push_back(i);
    }
    st.clear();
    for (int i = n - 1; i >= 0; i--) {
        while (!st.empty() && !beats(a[st.back()], a[i])) st.pop_back();
        nxt[i] = st.empty() ? n : st.back();
        st.push_back(i);
    }
    long long s = 0;
    for (int i = 0; i < n; i++) s += (long long)a[i] * (i - prv[i]) * (nxt[i] - i);
    return s;
}
long long subArrayRanges(vector<int> nums) {
    return contrib(nums, true) - contrib(nums, false);
}
```

**Java**
```java
static long contrib(int[] a, boolean mx) {
    int n = a.length;
    int[] prv = new int[n], nxt = new int[n];
    Deque<Integer> st = new ArrayDeque<>();
    for (int i = 0; i < n; i++) {
        while (!st.isEmpty() && !beats(a[st.peek()], a[i], mx) && a[st.peek()] != a[i]) st.pop();
        prv[i] = st.isEmpty() ? -1 : st.peek();
        st.push(i);
    }
    st.clear();
    for (int i = n - 1; i >= 0; i--) {
        while (!st.isEmpty() && !beats(a[st.peek()], a[i], mx)) st.pop();
        nxt[i] = st.isEmpty() ? n : st.peek();
        st.push(i);
    }
    long s = 0;
    for (int i = 0; i < n; i++) s += (long) a[i] * (i - prv[i]) * (nxt[i] - i);
    return s;
}
static boolean beats(int x, int y, boolean mx) { return mx ? x > y : x < y; }
static long subArrayRanges(int[] nums) {
    return contrib(nums, true) - contrib(nums, false);
}
```

**Python**
```python
def sub_array_ranges(nums):
    n = len(nums)
    def contrib(beats):                 # beats(x, y): x strictly better than y
        prv, nxt, st = [-1] * n, [n] * n, []
        for i in range(n):              # previous strictly better
            while st and not beats(nums[st[-1]], nums[i]) and nums[st[-1]] != nums[i]:
                st.pop()
            if st:
                prv[i] = st[-1]
            st.append(i)
        st = []
        for i in range(n - 1, -1, -1):  # next better-or-equal
            while st and not beats(nums[st[-1]], nums[i]):
                st.pop()
            if st:
                nxt[i] = st[-1]
            st.append(i)
        return sum(nums[i] * (i - prv[i]) * (nxt[i] - i) for i in range(n))
    return contrib(lambda x, y: x > y) - contrib(lambda x, y: x < y)
```

**Complexity:** time **O(n)**, space **O(n)** — four O(n) stack passes.

---

## Edge cases

- All equal: 0.
- Negative values: the contribution formula still holds.
- Large values: Σ can exceed 2³¹.

---

## Common mistakes

1. Same strictness on both sides (double counting with duplicates).
2. 32-bit accumulation.
3. Computing max − min per pair of NGE/NSE indices instead of separating the sums.

---

## Follow-ups

1. Why can you separate the sums?
2. Count subarrays where a[i] is max (for other problems)?

<details><summary>Answer sketches</summary>

**#1:** Σ(max − min) = Σmax − Σmin by linearity; each sum is independent.

**#2:** Same `(i − pge)·(nge − i)` term without the value.
</details>

---

## Flashcards

**Sum of subarray ranges in O(n)?** #flashcard
Σ contribution as max − Σ contribution as min, each via previous/next greater/smaller.

**Count of subarrays where a[i] is the maximum?** #flashcard
(i − previous greater) · (next greater-or-equal − i).

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
