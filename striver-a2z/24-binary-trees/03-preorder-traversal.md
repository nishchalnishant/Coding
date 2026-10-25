---
module: striver-a2z/24-binary-trees
lesson: 3
topic: Preorder Traversal
difficulty: Easy
source: https://takeuforward.org/learning/dsa/preorder-traversal?category=theory-and-traversals&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, dfs, traversal, stack]
---
# 3. Preorder Traversal

← [Inorder Traversal](02-inorder-traversal.md) · [Part 24 index](README.md) · Next → [Postorder Traversal](04-postorder-traversal.md)

> [!abstract] Problem at a glance
> **Task:** Return node values in **Root → Left → Right** order.
> **Key insight:** Iterative preorder is the simplest stack traversal. Pop, visit, then push **right before left** so that left is popped first.
> **Difficulty:** Easy · **Pattern:** DFS (stack) · **Also on:** [LC 144](https://leetcode.com/problems/binary-tree-preorder-traversal/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/preorder-traversal?category=theory-and-traversals&source=strivers-a2z-dsa-sheet) · **Time:** 8 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursive](#3-recursive) · [4. Iterative stack](#4-iterative-stack) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a binary tree, return the preorder traversal of its nodes' values.

| Input | Output | Why |
|---|---|---|
| `root = [1,2,3,4,5,null,6]` | `[1,2,4,5,3,6]` | root first, then the whole left subtree, then the right |
| `root = []` | `[]` |  |

**Constraints:** `0 ≤ n ≤ 100`; values `−100…100`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursive | visit; go(left); go(right) | O(n) | O(h) |
| Iterative stack | pop → visit → push right, push left | O(n) | O(h) |

> [!tip] Interview angle
> Preorder is the 'top-down' traversal. A parent is seen before its children, so it's how you copy or serialise a tree and how you pass state (depth, path sum, bounds) downward.

---

## 3. Recursive

**Intuition.** Visit, then recurse left, then right.

```python
def preorder_rec(root):
    out = []
    def go(n):
        if not n:
            return
        out.append(n.val)
        go(n.left)
        go(n.right)
    go(root)
    return out
```

**Complexity:** time **O(n)**, space **O(h)**.

---

## 4. Iterative stack

**Intuition.** A stack is LIFO, so to process left before right, push right first. Each popped node is visited immediately, since the root comes before its subtrees.

**Algorithm**

1. If root is null, return [].
2. Push root.
3. While stack: pop `n`, visit; push `n.right` if any; push `n.left` if any.

**Dry run** — [1,2,3,4,5,null,6]: pop 1 push 3,2 → pop 2 push 5,4 → pop 4 → pop 5 → pop 3 push 6 → pop 6. Out 1,2,4,5,3,6.

**C++**
```cpp
vector<int> preorder(TreeNode* root) {
    vector<int> out;
    if (!root) return out;
    stack<TreeNode*> st;
    st.push(root);
    while (!st.empty()) {
        TreeNode* n = st.top(); st.pop();
        out.push_back(n->val);
        if (n->right) st.push(n->right);
        if (n->left) st.push(n->left);
    }
    return out;
}
```

**Java**
```java
static List<Integer> preorder(TreeNode root) {
    List<Integer> out = new ArrayList<>();
    if (root == null) return out;
    Deque<TreeNode> st = new ArrayDeque<>();
    st.push(root);
    while (!st.isEmpty()) {
        TreeNode n = st.pop();
        out.add(n.val);
        if (n.right != null) st.push(n.right);
        if (n.left != null) st.push(n.left);
    }
    return out;
}
```

**Python**
```python
def preorder(root):
    if not root:
        return []
    out, st = [], [root]
    while st:
        n = st.pop()
        out.append(n.val)
        if n.right:
            st.append(n.right)
        if n.left:
            st.append(n.left)
    return out
```

**Complexity:** time **O(n)**, space **O(h)** — each node pushed/popped once. In the worst case the stack holds pending right siblings along a path, which is O(h).

---

## Edge cases

- Empty tree.
- Only left children / only right children.
- `null` children must not be pushed (or must be skipped on pop).

---

## Common mistakes

1. Pushing left before right, which gives Root→Right→Left.
2. Pushing `null` and then dereferencing it.

---

## Follow-ups

1. Postorder from this?
2. Space O(1)?

<details><summary>Answer sketches</summary>

**#1:** Push left before right to get Root→Right→Left, then reverse the output to get Left→Right→Root.

**#2:** Morris preorder: visit when you *create* the thread instead of when you remove it.
</details>

---

## Flashcards

**Iterative preorder push order?** #flashcard
Right first, then left — so left pops first.

**Which traversal serialises a tree top-down?** #flashcard
Preorder (with null markers).

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
