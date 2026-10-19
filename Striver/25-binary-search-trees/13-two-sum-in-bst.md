---
module: striver/25-binary-search-trees
lesson: 13
topic: Two sum in BST
difficulty: Medium
source: https://takeuforward.org/learning/dsa/two-sum-in-bst?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search-trees, bst, two-pointers, iterator]
---
# 13. Two sum in BST

← [BST iterator](12-bst-iterator.md) · [Part 25 index](README.md) · Next → [Correct BST with two nodes swapped](14-recover-bst.md)

> [!abstract] Problem at a glance
> **Task:** Return whether two **different** nodes sum to `k`.
> **Key insight:** The inorder sequence is sorted, so this is two-sum on a sorted array: a left pointer moving up and a right pointer moving down. Run an ascending BST iterator and a descending one; that's two pointers in O(h) memory without materialising the array.
> **Difficulty:** Medium · **Pattern:** Two pointers via two BST iterators · **Also on:** [LC 653](https://leetcode.com/problems/two-sum-iv-input-is-a-bst/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/two-sum-in-bst?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Hash set DFS](#3-hash-set-dfs) · [4. Two BST iterators](#4-two-bst-iterators) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a BST and an integer `k`, return `true` if there exist two distinct nodes whose values sum to `k`.

| Input | Output | Why |
|---|---|---|
| `root = [5,3,6,2,4,null,7], k = 9` | `true` | 2+7, 3+6, 4+5 |
| `same tree, k = 28` | `false` |  |

**Constraints:** `1 ≤ n ≤ 10⁴`; `−10⁴ ≤ val ≤ 10⁴`; `−10⁵ ≤ k ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Hash set DFS | for each node: k − val seen? | O(n) | O(n) |
| Two BST iterators | lo = next(), hi = before(); move the side that fixes the sum | O(n) | O(h) |

> [!tip] Interview angle
> Three answers, each better on one axis: a hash set during DFS (O(n)/O(n), works on any tree); inorder array + two pointers (O(n)/O(n)); two iterators (O(n)/O(h)). The last uses the BST. Stop when the two iterators meet, so a node is never paired with itself.

---

## 3. Hash set DFS

**Intuition.** Classic two-sum during any traversal. It ignores the BST property.

```python
def two_sum_set(root, k):
    seen, st = set(), [root] if root else []
    while st:
        n = st.pop()
        if k - n.val in seen:
            return True
        seen.add(n.val)
        st += [c for c in (n.left, n.right) if c]
    return False
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Two BST iterators

**Intuition.** `lo` yields ascending values from the left stack and `hi` yields descending values from the right stack. With sum `s = lo + hi`: if `s < k`, advance `lo`; if `s > k`, advance `hi`. Stop when `lo ≥ hi`. Values are distinct, so `lo == hi` means the same node.

**Algorithm**

1. `L` = left spine stack; `R` = right spine stack.
2. `nxt()`: pop `L`, push left spine of its right child. `prv()`: pop `R`, push right spine of its left child.
3. `i, j = nxt(), prv()`. While `i < j`: equal → true; `< k` → `i = nxt()`; else `j = prv()`.
4. Return false.

**Dry run** — [5,3,6,2,4,null,7], k 9: i 2, j 7 → 9 ✓. k 28: 2+7 < 28 → i 3, 4, 5, 6, then 7 = j → stop → false.

**C++**
```cpp
bool findTarget(TreeNode* root, int k) {
    stack<TreeNode*> L, R;
    auto push = [](stack<TreeNode*>& st, TreeNode* n, bool left) {
        while (n) { st.push(n); n = left ? n->left : n->right; }
    };
    push(L, root, true); push(R, root, false);
    auto nxt = [&] { TreeNode* n = L.top(); L.pop(); push(L, n->right, true); return n->val; };
    auto prv = [&] { TreeNode* n = R.top(); R.pop(); push(R, n->left, false); return n->val; };
    int i = nxt(), j = prv();
    while (i < j) {
        if (i + j == k) return true;
        if (i + j < k) i = nxt(); else j = prv();
    }
    return false;
}
```

**Java**
```java
static void pushSpine(Deque<TreeNode> st, TreeNode n, boolean left) {
    while (n != null) { st.push(n); n = left ? n.left : n.right; }
}
static boolean findTarget(TreeNode root, int k) {
    Deque<TreeNode> L = new ArrayDeque<>(), R = new ArrayDeque<>();
    pushSpine(L, root, true); pushSpine(R, root, false);
    TreeNode a = L.pop(); pushSpine(L, a.right, true);
    TreeNode b = R.pop(); pushSpine(R, b.left, false);
    int i = a.val, j = b.val;
    while (i < j) {
        if (i + j == k) return true;
        if (i + j < k) { a = L.pop(); pushSpine(L, a.right, true); i = a.val; }
        else { b = R.pop(); pushSpine(R, b.left, false); j = b.val; }
    }
    return false;
}
```

**Python**
```python
def find_target(root, k):
    L, R = [], []
    def push(st, n, side):
        while n:
            st.append(n)
            n = getattr(n, side)
    push(L, root, "left")
    push(R, root, "right")
    def nxt():
        n = L.pop()
        push(L, n.right, "left")
        return n.val
    def prv():
        n = R.pop()
        push(R, n.left, "right")
        return n.val
    i, j = nxt(), prv()
    while i < j:
        if i + j == k:
            return True
        if i + j < k:
            i = nxt()
        else:
            j = prv()
    return False
```

**Complexity:** time **O(n)**, space **O(h)** — each iterator visits each node at most once; each stack holds ≤ h nodes.

---

## Edge cases

- Single node → false.
- k = 2·val for some val → false (same node).
- Negative values.
- Pair includes the root.

---

## Common mistakes

1. Pairing a node with itself (`k = 2·val`).
2. Continuing after the iterators cross (popping an empty stack).
3. Building the inorder array and calling it O(h) space.

---

## Follow-ups

1. Three-sum in a BST?
2. Count pairs instead of existence?
3. Two BSTs, one value from each (LC 1214)?

<details><summary>Answer sketches</summary>

**#1:** Fix each node (inorder), then two iterators on the rest: O(n²) time, O(h) space.

**#2:** Same two pointers; increment and advance both.

**#3:** Ascending iterator on one, descending on the other.
</details>

---

## Flashcards

**Two sum in BST in O(h) space?** #flashcard
Ascending + descending BST iterators as two pointers.

**Two-iterator stop condition?** #flashcard
Stop when `lo ≥ hi` (they've met).

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
