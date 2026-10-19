---
module: striver/25-binary-search-trees
lesson: 15
topic: Largest BST in Binary Tree
difficulty: Hard
source: https://takeuforward.org/learning/dsa/largest-bst-in-binary-tree?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search-trees, bst, post-order, dp-on-trees]
---
# 15. Largest BST in Binary Tree

← [Correct BST with two nodes swapped](14-recover-bst.md) · [Part 25 index](README.md) · Next → [Part 26: Heaps](../26-heaps/README.md)

> [!abstract] Problem at a glance
> **Task:** Return the size (node count) of the largest subtree that is a valid BST.
> **Key insight:** Post-order information passing. Each subtree reports `(min, max, size)`. A node forms a BST iff `left.max < val < right.min`, and then it reports `(min(left.min, val), max(right.max, val), l + r + 1)`. Otherwise it reports an **impossible range** `(−∞, +∞)` so that no ancestor can be a BST, along with the best size found below. Empty subtrees report `(+∞, −∞, 0)`, which always passes the check.
> **Difficulty:** Hard · **Pattern:** Post-order return-info · **Also on:** [LC 333](https://leetcode.com/problems/largest-bst-subtree/) (premium)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/largest-bst-in-binary-tree?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Validate at every node](#3-validate-at-every-node) · [4. Post-order (min, max, size)](#4-post-order-min-max-size) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the root of a binary tree, find the largest subtree (all descendants of a node) that is also a BST, and return its number of nodes.

| Input | Output | Why |
|---|---|---|
| `root = [10,5,15,1,8,null,7]` | `3` | subtree at 5 = {5,1,8}; 15's subtree fails because 7 < 15 |
| `root = [5,2,4,1,3]` | `3` | {2,1,3}; 4 under 5 on the left breaks the root |

**Constraints:** `0 ≤ n ≤ 10⁴`; `−10⁴ ≤ val ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Validate at every node | for each node: isBST(subtree)? count | O(n²) | O(h) |
| Post-order (min, max, size) | valid iff l.max < val < r.min; invalid → (−∞, +∞, best) | O(n) | O(h) |

> [!tip] Interview angle
> It's the most-asked 'combine validate-BST with post-order' problem. Explain the sentinel ranges carefully: the empty tree's (+∞, −∞) and the invalid subtree's (−∞, +∞) are what make the check one line.

---

## 3. Validate at every node

**Intuition.** Run validate-BST (bounds) at every node and take the largest valid subtree's size. The repeated work makes it quadratic on a skewed tree.

```python
def largest_bst_brute(root):
    def ok(n, lo, hi):
        return not n or (lo < n.val < hi and ok(n.left, lo, n.val) and ok(n.right, n.val, hi))
    def size(n):
        return 1 + size(n.left) + size(n.right) if n else 0
    def best(n):
        if not n:
            return 0
        if ok(n, float("-inf"), float("inf")):
            return size(n)
        return max(best(n.left), best(n.right))
    return best(root)
```

**Complexity:** time **O(n²)**, space **O(h)**.

---

## 4. Post-order (min, max, size)

**Intuition.** One bottom-up pass. A valid subtree's size is its true node count. An invalid subtree carries the best size found inside it and a poisoned range that fails every ancestor's check.

**Algorithm**

1. `go(null) = (+∞, −∞, 0)`.
2. `(lmn, lmx, ls) = go(left)`, `(rmn, rmx, rs) = go(right)`.
3. If `lmx < val < rmn`: return `(min(lmn, val), max(rmx, val), ls + rs + 1)`.
4. Else return `(−∞, +∞, max(ls, rs))`.
5. Answer: third component of `go(root)`.

**Dry run** — [10,5,15,1,8,null,7]: 1 → (1,1,1); 8 → (8,8,1); 5: 1 < 5 < 8 → (1,8,3). 7 → (7,7,1); 15: left empty max −∞ < 15, right min 7 < 15 fails → (−∞,∞,1). 10: lmx 8 < 10 but rmn −∞ fails → (−∞,∞,max(3,1)) = 3.

**C++**
```cpp
struct Info { long long mn, mx; int sz; };
Info goL(TreeNode* n) {
    if (!n) return {LLONG_MAX, LLONG_MIN, 0};
    Info l = goL(n->left), r = goL(n->right);
    if (l.mx < n->val && n->val < r.mn)
        return {min<long long>(l.mn, n->val), max<long long>(r.mx, n->val), l.sz + r.sz + 1};
    return {LLONG_MIN, LLONG_MAX, max(l.sz, r.sz)};
}
int largestBst(TreeNode* root) { return goL(root).sz; }
```

**Java**
```java
static long[] goL(TreeNode n) {
    if (n == null) return new long[]{Long.MAX_VALUE, Long.MIN_VALUE, 0};
    long[] l = goL(n.left), r = goL(n.right);
    if (l[1] < n.val && n.val < r[0])
        return new long[]{Math.min(l[0], n.val), Math.max(r[1], n.val), l[2] + r[2] + 1};
    return new long[]{Long.MIN_VALUE, Long.MAX_VALUE, Math.max(l[2], r[2])};
}
static int largestBst(TreeNode root) { return (int) goL(root)[2]; }
```

**Python**
```python
def largest_bst(root):
    INF = float("inf")
    def go(n):
        if not n:
            return INF, -INF, 0
        lmn, lmx, ls = go(n.left)
        rmn, rmx, rs = go(n.right)
        if lmx < n.val < rmn:
            return min(lmn, n.val), max(rmx, n.val), ls + rs + 1
        return -INF, INF, max(ls, rs)
    return go(root)[2]
```

**Complexity:** time **O(n)**, space **O(h)** — each node is combined once from its children's summaries.

---

## Edge cases

- Empty tree → 0.
- Whole tree is a BST → n.
- Duplicates → not a strict BST.
- Only leaves are BSTs → 1.

---

## Common mistakes

1. Checking only direct children instead of subtree min/max.
2. Returning `min(lmn, val)` when the left subtree is empty: `lmn = +∞`, so the `min` correctly picks `val`, but writing `lmn` alone would be wrong.
3. Using a 'size' field that counts the whole subtree even when it's invalid.
4. Using 0 as the empty-range sentinel.

---

## Follow-ups

1. Max **sum** BST subtree (LC 1373)?
2. Return the root of the largest BST?
3. Why poison with (−∞, +∞)?

<details><summary>Answer sketches</summary>

**#1:** Same template returning sum; track the best sum globally (and allow 0 for empty).

**#2:** Carry the node with the best size in the tuple or a global.

**#3:** Any ancestor check `lmx < val < rmn` then fails, so invalidity propagates upward.
</details>

---

## Flashcards

**Largest BST subtree: what does each node return?** #flashcard
(min, max, size); invalid → (−∞, +∞, best size below).

**Empty subtree's (min, max)?** #flashcard
(+∞, −∞): it never blocks the parent's check.

**Largest BST: complexity?** #flashcard
O(n) time, O(h) space.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
