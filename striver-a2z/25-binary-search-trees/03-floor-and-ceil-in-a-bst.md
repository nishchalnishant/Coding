---
module: striver-a2z/25-binary-search-trees
lesson: 3
topic: Floor and Ceil in a BST
difficulty: Medium
source: https://takeuforward.org/learning/dsa/floor-and-ceil-in-a-bst?category=theory-and-basics&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search-trees, bst, floor-ceil, lower-bound]
---
# 3. Floor and Ceil in a BST

← [Search in BST](02-search-in-bst.md) · [Part 25 index](README.md) · Next → [Minimum and Maximum in BST](04-minimum-and-maximum-in-bst.md)

> [!abstract] Problem at a glance
> **Task:** Return `[floor, ceil]` of `key`: the largest value ≤ key and the smallest value ≥ key (−1 if none).
> **Key insight:** Walk as if searching for `key`. Each time you step **right**, the current node is ≤ key, so it's a floor candidate, and later candidates are only larger. Each time you step **left**, the node is ≥ key and becomes a ceil candidate. The last candidate recorded is the answer.
> **Difficulty:** Medium · **Pattern:** BST walk + candidate tracking · **Also on:** [GfG Floor in BST](https://www.geeksforgeeks.org/problems/floor-in-bst/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/floor-and-ceil-in-a-bst?category=theory-and-basics&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Inorder + scan](#3-inorder--scan) · [4. Single walk per side](#4-single-walk-per-side) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a BST and an integer `key`, find the floor (greatest value `≤ key`) and the ceil (smallest value `≥ key`). Return `-1` for a missing side.

| Input | Output | Why |
|---|---|---|
| `root = [5,3,8,2,4,7,9], key = 6` | `[5,7]` | 6 not present: 5 is the largest below, 7 the smallest above |
| `root = [5,3,8,2,4,7,9], key = 1` | `[-1,2]` | nothing ≤ 1 |

**Constraints:** `1 ≤ n ≤ 10⁵`; values distinct.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Inorder + scan | sorted list, then linear/binary search | O(n) | O(n) |
| Single walk per side | right-step → floor candidate; left-step → ceil candidate | O(h) | O(1) |

> [!tip] Interview angle
> It's the BST version of lower/upper bound. Say that out loud. `TreeMap.floorKey`/`ceilingKey` and `std::set::lower_bound` do the same walk on a balanced tree.

---

## 3. Inorder + scan

**Intuition.** Inorder gives the sorted values. Floor is the last value ≤ key and ceil the first value ≥ key. This ignores the tree's shape, so it's O(n).

```python
def floor_ceil_brute(root, key):
    vals = []
    def go(n):
        if n:
            go(n.left); vals.append(n.val); go(n.right)
    go(root)
    fl = max((v for v in vals if v <= key), default=-1)
    ce = min((v for v in vals if v >= key), default=-1)
    return [fl, ce]
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Single walk per side

**Intuition.** For floor: if `cur.val == key` it's exact. If `cur.val < key`, record it and go right to look for a larger one that's still ≤ key. Otherwise go left. Ceil mirrors this.

**Algorithm**

1. `fl = -1`, `cur = root`. While `cur`: equal → `fl = key`, stop; `cur.val < key` → `fl = cur.val`, go right; else go left.
2. `ce = -1`, `cur = root`. While `cur`: equal → `ce = key`, stop; `cur.val > key` → `ce = cur.val`, go left; else go right.
3. Return `[fl, ce]`.

**Dry run** — [5,3,8,2,4,7,9], key 6. Floor: 5 < 6 → fl 5, right 8; 8 > 6 → left 7; 7 > 6 → left null. fl = 5. Ceil: 5 < 6 → right 8; 8 > 6 → ce 8, left 7; 7 > 6 → ce 7, left null. → [5,7].

**C++**
```cpp
vector<int> floorCeil(TreeNode* root, int key) {
    int fl = -1, ce = -1;
    for (TreeNode* cur = root; cur; ) {
        if (cur->val == key) { fl = key; break; }
        if (cur->val < key) { fl = cur->val; cur = cur->right; }
        else cur = cur->left;
    }
    for (TreeNode* cur = root; cur; ) {
        if (cur->val == key) { ce = key; break; }
        if (cur->val > key) { ce = cur->val; cur = cur->left; }
        else cur = cur->right;
    }
    return {fl, ce};
}
```

**Java**
```java
static int[] floorCeil(TreeNode root, int key) {
    int fl = -1, ce = -1;
    for (TreeNode cur = root; cur != null; ) {
        if (cur.val == key) { fl = key; break; }
        if (cur.val < key) { fl = cur.val; cur = cur.right; }
        else cur = cur.left;
    }
    for (TreeNode cur = root; cur != null; ) {
        if (cur.val == key) { ce = key; break; }
        if (cur.val > key) { ce = cur.val; cur = cur.left; }
        else cur = cur.right;
    }
    return new int[]{fl, ce};
}
```

**Python**
```python
def floor_ceil(root, key):
    fl, cur = -1, root
    while cur:
        if cur.val == key:
            fl = key
            break
        if cur.val < key:
            fl, cur = cur.val, cur.right
        else:
            cur = cur.left
    ce, cur = -1, root
    while cur:
        if cur.val == key:
            ce = key
            break
        if cur.val > key:
            ce, cur = cur.val, cur.left
        else:
            cur = cur.right
    return [fl, ce]
```

**Complexity:** time **O(h)**, space **O(1)** — each walk is one root-to-leaf path.

---

## Edge cases

- Key present → floor = ceil = key.
- Key below the minimum → floor −1.
- Key above the maximum → ceil −1.

---

## Common mistakes

1. Recording the candidate on the wrong turn (floor is recorded when moving **right**).
2. Stopping at the first candidate instead of continuing to refine it.
3. Using −1 as a sentinel when −1 is a legal value; use null/Optional in real code.

---

## Follow-ups

1. Strictly less / strictly greater?
2. k closest values?
3. Both in one walk?

<details><summary>Answer sketches</summary>

**#1:** Drop the equality early-exit; use `<` for floor and `>` for ceil. That's the inorder predecessor/successor.

**#2:** Inorder with a deque of size k, or two stacks (predecessors, successors) merged.

**#3:** Possible: update both on each step, but two walks are clearer and the same O(h).
</details>

---

## Flashcards

**Floor in BST: when do you record a candidate?** #flashcard
When `cur.val < key` (then move right to look for a larger one ≤ key).

**Ceil in BST: when do you record a candidate?** #flashcard
When `cur.val > key` (then move left).

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
