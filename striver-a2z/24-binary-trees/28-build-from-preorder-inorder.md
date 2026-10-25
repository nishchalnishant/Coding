---
module: striver-a2z/24-binary-trees
lesson: 28
topic: Construct a BT from Preorder and Inorder
difficulty: Medium
source: https://takeuforward.org/learning/dsa/construct-a-bt-from-preorder-and-inorder?category=construction-problems&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, construction, divide-and-conquer, hashing]
---
# 28. Construct a BT from Preorder and Inorder

← [Requirements needed to construct a unique BT](27-unique-bt-requirements.md) · [Part 24 index](README.md) · Next → [Construct a BT from Postorder and Inorder](29-build-from-postorder-inorder.md)

> [!abstract] Problem at a glance
> **Task:** Rebuild the tree (unique values) from its preorder and inorder sequences.
> **Key insight:** `pre[0]` is the root. Its position `k` in inorder splits inorder into left (`k − inL` nodes) and right. Those sizes slice preorder the same way. A **hash map value → inorder index** makes each lookup O(1), so the whole build is O(n). Passing index bounds instead of slicing avoids O(n²).
> **Difficulty:** Medium · **Pattern:** Divide & conquer + index map · **Also on:** [LC 105](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/construct-a-bt-from-preorder-and-inorder?category=construction-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Slicing + index()](#3-slicing--index) · [4. Bounds + hash map](#4-bounds--hash-map) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given two integer arrays `preorder` and `inorder` of the same binary tree (values are unique), construct and return the tree.

| Input | Output | Why |
|---|---|---|
| `preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]` | `[3,9,20,null,null,15,7]` |  |

**Constraints:** `1 ≤ n ≤ 3000`; unique values.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Slicing + index() | root = pre[0]; k = ino.index(root); recurse on slices | O(n²) | O(n²) |
| Bounds + hash map | pos[val] = inorder index; build(preL, preR, inL, inR) | O(n) | O(n) |

> [!tip] Interview angle
> Write the recursion with four bounds `(preL, preR, inL, inR)` or the shorter 'global preorder pointer' version. Either way, mention why slicing is O(n²) and the hash map is mandatory. Deep skewed inputs can blow Python's recursion limit, so mention the iterative stack version as a follow-up.

---

## 3. Slicing + index()

**Intuition.** It's the definition taken literally. Each level copies and searches arrays.

```python
def build_slice(pre, ino):
    if not pre:
        return None
    root = TreeNode(pre[0])
    k = ino.index(pre[0])
    root.left = build_slice(pre[1:k + 1], ino[:k])
    root.right = build_slice(pre[k + 1:], ino[k + 1:])
    return root
```

**Complexity:** time **O(n²)**, space **O(n²)**.

---

## 4. Bounds + hash map

**Intuition.** Index ranges replace slices. The map replaces the linear search.

**Algorithm**

1. `pos = {v: i for i, v in enumerate(ino)}`.
2. `build(pL, pR, iL, iR)`: if `pL > pR` → null.
3. `root = pre[pL]`, `k = pos[root]`, `left = k − iL`.
4. `left child = build(pL+1, pL+left, iL, k−1)`; `right = build(pL+left+1, pR, k+1, iR)`.

**Dry run** — pre [3,9,20,15,7], in [9,3,15,20,7]: root 3, k=1, left size 1 → left from pre[1..1]=[9]; right from pre[2..4] with in[2..4] → root 20, k=3, left [15], right [7].

**C++**
```cpp
TreeNode* bpi(vector<int>& pre, int pl, int pr, int il, unordered_map<int, int>& pos) {
    if (pl > pr) return nullptr;
    TreeNode* root = new TreeNode(pre[pl]);
    int k = pos[pre[pl]], left = k - il;
    root->left = bpi(pre, pl + 1, pl + left, il, pos);
    root->right = bpi(pre, pl + left + 1, pr, k + 1, pos);
    return root;
}
TreeNode* buildTree(vector<int> preorder, vector<int> inorder) {
    unordered_map<int, int> pos;
    for (int i = 0; i < (int)inorder.size(); i++) pos[inorder[i]] = i;
    return bpi(preorder, 0, (int)preorder.size() - 1, 0, pos);
}
```

**Java**
```java
static TreeNode bpi(int[] pre, int pl, int pr, int il, Map<Integer, Integer> pos) {
    if (pl > pr) return null;
    TreeNode root = new TreeNode(pre[pl]);
    int k = pos.get(pre[pl]), left = k - il;
    root.left = bpi(pre, pl + 1, pl + left, il, pos);
    root.right = bpi(pre, pl + left + 1, pr, k + 1, pos);
    return root;
}
static TreeNode buildTree(int[] preorder, int[] inorder) {
    Map<Integer, Integer> pos = new HashMap<>();
    for (int i = 0; i < inorder.length; i++) pos.put(inorder[i], i);
    return bpi(preorder, 0, preorder.length - 1, 0, pos);
}
```

**Python**
```python
def build_tree(pre, ino):
    pos = {v: i for i, v in enumerate(ino)}
    def build(pl, pr, il, ir):
        if pl > pr:
            return None
        root = TreeNode(pre[pl])
        k = pos[pre[pl]]
        left = k - il
        root.left = build(pl + 1, pl + left, il, k - 1)
        root.right = build(pl + left + 1, pr, k + 1, ir)
        return root
    return build(0, len(pre) - 1, 0, len(ino) - 1)
```

**Complexity:** time **O(n)**, space **O(n)** — each node is created once with an O(1) lookup. (`inR` is implied by the preorder range, so C++/Java drop it.)

---

## Edge cases

- Single node.
- Left-skewed (pre == reversed in) and right-skewed (pre == in): recursion depth n.
- Empty arrays.

---

## Common mistakes

1. Off-by-one in the preorder split: left part is `pL+1 .. pL+leftSize`.
2. Using `ino.index` inside recursion (O(n²)).
3. Duplicate values: the map silently picks one, so the tree is wrong.

---

## Follow-ups

1. Iterative O(n)?
2. Pre + post (full tree)?

<details><summary>Answer sketches</summary>

**#1:** Stack of nodes; push left children while pre[i] ≠ in[j]; pop while top == in[j] then attach right.

**#2:** LC 889: left subtree root is pre[1], find it in post.
</details>

---

## Flashcards

**Pre+In build: how to find the left subtree size?** #flashcard
k − inL, where k = inorder index of the root (via hash map).

**Pre+In build complexity with a map?** #flashcard
O(n) time, O(n) space.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
