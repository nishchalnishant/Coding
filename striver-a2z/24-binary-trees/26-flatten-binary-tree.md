---
module: striver-a2z/24-binary-trees
lesson: 26
topic: Flatten Binary Tree to LinkedList
difficulty: Medium
source: https://takeuforward.org/learning/dsa/flatten-binary-tree-to-linkedlist?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, morris, in-place, linked-list]
---
# 26. Flatten Binary Tree to LinkedList

← [Count total Nodes in a COMPLETE BT](25-count-complete-tree-nodes.md) · [Part 24 index](README.md) · Next → [Requirements needed to construct a unique BT](27-unique-bt-requirements.md)

> [!abstract] Problem at a glance
> **Task:** Rewire the tree in place into a right-pointer chain in **preorder**; every `left` becomes null.
> **Key insight:** O(1) space, Morris-style. At each node with a left child, find the **rightmost node of the left subtree** (the last node of the left part in preorder), hang the current right subtree there, move the left subtree to the right and null out left. Then step right.
> **Difficulty:** Medium · **Pattern:** Rewire via predecessor (Morris-like) · **Also on:** [LC 114](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/flatten-binary-tree-to-linkedlist?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Reverse preorder with prev](#3-reverse-preorder-with-prev) · [4. Stack](#4-stack) · [5. Morris-style rewiring](#5-morris-style-rewiring) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a binary tree, flatten it into a 'linked list' in place: use the same `TreeNode` class, where `right` points to the next node and `left` is always `null`. The list must follow preorder.

| Input | Output | Why |
|---|---|---|
| `root = [1,2,5,3,4,null,6]` | `1→2→3→4→5→6` |  |

**Constraints:** `0 ≤ n ≤ 2000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Reverse preorder with prev | visit R, L, then node.right = prev, node.left = null, prev = node | O(n) | O(h) |
| Stack | pop n; push right, left; n.right = top; n.left = null | O(n) | O(h) |
| Morris-style rewiring | pred = rightmost(left); pred.right = cur.right; cur.right = cur.left; cur.left = null | O(n) | O(1) |

> [!tip] Interview angle
> Three versions, and Striver covers all three. (1) Reverse preorder (R, L, root) with a `prev` pointer: `node.right = prev; node.left = null; prev = node`. (2) Stack: push right then left, and link to the stack top. (3) Morris-style O(1). Lead with whichever you can code bug-free, then mention the O(1) one.

---

## 3. Reverse preorder with prev

**Intuition.** Building the list from its tail means each node just points to the previously processed node. The reverse of preorder is (right, left, root).

```python
def flatten_rec(root):
    prev = None
    def go(n):
        nonlocal prev
        if not n:
            return
        go(n.right)
        go(n.left)
        n.right, n.left = prev, None
        prev = n
    go(root)
```

**Complexity:** time **O(n)**, space **O(h)**.

---

## 4. Stack

**Intuition.** It's iterative preorder where each popped node links to the next node to be popped.

```python
def flatten_stack(root):
    if not root:
        return
    st = [root]
    while st:
        n = st.pop()
        if n.right:
            st.append(n.right)
        if n.left:
            st.append(n.left)
        n.right = st[-1] if st else None
        n.left = None
```

**Complexity:** time **O(n)**, space **O(h)**.

---

## 5. Morris-style rewiring

**Intuition.** In preorder the right subtree comes right after the last node of the left subtree, which is the rightmost node of the left subtree. Splice it there, then move left to right.

**Algorithm**

1. `cur = root`.
2. While `cur`: if `cur.left`: `p = cur.left`; walk `p` to its rightmost node; `p.right = cur.right`; `cur.right = cur.left`; `cur.left = null`.
3. `cur = cur.right`.

**Dry run** — [1,2,5,3,4,null,6]: at 1: rightmost(2-sub)=4, 4.right=5 → 1→2→3? (2 still has left 3). At 2: rightmost(3)=3, 3.right=4 → 2→3→4→5→6. Done.

**C++**
```cpp
void flatten(TreeNode* root) {
    for (TreeNode* cur = root; cur; cur = cur->right) {
        if (cur->left) {
            TreeNode* p = cur->left;
            while (p->right) p = p->right;
            p->right = cur->right;
            cur->right = cur->left;
            cur->left = nullptr;
        }
    }
}
```

**Java**
```java
static void flatten(TreeNode root) {
    for (TreeNode cur = root; cur != null; cur = cur.right) {
        if (cur.left != null) {
            TreeNode p = cur.left;
            while (p.right != null) p = p.right;
            p.right = cur.right;
            cur.right = cur.left;
            cur.left = null;
        }
    }
}
```

**Python**
```python
def flatten(root):
    cur = root
    while cur:
        if cur.left:
            p = cur.left
            while p.right:
                p = p.right
            p.right = cur.right
            cur.right = cur.left
            cur.left = None
        cur = cur.right
```

**Complexity:** time **O(n)**, space **O(1)** — every edge is walked at most twice (once by `cur`, once by a predecessor search), so O(n) total, O(1) extra.

---

## Edge cases

- Empty / single node.
- Only left children: each step splices an empty right.
- Already a right chain: no work.

---

## Common mistakes

1. Forgetting `cur.left = null`, which leaves a cycle-looking structure that fails the check.
2. Recursive version visiting L before R (builds reverse order).
3. Stack version: linking `n.right` before pushing its children (loses the right subtree).

---

## Follow-ups

1. Flatten to a doubly linked list in inorder?
2. Why is Morris flatten O(n)?

<details><summary>Answer sketches</summary>

**#1:** Use left as prev, right as next; inorder with a prev pointer (BST → DLL).

**#2:** Each left-subtree right spine is walked once before it's moved.
</details>

---

## Flashcards

**Flatten (O(1) space) step?** #flashcard
Rightmost of left subtree → its right = cur.right; cur.right = cur.left; cur.left = null.

**Flatten via recursion order?** #flashcard
Right, Left, Root with a prev pointer.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
