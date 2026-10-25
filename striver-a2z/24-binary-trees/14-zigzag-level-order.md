---
module: striver-a2z/24-binary-trees
lesson: 14
topic: Zig Zag Traversal Of Binary Tree
difficulty: Medium
source: https://takeuforward.org/learning/dsa/zig-zag-traversal-of-binary-tree?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, bfs, level-order]
---
# 14. Zig Zag Traversal Of Binary Tree

← [Children Sum Property in Binary Tree](13-children-sum-property.md) · [Part 24 index](README.md) · Next → [Boundary Traversal of a Binary Tree](15-boundary-traversal.md)

> [!abstract] Problem at a glance
> **Task:** Level order, but alternate left→right and right→left per level.
> **Key insight:** Run the normal level-size BFS. Children are always enqueued left before right. Only the **order of writing** each level changes: reverse it, or fill it from the back, on odd levels. Changing the enqueue order instead corrupts the levels below.
> **Difficulty:** Medium · **Pattern:** BFS + direction flag · **Also on:** [LC 103](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/zig-zag-traversal-of-binary-tree?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. BFS + reverse odd levels](#3-bfs--reverse-odd-levels) · [4. BFS + index placement](#4-bfs--index-placement) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a binary tree, return the zigzag level order traversal of its nodes' values (left to right, then right to left for the next level, and alternate).

| Input | Output | Why |
|---|---|---|
| `root = [3,9,20,null,null,15,7]` | `[[3],[20,9],[15,7]]` |  |

**Constraints:** `0 ≤ n ≤ 2000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| BFS + reverse odd levels | level order, reverse every other row | O(n) | O(w) |
| BFS + index placement | lvl[i] or lvl[size−1−i] depending on direction | O(n) | O(w) |

> [!tip] Interview angle
> Say clearly that the queue order never changes; only the output index does. The two-stack version (one stack per direction) is the classic alternative. Mention it, but the flag version is shorter and less error-prone.

---

## 3. BFS + reverse odd levels

**Intuition.** Build each level normally and reverse it when the flag is set. It's O(w) extra per level, which is fine.

```python
from collections import deque

def zigzag_rev(root):
    if not root:
        return []
    res, q, flip = [], deque([root]), False
    while q:
        lvl = []
        for _ in range(len(q)):
            n = q.popleft()
            lvl.append(n.val)
            if n.left:
                q.append(n.left)
            if n.right:
                q.append(n.right)
        res.append(lvl[::-1] if flip else lvl)
        flip = not flip
    return res
```

**Complexity:** time **O(n)**, space **O(w)**.

---

## 4. BFS + index placement

**Intuition.** Preallocate the level of length `size` and write each value directly into its final slot. No reversal is needed.

**Algorithm**

1. Standard BFS with `size = len(q)`.
2. `ltr = True`.
3. For `i` in `0..size-1`: pop node, `idx = i if ltr else size−1−i`, `lvl[idx] = val`, enqueue children L then R.
4. Append `lvl`, flip `ltr`.

**Dry run** — T7: L0 [1]; L1 nodes 2,3 written to idx 1,0 → [3,2]; L2 ltr → [4,5,6].

**C++**
```cpp
vector<vector<int>> zigzagLevelOrder(TreeNode* root) {
    vector<vector<int>> res;
    if (!root) return res;
    queue<TreeNode*> q;
    q.push(root);
    bool ltr = true;
    while (!q.empty()) {
        int sz = q.size();
        vector<int> lvl(sz);
        for (int i = 0; i < sz; i++) {
            TreeNode* n = q.front(); q.pop();
            lvl[ltr ? i : sz - 1 - i] = n->val;
            if (n->left) q.push(n->left);
            if (n->right) q.push(n->right);
        }
        res.push_back(lvl);
        ltr = !ltr;
    }
    return res;
}
```

**Java**
```java
static List<List<Integer>> zigzagLevelOrder(TreeNode root) {
    List<List<Integer>> res = new ArrayList<>();
    if (root == null) return res;
    Queue<TreeNode> q = new ArrayDeque<>();
    q.add(root);
    boolean ltr = true;
    while (!q.isEmpty()) {
        int sz = q.size();
        Integer[] lvl = new Integer[sz];
        for (int i = 0; i < sz; i++) {
            TreeNode n = q.poll();
            lvl[ltr ? i : sz - 1 - i] = n.val;
            if (n.left != null) q.add(n.left);
            if (n.right != null) q.add(n.right);
        }
        res.add(Arrays.asList(lvl));
        ltr = !ltr;
    }
    return res;
}
```

**Python**
```python
from collections import deque

def zigzag(root):
    if not root:
        return []
    res, q, ltr = [], deque([root]), True
    while q:
        size = len(q)
        lvl = [0] * size
        for i in range(size):
            n = q.popleft()
            lvl[i if ltr else size - 1 - i] = n.val
            if n.left:
                q.append(n.left)
            if n.right:
                q.append(n.right)
        res.append(lvl)
        ltr = not ltr
    return res
```

**Complexity:** time **O(n)**, space **O(w)** — each node is processed once and written straight to its final index.

---

## Edge cases

- Empty → `[]`.
- Odd-length last level that isn't full (test 5).
- Single node.

---

## Common mistakes

1. Enqueuing right-before-left on odd levels: this scrambles the next level.
2. Flipping the flag inside the inner loop.

---

## Follow-ups

1. Two-stack version?
2. Spiral matrix analogy?

<details><summary>Answer sketches</summary>

**#1:** s1 pushes L then R, s2 pushes R then L; alternate stacks.

**#2:** Same idea — direction flag, fixed traversal order.
</details>

---

## Flashcards

**Zigzag: what changes on odd levels?** #flashcard
Only the write index (or reverse the row) — queue order stays L→R.

**Zigzag write index on R→L level?** #flashcard
size − 1 − i.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
