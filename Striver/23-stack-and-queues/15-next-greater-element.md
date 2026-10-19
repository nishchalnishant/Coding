---
module: striver/23-stack-and-queues
lesson: 15
topic: Next Greater Element
difficulty: Medium
source: https://takeuforward.org/learning/dsa/next-greater-element?category=monotonic-stack&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, monotonic-stack, array]
---
# 15. Next Greater Element

← [Postfix to Prefix Conversion](14-postfix-to-prefix-conversion.md) · [Part 23 index](README.md) · Next → [Next Greater Element - 2](16-next-greater-element-ii.md)

> [!abstract] Problem at a glance
> **Task:** For each element, find the first element to its right that is strictly greater (−1 if none).
> **Key insight:** Scan **right to left** and keep a stack that **decreases from bottom to top**. Before answering for `a[i]`, pop every element `≤ a[i]`: those can never be anyone's answer again, because `a[i]` is both closer and at least as big. What remains on top is the answer. Then push `a[i]`.
> **Difficulty:** Medium · **Pattern:** Monotonic decreasing stack · **Also on:** [LC 496](https://leetcode.com/problems/next-greater-element-i/) (query variant)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/next-greater-element?category=monotonic-stack&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force](#3-brute-force) · [4. Monotonic stack, right to left](#4-monotonic-stack-right-to-left) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `arr`, return `ans` where `ans[i]` is the first element to the right of `i` that is strictly greater than `arr[i]`, or `-1` if none exists.

| Input | Output | Why |
|---|---|---|
| `arr = [6,0,8,1,3]` | `[8,8,-1,3,-1]` | 8 is the first bigger value right of 6 and of 0 |
| `arr = [1,3,2,4]` | `[3,4,4,-1]` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`; `|arr[i]| ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force | for each i, scan right until bigger | O(n²) | O(1) extra |
| Monotonic stack, right to left | pop ≤ current, top is the answer, push current | O(n) | O(n) |

> [!tip] Interview angle
> This is the template behind the whole section. Say the invariant out loud: the stack holds candidates in decreasing order, and each element is pushed and popped once, so it's O(n). LC 496 is the same scan plus a hashmap from value to answer.

---

## 3. Brute force

**Intuition.** For each `i`, walk `j = i+1…` and stop at the first `arr[j] > arr[i]`.

```python
def nge_brute(arr):
    n = len(arr)
    ans = [-1] * n
    for i in range(n):
        for j in range(i + 1, n):
            if arr[j] > arr[i]:
                ans[i] = arr[j]
                break
    return ans
```

**Complexity:** time **O(n²)**, space **O(1) extra**.

---

## 4. Monotonic stack, right to left

**Intuition.** An element `x` to the right of `i` that is `≤ arr[i]` is **dominated**: for any index left of `i`, `arr[i]` is closer and at least as large, so `x` can never be the answer again. Popping dominated elements keeps the stack strictly decreasing, and the top is the nearest greater value.

**Algorithm**

1. `st = []`, `ans = [-1]·n`.
2. For `i` from `n−1` down to 0: pop while `st.top ≤ arr[i]`.
3. `ans[i] = st.top` if the stack is non-empty.
4. Push `arr[i]`.

**Dry run** — [6,0,8,1,3] from the right: 3 → −1, st[3]. 1 → 3, st[3,1]. 8 pops 1,3 → −1, st[8]. 0 → 8, st[8,0]. 6 pops 0 → 8. Answer [8,8,−1,3,−1].

**C++**
```cpp
vector<int> nextGreater(vector<int> arr) {
    int n = arr.size();
    vector<int> ans(n, -1), st;
    for (int i = n - 1; i >= 0; i--) {
        while (!st.empty() && st.back() <= arr[i]) st.pop_back();
        if (!st.empty()) ans[i] = st.back();
        st.push_back(arr[i]);
    }
    return ans;
}
```

**Java**
```java
static int[] nextGreater(int[] arr) {
    int n = arr.length;
    int[] ans = new int[n];
    Deque<Integer> st = new ArrayDeque<>();
    for (int i = n - 1; i >= 0; i--) {
        while (!st.isEmpty() && st.peek() <= arr[i]) st.pop();
        ans[i] = st.isEmpty() ? -1 : st.peek();
        st.push(arr[i]);
    }
    return ans;
}
```

**Python**
```python
def next_greater(arr):
    n = len(arr)
    ans, st = [-1] * n, []
    for i in range(n - 1, -1, -1):
        while st and st[-1] <= arr[i]:
            st.pop()
        if st:
            ans[i] = st[-1]
        st.append(arr[i])
    return ans
```

**Complexity:** time **O(n)**, space **O(n)** — each element is pushed once and popped at most once.

---

## Edge cases

- Strictly decreasing array: all −1.
- Equal values: 'greater' is strict, so pop on `≤`.
- Single element.

---

## Common mistakes

1. Popping only on `<`, which returns an equal value as 'greater'.
2. Storing values when the follow-up needs indices (distance, span). Store indices by default.
3. Scanning left to right without realising the logic flips: then you resolve elements when they're popped.

---

## Follow-ups

1. Left-to-right version?
2. Days until a warmer temperature (LC 739)?
3. LC 496 (queries on a subset)?

<details><summary>Answer sketches</summary>

**#1:** Keep a stack of unresolved indices; when `arr[i]` exceeds the top, `ans[top] = arr[i]` and pop. Same O(n).

**#2:** Same scan with indices; answer `j − i`.

**#3:** Run the scan on `nums2`, store value → NGE in a map, answer each `nums1[i]` by lookup.
</details>

---

## Flashcards

**NGE invariant (right-to-left scan)?** #flashcard
Stack is strictly decreasing from bottom to top; pop everything ≤ current before reading the top.

**Why is the monotonic stack O(n)?** #flashcard
Each element is pushed once and popped at most once.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
