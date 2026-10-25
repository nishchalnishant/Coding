---
module: striver-a2z/25-binary-search-trees
lesson: 7
topic: Kth Smallest and Largest element in BST
difficulty: Medium
source: https://takeuforward.org/learning/dsa/kth-smallest-and-largest-element-in-bst?category=medium&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search-trees, bst, inorder, kth]
---
# 7. Kth Smallest and Largest element in BST

← [Delete a node in BST](06-delete-node-in-bst.md) · [Part 25 index](README.md) · Next → [Check if a tree is a BST or not](08-validate-bst.md)

> [!abstract] Problem at a glance
> **Task:** Return `[kth smallest, kth largest]` (1-indexed).
> **Key insight:** Inorder visits a BST in ascending order, so the kth node popped is the kth smallest. Reverse inorder (R → Root → L) is descending, so the kth popped is the kth largest. Stop early: O(h + k), not O(n).
> **Difficulty:** Medium · **Pattern:** Inorder with early exit · **Also on:** [LC 230](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/kth-smallest-and-largest-element-in-bst?category=medium&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Full inorder list](#3-full-inorder-list) · [4. Iterative inorder, early stop](#4-iterative-inorder-early-stop) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given the `root` of a BST and `k` (`1 ≤ k ≤ n`), return the kth smallest and the kth largest values.

| Input | Output | Why |
|---|---|---|
| `root = [3,1,4,null,2], k = 1` | `[1,4]` | sorted 1 2 3 4 |
| `root = [5,3,6,2,4,null,null,1], k = 3` | `[3,4]` | sorted 1 2 3 4 5 6; 3rd from the end is 4 |

**Constraints:** `1 ≤ k ≤ n ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Full inorder list | collect sorted list, index | O(n) | O(n) |
| Iterative inorder, early stop | kth pop of inorder; kth pop of reverse inorder | O(h + k) | O(h) |

> [!tip] Interview angle
> The follow-up is 'what if the BST is modified often and you query kth repeatedly?' Augment each node with its subtree size; then kth is an O(h) walk. Kth largest also equals the (n − k + 1)th smallest, but that needs n first.

---

## 3. Full inorder list

**Intuition.** Build the full sorted array, then answer `a[k−1]` and `a[n−k]`.

```python
def kth_brute(root, k):
    a = []
    def go(n):
        if n:
            go(n.left); a.append(n.val); go(n.right)
    go(root)
    return [a[k - 1], a[len(a) - k]]
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Iterative inorder, early stop

**Intuition.** Run the iterative inorder template and count pops; return at the kth. For the largest, mirror every left/right.

**Algorithm**

1. Inorder: push the left spine; pop → `k1 -= 1`; if 0 → smallest found; go right.
2. Reverse: push the right spine; pop → `k2 -= 1`; if 0 → largest found; go left.
3. Return both.

**Dry run** — [5,3,8,2,4,7,9], k 3. Inorder pops 2, 3, 4 → 4. Reverse pops 9, 8, 7 → 7. → [4,7].

**C++**
```cpp
vector<int> kthSmallLarge(TreeNode* root, int k) {
    auto walk = [&](bool asc) {
        stack<TreeNode*> st; TreeNode* cur = root; int c = k;
        while (cur || !st.empty()) {
            while (cur) { st.push(cur); cur = asc ? cur->left : cur->right; }
            cur = st.top(); st.pop();
            if (--c == 0) return cur->val;
            cur = asc ? cur->right : cur->left;
        }
        return -1;
    };
    return {walk(true), walk(false)};
}
```

**Java**
```java
static int walkK(TreeNode root, int k, boolean asc) {
    Deque<TreeNode> st = new ArrayDeque<>(); TreeNode cur = root; int c = k;
    while (cur != null || !st.isEmpty()) {
        while (cur != null) { st.push(cur); cur = asc ? cur.left : cur.right; }
        cur = st.pop();
        if (--c == 0) return cur.val;
        cur = asc ? cur.right : cur.left;
    }
    return -1;
}
static int[] kthSmallLarge(TreeNode root, int k) {
    return new int[]{walkK(root, k, true), walkK(root, k, false)};
}
```

**Python**
```python
def kth(root, k):
    def walk(first, second):
        st, cur, c = [], root, k
        while cur or st:
            while cur:
                st.append(cur)
                cur = getattr(cur, first)
            cur = st.pop()
            c -= 1
            if c == 0:
                return cur.val
            cur = getattr(cur, second)
        return -1
    return [walk("left", "right"), walk("right", "left")]
```

**Complexity:** time **O(h + k)**, space **O(h)** — the walk descends one spine (h) and then pops k nodes.

---

## Edge cases

- k = 1 → min / max.
- k = n → smallest and largest swap roles.
- Skewed tree → stack depth n.

---

## Common mistakes

1. Using a global counter in recursion without stopping the remaining calls (still O(n)).
2. Off-by-one: kth largest is index `n − k`, not `n − k − 1`.
3. Recursive counter passed by value in C++/Java, so it never decrements in the caller.

---

## Follow-ups

1. Frequent inserts/deletes + kth queries?
2. O(1) space?
3. Kth smallest in a sorted matrix / two arrays?

<details><summary>Answer sketches</summary>

**#1:** Store `size` in each node: if `k ≤ size(left)` go left; if `k == size(left)+1` return; else `k -= size(left)+1`, go right.

**#2:** Morris inorder, counting visits.

**#3:** Different structure: heap or binary search on the value.
</details>

---

## Flashcards

**Kth smallest in BST: technique and cost?** #flashcard
Iterative inorder, stop at the kth pop: O(h + k) time, O(h) space.

**Kth largest in BST?** #flashcard
Reverse inorder (right first), kth pop.

**Order-statistic BST?** #flashcard
Each node stores its subtree size → kth in O(h).

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
