---
tags: [coding, algorithms, backtracking]
topic: Backtracking
difficulty: mixed
---

# Backtracking — Problem Compendium

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop.
> `🎯 T2` — **TIER 2 · Build Fluidity**: This file is core Tier 2 material. Know patterns cold; skip niche edge cases.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Conceptual awareness only.


Backtracking is DFS over choices: pick something, go deeper, undo if it doesn't work. You explore every valid path unless you can prune early. The easy bug is forgetting to undo — always pop/unmark after the recursive call.

Prune when: the partial answer is already invalid, not enough room left to finish, or you'd repeat the same choice at the same depth (sort + skip duplicates).




---

## Subsets / Combinations

### Subsets (Power Set) `🎯 T2`

> [!example] Problem
> Given an integer array nums of unique elements, return all possible subsets (the power set).
> The solution set must not contain duplicate subsets. Return the solution in any order.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,3]
> Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0]
> Output: [[],[0]]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10
> - -10 <= nums[i] <= 10
> - All the numbers of nums are unique.

> [!info] Approach
> Every element has a binary choice — include or exclude. Tree depth = n, branching factor = 2, total leaves = 2^n. No pruning needed — every branch is valid. The `start` parameter enforces non-decreasing index selection, eliminating permutation variants of the same subset. At each recursive call, record the current path. Try adding each element from `start` onward; recurse with `start = i+1`; undo. Record subset at every node (not just leaves) — each partial path is itself a valid subset.

> [!note]- Python Solution
> ```python
> def subsets(nums):
>     result = []
>     path = []
> 
>     def backtrack(start):
>         result.append(path[:])  # save current path (not just at leaves)
>         for i in range(start, len(nums)):
>             path.append(nums[i])
>             backtrack(i + 1)
>             path.pop()
> 
>     backtrack(0)
>     return result
> ```

> [!success] Complexity
> O(n · 2^n) time (copy at each of 2^n nodes), O(n) recursion depth.

> [!tip] Alternatives
> Bitmask: for k in range(2^n), bits indicate inclusion — O(n · 2^n), no recursion. Iterative cascade: start with `[[]]`, extend by each new element — O(n · 2^n), simple.

---

### Subsets II (with duplicates) `🎯 T2`

> [!example] Problem
> Given an integer array nums that may contain duplicates, return all possible subsets (the power set).
> The solution set must not contain duplicate subsets. Return the solution in any order.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,2]
> Output: [[],[1],[1,2],[1,2,2],[2],[2,2]]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0]
> Output: [[],[0]]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10
> - -10 <= nums[i] <= 10

> [!info] Approach
> Duplicates produce identical subsets when same-valued elements are included at the same decision level. Sort to group duplicates together; skip `nums[i]` if `i > start and nums[i] == nums[i-1]`. The `i > start` (not `i > 0`) condition is critical: it only skips duplicates at the current level, not when the first copy was used at a parent level. Sort array; apply deduplication skip in backtracking loop. Same structure as Subsets but with `if i > start and nums[i] == nums[i-1]: continue`.

> [!note]- Python Solution
> ```python
> def subsets_with_dup(nums):
>     nums.sort()
>     result = []
>     path = []
> 
>     def backtrack(start):
>         result.append(path[:])
>         for i in range(start, len(nums)):
>             if i > start and nums[i] == nums[i - 1]:
>                 continue  # same value already tried at this depth
>             path.append(nums[i])
>             backtrack(i + 1)
>             path.pop()
> 
>     backtrack(0)
>     return result
> ```

> [!success] Complexity
> O(n · 2^n) worst case (all distinct), O(n) space.

> [!tip] Alternatives
> Set deduplication post-hoc — generates duplicates then discards; wasteful. Counter-based: iterate over how many copies of each unique value to include.

---

### Combination Sum (unbounded) `🎯 T2`

> [!example] Problem
> Given an array of distinct integers candidates and a target integer target, return a list of all unique combinations of candidates where the chosen numbers sum to target. You may return the combinations in any order.
> The same number may be chosen from candidates an unlimited number of times. Two combinations are unique if the frequency of at least one of the chosen numbers is different.
> The test cases are generated such that the number of unique combinations that sum up to target is less than 150 combinations for the given input.
> 
> **Example 1:**
> ```
> Input: candidates = [2,3,6,7], target = 7
> Output: [[2,2,3],[7]]
> Explanation:
> 2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times.
> 7 is a candidate, and 7 = 7.
> These are the only two combinations.
> ```
> 
> **Example 2:**
> ```
> Input: candidates = [2,3,5], target = 8
> Output: [[2,2,2,2],[2,3,3],[3,5]]
> ```
> 
> **Example 3:**
> ```
> Input: candidates = [2], target = 1
> Output: []
> ```
> 
> **Constraints:**
> - 1 <= candidates.length <= 30
> - 2 <= candidates[i] <= 40
> - All elements of candidates are distinct.
> - 1 <= target <= 40

> [!info] Approach
> Elements can be reused, but combinations (not permutations) are needed. Using `start = i` (not `i+1`) in the recursive call allows re-selecting the same element. The `start` parameter enforces non-decreasing order, so `[2,3]` and `[3,2]` are treated as the same combination. At each step, try candidates from `start` onward. Prune when `candidate > remaining`. Record when `remaining == 0`. Recurse with `backtrack(i, remaining - candidates[i])` — same `i`, not `i+1`.

> [!note]- Python Solution
> ```python
> def combination_sum(candidates, target):
>     result = []
>     path = []
> 
>     def backtrack(start, remaining):
>         if remaining == 0:
>             result.append(path[:])
>             return
>         for i in range(start, len(candidates)):
>             if candidates[i] > remaining:
>                 continue
>             path.append(candidates[i])
>             backtrack(i, remaining - candidates[i])  # stay on i — candidate can be picked again
>             path.pop()
> 
>     backtrack(0, target)
>     return result
> ```

> [!success] Complexity
> O(n^(T/M)) where T = target, M = min candidate; O(T/M) recursion depth.

> [!tip] Alternatives
> Sort candidates + replace `continue` with `break` (early exit). DP for count only: O(n · target). BFS: memory-intensive.

---

### Combination Sum II (0/1 — no reuse) `🎯 T2`

> [!example] Problem
> Given a collection of candidate numbers (candidates) and a target number (target), find all unique combinations in candidates where the candidate numbers sum to target.
> Each number in candidates may only be used once in the combination.
> Note: The solution set must not contain duplicate combinations.
> 
> **Example 1:**
> ```
> Input: candidates = [10,1,2,7,6,1,5], target = 8
> Output: 
> [
> [1,1,6],
> [1,2,5],
> [1,7],
> [2,6]
> ]
> ```
> 
> **Example 2:**
> ```
> Input: candidates = [2,5,2,1,2], target = 5
> Output: 
> [
> [1,2,2],
> [5]
> ]
> ```
> 
> **Constraints:**
> - 1 <= candidates.length <= 100
> - 1 <= candidates[i] <= 50
> - 1 <= target <= 30

> [!info] Approach
> No reuse → recurse with `i+1`. Duplicates need the same skip pattern as Subsets II: `i > start and candidates[i] == candidates[i-1]`. Sort enables both early termination (break when candidate > remaining) and deduplication. Sort; backtrack with `i+1`; skip duplicates at same level; break early. `if i > start and candidates[i] == candidates[i-1]: continue`.

> [!note]- Python Solution
> ```python
> def combination_sum2(candidates, target):
>     candidates.sort()
>     result = []
>     path = []
> 
>     def backtrack(start, remaining):
>         if remaining == 0:
>             result.append(path[:])
>             return
>         for i in range(start, len(candidates)):
>             if candidates[i] > remaining:
>                 break  # sorted: no later candidate can work
>             if i > start and candidates[i] == candidates[i - 1]:
>                 continue
>             path.append(candidates[i])
>             backtrack(i + 1, remaining - candidates[i])
>             path.pop()
> 
>     backtrack(0, target)
>     return result
> ```

> [!success] Complexity
> O(2^n) worst case; O(n) space.

> [!tip] Alternatives
> Counter-based deduplication: group by unique value, try 0..count copies. Avoids sort-based skip logic.

---

### Combinations `🎯 T2`

> [!example] Problem
> Given two integers n and k, return all possible combinations of k numbers chosen from the range [1, n].
> You may return the answer in any order.
> 
> **Example 1:**
> ```
> Input: n = 4, k = 2
> Output: [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
> Explanation: There are 4 choose 2 = 6 total combinations.
> Note that combinations are unordered, i.e., [1,2] and [2,1] are considered to be the same combination.
> ```
> 
> **Example 2:**
> ```
> Input: n = 1, k = 1
> Output: [[1]]
> Explanation: There is 1 choose 1 = 1 total combination.
> ```
> 
> **Constraints:**
> - 1 <= n <= 20
> - 1 <= k <= n

> [!info] Approach
> Fixed-size subset problem. At each level, choose one number from `start` to `n`; recurse with `start+1`. Prune when remaining slots can't be filled: `n - i + 1 < k - len(path)`. Standard subset backtracking with fixed depth k and pruning on remaining elements. Pruning: `if n - i + 1 < k - len(path): break` — not enough numbers remain.

> [!note]- Python Solution
> ```python
> def combine(n, k):
>     result = []
>     path = []
> 
>     def backtrack(start):
>         if len(path) == k:
>             result.append(path[:])
>             return
>         for i in range(start, n + 1):
>             if n - i + 1 < k - len(path):
>                 break  # not enough numbers left
>             path.append(i)
>             backtrack(i + 1)
>             path.pop()
> 
>     backtrack(1)
>     return result
> ```

> [!success] Complexity
> O(C(n,k) · k) time; O(k) recursion depth.

> [!tip] Alternatives
> Bitmask over n bits: try all subsets of size k — O(2^n), impractical for large n. Itertools.combinations in production code.

---

### Letter Combinations of a Phone Number `🎯 T2`

> [!example] Problem
> Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent. Return the answer in any order.
> A mapping of digits to letters (just like on the telephone buttons) is given below. Note that 1 does not map to any letters.
> 
> **Example 1:**
> ```
> Input: digits = "23"
> Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
> ```
> 
> **Example 2:**
> ```
> Input: digits = ""
> Output: []
> ```
> 
> **Example 3:**
> ```
> Input: digits = "2"
> Output: ["a","b","c"]
> ```
> 
> **Constraints:**
> - 0 <= digits.length <= 4
> - digits[i] is a digit in the range ['2', '9'].

> [!info] Approach
> Each digit maps to 3-4 letters — pure Cartesian product. Backtracking is the natural enumeration: at depth d, choose one letter for digit[d]; total combinations = product of group sizes. At each depth d, iterate over letters for `digits[d]`; append, recurse, pop. Base case: `d == len(digits)` → record. No pruning needed — every path is valid.

> [!note]- Python Solution
> ```python
> def letter_combinations(digits):
>     if not digits:
>         return []
>     phone = {
>         '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
>         '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
>     }
>     result = []
>     path = []
> 
>     def backtrack(d):
>         if d == len(digits):
>             result.append("".join(path))
>             return
>         for ch in phone[digits[d]]:
>             path.append(ch)
>             backtrack(d + 1)
>             path.pop()
> 
>     backtrack(0)
>     return result
> ```

> [!success] Complexity
> O(4^n · n) where n = len(digits); O(n) recursion depth.

> [!tip] Alternatives
> Iterative BFS: queue of partial strings, extend by one character per level — O(4^n · n). Equivalent, more memory.

---

## Permutations

### Permutations `🎯 T2`

> [!example] Problem
> Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,3]
> Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,1]
> Output: [[0,1],[1,0]]
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1]
> Output: [[1]]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 6
> - -10 <= nums[i] <= 10
> - All the integers of nums are unique.

> [!info] Approach
> Each permutation chooses from all remaining unused elements at each depth. Tree: depth n, branching factor decreasing from n to 1, total leaves = n!. A `used` boolean array gives O(1) per check without removing elements from the array. At each level, try all unused elements; mark used → recurse → mark unused. Base case: `len(path) == n`. No pruning — every branch leads to a valid permutation.

> [!note]- Python Solution
> ```python
> def permute(nums):
>     result = []
>     path = []
>     used = [False] * len(nums)
> 
>     def backtrack():
>         if len(path) == len(nums):
>             result.append(path[:])
>             return
>         for i, num in enumerate(nums):
>             if used[i]:
>                 continue
>             used[i] = True
>             path.append(num)
>             backtrack()
>             path.pop()
>             used[i] = False
> 
>     backtrack()
>     return result
> ```

> [!success] Complexity
> O(n · n!) time, O(n) recursion depth.

> [!tip] Alternatives
> Swap-based in-place: swap `nums[start]` with `nums[i]`, recurse on `start+1`, swap back — O(n!) space-efficient. Itertools.permutations.

---

### Permutations II (with duplicates) `🎯 T2`

> [!example] Problem
> Given a collection of numbers, nums, that might contain duplicates, return all possible unique permutations in any order.
> 
> **Example 1:**
> ```
> Input: nums = [1,1,2]
> Output:
> [[1,1,2],
>  [1,2,1],
>  [2,1,1]]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,3]
> Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 8
> - -10 <= nums[i] <= 10

> [!info] Approach
> Duplicate values can appear at the same position in the permutation tree, generating identical permutations. Sort the array; skip element i if `nums[i] == nums[i-1]` and `used[i-1] == False` — this enforces canonical ordering: among duplicates, always use the leftmost first (so its predecessor is always used before it). Same structure as Permutations; sort + the `not used[i-1]` deduplication condition. `if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue`.

> [!note]- Python Solution
> ```python
> def permute_unique(nums):
>     nums.sort()
>     result = []
>     path = []
>     used = [False] * len(nums)
> 
>     def backtrack():
>         if len(path) == len(nums):
>             result.append(path[:])
>             return
>         for i in range(len(nums)):
>             if used[i]:
>                 continue
>             if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
>                 continue  # canonical ordering: use first copy before second
>             used[i] = True
>             path.append(nums[i])
>             backtrack()
>             path.pop()
>             used[i] = False
> 
>     backtrack()
>     return result
> ```

> [!success] Complexity
> O(n · n!) worst case (all distinct), fewer with duplicates; O(n) space.

> [!tip] Alternatives
> Set deduplication: add results to set — generates duplicates then discards, wasteful. Counter-based: track remaining count per value, try each value up to its remaining count.

---

### Next Permutation (iterative approach) `🎯 T2`

> [!example] Problem
> A permutation of an array of integers is an arrangement of its members into a sequence or linear order.
> The next permutation of an array of integers is the next lexicographically greater permutation of its integer. More formally, if all the permutations of the array are sorted in one container according to their lexicographical order, then the next permutation of that array is the permutation that follows it in the sorted container. If such arrangement is not possible, the array must be rearranged as the lowest possible order (i.e., sorted in ascending order).
> Given an array of integers nums, find the next permutation of nums.
> The replacement must be in place and use only constant extra memory.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,3]
> Output: [1,3,2]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,2,1]
> Output: [1,2,3]
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1,1,5]
> Output: [1,5,1]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 100
> - 0 <= nums[i] <= 100

> [!info] Approach
> Not backtracking per se, but generates the next item in the permutation enumeration order. Algorithm: find the rightmost "ascent" — the pivot where the sequence stops being descending from right. Swap pivot with the smallest element to its right that is larger, then reverse the suffix. (1) Find pivot: rightmost i where nums[i] < nums[i+1]. (2) Find rightmost j > i where nums[j] > nums[i]. (3) Swap i and j. (4) Reverse suffix from i+1. If no pivot found (fully descending), entire array is reversed.

> [!note]- Python Solution
> ```python
> def next_permutation(nums):
>     n = len(nums)
>     # Step 1: Find pivot (rightmost ascent)
>     i = n - 2
>     while i >= 0 and nums[i] >= nums[i + 1]:
>         i -= 1
>     if i >= 0:
>         # Step 2: Find rightmost element larger than pivot
>         j = n - 1
>         while nums[j] <= nums[i]:
>             j -= 1
>         nums[i], nums[j] = nums[j], nums[i]
>     # Step 3: Reverse suffix (whether or not pivot found)
>     nums[i + 1:] = nums[i + 1:][::-1]
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> No practical alternatives for in-place O(n) O(1). Generating all permutations then finding next is O(n! · n) — infeasible.

---

### Letter Case Permutation `🎯 T2`

> [!example] Problem
> Given a string s, you can transform every letter individually to be lowercase or uppercase to create another string.
> Return a list of all possible strings we could create. Return the output in any order.
> 
> **Example 1:**
> ```
> Input: s = "a1b2"
> Output: ["a1b2","a1B2","A1b2","A1B2"]
> ```
> 
> **Example 2:**
> ```
> Input: s = "3z4"
> Output: ["3z4","3Z4"]
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 12
> - s consists of lowercase English letters, uppercase English letters, and digits.

> [!info] Approach
> Each letter has two choices (upper/lower); digits have one choice. Binary tree of depth = number of letters. Total leaves = 2^(# letters). No pruning needed. At each index, if digit: recurse on next index directly. If letter: try lowercase and uppercase, recurse each. String building via list (mutable); convert at leaf.

> [!note]- Python Solution
> ```python
> def letter_case_permutation(s):
>     result = []
>     path = list(s)
> 
>     def backtrack(i):
>         if i == len(path):
>             result.append("".join(path))
>             return
>         backtrack(i + 1)  # keep as-is (or digit)
>         if path[i].isalpha():
>             path[i] = path[i].swapcase()
>             backtrack(i + 1)
>             path[i] = path[i].swapcase()  # restore
> 
>     backtrack(0)
>     return result
> ```

> [!success] Complexity
> O(2^L · n) where L = # letters, n = len(s); O(n) recursion depth.

> [!tip] Alternatives
> BFS: queue of partial strings — O(2^L · n), more memory. Bitmask: iterate over 2^L masks, assign upper/lower based on bits.

---

## String Backtracking

### Generate Parentheses `🎯 T2`

> [!example] Problem
> Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.
> 
> **Example 1:**
> ```
> Input: n = 3
> Output: ["((()))","(()())","(())()","()(())","()()()"]
> ```
> 
> **Example 2:**
> ```
> Input: n = 1
> Output: ["()"]
> ```
> 
> **Constraints:**
> - 1 <= n <= 8

> [!info] Approach
> At each position, two choices: `(` or `)`. Constraint-driven pruning eliminates all invalid paths: add `(` only if `open < n`; add `)` only if `close < open`. This prunes invalid sequences before they're fully built — no validity check needed at the leaf. Track `open_cnt` and `close_cnt`. Branch into `(` or `)` based on constraints. Leaf count = Catalan number C(n). The invariant `close < open` ensures every partial string is a valid prefix.

> [!note]- Python Solution
> ```python
> def generate_parenthesis(n):
>     result = []
> 
>     def backtrack(path, open_cnt, close_cnt):
>         if len(path) == 2 * n:
>             result.append(path)
>             return
>         if open_cnt < n:
>             backtrack(path + '(', open_cnt + 1, close_cnt)
>         if close_cnt < open_cnt:
>             backtrack(path + ')', open_cnt, close_cnt + 1)
> 
>     backtrack('', 0, 0)
>     return result
> ```

> [!success] Complexity
> O(4^n / sqrt(n)) — Catalan number C(n); O(n) recursion depth.

> [!tip] Alternatives
> DP: `dp[i]` = all valid strings of i pairs, built from sub-problems — same time complexity. Closure number decomposition: `'(' + dp[c] + ')' + dp[n-1-c]` for c in 0..n-1.

---

### Palindrome Partitioning `🎯 T2`

> [!example] Problem
> Given a string s, partition s such that every substring of the partition is a palindrome. Return all possible palindrome partitioning of s.
> 
> **Example 1:**
> ```
> Input: s = "aab"
> Output: [["a","a","b"],["aa","b"]]
> ```
> 
> **Example 2:**
> ```
> Input: s = "a"
> Output: [["a"]]
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 16
> - s contains only lowercase English letters.

> [!info] Approach
> At each position, try all possible next partition points. Pruning: skip substrings that aren't palindromes. Precomputing palindrome-ness for all substrings (O(n²)) avoids O(n) palindrome checks during backtracking. At each start, try substrings `s[start..end]` for end from start to n-1. If it's a palindrome, add and recurse on rest. Precompute `is_pal[i][j]` via DP in O(n²). Then backtracking is O(2^n) calls × O(1) palindrome check.

> [!note]- Python Solution
> ```python
> def partition(s):
>     n = len(s)
>     # Precompute palindrome table
>     is_pal = [[False] * n for _ in range(n)]
>     for i in range(n - 1, -1, -1):
>         for j in range(i, n):
>             if s[i] == s[j] and (j - i <= 2 or is_pal[i + 1][j - 1]):
>                 is_pal[i][j] = True
> 
>     result = []
>     path = []
> 
>     def backtrack(start):
>         if start == n:
>             result.append(path[:])
>             return
>         for end in range(start, n):
>             if is_pal[start][end]:
>                 path.append(s[start:end + 1])
>                 backtrack(end + 1)
>                 path.pop()
> 
>     backtrack(0)
>     return result
> ```

> [!success] Complexity
> O(n · 2^n) time (2^n partitions, each O(n) to copy); O(n²) space for palindrome table.

> [!tip] Alternatives
> Without precomputation: O(n) palindrome check per substring — O(n² · 2^n) total. Manacher's algorithm for O(n) palindrome precomputation.

---

### Remove Invalid Parentheses

> [!example] Problem
> Given a string s that contains parentheses and letters, remove the minimum number of invalid parentheses to make the input string valid.
> Return a list of unique strings that are valid with the minimum number of removals. You may return the answer in any order.
> 
> **Example 1:**
> ```
> Input: s = "()())()"
> Output: ["(())()","()()()"]
> ```
> 
> **Example 2:**
> ```
> Input: s = "(a)())()"
> Output: ["(a())()","(a)()()"]
> ```
> 
> **Example 3:**
> ```
> Input: s = ")("
> Output: [""]
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 25
> - s consists of lowercase English letters and parentheses '(' and ')'.
> - There will be at most 20 parentheses in s.

> [!info] Approach
> First compute minimum removals (one scan: track unmatched `(` as `open_rem`, unmatched `)` as `close_rem`). Then backtrack: at each character, keep or remove it. Pruning: (1) removal budget exhausted; (2) `close_cnt > open_cnt` in current path (invalid prefix); (3) consecutive same brackets — only remove the first of a run (deduplication without a set). Backtrack with state `(index, path, open_cnt, close_cnt, open_rem, close_rem)`. Compute open_rem, close_rem first; backtrack with those exact budgets.

> [!note]- Python Solution
> ```python
> def remove_invalid_parentheses(s):
>     open_rem = close_rem = 0
>     for c in s:
>         if c == '(':
>             open_rem += 1
>         elif c == ')':
>             if open_rem > 0:
>                 open_rem -= 1
>             else:
>                 close_rem += 1
> 
>     result = set()
> 
>     def backtrack(i, path, open_cnt, close_cnt, open_r, close_r):
>         if i == len(s):
>             if open_r == 0 and close_r == 0:
>                 result.add(path)
>             return
>         c = s[i]
>         # Option 1: Remove current bracket (if budget allows and it's a bracket)
>         if c == '(' and open_r > 0:
>             backtrack(i + 1, path, open_cnt, close_cnt, open_r - 1, close_r)
>         if c == ')' and close_r > 0:
>             backtrack(i + 1, path, open_cnt, close_cnt, open_r, close_r - 1)
>         # Option 2: Keep current character
>         if c == '(':
>             backtrack(i + 1, path + c, open_cnt + 1, close_cnt, open_r, close_r)
>         elif c == ')':
>             if close_cnt < open_cnt:  # valid to add: won't go negative
>                 backtrack(i + 1, path + c, open_cnt, close_cnt + 1, open_r, close_r)
>         else:
>             backtrack(i + 1, path + c, open_cnt, close_cnt, open_r, close_r)
> 
>     backtrack(0, '', 0, 0, open_rem, close_rem)
>     return list(result)
> ```

> [!success] Complexity
> O(2^n) worst case; O(n) recursion depth.

> [!tip] Alternatives
> BFS level-by-level removing one bracket per level — O(n · 2^n), simpler correctness argument (BFS guarantees minimum removals), but higher memory. DFS with explicit consecutive-duplicate pruning can eliminate the set.

---

### Word Search `⚡ T1`

> [!example] Problem
> Given an m x n grid of characters board and a string word, return true if word exists in the grid.
> The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.
> 
> **Example 1:**
> ```
> Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "SEE"
> Output: true
> ```
> 
> **Example 3:**
> ```
> Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"
> Output: false
> ```
> 
> **Constraints:**
> - m == board.length
> - n = board[i].length
> - 1 <= m, n <= 6
> - 1 <= word.length <= 15
> - board and word consists of only lowercase and uppercase English letters.

> [!info] Approach
> Need to find a specific path through a grid — DFS with backtracking is the natural approach. Pruning: mismatch at any character immediately abandons that branch. Temporary in-place marking avoids extra visited array. DFS from each cell matching `word[0]`. At each step, mark cell visited (`'#'`), recurse on 4 neighbors for next character, then restore. Early return True on complete match. Board is restored on each backtrack.

> [!note]- Python Solution
> ```python
> def exist(board, word):
>     m, n = len(board), len(board[0])
>     directions = ((0, 1), (0, -1), (1, 0), (-1, 0))
>
>     def dfs(r, c, i):
>         if i == len(word):
>             return True
>         if not (0 <= r < m and 0 <= c < n):
>             return False
>         if board[r][c] != word[i]:
>             return False
>         tmp = board[r][c]
>         board[r][c] = '#'
>         found = False
>         for dr, dc in directions:
>             if dfs(r + dr, c + dc, i + 1):
>                 found = True
>                 break
>         board[r][c] = tmp
>         return found
>
>     for r in range(m):
>         for c in range(n):
>             if dfs(r, c, 0):
>                 return True
>     return False
> ```

> [!success] Complexity
> O(m · n · 4^L) where L = len(word); O(L) recursion depth.

> [!tip] Alternatives
> BFS per starting cell: exponential memory — infeasible. Pruning with character frequency check before DFS: O(mn) precheck can prune early.

---

### Expression Add Operators (LC 282)

> [!example] Problem
> Given a string num that contains only digits and an integer target, return all possibilities to insert the binary operators '+', '-', and/or '*' between the digits of num so that the resultant expression evaluates to the target value.
> Note that operands in the returned expressions should not contain leading zeros.
> Note that a number can contain multiple digits.
> 
> **Example 1:**
> ```
> Input: num = "123", target = 6
> Output: ["1*2*3","1+2+3"]
> Explanation: Both "1*2*3" and "1+2+3" evaluate to 6.
> ```
> 
> **Example 2:**
> ```
> Input: num = "232", target = 8
> Output: ["2*3+2","2+3*2"]
> Explanation: Both "2*3+2" and "2+3*2" evaluate to 8.
> ```
> 
> **Example 3:**
> ```
> Input: num = "3456237490", target = 9191
> Output: []
> Explanation: There are no expressions that can be created from "3456237490" to evaluate to 9191.
> ```
> 
> **Constraints:**
> - 1 <= num.length <= 10
> - num consists of only digits.
> - -2^{31} <= target <= 2^{31} - 1

> [!info] Approach
> Brute force tries all 3^(n-1) operator placements. Backtracking prunes early (e.g. skip leading-zero operands immediately). The key challenge: `*` has higher precedence — multiplying undoes the previous addition/subtraction, so we track `prev_operand` to "undo" it. Backtracking with state `(index, current_expression, current_value, prev_operand)`.

>   - At each position, try all possible next numbers (no leading zeros except `"0"` itself).
>   - For each number as next operand:
>     - First operand: recurse with `value = num_val`, `prev = num_val`.
>     - `+`: `new_val = value + num_val`, `new_prev = +num_val`.
>     - `-`: `new_val = value - num_val`, `new_prev = -num_val`.
>     - `*`: `new_val = value - prev + prev * num_val`, `new_prev = prev * num_val`. *(Undo prev add/sub, redo as product.)*
>   - Base: if `index == len(num)` and `value == target`: add expression to result.

> [!note]- Python Solution
> ```python
> def add_operators(num, target):
>     result = []
>     n = len(num)
> 
>     def backtrack(index, expr, value, prev):
>         if index == n:
>             if value == target:
>                 result.append(expr)
>             return
>         for end in range(index + 1, n + 1):
>             token = num[index:end]
>             # No leading zeros for multi-digit operands
>             if len(token) > 1 and token[0] == '0':
>                 break
>             num_val = int(token)
>             if index == 0:
>                 # First operand: no operator prefix
>                 backtrack(end, token, num_val, num_val)
>             else:
>                 # Try +
>                 backtrack(end, expr + '+' + token, value + num_val, num_val)
>                 # Try -
>                 backtrack(end, expr + '-' + token, value - num_val, -num_val)
>                 # Try *: undo previous op, apply multiplication
>                 backtrack(end, expr + '*' + token, value - prev + prev * num_val, prev * num_val)
> 
>     backtrack(0, '', 0, 0)
>     return result
> ```

> [!success] Complexity
> O(4^n × n) — at each of n digit positions, up to 4 choices (3 operators + extend operand); O(n) for string slicing/building at each node. Space O(n) recursion depth.

> [!tip] Alternatives
> - Build expression string then evaluate: simpler code (avoid tracking `prev`), but evaluation is O(n) per leaf — same overall complexity, harder to prove correctness for `*` precedence.
> - Pure brute force without backtracking: generate all 3^(n-1) operator strings, evaluate each — no early pruning on leading zeros, same worst-case O(4^n × n).

---

## Board / Matrix Backtracking

### N-Queens `🎯 T2`

> [!example] Problem
> The n-queens puzzle is the problem of placing n queens on an n x n chessboard such that no two queens attack each other.
> Given an integer n, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.
> Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space, respectively.
> 
> **Example 1:**
> ```
> Input: n = 4
> Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
> Explanation: There exist two distinct solutions to the 4-queens puzzle as shown above
> ```
> 
> **Example 2:**
> ```
> Input: n = 1
> Output: [["Q"]]
> ```
> 
> **Constraints:**
> - 1 <= n <= 9

> [!info] Approach
> One queen per row (DFS depth = row). At each row, try all columns; conflict check in O(1) using three constraint sets: `cols`, `diags` (row-col=const), `anti_diags` (row+col=const). Pruning eliminates all attacking positions immediately. Backtrack row by row. At each row, iterate columns; skip if any constraint set contains the column/diagonal. Add to sets before recursing; remove after. Leaf (row==n) records the board.

> [!note]- Python Solution
> ```python
> def solve_n_queens(n):
>     result = []
>     cols = set()
>     diags = set()
>     anti_diags = set()
>     board = [['.' ] * n for _ in range(n)]
> 
>     def backtrack(row):
>         if row == n:
>             result.append([''.join(r) for r in board])
>             return
>         for col in range(n):
>             d, ad = row - col, row + col
>             if col in cols or d in diags or ad in anti_diags:
>                 continue
>             cols.add(col)
>             diags.add(d)
>             anti_diags.add(ad)
>             board[row][col] = 'Q'
>             backtrack(row + 1)
>             board[row][col] = '.'
>             cols.remove(col)
>             diags.remove(d)
>             anti_diags.remove(ad)
> 
>     backtrack(0)
>     return result
> ```

> [!success] Complexity
> O(n!) upper bound; actual solutions grow roughly as n!/e^n; O(n²) board space.

> [!tip] Alternatives
> Bitmask N-Queens: represent cols/diags/anti-diags as integers, use bit ops to find valid positions per row — lower constant, cache-friendly. Symmetry reduction: halve work for row 0.

---

### Sudoku Solver `🎯 T2`

> [!example] Problem
> Write a program to solve a Sudoku puzzle by filling the empty cells.
> A sudoku solution must satisfy all of the following rules:
> The '.' character indicates empty cells.
> 
> **Example 1:**
> ```
> Input: board = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
> Output: [["5","3","4","6","7","8","9","1","2"],["6","7","2","1","9","5","3","4","8"],["1","9","8","3","4","2","5","6","7"],["8","5","9","7","6","1","4","2","3"],["4","2","6","8","5","3","7","9","1"],["7","1","3","9","2","4","8","5","6"],["9","6","1","5","3","7","2","8","4"],["2","8","7","4","1","9","6","3","5"],["3","4","5","2","8","6","1","7","9"]]
> Explanation: The input board is shown above and the only valid solution is shown below:
> ```
> 
> **Constraints:**
> - board.length == 9
> - board[i].length == 9
> - board[i][j] is a digit or '.'.
> - It is guaranteed that the input board has only one solution.

> [!info] Approach
> Constraint satisfaction: each empty cell has a small set of valid digits. Backtrack on the first empty cell, try all valid digits, recurse. Pruning is per-digit in O(1) via pre-populated boolean arrays. The search space is theoretically 9^81 but practically near-constant for valid puzzles due to constraint propagation via elimination. Precompute `rows[r][d]`, `cols[c][d]`, `boxes[b][d]` tracking used digits. Iterate empty cells; try 1-9; recurse; undo if stuck. box_id = `(r//3)*3 + c//3`. Linear scan for next empty cell at each recursion level.

> [!note]- Python Solution
> ```python
> def solve_sudoku(board):
>     rows = [[False] * 10 for _ in range(9)]
>     cols = [[False] * 10 for _ in range(9)]
>     boxes = [[False] * 10 for _ in range(9)]
> 
>     def box_id(r, c):
>         return (r // 3) * 3 + c // 3
> 
>     for r in range(9):
>         for c in range(9):
>             if board[r][c] != '.':
>                 d = int(board[r][c])
>                 rows[r][d] = cols[c][d] = boxes[box_id(r, c)][d] = True
> 
>     def backtrack(pos):
>         while pos < 81 and board[pos // 9][pos % 9] != '.':
>             pos += 1
>         if pos == 81:
>             return True
>         r, c = pos // 9, pos % 9
>         for d in range(1, 10):
>             if rows[r][d] or cols[c][d] or boxes[box_id(r, c)][d]:
>                 continue
>             rows[r][d] = cols[c][d] = boxes[box_id(r, c)][d] = True
>             board[r][c] = str(d)
>             if backtrack(pos + 1):
>                 return True
>             board[r][c] = '.'
>             rows[r][d] = cols[c][d] = boxes[box_id(r, c)][d] = False
>         return False
> 
>     backtrack(0)
> ```

> [!success] Complexity
> O(9^m) where m = empty cells; practically O(1) for valid puzzles.

> [!tip] Alternatives
> MRV heuristic (most-constrained variable): always fill cell with fewest valid digits first — dramatically reduces backtracking. Dancing Links (Algorithm X): optimal exact cover solver, overkill for interviews.

---

### Unique Paths III `🎯 T2`

> [!example] Problem
> You are given an m x n integer array grid where grid[i][j] could be:
> Return the number of 4-directional walks from the starting square to the ending square, that walk over every non-obstacle square exactly once.
> 
> **Example 1:**
> ```
> Input: grid = [[1,0,0,0],[0,0,0,0],[0,0,2,-1]]
> Output: 2
> Explanation: We have the following two paths: 
> 1. (0,0),(0,1),(0,2),(0,3),(1,3),(1,2),(1,1),(1,0),(2,0),(2,1),(2,2)
> 2. (0,0),(1,0),(2,0),(2,1),(1,1),(0,1),(0,2),(0,3),(1,3),(1,2),(2,2)
> ```
> 
> **Example 2:**
> ```
> Input: grid = [[1,0,0,0],[0,0,0,0],[0,0,0,2]]
> Output: 4
> Explanation: We have the following four paths: 
> 1. (0,0),(0,1),(0,2),(0,3),(1,3),(1,2),(1,1),(1,0),(2,0),(2,1),(2,2),(2,3)
> 2. (0,0),(0,1),(1,1),(1,0),(2,0),(2,1),(2,2),(1,2),(0,2),(0,3),(1,3),(2,3)
> 3. (0,0),(1,0),(2,0),(2,1),(2,2),(1,2),(1,1),(0,1),(0,2),(0,3),(1,3),(2,3)
> 4. (0,0),(1,0),(2,0),(2,1),(1,1),(0,1),(0,2),(0,3),(1,3),(1,2),(2,2),(2,3)
> ```
> 
> **Example 3:**
> ```
> Input: grid = [[0,1],[2,0]]
> Output: 0
> Explanation: There is no path that walks over every empty square exactly once.
> Note that the starting and ending square can be anywhere in the grid.
> ```
> 
> **Constraints:**
> - m == grid.length
> - n == grid[i].length
> - 1 <= m, n <= 20
> - 1 <= m * n <= 20
> - -1 <= grid[i][j] <= 2
> - There is exactly one starting cell and one ending cell.

> [!info] Approach
> Hamiltonian path problem on a grid — no polynomial algorithm exists. DFS with backtracking, pruning when all non-obstacle cells must be visited exactly once. Count all non-obstacle cells (including start and end). DFS from start; at each step, mark visited; if at end and all cells visited, count +1. Track `remaining` count of unvisited non-obstacle cells. Prune when stuck (all 4 neighbors blocked and remaining > 1).

> [!note]- Python Solution
> ```python
> def unique_paths_iii(grid):
>     m, n = len(grid), len(grid[0])
>     start_r = start_c = 0
>     total = 0  # total non-obstacle cells to visit
>     for r in range(m):
>         for c in range(n):
>             if grid[r][c] != -1:
>                 total += 1
>             if grid[r][c] == 1:
>                 start_r, start_c = r, c
> 
>     count = 0
> 
>     def dfs(r, c, visited):
>         nonlocal count
>         if grid[r][c] == 2:
>             if visited == total:
>                 count += 1
>             return
>         for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] != -1:
>                 grid[nr][nc], orig = -2, grid[nr][nc]  # mark
>                 dfs(nr, nc, visited + 1)
>                 grid[nr][nc] = orig  # restore
> 
>     grid[start_r][start_c] = -2  # mark start visited
>     dfs(start_r, start_c, 1)
>     grid[start_r][start_c] = 1
>     return count
> ```

> [!success] Complexity
> O(4^(m·n)) worst case; O(m·n) recursion depth.

> [!tip] Alternatives
> Bitmask DP: `dp[r][c][mask]` = number of paths visiting cells in `mask` ending at (r,c) — O(m·n·2^(mn)) space, infeasible for large grids. Backtracking with in-place marking is the standard approach.

---

## Trie + Backtracking

### Combination Sum III `🎯 T2`

> [!example] Problem
> Find all valid combinations of k numbers that sum up to n such that the following conditions are true:
> Return a list of all possible valid combinations. The list must not contain the same combination twice, and the combinations may be returned in any order.
> 
> **Example 1:**
> ```
> Input: k = 3, n = 7
> Output: [[1,2,4]]
> Explanation:
> 1 + 2 + 4 = 7
> There are no other valid combinations.
> ```
> 
> **Example 2:**
> ```
> Input: k = 3, n = 9
> Output: [[1,2,6],[1,3,5],[2,3,4]]
> Explanation:
> 1 + 2 + 6 = 9
> 1 + 3 + 5 = 9
> 2 + 3 + 4 = 9
> There are no other valid combinations.
> ```
> 
> **Example 3:**
> ```
> Input: k = 4, n = 1
> Output: []
> Explanation: There are no valid combinations.
> Using 4 different numbers in the range [1,9], the smallest sum we can get is 1+2+3+4 = 10 and since 10 > 1, there are no valid combination.
> ```
> 
> **Constraints:**
> - 2 <= k <= 9
> - 1 <= n <= 60

> [!info] Approach
> Fixed-size (exactly k elements), fixed-sum, fixed universe (1-9). Tight structural bounds enable strong pruning: (1) more than k elements chosen → stop; (2) remaining sum impossible with remaining numbers → stop (min achievable = sum of smallest k-len remaining numbers). Backtrack over digits 1-9 with `start`, tracking `remaining` and `count`. Prune when `count > k` or `remaining < 0`. Record when `count == k and remaining == 0`. Because the domain is tiny (1-9), no sorting needed — it's inherently sorted. Upper bound prune: if `remaining > sum(range(start, 10))[:k-len(path)]`, stop.

> [!note]- Python Solution
> ```python
> def combination_sum3(k, n):
>     result = []
>     path = []
> 
>     def backtrack(start, remaining):
>         if len(path) == k and remaining == 0:
>             result.append(path[:])
>             return
>         if len(path) == k or remaining <= 0:
>             return
>         for i in range(start, 10):
>             # Prune: even taking the smallest available numbers won't reach 0
>             slots_left = k - len(path)
>             if i > remaining:
>                 break  # i is the smallest we'd add; can't decrease remaining to 0
>             if slots_left == 1 and i != remaining:
>                 # Only one slot; must match exactly
>                 if i < remaining:
>                     continue
>                 break
>             path.append(i)
>             backtrack(i + 1, remaining - i)
>             path.pop()
> 
>     backtrack(1, n)
>     return result
> ```

> [!success] Complexity
> O(C(9,k) · k) — at most C(9,k) valid subsets of size k from {1..9}; O(k) recursion depth.

> [!tip] Alternatives
> Bitmask: iterate all 2^9 = 512 subsets, check popcount == k and sum == n — O(512 · 9), perfectly fine for this fixed domain. Simpler code, not generalizable.

---

### Target Sum `🎯 T2`

> [!example] Problem
> You are given an integer array nums and an integer target.
> You want to build an expression out of nums by adding one of the symbols '+' and '-' before each integer in nums and then concatenate all the integers.
> Return the number of different expressions that you can build, which evaluates to target.
> 
> **Example 1:**
> ```
> Input: nums = [1,1,1,1,1], target = 3
> Output: 5
> Explanation: There are 5 ways to assign symbols to make the sum of nums be target 3.
> -1 + 1 + 1 + 1 + 1 = 3
> +1 - 1 + 1 + 1 + 1 = 3
> +1 + 1 - 1 + 1 + 1 = 3
> +1 + 1 + 1 - 1 + 1 = 3
> +1 + 1 + 1 + 1 - 1 = 3
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1], target = 1
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 20
> - 0 <= nums[i] <= 1000
> - 0 <= sum(nums[i]) <= 1000
> - -1000 <= target <= 1000

> [!info] Approach
> Binary choice per element (+ or -) → 2^n branches. DP solution exists, but backtracking is instructive. Pruning: track remaining reachable range — if `current + sum(remaining) < target` or `current - sum(remaining) > target`, prune. DP (subset sum variant) is O(n · total_sum) and preferred at scale. At each index, branch into `+nums[i]` and `-nums[i]`. Count paths reaching target at depth n. Backtracking here: O(2^n). DP reduction: let P = sum of positives, N = sum of negatives. P - N = target, P + N = total → P = (target + total) / 2. Count subsets summing to P.

> [!note]- Python Solution
> ```python
> def find_target_sum_ways(nums, target):
>     # Backtracking approach (educational)
>     count = 0
>     n = len(nums)
>     suffix_sum = [0] * (n + 1)
>     for i in range(n - 1, -1, -1):
>         suffix_sum[i] = suffix_sum[i + 1] + nums[i]
> 
>     def backtrack(i, current):
>         nonlocal count
>         if i == n:
>             if current == target:
>                 count += 1
>             return
>         # Pruning: even if all remaining are +, can't reach target
>         if current + suffix_sum[i] < target:
>             return
>         # Pruning: even if all remaining are -, can't reach target
>         if current - suffix_sum[i] > target:
>             return
>         backtrack(i + 1, current + nums[i])
>         backtrack(i + 1, current - nums[i])
> 
>     backtrack(0, 0)
>     return count
> ```

> [!success] Complexity
> O(2^n) backtracking (with pruning, much less); O(n) space. DP alternative: O(n · S) where S = sum of all nums.

> [!tip] Alternatives
> Subset-sum DP: P = (target + total) / 2; count subsets summing to P using 1D DP — O(n · S), much better for large n. Memoization on (index, current_sum) — O(n · 2S) states.

---

### Beautiful Arrangement `🎯 T2`

> [!example] Problem
> Suppose you have n integers labeled 1 through n. A permutation of those n integers perm (1-indexed) is considered a beautiful arrangement if for every i (1 <= i <= n), either of the following is true:
> Given an integer n, return the number of the beautiful arrangements that you can construct.
> 
> **Example 1:**
> ```
> Input: n = 2
> Output: 2
> Explanation: 
> The first beautiful arrangement is [1,2]:
>     - perm[1] = 1 is divisible by i = 1
>     - perm[2] = 2 is divisible by i = 2
> The second beautiful arrangement is [2,1]:
>     - perm[1] = 2 is divisible by i = 1
>     - i = 2 is divisible by perm[2] = 1
> ```
> 
> **Example 2:**
> ```
> Input: n = 1
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= n <= 15

> [!info] Approach
> Permutation backtracking where each position has a constraint. Fill positions 1..n left to right; at position `pos`, only place number `num` if `num % pos == 0 or pos % num == 0`. A `used` boolean array tracks which numbers remain. Backtrack over positions 1 to n. For each position, try all unused numbers satisfying the divisibility constraint. Track with `used` array. Pruning is implicit: invalid choices are simply not tried. Iterate numbers in decreasing order to hit more valid placements early (empirically faster).

> [!note]- Python Solution
> ```python
> def count_arrangement(n):
>     used = [False] * (n + 1)
>     count = 0
> 
>     def backtrack(pos):
>         nonlocal count
>         if pos > n:
>             count += 1
>             return
>         for num in range(n, 0, -1):  # descending: hits valid earlier
>             if not used[num] and (num % pos == 0 or pos % num == 0):
>                 used[num] = True
>                 backtrack(pos + 1)
>                 used[num] = False
> 
>     backtrack(1)
>     return count
> ```

> [!success] Complexity
> O(k) where k = number of valid arrangements; in practice much less than O(n!) due to constraint pruning. Space O(n).

> [!tip] Alternatives
> Bitmask DP: `dp[mask]` = count of arrangements for the set of numbers in `mask` filling positions 1..popcount(mask) — O(n · 2^n) time and space. Faster for large n but uses significant memory.

---

### Restore IP Addresses `🎯 T2`

> [!example] Problem
> A valid IP address consists of exactly four integers separated by single dots. Each integer is between 0 and 255 (inclusive) and cannot have leading zeros.
> Given a string s containing only digits, return all possible valid IP addresses that can be formed by inserting dots into s. You are not allowed to reorder or remove any digits in s. You may return the valid IP addresses in any order.
> 
> **Example 1:**
> ```
> Input: s = "25525511135"
> Output: ["255.255.11.135","255.255.111.35"]
> ```
> 
> **Example 2:**
> ```
> Input: s = "0000"
> Output: ["0.0.0.0"]
> ```
> 
> **Example 3:**
> ```
> Input: s = "101023"
> Output: ["1.0.10.23","1.0.102.3","10.1.0.23","10.10.2.3","101.0.2.3"]
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 20
> - s consists of digits only.

> [!info] Approach
> Exactly 4 segments, each 1-3 digits. Backtracking tries all split points. Pruning: (1) segment value > 255; (2) leading zeros (segment starting with '0' must be exactly '0'); (3) remaining digits can't form the remaining segments (each needs 1-3 digits). At each step, try taking 1, 2, or 3 characters as the next segment. If the segment is valid, recurse for the next segment. After choosing 4 segments, the entire string must be consumed. Feasibility check: `remaining_digits` must be between `remaining_segments` and `3 * remaining_segments`.

> [!note]- Python Solution
> ```python
> def restore_ip_addresses(s):
>     result = []
>     path = []
> 
>     def backtrack(start):
>         if len(path) == 4:
>             if start == len(s):
>                 result.append('.'.join(path))
>             return
>         remaining_segs = 4 - len(path)
>         remaining_chars = len(s) - start
>         # Pruning: feasibility window
>         if remaining_chars < remaining_segs or remaining_chars > 3 * remaining_segs:
>             return
>         for length in range(1, 4):
>             if start + length > len(s):
>                 break
>             segment = s[start:start + length]
>             # No leading zeros for multi-digit segments
>             if len(segment) > 1 and segment[0] == '0':
>                 break
>             if int(segment) > 255:
>                 break
>             path.append(segment)
>             backtrack(start + length)
>             path.pop()
> 
>     backtrack(0)
>     return result
> ```

> [!success] Complexity
> O(1) — at most 3^4 = 81 combinations to check (4 segments × 3 length choices); O(1) space (path depth fixed at 4).

> [!tip] Alternatives
> Triple nested loops over the three split points — O(n^3) but bounded by string length constraints, equivalent. Iterative with explicit segment validation is slightly simpler.

---

## String Backtracking (continued)

### Word Break II `🎯 T2`

> [!example] Problem
> Given a string s and a dictionary of strings wordDict, add spaces in s to construct a sentence where each word is a valid dictionary word. Return all such possible sentences in any order.
> Note that the same word in the dictionary may be reused multiple times in the segmentation.
> 
> **Example 1:**
> ```
> Input: s = "catsanddog", wordDict = ["cat","cats","and","sand","dog"]
> Output: ["cats and dog","cat sand dog"]
> ```
> 
> **Example 2:**
> ```
> Input: s = "pineapplepenapple", wordDict = ["apple","pen","applepen","pine","pineapple"]
> Output: ["pine apple pen apple","pineapple pen apple","pine applepen apple"]
> Explanation: Note that you are allowed to reuse a dictionary word.
> ```
> 
> **Example 3:**
> ```
> Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
> Output: []
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 20
> - 1 <= wordDict.length <= 1000
> - 1 <= wordDict[i].length <= 10
> - s and wordDict[i] consist of only lowercase English letters.
> - All the strings of wordDict are unique.
> - Input is generated in a way that the length of the answer doesn't exceed 10^5.

> [!info] Approach
> Try every possible first word; recurse on the suffix. Without memoization this is O(2^n) — many suffixes are explored repeatedly. Memoize the list of sentences producible from each suffix to eliminate redundant work. For each prefix `s[start:end]` that is in the word set, recurse on `s[end:]`. At `start == len(s)`, return `['']` (empty sentence). Cache results per `start`. Memoization key is `start` index. Value is list of sentence suffixes from that position. Build full sentences by prepending current word.

> [!note]- Python Solution
> ```python
> def word_break(s, wordDict):
>     word_set = set(wordDict)
>     memo = {}
> 
>     def backtrack(start):
>         if start in memo:
>             return memo[start]
>         if start == len(s):
>             return ['']
>         sentences = []
>         for end in range(start + 1, len(s) + 1):
>             word = s[start:end]
>             if word in word_set:
>                 for rest in backtrack(end):
>                     if rest:
>                         sentences.append(word + ' ' + rest)
>                     else:
>                         sentences.append(word)
>         memo[start] = sentences
>         return sentences
> 
>     return backtrack(0)
> ```

> [!success] Complexity
> O(n^2 · 2^n / n) in worst case (exponential output); memoization ensures each suffix is solved once. O(n^2) time if output size is ignored; space O(n · output_size).

> [!tip] Alternatives
> Two-phase: (1) DP to check reachable positions; backtrack only through reachable ones — prunes dead-end paths early, same asymptotic. Trie for O(1) prefix lookups instead of O(n) hash.

---

### Palindrome Partitioning II (Minimum Cuts) `🎯 T2`

> [!example] Problem
> Given a string s, partition s such that every substring of the partition is a palindrome.
> Return the minimum cuts needed for a palindrome partitioning of s.
> 
> **Example 1:**
> ```
> Input: s = "aab"
> Output: 1
> Explanation: The palindrome partitioning ["aa","b"] could be produced using 1 cut.
> ```
> 
> **Example 2:**
> ```
> Input: s = "a"
> Output: 0
> ```
> 
> **Example 3:**
> ```
> Input: s = "ab"
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 2000
> - s consists of lowercase English letters only.

> [!info] Approach
> Pure backtracking (enumerate all partitions) is O(n · 2^n). This is an optimization problem — we want the minimum, not all solutions. DP with palindrome precomputation achieves O(n^2). Backtracking is included for completeness but DP is the correct approach here. **WHAT (DP):** Precompute `is_pal[i][j]`. Then `dp[i]` = min cuts for `s[:i]`. Transition: `dp[j] = min(dp[j], dp[i] + 1)` if `s[i:j]` is palindrome. `dp[0] = 0` (empty prefix needs 0 cuts). Final answer: `dp[n] - 1` (subtracting the artificial initial cut). Equivalently, `dp[i]` = min cuts for first `i` chars → `dp[n]`.

> [!note]- Python Solution
> ```python
> def min_cut(s):
>     n = len(s)
>     # Precompute palindrome table
>     is_pal = [[False] * n for _ in range(n)]
>     for i in range(n - 1, -1, -1):
>         for j in range(i, n):
>             if s[i] == s[j] and (j - i <= 2 or is_pal[i + 1][j - 1]):
>                 is_pal[i][j] = True
> 
>     # dp[i] = min cuts for s[0:i]
>     dp = list(range(n))  # worst case: cut between every character
>     for i in range(1, n):
>         if is_pal[0][i]:
>             dp[i] = 0
>             continue
>         for j in range(1, i + 1):
>             if is_pal[j][i]:
>                 dp[i] = min(dp[i], dp[j - 1] + 1)
>     return dp[n - 1]
> ```

> [!success] Complexity
> O(n^2) time (palindrome table + DP); O(n^2) space. Manacher's reduces palindrome precomputation to O(n).

> [!tip] Alternatives
> Pure backtracking: O(n · 2^n) — impractical. Expand-around-center for palindrome check during DP: avoids the O(n^2) table but requires careful integration. Manacher's + DP achieves O(n) time with O(n) space.

---

## Grid Traversal

### Rat in a Maze `🎯 T2`

> [!example] Problem
> Find all paths for a rat from top-left (0,0) to bottom-right (n-1,n-1) in an n×n binary maze (1=open, 0=blocked), moving in 4 directions without revisiting.

> [!info] Approach
> Enumerate all valid root-to-destination paths in a grid graph. DFS with backtracking; mark cells visited to prevent cycles; unmark on backtrack. From current cell (r,c), try all 4 directions. Move to neighbor if it's in bounds, open (value 1), and not visited. Mark visited before recursing; unmark after. Record path direction string at destination. Path encoded as direction string ('D','L','R','U'). Sort output lexicographically — lexicographic DFS order (try D,L,R,U alphabetically) naturally produces sorted output.

> [!note]- Python Solution
> ```python
> def find_path(maze):
>     n = len(maze)
>     if not maze or maze[0][0] == 0 or maze[n-1][n-1] == 0:
>         return []
>     result = []
>     visited = [[False] * n for _ in range(n)]
>     # Try directions in alphabetical order for sorted output
>     dirs = [('D', 1, 0), ('L', 0, -1), ('R', 0, 1), ('U', -1, 0)]
> 
>     def backtrack(r, c, path):
>         if r == n - 1 and c == n - 1:
>             result.append(''.join(path))
>             return
>         visited[r][c] = True
>         for d, dr, dc in dirs:
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < n and 0 <= nc < n and maze[nr][nc] == 1 and not visited[nr][nc]:
>                 path.append(d)
>                 backtrack(nr, nc, path)
>                 path.pop()
>         visited[r][c] = False
> 
>     backtrack(0, 0, [])
>     return result
> ```

> [!success] Complexity
> O(4^(n^2)) worst case; O(n^2) recursion depth.

> [!tip] Alternatives
> BFS for shortest path only (not all paths). Bitmask visited for small n. In practice, paths are few due to maze constraints.

---

### Word Search (All Occurrences) `⚡ T1`

> [!example] Problem
> Given an m x n grid of characters board and a string word, return true if word exists in the grid.
> The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.
> 
> **Example 1:**
> ```
> Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "SEE"
> Output: true
> ```
> 
> **Example 3:**
> ```
> Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"
> Output: false
> ```
> 
> **Constraints:**
> - m == board.length
> - n = board[i].length
> - 1 <= m, n <= 6
> - 1 <= word.length <= 15
> - board and word consists of only lowercase and uppercase English letters.

> [!info] Approach
> Extension of Word Search I: instead of stopping at the first match, collect all starting (r,c) positions. Same DFS + backtracking logic; just collect results instead of returning early. From each unvisited cell matching `word[0]`, run DFS. If DFS succeeds (all chars matched), add `(r,c)` to results. Each DFS is independent — board restored fully between starting cells. Use in-place `'#'` marking within a single DFS call.

> [!note]- Python Solution
> ```python
> def find_word_occurrences(board, word):
>     m, n = len(board), len(board[0])
>     results = []
>     directions = ((0, 1), (0, -1), (1, 0), (-1, 0))
>
>     def dfs(r, c, i):
>         if i == len(word):
>             return True
>         if not (0 <= r < m and 0 <= c < n):
>             return False
>         if board[r][c] != word[i]:
>             return False
>         tmp = board[r][c]
>         board[r][c] = '#'
>         found = False
>         for dr, dc in directions:
>             if dfs(r + dr, c + dc, i + 1):
>                 found = True
>                 break
>         board[r][c] = tmp
>         return found
>
>     for r in range(m):
>         for c in range(n):
>             if dfs(r, c, 0):
>                 results.append((r, c))
>     return results
> ```

> [!success] Complexity
> O(m · n · 4^L) where L = len(word); O(L) recursion depth per starting cell.

> [!tip] Alternatives
> Trie-based (Word Search II) if searching for multiple words simultaneously. Frequency pruning: if board character counts can't satisfy word character counts, skip entirely.

---

## Advanced Backtracking

### N-Queens II (Count Only) `🎯 T2`

> [!example] Problem
> The n-queens puzzle is the problem of placing n queens on an n x n chessboard such that no two queens attack each other.
> Given an integer n, return the number of distinct solutions to the n-queens puzzle.
> 
> **Example 1:**
> ```
> Input: n = 4
> Output: 2
> Explanation: There are two distinct solutions to the 4-queens puzzle as shown.
> ```
> 
> **Example 2:**
> ```
> Input: n = 1
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= n <= 9

> [!info] Approach
> Same algorithm as N-Queens but without board construction or path copying — just increment a counter at the leaf. The absence of O(n^2) board copying makes each leaf O(1) instead of O(n^2), which matters for large n. Backtrack row by row; use three integer bitmasks for columns, diagonals, anti-diagonals. At each row, iterate valid column positions using bitmask operations. Bitmask trick: valid columns = `((1<<n) - 1) & ~(cols | diags | anti_diags)`. Extract LSB: `pos = available & (-available)`. Iterate: `available &= available - 1`.

> [!note]- Python Solution
> ```python
> def total_n_queens(n):
>     count = 0
>     limit = (1 << n) - 1  # n lowest bits set
> 
>     def backtrack(cols, diags, anti_diags):
>         nonlocal count
>         if cols == limit:
>             count += 1
>             return
>         available = limit & ~(cols | diags | anti_diags)
>         while available:
>             pos = available & (-available)  # isolate lowest set bit
>             available &= available - 1       # clear lowest set bit
>             backtrack(cols | pos,
>                (diags | pos) << 1,
>                (anti_diags | pos) >> 1)
> 
>     backtrack(0, 0, 0)
>     return count
> ```

> [!success] Complexity
> O(n!) upper bound; bitmask operations are O(1) per step. Space O(n) recursion depth.

> [!tip] Alternatives
> Same set-based approach as N-Queens I but skip board construction — marginally slower than bitmask due to set overhead. For n ≤ 15, results can be hardcoded (OEIS A000170).

---

### Word Break (Decision — Backtracking + Memo) `🎯 T2`

> [!example] Problem
> Given a string s and a dictionary of strings wordDict, return true if s can be segmented into a space-separated sequence of one or more dictionary words.
> Note that the same word in the dictionary may be reused multiple times in the segmentation.
> 
> **Example 1:**
> ```
> Input: s = "leetcode", wordDict = ["leet","code"]
> Output: true
> Explanation: Return true because "leetcode" can be segmented as "leet code".
> ```
> 
> **Example 2:**
> ```
> Input: s = "applepenapple", wordDict = ["apple","pen"]
> Output: true
> Explanation: Return true because "applepenapple" can be segmented as "apple pen apple".
> Note that you are allowed to reuse a dictionary word.
> ```
> 
> **Example 3:**
> ```
> Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
> Output: false
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 300
> - 1 <= wordDict.length <= 1000
> - 1 <= wordDict[i].length <= 20
> - s and wordDict[i] consist of only lowercase English letters.
> - All the strings of wordDict are unique.

> [!info] Approach
> At each position, try every dictionary word as the next segment. Naive recursion re-solves the same suffix repeatedly. Memoization on the start index reduces it to O(n^2 · L) where L = max word length. `backtrack(start)` returns True if `s[start:]` can be fully segmented. For each word in the dictionary that matches `s[start:start+len(word)]`, recurse on `start+len(word)`. Cache False results to avoid re-exploration. Check only words in the dictionary (not all prefixes). Short-circuit on first True. BFS or DP are preferred in interviews.

> [!note]- Python Solution
> ```python
> def word_break_decision(s, wordDict):
>     word_set = set(wordDict)
>     max_len = max(len(w) for w in word_set) if word_set else 0
>     memo = {}
> 
>     def backtrack(start):
>         if start == len(s):
>             return True
>         if start in memo:
>             return memo[start]
>         for end in range(start + 1, min(start + max_len, len(s)) + 1):
>             if s[start:end] in word_set and backtrack(end):
>                 memo[start] = True
>                 return True
>         memo[start] = False
>         return False
> 
>     return backtrack(0)
> ```

> [!success] Complexity
> O(n · max_len) states × O(max_len) per transition = O(n · max_len^2); O(n) memo space.

> [!tip] Alternatives
> BFS: queue of reachable positions — O(n · |dict|), simpler. DP bottom-up: `dp[i] = any(dp[i-len(w)] and s[i-len(w):i] == w)` — same complexity. Trie for O(1) prefix lookup.

---

### Generate All Valid IP Addresses (Generalized Segmentation)

> [!example] Problem
> Same as Restore IP Addresses above, but with explicit segment count and segment range as parameters — useful for understanding the generalizable pattern.

> [!info] Approach
> Generalizes Restore IP Addresses: given a digit string, split into exactly `k` segments each in range `[lo, hi]` with no leading zeros. Parameterized backtracking applies to many partitioning problems (CIDR, version strings). At each step, try taking 1 to `max_seg_len` characters. Validate the segment. Recurse on remainder with `k-1` segments left. Feasibility pruning bounds the remaining characters. Feasibility: `remaining_chars` must be in `[k-1, (k-1)*max_seg_len + max_seg_len]` — i.e., between 1 and `max_seg_len` per remaining segment.

> [!note]- Python Solution
> ```python
> def segment_string(s, k, lo, hi, max_val):
>     """Split s into exactly k segments, each integer in [lo, max_val], no leading zeros."""
>     result = []
>     path = []
>     max_len = len(str(max_val))
> 
>     def backtrack(start):
>         if len(path) == k:
>             if start == len(s):
>                 result.append('.'.join(path))
>             return
>         segs_left = k - len(path)
>         chars_left = len(s) - start
>         # Feasibility: each remaining segment needs 1..max_len chars
>         if chars_left < segs_left or chars_left > segs_left * max_len:
>             return
>         for length in range(1, max_len + 1):
>             if start + length > len(s):
>                 break
>             seg = s[start:start + length]
>             if len(seg) > 1 and seg[0] == '0':
>                 break
>             val = int(seg)
>             if val > max_val:
>                 break
>             if val < lo:
>                 continue
>             path.append(seg)
>             backtrack(start + length)
>             path.pop()
> 
>     backtrack(0)
>     return result
> ```

> [!success] Complexity
> O(max_val^k) bounded by feasibility window; for IP: O(3^4) = O(81). Space O(k).

> [!tip] Alternatives
> For k=4 and IP validation specifically, three explicit loops over split points are O(n^3) but typically simpler in interviews. This parameterized version is better for system design or templating.

---

## See Also

[[recursion]] | [[dynamic-programming]] | [[trie]] | [[graph]]

---

## Backtracking — Hard Problems

### Remove Invalid Parentheses (LC 301)

> [!example] Problem
> Given a string s that contains parentheses and letters, remove the minimum number of invalid parentheses to make the input string valid.
> Return a list of unique strings that are valid with the minimum number of removals. You may return the answer in any order.
> 
> **Example 1:**
> ```
> Input: s = "()())()"
> Output: ["(())()","()()()"]
> ```
> 
> **Example 2:**
> ```
> Input: s = "(a)())()"
> Output: ["(a())()","(a)()()"]
> ```
> 
> **Example 3:**
> ```
> Input: s = ")("
> Output: [""]
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 25
> - s consists of lowercase English letters and parentheses '(' and ')'.
> - There will be at most 20 parentheses in s.

> [!info] Approach
> We need the minimum removal and all unique results. BFS layer by layer ensures we find minimum removal first: when any valid string is found at a BFS level, all strings at that level are candidates and we stop expanding. BFS from the input string. Generate all strings with one character removed. Dedup with a visited set. For each string check if it's valid. Once a valid string is found, collect all valid strings from that BFS level and return. `is_valid(s)`: count open brackets, decrement on `)`, return false if count < 0, return `count == 0` at end.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> def remove_invalid_parentheses(s):
>     def is_valid(string):
>         count = 0
>         for ch in string:
>             if ch == '(':
>                 count += 1
>             elif ch == ')':
>                 count -= 1
>                 if count < 0:
>                     return False
>         return count == 0
> >
>     visited = {s}
>     queue = deque([s])
>     result = []
>     found = False
>     while queue:
>         level_size = len(queue)
>         for _ in range(level_size):
>             curr = queue.popleft()
>             if is_valid(curr):
>                 result.append(curr)
>                 found = True
>             if not found:
>                 for i in range(len(curr)):
>                     if curr[i] in '()':
>                         next_s = curr[:i] + curr[i+1:]
>                         if next_s not in visited:
>                             visited.add(next_s)
>                             queue.append(next_s)
>         if found:
>             break
>     return result if result else ['']
> ```

> [!success] Complexity
> Time O(2^n * n) worst case (every subset of brackets tried, each validated in O(n)). Space O(2^n).

> [!tip] Alternatives
> - DFS with pruning: count the number of mismatched `(` and `)` first, then use DFS tracking how many of each have been removed so far. Prune when removals exceed the allowed count. More complex but avoids BFS's memory cost.

---



## Partition to K Equal Sum Subsets `🎯 T2`

> [!example] Problem
> Can `nums` be partitioned into k non-empty subsets with equal sums?

> [!info] Approach
> Backtracking over **buckets**: place each number (sorted descending) into one of k buckets without exceeding `target = total // k`. Three prunings make it feasible: (1) sort descending so contradictions surface early; (2) skip buckets whose current sum equals one already tried for this number — identical buckets give identical futures; (3) bail immediately if `total % k` or `max(nums) > target`.

> [!note]- Python Solution
> ```python
> def canPartitionKSubsets(nums, k):
>     total = sum(nums)
>     if total % k:
>         return False
>     target = total // k
>     nums.sort(reverse=True)
>     if nums[0] > target:
>         return False
>     buckets = [0] * k
> >
>     def dfs(i):
>         if i == len(nums):
>             return True
>         tried = set()
>         for b in range(k):
>             if buckets[b] + nums[i] <= target and buckets[b] not in tried:
>                 tried.add(buckets[b])
>                 buckets[b] += nums[i]
>                 if dfs(i + 1):
>                     return True
>                 buckets[b] -= nums[i]
>         return False
> >
>     return dfs(0)
> ```

> [!success] Complexity
> Time O(k^n) worst case, far less with pruning; Space O(n + k) recursion + buckets.

> [!tip] Follow-up
> Mention that an O(n·2ⁿ) bitmask-DP exists (`dp[mask]` = remainder in current bucket) — name it, don't implement it. The dedup-on-equal-buckets pruning is the same trick as skipping duplicate choices in Subsets II.

---
