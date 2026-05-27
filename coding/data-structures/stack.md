---
tags: [coding, data-structures, stack]
topic: stack
difficulty: mixed
---

# Stack Problems

---

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
> Time O(n logs); Space O(n) stack depth.

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

## See Also

[[queue]] | [[dynamic-programming]] | [[monotonic-techniques]]
