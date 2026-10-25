---
module: striver-a2z/23-stack-and-queues
lesson: 20
topic: Remove K Digits
difficulty: Medium
source: https://takeuforward.org/learning/dsa/remove-k-digits?category=monotonic-stack&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, monotonic-stack, greedy, string]
---
# 20. Remove K Digits

← [Sum of Subarray Ranges](19-sum-of-subarray-ranges.md) · [Part 23 index](README.md) · Next → [Next Smaller Element](21-next-smaller-element.md)

> [!abstract] Problem at a glance
> **Task:** Remove exactly `k` digits from a number string to make the smallest possible number.
> **Key insight:** Greedy from the left: a digit followed by a smaller digit should be removed, because lowering an earlier position beats anything later. A **non-decreasing stack** does this. Pop while `top > d` and `k > 0`. Any `k` left over is removed from the end. Strip leading zeros; empty means `"0"`.
> **Difficulty:** Medium · **Pattern:** Monotonic increasing stack + greedy · **Also on:** [LC 402](https://leetcode.com/problems/remove-k-digits/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/remove-k-digits?category=monotonic-stack&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Remove the first peak, k times](#3-remove-the-first-peak-k-times) · [4. Monotonic stack](#4-monotonic-stack) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a non-negative integer as string `num` and an integer `k`, return the smallest possible integer (as a string, no leading zeros) after removing exactly `k` digits.

| Input | Output | Why |
|---|---|---|
| `num = "1432219", k = 3` | `"1219"` | remove 4, 3, 2 |
| `num = "10200", k = 1` | `"200"` | remove 1, strip leading zero |
| `num = "10", k = 2` | `"0"` | everything removed |

**Constraints:** `1 ≤ k ≤ |num| ≤ 10⁵`; `num` has no leading zeros except `"0"` itself.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Remove the first peak, k times | each round delete the first i with num[i] > num[i+1] | O(n·k) | O(n) |
| Monotonic stack | pop larger tops while k > 0, then trim | O(n) | O(n) |

> [!tip] Interview angle
> Prove the greedy in one line: in two candidates of the same length, the first differing position decides, so removing the first 'peak' (a digit greater than its successor) is never worse. Then nail the three cleanups: leftover k, leading zeros, and empty result.

---

## 3. Remove the first peak, k times

**Intuition.** Each round, scan for the first digit greater than its successor (or the last digit if none) and delete it. This is the same greedy, applied one digit at a time.

```python
def remove_k_slow(num, k):
    s = list(num)
    for _ in range(k):
        i = 0
        while i + 1 < len(s) and s[i] <= s[i + 1]:
            i += 1
        del s[i]
    return ''.join(s).lstrip('0') or '0'
```

**Complexity:** time **O(n·k)**, space **O(n)**.

---

## 4. Monotonic stack

**Intuition.** The stack holds the kept prefix, non-decreasing. When a smaller digit arrives, each larger top is a peak; removing it makes an earlier position smaller. Once `k` runs out, keep everything.

**Algorithm**

1. For each digit `d`: while `k > 0` and `st.top > d`: pop, `k−−`. Push `d`.
2. While `k > 0`: pop, `k−−` (the stack is non-decreasing, so trim the largest tail).
3. Strip leading zeros; return `"0"` if empty.

**Dry run** — "1432219", k=3: 1 → [1]; 4 → [1,4]; 3 pops 4 (k=2) → [1,3]; 2 pops 3 (k=1) → [1,2]; 2 → [1,2,2]; 1 pops 2 (k=0) → [1,2,1]; 9 → [1,2,1,9]. "1219".

**C++**
```cpp
string removeKdigits(string num, int k) {
    string st;
    for (char d : num) {
        while (k > 0 && !st.empty() && st.back() > d) { st.pop_back(); k--; }
        st.push_back(d);
    }
    while (k > 0 && !st.empty()) { st.pop_back(); k--; }
    size_t i = 0;
    while (i < st.size() && st[i] == '0') i++;
    st = st.substr(i);
    return st.empty() ? "0" : st;
}
```

**Java**
```java
static String removeKdigits(String num, int k) {
    StringBuilder st = new StringBuilder();
    for (char d : num.toCharArray()) {
        while (k > 0 && st.length() > 0 && st.charAt(st.length() - 1) > d) { st.setLength(st.length() - 1); k--; }
        st.append(d);
    }
    st.setLength(st.length() - k);
    int i = 0;
    while (i < st.length() && st.charAt(i) == '0') i++;
    String r = st.substring(i);
    return r.isEmpty() ? "0" : r;
}
```

**Python**
```python
def remove_k_digits(num, k):
    st = []
    for d in num:
        while k and st and st[-1] > d:
            st.pop()
            k -= 1
        st.append(d)
    if k:
        st = st[:-k]
    return ''.join(st).lstrip('0') or '0'
```

**Complexity:** time **O(n)**, space **O(n)** — each digit is pushed and popped at most once.

---

## Edge cases

- Non-decreasing input: remove from the end.
- Leading zeros after removal (`"10200"`).
- `k == n`: return `"0"`.

---

## Common mistakes

1. Forgetting the leftover-k trim, so `"12345"` stays unchanged.
2. Not stripping leading zeros, or stripping to empty and returning `""`.
3. Popping on `≥`: harmless for correctness but wastes removals on equal digits, e.g. `"112"` with k=1 gives 12 instead of 11.

---

## Follow-ups

1. Largest number instead?
2. Smallest subsequence with each distinct letter once (LC 316)?

<details><summary>Answer sketches</summary>

**#1:** Flip the comparison: pop while `top < d`.

**#2:** Same stack, but only pop if the top appears again later, and skip letters already in the stack.
</details>

---

## Flashcards

**Remove K Digits greedy rule?** #flashcard
Pop the stack top while it's greater than the incoming digit and k > 0.

**Three cleanups after the stack pass in Remove K Digits?** #flashcard
Trim leftover k from the end, strip leading zeros, empty → "0".

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
