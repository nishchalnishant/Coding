---
tags: [coding, data-structures, stack]
topic: stack
difficulty: mixed
---

# Stack Problems

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop.
> `🎯 T2` — **TIER 2 · Build Fluidity**: This file is core Tier 2 material. Know patterns cold; skip niche edge cases.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Conceptual awareness only.





---

## Stack Interview Checklist

> [!info] When to reach for a stack
> - The problem asks for the next/previous greater or smaller item.
> - The input has nested structure: parentheses, scopes, encoded strings, call logs.
> - You need to undo the most recent unresolved action: duplicates cancel, collisions, path backtracking.
> - You want to keep a monotonic property while scanning once from left to right.
> - A brute-force solution repeatedly rescans past elements and feels quadratic.

> [!tip] Edge cases to sanity-check
> - Empty input, single element, and all-equal values.
> - Strict vs non-strict comparisons (`<` vs `<=`) when duplicates exist.
> - Sentinel values or end-of-array flushing.
> - Whether the answer is an index, a value, or a distance.

## Monotonic Stack — Next Greater/Smaller

### Daily Temperatures `🎯 T2`

> [!example] Problem
> Given an array of integers temperatures represents the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature. If there is no future day for which this is possible, keep answer[i] == 0 instead.
> 
> **Example 1:**
> ```
> Input: temperatures = [73,74,75,71,69,72,76,73]
> Output: [1,1,4,2,1,1,0,0]
> ```
> 
> **Example 2:**
> ```
> Input: temperatures = [30,40,50,60]
> Output: [1,1,1,0]
> ```
> 
> **Example 3:**
> ```
> Input: temperatures = [30,60,90]
> Output: [1,1,0]
> ```
> 
> **Constraints:**
> - 1 <= temperatures.length <= 10^5
> - 30 <= temperatures[i] <= 100

> [!info] Approach
> Brute force checks every future day for each index — O(n²). We need to resolve each index exactly once. Monotonic decreasing stack of indices. When a warmer temperature arrives, all cooler pending indices on the stack have found their answer. Push index `i` onto the stack. When `temps[i] > temps[stack[-1]]`, pop and record `result[popped] = i - popped`. Stack holds indices of temperatures that haven't yet seen a warmer day.

> [!note]- Python Solution
> ```python
> def daily_temperatures(temperatures):
>     result = [0] * len(temperatures)
>     stack = []  # indices, decreasing temperature order
>     for i, t in enumerate(temperatures):
>         while stack and temperatures[stack[-1]] < t:
>             j = stack.pop()
>             result[j] = i - j
>         stack.append(i)
>     return result
> ```

> [!success] Complexity
> Time O(n) — each index pushed and popped at most once; Space O(n).

> [!tip] Alternatives
> Brute force O(n²). Sparse table for range-minimum queries — overkill here.

---

### Next Greater Element II `🎯 T2`

> [!example] Problem
> Given a circular integer array nums (i.e., the next element of nums[nums.length - 1] is nums[0]), return the next greater number for every element in nums.
> The next greater number of a number x is the first greater number to its traversing-order next in the array, which means you could search circularly to find its next greater number. If it doesn't exist, return -1 for this number.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,1]
> Output: [2,-1,2]
> Explanation: The first 1's next greater number is 2; 
> The number 2 can't find next greater number. 
> The second 1's next greater number needs to search circularly, which is also 2.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,3,4,3]
> Output: [2,3,4,-1,4]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^4
> - -10^9 <= nums[i] <= 10^9

> [!info] Approach
> Circular array means element `0` might be the next greater for element `n-1`. Simulate by doubling the array conceptually. Same decreasing monotonic stack. Iterate `0..2n-1` with `i % n` for index. Only push on the first pass (`i < n`) to avoid duplicate results. Initialize `result = [-1] * n`. Iterate `2n` times. Use `i % n` to access elements. Only push `i % n` when `i < n`.

> [!note]- Python Solution
> ```python
> def next_greater_elements(nums):
>     n = len(nums)
>     result = [-1] * n
>     stack = []
>     for i in range(2 * n):
>         while stack and nums[stack[-1]] < nums[i % n]:
>             result[stack.pop()] = nums[i % n]
>         if i < n:
>             stack.append(i)
>     return result
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Brute force O(n²) with modular wrapping. No fundamentally better approach.

---

### Online Stock Span

> [!example] Problem
> Design an algorithm that collects daily price quotes for some stock and returns the span of that stock's price for the current day.
> The span of the stock's price in one day is the maximum number of consecutive days (starting from that day and going backward) for which the stock price was less than or equal to the price of that day.
> Implement the StockSpanner class
> 
> **Example 1:**
> ```
> Input
> ["StockSpanner", "next", "next", "next", "next", "next", "next", "next"]
> [[], [100], [80], [60], [70], [60], [75], [85]]
> Output
> [null, 1, 1, 1, 2, 1, 4, 6]
> 
> Explanation
> StockSpanner stockSpanner = new StockSpanner();
> stockSpanner.next(100); // return 1
> stockSpanner.next(80);  // return 1
> stockSpanner.next(60);  // return 1
> stockSpanner.next(70);  // return 2
> stockSpanner.next(60);  // return 1
> stockSpanner.next(75);  // return 4, because the last 4 prices (including today's price of 75) were less than or equal to today's price.
> stockSpanner.next(85);  // return 6
> ```
> 
> **Constraints:**
> - 1 <= price <= 10^5
> - At most 10^4 calls will be made to next.

> [!info] Approach
> Naively scan backwards each day — O(n) per call, O(n²) total. We need O(1) amortized. Monotonic decreasing stack of `(price, span)` tuples. When a new price arrives that's >= stack top, we absorb the top's span (it was already contiguous and all ≤ current). Pop all `(p, s)` where `p <= current_price`, accumulating their spans. Push `(current_price, accumulated_span + 1)`.

> [!note]- Python Solution
> ```python
> class StockSpanner:
>     def __init__(self):
>         self._stack: list[tuple[int, int]] = []  # (price, span)
> >
>     def next(self, price):
>         span = 1
>         while self._stack and self._stack[-1][0] <= price:
>             span += self._stack.pop()[1]
>         self._stack.append((price, span))
>         return span
> ```

> [!success] Complexity
> Time O(1) amortized per call (each price pushed/popped once); Space O(n).

> [!tip] Alternatives
> Brute force scan backwards each call — O(n) per call. No better amortized approach.

---

### Sum of Subarray Minimums

> [!example] Problem
> Given an array of integers arr, find the sum of min(b), where b ranges over every (contiguous) subarray of arr. Since the answer may be large, return the answer modulo 109 + 7.
> 
> **Example 1:**
> ```
> Input: arr = [3,1,2,4]
> Output: 17
> Explanation: 
> Subarrays are [3], [1], [2], [4], [3,1], [1,2], [2,4], [3,1,2], [1,2,4], [3,1,2,4]. 
> Minimums are 3, 1, 2, 4, 1, 1, 2, 1, 1, 1.
> Sum is 17.
> ```
> 
> **Example 2:**
> ```
> Input: arr = [11,81,94,43,3]
> Output: 444
> ```
> 
> **Constraints:**
> - 1 <= arr.length <= 3 * 10^4
> - 1 <= arr[i] <= 3 * 10^4

> [!info] Approach
> Enumerate all subarrays — O(n²) or O(n³). Instead, find for each element how many subarrays it is the minimum of. For element `arr[i]`, find `left[i]` = number of elements to the left where `arr[i]` is the minimum (stopping at the previous smaller), and `right[i]` = same for right. Contribution = `arr[i] * left[i] * right[i]`. Use monotonic increasing stack twice (or once with careful boundary tracking). Left boundary: strict `<` comparison; right boundary: `<=` to avoid double-counting equal elements.

> [!note]- Python Solution
> ```python
> def sum_subarray_mins(arr):
>     MOD = 10**9 + 7
>     n = len(arr)
>     left = [0] * n   # distance to previous smaller element
>     right = [0] * n  # distance to next smaller or equal element
>     stack = []
> >
>     # Left: how far left can arr[i] be the minimum (strict <)
>     for i in range(n):
>         while stack and arr[stack[-1]] >= arr[i]:
>             stack.pop()
>         left[i] = i - stack[-1] if stack else i + 1
>         stack.append(i)
> >
>     stack.clear()
>     # Right: how far right can arr[i] be the minimum (<=, strict to avoid double count)
>     for i in range(n - 1, -1, -1):
>         while stack and arr[stack[-1]] > arr[i]:
>             stack.pop()
>         right[i] = stack[-1] - i if stack else n - i
>         stack.append(i)
> >
>     return sum(arr[i] * left[i] * right[i] for i in range(n)) % MOD
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> DP with monotonic stack in one pass — possible but trickier to reason about. The two-pass approach above is clearer.

---

## Monotonic Stack — Histogram / Rectangle

### Largest Rectangle in Histogram `🎯 T2`

> [!example] Problem
> Given an array of integers heights representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.
> 
> **Example 1:**
> ```
> Input: heights = [2,1,5,6,2,3]
> Output: 10
> Explanation: The above is a histogram where width of each bar is 1.
> The largest rectangle is shown in the red area, which has an area = 10 units.
> ```
> 
> **Example 2:**
> ```
> Input: heights = [2,4]
> Output: 4
> ```
> 
> **Constraints:**
> - 1 <= heights.length <= 10^5
> - 0 <= heights[i] <= 10^4

> [!info] Approach
> For each bar as the height of the rectangle, the width extends left and right until a shorter bar is hit. Finding those boundaries naively is O(n) each. Monotonic increasing stack of indices. When a bar shorter than the stack top arrives, the top bar's right boundary has been found — compute area. Append sentinel `0` to flush the stack. On pop, `height = heights[popped]`. Width = `i - stack[-1] - 1` if stack is non-empty, else `i` (the bar is the global minimum so far).

> [!note]- Python Solution
> ```python
> def largest_rectangle_area(heights):
>     stack = []  # increasing stack of indices
>     best = 0
>     for i, h in enumerate(heights + [0]):  # sentinel 0 flushes stack
>         while stack and heights[stack[-1]] > h:
>             height = heights[stack.pop()]
>             width = i if not stack else i - stack[-1] - 1
>             best = max(best, height * width)
>         stack.append(i)
>     return best
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Divide and conquer O(n log n) average — find minimum bar, recurse on left and right. Brute force O(n²).

---

### Maximal Rectangle `🎯 T2`

> [!example] Problem
> Given a rows x cols binary matrix filled with 0's and 1's, find the largest rectangle containing only 1's and return its area.
> 
> **Example 1:**
> ```
> Input: matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]
> Output: 6
> Explanation: The maximal rectangle is shown in the above picture.
> ```
> 
> **Example 2:**
> ```
> Input: matrix = [["0"]]
> Output: 0
> ```
> 
> **Example 3:**
> ```
> Input: matrix = [["1"]]
> Output: 1
> ```
> 
> **Constraints:**
> - rows == matrix.length
> - cols == matrix[i].length
> - 1 <= row, cols <= 200
> - matrix[i][j] is '0' or '1'.

> [!info] Approach
> Reduce to Largest Rectangle in Histogram. Each row defines a histogram where `heights[j]` = consecutive '1's above and including `matrix[row][j]`. Maintain a `heights` array. For each row, update heights (reset to 0 on '0', increment on '1'). Apply the histogram algorithm per row. `heights[j] = heights[j] + 1 if matrix[row][j] == '1' else 0`. Run `largest_rectangle_area(heights)` for each row.

> [!note]- Python Solution
> ```python
> def maximal_rectangle(matrix):
>     if not matrix or not matrix[0]:
>         return 0
>     cols = len(matrix[0])
>     heights = [0] * cols
>     best = 0
>     for row in matrix:
>         for j in range(cols):
>             heights[j] = heights[j] + 1 if row[j] == '1' else 0
>         best = max(best, largest_rectangle_area(heights))
>     return best
> >
> def largest_rectangle_area(heights):
>     stack = []
>     best = 0
>     for i, h in enumerate(heights + [0]):
>         while stack and heights[stack[-1]] > h:
>             height = heights[stack.pop()]
>             width = i if not stack else i - stack[-1] - 1
>             best = max(best, height * width)
>         stack.append(i)
>     return best
> ```

> [!success] Complexity
> Time O(rows * cols); Space O(cols).

> [!tip] Alternatives
> DP with `left[j]`, `right[j]`, `height[j]` arrays — O(rows * cols), same complexity without the stack. Useful to know for follow-up.

---

### Trapping Rain Water (stack approach) `⚡ T1`

> [!example] Problem
> Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.
> 
> **Example 1:**
> ```
> Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
> Output: 6
> Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.
> ```
> 
> **Example 2:**
> ```
> Input: height = [4,2,0,3,2,5]
> Output: 9
> ```
> 
> **Constraints:**
> - n == height.length
> - 1 <= n <= 2 * 10^4
> - 0 <= height[i] <= 10^5

> [!info] Approach
> Water fills valleys. Each valley is bounded by taller bars on both sides. The stack lets us process valleys as they form. Monotonic decreasing stack. When a taller bar arrives, the top of the stack is a valley bottom. Water height = `min(left_bar, current_bar) - valley_bottom_height`. Width = distance between left and current bar minus 1. Push indices onto a decreasing stack. On pop (taller bar arrived), compute bounded water above the popped bar.

> [!note]- Python Solution
> ```python
> def trap(height):
>     stack = []
>     water = 0
>     for i, h in enumerate(height):
>         while stack and height[stack[-1]] < h:
>             bottom = stack.pop()
>             if not stack:
>                 break
>             left = stack[-1]
>             bounded_height = min(height[left], h) - height[bottom]
>             water += bounded_height * (i - left - 1)
>         stack.append(i)
>     return water
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Two-pointer O(n) time O(1) space — `left_max` and `right_max` pointers. Simpler to code in practice; stack version better for explaining the "why".

---

## Valid Parentheses / Nesting

### Valid Parentheses `🎯 T2`

> [!example] Problem
> Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.
> An input string is valid if
> 
> **Example 1:**
> ```
> Input: s = "()"
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: s = "()[]{}"
> Output: true
> ```
> 
> **Example 3:**
> ```
> Input: s = "(]"
> Output: false
> ```
> 
> **Example 4:**
> ```
> Input: s = "([])"
> Output: true
> ```
> 
> **Example 5:**
> ```
> Input: s = "([)]"
> Output: false
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^4
> - s consists of parentheses only '()[]{}'.

> [!info] Approach
> LIFO — the most recently opened bracket must be the next closed. Push opening brackets. On each closing bracket, pop the stack and verify it matches. Map `')' → '('`, etc. If stack is empty when closing bracket arrives, or top doesn't match, return `False`. Valid iff stack is empty at end.

> [!note]- Python Solution
> ```python
> def is_valid(s):
>     stack = []
>     pairs = {')': '(', ']': '[', '}': '{'}
>     for ch in s:
>         if ch in '([{':
>             stack.append(ch)
>         elif not stack or stack[-1] != pairs[ch]:
>             return False
>         else:
>             stack.pop()
>     return not stack
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Counter approach fails — `([)]` has equal counts but is invalid. Stack is necessary for order.

---

### Remove All Adjacent Duplicates in String

> [!example] Problem
> You are given a string s consisting of lowercase English letters. A duplicate removal consists of choosing two adjacent and equal letters and removing them.
> We repeatedly make duplicate removals on s until we no longer can.
> Return the final string after all such duplicate removals have been made. It can be proven that the answer is unique.
> 
> **Example 1:**
> ```
> Input: s = "abbaca"
> Output: "ca"
> Explanation: 
> For example, in "abbaca" we could remove "bb" since the letters are adjacent and equal, and this is the only possible move.  The result of this move is that the string is "aaca", of which only "aa" is possible, so the final string is "ca".
> ```
> 
> **Example 2:**
> ```
> Input: s = "azxxzy"
> Output: "ay"
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^5
> - s consists of lowercase English letters.

> [!info] Approach
> Removing one pair can create new adjacent duplicates — process must cascade. Stack handles this naturally. Push characters. If the new character equals the stack top, pop (they cancel). Otherwise push. Result is remaining stack joined. Linear scan. Maintain stack. At each character, cancel with top if equal. Analogous to bracket matching.

> [!note]- Python Solution
> ```python
> def remove_duplicates(s):
>     stack = []
>     for ch in s:
>         if stack and stack[-1] == ch:
>             stack.pop()
>         else:
>             stack.append(ch)
>     return ''.join(stack)
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> String simulation with repeated passes — O(n²) in worst case. Stack is optimal.

---

### Remove K Digits `🎯 T2`

> [!example] Problem
> Given string num representing a non-negative integer num, and an integer k, return the smallest possible integer after removing k digits from num.
> 
> **Example 1:**
> ```
> Input: num = "1432219", k = 3
> Output: "1219"
> Explanation: Remove the three digits 4, 3, and 2 to form the new number 1219 which is the smallest.
> ```
> 
> **Example 2:**
> ```
> Input: num = "10200", k = 1
> Output: "200"
> Explanation: Remove the leading 1 and the number is 200. Note that the output must not contain leading zeroes.
> ```
> 
> **Example 3:**
> ```
> Input: num = "10", k = 2
> Output: "0"
> Explanation: Remove all the digits from the number and it is left with nothing which is 0.
> ```
> 
> **Constraints:**
> - 1 <= k <= num.length <= 10^5
> - num consists of only digits.
> - num does not have any leading zeros except for the zero itself.

> [!info] Approach
> Greedy — to minimize, remove a digit when the next digit is smaller (it would be more beneficial at that position). Monotonic increasing stack. Pop the top when it's larger than the current digit and `k > 0`. Build the stack left to right. Pop larger elements while `k > 0`. If `k` still > 0 after the loop, trim last `k` digits from the stack (which is already sorted ascending). Strip leading zeros.

> [!note]- Python Solution
> ```python
> def remove_k_digits(num, k):
>     stack = []
>     for d in num:
>         while k > 0 and stack and stack[-1] > d:
>             stack.pop()
>             k -= 1
>         stack.append(d)
>     # If k > 0, remove from the end (stack is already non-decreasing)
>     stack = stack[:-k] if k else stack
>     result = ''.join(stack).lstrip('0')
>     return result or '0'
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> No fundamentally better approach. The greedy monotonic stack is O(n) optimal.

---

## Stack Design

### Min Stack `🎯 T2`

> [!example] Problem
> Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.
> Implement the MinStack class:
> You must implement a solution with O(1) time complexity for each function.
> 
> **Example 1:**
> ```
> Input
> ["MinStack","push","push","push","getMin","pop","top","getMin"]
> [[],[-2],[0],[-3],[],[],[],[]]
> 
> Output
> [null,null,null,null,-3,null,0,-2]
> 
> Explanation
> MinStack minStack = new MinStack();
> minStack.push(-2);
> minStack.push(0);
> minStack.push(-3);
> minStack.getMin(); // return -3
> minStack.pop();
> minStack.top();    // return 0
> minStack.getMin(); // return -2
> ```
> 
> **Constraints:**
> - -2^{31} <= val <= 2^{31} - 1
> - Methods pop, top and getMin operations will always be called on non-empty stacks.
> - At most 3 * 10^4 calls will be made to push, pop, top, and getMin.

> [!info] Approach
> A regular stack loses track of the minimum after pops. We need the minimum at every stack depth. Parallel `min_stack` where `min_stack[i]` = minimum of all elements in `stack[0..i]`. Both stacks stay synchronized. On push, `min_stack` pushes `min(val, min_stack[-1])`. On pop, both stacks pop. `get_min` returns `min_stack[-1]`.

> [!note]- Python Solution
> ```python
> class MinStack:
>     def __init__(self):
>         self._stack: list[int] = []
>         self._min_stack: list[int] = []
> >
>     def push(self, val):
>         self._stack.append(val)
>         current_min = val if not self._min_stack else min(val, self._min_stack[-1])
>         self._min_stack.append(current_min)
> >
>     def pop(self):
>         self._stack.pop()
>         self._min_stack.pop()
> >
>     def top(self):
>         return self._stack[-1]
> >
>     def get_min(self):
>         return self._min_stack[-1]
> ```

> [!success] Complexity
> Time O(1) all ops; Space O(n).

> [!tip] Alternatives
> Store `(val, current_min)` tuples in a single stack — same complexity, single structure. Saves one stack at the cost of slightly less readable code.

---

### Maximum Frequency Stack

> [!example] Problem
> Design a stack-like data structure to push elements to the stack and pop the most frequent element from the stack.
> Implement the FreqStack class
> 
> **Example 1:**
> ```
> Input
> ["FreqStack", "push", "push", "push", "push", "push", "push", "pop", "pop", "pop", "pop"]
> [[], [5], [7], [5], [7], [4], [5], [], [], [], []]
> Output
> [null, null, null, null, null, null, null, 5, 7, 5, 4]
> 
> Explanation
> FreqStack freqStack = new FreqStack();
> freqStack.push(5); // The stack is [5]
> freqStack.push(7); // The stack is [5,7]
> freqStack.push(5); // The stack is [5,7,5]
> freqStack.push(7); // The stack is [5,7,5,7]
> freqStack.push(4); // The stack is [5,7,5,7,4]
> freqStack.push(5); // The stack is [5,7,5,7,4,5]
> freqStack.pop();   // return 5, as 5 is the most frequent. The stack becomes [5,7,5,7,4].
> freqStack.pop();   // return 7, as 5 and 7 is the most frequent, but 7 is closest to the top. The stack becomes [5,7,5,4].
> freqStack.pop();   // return 5, as 5 is the most frequent. The stack becomes [5,7,4].
> freqStack.pop();   // return 4, as 4, 5 and 7 is the most frequent, but 4 is closest to the top. The stack becomes [5,7].
> ```
> 
> **Constraints:**
> - 0 <= val <= 10^9
> - At most 2 * 10^4 calls will be made to push and pop.
> - It is guaranteed that there will be at least one element in the stack before calling pop.

> [!info] Approach
> Standard stack gives LIFO; we want frequency-priority with LIFO for ties. Two maps: `val → frequency` and `freq → [stack of vals at that frequency]`. Track `max_freq`. Push: increment `freq[val]`, append `val` to `group[freq[val]]`, update `max_freq`. Pop: take from `group[max_freq]`, decrement `freq[val]`, decrement `max_freq` if the bucket is now empty.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> >
> class FreqStack:
>     def __init__(self):
>         self._freq: dict[int, int] = defaultdict(int)
>         self._group: dict[int, list[int]] = defaultdict(list)
>         self._max_freq = 0
> >
>     def push(self, val):
>         self._freq[val] += 1
>         f = self._freq[val]
>         self._max_freq = max(self._max_freq, f)
>         self._group[f].append(val)
> >
>     def pop(self):
>         val = self._group[self._max_freq].pop()
>         self._freq[val] -= 1
>         if not self._group[self._max_freq]:
>             self._max_freq -= 1
>         return val
> ```

> [!success] Complexity
> Time O(1) push and pop; Space O(n).

> [!tip] Alternatives
> Priority queue — O(log n) per op, doesn't handle ties by recency correctly without careful tuple design.

---

## Queue from Stacks

### Implement Queue using Stacks

> [!example] Problem
> Implement a first in first out (FIFO) queue using only two stacks. The implemented queue should support all the functions of a normal queue (push, peek, pop, and empty).
> Implement the MyQueue class:
> Notes
> 
> **Example 1:**
> ```
> Input
> ["MyQueue", "push", "push", "peek", "pop", "empty"]
> [[], [1], [2], [], [], []]
> Output
> [null, null, null, 1, 1, false]
> 
> Explanation
> MyQueue myQueue = new MyQueue();
> myQueue.push(1); // queue is: [1]
> myQueue.push(2); // queue is: [1, 2] (leftmost is front of the queue)
> myQueue.peek(); // return 1
> myQueue.pop(); // return 1, queue is [2]
> myQueue.empty(); // return false
> ```
> 
> **Constraints:**
> - 1 <= x <= 9
> - At most 100 calls will be made to push, pop, peek, and empty.
> - All the calls to pop and peek are valid.

> [!info] Approach
> Stack is LIFO; reversing the stack gives FIFO order. One stack for input, one for output. `in_stack` receives all pushes. `out_stack` is lazily populated from `in_stack` when needed. Reversing `in_stack` into `out_stack` makes the oldest element accessible at the top. `push` appends to `in_stack`. `pop`/`peek`: if `out_stack` is empty, move all of `in_stack` to `out_stack` (reversal). Then operate on `out_stack`. Amortized O(1).

> [!note]- Python Solution
> ```python
> class MyQueue:
>     def __init__(self):
>         self._in: list[int] = []
>         self._out: list[int] = []
> >
>     def push(self, x):
>         self._in.append(x)
> >
>     def _transfer(self):
>         if not self._out:
>             while self._in:
>                 self._out.append(self._in.pop())
> >
>     def pop(self):
>         self._transfer()
>         return self._out.pop()
> >
>     def peek(self):
>         self._transfer()
>         return self._out[-1]
> >
>     def empty(self):
>         return not self._in and not self._out
> ```

> [!success] Complexity
> Time O(1) amortized per op; Space O(n).

> [!tip] Alternatives
> Single stack with recursion for dequeue — O(n) each dequeue. Double-transfer is the canonical approach.

---

### Validate Stack Sequences

> [!example] Problem
> Given two integer arrays pushed and popped each with distinct values, return true if this could have been the result of a sequence of push and pop operations on an initially empty stack, or false otherwise.
> 
> **Example 1:**
> ```
> Input: pushed = [1,2,3,4,5], popped = [4,5,3,2,1]
> Output: true
> Explanation: We might do the following sequence:
> push(1), push(2), push(3), push(4),
> pop() -> 4,
> push(5),
> pop() -> 5, pop() -> 3, pop() -> 2, pop() -> 1
> ```
> 
> **Example 2:**
> ```
> Input: pushed = [1,2,3,4,5], popped = [4,3,5,1,2]
> Output: false
> Explanation: 1 cannot be popped before 2.
> ```
> 
> **Constraints:**
> - 1 <= pushed.length <= 1000
> - 0 <= pushed[i] <= 1000
> - All the elements of pushed are unique.
> - popped.length == pushed.length
> - popped is a permutation of pushed.

> [!info] Approach
> Simulate the push sequence and greedily pop when the top matches the next expected pop. Simulate with an explicit stack. Push elements from `pushed`. After each push, greedily pop while top matches `popped[j]`. Maintain pointer `j` into `popped`. After pushing `pushed[i]`, pop while `stack and stack[-1] == popped[j]`, incrementing `j`. Valid iff stack is empty at end.

> [!note]- Python Solution
> ```python
> def validate_stack_sequences(pushed, popped):
>     stack = []
>     j = 0
>     for val in pushed:
>         stack.append(val)
>         while stack and stack[-1] == popped[j]:
>             stack.pop()
>             j += 1
>     return not stack
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> No better approach — the greedy simulation is necessary and sufficient.

---

## Expression Evaluation

### Evaluate Reverse Polish Notation `🎯 T2`

> [!example] Problem
> You are given an array of strings tokens that represents an arithmetic expression in a Reverse Polish Notation.
> Evaluate the expression. Return an integer that represents the value of the expression.
> Note that
> 
> **Example 1:**
> ```
> Input: tokens = ["2","1","+","3","*"]
> Output: 9
> Explanation: ((2 + 1) * 3) = 9
> ```
> 
> **Example 2:**
> ```
> Input: tokens = ["4","13","5","/","+"]
> Output: 6
> Explanation: (4 + (13 / 5)) = 6
> ```
> 
> **Example 3:**
> ```
> Input: tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
> Output: 22
> Explanation: ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
> = ((10 * (6 / (12 * -11))) + 17) + 5
> = ((10 * (6 / -132)) + 17) + 5
> = ((10 * 0) + 17) + 5
> = (0 + 17) + 5
> = 17 + 5
> = 22
> ```
> 
> **Constraints:**
> - 1 <= tokens.length <= 10^4
> - tokens[i] is either an operator: "+", "-", "*", or "/", or an integer in the range [-200, 200].

> [!info] Approach
> RPN eliminates parentheses — operators apply to the two most recently seen operands. LIFO matches this. Operand stack. Push numbers. On operator, pop two operands, apply, push result. Pop `b` then `a` (order matters for `-` and `/`). Apply operator. Push result. Division truncates toward zero: `int(a / b)` not `a // b` (handles negatives).

> [!note]- Python Solution
> ```python
> def eval_rpn(tokens):
>     stack = []
>     ops = {'+', '-', '*', '/'}
>     for token in tokens:
>         if token in ops:
>             b, a = stack.pop(), stack.pop()
>             if token == '+': stack.append(a + b)
>             elif token == '-': stack.append(a - b)
>             elif token == '*': stack.append(a * b)
>             else: stack.append(int(a / b))  # truncate toward zero
>         else:
>             stack.append(int(token))
>     return stack[0]
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Recursive evaluation — same complexity but harder to implement iteratively for deeply nested expressions.

---

### Basic Calculator I

> [!example] Problem
> Given a string s representing a valid expression, implement a basic calculator to evaluate it, and return the result of the evaluation.
> Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as eval().
> 
> **Example 1:**
> ```
> Input: s = "1 + 1"
> Output: 2
> ```
> 
> **Example 2:**
> ```
> Input: s = " 2-1 + 2 "
> Output: 3
> ```
> 
> **Example 3:**
> ```
> Input: s = "(1+(4+5+2)-3)+(6+8)"
> Output: 23
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 3 * 10^5
> - s consists of digits, '+', '-', '(', ')', and ' '.
> - s represents a valid expression.
> - '+' is not used as a unary operation (i.e., "+1" and "+(2 + 3)" is invalid).
> - '-' could be used as a unary operation (i.e., "-1" and "-(2 + 3)" is valid).
> - There will be no two consecutive operators in the input.
> - Every number and running calculation will fit in a signed 32-bit integer.

> [!info] Approach
> Parentheses introduce nested scope. Stack saves the running result and sign when entering a new scope. Track `result` and `sign` (+1 or -1). On `(`: push `(result, sign)` and reset. On `)`: pop and combine `sign_before * inner_result + outer_result`. Parse multi-digit numbers. Accumulate into `result` using current `sign`. Handle `(` and `)` for scope management.

> [!note]- Python Solution
> ```python
> def calculate_i(s):
>     stack = []
>     result = 0
>     sign = 1
>     i = 0
>     while i < len(s):
>         ch = s[i]
>         if ch.isdigit():
>             num = 0
>             while i < len(s) and s[i].isdigit():
>                 num = num * 10 + int(s[i])
>                 i += 1
>             result += sign * num
>             continue
>         elif ch == '+':
>             sign = 1
>         elif ch == '-':
>             sign = -1
>         elif ch == '(':
>             stack.append(result)
>             stack.append(sign)
>             result = 0
>             sign = 1
>         elif ch == ')':
>             result = stack.pop() * result + stack.pop()
>         i += 1
>     return result
> ```

> [!success] Complexity
> Time O(n); Space O(n) for nested parentheses.

> [!tip] Alternatives
> Recursive descent — cleaner structure but risk of call-stack overflow on deep nesting.

---

### Basic Calculator II

> [!example] Problem
> Given a string s which represents an expression, evaluate this expression and return its value.
> The integer division should truncate toward zero.
> You may assume that the given expression is always valid. All intermediate results will be in the range of [-231, 231 - 1].
> Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as eval().
> 
> **Example 1:**
> ```
> Input: s = "3+2*2"
> Output: 7
> ```
> 
> **Example 2:**
> ```
> Input: s = " 3/2 "
> Output: 1
> ```
> 
> **Example 3:**
> ```
> Input: s = " 3+5 / 2 "
> Output: 5
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 3 * 10^5
> - s consists of integers and operators ('+', '-', '*', '/') separated by some number of spaces.
> - s represents a valid expression.
> - All the integers in the expression are non-negative integers in the range [0, 2^{31} - 1].
> - The answer is guaranteed to fit in a 32-bit integer.

> [!info] Approach
> `*` and `/` have higher precedence than `+` and `-`. Process high-precedence operators immediately; defer low-precedence to a final sum. Stack of terms to be summed. Track `prev_op`. On `+`/`-`, push `sign * num`. On `*`/`/`, pop top, apply, push result back. Parse number, apply `prev_op` with stack. Default `prev_op = '+'`. Final answer = sum of stack.

> [!note]- Python Solution
> ```python
> def calculate_ii(s):
>     stack = []
>     prev_op = '+'
>     num = 0
>     for i, ch in enumerate(s):
>         if ch.isdigit():
>             num = num * 10 + int(ch)
>         if (not ch.isdigit() and ch != ' ') or i == len(s) - 1:
>             if prev_op == '+':
>                 stack.append(num)
>             elif prev_op == '-':
>                 stack.append(-num)
>             elif prev_op == '*':
>                 stack.append(stack.pop() * num)
>             elif prev_op == '/':
>                 stack.append(int(stack.pop() / num))  # truncate toward zero
>             prev_op = ch
>             num = 0
>     return sum(stack)
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Evaluate left to right tracking just two variables — possible only without mixed precedence.

---

### Basic Calculator III

> [!example] Problem
> Given a string s representing a valid expression, implement a basic calculator to evaluate it, and return the result of the evaluation.
> Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as eval().
> 
> **Example 1:**
> ```
> Input: s = "1 + 1"
> Output: 2
> ```
> 
> **Example 2:**
> ```
> Input: s = " 2-1 + 2 "
> Output: 3
> ```
> 
> **Example 3:**
> ```
> Input: s = "(1+(4+5+2)-3)+(6+8)"
> Output: 23
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 3 * 10^5
> - s consists of digits, '+', '-', '(', ')', and ' '.
> - s represents a valid expression.
> - '+' is not used as a unary operation (i.e., "+1" and "+(2 + 3)" is invalid).
> - '-' could be used as a unary operation (i.e., "-1" and "-(2 + 3)" is valid).
> - There will be no two consecutive operators in the input.
> - Every number and running calculation will fit in a signed 32-bit integer.

> [!info] Approach
> Combination of I (parentheses) and II (precedence). Parentheses require scope management; precedence requires deferred addition. Recursive approach: when `(` is encountered, recursively evaluate the sub-expression inside until `)`, then continue with the result. Implement a helper that processes until end or `)`. Inside, use the stack-based approach from Calculator II. On `(`, recurse for the inner expression.

> [!note]- Python Solution
> ```python
> def calculate_iii(s):
>     idx = 0
> >
>     def helper():
>         nonlocal idx
>         stack = []
>         prev_op = '+'
>         num = 0
>         while idx < len(s):
>             ch = s[idx]
>             idx += 1
>             if ch.isdigit():
>                 num = num * 10 + int(ch)
>             elif ch == '(':
>                 num = helper()
>             if (not ch.isdigit() and ch != ' ') or idx == len(s):
>                 if prev_op == '+': stack.append(num)
>                 elif prev_op == '-': stack.append(-num)
>                 elif prev_op == '*': stack.append(stack.pop() * num)
>                 elif prev_op == '/': stack.append(int(stack.pop() / num))
>                 prev_op = ch
>                 num = 0
>             if ch == ')':
>                 break
>         return sum(stack)
> >
>     return helper()
> ```

> [!success] Complexity
> Time O(n); Space O(n) recursion depth + stack.

> [!tip] Alternatives
> Fully iterative with an explicit call stack — possible but significantly more complex code.

---

## Simulation / Other

### Exclusive Time of Functions

> [!example] Problem
> On a single-threaded CPU, we execute a program containing n functions. Each function has a unique ID between 0 and n-1.
> Function calls are stored in a call stack: when a function call starts, its ID is pushed onto the stack, and when a function call ends, its ID is popped off the stack. The function whose ID is at the top of the stack is the current function being executed. Each time a function starts or ends, we write a log with the ID, whether it started or ended, and the timestamp.
> You are given a list logs, where logs[i] represents the ith log message formatted as a string "{function_id}:{"start" | "end"}:{timestamp}". For example, "0:start:3" means a function call with function ID 0 started at the beginning of timestamp 3, and "1:end:2" means a function call with function ID 1 ended at the end of timestamp 2. Note that a function can be called multiple times, possibly recursively.
> A function's exclusive time is the sum of execution times for all function calls in the program. For example, if a function is called twice, one call executing for 2 time units and another call executing for 1 time unit, the exclusive time is 2 + 1 = 3.
> Return the exclusive time of each function in an array, where the value at the ith index represents the exclusive time for the function with ID i.
> 
> **Example 1:**
> ```
> Input: n = 2, logs = ["0:start:0","1:start:2","1:end:5","0:end:6"]
> Output: [3,4]
> Explanation:
> Function 0 starts at the beginning of time 0, then it executes 2 for units of time and reaches the end of time 1.
> Function 1 starts at the beginning of time 2, executes for 4 units of time, and ends at the end of time 5.
> Function 0 resumes execution at the beginning of time 6 and executes for 1 unit of time.
> So function 0 spends 2 + 1 = 3 units of total time executing, and function 1 spends 4 units of total time executing.
> ```
> 
> **Example 2:**
> ```
> Input: n = 1, logs = ["0:start:0","0:start:2","0:end:5","0:start:6","0:end:6","0:end:7"]
> Output: [8]
> Explanation:
> Function 0 starts at the beginning of time 0, executes for 2 units of time, and recursively calls itself.
> Function 0 (recursive call) starts at the beginning of time 2 and executes for 4 units of time.
> Function 0 (initial call) resumes execution then immediately calls itself again.
> Function 0 (2nd recursive call) starts at the beginning of time 6 and executes for 1 unit of time.
> Function 0 (initial call) resumes execution at the beginning of time 7 and executes for 1 unit of time.
> So function 0 spends 2 + 4 + 1 + 1 = 8 units of total time executing.
> ```
> 
> **Example 3:**
> ```
> Input: n = 2, logs = ["0:start:0","0:start:2","0:end:5","1:start:6","1:end:6","0:end:7"]
> Output: [7,1]
> Explanation:
> Function 0 starts at the beginning of time 0, executes for 2 units of time, and recursively calls itself.
> Function 0 (recursive call) starts at the beginning of time 2 and executes for 4 units of time.
> Function 0 (initial call) resumes execution then immediately calls function 1.
> Function 1 starts at the beginning of time 6, executes 1 unit of time, and ends at the end of time 6.
> Function 0 resumes execution at the beginning of time 6 and executes for 2 units of time.
> So function 0 spends 2 + 4 + 1 = 7 units of total time executing, and function 1 spends 1 unit of total time executing.
> ```
> 
> **Constraints:**
> - 1 <= n <= 100
> - 2 <= logs.length <= 500
> - 0 <= function_id < n
> - 0 <= timestamp <= 10^9
> - No two start events will happen at the same timestamp.
> - No two end events will happen at the same timestamp.
> - Each function has an "end" log for each "start" log.

> [!info] Approach
> Functions nest (call stack semantics). When a nested function starts, the outer function pauses. When it ends, the outer resumes. Explicit stack of `(func_id, start_time)`. On start: push. On end: pop, compute duration. Subtract this duration from the new top (the caller) to avoid double-counting. Parse each log. On `"start"`: if stack non-empty, add elapsed time to top's exclusive time. Push current. On `"end"`: pop, compute time, add to result. Update `prev_time = end + 1`.

> [!note]- Python Solution
> ```python
> def exclusive_time(n, logs):
>     result = [0] * n
>     stack = []  # stack of function ids
>     prev_time = 0
>     for log in logs:
>         fid_str, typ, time_str = log.split(':')
>         fid, t = int(fid_str), int(time_str)
>         if typ == 'start':
>             if stack:
>                 result[stack[-1]] += t - prev_time
>             stack.append(fid)
>             prev_time = t
>         else:  # end
>             result[stack.pop()] += t - prev_time + 1
>             prev_time = t + 1
>     return result
> ```

> [!success] Complexity
> Time O(m) where `m = len(logs)`; Space O(n) stack depth.

> [!tip] Alternatives
> No fundamentally different approach — call stack simulation is inherent to the problem structure.

---

### Simplify Path

> [!example] Problem
> You are given an absolute path for a Unix-style file system, which always begins with a slash '/'. Your task is to transform this absolute path into its simplified canonical path.
> The rules of a Unix-style file system are as follows:
> The simplified canonical path should follow these rules:
> Return the simplified canonical path.
> 
> **Example 1:**
> ```
> Input: path = "/home/"
> Output: "/home"
> Explanation:
> The trailing slash should be removed.
> ```
> 
> **Example 2:**
> ```
> Input: path = "/home//foo/"
> Output: "/home/foo"
> Explanation:
> Multiple consecutive slashes are replaced by a single one.
> ```
> 
> **Example 3:**
> ```
> Input: path = "/home/user/Documents/../Pictures"
> Output: "/home/user/Pictures"
> Explanation:
> A double period ".." refers to the directory up a level (the parent directory).
> ```
> 
> **Example 4:**
> ```
> Input: path = "/../"
> Output: "/"
> Explanation:
> Going one level up from the root directory is not possible.
> ```
> 
> **Example 5:**
> ```
> Input: path = "/.../a/../b/c/../d/./"
> Output: "/.../b/d"
> Explanation:
> "..." is a valid name for a directory in this problem.
> ```
> 
> **Constraints:**
> - 1 <= path.length <= 3000
> - path consists of English letters, digits, period '.', slash '/' or '_'.
> - path is a valid absolute Unix path.

> [!info] Approach
> `..` means go up one directory — pop from the path. `.` and empty tokens are no-ops. Stack of directory names. Push valid names. Pop on `..`. Ignore `.` and empty strings. Split on `/`. For each part: skip empty strings and `.`; pop on `..` (if stack non-empty); push otherwise. Join with `/` and prepend `/`.

> [!note]- Python Solution
> ```python
> def simplify_path(path):
>     stack = []
>     for part in path.split('/'):
>         if part == '..':
>             if stack:
>                 stack.pop()
>         elif part and part != '.':
>             stack.append(part)
>     return '/' + '/'.join(stack)
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> String manipulation without a stack — fragile and harder to reason about for edge cases.

---

### Baseball Game

> [!example] Problem
> You are keeping the scores for a baseball game with strange rules. At the beginning of the game, you start with an empty record.
> You are given a list of strings operations, where operations[i] is the ith operation you must apply to the record and is one of the following:
> Return the sum of all the scores on the record after applying all the operations.
> The test cases are generated such that the answer and all intermediate calculations fit in a 32-bit integer and that all operations are valid.
> 
> **Example 1:**
> ```
> Input: ops = ["5","2","C","D","+"]
> Output: 30
> Explanation:
> "5" - Add 5 to the record, record is now [5].
> "2" - Add 2 to the record, record is now [5, 2].
> "C" - Invalidate and remove the previous score, record is now [5].
> "D" - Add 2 * 5 = 10 to the record, record is now [5, 10].
> "+" - Add 5 + 10 = 15 to the record, record is now [5, 10, 15].
> The total sum is 5 + 10 + 15 = 30.
> ```
> 
> **Example 2:**
> ```
> Input: ops = ["5","-2","4","C","D","9","+","+"]
> Output: 27
> Explanation:
> "5" - Add 5 to the record, record is now [5].
> "-2" - Add -2 to the record, record is now [5, -2].
> "4" - Add 4 to the record, record is now [5, -2, 4].
> "C" - Invalidate and remove the previous score, record is now [5, -2].
> "D" - Add 2 * -2 = -4 to the record, record is now [5, -2, -4].
> "9" - Add 9 to the record, record is now [5, -2, -4, 9].
> "+" - Add -4 + 9 = 5 to the record, record is now [5, -2, -4, 9, 5].
> "+" - Add 9 + 5 = 14 to the record, record is now [5, -2, -4, 9, 5, 14].
> The total sum is 5 + -2 + -4 + 9 + 5 + 14 = 27.
> ```
> 
> **Example 3:**
> ```
> Input: ops = ["1","C"]
> Output: 0
> Explanation:
> "1" - Add 1 to the record, record is now [1].
> "C" - Invalidate and remove the previous score, record is now [].
> Since the record is empty, the total sum is 0.
> ```
> 
> **Constraints:**
> - 1 <= operations.length <= 1000
> - operations[i] is "C", "D", "+", or a string representing an integer in the range [-3 * 10^4, 3 * 10^4].
> - For operation "+", there will always be at least two previous scores on the record.
> - For operations "C" and "D", there will always be at least one previous score on the record.

> [!info] Approach
> All operations reference the top of the score history — LIFO structure. Stack of valid scores. Each operation modifies the stack top. Parse each op. Integer: push. `+`: push `stack[-1] + stack[-2]`. `D`: push `stack[-1] * 2`. `C`: pop. Sum the stack at the end.

> [!note]- Python Solution
> ```python
> def cal_points(operations):
>     stack = []
>     for op in operations:
>         if op == '+':
>             stack.append(stack[-1] + stack[-2])
>         elif op == 'D':
>             stack.append(stack[-1] * 2)
>         elif op == 'C':
>             stack.pop()
>         else:
>             stack.append(int(op))
>     return sum(stack)
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> No better approach — direct simulation is optimal.

---

### Asteroid Collision `🎯 T2`

> [!example] Problem
> We are given an array asteroids of integers representing asteroids in a row. The indices of the asteriod in the array represent their relative position in space.
> For each asteroid, the absolute value represents its size, and the sign represents its direction (positive meaning right, negative meaning left). Each asteroid moves at the same speed.
> Find out the state of the asteroids after all collisions. If two asteroids meet, the smaller one will explode. If both are the same size, both will explode. Two asteroids moving in the same direction will never meet.
> 
> **Example 1:**
> ```
> Input: asteroids = [5,10,-5]
> Output: [5,10]
> Explanation: The 10 and -5 collide resulting in 10. The 5 and 10 never collide.
> ```
> 
> **Example 2:**
> ```
> Input: asteroids = [8,-8]
> Output: []
> Explanation: The 8 and -8 collide exploding each other.
> ```
> 
> **Example 3:**
> ```
> Input: asteroids = [10,2,-5]
> Output: [10]
> Explanation: The 2 and -5 collide resulting in -5. The 10 and -5 collide resulting in 10.
> ```
> 
> **Constraints:**
> - 2 <= asteroids.length <= 10^4
> - -1000 <= asteroids[i] <= 1000
> - asteroids[i] != 0

> [!info] Approach
> Collisions only happen between a positive (right-moving) on the stack and a new negative (left-moving). Stack of survivors. Maintain a stack of surviving asteroids. A collision only occurs when `stack[-1] > 0 and asteroid < 0`. While collision conditions hold: if top is smaller, pop (top destroyed, current continues); if equal, pop and break (both destroyed); if top is larger, break (current destroyed, don't append). Use `while...else` to append only if current survived.

> [!note]- Python Solution
> ```python
> def asteroid_collision(asteroids):
>     stack = []
>     for ast in asteroids:
>         survived = True
>         while stack and stack[-1] > 0 and ast < 0:
>             if stack[-1] < abs(ast):
>                 stack.pop()
>             elif stack[-1] == abs(ast):
>                 stack.pop()
>                 survived = False
>                 break
>             else:
>                 survived = False
>                 break
>         if survived:
>             stack.append(ast)
>     return stack
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> No fundamentally different approach — stack simulation is inherent to sequential collision resolution.

---

## Parentheses — Score and Repair

### Score of Parentheses (LC 856)

> [!example] Problem
> Given a balanced parentheses string s, return the score of the string.
> The score of a balanced parentheses string is based on the following rule
> 
> **Example 1:**
> ```
> Input: s = "()"
> Output: 1
> ```
> 
> **Example 2:**
> ```
> Input: s = "(())"
> Output: 2
> ```
> 
> **Example 3:**
> ```
> Input: s = "()()"
> Output: 2
> ```
> 
> **Constraints:**
> - 2 <= s.length <= 50
> - s consists of only '(' and ')'.
> - s is a balanced parentheses string.

> [!info] Approach
> Depth determines the multiplier — each level of nesting doubles the score of inner `()`. A stack naturally tracks depth. Stack of running scores per depth level. `(` pushes a new scope (0). `)` pops: if the popped value is 0 it was a bare `()` so contribute `2^depth` = `max(2*v, 1)` to the parent; otherwise contribute `2*v`. Start with `[0]`. On `(`: append 0. On `)`: `v = stack.pop()`; `stack[-1] += max(2*v, 1)`. Return `stack[0]`.

> [!note]- Python Solution
> ```python
> def score_of_parentheses(s):
>     stack = [0]
>     for ch in s:
>         if ch == '(':
>             stack.append(0)
>         else:
>             v = stack.pop()
>             stack[-1] += max(2 * v, 1)
>     return stack[0]
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Bit-shift trick: iterate with depth counter; on `()` at depth `d`, add `1 << d`. O(n) time O(1) space.

---

### Minimum Add to Make Parentheses Valid (LC 921)

> [!example] Problem
> A parentheses string is valid if and only if:
> You are given a parentheses string s. In one move, you can insert a parenthesis at any position of the string.
> Return the minimum number of moves required to make s valid.
> 
> **Example 1:**
> ```
> Input: s = "())"
> Output: 1
> ```
> 
> **Example 2:**
> ```
> Input: s = "((("
> Output: 3
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 1000
> - s[i] is either '(' or ')'.

> [!info] Approach
> An unmatched `)` cannot be fixed by future characters — it needs an immediate `(` inserted to its left. Unmatched `(` at the end each need a `)`. Track `open` (unmatched `(`) and `close` (unmatched `)`). On `(`, increment `open`. On `)`, if `open > 0` match it (decrement `open`), else increment `close`. Final answer = `open + close`.

> [!note]- Python Solution
> ```python
> def min_add_to_make_valid(s):
>     open_count = 0  # unmatched '('
>     close_needed = 0  # unmatched ')'
>     for ch in s:
>         if ch == '(':
>             open_count += 1
>         else:
>             if open_count > 0:
>                 open_count -= 1
>             else:
>                 close_needed += 1
>     return open_count + close_needed
> ```

> [!success] Complexity
> Time O(n); Space O(1).

> [!tip] Alternatives
> Stack of unmatched chars — same logic, O(n) space. Counter approach above is optimal.

---

### Check if Word is Valid After Substitutions (LC 1003)

> [!example] Problem
> Given a string s, determine if it is valid.
> A string s is valid if, starting with an empty string t = "", you can transform t into s after performing the following operation any number of times:
> Return true if s is a valid string, otherwise, return false.
> 
> **Example 1:**
> ```
> Input: s = "aabcbc"
> Output: true
> Explanation:
> "" -> "abc" -> "aabcbc"
> Thus, "aabcbc" is valid.
> ```
> 
> **Example 2:**
> ```
> Input: s = "abcabcababcc"
> Output: true
> Explanation:
> "" -> "abc" -> "abcabc" -> "abcabcabc" -> "abcabcababcc"
> Thus, "abcabcababcc" is valid.
> ```
> 
> **Example 3:**
> ```
> Input: s = "abccba"
> Output: false
> Explanation: It is impossible to get "abccba" using the operation.
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 2 * 10^4
> - s consists of letters 'a', 'b', and 'c'

> [!info] Approach
> Every `c` must be preceded by `ab` immediately below it — a nesting structure. Stack validates this pairing. Push each character. When the top three characters are `a`, `b`, `c` (in order), pop all three — they form a complete `abc` unit. After each push check if `stack[-3:] == ['a','b','c']` and pop three. Valid iff stack is empty at end.

> [!note]- Python Solution
> ```python
> def is_valid(s):
>     stack = []
>     for ch in s:
>         stack.append(ch)
>         if len(stack) >= 3 and stack[-3] == 'a' and stack[-2] == 'b' and stack[-1] == 'c':
>             stack.pop()
>             stack.pop()
>             stack.pop()
>     return not stack
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Repeated `str.replace("abc", "")` — O(n²) in worst case. Stack is optimal.

---

## Monotonic Stack — Arrays and Sequences

### Car Fleet (LC 853) `🎯 T2`

> [!example] Problem
> There are n cars at given miles away from the starting mile 0, traveling to reach the mile target.
> You are given two integer arrays position and speed, both of length n, where position[i] is the starting mile of the ith car and speed[i] is the speed of the ith car in miles per hour.
> A car cannot pass another car, but it can catch up and then travel next to it at the speed of the slower car.
> A car fleet is a car or cars driving next to each other. The speed of the car fleet is the minimum speed of any car in the fleet.
> If a car catches up to a car fleet at the mile target, it will still be considered as part of the car fleet.
> Return the number of car fleets that will arrive at the destination.
> 
> **Example 1:**
> ```
> Input: target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]
> Output: 3
> Explanation:
> ```
> 
> **Example 2:**
> ```
> Input: target = 10, position = [3], speed = [3]
> Output: 1
> Explanation:
> ```
> 
> **Example 3:**
> ```
> Input: target = 100, position = [0,2,4], speed = [4,2,1]
> Output: 1
> Explanation:
> ```
> 
> **Constraints:**
> - n == position.length == speed.length
> - 1 <= n <= 10^5
> - 0 < target <= 10^6
> - 0 <= position[i] < target
> - All the values of position are unique.
> - 0 < speed[i] <= 10^6

> [!info] Approach
> Cars closer to the target are ahead. A car behind can only join the fleet ahead if it arrives no later. A stack of arrival times tracks fleets. Sort by position descending (closest to target first). Compute each car's arrival time `(target - pos) / speed`. A car merges into the fleet ahead if its time ≤ the current stack top (it catches up). Otherwise it starts a new fleet. Iterate sorted arrival times. Push if `> stack[-1]` (or stack empty). Stack size = number of fleets.

> [!note]- Python Solution
> ```python
> def car_fleet(target, position, speed):
>     pairs = sorted(zip(position, speed), reverse=True)
>     stack = []
>     for pos, spd in pairs:
>         time = (target - pos) / spd
>         if not stack or time > stack[-1]:
>             stack.append(time)
>         # else: merges into the fleet ahead (smaller or equal time)
>     return len(stack)
> ```

> [!success] Complexity
> Time O(n log n) for sort; Space O(n).

> [!tip] Alternatives
> After sorting, a single pass with a counter (no explicit stack) works: increment count whenever a car's time exceeds the current fleet's time.

---

### Maximum Width Ramp (LC 962)

> [!example] Problem
> A ramp in an integer array nums is a pair (i, j) for which i < j and nums[i] <= nums[j]. The width of such a ramp is j - i.
> Given an integer array nums, return the maximum width of a ramp in nums. If there is no ramp in nums, return 0.
> 
> **Example 1:**
> ```
> Input: nums = [6,0,8,2,1,5]
> Output: 4
> Explanation: The maximum width ramp is achieved at (i, j) = (1, 5): nums[1] = 0 and nums[5] = 5.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [9,8,1,0,1,9,4,0,4,1]
> Output: 7
> Explanation: The maximum width ramp is achieved at (i, j) = (2, 9): nums[2] = 1 and nums[9] = 1.
> ```
> 
> **Constraints:**
> - 2 <= nums.length <= 5 * 10^4
> - 0 <= nums[i] <= 5 * 10^4

> [!info] Approach
> We want the leftmost possible `i` and rightmost possible `j`. Build a decreasing stack of candidate left endpoints, then scan right to left for `j`. Pre-process a monotonically decreasing stack of indices from left to right (only push if strictly smaller than all previous — these are the only viable left anchors). Then scan from right to left: for each `j`, pop stack indices while `nums[stack[-1]] <= nums[j]`, recording max `j - i`. Build decreasing stack in one pass. Reverse scan: greedily pop all valid left endpoints.

> [!note]- Python Solution
> ```python
> def max_width_ramp(nums):
>     n = len(nums)
>     # Build decreasing stack of candidate left indices
>     stack = []
>     for i in range(n):
>         if not stack or nums[i] < nums[stack[-1]]:
>             stack.append(i)
>     best = 0
>     # Scan right to left, match against stack
>     for j in range(n - 1, -1, -1):
>         while stack and nums[stack[-1]] <= nums[j]:
>             best = max(best, j - stack.pop())
>     return best
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Binary search: O(n log n) — build the decreasing stack, then for each j binary search for the leftmost valid i. Harder to implement correctly.

---

### Number of Visible People in a Queue (LC 1944)

> [!example] Problem
> There are n people standing in a queue, and they numbered from 0 to n - 1 in left to right order. You are given an array heights of distinct integers where heights[i] represents the height of the ith person.
> A person can see another person to their right in the queue if everybody in between is shorter than both of them. More formally, the ith person can see the jth person if i  max(heights[i+1], heights[i+2], ..., heights[j-1]).
> Return an array answer of length n where answer[i] is the number of people the ith person can see to their right in the queue.
> 
> **Example 1:**
> ```
> Input: heights = [10,6,8,5,11,9]
> Output: [3,1,2,1,1,0]
> Explanation:
> Person 0 can see person 1, 2, and 4.
> Person 1 can see person 2.
> Person 2 can see person 3 and 4.
> Person 3 can see person 4.
> Person 4 can see person 5.
> Person 5 can see no one since nobody is to the right of them.
> ```
> 
> **Example 2:**
> ```
> Input: heights = [5,1,2,3,10]
> Output: [4,1,1,1,0]
> ```
> 
> **Constraints:**
> - n == heights.length
> - 1 <= n <= 10^5
> - 1 <= heights[i] <= 10^5
> - All the values of heights are unique.

> [!info] Approach
> A taller person blocks all shorter ones behind them. Scan right to left maintaining a decreasing monotonic stack of heights not yet blocked. For person `i`, count how many people they see = number of people popped from the stack (each shorter person directly in front until someone taller) + 1 if the stack is non-empty after popping (the first person taller than `i`). Process right to left. For each person, pop from the decreasing stack while top < current height, incrementing count. Add 1 if stack non-empty (blocked by a taller person). Push current height.

> [!note]- Python Solution
> ```python
> def can_see_persons_count(heights):
>     n = len(heights)
>     result = [0] * n
>     stack = []  # decreasing stack of heights
>     for i in range(n - 1, -1, -1):
>         count = 0
>         while stack and stack[-1] < heights[i]:
>             stack.pop()
>             count += 1
>         if stack:
>             count += 1  # can see the next taller person
>         result[i] = count
>         stack.append(heights[i])
>     return result
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> No O(n) approach without a monotonic structure — brute force is O(n²).

---

### Flatten Binary Tree to Linked List (LC 114 — iterative) `🎯 T2`

> [!example] Problem
> Given the root of a binary tree, flatten the tree into a "linked list"
> 
> **Example 1:**
> ```
> Input: root = [1,2,5,3,4,null,6]
> Output: [1,null,2,null,3,null,4,null,5,null,6]
> ```
> 
> **Example 2:**
> ```
> Input: root = []
> Output: []
> ```
> 
> **Example 3:**
> ```
> Input: root = [0]
> Output: [0]
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 2000].
> - -100 <= Node.val <= 100

> [!info] Approach
> Recursive flatten risks call-stack overflow on skewed trees. Iterative with an explicit stack gives O(h) space. Preorder traversal with a stack. Process root, push right child then left child (so left is processed first). After visiting each node, redirect its `right` to the next preorder node, set `left = None`. Push root. While stack: pop node, if node.right exists push it, if node.left exists push it. Set `node.right = stack[-1] if stack else None`, `node.left = None`.

> [!note]- Python Solution
> ```python
> class TreeNode:
>     def __init__(self, val=0, left=None, right=None):
>         self.val = val
>         self.left = left
>         self.right = right
> >
> def flatten(root):
>     if not root:
>         return
>     stack = [root]
>     while stack:
>         node = stack.pop()
>         if node.right:
>             stack.append(node.right)
>         if node.left:
>             stack.append(node.left)
>         node.right = stack[-1] if stack else None
>         node.left = None
> ```

> [!success] Complexity
> Time O(n); Space O(h) where h = tree height.

> [!tip] Alternatives
> Morris traversal — O(n) time O(1) space (no stack), but modifies tree temporarily and is harder to reason about. The "find predecessor" approach in O(n) with constant space is also canonical.

---

### Path Sum II (LC 113 — iterative DFS) `🎯 T2`

> [!example] Problem
> Given the root of a binary tree and an integer targetSum, return all root-to-leaf paths where the sum of the node values in the path equals targetSum. Each path should be returned as a list of the node values, not node references.
> A root-to-leaf path is a path starting from the root and ending at any leaf node. A leaf is a node with no children.
> 
> **Example 1:**
> ```
> Input: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
> Output: [[5,4,11,2],[5,8,4,5]]
> Explanation: There are two paths whose sum equals targetSum:
> 5 + 4 + 11 + 2 = 22
> 5 + 8 + 4 + 5 = 22
> ```
> 
> **Example 2:**
> ```
> Input: root = [1,2,3], targetSum = 5
> Output: []
> ```
> 
> **Example 3:**
> ```
> Input: root = [1,2], targetSum = 0
> Output: []
> ```
> 
> **Constraints:**
> - The number of nodes in the tree is in the range [0, 5000].
> - -1000 <= Node.val <= 1000
> - -1000 <= targetSum <= 1000

> [!info] Approach
> Recursive DFS is natural but risks stack overflow. An iterative DFS with an explicit stack carrying path state mirrors the recursion exactly. Stack of `(node, remaining_sum, path)` tuples. When a leaf is reached with `remaining == 0`, record the path. Push `(root, target, [])`. On each pop: if leaf and remaining == 0, add copy of path to results. Push right child, then left child (left processed first) with updated remaining and path.

> [!note]- Python Solution
> ```python
> def path_sum(root, target_sum):
>     if not root:
>         return []
>     results = []
>     stack = [(root, target_sum, [])]
>     while stack:
>         node, remaining, path = stack.pop()
>         path = path + [node.val]
>         remaining -= node.val
>         if not node.left and not node.right:
>             if remaining == 0:
>                 results.append(path)
>         else:
>             if node.right:
>                 stack.append((node.right, remaining, path))
>             if node.left:
>                 stack.append((node.left, remaining, path))
>     return results
> ```

> [!success] Complexity
> Time O(n); Space O(n) for stack and path copies (worst case skewed tree).

> [!tip] Alternatives
> Recursive DFS with backtracking — cleaner code, but O(h) call stack. For a balanced tree that's O(log n); for skewed trees risk overflow.

---

## See Also

[[queue]] | [[dynamic-programming]] | [[monotonic-techniques]]
### Next Greater Element I `🎯 T2`

> [!example] Problem
> The next greater element of some element x in an array is the first greater element that is to the right of x in the same array.
> You are given two distinct 0-indexed integer arrays nums1 and nums2, where nums1 is a subset of nums2.
> For each 0 <= i < nums1.length, find the index j such that nums1[i] == nums2[j] and determine the next greater element of nums2[j] in nums2. If there is no next greater element, then the answer for this query is -1.
> Return an array ans of length nums1.length such that ans[i] is the next greater element as described above.
> 
> **Example 1:**
> ```
> Input: nums1 = [4,1,2], nums2 = [1,3,4,2]
> Output: [-1,3,-1]
> Explanation: The next greater element for each value of nums1 is as follows:
> - 4 is underlined in nums2 = [1,3,4,2]. There is no next greater element, so the answer is -1.
> - 1 is underlined in nums2 = [1,3,4,2]. The next greater element is 3.
> - 2 is underlined in nums2 = [1,3,4,2]. There is no next greater element, so the answer is -1.
> ```
> 
> **Example 2:**
> ```
> Input: nums1 = [2,4], nums2 = [1,2,3,4]
> Output: [3,-1]
> Explanation: The next greater element for each value of nums1 is as follows:
> - 2 is underlined in nums2 = [1,2,3,4]. The next greater element is 3.
> - 4 is underlined in nums2 = [1,2,3,4]. There is no next greater element, so the answer is -1.
> ```
> 
> **Constraints:**
> - 1 <= nums1.length <= nums2.length <= 1000
> - 0 <= nums1[i], nums2[i] <= 10^4
> - All integers in nums1 and nums2 are unique.
> - All the integers of nums1 also appear in nums2.

> [!info] Approach
> We need the next greater element for many values, so we preprocess `nums2` with a monotonic stack to avoid repeated scans. Scan `nums2` once with a decreasing stack. When a larger value arrives, it resolves all smaller values on the stack. Store a map `value -> next greater value` and then answer each query from `nums1` in O(1).

> [!note]- Python Solution
> ```python
> def next_greater_element(nums1, nums2):
>     stack = []
>     nxt = {}
>     for x in nums2:
>         while stack and stack[-1] < x:
>             nxt[stack.pop()] = x
>         stack.append(x)
>     return [nxt.get(x, -1) for x in nums1]
> ```

> [!success] Complexity
> O(n) time, O(n) space.

> [!tip] Alternatives
> The same monotonic stack pattern generalizes to next greater/smaller element variants and stock-span style problems.

---

## Monotonic Stack — Advanced

### Sum of Subarray Minimums (LC 907)

> [!example] Problem
> Given an array of integers arr, find the sum of min(b), where b ranges over every (contiguous) subarray of arr. Since the answer may be large, return the answer modulo 109 + 7.
> 
> **Example 1:**
> ```
> Input: arr = [3,1,2,4]
> Output: 17
> Explanation: 
> Subarrays are [3], [1], [2], [4], [3,1], [1,2], [2,4], [3,1,2], [1,2,4], [3,1,2,4]. 
> Minimums are 3, 1, 2, 4, 1, 1, 2, 1, 1, 1.
> Sum is 17.
> ```
> 
> **Example 2:**
> ```
> Input: arr = [11,81,94,43,3]
> Output: 444
> ```
> 
> **Constraints:**
> - 1 <= arr.length <= 3 * 10^4
> - 1 <= arr[i] <= 3 * 10^4

> [!info] Approach
> Brute force is O(n²). For each element, we need to know how many subarrays it is the minimum of. That equals `(elements to the left before a smaller value + 1) * (elements to the right before a smaller or equal value + 1)`. Use a monotonic increasing stack to find, for each index, its "previous less element" (PLE) and "next less or equal element" (NLE). The contribution of `nums[i]` is `nums[i] * left_count * right_count`. In one pass, use the stack to track unresolved indices. When `nums[i]` is smaller than the stack top, pop and compute the contribution of the popped element with `i` as its right boundary. Left boundary comes from the new stack top (or -1 if empty).

> [!note]- Python Solution
> ```python
> def sum_subarray_mins(arr):
>     MOD = 10 ** 9 + 7
>     total = 0
>     stack = []   # indices, increasing by arr value
>     for i in range(len(arr) + 1):
>         while stack and (i == len(arr) or arr[stack[-1]] >= arr[i]):
>             mid = stack.pop()
>             left = stack[-1] if stack else -1
>             right = i
>             count = (mid - left) * (right - mid)
>             total += arr[mid] * count
>         stack.append(i)
>     return total % MOD
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - O(n²) DP: `dp[i]` = sum of mins of subarrays ending at `i`. `dp[i] = arr[i] + (dp[i-1] if arr[i] >= arr[i-1] else arr[i] * k)` where `k` is the count of subarrays where `arr[i]` is still the min.
> - Key insight: use `>=` when popping for the left side and `>` for the right to avoid double-counting equal elements.

---

### 132 Pattern (LC 456)

> [!example] Problem
> Given an array of n integers nums, a 132 pattern is a subsequence of three integers nums[i], nums[j] and nums[k] such that i < j < k and nums[i] < nums[k] < nums[j].
> Return true if there is a 132 pattern in nums, otherwise, return false.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,3,4]
> Output: false
> Explanation: There is no 132 pattern in the sequence.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,1,4,2]
> Output: true
> Explanation: There is a 132 pattern in the sequence: [1, 4, 2].
> ```
> 
> **Example 3:**
> ```
> Input: nums = [-1,3,2,0]
> Output: true
> Explanation: There are three 132 patterns in the sequence: [-1, 3, 2], [-1, 3, 0] and [-1, 2, 0].
> ```
> 
> **Constraints:**
> - n == nums.length
> - 1 <= n <= 2 * 10^5
> - -10^9 <= nums[i] <= 10^9

> [!info] Approach
> Brute force is O(n³). The key observation: if we scan right to left, we can track the best candidate for the "3" (the middle-largest value) using a stack, and maintain the current maximum "2" (the `k` value) seen so far. Scan right to left. Maintain a decreasing stack. Whenever we pop a value from the stack (because the current element is larger), that popped value becomes our best candidate for `nums[k]` (the "2" in 132). If the current element is less than this candidate, we found the pattern. `third = -inf`. For each element right to left: if `num < third`, return True. While stack and `stack[-1] < num`, set `third = stack.pop()`. Push `num`.

> [!note]- Python Solution
> ```python
> def find132pattern(nums):
>     stack = []
>     third = float('-inf')   # best candidate for the "2" in 132
>     for num in reversed(nums):
>         if num < third:
>             return True
>         while stack and stack[-1] < num:
>             third = stack.pop()
>         stack.append(num)
>     return False
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - O(n²) with prefix minimum: for each `j`, `nums[i]` = prefix min up to `j-1`. Scan `k > j` for `nums[i] < nums[k] < nums[j]`. Still O(n²).
> - O(n³) brute force — enumerate all triples.

---

### Buildings With an Ocean View (LC 1762)

> [!example] Problem
> There are `n` buildings in a line. You are given an integer array `heights` of size `n` that represents the heights of the buildings in the line.
> 
> The ocean is to the right of the buildings. A building has an ocean view if the building can see the ocean without obstructions. Formally, a building has an ocean view if all the buildings to its right have a **smaller** height.
> 
> Return a list of indices **(0-indexed)** of buildings that have an ocean view, sorted in increasing order.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** heights = [4,2,3,1]
> **Output:** [0,2,3]
> **Explanation:** Building 1 (0-indexed) does not have an ocean view because building 2 is taller.
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** heights = [4,3,2,1]
> **Output:** [0,1,2,3]
> **Explanation:** All the buildings have an ocean view.
> 
> ```
> 
> Example 3:
> 
> ```
> 
> **Input:** heights = [1,3,2,4]
> **Output:** [3]
> **Explanation:** Only building 3 has an ocean view.
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= heights.length <= 10^5`
> 	
> - `1 <= heights[i] <= 10^9`

> [!info] Approach
> A building has an ocean view iff it is taller than all buildings to its right. Scanning right to left with a running maximum tells us this in one pass. Scan from right to left, tracking the maximum height seen so far. If the current building is strictly taller than the running max, it has an ocean view. Walk right to left. If `heights[i] > max_right`, append `i` to results and update `max_right`. Reverse the results before returning (indices must be in ascending order).

> [!note]- Python Solution
> ```python
> def find_buildings(heights):
>     max_right = 0
>     result = []
>     for i in range(len(heights) - 1, -1, -1):
>         if heights[i] > max_right:
>             result.append(i)
>             max_right = heights[i]
>     result.reverse()
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(1) extra.

> [!tip] Alternatives
> - Monotonic stack (decreasing): push each building; pop all buildings shorter than the current one. Whatever remains at the end has ocean views. Same O(n) but slightly more overhead.
> - The right-to-left scan is cleaner for this specific problem since the answer is just "greater than all to the right."

---

## See Also

[[queue]] | [[dynamic-programming]] | [[monotonic-techniques]]
