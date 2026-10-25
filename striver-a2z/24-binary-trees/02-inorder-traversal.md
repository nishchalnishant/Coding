---
module: striver-a2z/24-binary-trees
lesson: 2
topic: Inorder Traversal
difficulty: Easy
source: https://takeuforward.org/learning/dsa/inorder-traversal?category=theory-and-traversals&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, dfs, traversal, stack]
---
# 2. Inorder Traversal

← [Binary Trees: Terminology, Representation and Traversal Templates](01-binary-tree-theory.md) · [Part 24 index](README.md) · Next → [Preorder Traversal](03-preorder-traversal.md)

> [!abstract] Problem at a glance
> **Task:** Return node values in **Left → Root → Right** order.
> **Key insight:** Recursively it's three lines. Iteratively: keep pushing the left spine onto a stack. When you can't go left any more, pop a node, visit it, and move to its right child. The stack holds exactly the ancestors whose left subtree you are still inside.
> **Difficulty:** Easy · **Pattern:** DFS (stack simulates recursion) · **Also on:** [LC 94](https://leetcode.com/problems/binary-tree-inorder-traversal/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/inorder-traversal?category=theory-and-traversals&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursive](#3-recursive) · [4. Iterative with explicit stack](#4-iterative-with-explicit-stack) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a binary tree, return the inorder traversal of its nodes' values.

| Input | Output | Why |
|---|---|---|
| `root = [1,2,3,4,5,null,6]` | `[4,2,5,1,3,6]` | left subtree (4,2,5), root 1, right subtree (3,6) |
| `root = [1,null,2,null,3]` | `[1,2,3]` | right-skewed: root comes first because there is no left subtree |

**Constraints:** `0 ≤ n ≤ 100` (LC); values `−100…100`. Assume depth may reach `n` (skewed).

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursive | go(left); visit; go(right) | O(n) | O(h) call stack |
| Iterative with explicit stack | push left spine; pop → visit → go right | O(n) | O(h) |

> [!tip] Interview angle
> Expect the follow-up "now without recursion". The iterative version is a template you reuse for kth smallest in BST, the BST iterator and validating a BST, so write it from memory. Morris (O(1) space) is the senior follow-up.

---

## 3. Recursive

**Intuition.** The definition *is* the algorithm. Each node is entered once; the call stack holds one frame per level, so the space is O(h), where h = log n balanced and n skewed.

```python
def inorder_rec(root):
    out = []
    def go(n):
        if not n:
            return
        go(n.left)
        out.append(n.val)
        go(n.right)
    go(root)
    return out
```

**Complexity:** time **O(n)**, space **O(h) call stack**.

---

## 4. Iterative with explicit stack

**Intuition.** Recursion pauses at a node while it handles the left subtree. An explicit stack stores those paused nodes. After popping a node, its left side is finished, so visit it and handle the right subtree the same way.

**Algorithm**

1. `cur = root`, `st = []`.
2. While `cur` or `st` is non-empty:
3. • While `cur`: push `cur`, `cur = cur.left`.
4. • `cur = st.pop()`; visit `cur`; `cur = cur.right`.

**Dry run** — [1,2,3,4,5,null,6]: push 1,2,4 → pop 4 (visit), right null → pop 2 (visit) → cur=5, push 5 → pop 5 → pop 1 → cur=3, push 3 → pop 3 → cur=6 → pop 6. Out 4,2,5,1,3,6.

**C++**
```cpp
vector<int> inorder(TreeNode* root) {
    vector<int> out;
    stack<TreeNode*> st;
    TreeNode* cur = root;
    while (cur || !st.empty()) {
        while (cur) { st.push(cur); cur = cur->left; }
        cur = st.top(); st.pop();
        out.push_back(cur->val);
        cur = cur->right;
    }
    return out;
}
```

**Java**
```java
static List<Integer> inorder(TreeNode root) {
    List<Integer> out = new ArrayList<>();
    Deque<TreeNode> st = new ArrayDeque<>();
    TreeNode cur = root;
    while (cur != null || !st.isEmpty()) {
        while (cur != null) { st.push(cur); cur = cur.left; }
        cur = st.pop();
        out.add(cur.val);
        cur = cur.right;
    }
    return out;
}
```

**Python**
```python
def inorder(root):
    out, st, cur = [], [], root
    while cur or st:
        while cur:
            st.append(cur)
            cur = cur.left
        cur = st.pop()
        out.append(cur.val)
        cur = cur.right
    return out
```

**Complexity:** time **O(n)**, space **O(h)** — each node is pushed and popped exactly once; the stack never holds more than one root-to-leaf path.

---

## Edge cases

- Empty tree → `[]`.
- Left-skewed tree: stack grows to n before the first visit.
- Right-skewed: stack never holds more than 1 node.

---

## Common mistakes

1. Loop condition `while st` only, which exits immediately because the stack starts empty.
2. Visiting on push instead of on pop (that gives preorder).
3. Recursion on a 10⁵-deep skewed tree overflows the Python/Java stack.

---

## Follow-ups

1. O(1) extra space?
2. Kth smallest in a BST?
3. Reverse inorder (R→Root→L)?

<details><summary>Answer sketches</summary>

**#1:** Morris inorder: thread each predecessor's right pointer back to the current node.

**#2:** Run this iterative loop and stop at the kth pop.

**#3:** Swap left/right everywhere; gives BST values descending.
</details>

---

## Flashcards

**Iterative inorder loop condition?** #flashcard
`while cur or stack` — push the left spine, pop+visit, then go right.

**What does the stack hold in iterative inorder?** #flashcard
Ancestors whose left subtree is in progress (their own visit is pending).

**Space of recursive traversal?** #flashcard
O(h): log n balanced, n skewed.

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
