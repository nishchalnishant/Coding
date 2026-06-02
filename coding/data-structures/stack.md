---
tags: [coding, data-structures, stack]
topic: stack
difficulty: mixed
---

# Stack Problems

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

### Daily Temperatures

> [!example] Problem
> Given a list of daily temperatures, return an array where `result[i]` is the number of days until a warmer temperature. If no warmer day exists, `result[i] = 0`.

> [!info] Approach
> - **WHY:** Brute force checks every future day for each index — O(n²). We need to resolve each index exactly once.
> - **WHAT:** Monotonic decreasing stack of indices. When a warmer temperature arrives, all cooler pending indices on the stack have found their answer.
> - **HOW:** Push index `i` onto the stack. When `temps[i] > temps[stack[-1]]`, pop and record `result[popped] = i - popped`. Stack holds indices of temperatures that haven't yet seen a warmer day.

> [!note]- Python Solution
> ```python
> def daily_temperatures(temperatures: list[int]) -> list[int]:
>     result = [0] * len(temperatures)
>     stack: list[int] = []  # indices, decreasing temperature order
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

### Next Greater Element II

> [!example] Problem
> Given a circular array, find the next greater element for each element. Search wraps around.

> [!info] Approach
> - **WHY:** Circular array means element `0` might be the next greater for element `n-1`. Simulate by doubling the array conceptually.
> - **WHAT:** Same decreasing monotonic stack. Iterate `0..2n-1` with `i % n` for index. Only push on the first pass (`i < n`) to avoid duplicate results.
> - **HOW:** Initialize `result = [-1] * n`. Iterate `2n` times. Use `i % n` to access elements. Only push `i % n` when `i < n`.

> [!note]- Python Solution
> ```python
> def next_greater_elements(nums: list[int]) -> list[int]:
>     n = len(nums)
>     result = [-1] * n
>     stack: list[int] = []
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
> For each new day's price, compute the stock span — the maximum number of consecutive days (including today) with price ≤ today's price.

> [!info] Approach
> - **WHY:** Naively scan backwards each day — O(n) per call, O(n²) total. We need O(1) amortized.
> - **WHAT:** Monotonic decreasing stack of `(price, span)` tuples. When a new price arrives that's >= stack top, we absorb the top's span (it was already contiguous and all ≤ current).
> - **HOW:** Pop all `(p, s)` where `p <= current_price`, accumulating their spans. Push `(current_price, accumulated_span + 1)`.

> [!note]- Python Solution
> ```python
> class StockSpanner:
>     def __init__(self) -> None:
>         self._stack: list[tuple[int, int]] = []  # (price, span)
>
>     def next(self, price: int) -> int:
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
> Find the sum of `min(subarray)` for all contiguous subarrays of `arr`. Answer modulo 1e9+7.

> [!info] Approach
> - **WHY:** Enumerate all subarrays — O(n²) or O(n³). Instead, find for each element how many subarrays it is the minimum of.
> - **WHAT:** For element `arr[i]`, find `left[i]` = number of elements to the left where `arr[i]` is the minimum (stopping at the previous smaller), and `right[i]` = same for right. Contribution = `arr[i] * left[i] * right[i]`.
> - **HOW:** Use monotonic increasing stack twice (or once with careful boundary tracking). Left boundary: strict `<` comparison; right boundary: `<=` to avoid double-counting equal elements.

> [!note]- Python Solution
> ```python
> def sum_subarray_mins(arr: list[int]) -> int:
>     MOD = 10**9 + 7
>     n = len(arr)
>     left = [0] * n   # distance to previous smaller element
>     right = [0] * n  # distance to next smaller or equal element
>     stack: list[int] = []
>
>     # Left: how far left can arr[i] be the minimum (strict <)
>     for i in range(n):
>         while stack and arr[stack[-1]] >= arr[i]:
>             stack.pop()
>         left[i] = i - stack[-1] if stack else i + 1
>         stack.append(i)
>
>     stack.clear()
>     # Right: how far right can arr[i] be the minimum (<=, strict to avoid double count)
>     for i in range(n - 1, -1, -1):
>         while stack and arr[stack[-1]] > arr[i]:
>             stack.pop()
>         right[i] = stack[-1] - i if stack else n - i
>         stack.append(i)
>
>     return sum(arr[i] * left[i] * right[i] for i in range(n)) % MOD
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> DP with monotonic stack in one pass — possible but trickier to reason about. The two-pass approach above is clearer.

---

## Monotonic Stack — Histogram / Rectangle

### Largest Rectangle in Histogram

> [!example] Problem
> Given heights of bars in a histogram, find the area of the largest rectangle that fits within the histogram.

> [!info] Approach
> - **WHY:** For each bar as the height of the rectangle, the width extends left and right until a shorter bar is hit. Finding those boundaries naively is O(n) each.
> - **WHAT:** Monotonic increasing stack of indices. When a bar shorter than the stack top arrives, the top bar's right boundary has been found — compute area.
> - **HOW:** Append sentinel `0` to flush the stack. On pop, `height = heights[popped]`. Width = `i - stack[-1] - 1` if stack is non-empty, else `i` (the bar is the global minimum so far).

> [!note]- Python Solution
> ```python
> def largest_rectangle_area(heights: list[int]) -> int:
>     stack: list[int] = []  # increasing stack of indices
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

### Maximal Rectangle

> [!example] Problem
> Given a binary matrix of '0's and '1's, find the largest rectangle containing only '1's.

> [!info] Approach
> - **WHY:** Reduce to Largest Rectangle in Histogram. Each row defines a histogram where `heights[j]` = consecutive '1's above and including `matrix[row][j]`.
> - **WHAT:** Maintain a `heights` array. For each row, update heights (reset to 0 on '0', increment on '1'). Apply the histogram algorithm per row.
> - **HOW:** `heights[j] = heights[j] + 1 if matrix[row][j] == '1' else 0`. Run `largest_rectangle_area(heights)` for each row.

> [!note]- Python Solution
> ```python
> def maximal_rectangle(matrix: list[list[str]]) -> int:
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
>
> def largest_rectangle_area(heights: list[int]) -> int:
>     stack: list[int] = []
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

### Trapping Rain Water (stack approach)

> [!example] Problem
> Given an elevation map, compute how much water it can trap after raining.

> [!info] Approach
> - **WHY:** Water fills valleys. Each valley is bounded by taller bars on both sides. The stack lets us process valleys as they form.
> - **WHAT:** Monotonic decreasing stack. When a taller bar arrives, the top of the stack is a valley bottom. Water height = `min(left_bar, current_bar) - valley_bottom_height`. Width = distance between left and current bar minus 1.
> - **HOW:** Push indices onto a decreasing stack. On pop (taller bar arrived), compute bounded water above the popped bar.

> [!note]- Python Solution
> ```python
> def trap(height: list[int]) -> int:
>     stack: list[int] = []
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

### Valid Parentheses

> [!example] Problem
> Given a string of `()[]{}`, determine if the brackets are valid (properly nested and matched).

> [!info] Approach
> - **WHY:** LIFO — the most recently opened bracket must be the next closed.
> - **WHAT:** Push opening brackets. On each closing bracket, pop the stack and verify it matches.
> - **HOW:** Map `')' → '('`, etc. If stack is empty when closing bracket arrives, or top doesn't match, return `False`. Valid iff stack is empty at end.

> [!note]- Python Solution
> ```python
> def is_valid(s: str) -> bool:
>     stack: list[str] = []
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

### Decode String

> [!example] Problem
> Decode a string encoded as `k[encoded_string]`. E.g., `3[a2[c]]` → `accaccacc`.

> [!info] Approach
> - **WHY:** Nesting requires tracking context at each `[`. LIFO matches nested structure.
> - **WHAT:** Stack stores `(built_string, repeat_count)` pairs. On `[`, push current context and reset. On `]`, pop and expand.
> - **HOW:** Parse digits to get `k`. On `[`: push `(current_string, k)`, reset both. On `]`: pop `(prev_str, k)`, set `current = prev_str + current * k`. Characters append to `current`.

> [!note]- Python Solution
> ```python
> def decode_string(s: str) -> str:
>     stack: list[tuple[str, int]] = []
>     current = ''
>     k = 0
>     for ch in s:
>         if ch.isdigit():
>             k = k * 10 + int(ch)
>         elif ch == '[':
>             stack.append((current, k))
>             current = ''
>             k = 0
>         elif ch == ']':
>             prev_str, repeat = stack.pop()
>             current = prev_str + current * repeat
>         else:
>             current += ch
>     return current
> ```

> [!success] Complexity
> Time O(output length) in worst case; Space O(depth * string length).

> [!tip] Alternatives
> Recursive descent parser — equivalent logic, harder to control stack depth.

---

### Remove All Adjacent Duplicates in String

> [!example] Problem
> Repeatedly remove adjacent duplicate characters until no adjacent duplicates remain.

> [!info] Approach
> - **WHY:** Removing one pair can create new adjacent duplicates — process must cascade. Stack handles this naturally.
> - **WHAT:** Push characters. If the new character equals the stack top, pop (they cancel). Otherwise push. Result is remaining stack joined.
> - **HOW:** Linear scan. Maintain stack. At each character, cancel with top if equal. Analogous to bracket matching.

> [!note]- Python Solution
> ```python
> def remove_duplicates(s: str) -> str:
>     stack: list[str] = []
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

### Remove K Digits

> [!example] Problem
> Remove `k` digits from `num` (string) to make the smallest possible number. No leading zeros.

> [!info] Approach
> - **WHY:** Greedy — to minimize, remove a digit when the next digit is smaller (it would be more beneficial at that position).
> - **WHAT:** Monotonic increasing stack. Pop the top when it's larger than the current digit and `k > 0`.
> - **HOW:** Build the stack left to right. Pop larger elements while `k > 0`. If `k` still > 0 after the loop, trim last `k` digits from the stack (which is already sorted ascending). Strip leading zeros.

> [!note]- Python Solution
> ```python
> def remove_k_digits(num: str, k: int) -> str:
>     stack: list[str] = []
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

### Min Stack

> [!example] Problem
> Design a stack with O(1) `push`, `pop`, `top`, and `get_min`.

> [!info] Approach
> - **WHY:** A regular stack loses track of the minimum after pops. We need the minimum at every stack depth.
> - **WHAT:** Parallel `min_stack` where `min_stack[i]` = minimum of all elements in `stack[0..i]`. Both stacks stay synchronized.
> - **HOW:** On push, `min_stack` pushes `min(val, min_stack[-1])`. On pop, both stacks pop. `get_min` returns `min_stack[-1]`.

> [!note]- Python Solution
> ```python
> class MinStack:
>     def __init__(self) -> None:
>         self._stack: list[int] = []
>         self._min_stack: list[int] = []
>
>     def push(self, val: int) -> None:
>         self._stack.append(val)
>         current_min = val if not self._min_stack else min(val, self._min_stack[-1])
>         self._min_stack.append(current_min)
>
>     def pop(self) -> None:
>         self._stack.pop()
>         self._min_stack.pop()
>
>     def top(self) -> int:
>         return self._stack[-1]
>
>     def get_min(self) -> int:
>         return self._min_stack[-1]
> ```

> [!success] Complexity
> Time O(1) all ops; Space O(n).

> [!tip] Alternatives
> Store `(val, current_min)` tuples in a single stack — same complexity, single structure. Saves one stack at the cost of slightly less readable code.

---

### Maximum Frequency Stack

> [!example] Problem
> Design a stack where `pop` returns the most frequently pushed element (ties broken by most recently pushed).

> [!info] Approach
> - **WHY:** Standard stack gives LIFO; we want frequency-priority with LIFO for ties.
> - **WHAT:** Two maps: `val → frequency` and `freq → [stack of vals at that frequency]`. Track `max_freq`.
> - **HOW:** Push: increment `freq[val]`, append `val` to `group[freq[val]]`, update `max_freq`. Pop: take from `group[max_freq]`, decrement `freq[val]`, decrement `max_freq` if the bucket is now empty.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
>
> class FreqStack:
>     def __init__(self) -> None:
>         self._freq: dict[int, int] = defaultdict(int)
>         self._group: dict[int, list[int]] = defaultdict(list)
>         self._max_freq = 0
>
>     def push(self, val: int) -> None:
>         self._freq[val] += 1
>         f = self._freq[val]
>         self._max_freq = max(self._max_freq, f)
>         self._group[f].append(val)
>
>     def pop(self) -> int:
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
> Implement a FIFO queue using only two stacks.

> [!info] Approach
> - **WHY:** Stack is LIFO; reversing the stack gives FIFO order. One stack for input, one for output.
> - **WHAT:** `in_stack` receives all pushes. `out_stack` is lazily populated from `in_stack` when needed. Reversing `in_stack` into `out_stack` makes the oldest element accessible at the top.
> - **HOW:** `push` appends to `in_stack`. `pop`/`peek`: if `out_stack` is empty, move all of `in_stack` to `out_stack` (reversal). Then operate on `out_stack`. Amortized O(1).

> [!note]- Python Solution
> ```python
> class MyQueue:
>     def __init__(self) -> None:
>         self._in: list[int] = []
>         self._out: list[int] = []
>
>     def push(self, x: int) -> None:
>         self._in.append(x)
>
>     def _transfer(self) -> None:
>         if not self._out:
>             while self._in:
>                 self._out.append(self._in.pop())
>
>     def pop(self) -> int:
>         self._transfer()
>         return self._out.pop()
>
>     def peek(self) -> int:
>         self._transfer()
>         return self._out[-1]
>
>     def empty(self) -> bool:
>         return not self._in and not self._out
> ```

> [!success] Complexity
> Time O(1) amortized per op; Space O(n).

> [!tip] Alternatives
> Single stack with recursion for dequeue — O(n) each dequeue. Double-transfer is the canonical approach.

---

### Validate Stack Sequences

> [!example] Problem
> Given `pushed` and `popped` sequences, determine if they could be the result of a valid push/pop sequence on an empty stack.

> [!info] Approach
> - **WHY:** Simulate the push sequence and greedily pop when the top matches the next expected pop.
> - **WHAT:** Simulate with an explicit stack. Push elements from `pushed`. After each push, greedily pop while top matches `popped[j]`.
> - **HOW:** Maintain pointer `j` into `popped`. After pushing `pushed[i]`, pop while `stack and stack[-1] == popped[j]`, incrementing `j`. Valid iff stack is empty at end.

> [!note]- Python Solution
> ```python
> def validate_stack_sequences(pushed: list[int], popped: list[int]) -> bool:
>     stack: list[int] = []
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

### Evaluate Reverse Polish Notation

> [!example] Problem
> Evaluate an expression in Reverse Polish Notation (postfix). Tokens are integers or `+`, `-`, `*`, `/` (truncates toward zero).

> [!info] Approach
> - **WHY:** RPN eliminates parentheses — operators apply to the two most recently seen operands. LIFO matches this.
> - **WHAT:** Operand stack. Push numbers. On operator, pop two operands, apply, push result.
> - **HOW:** Pop `b` then `a` (order matters for `-` and `/`). Apply operator. Push result. Division truncates toward zero: `int(a / b)` not `a // b` (handles negatives).

> [!note]- Python Solution
> ```python
> def eval_rpn(tokens: list[str]) -> int:
>     stack: list[int] = []
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
> Evaluate a string expression with `+`, `-`, spaces, and parentheses. No `*` or `/`.

> [!info] Approach
> - **WHY:** Parentheses introduce nested scope. Stack saves the running result and sign when entering a new scope.
> - **WHAT:** Track `result` and `sign` (+1 or -1). On `(`: push `(result, sign)` and reset. On `)`: pop and combine `sign_before * inner_result + outer_result`.
> - **HOW:** Parse multi-digit numbers. Accumulate into `result` using current `sign`. Handle `(` and `)` for scope management.

> [!note]- Python Solution
> ```python
> def calculate_i(s: str) -> int:
>     stack: list[int] = []
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
> Evaluate a string with `+`, `-`, `*`, `/` and spaces. No parentheses. Division truncates toward zero.

> [!info] Approach
> - **WHY:** `*` and `/` have higher precedence than `+` and `-`. Process high-precedence operators immediately; defer low-precedence to a final sum.
> - **WHAT:** Stack of terms to be summed. Track `prev_op`. On `+`/`-`, push `sign * num`. On `*`/`/`, pop top, apply, push result back.
> - **HOW:** Parse number, apply `prev_op` with stack. Default `prev_op = '+'`. Final answer = sum of stack.

> [!note]- Python Solution
> ```python
> def calculate_ii(s: str) -> int:
>     stack: list[int] = []
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
> Evaluate a full expression with `+`, `-`, `*`, `/`, and nested parentheses.

> [!info] Approach
> - **WHY:** Combination of I (parentheses) and II (precedence). Parentheses require scope management; precedence requires deferred addition.
> - **WHAT:** Recursive approach: when `(` is encountered, recursively evaluate the sub-expression inside until `)`, then continue with the result.
> - **HOW:** Implement a helper that processes until end or `)`. Inside, use the stack-based approach from Calculator II. On `(`, recurse for the inner expression.

> [!note]- Python Solution
> ```python
> def calculate_iii(s: str) -> int:
>     idx = 0
>
>     def helper() -> int:
>         nonlocal idx
>         stack: list[int] = []
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
>
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
> Given logs of function start/end events on a single thread, return the exclusive execution time of each function.

> [!info] Approach
> - **WHY:** Functions nest (call stack semantics). When a nested function starts, the outer function pauses. When it ends, the outer resumes.
> - **WHAT:** Explicit stack of `(func_id, start_time)`. On start: push. On end: pop, compute duration. Subtract this duration from the new top (the caller) to avoid double-counting.
> - **HOW:** Parse each log. On `"start"`: if stack non-empty, add elapsed time to top's exclusive time. Push current. On `"end"`: pop, compute time, add to result. Update `prev_time = end + 1`.

> [!note]- Python Solution
> ```python
> def exclusive_time(n: int, logs: list[str]) -> list[int]:
>     result = [0] * n
>     stack: list[int] = []  # stack of function ids
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
> Simplify an absolute Unix file path (handles `.`, `..`, and multiple slashes).

> [!info] Approach
> - **WHY:** `..` means go up one directory — pop from the path. `.` and empty tokens are no-ops.
> - **WHAT:** Stack of directory names. Push valid names. Pop on `..`. Ignore `.` and empty strings.
> - **HOW:** Split on `/`. For each part: skip empty strings and `.`; pop on `..` (if stack non-empty); push otherwise. Join with `/` and prepend `/`.

> [!note]- Python Solution
> ```python
> def simplify_path(path: str) -> str:
>     stack: list[str] = []
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
> Given a list of operations, simulate a baseball game scoring: integer = new score, `+` = sum of last two, `D` = double last, `C` = remove last. Return the total score.

> [!info] Approach
> - **WHY:** All operations reference the top of the score history — LIFO structure.
> - **WHAT:** Stack of valid scores. Each operation modifies the stack top.
> - **HOW:** Parse each op. Integer: push. `+`: push `stack[-1] + stack[-2]`. `D`: push `stack[-1] * 2`. `C`: pop. Sum the stack at the end.

> [!note]- Python Solution
> ```python
> def cal_points(operations: list[str]) -> int:
>     stack: list[int] = []
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

### Asteroid Collision

> [!example] Problem
> Asteroids move right (positive) or left (negative). When a right-moving and left-moving asteroid collide, the smaller one explodes; equal-size both explode. Return the final state.

> [!info] Approach
> - **WHY:** Collisions only happen between a positive (right-moving) on the stack and a new negative (left-moving). Stack of survivors.
> - **WHAT:** Maintain a stack of surviving asteroids. A collision only occurs when `stack[-1] > 0 and asteroid < 0`.
> - **HOW:** While collision conditions hold: if top is smaller, pop (top destroyed, current continues); if equal, pop and break (both destroyed); if top is larger, break (current destroyed, don't append). Use `while...else` to append only if current survived.

> [!note]- Python Solution
> ```python
> def asteroid_collision(asteroids: list[int]) -> list[int]:
>     stack: list[int] = []
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
> A balanced parentheses string has a score: `()` = 1, `AB` = score(A) + score(B), `(A)` = 2 × score(A). Given a valid string, return its score.

> [!info] Approach
> - **WHY:** Depth determines the multiplier — each level of nesting doubles the score of inner `()`. A stack naturally tracks depth.
> - **WHAT:** Stack of running scores per depth level. `(` pushes a new scope (0). `)` pops: if the popped value is 0 it was a bare `()` so contribute `2^depth` = `max(2*v, 1)` to the parent; otherwise contribute `2*v`.
> - **HOW:** Start with `[0]`. On `(`: append 0. On `)`: `v = stack.pop()`; `stack[-1] += max(2*v, 1)`. Return `stack[0]`.

> [!note]- Python Solution
> ```python
> def score_of_parentheses(s: str) -> int:
>     stack: list[int] = [0]
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
> Given a string of `(` and `)`, return the minimum number of parentheses to insert to make it valid.

> [!info] Approach
> - **WHY:** An unmatched `)` cannot be fixed by future characters — it needs an immediate `(` inserted to its left. Unmatched `(` at the end each need a `)`.
> - **WHAT:** Track `open` (unmatched `(`) and `close` (unmatched `)`). On `(`, increment `open`. On `)`, if `open > 0` match it (decrement `open`), else increment `close`.
> - **HOW:** Final answer = `open + close`.

> [!note]- Python Solution
> ```python
> def min_add_to_make_valid(s: str) -> int:
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
> A valid string is either empty, or formed by inserting `"abc"` anywhere in a valid string. Determine if a given string is valid.

> [!info] Approach
> - **WHY:** Every `c` must be preceded by `ab` immediately below it — a nesting structure. Stack validates this pairing.
> - **WHAT:** Push each character. When the top three characters are `a`, `b`, `c` (in order), pop all three — they form a complete `abc` unit.
> - **HOW:** After each push check if `stack[-3:] == ['a','b','c']` and pop three. Valid iff stack is empty at end.

> [!note]- Python Solution
> ```python
> def is_valid(s: str) -> bool:
>     stack: list[str] = []
>     for ch in s:
>         stack.append(ch)
>         if len(stack) >= 3 and stack[-3] == 'a' and stack[-2] == 'b' and stack[-1] == 'c':
>             stack.pop(); stack.pop(); stack.pop()
>     return not stack
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Repeated `str.replace("abc", "")` — O(n²) in worst case. Stack is optimal.

---

## Monotonic Stack — Arrays and Sequences

### 132 Pattern (LC 456)

> [!example] Problem
> Given an array, determine if there exist indices `i < j < k` such that `nums[i] < nums[k] < nums[j]`.

> [!info] Approach
> - **WHY:** We need the "3" (nums[j]) to be as large as possible and the "2" (nums[k]) to be just below it — a monotonic stack from the right maintains candidate "2" values.
> - **WHAT:** Scan right to left. Maintain a decreasing monotonic stack of candidates for nums[j]. Track `third` = the best candidate for nums[k] (largest value popped from the stack so far, meaning it was once a "3" that got beaten by a taller bar).
> - **HOW:** When `stack[-1] < nums[i]`, pop into `third` (this becomes nums[k]). If `nums[i] < third`, we found nums[i] < nums[k] < nums[j] — return True. Push `nums[i]`.

> [!note]- Python Solution
> ```python
> def find132pattern(nums: list[int]) -> bool:
>     stack: list[int] = []
>     third = float('-inf')  # best candidate for nums[k] (the "2")
>     for num in reversed(nums):
>         if num < third:
>             return True
>         while stack and stack[-1] < num:
>             third = stack.pop()
>         stack.append(num)
>     return False
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> O(n²) brute force: for each j, track prefix min as i, scan right for k. Stack approach is the only O(n) solution.

---

### Car Fleet (LC 853)

> [!example] Problem
> N cars head to the same destination `target`. Each car has a position and speed. A faster car that catches a slower one forms a fleet and travels at the slower car's speed. Return the number of fleets that arrive.

> [!info] Approach
> - **WHY:** Cars closer to the target are ahead. A car behind can only join the fleet ahead if it arrives no later. A stack of arrival times tracks fleets.
> - **WHAT:** Sort by position descending (closest to target first). Compute each car's arrival time `(target - pos) / speed`. A car merges into the fleet ahead if its time ≤ the current stack top (it catches up). Otherwise it starts a new fleet.
> - **HOW:** Iterate sorted arrival times. Push if `> stack[-1]` (or stack empty). Stack size = number of fleets.

> [!note]- Python Solution
> ```python
> def car_fleet(target: int, position: list[int], speed: list[int]) -> int:
>     pairs = sorted(zip(position, speed), reverse=True)
>     stack: list[float] = []
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
> A ramp is a pair `(i, j)` with `i < j` and `nums[i] <= nums[j]`. Find the maximum width `j - i`.

> [!info] Approach
> - **WHY:** We want the leftmost possible `i` and rightmost possible `j`. Build a decreasing stack of candidate left endpoints, then scan right to left for `j`.
> - **WHAT:** Pre-process a monotonically decreasing stack of indices from left to right (only push if strictly smaller than all previous — these are the only viable left anchors). Then scan from right to left: for each `j`, pop stack indices while `nums[stack[-1]] <= nums[j]`, recording max `j - i`.
> - **HOW:** Build decreasing stack in one pass. Reverse scan: greedily pop all valid left endpoints.

> [!note]- Python Solution
> ```python
> def max_width_ramp(nums: list[int]) -> int:
>     n = len(nums)
>     # Build decreasing stack of candidate left indices
>     stack: list[int] = []
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
> People stand in a queue. Person `i` can see person `j` (j > i) if all people between them are shorter than both `heights[i]` and `heights[j]`. Return the count of visible people for each person.

> [!info] Approach
> - **WHY:** A taller person blocks all shorter ones behind them. Scan right to left maintaining a decreasing monotonic stack of heights not yet blocked.
> - **WHAT:** For person `i`, count how many people they see = number of people popped from the stack (each shorter person directly in front until someone taller) + 1 if the stack is non-empty after popping (the first person taller than `i`).
> - **HOW:** Process right to left. For each person, pop from the decreasing stack while top < current height, incrementing count. Add 1 if stack non-empty (blocked by a taller person). Push current height.

> [!note]- Python Solution
> ```python
> def can_see_persons_count(heights: list[int]) -> list[int]:
>     n = len(heights)
>     result = [0] * n
>     stack: list[int] = []  # decreasing stack of heights
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

### Buildings With an Ocean View (LC 1762)

> [!example] Problem
> Buildings face the ocean to the right. A building has an ocean view if all buildings to its right are shorter. Return indices of buildings with an ocean view, in increasing order.

> [!info] Approach
> - **WHY:** Scan left to right: a building loses its ocean view if a taller building appears to its right. Maintain a decreasing monotonic stack — only the "visible" candidates remain.
> - **WHAT:** Monotonic decreasing stack of indices. Pop any building shorter than the current one (it lost its view). Push current.
> - **HOW:** Iterate left to right. While `stack and heights[stack[-1]] <= heights[i]`: pop. Push `i`. Stack contains all indices with ocean views in order.

> [!note]- Python Solution
> ```python
> def find_buildings(heights: list[int]) -> list[int]:
>     stack: list[int] = []
>     for i, h in enumerate(heights):
>         while stack and heights[stack[-1]] <= h:
>             stack.pop()
>         stack.append(i)
>     return stack
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Scan right to left tracking running max — O(n) time O(1) extra space (excluding output). Simpler but requires reversing the output.

---

## Iterative Tree Traversal

### Flatten Binary Tree to Linked List (LC 114 — iterative)

> [!example] Problem
> Flatten a binary tree to a linked list in-place (preorder: root → left → right), using the `right` pointer as next. Do it iteratively.

> [!info] Approach
> - **WHY:** Recursive flatten risks call-stack overflow on skewed trees. Iterative with an explicit stack gives O(h) space.
> - **WHAT:** Preorder traversal with a stack. Process root, push right child then left child (so left is processed first). After visiting each node, redirect its `right` to the next preorder node, set `left = None`.
> - **HOW:** Push root. While stack: pop node, if node.right exists push it, if node.left exists push it. Set `node.right = stack[-1] if stack else None`, `node.left = None`.

> [!note]- Python Solution
> ```python
> class TreeNode:
>     def __init__(self, val=0, left=None, right=None):
>         self.val = val; self.left = left; self.right = right
>
> def flatten(root: TreeNode | None) -> None:
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

### Path Sum II (LC 113 — iterative DFS)

> [!example] Problem
> Find all root-to-leaf paths in a binary tree where the sum of node values equals `target`. Return all such paths.

> [!info] Approach
> - **WHY:** Recursive DFS is natural but risks stack overflow. An iterative DFS with an explicit stack carrying path state mirrors the recursion exactly.
> - **WHAT:** Stack of `(node, remaining_sum, path)` tuples. When a leaf is reached with `remaining == 0`, record the path.
> - **HOW:** Push `(root, target, [])`. On each pop: if leaf and remaining == 0, add copy of path to results. Push right child, then left child (left processed first) with updated remaining and path.

> [!note]- Python Solution
> ```python
> def path_sum(root: TreeNode | None, target_sum: int) -> list[list[int]]:
>     if not root:
>         return []
>     results: list[list[int]] = []
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
### Next Greater Element I

> [!example] Problem
> For each element in `nums1`, find the first greater element to its right in `nums2`.

> [!info] Approach
> - **WHY:** We need the next greater element for many values, so we preprocess `nums2` with a monotonic stack to avoid repeated scans.
> - **WHAT:** Scan `nums2` once with a decreasing stack. When a larger value arrives, it resolves all smaller values on the stack.
> - **HOW:** Store a map `value -> next greater value` and then answer each query from `nums1` in O(1).

> [!note]- Python Solution
> ```python
> def next_greater_element(nums1: list[int], nums2: list[int]) -> list[int]:
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
> Given an array, find the sum of `min(subarray)` for every contiguous subarray. Return the answer modulo 10^9 + 7.

> [!info] Approach
> - **WHY:** Brute force is O(n²). For each element, we need to know how many subarrays it is the minimum of. That equals `(elements to the left before a smaller value + 1) * (elements to the right before a smaller or equal value + 1)`.
> - **WHAT:** Use a monotonic increasing stack to find, for each index, its "previous less element" (PLE) and "next less or equal element" (NLE). The contribution of `nums[i]` is `nums[i] * left_count * right_count`.
> - **HOW:** In one pass, use the stack to track unresolved indices. When `nums[i]` is smaller than the stack top, pop and compute the contribution of the popped element with `i` as its right boundary. Left boundary comes from the new stack top (or -1 if empty).

> [!note]- Python Solution
> ```python
> def sum_subarray_mins(arr: list[int]) -> int:
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
> Given an array, return `True` if there exist indices `i < j < k` such that `nums[i] < nums[k] < nums[j]` (a "132 pattern").

> [!info] Approach
> - **WHY:** Brute force is O(n³). The key observation: if we scan right to left, we can track the best candidate for the "3" (the middle-largest value) using a stack, and maintain the current maximum "2" (the `k` value) seen so far.
> - **WHAT:** Scan right to left. Maintain a decreasing stack. Whenever we pop a value from the stack (because the current element is larger), that popped value becomes our best candidate for `nums[k]` (the "2" in 132). If the current element is less than this candidate, we found the pattern.
> - **HOW:** `third = -inf`. For each element right to left: if `num < third`, return True. While stack and `stack[-1] < num`, set `third = stack.pop()`. Push `num`.

> [!note]- Python Solution
> ```python
> def find132pattern(nums: list[int]) -> bool:
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
> Given an array where `heights[i]` is the height of building `i`, a building has an ocean view if all buildings to its right are shorter. Return the indices (in increasing order) of buildings with an ocean view.

> [!info] Approach
> - **WHY:** A building has an ocean view iff it is taller than all buildings to its right. Scanning right to left with a running maximum tells us this in one pass.
> - **WHAT:** Scan from right to left, tracking the maximum height seen so far. If the current building is strictly taller than the running max, it has an ocean view.
> - **HOW:** Walk right to left. If `heights[i] > max_right`, append `i` to results and update `max_right`. Reverse the results before returning (indices must be in ascending order).

> [!note]- Python Solution
> ```python
> def find_buildings(heights: list[int]) -> list[int]:
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
