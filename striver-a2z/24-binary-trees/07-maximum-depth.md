---
module: striver-a2z/24-binary-trees
lesson: 7
topic: Maximum Depth in BT
difficulty: Easy
source: https://takeuforward.org/learning/dsa/maximum-depth-in-bt?category=medium-problems&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, dfs, postorder, height]
---
# 7. Maximum Depth in BT

← [Pre, Post, Inorder in one traversal](06-all-traversals-in-one-pass.md) · [Part 24 index](README.md) · Next → [Check if two trees are identical or not](08-same-tree.md)

> [!abstract] Problem at a glance
> **Task:** Number of nodes on the longest root-to-leaf path.
> **Key insight:** `depth(n) = 1 + max(depth(left), depth(right))`, with `depth(null) = 0`. This is the template for every bottom-up tree problem: ask the children, combine, return.
> **Difficulty:** Easy · **Pattern:** Postorder (bottom-up) · **Also on:** [LC 104](https://leetcode.com/problems/maximum-depth-of-binary-tree/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/maximum-depth-in-bt?category=medium-problems&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. BFS level count](#3-bfs-level-count) · [4. Recursive postorder](#4-recursive-postorder) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a binary tree, return its maximum depth: the number of nodes along the longest path from the root down to the farthest leaf.

| Input | Output | Why |
|---|---|---|
| `root = [3,9,20,null,null,15,7]` | `3` | 3 → 20 → 15 |
| `root = [1,null,2]` | `2` |  |

**Constraints:** `0 ≤ n ≤ 10⁴`; values `−100…100`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| BFS level count | count BFS rounds | O(n) | O(w) |
| Recursive postorder | 1 + max(L, R) | O(n) | O(h) |

> [!tip] Interview angle
> Clarify the convention: nodes vs edges (LC counts nodes; some textbooks count edges, so a single node has height 0). Write the recursive one-liner, then mention BFS counting levels as the stack-safe alternative.

---

## 3. BFS level count

**Intuition.** Each round of the level-size BFS is one level. It can't overflow the stack.

```python
from collections import deque

def max_depth_bfs(root):
    if not root:
        return 0
    q, d = deque([root]), 0
    while q:
        d += 1
        for _ in range(len(q)):
            n = q.popleft()
            if n.left:
                q.append(n.left)
            if n.right:
                q.append(n.right)
    return d
```

**Complexity:** time **O(n)**, space **O(w)**.

---

## 4. Recursive postorder

**Intuition.** The deepest path through `n` goes into whichever child's subtree is deeper.

**Algorithm**

1. `if not n: return 0`.
2. `return 1 + max(depth(n.left), depth(n.right))`.

**Dry run** — [3,9,20,null,null,15,7]: 9→1, 15→1, 7→1, 20→2, 3→1+max(1,2)=3.

**C++**
```cpp
int maxDepth(TreeNode* root) {
    if (!root) return 0;
    return 1 + max(maxDepth(root->left), maxDepth(root->right));
}
```

**Java**
```java
static int maxDepth(TreeNode root) {
    if (root == null) return 0;
    return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}
```

**Python**
```python
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

**Complexity:** time **O(n)**, space **O(h)** — one call per node; the call stack is the current path.

---

## Edge cases

- Empty → 0.
- Single node → 1.
- Skewed tree of 10⁴ → recursion depth 10⁴ (fine in C++/Java, raise limit in Python or use BFS).

---

## Common mistakes

1. Returning −1 for null and mixing up the edges/nodes conventions.
2. `1 + max(...)` placed before the null check.

---

## Follow-ups

1. Minimum depth?
2. N-ary tree?

<details><summary>Answer sketches</summary>

**#1:** Careful: a node with one child isn't a leaf — `min` only over existing children (BFS: first leaf seen).

**#2:** `1 + max(depth(c) for c in children)`.
</details>

---

## Flashcards

**Max depth recurrence?** #flashcard
depth(null)=0; depth(n)=1+max(depth(L), depth(R)).

**Stack-safe max depth?** #flashcard
BFS counting level rounds.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
