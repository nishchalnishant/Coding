---
module: striver/24-binary-trees
lesson: 18
topic: Bottom view of Binary Tree
difficulty: Medium
source: https://takeuforward.org/learning/dsa/bottom-view-of-binary-tree?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, bfs, hashing, views]
---
# 18. Bottom view of Binary Tree

← [Top View of Binary Tree](17-top-view.md) · [Part 24 index](README.md) · Next → [Right/Left View of Binary Tree](19-right-left-view.md)

> [!abstract] Problem at a glance
> **Task:** For each column left→right, the bottom-most node (ties → the later one in level order).
> **Key insight:** It's the top view with the update rule flipped: **overwrite on every visit**. BFS visits deeper nodes later, and within a level from left to right, so the last write per column is the bottom-most node, with ties going to the right-most one, matching GfG.
> **Difficulty:** Medium · **Pattern:** BFS + HD map (last wins) · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/bottom-view-of-binary-tree/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/bottom-view-of-binary-tree?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. DFS with (depth, val), replace on ≥](#3-dfs-with-depth-val-replace-on-) · [4. BFS + overwrite per HD](#4-bfs--overwrite-per-hd) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Return the bottom view of a binary tree: for every horizontal distance, from leftmost to rightmost, the deepest node. If two nodes share the same column and depth, take the one that appears later in level order traversal.

| Input | Output | Why |
|---|---|---|
| `[20,8,22,5,3,4,25,null,null,10,14]` | `[5,10,4,14,25]` | 3 and 4 share HD 0 and depth 2; 4 comes later. Then 10 (HD −1) replaces 8, 14 (HD +1) replaces 22 |

**Constraints:** `1 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| DFS with (depth, val), replace on ≥ | preorder L then R; replace if depth ≥ stored | O(n log n) | O(n) |
| BFS + overwrite per HD | queue of (node, hd); seen[hd] = val every time | O(n) | O(n) |

> [!tip] Interview angle
> Say the tie rule out loud ('later in level order'). That rule is why BFS is the natural fit. A DFS version needs `(depth, val)` and `>=` on the depth with a right-after-left visit order.

---

## 3. DFS with (depth, val), replace on ≥

**Intuition.** With equal depth, a later preorder visit is further right, which matches 'later in level order' within a level.

```python
def bottom_view_dfs(root):
    best = {}
    def go(n, d, hd):
        if not n:
            return
        if hd not in best or d >= best[hd][0]:
            best[hd] = (d, n.val)
        go(n.left, d + 1, hd - 1)
        go(n.right, d + 1, hd + 1)
    go(root, 0, 0)
    return [best[k][1] for k in sorted(best)]
```

**Complexity:** time **O(n log n)**, space **O(n)**.

---

## 4. BFS + overwrite per HD

**Intuition.** The last BFS visit to a column is its deepest node, and among equal depths it is the right-most.

**Algorithm**

1. Queue `(root, 0)`.
2. Pop `(n, hd)`: `seen[hd] = n.val`; track lo/hi.
3. Push children with hd∓1.
4. Output `seen[lo..hi]`.

**Dry run** — T7: 1@0 → 5@0 overwrites, others unique → [4,2,5,3,6].

**C++**
```cpp
vector<int> bottomView(TreeNode* root) {
    vector<int> res;
    if (!root) return res;
    map<int, int> seen;
    queue<pair<TreeNode*, int>> q;
    q.push({root, 0});
    while (!q.empty()) {
        auto [n, hd] = q.front(); q.pop();
        seen[hd] = n->val;
        if (n->left) q.push({n->left, hd - 1});
        if (n->right) q.push({n->right, hd + 1});
    }
    for (auto& [hd, v] : seen) res.push_back(v);
    return res;
}
```

**Java**
```java
static List<Integer> bottomView(TreeNode root) {
    List<Integer> res = new ArrayList<>();
    if (root == null) return res;
    TreeMap<Integer, Integer> seen = new TreeMap<>();
    Deque<Object[]> q = new ArrayDeque<>();
    q.add(new Object[]{root, 0});
    while (!q.isEmpty()) {
        Object[] e = q.poll();
        TreeNode n = (TreeNode) e[0];
        int hd = (int) e[1];
        seen.put(hd, n.val);
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

def bottom_view(root):
    if not root:
        return []
    seen, q, lo, hi = {}, deque([(root, 0)]), 0, 0
    while q:
        n, hd = q.popleft()
        seen[hd] = n.val
        lo, hi = min(lo, hd), max(hi, hd)
        if n.left:
            q.append((n.left, hd - 1))
        if n.right:
            q.append((n.right, hd + 1))
    return [seen[h] for h in range(lo, hi + 1)]
```

**Complexity:** time **O(n)**, space **O(n)** — one BFS; ordered map adds log w per write.

---

## Edge cases

- Two nodes at the same depth and HD: the later (right-more) one wins.
- Skewed tree.
- Empty tree.

---

## Common mistakes

1. DFS with 'last visit wins' and no depth check (a shallow right-subtree node can overwrite a deeper left-subtree node).
2. Using the top-view `if hd not in seen` guard.

---

## Follow-ups

1. Top view?
2. Vertical sum?

<details><summary>Answer sketches</summary>

**#1:** First write wins.

**#2:** Same HD labelling, `sum[hd] += val`.
</details>

---

## Flashcards

**Bottom view rule?** #flashcard
BFS with HD; overwrite every time (last wins).

**Bottom-view tie (same depth & HD)?** #flashcard
Later in level order (right-most).

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
