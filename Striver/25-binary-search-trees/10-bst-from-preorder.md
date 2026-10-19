---
module: striver/25-binary-search-trees
lesson: 10
topic: Construct a BST from a preorder traversal
difficulty: Medium
source: https://takeuforward.org/learning/dsa/construct-a-bst-from-a-preorder-traversal?category=medium&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search-trees, bst, construction, preorder]
---
# 10. Construct a BST from a preorder traversal

← [LCA in BST](09-lca-in-bst.md) · [Part 25 index](README.md) · Next → [Inorder successor and predecessor in BST](11-inorder-successor-predecessor.md)

> [!abstract] Problem at a glance
> **Task:** Rebuild the BST whose preorder traversal is `preorder`.
> **Key insight:** For a BST, preorder alone is enough because the ordering is the missing inorder. Consume values left to right with a shared index. A subtree accepts the next value only if it's **below the upper bound** inherited from its ancestors. When a value exceeds the bound, that subtree is finished. O(n) total.
> **Difficulty:** Medium · **Pattern:** Preorder + upper bound · **Also on:** [LC 1008](https://leetcode.com/problems/construct-binary-search-tree-from-preorder-traversal/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/construct-a-bst-from-a-preorder-traversal?category=medium&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Insert one by one](#3-insert-one-by-one) · [4. Upper-bound recursion](#4-upper-bound-recursion) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `preorder` of distinct values that is the preorder traversal of some BST, construct and return its root.

| Input | Output | Why |
|---|---|---|
| `preorder = [8,5,1,7,10,12]` | `[8,5,10,1,7,null,12]` | 8 root; 5,1,7 < 8 form the left subtree; 10,12 the right |
| `preorder = [1,3]` | `[1,null,3]` |  |

**Constraints:** `1 ≤ n ≤ 100`; values distinct, `1…10⁸`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Insert one by one | BST insert each value in order | O(n²) worst, O(n log n) avg | O(h) |
| Upper-bound recursion | build(bound): take pre[i] if < bound; left = build(val), right = build(bound) | O(n) | O(h) |

> [!tip] Interview angle
> Give all three approaches with their costs: n inserts O(n²) worst; sort to get the inorder and use the pre+in build O(n log n); upper-bound recursion O(n). The last is the one they want.

---

## 3. Insert one by one

**Intuition.** Inserting values in preorder reproduces the same tree, because every node is inserted after its ancestors.

```python
def bst_pre_insert(pre):
    root = None
    for v in pre:
        if not root:
            root = TreeNode(v)
            continue
        cur = root
        while True:
            side = "left" if v < cur.val else "right"
            nxt = getattr(cur, side)
            if not nxt:
                setattr(cur, side, TreeNode(v))
                break
            cur = nxt
    return root
```

**Complexity:** time **O(n²) worst, O(n log n) avg**, space **O(h)**.

---

## 4. Upper-bound recursion

**Intuition.** `build(bound)` builds the largest subtree from the current index whose values are all `< bound`. The left child's bound is the node's value and the right child's bound is the parent's bound. The lower bound is implied: preorder never hands us a value smaller than one already finished.

**Algorithm**

1. `i = 0`.
2. `build(bound)`: if `i == n` or `pre[i] > bound` → null.
3. `node = pre[i]`, `i += 1`; `node.left = build(node.val)`; `node.right = build(bound)`; return node.
4. Return `build(+∞)`.

**Dry run** — [8,5,1,7,10,12]: build(∞) → 8; left build(8) → 5; left build(5) → 1; build(1): 7 > 1 → null; right build(5): 7 > 5 → null. 5.right = build(8) → 7 … 8.right = build(∞) → 10 → 12.

**C++**
```cpp
TreeNode* buildPre(const vector<int>& pre, int& i, long long bound) {
    if (i == (int)pre.size() || pre[i] > bound) return nullptr;
    TreeNode* node = new TreeNode(pre[i++]);
    node->left = buildPre(pre, i, node->val);
    node->right = buildPre(pre, i, bound);
    return node;
}
TreeNode* bstFromPreorder(const vector<int>& pre) {
    int i = 0;
    return buildPre(pre, i, LLONG_MAX);
}
```

**Java**
```java
static int preIdx;
static TreeNode buildPre(int[] pre, long bound) {
    if (preIdx == pre.length || pre[preIdx] > bound) return null;
    TreeNode node = new TreeNode(pre[preIdx++]);
    node.left = buildPre(pre, node.val);
    node.right = buildPre(pre, bound);
    return node;
}
static TreeNode bstFromPreorder(int[] pre) {
    preIdx = 0;
    return buildPre(pre, Long.MAX_VALUE);
}
```

**Python**
```python
def bst_from_preorder(pre):
    i = 0
    def build(bound):
        nonlocal i
        if i == len(pre) or pre[i] > bound:
            return None
        node = TreeNode(pre[i])
        i += 1
        node.left = build(node.val)
        node.right = build(bound)
        return node
    return build(float("inf"))
```

**Complexity:** time **O(n)**, space **O(h)** — each value is consumed once; each null return is charged to a consumed node.

---

## Edge cases

- Single value.
- Strictly decreasing preorder → left-skewed.
- Strictly increasing → right-skewed.

---

## Common mistakes

1. Passing the index by value, so the recursion re-reads the same element.
2. Using the node's value as the bound for the right child (it must be the parent's bound).
3. Forgetting to reset a static index between test cases.

---

## Follow-ups

1. From postorder?
2. Verify a preorder is a valid BST preorder (LC 255)?
3. Serialise a BST compactly?

<details><summary>Answer sketches</summary>

**#1:** Consume from the end with a lower bound, building right before left.

**#2:** Monotonic stack: pop while top < x, raising a running lower bound; fail if x < lower bound.

**#3:** Preorder without nulls, rebuilt with this algorithm.
</details>

---

## Flashcards

**Why is preorder enough for a BST?** #flashcard
Sorting the values gives the inorder; the bound trick avoids even that.

**Upper-bound build: bounds for the children?** #flashcard
Left: `node.val`; right: the parent's bound.

**Complexity of upper-bound construction?** #flashcard
O(n) time, O(h) space.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
