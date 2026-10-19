---
module: striver/24-binary-trees
lesson: 19
topic: Right/Left View of Binary Tree
difficulty: Medium
source: https://takeuforward.org/learning/dsa/right-left-view-of-binary-tree?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, dfs, bfs, views]
---
# 19. Right/Left View of Binary Tree

← [Bottom view of Binary Tree](18-bottom-view.md) · [Part 24 index](README.md) · Next → [Print root to node path in BT](20-root-to-leaf-paths.md)

> [!abstract] Problem at a glance
> **Task:** Return `[rightView, leftView]`: the last and first node of every level.
> **Key insight:** DFS with depth, visiting the preferred side first. The first node you meet at a new depth (`depth == len(res)`) is the visible one. For the right view go right-first; for the left view go left-first. It's O(h) space, beating BFS's O(w).
> **Difficulty:** Medium · **Pattern:** DFS: first node per depth · **Also on:** [LC 199](https://leetcode.com/problems/binary-tree-right-side-view/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/right-left-view-of-binary-tree?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. BFS: first/last per level](#3-bfs-firstlast-per-level) · [4. DFS: first node per depth](#4-dfs-first-node-per-depth) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a binary tree, imagine standing on its right side: return the values of the nodes you can see, ordered top to bottom (the right view). Also return the left view. Output `[right, left]`.

| Input | Output | Why |
|---|---|---|
| `root = [1,2,3,null,5,null,4]` | `[[1,3,4],[1,2,5]]` |  |
| `root = [1,2,3,4]` | `[[1,3,4],[1,2,4]]` | 4 is the only node at depth 2, so both views see it |

**Constraints:** `0 ≤ n ≤ 100`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| BFS: first/last per level | level snapshot; record level[0] and level[-1] | O(n) | O(w) |
| DFS: first node per depth | right view: visit R before L; append when depth == len(res) | O(n) | O(h) |

> [!tip] Interview angle
> Show both versions: BFS (last of each level) and the shorter DFS. The trap is assuming the right view is the right edge. Test 5 shows a left-subtree node visible from the right because the right subtree is shallower.

---

## 3. BFS: first/last per level

**Intuition.** It's the level-order template with two reads per level.

```python
from collections import deque

def views_bfs(root):
    if not root:
        return [[], []]
    r, l, q = [], [], deque([root])
    while q:
        size = len(q)
        for i in range(size):
            n = q.popleft()
            if i == 0:
                l.append(n.val)
            if i == size - 1:
                r.append(n.val)
            if n.left:
                q.append(n.left)
            if n.right:
                q.append(n.right)
    return [r, l]
```

**Complexity:** time **O(n)**, space **O(w)**.

---

## 4. DFS: first node per depth

**Intuition.** Exactly one node per depth is recorded: the first to arrive. Visiting the right child first means the right-most node at each depth arrives first.

**Algorithm**

1. `go(n, d, res, rightFirst)`: if null return.
2. If `d == len(res)`: append `n.val`.
3. Recurse on preferred child, then the other, with `d+1`.
4. Run twice: right-first and left-first.

**Dry run** — [1,2,3,null,5,null,4] right-first: 1 (d0) → 3 (d1) → 4 (d2) → 2 (d1, skip) → 5 (d2, skip) → [1,3,4].

**C++**
```cpp
void viewGo(TreeNode* n, int d, vector<int>& res, bool rightFirst) {
    if (!n) return;
    if (d == (int)res.size()) res.push_back(n->val);
    viewGo(rightFirst ? n->right : n->left, d + 1, res, rightFirst);
    viewGo(rightFirst ? n->left : n->right, d + 1, res, rightFirst);
}
vector<vector<int>> views(TreeNode* root) {
    vector<int> r, l;
    viewGo(root, 0, r, true);
    viewGo(root, 0, l, false);
    return {r, l};
}
```

**Java**
```java
static void viewGo(TreeNode n, int d, List<Integer> res, boolean rightFirst) {
    if (n == null) return;
    if (d == res.size()) res.add(n.val);
    viewGo(rightFirst ? n.right : n.left, d + 1, res, rightFirst);
    viewGo(rightFirst ? n.left : n.right, d + 1, res, rightFirst);
}
static List<List<Integer>> views(TreeNode root) {
    List<Integer> r = new ArrayList<>(), l = new ArrayList<>();
    viewGo(root, 0, r, true);
    viewGo(root, 0, l, false);
    return List.of(r, l);
}
```

**Python**
```python
def views(root):
    def go(n, d, res, right_first):
        if not n:
            return
        if d == len(res):
            res.append(n.val)
        a, b = (n.right, n.left) if right_first else (n.left, n.right)
        go(a, d + 1, res, right_first)
        go(b, d + 1, res, right_first)
    r, l = [], []
    go(root, 0, r, True)
    go(root, 0, l, False)
    return [r, l]
```

**Complexity:** time **O(n)**, space **O(h)** — each node visited once per view; recursion depth h.

---

## Edge cases

- A shallow right subtree: deeper left nodes appear in the right view.
- Single node: both views `[root]`.
- Empty tree.

---

## Common mistakes

1. Walking only the right edge (`cur = cur.right`).
2. Using `d > len(res)` (off by one, records nothing).

---

## Follow-ups

1. Top/bottom view?
2. Right view of an N-ary tree?

<details><summary>Answer sketches</summary>

**#1:** Column-based — BFS with horizontal distance.

**#2:** DFS children from last to first, same depth rule.
</details>

---

## Flashcards

**Right view DFS rule?** #flashcard
Visit right first; record node when depth == len(res).

**Is the right view the right edge?** #flashcard
No — a deeper left-subtree node can be visible.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
