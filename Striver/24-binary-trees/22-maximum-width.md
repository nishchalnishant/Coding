---
module: striver/24-binary-trees
lesson: 22
topic: Maximum width of a Binary Tree
difficulty: Medium
source: https://takeuforward.org/learning/dsa/maximum-width-of-a-binary-tree?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, bfs, indexing]
---
# 22. Maximum width of a Binary Tree

← [LCA in BT](21-lowest-common-ancestor.md) · [Part 24 index](README.md) · Next → [Print all the Nodes at a distance of K in a BT](23-all-nodes-distance-k.md)

> [!abstract] Problem at a glance
> **Task:** Max over levels of (rightmost index − leftmost index + 1), counting the null gaps between them.
> **Key insight:** Number nodes as in a heap: root `i`, children `2i+1`, `2i+2`. The width of a level is `last − first + 1`. Indices double every level and overflow after ~64 levels, so **renormalise**: subtract the level's first index before computing children.
> **Difficulty:** Medium · **Pattern:** BFS + heap indexing · **Also on:** [LC 662](https://leetcode.com/problems/maximum-width-of-binary-tree/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/maximum-width-of-a-binary-tree?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. BFS + normalised heap index](#3-bfs--normalised-heap-index) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Return the maximum width of the given tree. The width of a level is the length between its leftmost and rightmost non-null nodes, counting the null positions in between as if the tree were complete.

| Input | Output | Why |
|---|---|---|
| `root = [1,3,2,5,3,null,9]` | `4` | level 3: 5 _ _ 9? no — 5,3,null,9 → 4 |
| `root = [1,3,2,5,null,null,9,6,null,7]` | `7` | last level: 6 at index 0, 7 at index 6 |

**Constraints:** `1 ≤ n ≤ 3000`; answer fits in 32-bit.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| BFS + normalised heap index | idx -= first of level; children 2i+1, 2i+2 | O(n) | O(w) |

> [!tip] Interview angle
> The overflow is the interview point. A skewed-zigzag tree of depth 3000 gives indices of 2³⁰⁰⁰. Python hides it with big ints; C++/Java need the per-level offset trick (or unsigned wraparound, which works because only differences matter).

---

## 3. BFS + normalised heap index

**Intuition.** Only differences between indices on the same level matter, so subtracting a per-level constant is harmless and keeps the numbers small.

**Algorithm**

1. Queue `(root, 0)`.
2. Per level: `first = q[0].idx`, `size`.
3. For each `(n, i)`: `i -= first`; track last `i`; push `(L, 2i+1)`, `(R, 2i+2)`.
4. `best = max(best, last + 1)`.

**Dry run** — [1,3,2,5,null,null,9,6,null,7]: L2 nodes 5@0, 9@3 → 4; L3 6@0, 7@6 → 7.

**C++**
```cpp
int widthOfBinaryTree(TreeNode* root) {
    if (!root) return 0;
    long long best = 0;
    queue<pair<TreeNode*, long long>> q;
    q.push({root, 0});
    while (!q.empty()) {
        long long first = q.front().second, last = 0;
        int sz = q.size();
        while (sz--) {
            auto [n, i] = q.front(); q.pop();
            i -= first;
            last = i;
            if (n->left) q.push({n->left, 2 * i + 1});
            if (n->right) q.push({n->right, 2 * i + 2});
        }
        best = max(best, last + 1);
    }
    return (int)best;
}
```

**Java**
```java
static int widthOfBinaryTree(TreeNode root) {
    if (root == null) return 0;
    long best = 0;
    Deque<Object[]> q = new ArrayDeque<>();
    q.add(new Object[]{root, 0L});
    while (!q.isEmpty()) {
        long first = (long) q.peek()[1], last = 0;
        int sz = q.size();
        while (sz-- > 0) {
            Object[] e = q.poll();
            TreeNode n = (TreeNode) e[0];
            long i = (long) e[1] - first;
            last = i;
            if (n.left != null) q.add(new Object[]{n.left, 2 * i + 1});
            if (n.right != null) q.add(new Object[]{n.right, 2 * i + 2});
        }
        best = Math.max(best, last + 1);
    }
    return (int) best;
}
```

**Python**
```python
from collections import deque

def max_width(root):
    if not root:
        return 0
    best, q = 0, deque([(root, 0)])
    while q:
        first, last = q[0][1], 0
        for _ in range(len(q)):
            n, i = q.popleft()
            i -= first
            last = i
            if n.left:
                q.append((n.left, 2 * i + 1))
            if n.right:
                q.append((n.right, 2 * i + 2))
        best = max(best, last + 1)
    return best
```

**Complexity:** time **O(n)**, space **O(w)** — one BFS; after normalisation indices stay below 2·(level width).

---

## Edge cases

- Single node → 1.
- Skewed tree → 1 at every level.
- Deep zig-zag tree → overflow without normalisation.

---

## Common mistakes

1. Counting only non-null nodes per level (that's not the width).
2. No normalisation in C++/Java (overflow).
3. Using `i` from before normalisation for the children.

---

## Follow-ups

1. DFS version?
2. Level with max width (index)?

<details><summary>Answer sketches</summary>

**#1:** Record first index per depth; width = i − first[d] + 1.

**#2:** Track the level counter alongside best.
</details>

---

## Flashcards

**Max width indexing?** #flashcard
Heap indices 2i+1, 2i+2 per level, width = last − first + 1.

**How to avoid overflow in max width?** #flashcard
Subtract the level's first index before computing children.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
