# Stack — SDE-3 Gold Standard

LIFO (Last In, First Out) structure. SDE-3 focus: **monotonic stack** for "next greater/smaller" in O(N), expression parsing, and the deque extension for sliding window problems.

---

## 1. Concept Overview

**Problem space**: Next Greater/Smaller Element (NGE/NSE), largest rectangle in histogram, trapping rain water, expression evaluation, valid parentheses, DFS simulation, decode string, exclusive function time.

**When to use**: You need the "last relevant" element — OR — you're tracking a sequence where older elements become irrelevant once a newer one is processed.

---

## 2. Core Algorithms & Click Moments

### Monotonic Stack — Next Greater Element

> [!IMPORTANT]
> **The Click Moment**: "**Next greater** element to the right" — OR — "**nearest smaller** to the left" — OR — "**daily temperatures**, span, or stock price" problems. Any problem asking "for each element, find the first X in one direction" maps to a monotonic stack. Brute force is O(N²); monotonic stack is O(N) — each element pushed and popped exactly once.

- **Decreasing stack** (top = smallest): when a larger element arrives, all smaller stack elements have found their Next Greater → pop and record.
- **Increasing stack** (top = largest): when a smaller element arrives, pop and record Next Smaller.

```python
def next_greater_element(nums: list[int]) -> list[int]:
    n = len(nums)
    result = [-1] * n
    stack: list[int] = []  # stores indices, not values
    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            result[stack.pop()] = nums[i]
        stack.append(i)
    return result

def daily_temperatures(temps: list[int]) -> list[int]:
    result = [0] * len(temps)
    stack: list[int] = []
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            result[j] = i - j
        stack.append(i)
    return result
```

> [!CAUTION]
> Always store **indices** on the stack, not values. You need the index to compute distances (`i - j`) or to fill the result array. Storing values loses position information.

---

### Largest Rectangle in Histogram

> [!IMPORTANT]
> **The Click Moment**: "Largest rectangle in **histogram**" — OR — "maximum area in a **matrix** of 0s and 1s" (Maximal Rectangle = histogram per row). The key insight: for each bar, its maximum-width rectangle extends as far left and right as bars of equal or greater height. A monotonic **increasing** stack finds both boundaries in one pass.

```python
def largest_rectangle_area(heights: list[int]) -> int:
    stack: list[int] = []  # increasing stack of indices
    best = 0
    for i, h in enumerate(heights + [0]):  # sentinel 0 flushes remaining stack
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            best = max(best, height * width)
        stack.append(i)
    return best

def maximal_rectangle(matrix: list[list[str]]) -> int:
    if not matrix or not matrix[0]:
        return 0
    cols = len(matrix[0])
    heights = [0] * cols
    best = 0
    for row in matrix:
        for j in range(cols):
            heights[j] = heights[j] + 1 if row[j] == '1' else 0
        best = max(best, largest_rectangle_area(heights))
    return best
```

> [!TIP]
> **Width calculation when stack is empty**: If the stack is empty after popping, the popped bar is the shortest seen so far — its left boundary is index 0, so `width = i` (the entire range up to current index).

---

### Valid Parentheses / Nesting Matching

> [!IMPORTANT]
> **The Click Moment**: "Valid **brackets**" — OR — "**matching** pairs of open/close" — OR — "valid string with **nested** structure". Push opening characters; on each closing character, pop and verify the match. Final stack must be empty.

```python
def is_valid(s: str) -> bool:
    stack: list[str] = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        elif not stack or stack[-1] != pairs[ch]:
            return False
        else:
            stack.pop()
    return not stack
```

> [!CAUTION]
> Check `not stack` before `stack[-1]` — if the stack is empty when a closing bracket arrives, the string is invalid. Without this guard you get an `IndexError`.

---

### Min Stack — O(1) getMin

> [!IMPORTANT]
> **The Click Moment**: "Stack that supports **getMin** in O(1)" — OR — "track minimum with push/pop". Maintain a parallel auxiliary stack storing the current minimum at each depth level.

```python
class MinStack:
    def __init__(self):
        self._stack: list[int] = []
        self._min_stack: list[int] = []  # min_stack[i] = min of stack[0:i+1]

    def push(self, val: int) -> None:
        self._stack.append(val)
        self._min_stack.append(min(val, self._min_stack[-1] if self._min_stack else val))

    def pop(self) -> None:
        self._stack.pop()
        self._min_stack.pop()

    def top(self) -> int:
        return self._stack[-1]

    def get_min(self) -> int:
        return self._min_stack[-1]
```

---

### Expression Evaluation (Basic Calculator)

> [!IMPORTANT]
> **The Click Moment**: "Evaluate expression with `+`, `-`, parentheses" — OR — "Basic Calculator I/II/III". A stack saves the running result and sign when entering a new parenthesis level; on `)`, restore the previous context.

```python
def calculate(s: str) -> int:
    stack: list[int] = []
    result = 0
    sign = 1
    i = 0
    while i < len(s):
        ch = s[i]
        if ch.isdigit():
            num = 0
            while i < len(s) and s[i].isdigit():
                num = num * 10 + int(s[i])
                i += 1
            result += sign * num
            continue
        elif ch == '+':
            sign = 1
        elif ch == '-':
            sign = -1
        elif ch == '(':
            stack.append(result)   # save current result
            stack.append(sign)     # save sign before '('
            result = 0
            sign = 1
        elif ch == ')':
            result = stack.pop() * result + stack.pop()  # sign * inner + outer
        i += 1
    return result
```

---

## 3. SDE-3 Deep Dives

### Scalability: Stream Processing with Monotonic Stack

> [!TIP]
> Monotonic stacks process data in a **single pass** with O(N) total work — ideal for streaming. For the "next greater element in a stream", you can maintain a persistent monotonic stack across arrivals: new elements resolve pending queries for all smaller elements in the stack. This is the architecture behind real-time alert systems ("when does this metric first exceed threshold X?").

For very large streams that don't fit in memory: partition the stream into chunks, compute NGE within each chunk, then handle cross-chunk boundaries with a reconciliation pass — the unresolved tail of each chunk is a small monotonic stack passed forward.

### Concurrency: Thread-Safe Stacks

> [!TIP]
> **Java**: `ArrayDeque` is not thread-safe. Use `Deque<T>` wrapped with `Collections.synchronizedDeque()`, or switch to `LinkedBlockingDeque` for producer-consumer patterns. Prefer `LinkedBlockingDeque` when multiple threads push/pop concurrently — it uses two locks (head + tail) for lower contention.
>
> **Lock-free stack**: Treiber's stack uses CAS on the top pointer. `push`: `new.next = top; CAS(top, old_top, new)`. `pop`: `old = top; CAS(top, old, old.next)`. O(1) amortized with retry on CAS failure. Used in JVM's thread-local allocation buffers.
>
> **Python**: Use `collections.deque` with `appendleft`/`popleft` — each operation is thread-safe in CPython due to the GIL, but don't rely on multi-operation atomicity.

### Trade-offs

| Approach | Time per Element | Space | When to Prefer |
| :--- | :--- | :--- | :--- |
| Brute force (nested loop) | O(N) | O(1) | N ≤ 1000; clarity over performance |
| Monotonic stack | O(1) amortized | O(N) | N > 1000; stream processing |
| Sparse table (RMQ) | O(1) query | O(N log N) | Many range-min queries; static data |
| Segment tree | O(log N) query | O(N) | Range queries with updates |
| Two pointers (rain water) | O(N) | O(1) | Rain water specific; simpler than stack |

---

## 4. Common Interview Problems

### Easy
- **Valid Parentheses** — Push opens; pop on close; check match.
- **Min Stack** — Parallel min-tracking stack.
- **Implement Queue using Stacks** — Two stacks: push to in-stack; pop lazy-moves to out-stack.

### Medium
- **Daily Temperatures** — Decreasing monotonic stack of indices.
- **Next Greater Element II** (circular) — Process `2N` indices with `% N`.
- **Evaluate RPN** — Operand stack; on operator, pop two and push result.
- **Decode String** — Stack of `(prefix, repeat_count)` at `[`; unwind on `]`.
- **Exclusive Time of Functions** — Stack of `(id, start)`; pause inner on nested start.
- **Simplify Path** — Split by `/`; stack with `..` logic.

### Hard
- **Largest Rectangle in Histogram** — Monotonic increasing stack; sentinel `0`.
- **Maximal Rectangle** — Histogram per row + above.
- **Trapping Rain Water** — Monotonic stack or two-pointer; stack explains "why" better.
- **Basic Calculator I/II/III** — Two-stack or single stack with sign tracking.
- **Maximum Frequency Stack** — FreqStack: push increments freq; pop from highest-freq bucket.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **[Daily Temperatures](../../google-sde2/PROBLEM_DETAILS.md#daily-temperatures)** | "Days until warmer" | Decreasing stack of indices; `result[j] = i - j` | Store **indices**, not values — need distance computation. |
| **Next Greater Element II** | "Next greater in circular array" | Iterate `0..2N-1` with `% N`; same monotonic stack | Never push index `i % N` when `i >= N` — only query, don't double-add. |
| **[Largest Rectangle](../../google-sde2/PROBLEM_DETAILS.md#largest-rectangle-in-histogram)** | "Max area in histogram" | Increasing stack; pop on lower bar; width = `i - stack[-1] - 1` | Empty stack after pop → `width = i` (bar is global minimum so far). |
| **Maximal Rectangle** | "Max rectangle of 1s in matrix" | Build histogram row by row; run LRH each row | Heights reset to 0 on encountering `'0'`; LRH applied to each row. |
| **[Valid Parentheses](../../google-sde2/PROBLEM_DETAILS.md#valid-parentheses)** | "Matching nested brackets" | Push open; pop on close and verify | Check `not stack` before peek — empty stack on close char = invalid. |
| **Min Stack** | "O(1) getMin with push/pop" | Parallel min-stack synced with main | Popping from both stacks atomically; duplicates in min-stack are fine. |
| **[Decode String](../../google-sde2/PROBLEM_DETAILS.md#decode-string)** | "Nested repetition decoding" | Stack `(built_string, repeat_k)` on `[`; unwind on `]` | Multi-digit `k`; deeply nested `"3[a2[c]]"` must handle stack depth. |
| **Exclusive Time of Functions** | "Non-overlapping function runtimes" | Stack of `(id, start)`; on end: `time += end - start + 1` | Nested calls: pause outer by subtracting inner's duration from outer's start time. |
| **[Trapping Rain Water](../../google-sde2/PROBLEM_DETAILS.md#trapping-rain-water)** | "Water trapped between bars" | Decreasing stack; pop and compute water above popped bar | Stack approach is more intuitive for "explain why"; two-pointer is simpler to code. |
| **Maximum Frequency Stack** | "Pop most frequent; ties: most recent" | Map `freq→[elements]`; map `val→freq`; track `max_freq` | On pop, decrement `max_freq` if top bucket becomes empty. |

---

## See also

- [Queue](queue.md) — monotonic deque for sliding window max/min
- [Graph](../algorithms/graph.md) — iterative DFS uses an explicit stack
- [Greedy](../algorithms/greedy.md) — some monotonic stack problems have greedy structure
- [Patterns Master](../../../reference/patterns/patterns-master.md) — monotonic stack pattern triggers
