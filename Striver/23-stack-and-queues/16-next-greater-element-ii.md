---
module: striver/23-stack-and-queues
lesson: 16
topic: Next Greater Element - 2
difficulty: Medium
source: https://takeuforward.org/learning/dsa/next-greater-element---2?category=monotonic-stack&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, monotonic-stack, circular]
---
# 16. Next Greater Element - 2

← [Next Greater Element](15-next-greater-element.md) · [Part 23 index](README.md) · Next → [Asteroid Collision](17-asteroid-collision.md)

> [!abstract] Problem at a glance
> **Task:** Next greater element in a **circular** array.
> **Key insight:** Pretend the array is written twice: scan `i` from `2n−1` down to 0 using `a[i % n]`. The first pass (indices `n…2n−1`) only fills the stack with the 'wrapped-around' candidates; answers are recorded only for `i < n`.
> **Difficulty:** Medium · **Pattern:** Monotonic stack over a doubled array · **Also on:** [LC 503](https://leetcode.com/problems/next-greater-element-ii/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/next-greater-element---2?category=monotonic-stack&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force](#3-brute-force) · [4. Monotonic stack over 2n](#4-monotonic-stack-over-2n) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a circular array `nums` (the element after the last is the first), return the next greater number for every element, or `-1` if none exists.

| Input | Output | Why |
|---|---|---|
| `nums = [1,2,1]` | `[2,-1,2]` | the last 1 wraps around to find 2 |
| `nums = [1,2,3,4,3]` | `[2,3,4,-1,4]` |  |

**Constraints:** `1 ≤ n ≤ 10⁴`; `−10⁹ ≤ nums[i] ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force | for each i, look at the next n−1 positions circularly | O(n²) | O(1) extra |
| Monotonic stack over 2n | right-to-left from 2n−1, answer only for i < n | O(n) | O(n) |

> [!tip] Interview angle
> The modulo trick is what they want. Don't actually allocate the doubled array; index with `i % n`. The maximum element is always −1 (and so are its duplicates).

---

## 3. Brute force

**Intuition.** For each `i`, check `nums[(i+k) % n]` for `k = 1…n−1`.

```python
def nge2_brute(nums):
    n = len(nums)
    ans = [-1] * n
    for i in range(n):
        for k in range(1, n):
            if nums[(i + k) % n] > nums[i]:
                ans[i] = nums[(i + k) % n]
                break
    return ans
```

**Complexity:** time **O(n²)**, space **O(1) extra**.

---

## 4. Monotonic stack over 2n

**Intuition.** The candidates for `nums[i]` are everything to its right, then everything from index 0 up to `i`. That's exactly the suffix of the doubled array starting at `i+1`. One right-to-left pass over `2n` indices builds the right stack.

**Algorithm**

1. For `i` from `2n−1` down to 0, with `x = nums[i % n]`:
2. Pop while `st.top ≤ x`.
3. If `i < n`: `ans[i] = st.top` or −1.
4. Push `x`.

**Dry run** — [1,2,1]: i=5 (1) → push. i=4 (2) pops 1 → push 2. i=3 (1) → push, st[2,1]. i=2 (1): pop 1 → ans=2. i=1 (2): pop 1,2 → −1. i=0 (1) → ans=2. [2,−1,2].

**C++**
```cpp
vector<int> nextGreaterCircular(vector<int> nums) {
    int n = nums.size();
    vector<int> ans(n, -1), st;
    for (int i = 2 * n - 1; i >= 0; i--) {
        int x = nums[i % n];
        while (!st.empty() && st.back() <= x) st.pop_back();
        if (i < n && !st.empty()) ans[i] = st.back();
        st.push_back(x);
    }
    return ans;
}
```

**Java**
```java
static int[] nextGreaterCircular(int[] nums) {
    int n = nums.length;
    int[] ans = new int[n];
    Arrays.fill(ans, -1);
    Deque<Integer> st = new ArrayDeque<>();
    for (int i = 2 * n - 1; i >= 0; i--) {
        int x = nums[i % n];
        while (!st.isEmpty() && st.peek() <= x) st.pop();
        if (i < n && !st.isEmpty()) ans[i] = st.peek();
        st.push(x);
    }
    return ans;
}
```

**Python**
```python
def next_greater_circular(nums):
    n = len(nums)
    ans, st = [-1] * n, []
    for i in range(2 * n - 1, -1, -1):
        x = nums[i % n]
        while st and st[-1] <= x:
            st.pop()
        if i < n and st:
            ans[i] = st[-1]
        st.append(x)
    return ans
```

**Complexity:** time **O(n)**, space **O(n)** — 2n pushes, at most 2n pops.

---

## Edge cases

- All equal: all −1.
- Maximum (and duplicates of it): −1.
- Strictly decreasing: everything but the first wraps to the first.

---

## Common mistakes

1. Allocating a real doubled array (works, wastes memory) and then returning `2n` answers.
2. Recording answers in the first pass (`i ≥ n`), which writes out of bounds.
3. Using `<` instead of `≤` on pop.

---

## Follow-ups

1. Circular next smaller?
2. Return indices / distances?

<details><summary>Answer sketches</summary>

**#1:** Same loop with the comparison flipped.

**#2:** Push `i % n` and compare `nums[st.top]`.
</details>

---

## Flashcards

**Circular NGE trick?** #flashcard
Iterate i from 2n−1 down to 0 using nums[i % n]; only write ans[i] when i < n.

**Which elements always get −1 in circular NGE?** #flashcard
Every occurrence of the maximum.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
