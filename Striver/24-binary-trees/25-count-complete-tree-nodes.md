---
module: striver/24-binary-trees
lesson: 25
topic: Count total Nodes in a COMPLETE BT
difficulty: Medium
source: https://takeuforward.org/learning/dsa/count-total-nodes-in-a-complete-bt?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, complete-tree, binary-search, divide-and-conquer]
---
# 25. Count total Nodes in a COMPLETE BT

← [Minimum time taken to burn the BT from a given Node](24-burn-binary-tree.md) · [Part 24 index](README.md) · Next → [Flatten Binary Tree to LinkedList](26-flatten-binary-tree.md)

> [!abstract] Problem at a glance
> **Task:** Count nodes in a complete binary tree faster than O(n).
> **Key insight:** Measure the leftmost and rightmost depths. If they are equal, the subtree is **perfect** with `2^h − 1` nodes, so stop. Otherwise recurse into both children: `1 + count(L) + count(R)`. At every level at least one of the two children is perfect, so there are O(log n) recursive calls, each costing O(log n).
> **Difficulty:** Medium · **Pattern:** Perfect-subtree shortcut · **Also on:** [LC 222](https://leetcode.com/problems/count-complete-tree-nodes/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-total-nodes-in-a-complete-bt?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Plain traversal](#3-plain-traversal) · [4. Left/right height shortcut](#4-leftright-height-shortcut) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a **complete** binary tree (every level full except possibly the last, which is filled from the left), return the number of nodes. Design an algorithm that runs in less than O(n).

| Input | Output | Why |
|---|---|---|
| `root = [1,2,3,4,5,6]` | `6` |  |
| `root = [1]` | `1` |  |

**Constraints:** `0 ≤ n ≤ 5·10⁴`; the tree is complete.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Plain traversal | 1 + count(L) + count(R) | O(n) | O(h) |
| Left/right height shortcut | hl == hr → 2^h − 1 else 1 + rec(L) + rec(R) | O(log² n) | O(log n) |

> [!tip] Interview angle
> State the complexity argument: when the left and right heights differ, at least one child subtree is perfect and returns in O(log n). Only one path is ever explored deeply, which gives O(log² n). The binary search on the last level (by bit path) is an alternative with the same bound.

---

## 3. Plain traversal

**Intuition.** It ignores completeness. It's correct, but not what the question asks for.

```python
def count_nodes_naive(root):
    return 0 if not root else 1 + count_nodes_naive(root.left) + count_nodes_naive(root.right)
```

**Complexity:** time **O(n)**, space **O(h)**.

---

## 4. Left/right height shortcut

**Intuition.** In a complete tree, equal left-spine and right-spine depths means every level is full.

**Algorithm**

1. If null → 0.
2. `hl` = depth following `.left` from root; `hr` = depth following `.right`.
3. If `hl == hr` → return `(1 << hl) − 1`.
4. Else return `1 + count(left) + count(right)`.

**Dry run** — [1,2,3,4,5,6]: hl=3, hr=2 → recurse. Left (2,4,5): hl=hr=2 → 3. Right (3,6): hl=2, hr=1 → 1 + count(6)=1 + 0 → 2. Total 1+3+2=6.

**C++**
```cpp
int countNodes(TreeNode* root) {
    if (!root) return 0;
    int hl = 0, hr = 0;
    for (TreeNode* n = root; n; n = n->left) hl++;
    for (TreeNode* n = root; n; n = n->right) hr++;
    if (hl == hr) return (1 << hl) - 1;
    return 1 + countNodes(root->left) + countNodes(root->right);
}
```

**Java**
```java
static int countNodes(TreeNode root) {
    if (root == null) return 0;
    int hl = 0, hr = 0;
    for (TreeNode n = root; n != null; n = n.left) hl++;
    for (TreeNode n = root; n != null; n = n.right) hr++;
    if (hl == hr) return (1 << hl) - 1;
    return 1 + countNodes(root.left) + countNodes(root.right);
}
```

**Python**
```python
def count_nodes(root):
    if not root:
        return 0
    hl, n = 0, root
    while n:
        hl, n = hl + 1, n.left
    hr, n = 0, root
    while n:
        hr, n = hr + 1, n.right
    if hl == hr:
        return (1 << hl) - 1
    return 1 + count_nodes(root.left) + count_nodes(root.right)
```

**Complexity:** time **O(log² n)**, space **O(log n)** — O(log n) levels of recursion where work happens, O(log n) height measurement each.

---

## Edge cases

- Perfect tree → shortcut fires at the root.
- Last level has a single node.
- Empty tree.

---

## Common mistakes

1. Comparing `height(left)` vs `height(right)` with full height functions (O(n) per call).
2. `2 ** h` with h in edges instead of nodes (off by one).
3. Applying the shortcut to a non-complete tree.

---

## Follow-ups

1. Binary search approach?
2. Is a tree complete?

<details><summary>Answer sketches</summary>

**#1:** Last level indices 0..2^(h−1)−1; test existence via bit path in O(h); total O(h²).

**#2:** BFS: once a null child is seen, no non-null node may follow (LC 958).
</details>

---

## Flashcards

**Complete tree count shortcut?** #flashcard
Leftmost depth == rightmost depth → 2^h − 1 nodes.

**Complexity of complete-tree count?** #flashcard
O(log² n).

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
