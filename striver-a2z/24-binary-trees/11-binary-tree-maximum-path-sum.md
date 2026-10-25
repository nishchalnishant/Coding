---
module: striver-a2z/24-binary-trees
lesson: 11
topic: Maximum path sum
difficulty: Hard
source: https://takeuforward.org/learning/dsa/maximum-path-sum-?category=medium-problems&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, dfs, postorder, tree-dp, hard]
---
# 11. Maximum path sum

← [Diameter of Binary Tree](10-diameter-of-binary-tree.md) · [Part 24 index](README.md) · Next → [Check for symmetrical BTs](12-symmetric-tree.md)

> [!abstract] Problem at a glance
> **Task:** Maximum sum over all non-empty paths (any node to any node).
> **Key insight:** Same skeleton as diameter. Each node returns its best **downward** gain, `val + max(0, gainL, gainR)` (a negative branch is dropped, never extended). At each node, record `val + max(0, gainL) + max(0, gainR)` as a candidate for the path that bends there.
> **Difficulty:** Hard · **Pattern:** Postorder: return one-armed gain, record two-armed path · **Also on:** [LC 124](https://leetcode.com/problems/binary-tree-maximum-path-sum/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/maximum-path-sum-?category=medium-problems&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Try every node as the top (recomputing gains)](#3-try-every-node-as-the-top-recomputing-gains) · [4. Single postorder pass](#4-single-postorder-pass) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

A path is a sequence of nodes where each adjacent pair is connected by an edge, with each node appearing at most once. The path need not pass through the root. Return the maximum path sum of any non-empty path.

| Input | Output | Why |
|---|---|---|
| `root = [1,2,3]` | `6` | 2 → 1 → 3 |
| `root = [-10,9,20,null,null,15,7]` | `42` | 15 → 20 → 7 |
| `root = [-3]` | `-3` | must be non-empty |

**Constraints:** `1 ≤ n ≤ 3·10⁴`; `−1000 ≤ val ≤ 1000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Try every node as the top (recomputing gains) | for each node: val + max(0, gain(L)) + max(0, gain(R)) | O(n²) | O(h) |
| Single postorder pass | g = val + max(0, gL, gR); best = max(best, val + max(0,gL) + max(0,gR)) | O(n) | O(h) |

> [!tip] Interview angle
> A classic Google/FAANG hard. Name both quantities out loud: the *return* value (a path going down one side, extendable by the parent) and the *answer* (a path that may use both sides, not extendable). Initialise the answer to −∞ (or `root.val`), not 0, because all-negative trees must return the largest single value.

---

## 3. Try every node as the top (recomputing gains)

**Intuition.** Compute the downward gain function from scratch at every node. It's correct but slow, so use it as a reference.

```python
def max_path_naive(root):
    def gain(n):
        return 0 if not n else n.val + max(0, gain(n.left), gain(n.right))
    best = float('-inf')
    st = [root]
    while st:
        n = st.pop()
        if not n:
            continue
        best = max(best, n.val + max(0, gain(n.left)) + max(0, gain(n.right)))
        st += [n.left, n.right]
    return best
```

**Complexity:** time **O(n²)**, space **O(h)**.

---

## 4. Single postorder pass

**Intuition.** Gains clipped at 0 mean 'don't take that branch'. The bending path at `n` uses both clipped gains. The parent can only extend one arm.

**Algorithm**

1. `best = −∞`.
2. `gain(null) = 0`.
3. `l = max(0, gain(left))`, `r = max(0, gain(right))`.
4. `best = max(best, n.val + l + r)`.
5. Return `n.val + max(l, r)`.

**Dry run** — [-10,9,20,null,null,15,7]: 9→9 (best 9); 15→15; 7→7; 20: best=20+15+7=42, return 35; −10: best=max(42, −10+9+35=34)=42.

**C++**
```cpp
int mpsGain(TreeNode* n, int& best) {
    if (!n) return 0;
    int l = max(0, mpsGain(n->left, best));
    int r = max(0, mpsGain(n->right, best));
    best = max(best, n->val + l + r);
    return n->val + max(l, r);
}
int maxPathSum(TreeNode* root) {
    int best = INT_MIN;
    mpsGain(root, best);
    return best;
}
```

**Java**
```java
static int bestSum;
static int mpsGain(TreeNode n) {
    if (n == null) return 0;
    int l = Math.max(0, mpsGain(n.left));
    int r = Math.max(0, mpsGain(n.right));
    bestSum = Math.max(bestSum, n.val + l + r);
    return n.val + Math.max(l, r);
}
static int maxPathSum(TreeNode root) {
    bestSum = Integer.MIN_VALUE;
    mpsGain(root);
    return bestSum;
}
```

**Python**
```python
def max_path_sum(root):
    best = float('-inf')
    def gain(n):
        nonlocal best
        if not n:
            return 0
        l = max(0, gain(n.left))
        r = max(0, gain(n.right))
        best = max(best, n.val + l + r)
        return n.val + max(l, r)
    gain(root)
    return best
```

**Complexity:** time **O(n)**, space **O(h)** — each node computes its gain once.

---

## Edge cases

- All negative → the max single node (`[-2,-1]` → −1).
- Single node.
- The best path is a lone subtree far from the root.

---

## Common mistakes

1. `best = 0` initial value (wrong for all-negative trees).
2. Returning `val + l + r` to the parent (a path can't fork).
3. Not clipping negative gains at 0.

---

## Follow-ups

1. Path must go root → leaf?
2. Return the path nodes?
3. Same on a general tree?

<details><summary>Answer sketches</summary>

**#1:** Plain DFS: `val + max(f(L), f(R))`, no clipping, leaf base case.

**#2:** Track argmax node and which arms were positive, then reconstruct downward.

**#3:** Keep the top-2 positive child gains.
</details>

---

## Flashcards

**Max path sum: return vs record?** #flashcard
Return val + max(0, gL, gR); record val + max(0,gL) + max(0,gR).

**Initial best in max path sum?** #flashcard
−∞ (all-negative trees).

**Why clip gains at 0?** #flashcard
A negative branch only lowers the sum, so drop it.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
