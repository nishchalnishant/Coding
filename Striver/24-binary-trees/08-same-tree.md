---
module: striver/24-binary-trees
lesson: 8
topic: Check if two trees are identical or not
difficulty: Easy
source: https://takeuforward.org/learning/dsa/check-if-two-trees-are-identical-or-not?category=medium-problems&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, dfs, comparison]
---
# 8. Check if two trees are identical or not

← [Maximum Depth in BT](07-maximum-depth.md) · [Part 24 index](README.md) · Next → [Check for balanced binary tree](09-balanced-binary-tree.md)

> [!abstract] Problem at a glance
> **Task:** Return true iff two trees have the same shape and the same value at every position.
> **Key insight:** Both null → true. Exactly one null → false. Otherwise the values must match **and** the left subtrees and the right subtrees must be identical. Short-circuit on the first mismatch.
> **Difficulty:** Easy · **Pattern:** Simultaneous DFS · **Also on:** [LC 100](https://leetcode.com/problems/same-tree/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/check-if-two-trees-are-identical-or-not?category=medium-problems&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Compare serialisations](#3-compare-serialisations) · [4. Recursive lock-step](#4-recursive-lock-step) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the roots `p` and `q` of two binary trees, return `true` if they are structurally identical and the nodes have the same values.

| Input | Output | Why |
|---|---|---|
| `p = [1,2,3], q = [1,2,3]` | `true` |  |
| `p = [1,2], q = [1,null,2]` | `false` | same values, different shape |

**Constraints:** `0 ≤ n ≤ 100` per tree.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Compare serialisations | preorder with null markers, compare lists | O(n + m) | O(n + m) |
| Recursive lock-step | null checks, value check, recurse both sides | O(min(n, m)) | O(min(h₁, h₂)) |

> [!tip] Interview angle
> A building block for *Subtree of Another Tree* (LC 572) and *Symmetric Tree*. Note why comparing a single traversal is wrong: `[1,2]` and `[1,null,2]` have the same preorder `1,2`. You need null markers or two traversals.

---

## 3. Compare serialisations

**Intuition.** Preorder **with null markers** is a unique encoding of a binary tree. Equal encodings mean identical trees. It doesn't short-circuit and uses extra memory.

```python
def same_tree_ser(p, q):
    def ser(n, out):
        if not n:
            out.append(None)
            return out
        out.append(n.val)
        ser(n.left, out)
        ser(n.right, out)
        return out
    return ser(p, []) == ser(q, [])
```

**Complexity:** time **O(n + m)**, space **O(n + m)**.

---

## 4. Recursive lock-step

**Intuition.** Walk both trees together and stop at the first difference.

**Algorithm**

1. Both null → true.
2. One null → false.
3. `p.val == q.val and same(p.left, q.left) and same(p.right, q.right)`.

**Dry run** — [1,2] vs [1,null,2]: roots 1==1 → left: 2 vs null → false.

**C++**
```cpp
bool isSameTree(TreeNode* p, TreeNode* q) {
    if (!p || !q) return p == q;
    return p->val == q->val && isSameTree(p->left, q->left) && isSameTree(p->right, q->right);
}
```

**Java**
```java
static boolean isSameTree(TreeNode p, TreeNode q) {
    if (p == null || q == null) return p == q;
    return p.val == q.val && isSameTree(p.left, q.left) && isSameTree(p.right, q.right);
}
```

**Python**
```python
def same_tree(p, q):
    if not p or not q:
        return p is q
    return p.val == q.val and same_tree(p.left, q.left) and same_tree(p.right, q.right)
```

**Complexity:** time **O(min(n, m))**, space **O(min(h₁, h₂))** — stops at the first mismatch; at most min(n, m) node pairs.

---

## Edge cases

- Both empty → true.
- One empty → false.
- Same values, mirrored shape → false.

---

## Common mistakes

1. Comparing only preorder (or only inorder) without null markers.
2. `p.val == q.val` evaluated before the null check.

---

## Follow-ups

1. Subtree of another tree?
2. Identical up to swapping children (flip-equivalent)?

<details><summary>Answer sketches</summary>

**#1:** For each node of the big tree run `same(node, sub)` — O(n·m); O(n+m) via serialisation + KMP.

**#2:** LC 951: same(L,L)&&same(R,R) || same(L,R)&&same(R,L).
</details>

---

## Flashcards

**`if not p or not q: return ?`** #flashcard
`p is q` — true only if both are null.

**Why does preorder alone not identify a tree?** #flashcard
[1,2] and [1,null,2] share preorder 1,2 — need null markers.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
