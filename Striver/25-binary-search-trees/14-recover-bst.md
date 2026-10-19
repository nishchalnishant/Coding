---
module: striver/25-binary-search-trees
lesson: 14
topic: Correct BST with two nodes swapped
difficulty: Hard
source: https://takeuforward.org/learning/dsa/correct-bst-with-two-nodes-swapped?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search-trees, bst, inorder, recovery]
---
# 14. Correct BST with two nodes swapped

← [Two sum in BST](13-two-sum-in-bst.md) · [Part 25 index](README.md) · Next → [Largest BST in Binary Tree](15-largest-bst-subtree.md)

> [!abstract] Problem at a glance
> **Task:** Exactly two node values were swapped. Fix the tree in place without changing its structure.
> **Key insight:** In the inorder sequence, a swap produces either **one** descent (adjacent elements swapped) or **two** descents (distant elements). Record `first` = the larger element of the first descent and `last` = the smaller element of the last descent, then swap their values.
> **Difficulty:** Hard · **Pattern:** Inorder with prev + violation tracking · **Also on:** [LC 99](https://leetcode.com/problems/recover-binary-search-tree/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/correct-bst-with-two-nodes-swapped?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Sort the inorder values](#3-sort-the-inorder-values) · [4. Inorder, track first/last violation](#4-inorder-track-firstlast-violation) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

You are given the `root` of a BST in which the values of exactly two nodes were swapped by mistake. Recover the tree without changing its structure.

| Input | Output | Why |
|---|---|---|
| `root = [1,3,null,null,2]` | `[3,1,null,null,2]` | inorder 3 2 1 → descents (3,2) and (2,1) → swap 3 and 1 |
| `root = [3,1,4,null,null,2]` | `[2,1,4,null,null,3]` | inorder 1 3 2 4 → one descent (3,2) → swap them |

**Constraints:** `2 ≤ n ≤ 1000`; `−2³¹ ≤ val ≤ 2³¹ − 1`. Follow-up: O(1) space.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Sort the inorder values | inorder vals → sort → write back in inorder | O(n log n) | O(n) |
| Inorder, track first/last violation | on prev > cur: first ← prev (once), last ← cur | O(n) | O(h) |

> [!tip] Interview angle
> Draw the inorder sequence and show both cases (adjacent vs distant swap). Recording `first` once and updating `last` at every descent covers both without special-casing. The O(1) follow-up is Morris inorder with the same prev logic.

---

## 3. Sort the inorder values

**Intuition.** The correct BST has the same structure and the same multiset of values in sorted inorder. Collect, sort and reassign in a second inorder pass.

```python
def recover_sort(root):
    nodes = []
    def go(n):
        if n:
            go(n.left); nodes.append(n); go(n.right)
    go(root)
    for n, v in zip(nodes, sorted(n.val for n in nodes)):
        n.val = v
```

**Complexity:** time **O(n log n)**, space **O(n)**.

---

## 4. Inorder, track first/last violation

**Intuition.** Walk the inorder sequence with `prev`. At each descent (`prev.val > cur.val`), set `first = prev` if it isn't set yet, and always set `last = cur`. An adjacent swap gives one descent, which sets both. A distant swap gives two, and `last` is updated at the second.

**Algorithm**

1. Iterative inorder with `prev = None`, `first = last = None`.
2. On each visit: if `prev` and `prev.val > cur.val`: `first = first or prev`; `last = cur`.
3. `prev = cur`.
4. Swap `first.val` and `last.val`.

**Dry run** — [1,3,null,null,2], inorder 3 2 1: (3,2) → first 3, last 2; (2,1) → last 1. Swap 3 ↔ 1 → inorder 1 2 3.

**C++**
```cpp
void recoverTree(TreeNode* root) {
    stack<TreeNode*> st;
    TreeNode *cur = root, *prev = nullptr, *first = nullptr, *last = nullptr;
    while (cur || !st.empty()) {
        while (cur) { st.push(cur); cur = cur->left; }
        cur = st.top(); st.pop();
        if (prev && prev->val > cur->val) {
            if (!first) first = prev;
            last = cur;
        }
        prev = cur;
        cur = cur->right;
    }
    swap(first->val, last->val);
}
```

**Java**
```java
static void recoverTree(TreeNode root) {
    Deque<TreeNode> st = new ArrayDeque<>();
    TreeNode cur = root, prev = null, first = null, last = null;
    while (cur != null || !st.isEmpty()) {
        while (cur != null) { st.push(cur); cur = cur.left; }
        cur = st.pop();
        if (prev != null && prev.val > cur.val) {
            if (first == null) first = prev;
            last = cur;
        }
        prev = cur;
        cur = cur.right;
    }
    int t = first.val; first.val = last.val; last.val = t;
}
```

**Python**
```python
def recover_tree(root):
    st, cur, prev = [], root, None
    first = last = None
    while cur or st:
        while cur:
            st.append(cur)
            cur = cur.left
        cur = st.pop()
        if prev and prev.val > cur.val:
            if not first:
                first = prev
            last = cur
        prev = cur
        cur = cur.right
    first.val, last.val = last.val, first.val
```

**Complexity:** time **O(n)**, space **O(h)** — a single inorder pass; the stack is O(h).

---

## Edge cases

- Adjacent swap (one descent).
- Root swapped with a leaf.
- Two-node tree.
- Values at the int limits (compare nodes, don't use sentinels).

---

## Common mistakes

1. Setting `last = prev` at the second descent (it must be `cur`).
2. Overwriting `first` at the second descent.
3. Swapping nodes (pointers) instead of values: the structure must not change.
4. Using an int sentinel for `prev`.

---

## Follow-ups

1. O(1) space?
2. More than two nodes swapped?
3. Array version?

<details><summary>Answer sketches</summary>

**#1:** Morris inorder with the same prev/first/last logic.

**#2:** No longer O(n) by this trick; sort the inorder (O(n log n)) and reassign.

**#3:** Same descent logic on a nearly sorted array with one swap.
</details>

---

## Flashcards

**Recover BST: what to record at a descent prev > cur?** #flashcard
`first = prev` (only the first time); `last = cur` (every time).

**Recover BST: why can there be one or two descents?** #flashcard
Adjacent swapped elements create one descent; distant ones create two.

**Recover BST in O(1) space?** #flashcard
Morris inorder.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
