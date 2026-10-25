---
module: striver-a2z/25-binary-search-trees
lesson: 5
topic: Insert a given node in BST
difficulty: Medium
source: https://takeuforward.org/learning/dsa/insert-a-given-node-in-bst?category=medium&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search-trees, bst, insert]
---
# 5. Insert a given node in BST

← [Minimum and Maximum in BST](04-minimum-and-maximum-in-bst.md) · [Part 25 index](README.md) · Next → [Delete a node in BST](06-delete-node-in-bst.md)

> [!abstract] Problem at a glance
> **Task:** Insert `val` (not already present) and return the root.
> **Key insight:** Search for `val`. The null pointer where the search falls off the tree is exactly where it belongs. Attach a new leaf there. No existing node moves.
> **Difficulty:** Medium · **Pattern:** BST walk to a null slot · **Also on:** [LC 701](https://leetcode.com/problems/insert-into-a-binary-search-tree/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/insert-a-given-node-in-bst?category=medium&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursive (return subtree root)](#3-recursive-return-subtree-root) · [4. Iterative](#4-iterative) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a BST and a value `val` not in the tree, insert it and return the root. Any valid BST is accepted; the standard answer inserts as a leaf.

| Input | Output | Why |
|---|---|---|
| `root = [4,2,7,1,3], val = 5` | `[4,2,7,1,3,5]` | 5 > 4 → 7; 5 < 7 → left slot is free |
| `root = [], val = 5` | `[5]` | new root |

**Constraints:** `0 ≤ n ≤ 10⁴`; values distinct; `val` not in the tree.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursive (return subtree root) | root.side = insert(root.side, val) | O(h) | O(h) |
| Iterative | walk until the needed child is null, attach | O(h) | O(1) |

> [!tip] Interview angle
> Watch the empty-tree case: the function has to *return* the new root. The recursive `root.left = insert(root.left, val)` pattern returns subtree roots; delete reuses it, so learn it here.

---

## 3. Recursive (return subtree root)

**Intuition.** `insert(node)` returns the root of the subtree after insertion. A null subtree becomes a new node, and any other node returns itself after updating one child.

```python
def insert_rec(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert_rec(root.left, val)
    else:
        root.right = insert_rec(root.right, val)
    return root
```

**Complexity:** time **O(h)**, space **O(h)**.

---

## 4. Iterative

**Intuition.** Walk down. At each node, if the child on `val`'s side is null, attach there and stop. Otherwise step into it.

**Algorithm**

1. If root is null, return a new node.
2. `cur = root`. Loop: if `val < cur.val`: if `cur.left` is null attach and break, else go left. Mirror for right.
3. Return root.

**Dry run** — [5,3,8,2,4,7,9], val 6: 6 > 5 → 8; 6 < 8 → 7; 6 < 7 and 7.left is null → attach 6 as 7.left.

**C++**
```cpp
TreeNode* insertIntoBST(TreeNode* root, int val) {
    TreeNode* node = new TreeNode(val);
    if (!root) return node;
    TreeNode* cur = root;
    while (true) {
        if (val < cur->val) {
            if (!cur->left) { cur->left = node; break; }
            cur = cur->left;
        } else {
            if (!cur->right) { cur->right = node; break; }
            cur = cur->right;
        }
    }
    return root;
}
```

**Java**
```java
static TreeNode insertIntoBST(TreeNode root, int val) {
    TreeNode node = new TreeNode(val);
    if (root == null) return node;
    TreeNode cur = root;
    while (true) {
        if (val < cur.val) {
            if (cur.left == null) { cur.left = node; break; }
            cur = cur.left;
        } else {
            if (cur.right == null) { cur.right = node; break; }
            cur = cur.right;
        }
    }
    return root;
}
```

**Python**
```python
def insert_into_bst(root, val):
    node = TreeNode(val)
    if not root:
        return node
    cur = root
    while True:
        if val < cur.val:
            if not cur.left:
                cur.left = node
                break
            cur = cur.left
        else:
            if not cur.right:
                cur.right = node
                break
            cur = cur.right
    return root
```

**Complexity:** time **O(h)**, space **O(1)** — one root-to-leaf walk; no rebalancing.

---

## Edge cases

- Empty tree → the new node is the root.
- Insert below the min / above the max → extends a spine.
- Inserting sorted values one by one → a skewed tree (h = n).

---

## Common mistakes

1. Walking to `cur = null` and then trying to attach: you've lost the parent.
2. Forgetting to return the root in the recursive version.
3. Not handling `root == null`.

---

## Follow-ups

1. Duplicates allowed?
2. Keep the tree balanced?
3. Build a BST from an unsorted array?

<details><summary>Answer sketches</summary>

**#1:** Pick a convention (e.g. equal goes right) and use it for search and delete too, or store a count per node.

**#2:** AVL/red-black rotations after insert; mention, don't implement.

**#3:** n inserts: O(n log n) average, O(n²) worst (sorted input). From sorted input, build mid-first for a balanced tree.
</details>

---

## Flashcards

**Where does a new value go in a BST?** #flashcard
At the null slot where an unsuccessful search for it ends; always as a leaf.

**Recursive insert idiom?** #flashcard
`root.left = insert(root.left, val)`; the function returns the subtree root.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
