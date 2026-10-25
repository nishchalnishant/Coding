---
module: striver-a2z/24-binary-trees
lesson: 10
topic: Diameter of Binary Tree
difficulty: Easy
source: https://takeuforward.org/learning/dsa/diameter-of-binary-tree?category=medium-problems&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, dfs, postorder, height]
---
# 10. Diameter of Binary Tree

← [Check for balanced binary tree](09-balanced-binary-tree.md) · [Part 24 index](README.md) · Next → [Maximum path sum](11-binary-tree-maximum-path-sum.md)

> [!abstract] Problem at a glance
> **Task:** Length (in **edges**) of the longest path between any two nodes.
> **Key insight:** Every path has a single highest node. At that node its length is `height(left) + height(right)`. Compute heights in postorder and update a global best with `hl + hr` at every node. The return value (height) and the answer (diameter) are different quantities.
> **Difficulty:** Easy · **Pattern:** Postorder: return one thing, record another · **Also on:** [LC 543](https://leetcode.com/problems/diameter-of-binary-tree/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/diameter-of-binary-tree?category=medium-problems&source=strivers-a2z-dsa-sheet) · **Time:** 12 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Height at every node](#3-height-at-every-node) · [4. Single postorder pass](#4-single-postorder-pass) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a binary tree, return the length of the diameter, the number of edges on the longest path between any two nodes. The path may or may not pass through the root.

| Input | Output | Why |
|---|---|---|
| `root = [1,2,3,4,5]` | `3` | 4 → 2 → 1 → 3 (or 5 → 2 → 1 → 3) |
| `root = [1,2]` | `1` |  |

**Constraints:** `1 ≤ n ≤ 10⁴` (handle 0 anyway).

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Height at every node | max over nodes of h(L) + h(R), heights recomputed | O(n²) worst | O(h) |
| Single postorder pass | best = max(best, hl + hr); return 1 + max(hl, hr) | O(n) | O(h) |

> [!tip] Interview angle
> The trap is assuming the path goes through the root. The last test has a longer path entirely inside the left subtree. Explain the 'return height, record diameter' split clearly, because max path sum is the same skeleton with values instead of counts.

---

## 3. Height at every node

**Intuition.** Try each node as the path's top and recompute heights each time.

```python
def diameter_naive(root):
    def h(n):
        return 0 if not n else 1 + max(h(n.left), h(n.right))
    if not root:
        return 0
    return max(h(root.left) + h(root.right), diameter_naive(root.left), diameter_naive(root.right))
```

**Complexity:** time **O(n²) worst**, space **O(h)**.

---

## 4. Single postorder pass

**Intuition.** While computing heights bottom-up you already have `hl` and `hr` at every node, so record `hl + hr` there.

**Algorithm**

1. `best = 0`.
2. `h(null) = 0`.
3. At node: `l = h(left)`, `r = h(right)`, `best = max(best, l + r)`, return `1 + max(l, r)`.
4. Return `best`.

**Dry run** — [1,2,3,4,5]: 4,5 → 1; at 2: best=2, h=2; 3 → 1; at 1: best=max(2, 2+1)=3.

**C++**
```cpp
int diaH(TreeNode* n, int& best) {
    if (!n) return 0;
    int l = diaH(n->left, best), r = diaH(n->right, best);
    best = max(best, l + r);
    return 1 + max(l, r);
}
int diameterOfBinaryTree(TreeNode* root) {
    int best = 0;
    diaH(root, best);
    return best;
}
```

**Java**
```java
static int best;
static int diaH(TreeNode n) {
    if (n == null) return 0;
    int l = diaH(n.left), r = diaH(n.right);
    best = Math.max(best, l + r);
    return 1 + Math.max(l, r);
}
static int diameterOfBinaryTree(TreeNode root) {
    best = 0;
    diaH(root);
    return best;
}
```

**Python**
```python
def diameter(root):
    best = 0
    def h(n):
        nonlocal best
        if not n:
            return 0
        l, r = h(n.left), h(n.right)
        best = max(best, l + r)
        return 1 + max(l, r)
    h(root)
    return best
```

**Complexity:** time **O(n)**, space **O(h)** — one height computation per node.

---

## Edge cases

- Single node → 0 edges.
- Longest path not through the root (last test).
- Skewed chain of n nodes → n − 1.

---

## Common mistakes

1. Returning `hl + hr` up the tree instead of the height.
2. Counting nodes instead of edges (off by one).
3. Java static `best` not reset between calls.

---

## Follow-ups

1. Diameter of an N-ary tree / general tree?
2. Return the path itself?
3. Graph tree (adjacency list)?

<details><summary>Answer sketches</summary>

**#1:** Keep the two largest child heights at every node.

**#2:** Store the node where the best was achieved, then walk down the deeper side of each child.

**#3:** Two BFS: farthest from any node, then farthest from that.
</details>

---

## Flashcards

**Diameter at a node?** #flashcard
height(left) + height(right) (edges).

**What does the diameter DFS return vs record?** #flashcard
Returns height; records hl + hr in a global max.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
