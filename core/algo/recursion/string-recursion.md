# String Recursion — Parsing, Matching & Manipulation

String problems solved recursively: pattern matching, expression evaluation, string transformation and generation. For the recursion foundation see [README.md](README.md).

---

## Part 1 — Pattern Matching (Memoized)

### 1.1 Regular Expression Matching (LC 10)

**Pattern:** `.` matches any single char. `*` matches zero or more of preceding char.

**State:** `dp(i, j)` = does `s[i:]` match `p[j:]`?

```python
from functools import lru_cache

def is_match_regex(s: str, p: str) -> bool:
    @lru_cache(maxsize=None)
    def dp(i: int, j: int) -> bool:
        if j == len(p): return i == len(s)   # pattern exhausted

        first_match = i < len(s) and (p[j] == '.' or p[j] == s[i])

        if j + 1 < len(p) and p[j+1] == '*':
            return (dp(i, j+2)                    # use '*' as zero occurrences
                    or (first_match and dp(i+1, j)))  # use '*' as one+ occurrence
        else:
            return first_match and dp(i+1, j+1)

    return dp(0, 0)
```

> [!CAUTION]
> `*` means "zero or more of the PRECEDING character" — not a wildcard on its own. Always look at `p[j+1]` when deciding whether `p[j]` can repeat. The "zero occurrence" case (`dp(i, j+2)`) is what makes this tricky — it skips both `p[j]` AND the `*`.

---

### 1.2 Wildcard Matching (LC 44)

**Pattern:** `?` matches any single char. `*` matches any sequence (including empty).

```python
from functools import lru_cache

def is_match_wildcard(s: str, p: str) -> bool:
    @lru_cache(maxsize=None)
    def dp(i: int, j: int) -> bool:
        if j == len(p): return i == len(s)
        if i == len(s): return all(c == '*' for c in p[j:])   # remaining pattern all '*'?

        if p[j] == '*':
            return dp(i+1, j) or dp(i, j+1)   # consume s[i] | advance pattern past '*'
        elif p[j] == '?' or p[j] == s[i]:
            return dp(i+1, j+1)
        return False

    return dp(0, 0)
```

> [!TIP]
> **Regex vs Wildcard differences:**
> - Regex `*`: requires a preceding character to repeat; check `p[j+1]`
> - Wildcard `*`: standalone; matches any sequence; `dp(i+1, j)` consumes one char from s, `dp(i, j+1)` treats `*` as empty

---

## Part 2 — Expression Evaluation

### 2.1 Expression Add Operators (LC 282)

**Problem:** Add `+`, `-`, or `*` between digits of a string to make it equal target. Return all valid expressions.

```python
def add_operators(num: str, target: int) -> list[str]:
    result = []

    def backtrack(index: int, path: str, value: int, prev: int) -> None:
        if index == len(num):
            if value == target:
                result.append(path)
            return
        for i in range(index, len(num)):
            curr_str = num[index:i+1]
            if len(curr_str) > 1 and curr_str[0] == '0':
                break              # no leading zeros (break, not continue)
            curr = int(curr_str)
            if index == 0:
                backtrack(i+1, curr_str, curr, curr)   # first number, no operator
            else:
                backtrack(i+1, path+'+'+curr_str, value+curr, curr)
                backtrack(i+1, path+'-'+curr_str, value-curr, -curr)
                # Multiplication: undo prev contribution, apply new product
                backtrack(i+1, path+'*'+curr_str, value - prev + prev*curr, prev*curr)

    backtrack(0, '', 0, 0)
    return result
```

> [!IMPORTANT]
> **Multiplication tracking:** `prev` stores the last operand. For `*`, undo `prev`'s contribution with `value - prev`, then add `prev * curr`. This handles left-to-right multiplication precedence without a stack.

---

### 2.2 Decode String (LC 394)

**Problem:** Decode `k[encoded_string]` format recursively. E.g. `"3[a2[c]]"` → `"accaccacc"`.

```python
def decode_string(s: str) -> str:
    def decode(i: int) -> tuple[str, int]:
        result = []
        while i < len(s) and s[i] != ']':
            if s[i].isdigit():
                k = 0
                while i < len(s) and s[i].isdigit():
                    k = k * 10 + int(s[i])
                    i += 1
                i += 1              # skip '['
                inner, i = decode(i)
                i += 1              # skip ']'
                result.append(inner * k)
            else:
                result.append(s[i])
                i += 1
        return ''.join(result), i

    return decode(0)[0]
```

> [!TIP]
> Recursion handles nested brackets naturally — each `[` triggers a recursive call, and `]` is the base-case return signal. Pass and return the index `i` to maintain position across the call stack.

---

### 2.3 Basic Calculator (Recursive Descent) (LC 224)

**Problem:** Evaluate expression with `+`, `-`, `(`, `)`.

```python
def calculate(s: str) -> int:
    i = [0]   # mutable index shared across calls

    def expr() -> int:
        result = 0
        sign = 1
        while i[0] < len(s):
            c = s[i[0]]
            if c.isdigit():
                num = 0
                while i[0] < len(s) and s[i[0]].isdigit():
                    num = num * 10 + int(s[i[0]])
                    i[0] += 1
                result += sign * num
            elif c == '+':
                sign = 1;  i[0] += 1
            elif c == '-':
                sign = -1; i[0] += 1
            elif c == '(':
                i[0] += 1          # skip '('
                result += sign * expr()
            elif c == ')':
                i[0] += 1          # skip ')'
                return result
            elif c == ' ':
                i[0] += 1
        return result

    return expr()
```

---

## Part 3 — String Generation & Transformation

### 3.1 Remove Invalid Parentheses (LC 301)

**Problem:** Remove minimum invalid parentheses to make the string valid. Return all valid results.

```python
def remove_invalid_parentheses(s: str) -> list[str]:
    result = set()

    # Count minimum removals needed
    open_rem = close_rem = 0
    for c in s:
        if c == '(':
            open_rem += 1
        elif c == ')':
            if open_rem > 0: open_rem -= 1
            else: close_rem += 1

    def is_valid(t: str) -> bool:
        count = 0
        for c in t:
            if c == '(': count += 1
            elif c == ')':
                count -= 1
                if count < 0: return False
        return count == 0

    def backtrack(index: int, left_rem: int, right_rem: int,
                  left_count: int, right_count: int, current: list) -> None:
        if index == len(s):
            if left_rem == 0 and right_rem == 0:
                candidate = ''.join(current)
                if is_valid(candidate):
                    result.add(candidate)
            return
        ch = s[index]
        # Remove current char (if it's a parenthesis and we still have removals left)
        if ch == '(' and left_rem > 0:
            backtrack(index+1, left_rem-1, right_rem, left_count, right_count, current)
        if ch == ')' and right_rem > 0:
            backtrack(index+1, left_rem, right_rem-1, left_count, right_count, current)
        # Keep current char
        current.append(ch)
        if ch == '(':
            backtrack(index+1, left_rem, right_rem, left_count+1, right_count, current)
        elif ch == ')' and left_count > right_count:
            backtrack(index+1, left_rem, right_rem, left_count, right_count+1, current)
        else:
            backtrack(index+1, left_rem, right_rem, left_count, right_count, current)
        current.pop()

    backtrack(0, open_rem, close_rem, 0, 0, [])
    return list(result)
```

---

### 3.2 Generate All Palindromic Partitions (LC 131)

**Problem:** Partition string `s` such that every substring is a palindrome. Return all such partitions.

```python
def partition(s: str) -> list[list[str]]:
    result = []

    def is_palindrome(sub: str) -> bool:
        return sub == sub[::-1]

    def backtrack(start: int, current: list[str]) -> None:
        if start == len(s):
            result.append(current[:])
            return
        for end in range(start + 1, len(s) + 1):
            sub = s[start:end]
            if is_palindrome(sub):
                current.append(sub)
                backtrack(end, current)
                current.pop()

    backtrack(0, [])
    return result
```

> [!TIP]
> Precompute the palindrome table `is_pal[i][j]` for O(1) lookup instead of `O(N)` per check — reduces overall complexity from `O(N × 2^N)` to `O(2^N)`.

---

### 3.3 Word Search (LC 79)

**Problem:** Find if word exists in 2D board by traversing adjacent cells (no cell reused).

```python
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int, k: int) -> bool:
        if k == len(word): return True
        if not (0 <= r < rows and 0 <= c < cols): return False
        if board[r][c] != word[k]: return False

        temp, board[r][c] = board[r][c], '#'   # mark visited
        found = any(dfs(r+dr, c+dc, k+1)
                    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)])
        board[r][c] = temp                      # restore
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
```

---

### 3.4 Scramble String (LC 87)

**Problem:** Can `s1` be scrambled to produce `s2` by recursively splitting and swapping?

```python
from functools import lru_cache

def is_scramble(s1: str, s2: str) -> bool:
    @lru_cache(maxsize=None)
    def dp(a: str, b: str) -> bool:
        if a == b: return True
        if sorted(a) != sorted(b): return False   # character count mismatch
        n = len(a)
        for i in range(1, n):
            # No swap: a[:i] ↔ b[:i], a[i:] ↔ b[i:]
            if dp(a[:i], b[:i]) and dp(a[i:], b[i:]):
                return True
            # Swap: a[:i] ↔ b[n-i:], a[i:] ↔ b[:n-i]
            if dp(a[:i], b[n-i:]) and dp(a[i:], b[:n-i]):
                return True
        return False

    return dp(s1, s2)
```

> [!TIP]
> **Early termination:** `sorted(a) != sorted(b)` quickly eliminates strings with different character counts — they can't be scrambles. This prunes most branches in practice.

---

## Part 4 — String Manipulation Recursion

### 4.1 Reverse String Recursively

```python
def reverse_string(s: list[str]) -> None:
    def swap(lo: int, hi: int) -> None:
        if lo >= hi: return
        s[lo], s[hi] = s[hi], s[lo]
        swap(lo + 1, hi - 1)
    swap(0, len(s) - 1)
```

### 4.2 Check Palindrome Recursively

```python
def is_palindrome(s: str, lo: int = 0, hi: int = None) -> bool:
    if hi is None: hi = len(s) - 1
    if lo >= hi: return True
    if s[lo] != s[hi]: return False
    return is_palindrome(s, lo + 1, hi - 1)
```

### 4.3 Recursively Print All Subsequences

```python
def all_subsequences(s: str, i: int = 0, current: str = '') -> None:
    if i == len(s):
        print(current or '(empty)')
        return
    all_subsequences(s, i+1, current + s[i])   # include s[i]
    all_subsequences(s, i+1, current)           # exclude s[i]
```

---

## Interview Questions — Logic & Trickiness

| Problem | LC # | Pattern | Click Moment | Gotcha |
| :--- | :--- | :--- | :--- | :--- |
| **Regular Expression** | 10 | Memoized recursion | `*` = zero-or-more of PRECEDING; check `p[j+1]` | Zero-occurrence case: `dp(i, j+2)` |
| **Wildcard Matching** | 44 | Memoized recursion | `*` standalone matches any sequence | `dp(i+1,j)`: consume s[i]; `dp(i,j+1)`: `*` empty |
| **Expression Add Operators** | 282 | Backtracking | Track `prev` for multiplication undo | Leading zeros: break (not continue) after detecting |
| **Decode String** | 394 | Recursive descent | `[` triggers recursion; `]` is base case return | Pass and return index `i` across calls |
| **Basic Calculator** | 224 | Recursive descent | `(` triggers recursive call; `)` returns | Use mutable index `i=[0]` for shared state |
| **Remove Invalid Parentheses** | 301 | Backtracking + counting | Count min open/close to remove first | Use set to deduplicate results |
| **Palindrome Partitioning** | 131 | Backtracking | Try all split points; add if palindrome | Precompute `is_pal[i][j]` for O(1) check |
| **Word Search** | 79 | DFS backtracking | Mark cell `'#'`; restore after recursion | Restore even on failure — don't skip restore |
| **Scramble String** | 87 | Memoized divide & conquer | Try all split points; swap and no-swap variants | `sorted(a)!=sorted(b)` early pruning |

---

## See also

- [README.md](README.md) — Memoized recursion pattern
- [aditya-verma.md](aditya-verma.md) — IP/OP string building (Pattern 3)
- [combination-problems.md](combination-problems.md) — Backtracking on arrays
- [questions-bank.md](questions-bank.md) — String recursion drill problems
