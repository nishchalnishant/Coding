---
module: striver-a2z/24-binary-trees
lesson: 15
topic: Boundary Traversal of a Binary Tree
difficulty: Medium
source: https://takeuforward.org/learning/dsa/boundary-traversal-of-a-binary-tree?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, dfs, traversal]
---
# 15. Boundary Traversal of a Binary Tree

← [Zig Zag Traversal Of Binary Tree](14-zigzag-level-order.md) · [Part 24 index](README.md) · Next → [Vertical Order Traversal](16-vertical-order-traversal.md)

> [!abstract] Problem at a glance
> **Task:** Anticlockwise boundary: root → left boundary (no leaves) → all leaves L→R → right boundary bottom-up (no leaves).
> **Key insight:** Split it into three independent walks and stitch them together. (1) Left edge: from `root.left`, prefer left and fall back to right, skipping leaves. (2) Leaves: any DFS that visits left before right. (3) Right edge: from `root.right`, prefer right and fall back to left, skipping leaves, then **reversed**. The root is added once, and only skipped by the leaves step if it is itself a leaf.
> **Difficulty:** Medium · **Pattern:** Three-part DFS · **Also on:** [LC 545](https://leetcode.com/problems/boundary-of-binary-tree/) · [GfG](https://www.geeksforgeeks.org/problems/boundary-traversal-of-binary-tree/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/boundary-traversal-of-a-binary-tree?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Left edge + leaves + reversed right edge](#3-left-edge--leaves--reversed-right-edge) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Return the values on the boundary of a binary tree in anticlockwise order starting at the root: the root, the left boundary (excluding leaves), the leaves from left to right, and the right boundary in reverse (excluding leaves). If the root has no left child, the left boundary is empty (and similarly for the right).

| Input | Output | Why |
|---|---|---|
| `root = [1,null,2,3,4]` | `[1,3,4,2]` | no left boundary; leaves 3,4; right boundary 2 |
| `root = [1,2,3,4,5,6,null,null,null,7,8,9,10]` | `[1,2,4,7,8,9,10,6,3]` |  |

**Constraints:** `1 ≤ n ≤ 10⁴` (handle 0).

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Left edge + leaves + reversed right edge | three loops, leaves via DFS | O(n) | O(h) |

> [!tip] Interview angle
> It's all about edge cases, so state the three-part definition before coding. Common bugs: double-counting a leaf that is also on the left edge, adding the root twice when it is a leaf, and forgetting the fallback to the other child on the edges.

---

## 3. Left edge + leaves + reversed right edge

**Intuition.** Each part is a simple loop or DFS. Leaves are excluded from the edge walks, so nothing is counted twice.

**Algorithm**

1. If root null → [].
2. `res = [root.val]` unless root is a leaf (then return [root.val]).
3. Walk `cur = root.left`: while cur and not leaf, append, `cur = cur.left or cur.right`.
4. DFS from root appending leaves left→right.
5. Walk `cur = root.right` likewise (prefer right), collect, append reversed.

**Dry run** — [1,null,2,3,4]: res [1]; left edge empty; leaves 3,4; right edge from 2: not leaf → [2] reversed → [1,3,4,2].

**C++**
```cpp
bool isLeaf(TreeNode* n) { return !n->left && !n->right; }
void addLeaves(TreeNode* n, vector<int>& res) {
    if (!n) return;
    if (isLeaf(n)) { res.push_back(n->val); return; }
    addLeaves(n->left, res);
    addLeaves(n->right, res);
}
vector<int> boundaryTraversal(TreeNode* root) {
    vector<int> res;
    if (!root) return res;
    res.push_back(root->val);
    if (isLeaf(root)) return res;
    for (TreeNode* c = root->left; c && !isLeaf(c); c = c->left ? c->left : c->right) res.push_back(c->val);
    addLeaves(root, res);
    vector<int> right;
    for (TreeNode* c = root->right; c && !isLeaf(c); c = c->right ? c->right : c->left) right.push_back(c->val);
    res.insert(res.end(), right.rbegin(), right.rend());
    return res;
}
```

**Java**
```java
static boolean isLeaf(TreeNode n) { return n.left == null && n.right == null; }
static void addLeaves(TreeNode n, List<Integer> res) {
    if (n == null) return;
    if (isLeaf(n)) { res.add(n.val); return; }
    addLeaves(n.left, res);
    addLeaves(n.right, res);
}
static List<Integer> boundaryTraversal(TreeNode root) {
    List<Integer> res = new ArrayList<>();
    if (root == null) return res;
    res.add(root.val);
    if (isLeaf(root)) return res;
    for (TreeNode c = root.left; c != null && !isLeaf(c); c = c.left != null ? c.left : c.right) res.add(c.val);
    addLeaves(root, res);
    List<Integer> right = new ArrayList<>();
    for (TreeNode c = root.right; c != null && !isLeaf(c); c = c.right != null ? c.right : c.left) right.add(c.val);
    Collections.reverse(right);
    res.addAll(right);
    return res;
}
```

**Python**
```python
def boundary(root):
    if not root:
        return []
    leaf = lambda n: not n.left and not n.right
    if leaf(root):
        return [root.val]
    res = [root.val]
    cur = root.left
    while cur and not leaf(cur):
        res.append(cur.val)
        cur = cur.left or cur.right
    st = [root]
    while st:
        n = st.pop()
        if leaf(n):
            res.append(n.val)
        if n.right:
            st.append(n.right)
        if n.left:
            st.append(n.left)
    right, cur = [], root.right
    while cur and not leaf(cur):
        right.append(cur.val)
        cur = cur.right or cur.left
    return res + right[::-1]
```

**Complexity:** time **O(n)**, space **O(h)** — edges are O(h) walks, leaves are one O(n) DFS.

---

## Edge cases

- Single node → `[root]` (not twice).
- Root with only a right subtree: left boundary is empty, *not* the right subtree's left edge.
- Edge nodes that have only the 'wrong' child: fall back to it.

---

## Common mistakes

1. Including leaves in the left/right edge walk (double count).
2. Not reversing the right boundary.
3. Running the leaf DFS from `root.left`/`root.right` separately but forgetting a one-child root.

---

## Follow-ups

1. Clockwise boundary?
2. Iterative leaves?

<details><summary>Answer sketches</summary>

**#1:** Root, right edge top-down, leaves R→L, left edge bottom-up.

**#2:** Stack DFS pushing right before left (as above).
</details>

---

## Flashcards

**Boundary traversal's three parts?** #flashcard
Left edge (no leaves) · leaves L→R · right edge reversed (no leaves).

**Edge walk fallback?** #flashcard
Left edge: `left or right`; right edge: `right or left`.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
