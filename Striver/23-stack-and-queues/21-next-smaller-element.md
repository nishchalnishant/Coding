---
module: striver/23-stack-and-queues
lesson: 21
topic: Next Smaller Element
difficulty: Medium
source: https://takeuforward.org/learning/dsa/next-smaller-element?category=monotonic-stack&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, monotonic-stack, array]
---
# 21. Next Smaller Element

← [Remove K Digits](20-remove-k-digits.md) · [Part 23 index](README.md) · Next → [Implement Min Stack](22-implement-min-stack.md)

> [!abstract] Problem at a glance
> **Task:** For each element, find the first element to its right that is strictly smaller (−1 if none).
> **Key insight:** Mirror of NGE: keep the stack **increasing** from bottom to top. Scanning right to left, pop everything `≥ a[i]`; the remaining top is the nearest strictly smaller value. Paired with previous-smaller, this is the building block for histograms, contribution sums and span problems.
> **Difficulty:** Medium · **Pattern:** Monotonic increasing stack · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/help-classmates--141631/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/next-smaller-element?category=monotonic-stack&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force](#3-brute-force) · [4. Monotonic stack, right to left](#4-monotonic-stack-right-to-left) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `arr`, return `ans` where `ans[i]` is the first element to the right of `i` that is strictly smaller than `arr[i]`, or `-1`.

| Input | Output | Why |
|---|---|---|
| `arr = [4,8,5,2,25]` | `[2,5,2,-1,-1]` |  |
| `arr = [13,7,6,12]` | `[7,6,-1,-1]` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force | scan right for the first smaller | O(n²) | O(1) extra |
| Monotonic stack, right to left | pop ≥ current, top is the answer, push | O(n) | O(n) |

> [!tip] Interview angle
> Usually asked together with NGE or as a sub-step. Have all four variants straight: next/previous × greater/smaller. Each is the same loop with a flipped comparison or direction.

---

## 3. Brute force

**Intuition.** For each `i`, walk right until a smaller value appears.

```python
def nse_brute(arr):
    n = len(arr)
    ans = [-1] * n
    for i in range(n):
        for j in range(i + 1, n):
            if arr[j] < arr[i]:
                ans[i] = arr[j]
                break
    return ans
```

**Complexity:** time **O(n²)**, space **O(1) extra**.

---

## 4. Monotonic stack, right to left

**Intuition.** A value to the right of `i` that's `≥ arr[i]` can never be the nearest smaller for anything further left: `arr[i]` is closer and no larger. Popping those keeps the stack strictly increasing.

**Algorithm**

1. For `i` from `n−1` down to 0: pop while `st.top ≥ arr[i]`.
2. `ans[i] = st.top` or −1.
3. Push `arr[i]`.

**Dry run** — [4,8,5,2,25]: 25 → −1; 2 pops 25 → −1; 5 → 2; 8 → 5; 4 pops 8,5 → 2. [2,5,2,−1,−1].

**C++**
```cpp
vector<int> nextSmaller(vector<int> arr) {
    int n = arr.size();
    vector<int> ans(n, -1), st;
    for (int i = n - 1; i >= 0; i--) {
        while (!st.empty() && st.back() >= arr[i]) st.pop_back();
        if (!st.empty()) ans[i] = st.back();
        st.push_back(arr[i]);
    }
    return ans;
}
```

**Java**
```java
static int[] nextSmaller(int[] arr) {
    int n = arr.length;
    int[] ans = new int[n];
    Deque<Integer> st = new ArrayDeque<>();
    for (int i = n - 1; i >= 0; i--) {
        while (!st.isEmpty() && st.peek() >= arr[i]) st.pop();
        ans[i] = st.isEmpty() ? -1 : st.peek();
        st.push(arr[i]);
    }
    return ans;
}
```

**Python**
```python
def next_smaller(arr):
    n = len(arr)
    ans, st = [-1] * n, []
    for i in range(n - 1, -1, -1):
        while st and st[-1] >= arr[i]:
            st.pop()
        if st:
            ans[i] = st[-1]
        st.append(arr[i])
    return ans
```

**Complexity:** time **O(n)**, space **O(n)** — each element pushed once, popped at most once.

---

## Edge cases

- Strictly increasing: all −1.
- Duplicates: an equal value is not smaller.

---

## Common mistakes

1. Popping on `>` only, which returns equal values.
2. Mixing up the direction of the inequality between NGE and NSE.
3. Returning indices when values are asked, or vice versa.

---

## Follow-ups

1. Previous smaller element?
2. Nearest smaller on either side (for histograms)?

<details><summary>Answer sketches</summary>

**#1:** Scan left to right with the same pop rule.

**#2:** Compute PSE and NSE as indices; width = NSE − PSE − 1.
</details>

---

## Flashcards

**NSE stack order?** #flashcard
Strictly increasing from bottom to top (pop everything ≥ current).

**Four monotonic-stack variants?** #flashcard
Next/previous × greater/smaller: flip scan direction or the comparison.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
