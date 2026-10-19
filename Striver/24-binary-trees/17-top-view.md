---
module: striver/24-binary-trees
lesson: 17
topic: Top View of Binary Tree
difficulty: Medium
source: https://takeuforward.org/learning/dsa/top-view-of-binary-tree?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, bfs, hashing, views]
---
# 17. Top View of Binary Tree

← [Vertical Order Traversal](16-vertical-order-traversal.md) · [Part 24 index](README.md) · Next → [Bottom view of Binary Tree](18-bottom-view.md)

> [!abstract] Problem at a glance
> **Task:** For each vertical column (left→right), the node seen first from above, i.e. the topmost one.
> **Key insight:** BFS with horizontal distance (HD). The **first** node BFS reaches in a column is the topmost, so record it only if the column is new. BFS, not DFS: a DFS can reach a deeper node in a column before a shallower one.
> **Difficulty:** Medium · **Pattern:** BFS + HD map (first wins) · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/top-view-of-binary-tree/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/top-view-of-binary-tree?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 12 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. DFS with (depth, val) per HD](#3-dfs-with-depth-val-per-hd) · [4. BFS + first-seen per HD](#4-bfs--first-seen-per-hd) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a binary tree, return the nodes visible when it is viewed from the top, ordered from the leftmost column to the rightmost. When two nodes share a column, the one higher up (earlier in level order) is visible.

| Input | Output | Why |
|---|---|---|
| `[1,2,3,4,5,null,6]` | `[4,2,1,3,6]` | 5 is hidden under 1 (both HD 0) |
| `[1,2,3,null,4,null,null,null,5,null,6]` | `[2,1,3,6]` | 4 (HD 0) and 5 (HD 1) are hidden under 1 and 3; 6 at HD 2 is visible |

**Constraints:** `1 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| DFS with (depth, val) per HD | keep smallest depth per column | O(n log n) | O(n) |
| BFS + first-seen per HD | queue of (node, hd); record if hd unseen | O(n) | O(n) |

> [!tip] Interview angle
> The usual follow-up is 'why not DFS?'. With DFS you have to keep (depth, value) per column and replace only on a smaller depth. That works, but BFS gets it right by construction. Keep track of min/max HD so you can output without sorting.

---

## 3. DFS with (depth, val) per HD

**Intuition.** It works if you compare depths. With preorder (left first), equal depths keep the leftmost node, which matches BFS order.

```python
def top_view_dfs(root):
    best = {}
    def go(n, d, hd):
        if not n:
            return
        if hd not in best or d < best[hd][0]:
            best[hd] = (d, n.val)
        go(n.left, d + 1, hd - 1)
        go(n.right, d + 1, hd + 1)
    go(root, 0, 0)
    return [best[k][1] for k in sorted(best)]
```

**Complexity:** time **O(n log n)**, space **O(n)**.

---

## 4. BFS + first-seen per HD

**Intuition.** BFS visits in increasing depth, so the first arrival in a column is the topmost. A dict plus min/max HD avoids sorting.

**Algorithm**

1. Queue `(root, 0)`; `seen = {}`; `lo = hi = 0`.
2. Pop `(n, hd)`; if `hd` not in seen, store `n.val`; update lo/hi.
3. Push `(left, hd−1)`, `(right, hd+1)`.
4. Output `seen[lo..hi]`.

**Dry run** — T7: 1@0, 2@−1, 3@1, 4@−2, 5@0 (skip), 6@2 → cols −2..2 → [4,2,1,3,6].

**C++**
```cpp
vector<int> topView(TreeNode* root) {
    vector<int> res;
    if (!root) return res;
    map<int, int> seen;
    queue<pair<TreeNode*, int>> q;
    q.push({root, 0});
    while (!q.empty()) {
        auto [n, hd] = q.front(); q.pop();
        if (!seen.count(hd)) seen[hd] = n->val;
        if (n->left) q.push({n->left, hd - 1});
        if (n->right) q.push({n->right, hd + 1});
    }
    for (auto& [hd, v] : seen) res.push_back(v);
    return res;
}
```

**Java**
```java
static List<Integer> topView(TreeNode root) {
    List<Integer> res = new ArrayList<>();
    if (root == null) return res;
    TreeMap<Integer, Integer> seen = new TreeMap<>();
    Deque<Object[]> q = new ArrayDeque<>();
    q.add(new Object[]{root, 0});
    while (!q.isEmpty()) {
        Object[] e = q.poll();
        TreeNode n = (TreeNode) e[0];
        int hd = (int) e[1];
        seen.putIfAbsent(hd, n.val);
        if (n.left != null) q.add(new Object[]{n.left, hd - 1});
        if (n.right != null) q.add(new Object[]{n.right, hd + 1});
    }
    res.addAll(seen.values());
    return res;
}
```

**Python**
```python
from collections import deque

def top_view(root):
    if not root:
        return []
    seen, q, lo, hi = {}, deque([(root, 0)]), 0, 0
    while q:
        n, hd = q.popleft()
        if hd not in seen:
            seen[hd] = n.val
            lo, hi = min(lo, hd), max(hi, hd)
        if n.left:
            q.append((n.left, hd - 1))
        if n.right:
            q.append((n.right, hd + 1))
    return [seen[h] for h in range(lo, hi + 1)]
```

**Complexity:** time **O(n)**, space **O(n)** — O(n) with a hash map + lo/hi; O(n log w) with an ordered map (C++/Java versions).

---

## Edge cases

- Skewed tree: every node visible.
- A deep node in a far column (test 4: 6 at HD 2).
- Empty tree.

---

## Common mistakes

1. DFS with 'first visit wins': a left-subtree node can reach HD +1 before the right child does.
2. Overwriting on every visit (that's the bottom view).

---

## Follow-ups

1. Bottom view?
2. Left/right view?

<details><summary>Answer sketches</summary>

**#1:** Same BFS, overwrite every time (last wins).

**#2:** First/last node per *level*, not per column.
</details>

---

## Flashcards

**Top view rule?** #flashcard
BFS with HD; first node seen per HD.

**Why BFS for top view?** #flashcard
BFS reaches every column at its smallest depth first.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
