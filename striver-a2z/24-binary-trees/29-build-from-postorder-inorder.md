---
module: striver-a2z/24-binary-trees
lesson: 29
topic: Construct a BT from Postorder and Inorder
difficulty: Medium
source: https://takeuforward.org/learning/dsa/construct-a-bt-from-postorder-and-inorder?category=construction-problems&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, construction, divide-and-conquer, hashing]
---
# 29. Construct a BT from Postorder and Inorder

← [Construct a BT from Preorder and Inorder](28-build-from-preorder-inorder.md) · [Part 24 index](README.md) · Next → [Serialize and De-serialize BT](30-serialize-deserialize.md)

> [!abstract] Problem at a glance
> **Task:** Rebuild the tree from postorder and inorder (unique values).
> **Key insight:** It mirrors the preorder version: the root is `post[pR]`. With the left size `k − iL`, the left subtree is `post[pL .. pL+left−1]` and the right is `post[pL+left .. pR−1]`. In the global-pointer variant, consume postorder **from the back** and build the **right subtree first**.
> **Difficulty:** Medium · **Pattern:** Divide & conquer + index map · **Also on:** [LC 106](https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/construct-a-bt-from-postorder-and-inorder?category=construction-problems&source=strivers-a2z-dsa-sheet) · **Time:** 12 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Global pointer from the back](#3-global-pointer-from-the-back) · [4. Bounds + hash map](#4-bounds--hash-map) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given two integer arrays `inorder` and `postorder` of the same binary tree (unique values), construct and return the tree. (Arguments here: `postorder`, then `inorder`.)

| Input | Output | Why |
|---|---|---|
| `postorder = [9,15,7,20,3], inorder = [9,3,15,20,7]` | `[3,9,20,null,null,15,7]` |  |

**Constraints:** `1 ≤ n ≤ 3000`; unique values.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Global pointer from the back | idx = n−1; build right subtree before left | O(n) | O(n) |
| Bounds + hash map | root = post[pR]; left size = k − iL | O(n) | O(n) |

> [!tip] Interview angle
> Show you understand the symmetry rather than memorising two solutions: preorder reads root-first from the left, postorder reads root-first from the right. With a global pointer, the order of the recursive calls has to flip, and that's the bug interviewers watch for.

---

## 3. Global pointer from the back

**Intuition.** Reading postorder backwards gives root, right, left, so recurse in that order.

```python
def build_post_ptr(post, ino):
    pos = {v: i for i, v in enumerate(ino)}
    idx = len(post) - 1
    def build(il, ir):
        nonlocal idx
        if il > ir:
            return None
        root = TreeNode(post[idx])
        idx -= 1
        k = pos[root.val]
        root.right = build(k + 1, ir)
        root.left = build(il, k - 1)
        return root
    return build(0, len(ino) - 1)
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Bounds + hash map

**Intuition.** Explicit ranges make it independent of call order.

**Algorithm**

1. `pos` map over inorder.
2. `build(pL, pR, iL)`: if `pL > pR` → null.
3. `root = post[pR]`, `k = pos[root]`, `left = k − iL`.
4. `left child = build(pL, pL+left−1, iL)`; `right = build(pL+left, pR−1, k+1)`.

**Dry run** — post [9,15,7,20,3]: root 3, k=1, left 1 → post[0..0]=[9]; right post[1..3]=[15,7,20] → root 20, k=3 (iL 2) left 1 → [15], right [7].

**C++**
```cpp
TreeNode* bpo(vector<int>& post, int pl, int pr, int il, unordered_map<int, int>& pos) {
    if (pl > pr) return nullptr;
    TreeNode* root = new TreeNode(post[pr]);
    int k = pos[post[pr]], left = k - il;
    root->left = bpo(post, pl, pl + left - 1, il, pos);
    root->right = bpo(post, pl + left, pr - 1, k + 1, pos);
    return root;
}
TreeNode* buildTreePost(vector<int> postorder, vector<int> inorder) {
    unordered_map<int, int> pos;
    for (int i = 0; i < (int)inorder.size(); i++) pos[inorder[i]] = i;
    return bpo(postorder, 0, (int)postorder.size() - 1, 0, pos);
}
```

**Java**
```java
static TreeNode bpo(int[] post, int pl, int pr, int il, Map<Integer, Integer> pos) {
    if (pl > pr) return null;
    TreeNode root = new TreeNode(post[pr]);
    int k = pos.get(post[pr]), left = k - il;
    root.left = bpo(post, pl, pl + left - 1, il, pos);
    root.right = bpo(post, pl + left, pr - 1, k + 1, pos);
    return root;
}
static TreeNode buildTreePost(int[] postorder, int[] inorder) {
    Map<Integer, Integer> pos = new HashMap<>();
    for (int i = 0; i < inorder.length; i++) pos.put(inorder[i], i);
    return bpo(postorder, 0, postorder.length - 1, 0, pos);
}
```

**Python**
```python
def build_post(post, ino):
    pos = {v: i for i, v in enumerate(ino)}
    def build(pl, pr, il):
        if pl > pr:
            return None
        root = TreeNode(post[pr])
        k = pos[post[pr]]
        left = k - il
        root.left = build(pl, pl + left - 1, il)
        root.right = build(pl + left, pr - 1, k + 1)
        return root
    return build(0, len(post) - 1, 0)
```

**Complexity:** time **O(n)**, space **O(n)** — one node per call, O(1) map lookups.

---

## Edge cases

- Single node.
- Skewed trees (recursion depth n).
- Empty input.

---

## Common mistakes

1. Global-pointer version building left before right (wrong tree).
2. Right range `pL+left .. pR−1`: forgetting the −1 (root counted twice).
3. Mixing up the argument order (LC 106 passes inorder first).

---

## Follow-ups

1. Which pairs are enough?
2. Build a BST from preorder alone?

<details><summary>Answer sketches</summary>

**#1:** See *Requirements needed to construct a unique BT*: inorder + one of pre/post.

**#2:** Yes — bounds recursion (next part, LC 1008).
</details>

---

## Flashcards

**Post+In: where is the root?** #flashcard
Last element of the postorder range.

**Post+In global pointer: recursion order?** #flashcard
Right subtree before left (reading postorder backwards).

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
