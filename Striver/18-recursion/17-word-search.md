---
module: striver/18-recursion
lesson: 17
topic: Word Search
difficulty: Medium
source: https://takeuforward.org/learning/dsa/word-search?category=faqs-hard&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, backtracking, matrix]
---
# 17. Word Search

← [Palindrome Partitioning](16-palindrome-partitioning.md) · [Part 18 index](README.md) · Next → [N-Queens](18-n-queens.md)

> [!abstract] Problem at a glance
> **Task:** Decide whether a word can be traced in a letter grid through 4-directionally adjacent cells, each used at most once.
> **Key insight:** DFS from every cell matching `word[0]`; at depth k the cell must equal `word[k]`. Mark the cell visited (overwrite with `#`) before exploring neighbours and restore it after — backtracking on the grid itself.
> **Difficulty:** Medium · **Pattern:** Grid DFS backtracking · **Also on:** [LC 79](https://leetcode.com/problems/word-search/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/word-search?category=faqs-hard&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. DFS with a visited matrix](#3-dfs-with-a-visited-matrix) · [4. DFS marking the board in place](#4-dfs-marking-the-board-in-place) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `m × n` grid of characters `board` and a string `word`, return `true` if `word` exists in the grid. The word is built from letters of sequentially adjacent cells (horizontally or vertically); the same cell may not be used more than once.

| Input | Output | Why |
|---|---|---|
| `board = [[A,B,C,E],[S,F,C,S],[A,D,E,E]], word = "ABCCED"` | `true` |  |
| `same board, word = "SEE"` | `true` |  |
| `same board, word = "ABCB"` | `false` | B would be reused |

**Constraints:** `1 ≤ m, n ≤ 6`, `1 ≤ |word| ≤ 15`, upper/lowercase letters.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| DFS with a visited matrix | separate boolean grid for used cells | O(m·n·3^L) | O(m·n) |
| DFS marking the board in place | board[r][c] = '#' during the visit, restore after | O(m·n·3^L) | O(L) recursion |

> [!tip] Interview angle
> Expect: in-place visited marking (no extra matrix), short-circuit on the first true, and a complexity of O(m · n · 3^L) (after the first step each cell has ≤ 3 unvisited neighbours). Bonus prunes: if the word has more of some letter than the board, return false; if the last letter is rarer than the first, search the reversed word.

---

## 3. DFS with a visited matrix

**Intuition.** Same search, but tracks visited cells in a separate `seen` grid. Works; the in-place version saves the O(m·n) memory.

```python
def exist_seen(board, word):
    m, n = len(board), len(board[0])
    seen = [[False] * n for _ in range(m)]
    def dfs(r, c, k):
        if k == len(word):
            return True
        if not (0 <= r < m and 0 <= c < n) or seen[r][c] or board[r][c] != word[k]:
            return False
        seen[r][c] = True
        ok = dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1) or dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1)
        seen[r][c] = False
        return ok
    return any(dfs(r, c, 0) for r in range(m) for c in range(n))
```

**Complexity:** time **O(m·n·3^L)**, space **O(m·n)**.

---

## 4. DFS marking the board in place

**Intuition.** `dfs(r, c, k)`: out of bounds or `board[r][c] != word[k]` → false; `k == L − 1` → true. Save the char, write `#`, try 4 neighbours with `||` short-circuit, restore, return.

**Algorithm**

1. For each cell: if `dfs(r, c, 0)` → true.
2. `dfs`: bounds / mismatch → false; last letter → true.
3. tmp = cell; cell = '#'; found = any neighbour dfs(k + 1); cell = tmp; return found.

**Dry run** — ABCCED: A(0,0) → B(0,1) → C(0,2) → C(1,2) → E(2,2) → D(2,1) ✓.

**C++**
```cpp
bool dfs(vector<vector<char>>& b, const string& w, int r, int c, int k) {
    if (r < 0 || c < 0 || r >= (int)b.size() || c >= (int)b[0].size() || b[r][c] != w[k]) return false;
    if (k == (int)w.size() - 1) return true;
    char tmp = b[r][c];
    b[r][c] = '#';
    bool found = dfs(b, w, r + 1, c, k + 1) || dfs(b, w, r - 1, c, k + 1) ||
                 dfs(b, w, r, c + 1, k + 1) || dfs(b, w, r, c - 1, k + 1);
    b[r][c] = tmp;
    return found;
}
bool exist(vector<vector<char>>& board, string word) {
    for (int r = 0; r < (int)board.size(); r++)
        for (int c = 0; c < (int)board[0].size(); c++)
            if (dfs(board, word, r, c, 0)) return true;
    return false;
}
```

**Java**
```java
static boolean dfs(char[][] b, String w, int r, int c, int k) {
    if (r < 0 || c < 0 || r >= b.length || c >= b[0].length || b[r][c] != w.charAt(k)) return false;
    if (k == w.length() - 1) return true;
    char tmp = b[r][c];
    b[r][c] = '#';
    boolean found = dfs(b, w, r + 1, c, k + 1) || dfs(b, w, r - 1, c, k + 1) ||
                    dfs(b, w, r, c + 1, k + 1) || dfs(b, w, r, c - 1, k + 1);
    b[r][c] = tmp;
    return found;
}
static boolean exist(char[][] board, String word) {
    for (int r = 0; r < board.length; r++)
        for (int c = 0; c < board[0].length; c++)
            if (dfs(board, word, r, c, 0)) return true;
    return false;
}
```

**Python**
```python
def exist(board, word):
    m, n = len(board), len(board[0])
    def dfs(r, c, k):
        if not (0 <= r < m and 0 <= c < n) or board[r][c] != word[k]:
            return False
        if k == len(word) - 1:
            return True
        tmp, board[r][c] = board[r][c], '#'
        found = dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1) or dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1)
        board[r][c] = tmp
        return found
    return any(dfs(r, c, 0) for r in range(m) for c in range(n))
```

**Complexity:** time **O(m·n·3^L)**, space **O(L) recursion** — m·n starts × ≤ 4·3^(L−1) paths each; depth L.

---

## Edge cases

- 1 × 1 board.
- Word longer than m · n → false.
- Word needs a cell twice ("aaa" on a 1 × 2 board).

---

## Common mistakes

1. Not restoring the cell — later starts see `#` and fail.
2. Checking `k == L` after the bounds check order is wrong, missing single-letter words.
3. Evaluating all 4 neighbours instead of short-circuiting.

---

## Follow-ups

1. Many words (Word Search II, LC 212).
2. Diagonal moves allowed.

<details><summary>Answer sketches</summary>

**#1:** Build a trie of the words; DFS once per cell walking the trie; prune finished branches.

**#2:** 8 directions; complexity base becomes 7.
</details>

---

## Flashcards

**Word Search visited trick?** #flashcard
Overwrite the cell with '#' before recursing, restore after.

**Word Search complexity?** #flashcard
O(m · n · 3^L).

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../coding/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../coding/algorithms/12-backtracking.md)
