---
module: striver-a2z/25-binary-search-trees
lesson: 6
topic: Delete a node in BST
difficulty: Medium
source: https://takeuforward.org/learning/dsa/delete-a-node-in-bst?category=medium&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search-trees, bst, delete]
---
# 6. Delete a node in BST

← [Insert a given node in BST](05-insert-into-bst.md) · [Part 25 index](README.md) · Next → [Kth Smallest and Largest element in BST](07-kth-smallest-largest-in-bst.md)

> [!abstract] Problem at a glance
> **Task:** Remove the node with value `key` (if present) and return the root.
> **Key insight:** Leaves and one-child nodes are easy: replace the node with its only child (or null). For **two children**, either (a) copy the inorder successor's value up and delete the successor, or (b) splice: hang the right subtree off the rightmost node of the left subtree and return the left subtree. Both keep inorder order intact.
> **Difficulty:** Medium · **Pattern:** BST walk + case split · **Also on:** [LC 450](https://leetcode.com/problems/delete-node-in-a-bst/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/delete-a-node-in-bst?category=medium&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursive, successor copy](#3-recursive-successor-copy) · [4. Iterative, splice](#4-iterative-splice) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a BST and a `key`, delete the node with that value if it exists and return the (possibly new) root. Any valid result is accepted.

| Input | Output | Why |
|---|---|---|
| `root = [5,3,6,2,4,null,7], key = 3` | `[5,2,6,null,4,null,7]` | splice: 3's left (2) takes its place; 4 hangs off 2's right |
| `root = [5,3,6,2,4,null,7], key = 0` | `[5,3,6,2,4,null,7]` | key absent → unchanged |

**Constraints:** `0 ≤ n ≤ 10⁴`; values distinct; `−10⁵ ≤ key ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursive, successor copy | find; 0/1 child → return child; 2 children → copy min of right, delete it there | O(h) | O(h) |
| Iterative, splice | find parent; replace child with helper(child) | O(h) | O(1) |

> [!tip] Interview angle
> Name the three cases before you code. The successor-copy method is the textbook answer and keeps the height change small. The splice is shorter but can deepen the tree. Either is accepted; say which you're using and why.

---

## 3. Recursive, successor copy

**Intuition.** `delete(node, key)` returns the new subtree root. When `node` is the target with two children, its inorder successor (leftmost of the right subtree) has no left child. Copy its value into `node`, then delete that value from the right subtree. That delete is the easy case.

```python
def delete_succ(root, key):
    if not root:
        return None
    if key < root.val:
        root.left = delete_succ(root.left, key)
    elif key > root.val:
        root.right = delete_succ(root.right, key)
    else:
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        s = root.right
        while s.left:
            s = s.left
        root.val = s.val
        root.right = delete_succ(root.right, s.val)
    return root
```

**Complexity:** time **O(h)**, space **O(h)**.

---

## 4. Iterative, splice

**Intuition.** `helper(n)` returns what should replace `n`. With no left child that's `n.right`, and with no right child it's `n.left`. With both, everything in `n.right` is larger than everything in `n.left`, so attach `n.right` as the right child of the **rightmost node of `n.left`** and return `n.left`. Inorder order is unchanged.

**Algorithm**

1. If root is null → null. If `root.val == key` → return `helper(root)`.
2. Walk with `cur`: if `key < cur.val`: if `cur.left.val == key` → `cur.left = helper(cur.left)`, stop; else go left. Mirror on the right.
3. `helper(n)`: no left → `n.right`; no right → `n.left`; else `last` = rightmost of `n.left`; `last.right = n.right`; return `n.left`.

**Dry run** — [5,3,6,2,4,null,7], key 5 (root, two children): rightmost of left subtree {3,2,4} is 4; 4.right = 6; return 3. Result 3 → (2, 4), 4 → (null, 6), 6 → (null, 7).

**C++**
```cpp
TreeNode* helperDel(TreeNode* n) {
    if (!n->left) return n->right;
    if (!n->right) return n->left;
    TreeNode* last = n->left;
    while (last->right) last = last->right;
    last->right = n->right;
    return n->left;
}
TreeNode* deleteNode(TreeNode* root, int key) {
    if (!root) return nullptr;
    if (root->val == key) return helperDel(root);
    TreeNode* cur = root;
    while (cur) {
        if (key < cur->val) {
            if (cur->left && cur->left->val == key) { cur->left = helperDel(cur->left); break; }
            cur = cur->left;
        } else {
            if (cur->right && cur->right->val == key) { cur->right = helperDel(cur->right); break; }
            cur = cur->right;
        }
    }
    return root;
}
```

**Java**
```java
static TreeNode helperDel(TreeNode n) {
    if (n.left == null) return n.right;
    if (n.right == null) return n.left;
    TreeNode last = n.left;
    while (last.right != null) last = last.right;
    last.right = n.right;
    return n.left;
}
static TreeNode deleteNode(TreeNode root, int key) {
    if (root == null) return null;
    if (root.val == key) return helperDel(root);
    TreeNode cur = root;
    while (cur != null) {
        if (key < cur.val) {
            if (cur.left != null && cur.left.val == key) { cur.left = helperDel(cur.left); break; }
            cur = cur.left;
        } else {
            if (cur.right != null && cur.right.val == key) { cur.right = helperDel(cur.right); break; }
            cur = cur.right;
        }
    }
    return root;
}
```

**Python**
```python
def delete_node(root, key):
    def helper(n):
        if not n.left:
            return n.right
        if not n.right:
            return n.left
        last = n.left
        while last.right:
            last = last.right
        last.right = n.right
        return n.left
    if not root:
        return None
    if root.val == key:
        return helper(root)
    cur = root
    while cur:
        if key < cur.val:
            if cur.left and cur.left.val == key:
                cur.left = helper(cur.left)
                break
            cur = cur.left
        else:
            if cur.right and cur.right.val == key:
                cur.right = helper(cur.right)
                break
            cur = cur.right
    return root
```

**Complexity:** time **O(h)**, space **O(1)** — one walk to the key plus one walk down the left subtree's right spine.

---

## Edge cases

- Key absent → unchanged tree.
- Deleting the root (a new root is returned).
- Deleting the only node → empty tree.
- Deleting a leaf.

---

## Common mistakes

1. Not returning the new root when the root itself is deleted.
2. Two-children case: attaching `n.left` under `n.right`'s *rightmost* node (it must go under the right subtree's **leftmost**, or the right under the left's rightmost).
3. Successor copy: deleting the successor from the whole tree instead of from `root.right`.

---

## Follow-ups

1. Which keeps the tree shallower?
2. Delete all nodes outside [lo, hi] (LC 669 Trim BST)?
3. Predecessor instead of successor?

<details><summary>Answer sketches</summary>

**#1:** Successor copy: height grows by at most 0. The splice can add the left subtree's height to the right subtree's depth.

**#2:** Recursive: if `val < lo` return trim(right); if `val > hi` return trim(left); else trim both children.

**#3:** Symmetric: rightmost of the left subtree; either is valid.
</details>

---

## Flashcards

**Delete in BST: three cases?** #flashcard
Leaf → null; one child → that child; two children → successor copy or splice.

**Splice for a two-child node?** #flashcard
Attach the right subtree to the rightmost node of the left subtree; return the left subtree.

**Why does the inorder successor of a two-child node have no left child?** #flashcard
It's the leftmost node of the right subtree.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
