---
module: striver/25-binary-search-trees
lesson: 4
topic: Minimum and Maximum in BST
difficulty: Easy
source: https://takeuforward.org/learning/dsa/minimum-and-maximum-in-bst?category=theory-and-basics&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search-trees, bst]
---
# 4. Minimum and Maximum in BST

← [Floor and Ceil in a BST](03-floor-and-ceil-in-a-bst.md) · [Part 25 index](README.md) · Next → [Insert a given node in BST](05-insert-into-bst.md)

> [!abstract] Problem at a glance
> **Task:** Return `[min, max]` of a non-empty BST.
> **Key insight:** The minimum is the **leftmost** node and the maximum is the **rightmost** node. Follow one pointer until it's null. This is also the 'go far left/right' helper used in delete, successor and Morris.
> **Difficulty:** Easy · **Pattern:** BST spine walk · **Also on:** [GfG Min in BST](https://www.geeksforgeeks.org/problems/minimum-element-in-bst/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/minimum-and-maximum-in-bst?category=theory-and-basics&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Full traversal](#3-full-traversal) · [4. Spine walks](#4-spine-walks) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a non-empty BST, return its minimum and maximum values.

| Input | Output | Why |
|---|---|---|
| `root = [5,3,8,2,4,7,9]` | `[2,9]` | leftmost 2, rightmost 9 |
| `root = [5,4,null,3]` | `[3,5]` | no right child: the root is the max |

**Constraints:** `1 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Full traversal | visit all, track min/max | O(n) | O(h) |
| Spine walks | leftmost = min, rightmost = max | O(h) | O(1) |

> [!tip] Interview angle
> Mention that in a plain binary tree this needs a full O(n) traversal, while the BST makes it O(h). That contrast is the point of the question.

---

## 3. Full traversal

**Intuition.** Works for any binary tree but ignores the ordering.

```python
def min_max_brute(root):
    mn, mx = float("inf"), float("-inf")
    st = [root]
    while st:
        n = st.pop()
        mn, mx = min(mn, n.val), max(mx, n.val)
        st += [c for c in (n.left, n.right) if c]
    return [mn, mx]
```

**Complexity:** time **O(n)**, space **O(h)**.

---

## 4. Spine walks

**Intuition.** Every left step goes to smaller values and every right step to larger ones. The node with no left child at the end of the left spine is the minimum.

**Algorithm**

1. `lo = root`; while `lo.left`: `lo = lo.left`.
2. `hi = root`; while `hi.right`: `hi = hi.right`.
3. Return `[lo.val, hi.val]`.

**Dry run** — [10,5,15,null,7,12]: left spine 10 → 5 (5 has no left) → min 5. Right spine 10 → 15 → max 15. Node 7 is in 5's right subtree but is irrelevant.

**C++**
```cpp
vector<int> minMax(TreeNode* root) {
    TreeNode *lo = root, *hi = root;
    while (lo->left) lo = lo->left;
    while (hi->right) hi = hi->right;
    return {lo->val, hi->val};
}
```

**Java**
```java
static int[] minMax(TreeNode root) {
    TreeNode lo = root, hi = root;
    while (lo.left != null) lo = lo.left;
    while (hi.right != null) hi = hi.right;
    return new int[]{lo.val, hi.val};
}
```

**Python**
```python
def min_max(root):
    lo = hi = root
    while lo.left:
        lo = lo.left
    while hi.right:
        hi = hi.right
    return [lo.val, hi.val]
```

**Complexity:** time **O(h)**, space **O(1)** — two spine walks, each at most h steps.

---

## Edge cases

- Single node → `[v, v]`.
- Root has no left child → root is the min.
- Skewed tree → O(n).

---

## Common mistakes

1. Taking the leftmost *leaf* rather than the leftmost *node*: the min may have a right child.
2. Not guarding an empty tree (LC/GfG variants that allow it expect −1).

---

## Follow-ups

1. Min of a subtree (used in delete)?
2. Second minimum?

<details><summary>Answer sketches</summary>

**#1:** Leftmost of that subtree's root.

**#2:** If min has a right child → leftmost of that right child; else its parent.
</details>

---

## Flashcards

**Where is the minimum of a BST?** #flashcard
The leftmost node: follow `.left` until null.

**Does the minimum have to be a leaf?** #flashcard
No. It has no left child but may have a right child.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
