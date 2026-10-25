---
module: striver-a2z/25-binary-search-trees
lesson: 2
topic: Search in BST
difficulty: Easy
source: https://takeuforward.org/learning/dsa/search-in-bst?category=theory-and-basics&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search-trees, bst, search]
---
# 2. Search in BST

← [Binary Search Trees: Invariant, Walks, Insert/Delete and Inorder](01-bst-theory.md) · [Part 25 index](README.md) · Next → [Floor and Ceil in a BST](03-floor-and-ceil-in-a-bst.md)

> [!abstract] Problem at a glance
> **Task:** Return the subtree rooted at the node whose value is `val`, or null.
> **Key insight:** The BST invariant tells you which side the target must be on, so you never explore both children. The search is a single root-to-leaf walk: O(h), not O(n). Because it's tail recursion, write it as a loop.
> **Difficulty:** Easy · **Pattern:** BST walk · **Also on:** [LC 700](https://leetcode.com/problems/search-in-a-binary-search-tree/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/search-in-bst?category=theory-and-basics&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursive](#3-recursive) · [4. Iterative walk](#4-iterative-walk) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a BST and an integer `val`, find the node whose value equals `val` and return the subtree rooted there. Return `null` if it doesn't exist.

| Input | Output | Why |
|---|---|---|
| `root = [4,2,7,1,3], val = 2` | `[2,1,3]` | 2 < 4 → go left; found |
| `root = [4,2,7,1,3], val = 5` | `[]` | 5 > 4 → right to 7; 5 < 7 → left is null |

**Constraints:** `1 ≤ n ≤ 5000`; values distinct; `1 ≤ val ≤ 10⁷`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursive | compare, recurse into one side | O(h) | O(h) |
| Iterative walk | while cur and cur.val != val: step left/right | O(h) | O(1) |

> [!tip] Interview angle
> This is a warm-up. State O(h) and that h is log n only when the tree is balanced. The walk becomes the skeleton of floor/ceil, insert, delete, LCA and successor, so write it cleanly.

---

## 3. Recursive

**Intuition.** If the node is null or matches, return it. Otherwise recurse into the only side that can contain `val`.

```python
def search_rec(root, val):
    if not root or root.val == val:
        return root
    return search_rec(root.left if val < root.val else root.right, val)
```

**Complexity:** time **O(h)**, space **O(h)**.

---

## 4. Iterative walk

**Intuition.** The recursion is a tail call, so a loop that moves `cur` replaces it and uses no stack.

**Algorithm**

1. `cur = root`.
2. While `cur` and `cur.val != val`: `cur = cur.left` if `val < cur.val` else `cur.right`.
3. Return `cur`.

**Dry run** — [4,2,7,1,3], val 2: 4 → 2 < 4 → node 2 → match. val 5: 4 → right 7 → left null → return null.

**C++**
```cpp
TreeNode* searchBST(TreeNode* root, int val) {
    TreeNode* cur = root;
    while (cur && cur->val != val)
        cur = val < cur->val ? cur->left : cur->right;
    return cur;
}
```

**Java**
```java
static TreeNode searchBST(TreeNode root, int val) {
    TreeNode cur = root;
    while (cur != null && cur.val != val)
        cur = val < cur.val ? cur.left : cur.right;
    return cur;
}
```

**Python**
```python
def search_bst(root, val):
    cur = root
    while cur and cur.val != val:
        cur = cur.left if val < cur.val else cur.right
    return cur
```

**Complexity:** time **O(h)**, space **O(1)** — one comparison per level; no stack.

---

## Edge cases

- Empty tree → null.
- Target is the root → whole tree.
- Skewed BST → O(n) walk.

---

## Common mistakes

1. Searching both subtrees (O(n)), which ignores the invariant.
2. Returning `cur.val` instead of the node.
3. Claiming O(log n) without saying 'balanced'.

---

## Follow-ups

1. Closest value to a target?
2. Search for a range [lo, hi]?
3. Guarantee O(log n)?

<details><summary>Answer sketches</summary>

**#1:** Same walk; track `best` by |cur.val − target|.

**#2:** Prune: recurse left only if `lo < val`, right only if `val < hi`. O(h + k).

**#3:** Self-balancing BST (AVL, red-black), e.g. `std::map`, `TreeMap`.
</details>

---

## Flashcards

**Search in BST: time and space (iterative)?** #flashcard
O(h) time, O(1) space.

**When is h = log n?** #flashcard
Only if the BST is balanced; a sorted insertion order gives h = n.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
