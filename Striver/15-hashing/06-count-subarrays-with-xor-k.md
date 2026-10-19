---
module: striver/15-hashing
lesson: 6
topic: Count Subarrays with Given XOR K
difficulty: Medium
source: https://takeuforward.org/learning/dsa/count-subarrays-with-given-xor-k?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, hashing, hashing, prefix-xor, bit-manipulation]
---
# 6. Count Subarrays with Given XOR K

← [Count Subarrays with Given Sum](05-count-subarrays-with-given-sum.md) · [Part 15 index](README.md) · Next → [Part 16: Binary Search](../16-binary-search/README.md)

> [!abstract] Problem at a glance
> **Task:** Return how many contiguous subarrays have bitwise XOR equal to `k`.
> **Key insight:** `xor(l..r) = X[r] ^ X[l − 1]`, and `a ^ b = k ⇔ b = a ^ k`. So it's the count-subarrays-sum-k loop with `p − k` replaced by `x ^ k`, seeded `{0: 1}`.
> **Difficulty:** Medium · **Pattern:** Prefix XOR + count map · **Also on:** [InterviewBit: Subarray with given XOR](https://www.interviewbit.com/problems/subarray-with-given-xor/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-subarrays-with-given-xor-k?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. All subarrays with a running XOR](#3-all-subarrays-with-a-running-xor) · [4. Prefix XOR + count map](#4-prefix-xor--count-map) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums` and an integer `k`, return the number of subarrays whose elements XOR to `k`.

| Input | Output | Why |
|---|---|---|
| `nums = [4, 2, 2, 6, 4], k = 6` | `4` | [4, 2], [4, 2, 2, 6, 4], [2, 2, 6], [6] |
| `nums = [5, 6, 7, 8, 9], k = 5` | `2` | [5], [5, 6, 7, 8, 9] |

**Constraints:** `1 ≤ n ≤ 10⁵`, `0 ≤ nums[i], k ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| All subarrays with a running XOR | fix l, extend r, x ^= nums[r] | O(n²) | O(1) |
| Prefix XOR + count map | ans += cnt[x ^ k]; then cnt[x] += 1; seed {0: 1} | O(n) average | O(n) |

> [!tip] Interview angle
> XOR has no 'monotone' property at all, so there's no window alternative. Point out the two identities: `x ^ x = 0` (prefix cancellation) and `x ^ 0 = x` (the seed).

---

## 3. All subarrays with a running XOR

**Intuition.** Same shape as the sum brute force.

```python
def xor_count_brute(nums, k):
    count = 0
    for l in range(len(nums)):
        x = 0
        for r in range(l, len(nums)):
            x ^= nums[r]
            if x == k:
                count += 1
    return count
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Prefix XOR + count map

**Intuition.** Let `x` be the XOR of `nums[0..i]`. A subarray `(j, i]` has XOR `k` iff `X[j] ^ x = k`, i.e. `X[j] = x ^ k`. Count how many earlier prefixes had that value. XOR is its own inverse, which is why `^` replaces both the `−` in the lookup and nothing else changes.

**Dry run** — `[4 2 2 6 4]`, k = 6: cnt{0:1}. x=4: need 2 → 0. x=6: need 0 → +1. x=4: need 2 → 0. x=2: need 4 → +2 (two 4s). x=6: need 0 → +1. Total 4.

**C++**
```cpp
int subarraysWithXorK(vector<int>& nums, int k) {
    unordered_map<int, int> cnt;
    cnt[0] = 1;
    int x = 0, ans = 0;
    for (int v : nums) {
        x ^= v;
        auto it = cnt.find(x ^ k);
        if (it != cnt.end()) ans += it->second;
        cnt[x]++;
    }
    return ans;
}
```

**Java**
```java
static int subarraysWithXorK(int[] nums, int k) {
    HashMap<Integer, Integer> cnt = new HashMap<>();
    cnt.put(0, 1);
    int x = 0, ans = 0;
    for (int v : nums) {
        x ^= v;
        ans += cnt.getOrDefault(x ^ k, 0);
        cnt.merge(x, 1, Integer::sum);
    }
    return ans;
}
```

**Python**
```python
def xor_count(nums, k):
    cnt = {0: 1}
    x = ans = 0
    for v in nums:
        x ^= v
        ans += cnt.get(x ^ k, 0)
        cnt[x] = cnt.get(x, 0) + 1
    return ans
```

**Complexity:** time **O(n) average**, space **O(n)**.

---

## Edge cases

- k = 0: subarrays that cancel (`[1, 1]`).
- All zeros → n(n + 1)/2.
- Single element equal to k.

---

## Common mistakes

1. Looking up `x − k` out of habit.
2. Missing the `{0: 1}` seed.
3. Answer overflow for big n — n(n + 1)/2 exceeds `int` past n ≈ 65 000; use `long` there.

---

## Follow-ups

1. Longest subarray with XOR k.
2. Maximum XOR of any subarray.
3. Count triplets i < j ≤ k with xor(i..j−1) = xor(j..k) (LC 1442).

<details><summary>Answer sketches</summary>

**#1:** First-index map seeded {0: −1}, as in [Longest Subarray with Sum K](03-longest-subarray-with-sum-k.md).

**#2:** Binary trie over prefix XORs: [Tries](../29-tries/README.md).

**#3:** Equivalent to X[i] == X[k + 1]; each such pair contributes k − i triplets.
</details>

---

## Flashcards

**Subarray XOR k ⇔ ?** #flashcard
Some earlier prefix equals x ^ k.

**Why does the sum template carry over to XOR?** #flashcard
XOR is invertible: a ^ b = k ⇔ a = b ^ k, just like a − b = k ⇔ a = b + k.

**Seed for counting XOR subarrays?** #flashcard
{0: 1}.

**Interview track →** [Hashing deep-dive](../../01-data-structures/02-hashing.md) · [Hashing walkthroughs](../../coding/data-structures/02-hashing.md) · [Sliding window](../../02-algorithms/04-sliding-window.md)
