---
module: striver/25-binary-search-trees
lesson: 9
topic: LCA in BST
difficulty: Medium
source: https://takeuforward.org/learning/dsa/lca-in-bst?category=medium&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search-trees, bst, lca]
---
# 9. LCA in BST

← [Check if a tree is a BST or not](08-validate-bst.md) · [Part 25 index](README.md) · Next → [Construct a BST from a preorder traversal](10-bst-from-preorder.md)

> [!abstract] Problem at a glance
> **Task:** Return the lowest common ancestor of nodes `p` and `q` in a BST.
> **Key insight:** While both values are smaller than the current node, the LCA is to the left; while both are larger, it's to the right. The **first node where they split** (or where one equals the node) is the LCA. One walk, no recursion into both sides.
> **Difficulty:** Medium · **Pattern:** BST split point · **Also on:** [LC 235](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/lca-in-bst?category=medium&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursive split](#3-recursive-split) · [4. Iterative split](#4-iterative-split) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a BST and two nodes `p` and `q` that are both in it, return their lowest common ancestor (a node may be its own ancestor).

| Input | Output | Why |
|---|---|---|
| `root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8` | `6` | they split at the root |
| `same tree, p = 2, q = 4` | `2` | 2 is an ancestor of 4 |

**Constraints:** `2 ≤ n ≤ 10⁵`; values distinct; `p ≠ q`; both exist.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursive split | both < → left; both > → right; else root | O(h) | O(h) |
| Iterative split | loop until p and q fall on different sides | O(h) | O(1) |

> [!tip] Interview angle
> Contrast it with LCA in a general binary tree (O(n), post-order). Here ordering gives O(h) and O(1) space. If the nodes might not exist, verify with two searches.

---

## 3. Recursive split

**Intuition.** Direct recursion on the three cases.

```python
def lca_rec(root, p, q):
    if p.val < root.val and q.val < root.val:
        return lca_rec(root.left, p, q)
    if p.val > root.val and q.val > root.val:
        return lca_rec(root.right, p, q)
    return root
```

**Complexity:** time **O(h)**, space **O(h)**.

---

## 4. Iterative split

**Intuition.** Tail recursion → loop.

**Algorithm**

1. `cur = root`.
2. Loop: if both `< cur.val` → left; elif both `> cur.val` → right; else return `cur`.

**Dry run** — p = 3, q = 5: 6 → both smaller → 2 → both larger → 4 → 3 < 4 < 5 → split → 4.

**C++**
```cpp
TreeNode* lcaBST(TreeNode* root, TreeNode* p, TreeNode* q) {
    TreeNode* cur = root;
    while (cur) {
        if (p->val < cur->val && q->val < cur->val) cur = cur->left;
        else if (p->val > cur->val && q->val > cur->val) cur = cur->right;
        else return cur;
    }
    return nullptr;
}
```

**Java**
```java
static TreeNode lcaBST(TreeNode root, TreeNode p, TreeNode q) {
    TreeNode cur = root;
    while (cur != null) {
        if (p.val < cur.val && q.val < cur.val) cur = cur.left;
        else if (p.val > cur.val && q.val > cur.val) cur = cur.right;
        else return cur;
    }
    return null;
}
```

**Python**
```python
def lca_bst(root, p, q):
    cur = root
    while cur:
        if p.val < cur.val and q.val < cur.val:
            cur = cur.left
        elif p.val > cur.val and q.val > cur.val:
            cur = cur.right
        else:
            return cur
    return None
```

**Complexity:** time **O(h)**, space **O(1)** — one downward walk.

---

## Edge cases

- One node is the ancestor of the other → it's the LCA.
- p and q on either side of the root → root.
- Skewed tree → O(n).

---

## Common mistakes

1. Using the general binary-tree LCA (correct but O(n), misses the point).
2. Comparing node references instead of values for the direction test.
3. Strict vs non-strict comparisons: equality must fall into the 'return cur' branch.

---

## Follow-ups

1. Distance between two nodes in a BST?
2. Nodes may be absent?
3. LCA of many nodes?

<details><summary>Answer sketches</summary>

**#1:** depth(p) + depth(q) − 2·depth(LCA), all via BST walks.

**#2:** Search for both first; return null if either is missing.

**#3:** Use min and max of the set: the split point of min and max.
</details>

---

## Flashcards

**LCA in BST: rule?** #flashcard
First node with `min(p,q) ≤ node ≤ max(p,q)` on the walk from the root.

**LCA in BST: complexity?** #flashcard
O(h) time, O(1) space iteratively.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
