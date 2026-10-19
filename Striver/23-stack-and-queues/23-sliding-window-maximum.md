---
module: striver/23-stack-and-queues
lesson: 23
topic: Sliding Window Maximum
difficulty: Hard
source: https://takeuforward.org/learning/dsa/sliding-window-maximum?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, deque, monotonic-queue, sliding-window]
---
# 23. Sliding Window Maximum

← [Implement Min Stack](22-implement-min-stack.md) · [Part 23 index](README.md) · Next → [Trapping Rainwater](24-trapping-rainwater.md)

> [!abstract] Problem at a glance
> **Task:** Maximum of every window of size `k`.
> **Key insight:** Keep a **deque of indices whose values are decreasing**. A new element evicts smaller ones from the back: they're older *and* smaller, so they can never be a window max again. The front is the current max; drop it when it slides out of the window.
> **Difficulty:** Hard · **Pattern:** Monotonic deque · **Also on:** [LC 239](https://leetcode.com/problems/sliding-window-maximum/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/sliding-window-maximum?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Scan each window](#3-scan-each-window) · [4. Monotonic deque of indices](#4-monotonic-deque-of-indices) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `nums` and window size `k`, return the max of each of the `n − k + 1` windows.

| Input | Output | Why |
|---|---|---|
| `nums = [1,3,-1,-3,5,3,6,7], k = 3` | `[3,3,5,5,6,7]` |  |
| `nums = [1], k = 1` | `[1]` |  |

**Constraints:** `1 ≤ k ≤ n ≤ 10⁵`; `|nums[i]| ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Scan each window | max of nums[i:i+k] for every i | O(n·k) | O(1) extra |
| Monotonic deque of indices | pop expired front, pop smaller back, push, read front | O(n) | O(k) |

> [!tip] Interview angle
> The canonical monotonic-deque problem. Say why indices, not values: you need indices to know when the front leaves the window. Cover both pops: the front (expiry) and the back (dominance).

---

## 3. Scan each window

**Intuition.** Compute each window's max directly.

```python
def swm_brute(nums, k):
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]
```

**Complexity:** time **O(n·k)**, space **O(1) extra**.

---

## 4. Monotonic deque of indices

**Intuition.** Invariant: deque indices are increasing and their values strictly decreasing, and all lie within the current window. The front is therefore the window max. Any index `j < i` with `nums[j] ≤ nums[i]` is useless for the rest of time, so pop it from the back.

**Algorithm**

1. For each `i`: if `dq.front ≤ i − k`, pop front.
2. While `nums[dq.back] ≤ nums[i]`, pop back.
3. Push `i`.
4. If `i ≥ k − 1`, append `nums[dq.front]`.

**Dry run** — [1,3,−1,−3,5,3,6,7], k=3: i0 [0]; i1 pops 0 → [1]; i2 [1,2] → 3; i3 [1,2,3] → 3; i4: 1 expires, 5 pops 2,3 → [4] → 5; i5 [4,5] → 5; i6 pops 5,4 → [6] → 6; i7 → [7] → 7.

**C++**
```cpp
vector<int> maxSlidingWindow(vector<int> nums, int k) {
    deque<int> dq;
    vector<int> ans;
    for (int i = 0; i < (int)nums.size(); i++) {
        if (!dq.empty() && dq.front() <= i - k) dq.pop_front();
        while (!dq.empty() && nums[dq.back()] <= nums[i]) dq.pop_back();
        dq.push_back(i);
        if (i >= k - 1) ans.push_back(nums[dq.front()]);
    }
    return ans;
}
```

**Java**
```java
static int[] maxSlidingWindow(int[] nums, int k) {
    Deque<Integer> dq = new ArrayDeque<>();
    int[] ans = new int[nums.length - k + 1];
    for (int i = 0; i < nums.length; i++) {
        if (!dq.isEmpty() && dq.peekFirst() <= i - k) dq.pollFirst();
        while (!dq.isEmpty() && nums[dq.peekLast()] <= nums[i]) dq.pollLast();
        dq.offerLast(i);
        if (i >= k - 1) ans[i - k + 1] = nums[dq.peekFirst()];
    }
    return ans;
}
```

**Python**
```python
from collections import deque

def max_sliding_window(nums, k):
    dq, ans = deque(), []
    for i, x in enumerate(nums):
        if dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            ans.append(nums[dq[0]])
    return ans
```

**Complexity:** time **O(n)**, space **O(k)** — each index enters and leaves the deque once.

---

## Edge cases

- `k == 1`: the array itself.
- `k == n`: single max.
- Decreasing array: deque holds up to k elements; expiry pops matter.

---

## Common mistakes

1. Storing values instead of indices (can't detect expiry).
2. Checking expiry with `<` instead of `≤ i − k` (off by one).
3. Using a heap without lazy deletion; with lazy deletion it's O(n log n), acceptable but not optimal.

---

## Follow-ups

1. Sliding window minimum?
2. Shortest subarray with sum ≥ K, negatives allowed (LC 862)?
3. Constrained subsequence sum (LC 1425)?

<details><summary>Answer sketches</summary>

**#1:** Flip the comparison: keep values increasing.

**#2:** Monotonic deque over prefix sums.

**#3:** DP where dp[i] needs the max of the last k dp values: a monotonic deque.
</details>

---

## Flashcards

**Sliding window max: what does the deque hold?** #flashcard
Indices in the window with strictly decreasing values; front is the max.

**Two kinds of deque pops in sliding window max?** #flashcard
Front: index expired (≤ i − k). Back: value ≤ incoming.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
