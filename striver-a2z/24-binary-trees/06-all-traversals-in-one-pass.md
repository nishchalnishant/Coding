---
module: striver-a2z/24-binary-trees
lesson: 6
topic: Pre, Post, Inorder in one traversal
difficulty: Medium
source: https://takeuforward.org/learning/dsa/pre,-post,-inorder-in-one-traversal?category=theory-and-traversals&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, dfs, traversal, stack]
---
# 6. Pre, Post, Inorder in one traversal

← [Level Order Traversal](05-level-order-traversal.md) · [Part 24 index](README.md) · Next → [Maximum Depth in BT](07-maximum-depth.md)

> [!abstract] Problem at a glance
> **Task:** Produce preorder, inorder and postorder lists with a single stack walk.
> **Key insight:** Push `(node, state)`. State 1 → record in **pre**, bump to 2, push left. State 2 → record in **in**, bump to 3, push right. State 3 → record in **post** and pop. Every node passes through 1→2→3, the same three moments at which recursion 'touches' a node.
> **Difficulty:** Medium · **Pattern:** Stack of (node, state) · **Also on:** [GfG](https://www.geeksforgeeks.org/problems/tree-traversal-in-a-single-stack/0)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/pre,-post,-inorder-in-one-traversal?category=theory-and-traversals&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Three separate traversals](#3-three-separate-traversals) · [4. Stack of (node, state)](#4-stack-of-node-state) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a binary tree, return `[preorder, inorder, postorder]` computed in one traversal.

| Input | Output | Why |
|---|---|---|
| `root = [1,2,3,4,5,null,6]` | `[[1,2,4,5,3,6],[4,2,5,1,3,6],[4,5,2,6,3,1]]` |  |

**Constraints:** `0 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Three separate traversals | run pre, in, post independently | O(3n) | O(h) |
| Stack of (node, state) | state 1 pre→left · 2 in→right · 3 post→pop | O(n) | O(h) |

> [!tip] Interview angle
> The point is to show you understand recursion as a state machine. Recursion reaches every node three times: on entry, between the two children, and on exit. The (node, state) stack makes those three moments explicit. The same trick converts any recursive tree DP to an iterative one.

---

## 3. Three separate traversals

**Intuition.** It's correct and fine in practice, but it misses the point of the question.

```python
def all_three_naive(root):
    pre, ino, post = [], [], []
    def go(n):
        if not n:
            return
        pre.append(n.val)
        go(n.left)
        ino.append(n.val)
        go(n.right)
        post.append(n.val)
    go(root)
    return [pre, ino, post]
```

**Complexity:** time **O(3n)**, space **O(h)**.

---

## 4. Stack of (node, state)

**Intuition.** Simulate the recursive call frame. `state` is the program counter: where this frame will resume.

**Algorithm**

1. If root null → three empty lists.
2. Push `(root, 1)`.
3. Peek top `(n, s)`:
4. • s=1: pre += n; s=2; push `(n.left,1)` if any.
5. • s=2: in += n; s=3; push `(n.right,1)` if any.
6. • s=3: post += n; pop.

**Dry run** — [1,2,3]: (1,1) pre1 → push (2,1): pre2 → (2,2) in2 → (2,3) post2 pop → (1,2) in1 → push (3,1) pre3 → in3 → post3 → (1,3) post1. pre 1,2,3 · in 2,1,3 · post 2,3,1.

**C++**
```cpp
vector<vector<int>> allThree(TreeNode* root) {
    vector<int> pre, in, post;
    if (!root) return {pre, in, post};
    stack<pair<TreeNode*, int>> st;
    st.push({root, 1});
    while (!st.empty()) {
        auto& [n, s] = st.top();
        if (s == 1) {
            pre.push_back(n->val); s = 2;
            if (n->left) st.push({n->left, 1});
        } else if (s == 2) {
            in.push_back(n->val); s = 3;
            if (n->right) st.push({n->right, 1});
        } else {
            post.push_back(n->val); st.pop();
        }
    }
    return {pre, in, post};
}
```

**Java**
```java
static List<List<Integer>> allThree(TreeNode root) {
    List<Integer> pre = new ArrayList<>(), in = new ArrayList<>(), post = new ArrayList<>();
    if (root == null) return List.of(pre, in, post);
    Deque<Object[]> st = new ArrayDeque<>();
    st.push(new Object[]{root, 1});
    while (!st.isEmpty()) {
        Object[] top = st.peek();
        TreeNode n = (TreeNode) top[0];
        int s = (int) top[1];
        if (s == 1) {
            pre.add(n.val); top[1] = 2;
            if (n.left != null) st.push(new Object[]{n.left, 1});
        } else if (s == 2) {
            in.add(n.val); top[1] = 3;
            if (n.right != null) st.push(new Object[]{n.right, 1});
        } else {
            post.add(n.val); st.pop();
        }
    }
    return List.of(pre, in, post);
}
```

**Python**
```python
def all_three(root):
    pre, ino, post = [], [], []
    if not root:
        return [pre, ino, post]
    st = [[root, 1]]
    while st:
        top = st[-1]
        n, s = top
        if s == 1:
            pre.append(n.val)
            top[1] = 2
            if n.left:
                st.append([n.left, 1])
        elif s == 2:
            ino.append(n.val)
            top[1] = 3
            if n.right:
                st.append([n.right, 1])
        else:
            post.append(n.val)
            st.pop()
    return [pre, ino, post]
```

**Complexity:** time **O(n)**, space **O(h)** — each node is touched exactly three times (states 1, 2, 3).

---

## Edge cases

- Empty tree → `[[],[],[]]`.
- Single node: all three lists equal.
- C++: `auto& [n, s] = st.top()` — take a reference *before* pushing (the push may invalidate it only for vector-backed stacks; `std::stack` defaults to deque, where push doesn't invalidate references).

---

## Common mistakes

1. Popping in state 1 or 2: the node must stay on the stack until state 3.
2. Pushing a child before updating the parent's state, which re-records the parent.
3. Copying `(n, s)` by value and bumping the copy.

---

## Follow-ups

1. Iterative tree DP (e.g. height) without recursion?

<details><summary>Answer sketches</summary>

**#1:** Same (node, state) stack; compute the node's value in state 3 from children's stored results.
</details>

---

## Flashcards

**(node, state) traversal: what happens in each state?** #flashcard
1: pre, push left · 2: in, push right · 3: post, pop.

**How many times does recursion 'touch' each node?** #flashcard
Three: entry (pre), between children (in), exit (post).

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
