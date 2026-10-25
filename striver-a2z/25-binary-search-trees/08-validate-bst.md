---
module: striver-a2z/25-binary-search-trees
lesson: 8
topic: Check if a tree is a BST or not
difficulty: Medium
source: https://takeuforward.org/learning/dsa/check-if-a-tree-is-a-bst-or-not?category=medium&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search-trees, bst, validation, dfs]
---
# 8. Check if a tree is a BST or not

← [Kth Smallest and Largest element in BST](07-kth-smallest-largest-in-bst.md) · [Part 25 index](README.md) · Next → [LCA in BST](09-lca-in-bst.md)

> [!abstract] Problem at a glance
> **Task:** Return whether the binary tree is a valid BST (strict: left < node < right for **all** descendants).
> **Key insight:** Comparing a node only with its children is the classic trap. Every node must lie inside an **(low, high) window** inherited from all its ancestors: go left and the high bound becomes this value, go right and the low bound does. Equivalently, the inorder sequence must be strictly increasing.
> **Difficulty:** Medium · **Pattern:** DFS with bounds / inorder monotonicity · **Also on:** [LC 98](https://leetcode.com/problems/validate-binary-search-tree/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/check-if-a-tree-is-a-bst-or-not?category=medium&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Inorder strictly increasing](#3-inorder-strictly-increasing) · [4. Bounds recursion](#4-bounds-recursion) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a binary tree, determine whether it is a valid BST: each node's left subtree has only smaller keys, its right subtree only larger keys, and both subtrees are BSTs.

| Input | Output | Why |
|---|---|---|
| `root = [2,1,3]` | `true` |  |
| `root = [5,4,6,null,null,3,7]` | `false` | 3 < 6 locally, but it's in 5's right subtree, so it must be > 5 |

**Constraints:** `1 ≤ n ≤ 10⁴`; `−2³¹ ≤ val ≤ 2³¹ − 1`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Inorder strictly increasing | iterative inorder; compare with prev | O(n) | O(h) |
| Bounds recursion | valid(n, lo, hi): lo < n.val < hi, recurse with narrowed window | O(n) | O(h) |

> [!tip] Interview angle
> The values reach the int limits, so `INT_MIN`/`INT_MAX` sentinels break on `[2147483647]`. Use `long`, nullable bounds, or `±∞` in Python. Interviewers try exactly this input.

---

## 3. Inorder strictly increasing

**Intuition.** A tree is a BST iff its inorder sequence is strictly increasing. Track the previous value; the first non-increase fails.

```python
def is_bst_inorder(root):
    st, cur, prev = [], root, None
    while cur or st:
        while cur:
            st.append(cur)
            cur = cur.left
        cur = st.pop()
        if prev is not None and cur.val <= prev:
            return False
        prev = cur.val
        cur = cur.right
    return True
```

**Complexity:** time **O(n)**, space **O(h)**.

---

## 4. Bounds recursion

**Intuition.** Pass the open interval allowed for the subtree. The root gets (−∞, +∞). The left child inherits (lo, val) and the right child (val, hi).

**Algorithm**

1. `ok(n, lo, hi)`: null → true.
2. If not `lo < n.val < hi` → false.
3. Return `ok(n.left, lo, n.val) and ok(n.right, n.val, hi)`.

**Dry run** — [5,4,6,null,null,3,7]: ok(5,−∞,∞) → ok(4,−∞,5) ✓ → ok(6,5,∞) → ok(3,5,6): 3 ≤ 5 → false.

**C++**
```cpp
bool okB(TreeNode* n, long long lo, long long hi) {
    if (!n) return true;
    if (n->val <= lo || n->val >= hi) return false;
    return okB(n->left, lo, n->val) && okB(n->right, n->val, hi);
}
bool isValidBST(TreeNode* root) { return okB(root, LLONG_MIN, LLONG_MAX); }
```

**Java**
```java
static boolean okB(TreeNode n, long lo, long hi) {
    if (n == null) return true;
    if (n.val <= lo || n.val >= hi) return false;
    return okB(n.left, lo, n.val) && okB(n.right, n.val, hi);
}
static boolean isValidBST(TreeNode root) { return okB(root, Long.MIN_VALUE, Long.MAX_VALUE); }
```

**Python**
```python
def is_valid_bst(root):
    def ok(n, lo, hi):
        if not n:
            return True
        if not (lo < n.val < hi):
            return False
        return ok(n.left, lo, n.val) and ok(n.right, n.val, hi)
    return ok(root, float("-inf"), float("inf"))
```

**Complexity:** time **O(n)**, space **O(h)** — each node checked once against its window.

---

## Edge cases

- Empty tree → valid.
- Duplicates → invalid under the strict definition.
- Values at INT_MIN / INT_MAX.
- A violation deep in the tree against a distant ancestor.

---

## Common mistakes

1. Checking only `left.val < val < right.val`.
2. `int` sentinels that collide with legal values.
3. Allowing `≤` when the problem says strictly less (or vice versa).
4. Comparing with `prev` using `0` as the initial value (fails for negative trees).

---

## Follow-ups

1. Duplicates allowed on the left (≤)?
2. Largest BST subtree?
3. O(1) space?

<details><summary>Answer sketches</summary>

**#1:** Change the left bound check to `lo < val ≤ hi` and be consistent.

**#2:** Post-order returning (isBST, min, max, size). See the Largest BST problem.

**#3:** Morris inorder with a prev check (restore threads even on early failure).
</details>

---

## Flashcards

**Validate BST: the classic bug?** #flashcard
Comparing only with direct children; constraints come from all ancestors.

**Bounds recursion for the left child?** #flashcard
`(lo, node.val)`; right child `(node.val, hi)`.

**Inorder test for BST?** #flashcard
Inorder must be strictly increasing.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
