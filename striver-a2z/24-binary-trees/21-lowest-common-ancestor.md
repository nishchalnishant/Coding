---
module: striver-a2z/24-binary-trees
lesson: 21
topic: LCA in BT
difficulty: Medium
source: https://takeuforward.org/learning/dsa/lca-in-bt?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, dfs, postorder, lca]
---
# 21. LCA in BT

← [Print root to node path in BT](20-root-to-leaf-paths.md) · [Part 24 index](README.md) · Next → [Maximum width of a Binary Tree](22-maximum-width.md)

> [!abstract] Problem at a glance
> **Task:** Lowest node that has both `p` and `q` as descendants (a node is its own descendant).
> **Key insight:** Ask each subtree: 'do you contain p or q?' Return the node itself if it **is** p or q. If both sides return non-null, this node is where the paths split, so it's the LCA. Otherwise pass up whichever side is non-null.
> **Difficulty:** Medium · **Pattern:** Postorder: return found node · **Also on:** [LC 236](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/lca-in-bt?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 12 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Root-to-node paths](#3-root-to-node-paths) · [4. Single postorder](#4-single-postorder) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a binary tree and two nodes `p` and `q` that both exist in it, return their lowest common ancestor: the lowest node that has both `p` and `q` as descendants (a node may be a descendant of itself).

| Input | Output | Why |
|---|---|---|
| `root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1` | `3` |  |
| `same tree, p = 5, q = 4` | `5` | 5 is an ancestor of 4 |

**Constraints:** `2 ≤ n ≤ 10⁵`; all values unique; `p ≠ q`; both exist.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Root-to-node paths | find both paths, last common node | O(n) | O(h) |
| Single postorder | if n in {p,q,null} return n; L,R; both → n else L or R | O(n) | O(h) |

> [!tip] Interview angle
> The short recursion is expected. Be ready to justify the case where p is an ancestor of q: we return p without looking below it, which is right because the LCA is p. If the guarantee that both exist is removed, you need counts or a second check. The BST version is easier (walk by value).

---

## 3. Root-to-node paths

**Intuition.** Find the root→p and root→q paths with backtracking. The LCA is the last node they share.

```python
def lca_paths(root, p, q):
    def path(n, t, out):
        if not n:
            return False
        out.append(n)
        if n is t or path(n.left, t, out) or path(n.right, t, out):
            return True
        out.pop()
        return False
    a, b = [], []
    path(root, p, a)
    path(root, q, b)
    i = 0
    while i < min(len(a), len(b)) and a[i] is b[i]:
        i += 1
    return a[i - 1]
```

**Complexity:** time **O(n)**, space **O(h)**.

---

## 4. Single postorder

**Intuition.** A non-null return means 'I found p or q (or their LCA) in here'. The first node to receive non-null from both sides is the split point.

**Algorithm**

1. If `n` is null, p or q → return `n`.
2. `L = lca(n.left)`, `R = lca(n.right)`.
3. If both non-null → return `n`.
4. Return `L or R`.

**Dry run** — p=5, q=1: at 3, left returns 5 (hit), right returns 1 (hit) → 3. p=5, q=4: at 5 return 5 immediately; right of 3 returns null → 5.

**C++**
```cpp
TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (!root || root == p || root == q) return root;
    TreeNode* l = lowestCommonAncestor(root->left, p, q);
    TreeNode* r = lowestCommonAncestor(root->right, p, q);
    if (l && r) return root;
    return l ? l : r;
}
```

**Java**
```java
static TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if (root == null || root == p || root == q) return root;
    TreeNode l = lowestCommonAncestor(root.left, p, q);
    TreeNode r = lowestCommonAncestor(root.right, p, q);
    if (l != null && r != null) return root;
    return l != null ? l : r;
}
```

**Python**
```python
def lca(root, p, q):
    if not root or root is p or root is q:
        return root
    l = lca(root.left, p, q)
    r = lca(root.right, p, q)
    if l and r:
        return root
    return l or r
```

**Complexity:** time **O(n)**, space **O(h)** — every node is visited at most once.

---

## Edge cases

- p is an ancestor of q → p.
- p and q are siblings → parent.
- Two-node tree.

---

## Common mistakes

1. Comparing values when duplicates are possible (compare node identity).
2. Using this short version when p or q might be missing (it returns the one that exists).
3. Stopping the search at the first hit *in both* subtrees by mistake.

---

## Follow-ups

1. LCA in a BST?
2. p or q may be absent?
3. Many LCA queries?

<details><summary>Answer sketches</summary>

**#1:** Walk from root: both smaller → left, both larger → right, else current.

**#2:** Count hits (LC 1644) or verify both exist first.

**#3:** Binary lifting / Euler tour + RMQ (beyond L3).
</details>

---

## Flashcards

**LCA recursion base case?** #flashcard
Return node if it's null, p or q.

**When is the current node the LCA?** #flashcard
When both subtrees return non-null.

**LCA when p is an ancestor of q?** #flashcard
p (returned before searching below).

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
