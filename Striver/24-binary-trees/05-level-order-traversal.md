---
module: striver/24-binary-trees
lesson: 5
topic: Level Order Traversal
difficulty: Medium
source: https://takeuforward.org/learning/dsa/level-order-traversal?category=theory-and-traversals&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, bfs, traversal, queue]
---
# 5. Level Order Traversal

← [Postorder Traversal](04-postorder-traversal.md) · [Part 24 index](README.md) · Next → [Pre, Post, Inorder in one traversal](06-all-traversals-in-one-pass.md)

> [!abstract] Problem at a glance
> **Task:** Return values level by level, left to right, as a list of lists.
> **Key insight:** BFS with a queue. To split by level, read `len(queue)` **before** processing: exactly that many nodes belong to the current level, and everything they enqueue belongs to the next.
> **Difficulty:** Medium · **Pattern:** BFS (level-size snapshot) · **Also on:** [LC 102](https://leetcode.com/problems/binary-tree-level-order-traversal/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/level-order-traversal?category=theory-and-traversals&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. DFS with depth](#3-dfs-with-depth) · [4. BFS with level snapshot](#4-bfs-with-level-snapshot) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a binary tree, return the level order traversal of its nodes' values (i.e. from left to right, level by level).

| Input | Output | Why |
|---|---|---|
| `root = [3,9,20,null,null,15,7]` | `[[3],[9,20],[15,7]]` |  |
| `root = [1]` | `[[1]]` |  |
| `root = []` | `[]` |  |

**Constraints:** `0 ≤ n ≤ 2000`; values `−1000…1000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| DFS with depth | preorder; append to res[depth] | O(n) | O(h) |
| BFS with level snapshot | for _ in range(len(q)): pop, record, push children | O(n) | O(w) |

> [!tip] Interview angle
> The level-size snapshot is the core template for zigzag, right view, max width, level averages, minimum depth, burning tree and nodes at distance K. Mention that BFS space is O(w), the max width, up to n/2 for the last level of a perfect tree.

---

## 3. DFS with depth

**Intuition.** Preorder visits left before right, so values reach each `res[depth]` in left-to-right order. It's handy when you are already doing DFS, but it isn't 'real' BFS. It can't stop early at the first level that meets a condition.

```python
def level_order_dfs(root):
    res = []
    def go(n, d):
        if not n:
            return
        if d == len(res):
            res.append([])
        res[d].append(n.val)
        go(n.left, d + 1)
        go(n.right, d + 1)
    go(root, 0)
    return res
```

**Complexity:** time **O(n)**, space **O(h)**.

---

## 4. BFS with level snapshot

**Intuition.** The queue always holds one complete level (plus, while you are processing it, the start of the next). Taking `size = len(q)` at the top of each round separates them.

**Algorithm**

1. If root null → [].
2. `q = [root]`.
3. While q: `size = len(q)`, `level = []`; repeat `size` times: pop front, append val, push left/right.
4. Append `level`.

**Dry run** — [3,9,20,null,null,15,7]: q=[3] → [3]; q=[9,20] → [9,20]; q=[15,7] → [15,7].

**C++**
```cpp
vector<vector<int>> levelOrder(TreeNode* root) {
    vector<vector<int>> res;
    if (!root) return res;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        int sz = q.size();
        vector<int> level;
        while (sz--) {
            TreeNode* n = q.front(); q.pop();
            level.push_back(n->val);
            if (n->left) q.push(n->left);
            if (n->right) q.push(n->right);
        }
        res.push_back(level);
    }
    return res;
}
```

**Java**
```java
static List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> res = new ArrayList<>();
    if (root == null) return res;
    Queue<TreeNode> q = new ArrayDeque<>();
    q.add(root);
    while (!q.isEmpty()) {
        int sz = q.size();
        List<Integer> level = new ArrayList<>();
        while (sz-- > 0) {
            TreeNode n = q.poll();
            level.add(n.val);
            if (n.left != null) q.add(n.left);
            if (n.right != null) q.add(n.right);
        }
        res.add(level);
    }
    return res;
}
```

**Python**
```python
from collections import deque

def level_order(root):
    if not root:
        return []
    res, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            n = q.popleft()
            level.append(n.val)
            if n.left:
                q.append(n.left)
            if n.right:
                q.append(n.right)
        res.append(level)
    return res
```

**Complexity:** time **O(n)**, space **O(w)** — each node enqueued/dequeued once; the queue peaks at the widest level.

---

## Edge cases

- Empty tree → `[]` (not `[[]]`).
- Skewed tree: one node per level.
- Python: `list.pop(0)` is O(n) — use `deque`.

---

## Common mistakes

1. Calling `len(q)` inside the loop condition, so the level boundary moves as children are enqueued.
2. Using a Python list as a queue (`pop(0)`), which makes the whole BFS O(n²).
3. Enqueuing `null` children without skipping them.

---

## Follow-ups

1. Bottom-up levels?
2. Zigzag?
3. Level averages / max per level?

<details><summary>Answer sketches</summary>

**#1:** Same BFS, reverse `res` at the end.

**#2:** Alternate direction per level — Zig Zag problem.

**#3:** Aggregate inside the `size` loop.
</details>

---

## Flashcards

**How does BFS know where a level ends?** #flashcard
Snapshot `size = len(q)` before the inner loop.

**BFS space on a perfect tree?** #flashcard
O(n/2) = O(n) — the last level.

**Python queue for BFS?** #flashcard
`collections.deque` + `popleft()`.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
