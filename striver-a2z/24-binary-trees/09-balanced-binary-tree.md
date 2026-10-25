---
module: striver-a2z/24-binary-trees
lesson: 9
topic: Check for balanced binary tree
difficulty: Easy
source: https://takeuforward.org/learning/dsa/check-for-balanced-binary-tree?category=medium-problems&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, dfs, postorder, height]
---
# 9. Check for balanced binary tree

← [Check if two trees are identical or not](08-same-tree.md) · [Part 24 index](README.md) · Next → [Diameter of Binary Tree](10-diameter-of-binary-tree.md)

> [!abstract] Problem at a glance
> **Task:** Is every node's |height(left) − height(right)| ≤ 1?
> **Key insight:** Compute height bottom-up and use **−1 as an 'unbalanced' sentinel**. Once any subtree is unbalanced, the −1 propagates to the root and no more work is needed. One pass, O(n).
> **Difficulty:** Easy · **Pattern:** Postorder with sentinel · **Also on:** [LC 110](https://leetcode.com/problems/balanced-binary-tree/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/check-for-balanced-binary-tree?category=medium-problems&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Top-down height at every node](#3-top-down-height-at-every-node) · [4. Bottom-up height with −1 sentinel](#4-bottom-up-height-with-1-sentinel) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a binary tree, determine if it is height-balanced: for **every** node, the heights of its left and right subtrees differ by at most one.

| Input | Output | Why |
|---|---|---|
| `root = [3,9,20,null,null,15,7]` | `true` |  |
| `root = [1,2,2,3,3,null,null,4,4]` | `false` | root: left height 3, right height 1 |

**Constraints:** `0 ≤ n ≤ 5000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Top-down height at every node | check |h(L) − h(R)| then recurse | O(n²) worst, O(n log n) balanced | O(h) |
| Bottom-up height with −1 sentinel | h = −1 if a child is −1 or |hl − hr| > 1 | O(n) | O(h) |

> [!tip] Interview angle
> The naive version calls `height()` at every node, which is O(n²) on a skewed tree. The interviewer wants you to fold the check into the height computation. 'Return a sentinel or a pair from postorder' is the pattern behind diameter and max path sum too.

---

## 3. Top-down height at every node

**Intuition.** It's a direct translation of the definition, but each node's height is recomputed by every ancestor.

```python
def is_balanced_naive(root):
    def h(n):
        return 0 if not n else 1 + max(h(n.left), h(n.right))
    if not root:
        return True
    return abs(h(root.left) - h(root.right)) <= 1 and is_balanced_naive(root.left) and is_balanced_naive(root.right)
```

**Complexity:** time **O(n²) worst, O(n log n) balanced**, space **O(h)**.

---

## 4. Bottom-up height with −1 sentinel

**Intuition.** Return the height if the subtree is balanced, else −1. A parent checks its children's results before combining them, so the answer bubbles up in one postorder pass.

**Algorithm**

1. `h(null) = 0`.
2. `l = h(left)`; if −1 return −1.
3. `r = h(right)`; if −1 return −1.
4. If `|l − r| > 1` return −1.
5. Return `1 + max(l, r)`.
6. Answer: `h(root) != −1`.

**Dry run** — [1,2,2,3,3,null,null,4,4]: 4,4 → 1; node 3 (with 4s) → 2; other 3 → 1; node 2 → 3; right 2 → 1; root |3−1|=2 → −1 → false.

**C++**
```cpp
int balH(TreeNode* n) {
    if (!n) return 0;
    int l = balH(n->left);
    if (l < 0) return -1;
    int r = balH(n->right);
    if (r < 0 || abs(l - r) > 1) return -1;
    return 1 + max(l, r);
}
bool isBalanced(TreeNode* root) { return balH(root) >= 0; }
```

**Java**
```java
static int balH(TreeNode n) {
    if (n == null) return 0;
    int l = balH(n.left);
    if (l < 0) return -1;
    int r = balH(n.right);
    if (r < 0 || Math.abs(l - r) > 1) return -1;
    return 1 + Math.max(l, r);
}
static boolean isBalanced(TreeNode root) { return balH(root) >= 0; }
```

**Python**
```python
def is_balanced(root):
    def h(n):
        if not n:
            return 0
        l = h(n.left)
        if l < 0:
            return -1
        r = h(n.right)
        if r < 0 or abs(l - r) > 1:
            return -1
        return 1 + max(l, r)
    return h(root) >= 0
```

**Complexity:** time **O(n)**, space **O(h)** — each node's height is computed exactly once.

---

## Edge cases

- Empty tree is balanced.
- Balanced at the root but not deeper (last test) — every node must satisfy it.
- Right-skewed of 3 nodes → false.

---

## Common mistakes

1. Checking only the root's two heights.
2. Forgetting to propagate −1 (computing `1 + max(-1, x)`).
3. Confusing balanced with complete/perfect.

---

## Follow-ups

1. Return the pair (balanced, height) instead?
2. Make it balanced (BST)?

<details><summary>Answer sketches</summary>

**#1:** Same thing — tuple instead of sentinel; cleaner in languages with tuples.

**#2:** Inorder to sorted array, rebuild from middle (LC 1382).
</details>

---

## Flashcards

**Balanced tree check in O(n)?** #flashcard
Postorder height returning −1 as 'unbalanced' sentinel.

**Why is the naive balanced check O(n²)?** #flashcard
Every ancestor recomputes the height of every subtree.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
