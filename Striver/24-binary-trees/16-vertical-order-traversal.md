---
module: striver/24-binary-trees
lesson: 16
topic: Vertical Order Traversal
difficulty: Hard
source: https://takeuforward.org/learning/dsa/vertical-order-traversal?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-trees, binary-tree, dfs, sorting, hashing, hard]
---
# 16. Vertical Order Traversal

← [Boundary Traversal of a Binary Tree](15-boundary-traversal.md) · [Part 24 index](README.md) · Next → [Top View of Binary Tree](17-top-view.md)

> [!abstract] Problem at a glance
> **Task:** Group nodes by column (root col 0, left −1, right +1), columns left→right; within a column sort by row, then by value.
> **Key insight:** Label each node with `(col, row)` during any traversal, then **sort by (col, row, val)** and group by col. The tie-breaking rule (same row and column → smaller value first) is what makes it 'Hard'. BFS alone doesn't give it.
> **Difficulty:** Hard · **Pattern:** Coordinate labelling + sort · **Also on:** [LC 987](https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/vertical-order-traversal?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Nested ordered maps](#3-nested-ordered-maps) · [4. Collect triples + one sort](#4-collect-triples--one-sort) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

For each node at `(row, col)`, its left child is at `(row+1, col−1)` and its right child at `(row+1, col+1)`. The root is at `(0, 0)`. Return the vertical order traversal: one list per column from leftmost to rightmost. Within a column, order nodes top to bottom; nodes in the same row and column are sorted by value.

| Input | Output | Why |
|---|---|---|
| `root = [3,9,20,null,null,15,7]` | `[[9],[3,15],[20],[7]]` |  |
| `root = [1,2,3,4,6,5,7]` | `[[4],[2],[1,5,6],[3],[7]]` | 5 and 6 share (2, 0) → sorted 5, 6 |

**Constraints:** `1 ≤ n ≤ 1000`; `0 ≤ val ≤ 1000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Nested ordered maps | map col → map row → multiset vals | O(n log n) | O(n) |
| Collect triples + one sort | (col, row, val) for every node, sort, group by col | O(n log n) | O(n) |

> [!tip] Interview angle
> Ask about the tie rule first. LC 314 (premium) keeps BFS order for ties, and LC 987 sorts by value, so the answer depends on it. Striver's version uses `map<col, map<row, multiset>>`, which is equivalent to sorting triples. Top and bottom view are this problem with only the first or last node per column.

---

## 3. Nested ordered maps

**Intuition.** Ordered maps keep columns and rows sorted. A multiset (here a sorted list) breaks ties by value.

```python
from collections import defaultdict

def vertical_maps(root):
    cols = defaultdict(lambda: defaultdict(list))
    st = [(root, 0, 0)] if root else []
    while st:
        n, r, c = st.pop()
        cols[c][r].append(n.val)
        if n.left:
            st.append((n.left, r + 1, c - 1))
        if n.right:
            st.append((n.right, r + 1, c + 1))
    return [[v for r in sorted(cols[c]) for v in sorted(cols[c][r])] for c in sorted(cols)]
```

**Complexity:** time **O(n log n)**, space **O(n)**.

---

## 4. Collect triples + one sort

**Intuition.** One flat list and one sort. It's the least code and the easiest to get right in every language.

**Algorithm**

1. DFS from `(root, row 0, col 0)` appending `(col, row, val)`.
2. Sort the triples lexicographically.
3. Walk them; start a new group whenever `col` changes.

**Dry run** — [1,2,3,4,6,5,7]: triples (−2,2,4) (−1,1,2) (0,0,1) (0,2,5) (0,2,6) (1,1,3) (2,2,7) → [[4],[2],[1,5,6],[3],[7]].

**C++**
```cpp
void vtGo(TreeNode* n, int r, int c, vector<array<int, 3>>& t) {
    if (!n) return;
    t.push_back({c, r, n->val});
    vtGo(n->left, r + 1, c - 1, t);
    vtGo(n->right, r + 1, c + 1, t);
}
vector<vector<int>> verticalTraversal(TreeNode* root) {
    vector<array<int, 3>> t;
    vtGo(root, 0, 0, t);
    sort(t.begin(), t.end());
    vector<vector<int>> res;
    for (size_t i = 0; i < t.size(); i++) {
        if (i == 0 || t[i][0] != t[i - 1][0]) res.push_back({});
        res.back().push_back(t[i][2]);
    }
    return res;
}
```

**Java**
```java
static void vtGo(TreeNode n, int r, int c, List<int[]> t) {
    if (n == null) return;
    t.add(new int[]{c, r, n.val});
    vtGo(n.left, r + 1, c - 1, t);
    vtGo(n.right, r + 1, c + 1, t);
}
static List<List<Integer>> verticalTraversal(TreeNode root) {
    List<int[]> t = new ArrayList<>();
    vtGo(root, 0, 0, t);
    t.sort((a, b) -> a[0] != b[0] ? a[0] - b[0] : a[1] != b[1] ? a[1] - b[1] : a[2] - b[2]);
    List<List<Integer>> res = new ArrayList<>();
    for (int i = 0; i < t.size(); i++) {
        if (i == 0 || t.get(i)[0] != t.get(i - 1)[0]) res.add(new ArrayList<>());
        res.get(res.size() - 1).add(t.get(i)[2]);
    }
    return res;
}
```

**Python**
```python
def vertical(root):
    trip = []
    def go(n, r, c):
        if not n:
            return
        trip.append((c, r, n.val))
        go(n.left, r + 1, c - 1)
        go(n.right, r + 1, c + 1)
    go(root, 0, 0)
    trip.sort()
    res, last = [], None
    for c, _, v in trip:
        if c != last:
            res.append([])
            last = c
        res[-1].append(v)
    return res
```

**Complexity:** time **O(n log n)**, space **O(n)** — O(n) labelling plus an O(n log n) sort.

---

## Edge cases

- Two nodes with the same (row, col): sort by value.
- Same column, different rows: higher row (smaller index) first.
- Single node.

---

## Common mistakes

1. Using BFS order for ties (that's LC 314, not 987).
2. Sorting by (col, val) and ignoring row.
3. Using a hash map for columns and forgetting to sort the keys.

---

## Follow-ups

1. O(n) without sorting columns?
2. Top / bottom view?

<details><summary>Answer sketches</summary>

**#1:** Track min/max col, bucket into an array of size (max−min+1); still sort within a cell.

**#2:** Keep only the first / last node per column in BFS order.
</details>

---

## Flashcards

**Vertical order (LC 987) sort key?** #flashcard
(col, row, val).

**Child coordinates?** #flashcard
left (r+1, c−1), right (r+1, c+1).

**Interview track →** [Tree deep-dive](../../01-data-structures/08-tree.md)
