---
module: striver/25-binary-search-trees
lesson: 12
topic: BST iterator
difficulty: Medium
source: https://takeuforward.org/learning/dsa/bst-iterator?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search-trees, bst, iterator, design, stack]
---
# 12. BST iterator

← [Inorder successor and predecessor in BST](11-inorder-successor-predecessor.md) · [Part 25 index](README.md) · Next → [Two sum in BST](13-two-sum-in-bst.md)

> [!abstract] Problem at a glance
> **Task:** Design `BSTIterator(root)` with `next()` (the next smallest value) and `hasNext()`.
> **Key insight:** Turn iterative inorder into a resumable object. The stack holds the **left spine** still to be visited. `next()` pops the top (the smallest remaining), then pushes the left spine of its right child. Each node is pushed and popped once, so it's **amortised O(1)** per call with O(h) memory.
> **Difficulty:** Medium · **Pattern:** Paused inorder (stack) · **Also on:** [LC 173](https://leetcode.com/problems/binary-search-tree-iterator/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/bst-iterator?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Flatten to list](#3-flatten-to-list) · [4. Stack of left spine](#4-stack-of-left-spine) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Implement `BSTIterator`: the constructor takes the BST root; `next()` returns the next number in ascending order; `hasNext()` returns whether one exists. `next()` is only called when valid.

| Input | Output | Why |
|---|---|---|
| `[7,3,15,null,null,9,20]; next ×5` | `[3,7,9,15,20]` | inorder, produced lazily |

**Constraints:** `1 ≤ n ≤ 10⁵`; at most 10⁵ calls. Target: average O(1) time, O(h) memory.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Flatten to list | precompute inorder; pointer | O(1) per call | O(n) |
| Stack of left spine | push left spine; next = pop + push left spine of right | O(1) amortised | O(h) |

> [!tip] Interview angle
> The interviewer wants the O(h)-memory version and an explanation of 'amortised O(1)'. Over all calls each node is pushed once and popped once, so n calls cost O(n) in total. A single `next()` can cost O(h).

---

## 3. Flatten to list

**Intuition.** Store the whole inorder sequence up front and step through it. It's simple but uses O(n) memory and does all the work eagerly.

```python
class BSTIteratorList:
    def __init__(self, root):
        self.a, self.i = [], 0
        def go(n):
            if n:
                go(n.left); self.a.append(n.val); go(n.right)
        go(root)

    def next(self):
        self.i += 1
        return self.a[self.i - 1]

    def hasNext(self):
        return self.i < len(self.a)
```

**Complexity:** time **O(1) per call**, space **O(n)**.

---

## 4. Stack of left spine

**Intuition.** The stack top is always the smallest unvisited node. After visiting it, its right subtree comes next in inorder, and that subtree's leftmost node is the next smallest. So push its left spine.

**Algorithm**

1. Constructor: `push_left(root)`.
2. `next()`: `n = pop()`; `push_left(n.right)`; return `n.val`.
3. `hasNext()`: stack non-empty.
4. `push_left(x)`: while `x`: push, `x = x.left`.

**Dry run** — [7,3,15,null,null,9,20]: init stack [7,3]. next → 3 (no right) → [7]. next → 7, push 15, 9 → [15,9]. next → 9 → [15]. next → 15, push 20 → [20]. next → 20 → [].

**C++**
```cpp
class BSTIterator {
    stack<TreeNode*> st;
    void pushLeft(TreeNode* n) { while (n) { st.push(n); n = n->left; } }
public:
    BSTIterator(TreeNode* root) { pushLeft(root); }
    int next() {
        TreeNode* n = st.top(); st.pop();
        pushLeft(n->right);
        return n->val;
    }
    bool hasNext() { return !st.empty(); }
};
```

**Java**
```java
static class BSTIterator {
    private final Deque<TreeNode> st = new ArrayDeque<>();
    BSTIterator(TreeNode root) { pushLeft(root); }
    private void pushLeft(TreeNode n) { while (n != null) { st.push(n); n = n.left; } }
    int next() {
        TreeNode n = st.pop();
        pushLeft(n.right);
        return n.val;
    }
    boolean hasNext() { return !st.isEmpty(); }
}
```

**Python**
```python
class BSTIterator:
    def __init__(self, root):
        self.st = []
        self._push(root)

    def _push(self, n):
        while n:
            self.st.append(n)
            n = n.left

    def next(self):
        n = self.st.pop()
        self._push(n.right)
        return n.val

    def hasNext(self):
        return bool(self.st)
```

**Complexity:** time **O(1) amortised**, space **O(h)** — each node is pushed and popped once over the whole iteration; the stack holds one root-to-leaf path.

---

## Edge cases

- Empty tree → `hasNext()` false immediately.
- Skewed left → the constructor pushes n nodes, then each `next()` is O(1).
- Skewed right → stack size stays 1.

---

## Common mistakes

1. Pushing the whole tree in the constructor (that's the O(n) list in disguise).
2. Pushing only `n.right` instead of its whole left spine.
3. Claiming worst-case O(1) per `next()` (it's amortised).

---

## Follow-ups

1. Descending iterator (`before()`)?
2. `peek()`?
3. Two-sum in a BST in O(h) space?

<details><summary>Answer sketches</summary>

**#1:** Mirror: push the right spine, pop, push the right spine of the left child.

**#2:** Return the top without popping.

**#3:** One ascending and one descending iterator as two pointers (next problem).
</details>

---

## Flashcards

**BST iterator: what's on the stack?** #flashcard
The left spine of the unvisited part; the top is the next smallest.

**BST iterator `next()` cost?** #flashcard
Amortised O(1); worst case O(h) for a single call.

**BST iterator memory?** #flashcard
O(h).

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
