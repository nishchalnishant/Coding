---
module: striver-a2z/25-binary-search-trees
lesson: 11
topic: Inorder successor and predecessor in BST
difficulty: Medium
source: https://takeuforward.org/learning/dsa/inorder-successor-and-predecessor-in-bst?category=medium&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search-trees, bst, successor, predecessor]
---
# 11. Inorder successor and predecessor in BST

← [Construct a BST from a preorder traversal](10-bst-from-preorder.md) · [Part 25 index](README.md) · Next → [BST iterator](12-bst-iterator.md)

> [!abstract] Problem at a glance
> **Task:** Return `[predecessor, successor]` of `key`: the largest value < key and the smallest value > key (−1 if none).
> **Key insight:** This is floor/ceil with **strict** inequalities. Walking down, every time you go left past a node, that node is a successor candidate (it's bigger and may be the closest). Every time you go right, the node is a predecessor candidate. It works even if `key` isn't in the tree.
> **Difficulty:** Medium · **Pattern:** BST walk + candidate tracking · **Also on:** [LC 285](https://leetcode.com/problems/inorder-successor-in-bst/) (premium)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/inorder-successor-and-predecessor-in-bst?category=medium&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Inorder list](#3-inorder-list) · [4. Two candidate walks](#4-two-candidate-walks) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a BST and a value `key`, find its inorder predecessor and successor. Return `-1` for a side that doesn't exist.

| Input | Output | Why |
|---|---|---|
| `root = [5,3,8,2,4,7,9], key = 5` | `[4,7]` | max of left subtree, min of right subtree |
| `root = [5,3,8,2,4,7,9], key = 2` | `[-1,3]` | 2 is the minimum |

**Constraints:** `1 ≤ n ≤ 10⁴`; values distinct.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Inorder list | sorted list; neighbours of key | O(n) | O(n) |
| Two candidate walks | succ: go left → record; pred: go right → record | O(h) | O(1) |

> [!tip] Interview angle
> The textbook answer has two cases: if the node has a right child, the successor is the leftmost of it; otherwise it's the nearest ancestor you went left from. The candidate walk below handles both cases in one loop. It also needs no parent pointers.

---

## 3. Inorder list

**Intuition.** Inorder, then scan for the largest < key and the smallest > key.

```python
def pred_succ_brute(root, key):
    a = []
    def go(n):
        if n:
            go(n.left); a.append(n.val); go(n.right)
    go(root)
    p = max((v for v in a if v < key), default=-1)
    s = min((v for v in a if v > key), default=-1)
    return [p, s]
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Two candidate walks

**Intuition.** Successor: if `cur.val > key`, record it and go left to look for something closer. Otherwise go right, and equality also goes right. Predecessor mirrors this.

**Algorithm**

1. `s = -1`; walk: `cur.val > key` → `s = cur.val`, left; else right.
2. `p = -1`; walk: `cur.val < key` → `p = cur.val`, right; else left.
3. Return `[p, s]`.

**Dry run** — [5,3,8,2,4,7,9], key 5. Succ: 5 not > 5 → right 8; 8 > 5 → s 8, left 7; 7 > 5 → s 7, left null → 7. Pred: 5 not < 5 → left 3; 3 < 5 → p 3, right 4; 4 < 5 → p 4, right null → 4.

**C++**
```cpp
vector<int> predSucc(TreeNode* root, int key) {
    int p = -1, s = -1;
    for (TreeNode* cur = root; cur; )
        if (cur->val > key) { s = cur->val; cur = cur->left; } else cur = cur->right;
    for (TreeNode* cur = root; cur; )
        if (cur->val < key) { p = cur->val; cur = cur->right; } else cur = cur->left;
    return {p, s};
}
```

**Java**
```java
static int[] predSucc(TreeNode root, int key) {
    int p = -1, s = -1;
    for (TreeNode cur = root; cur != null; )
        if (cur.val > key) { s = cur.val; cur = cur.left; } else cur = cur.right;
    for (TreeNode cur = root; cur != null; )
        if (cur.val < key) { p = cur.val; cur = cur.right; } else cur = cur.left;
    return new int[]{p, s};
}
```

**Python**
```python
def pred_succ(root, key):
    s, cur = -1, root
    while cur:
        if cur.val > key:
            s, cur = cur.val, cur.left
        else:
            cur = cur.right
    p, cur = -1, root
    while cur:
        if cur.val < key:
            p, cur = cur.val, cur.right
        else:
            cur = cur.left
    return [p, s]
```

**Complexity:** time **O(h)**, space **O(1)** — two root-to-leaf walks.

---

## Edge cases

- Key is the min → no predecessor.
- Key is the max → no successor.
- Key absent → still well defined.
- Single node.

---

## Common mistakes

1. Going left on equality for the successor (you'd record smaller values).
2. Only handling the 'right subtree exists' case.
3. Confusing predecessor/successor with floor/ceil (strict vs non-strict).

---

## Follow-ups

1. Given a node with parent pointers (LC 510)?
2. Successor in a general binary tree?
3. Used where?

<details><summary>Answer sketches</summary>

**#1:** Right child exists → leftmost of right; else climb until you arrive from a left child.

**#2:** Inorder traversal with prev tracking: O(n).

**#3:** Deleting a two-child node, BST iterator, range queries.
</details>

---

## Flashcards

**Inorder successor in BST (walk)?** #flashcard
Record the node whenever you go left (`cur.val > key`); the last one recorded is the answer.

**Successor when the node has a right child?** #flashcard
Leftmost node of its right subtree.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
