---
module: striver-a2z/24-binary-trees
lesson: 20
topic: Print root to node path in BT
difficulty: Medium
source: https://takeuforward.org/learning/dsa/print-root-to-node-path-in-bt?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, dfs, backtracking, paths]
---
# 20. Print root to node path in BT

← [Right/Left View of Binary Tree](19-right-left-view.md) · [Part 24 index](README.md) · Next → [LCA in BT](21-lowest-common-ancestor.md)

> [!abstract] Problem at a glance
> **Task:** All root-to-leaf paths, left to right (also: the path to one given node).
> **Key insight:** DFS with a shared `path` list: **push on entry, pop on exit** (backtracking). At a leaf, copy the path into the answer. Copy only at leaves, not at every node, to keep it O(n·h) rather than O(n²).
> **Difficulty:** Medium · **Pattern:** DFS + backtracking path · **Also on:** [LC 257](https://leetcode.com/problems/binary-tree-paths/) · [GfG](https://www.geeksforgeeks.org/problems/root-to-leaf-paths/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/print-root-to-node-path-in-bt?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. DFS passing new lists](#3-dfs-passing-new-lists) · [4. DFS + backtracking](#4-dfs--backtracking) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a binary tree, return all root-to-leaf paths as lists of node values, in left-to-right order. (Striver also covers the variant *root-to-node path for a given target*, which is the same DFS returning true once the target is found.)

| Input | Output | Why |
|---|---|---|
| `root = [1,2,3,null,5]` | `[[1,2,5],[1,3]]` |  |

**Constraints:** `1 ≤ n ≤ 100` (handle 0).

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| DFS passing new lists | go(n, path + [val]) | O(n·h) | O(n·h) |
| DFS + backtracking | append; if leaf copy; recurse; pop | O(n·h) (copies at leaves) | O(h) + output |

> [!tip] Interview angle
> This is the backtracking skeleton you reuse for path sum II and for LCA via paths. For the target-node variant, return a boolean so recursion stops as soon as the target is found and the path is kept, instead of being popped.

---

## 3. DFS passing new lists

**Intuition.** Each call gets its own copy of the path. It's the simplest to write and wastes some memory.

```python
def paths_copy(root):
    res = []
    def go(n, p):
        if not n:
            return
        p = p + [n.val]
        if not n.left and not n.right:
            res.append(p)
            return
        go(n.left, p)
        go(n.right, p)
    go(root, [])
    return res
```

**Complexity:** time **O(n·h)**, space **O(n·h)**.

---

## 4. DFS + backtracking

**Intuition.** One shared list mirrors the current root-to-node path.

**Algorithm**

1. `path = []`.
2. `go(n)`: if null return; `path.append(n.val)`.
3. If leaf: `res.append(path[:])`; else go(left), go(right).
4. `path.pop()`.

**Dry run** — [1,2,3,null,5]: [1] → [1,2] → [1,2,5] leaf ✓ → pop → pop → [1,3] leaf ✓.

**C++**
```cpp
void rlGo(TreeNode* n, vector<int>& path, vector<vector<int>>& res) {
    if (!n) return;
    path.push_back(n->val);
    if (!n->left && !n->right) res.push_back(path);
    else { rlGo(n->left, path, res); rlGo(n->right, path, res); }
    path.pop_back();
}
vector<vector<int>> rootToLeafPaths(TreeNode* root) {
    vector<vector<int>> res;
    vector<int> path;
    rlGo(root, path, res);
    return res;
}
```

**Java**
```java
static void rlGo(TreeNode n, List<Integer> path, List<List<Integer>> res) {
    if (n == null) return;
    path.add(n.val);
    if (n.left == null && n.right == null) res.add(new ArrayList<>(path));
    else { rlGo(n.left, path, res); rlGo(n.right, path, res); }
    path.remove(path.size() - 1);
}
static List<List<Integer>> rootToLeafPaths(TreeNode root) {
    List<List<Integer>> res = new ArrayList<>();
    rlGo(root, new ArrayList<>(), res);
    return res;
}
```

**Python**
```python
def root_to_leaf_paths(root):
    res, path = [], []
    def go(n):
        if not n:
            return
        path.append(n.val)
        if not n.left and not n.right:
            res.append(path[:])
        else:
            go(n.left)
            go(n.right)
        path.pop()
    go(root)
    return res
```

**Complexity:** time **O(n·h) (copies at leaves)**, space **O(h) + output** — O(n) traversal plus O(h) per leaf copy; at most n/2 leaves.

---

## Edge cases

- Node with one child is not a leaf.
- Single node → `[[root]]`.
- Empty tree → `[]`.

---

## Common mistakes

1. Appending `path` itself (all entries alias the same list, which ends up empty).
2. Forgetting to pop in the leaf branch.
3. Treating a one-child node as a leaf (null check on either side).

---

## Follow-ups

1. Path to a specific node?
2. Path sum II (sum == target)?
3. As strings `1->2->5`?

<details><summary>Answer sketches</summary>

**#1:** `bool go(n)`: push; if n is target or go(L) or go(R) → return true; pop; return false.

**#2:** Same backtracking with a running sum.

**#3:** `'->'.join(map(str, path))` at the leaf.
</details>

---

## Flashcards

**Backtracking path rule?** #flashcard
Push on entry, copy at leaf, pop on exit.

**Path to a target node — how to stop early?** #flashcard
Return true up the stack; skip the pop when found.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
