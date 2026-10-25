---
module: striver-a2z/24-binary-trees
lesson: 13
topic: Children Sum Property in Binary Tree
difficulty: Medium
source: https://takeuforward.org/learning/dsa/children-sum-property-in-binary-tree?category=medium-problems&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, dfs, modify-in-place]
---
# 13. Children Sum Property in Binary Tree

← [Check for symmetrical BTs](12-symmetric-tree.md) · [Part 24 index](README.md) · Next → [Zig Zag Traversal Of Binary Tree](14-zigzag-level-order.md)

> [!abstract] Problem at a glance
> **Task:** Make every internal node equal the sum of its children, using **only increments** (any number of +1 on any node), without changing structure.
> **Key insight:** You can't decrease, so fix the deficit **on the way down**. If the children's sum is less than the node, raise the children to the node's value. Otherwise raise the node to the children's sum. Recurse. On the way **up**, set `node = left + right`. Because the children were raised to at least the parent's value, the final sum never ends up below what the parent needed.
> **Difficulty:** Medium · **Pattern:** Pre + post order (fix down, sum up) · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/children-sum-parent/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/children-sum-property-in-binary-tree?category=medium-problems&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Push down, sum up](#3-push-down-sum-up) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a binary tree, convert it so that it satisfies the *children sum property*: every non-leaf node's value equals the sum of its children's values (a missing child counts as 0). You may only **increment** node values, any number of times, and must not change the structure. Return the modified tree.

| Input | Output | Why |
|---|---|---|
| `[2,35,10,2,3,5,2]` | `[90,70,20,35,35,10,10]` | 35 pushes 35 to both leaves → 70; 10 → 20; root = 90 |
| `[50,7,2,3,5,1,30]` | `[200,100,100,50,50,50,50]` | 50 pushed all the way down, then summed up |

**Constraints:** `1 ≤ n ≤ 10⁵`. Many valid outputs exist; this note returns the one produced by the algorithm below.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Push down, sum up | pre: if childSum < val → children = val else val = childSum; post: val = L + R | O(n) | O(h) |

> [!tip] Interview angle
> Striver's O(n) trick. The GfG *check* version is a trivial DFS. The *convert* version is the interesting one. Explain why pushing the parent's value down is safe: it only makes subtrees larger, and larger is always fixable because we sum on the way up. Mention that the answer isn't unique.

---

## 3. Push down, sum up

**Intuition.** Pre-step guarantees `children ≥ parent` before recursing, so every subtree's final value (sum of its children) is at least what the parent requires. Post-step fixes the parent exactly.

**Algorithm**

1. If null return.
2. `s = (left?.val or 0) + (right?.val or 0)`.
3. If `s ≥ val`: `val = s`. Else set each existing child's val = `val`.
4. Recurse left, right.
5. If node has any child: `val = (left?.val or 0) + (right?.val or 0)`.

**Dry run** — [2,35,10,2,3,5,2]: root s=45≥2 → 45. Node 35: s=5<35 → leaves 35,35; up 70. Node 10: s=7<10 → 10,10; up 20. Root up 90.

**C++**
```cpp
void childrenSum(TreeNode* root) {
    if (!root) return;
    int s = (root->left ? root->left->val : 0) + (root->right ? root->right->val : 0);
    if (s >= root->val) root->val = s;
    else {
        if (root->left) root->left->val = root->val;
        if (root->right) root->right->val = root->val;
    }
    childrenSum(root->left);
    childrenSum(root->right);
    if (root->left || root->right)
        root->val = (root->left ? root->left->val : 0) + (root->right ? root->right->val : 0);
}
```

**Java**
```java
static void childrenSum(TreeNode root) {
    if (root == null) return;
    int s = (root.left != null ? root.left.val : 0) + (root.right != null ? root.right.val : 0);
    if (s >= root.val) root.val = s;
    else {
        if (root.left != null) root.left.val = root.val;
        if (root.right != null) root.right.val = root.val;
    }
    childrenSum(root.left);
    childrenSum(root.right);
    if (root.left != null || root.right != null)
        root.val = (root.left != null ? root.left.val : 0) + (root.right != null ? root.right.val : 0);
}
```

**Python**
```python
def children_sum(root):
    if not root:
        return
    s = (root.left.val if root.left else 0) + (root.right.val if root.right else 0)
    if s >= root.val:
        root.val = s
    else:
        if root.left:
            root.left.val = root.val
        if root.right:
            root.right.val = root.val
    children_sum(root.left)
    children_sum(root.right)
    if root.left or root.right:
        root.val = (root.left.val if root.left else 0) + (root.right.val if root.right else 0)
```

**Complexity:** time **O(n)**, space **O(h)** — each node visited once; O(1) work per visit.

---

## Edge cases

- Leaf: unchanged.
- Node with one child: the missing child counts as 0, so the existing child carries the whole value.
- Empty tree.

---

## Common mistakes

1. Overwriting a leaf with 0 in the post-step (only internal nodes are re-summed).
2. Trying to fix bottom-up only: you'd need to *decrease* a child when the parent is smaller, which isn't allowed.
3. Pushing the parent's value only to the left child (fine for correctness, but be consistent with the expected output).

---

## Follow-ups

1. Just check the property?
2. Minimise total increments?

<details><summary>Answer sketches</summary>

**#1:** DFS: every internal node == sum of children; O(n).

**#2:** Different problem — needs a more careful DP; not what Striver asks.
</details>

---

## Flashcards

**Children sum (increments only): what happens going down?** #flashcard
If childSum < val, set children to val; else val = childSum.

**…and going up?** #flashcard
val = left + right for every internal node.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
