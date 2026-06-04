---
module: 01-data-structures
topic: Stack
subtopic: 
status: unread
tags: [data-structures, stack]
---

← [Data structures index](./README.md) · [DS decision tree](./ds_tree.md)
## First-Principles Map

```
WHY stacks exist → WHAT they are → HOW they work → WHEN to use → WHAT can go wrong
       │                 │                │               │               │
  [Recursion and      [LIFO abstract   [push to top;  [expression       [stack overflow
   expression         data type;        pop from top;  parsing, DFS,     on deep recursion;
   parsing require    backed by         peek is O(1);  undo/redo,        monotonic stack
   last-in-first-     array or linked   all ops O(1)   backtracking,     misuse if invariant
   out semantics]     list]             amortized]     call frames]      not maintained]
       │                 │                │
  [real-world:        [invariant:      [monotonic stack: maintain
   stack of plates    top always        increasing/decreasing order
   — only access      points to most    to find next greater/smaller
   the top]           recent element]   element in O(n) total]
       ↓
[Decision: Stack vs alternatives]
  ├── vs Queue       → LIFO vs FIFO; stack for DFS/backtrack, queue for BFS/levels
  ├── vs Recursion   → explicit stack avoids call-stack overflow, same semantics
  └── vs Deque       → deque generalizes stack; use stack when LIFO is all you need
```

## First-Principles Breakdown
- **Root problem**: Many algorithms (expression eval, DFS, undo) need to process the most recently seen item first — LIFO ordering.
- **Core insight**: Restricting access to one end (the top) enforces LIFO and enables O(1) push/pop without any shifting.
- **Invariant**: The top element is always the most recently pushed, not-yet-popped element.
- **Why it's fast**: Push/pop only touch the top pointer — no traversal, no rebalancing, O(1) always.
- **Where it breaks**: Unbounded recursion overflows the call stack; monotonic stack loses its invariant if push/pop conditions are wrong; not suitable when you need arbitrary access.

# Stack — SDE-3 Gold Standard

```
[STACK]
├── WHY IT EXISTS
│   ├── Problem it solves: track state in reverse-chronological order; undo the most recent action first
│   ├── Without it: managing "what was the last open thing" requires O(N) array scan
│   └── Real-world analogy: stack of plates — you always take from (and add to) the top
├── WHAT IT IS (First Principles)
│   ├── Core property: LIFO — Last In, First Out; only the top element is accessible
│   ├── Abstract data type: push, pop, peek operations; implementation-agnostic
│   ├── Implementation — array: push/pop at tail, O(1) amortized, cache-friendly (preferred)
│   └── Implementation — linked list: push/pop at head, O(1) guaranteed, more memory overhead
├── HOW IT WORKS
│   ├── Push: add element to top → O(1)
│   ├── Pop: remove and return top element → O(1)
│   ├── Peek/Top: return top without removing → O(1)
│   ├── isEmpty: check if stack is empty → O(1)
│   └── All operations are at one end — the top
├── KEY TECHNIQUES (SDE-3)
│   ├── Monotonic Stack — the most critical SDE-3 pattern
│   │   ├── Monotonic increasing: pop while top ≥ current → finds next smaller element
│   │   ├── Monotonic decreasing: pop while top ≤ current → finds next greater element
│   │   ├── Each element pushed/popped at most once → O(N) total
│   │   └── Problems: next greater element, largest rectangle in histogram, trapping rain water
│   ├── Expression parsing
│   │   ├── Balanced parentheses: push opens, pop on close, check match
│   │   └── Evaluate RPN / infix→postfix conversion
│   ├── DFS simulation: replace recursion stack with explicit stack (avoids stack overflow)
│   ├── Min-stack: maintain auxiliary stack tracking current minimum → O(1) getMin
│   └── Stack with deque extension: deque supports O(1) at both ends → sliding window max
├── COMPLEXITY
│   ├── Time — push/pop/peek: O(1) all operations
│   ├── Time — monotonic stack over N elements: O(N) total (each element processed once)
│   └── Space: O(N) worst case (all elements pushed, none popped)
└── WHEN TO USE vs ALTERNATIVES
    ├── Use stack when: need LIFO order, undo/redo, DFS traversal, expression evaluation
    ├── Use monotonic stack when: "next greater/smaller" for each element in O(N)
    ├── Use queue when: FIFO order needed (BFS, scheduling)
    ├── Use deque when: need O(1) access at both ends (sliding window, palindrome check)
    └── Avoid stack when: random access to elements is needed
```

LIFO (Last In, First Out) structure. SDE-3 focus: **monotonic stack** for "next greater/smaller" in O(N), expression parsing, and the deque extension for sliding window problems.


> [!abstract] Google Interview Legend
> `🔥 Google` — **Core** problem: extremely high frequency at Google SDE 2/3 interviews. Cover these first.
> `⭐ Google` — **Important** problem: medium frequency at Google SDE 2/3 level. Cover after core.
> Problems without a marker are good practice but less Google-specific at SDE 2/3 level.

---

## Theory & Mental Models

**What it is:** An abstract data type where all insertions (push) and deletions (pop) happen at the same end — the top. Core invariant: LIFO — the most recently pushed item is always the next to be popped.

**Why it exists:** Solves the problem of tracking "last relevant" state and undoing or replaying operations. Real-world analogy: a stack of plates — you always take from the top; the bottom plate was the first placed and last removed.

**Memory layout:** Implemented as a dynamic array (Python `list`) or linked list. Dynamic array gives O(1) amortized push/pop with good cache locality. Linked list gives O(1) push/pop with overhead of pointer allocation per node.

**Key invariants:**
- All insert and delete operations touch only the top — never middle or bottom.
- Pop on an empty stack is undefined (check `not stack` before popping).
- The top of the stack reflects the most recent state; the bottom reflects the earliest unresolved state.

**Complexity at a glance:**

| Operation | Time | Notes |
| :--- | :--- | :--- |
| Push | O(1) amortized | Array append |
| Pop | O(1) | Remove top |
| Peek (top) | O(1) | `stack[-1]` in Python |
| Search | O(N) | Must scan entire stack |
| Space | O(N) | N elements stored |

**When to reach for it:**
- Undo/redo operations — each action is a frame; undo pops the top frame.
- Balanced parentheses / nested structure validation.
- Iterative DFS — explicit stack replaces the call stack.
- Monotonic relationships: next greater element, largest rectangle, daily temperatures.
- Expression evaluation with operator precedence (Basic Calculator variants).

**Common mistakes:**
- Not checking `not stack` before calling `pop()` or accessing `stack[-1]` — causes `IndexError`.
- Confusing push/pop order when simulating a process — trace through a small example first.
- Storing values instead of indices on the stack — you lose position info needed for distance or result-array filling.
- Not resetting the stack between test cases in batch-input problems.

---

## 1. Concept Overview

**Problem space**: Next Greater/Smaller Element (NGE/NSE), largest rectangle in histogram, trapping rain water, expression evaluation, valid parentheses, DFS simulation, decode string, exclusive function time.

**When to use**: You need the "last relevant" element — OR — you're tracking a sequence where older elements become irrelevant once a newer one is processed.

---

## 2. Core Algorithms & Click Moments

### Monotonic Stack — Next Greater Element

> [!IMPORTANT]
> **The Click Moment**: "**Next greater `⭐ Google`** element to the right" — OR — "**nearest smaller** to the left" — OR — "**daily temperatures `🔥 Google`**, span, or stock price" problems. Any problem asking "for each element, find the first X in one direction" maps to a monotonic stack. Brute force is O(N²); monotonic stack is O(N) — each element pushed and popped exactly once.

- **Decreasing stack** (top = smallest): when a larger element arrives, all smaller stack elements have found their Next Greater → pop and record.
- **Increasing stack** (top = largest): when a smaller element arrives, pop and record Next Smaller.

> [!TIP]
> Think of a monotonic stack as a bouncer at a club — when a new VIP arrives (larger element), the bouncer kicks out everyone shorter in the line before them. The kicked-out elements have found their "next greater"; the VIP takes their place. This is why each element is pushed and popped exactly once: O(N) total.

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

#### Common Variants & Twists
1. **Next Greater Element II (Circular Array Twist) `⭐ Google`**:
   - **What (The Problem & Goal):** Find the next greater element, but the array is circular (the element after the last element is the first element).
   - **How (Intuition & Mental Model):** To simulate a circular array, iterate from `0` to `2*N - 1` and use the modulo operator `i % N` to wrap around. Use the exact same monotonic stack logic, but be careful not to double-push elements on the second pass (only query the stack).
2. **Daily Temperatures `🔥 Google`**:
   - **What (The Problem & Goal):** Given an array of temperatures, return an array answering "how many days do you have to wait until a warmer temperature?"
   - **How (Intuition & Mental Model):** This is the classic Next Greater Element problem in disguise. Instead of storing the *value* of the next greater element, you store the *distance* (difference in indices) by computing `current_index - stack.pop()`.
3. **Online Stock Span `⭐ Google`**:
   - **What (The Problem & Goal):** You receive elements one by one (online). For each element, find how many consecutive previous days had a price `<=` today's price.
   - **How (Intuition & Mental Model):** Keep a monotonic decreasing stack of tuples: `(price, span)`. When a new price arrives, pop all prices `<= current`. As you pop, accumulate their spans. The current element's span becomes `1 + sum_of_popped_spans`.

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

#### Common Variants & Twists
1. **Basic Calculator II (Precedence Twist) `🔥 Google`**:
   - **What (The Problem & Goal):** The expression has `*` and `/` (higher precedence) alongside `+` and `-`, but no parentheses.
   - **How (Intuition & Mental Model):** Maintain a stack of numbers that will simply be summed up at the very end. Keep track of the *previous operator* seen. If it was `+` or `-`, push the number (or its negative). If it was `*` or `/`, immediately pop the top of the stack, perform the multiplication/division with the current number, and push the result back.
2. **Decode String (Nested String Twist) `⭐ Google`**:
   - **What (The Problem & Goal):** Decode a string like `3[a2[c]]` into `accaccacc`.
   - **How (Intuition & Mental Model):** The stack stores "context" just like parentheses in math. When seeing `[`, push a tuple `(string_built_so_far, repeat_count)` onto the stack and reset your current trackers. When seeing `]`, pop the context, multiply your current inner string by `repeat_count`, and append it to `string_built_so_far`.

---

### Asteroid Collision (Positive vs Negative Cancellation)

> [!IMPORTANT]
> **The Click Moment**: "Elements moving in **opposite directions** annihilate each other based on size." The stack represents surviving elements moving right (positive). When a left-moving element (negative) arrives, it repeatedly collides with the top of the stack until one or both are destroyed.

```python
def asteroid_collision(asteroids: list[int]) -> list[int]:
    stack: list[int] = []
    for ast in asteroids:
        # Collision only happens when stack top is positive and current is negative
        while stack and stack[-1] > 0 and ast < 0:
            if stack[-1] < abs(ast):
                stack.pop()
                continue
            elif stack[-1] == abs(ast):
                stack.pop()
            break  # Current asteroid is destroyed
        else:
            # Reached if the while loop completes without breaking
            stack.append(ast)
    return stack
```

> [!TIP]
> Using the `while ... else` construct in Python is perfect here: the `else` block executes only if the loop finishes naturally (the negative asteroid destroyed everything in its path or the stack was empty/had negative top). If the loop breaks (the current asteroid was destroyed), the `else` block is skipped and the asteroid is not appended.

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
- **Valid Parentheses `🔥 Google`** — Push opens; pop on close; check match.
- **Min Stack `🔥 Google`** — Parallel min-tracking stack.
- **Implement Queue using Stacks** — Two stacks: push to in-stack; pop lazy-moves to out-stack.

### Medium
- **Daily Temperatures `🔥 Google`** — Decreasing monotonic stack of indices.
- **Next Greater Element II `⭐ Google`** (circular) — Process `2N` indices with `% N`.
- **Evaluate RPN** — Operand stack; on operator, pop two and push result.
- **Decode String `⭐ Google`** — Stack of `(prefix, repeat_count)` at `[`; unwind on `]`.
- **Exclusive Time of Functions `⭐ Google`** — Stack of `(id, start)`; pause inner on nested start.
- **Simplify Path** — Split by `/`; stack with `..` logic.

### Hard
- **Largest Rectangle in Histogram `🔥 Google`** — Monotonic increasing stack; sentinel `0`.
- **Maximal Rectangle `⭐ Google`** — Histogram per row + above.
- **Trapping Rain Water `🔥 Google`** — Monotonic stack or two-pointer; stack explains "why" better.
- **Basic Calculator I/II/III `🔥 Google`** — Two-stack or single stack with sign tracking.
- **Maximum Frequency Stack `⭐ Google`** — FreqStack: push increments freq; pop from highest-freq bucket.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **[Daily Temperatures](../02-algorithms/problem-deep-dives.md#daily-temperatures) `🔥 Google`** | Monotonic Stack (Decreasing) | "Days until warmer" | Decreasing stack of indices; `result[j] = i - j` | Store **indices**, not values — need distance computation. |
| **Next Greater Element II `⭐ Google`** | "Next greater in circular array" | Iterate `0..2N-1` with `% N`; same monotonic stack | Never push index `i % N` when `i >= N` — only query, don't double-add. |
| **[Largest Rectangle](../02-algorithms/problem-deep-dives.md#largest-rectangle-in-histogram) `🔥 Google`** | "Max area in histogram" | Increasing stack; pop on lower bar; width = `i - stack[-1] - 1` | Empty stack after pop → `width = i` (bar is global minimum so far). |
| **Maximal Rectangle `⭐ Google`** | "Max rectangle of 1s in matrix" | Build histogram row by row; run LRH each row | Heights reset to 0 on encountering `'0'`; LRH applied to each row. |
| **[Valid Parentheses](../02-algorithms/problem-deep-dives.md#valid-parentheses) `🔥 Google`** | "Matching nested brackets" | Push open; pop on close and verify | Check `not stack` before peek — empty stack on close char = invalid. |
| **Min Stack `🔥 Google`** | "O(1) getMin with push/pop" | Parallel min-stack synced with main | Popping from both stacks atomically; duplicates in min-stack are fine. |
| **[Decode String](../02-algorithms/problem-deep-dives.md#decode-string) `⭐ Google`** | "Nested repetition decoding" | Stack `(built_string, repeat_k)` on `[`; unwind on `]` | Multi-digit `k`; deeply nested `"3[a2[c]]"` must handle stack depth. |
| **Exclusive Time of Functions `⭐ Google`** | "Non-overlapping function runtimes" | Stack of `(id, start)`; on end: `time += end - start + 1` | Nested calls: pause outer by subtracting inner's duration from outer's start time. |
| **[Trapping Rain Water](../02-algorithms/problem-deep-dives.md#trapping-rain-water) `🔥 Google`** | "Water trapped between bars" | Decreasing stack; pop and compute water above popped bar | Stack approach is more intuitive for "explain why"; two-pointer is simpler to code. |
| **Maximum Frequency Stack `⭐ Google`** | "Pop most frequent; ties: most recent" | Map `freq→[elements]`; map `val→freq`; track `max_freq` | On pop, decrement `max_freq` if top bucket becomes empty. |
| **Balanced Parentheses** [E] | "Check if brackets are balanced" | Push open brackets; on close check top matches; stack empty at end | Map `')': '('` for clean matching; early return if stack empty on close. |
| **Baseball Game** [E] | "Simulate score with ops `+`, `D`, `C`, int" | Stack; `+` sums top two; `D` doubles top; `C` pops top | Process in order; `+` looks at top two without popping them before pushing sum. |
| **Remove All Adjacent Duplicates** [E] | "Repeatedly remove adjacent equal pairs" | Stack; push if top ≠ curr; pop if top == curr | Result is remaining stack joined — equivalent to cancellation like bracket matching. |
| **Asteroid Collision `⭐ Google`** [M] | "Positive (right) and negative (left) collide; larger survives" | Stack; negative asteroid collides with positive top | Same size → both explode. Negative vs negative → no collision (both going left). |
| **Online Stock Span `⭐ Google`** [M] | "Days where price ≤ today's for consecutive run" | Monotonic decreasing stack of `(price, span)`; merge spans | On pop, accumulate `span += popped_span` — key: spans propagate multiplicatively. |
| **Remove K Digits `⭐ Google`** [M] | "Remove K digits to form smallest number" | Monotonic increasing stack; pop when top > curr and k > 0 | Strip leading zeros from result. If k > 0 after loop, trim last k from stack (they're already sorted). |
| **Sum of Subarray Minimums `⭐ Google`** [M] | "Sum of min of every contiguous subarray" | Monotonic stack; compute left and right boundaries for each element as minimum | `answer += stack_val * left_count * right_count`; left boundary uses strict `<`, right uses `<=` to avoid double-counting equal values. |
| **Largest Rectangle in Histogram `🔥 Google`** [H] | "Max area rectangle in bar chart" | Monotonic increasing stack; for each bar compute max width it can span | Width = `right_boundary - left_boundary - 1`; append sentinel `0` to flush remaining stack at end. |
| **Basic Calculator II `🔥 Google`** [M] | "Evaluate expression with `+`, `-`, `*`, `/`" | Stack; flush on `+`/`-`; compute `*`/`/` with last operand | Unary minus: treat as `0 - ...`. Integer division truncates toward zero in Python use `int(a/b)` not `a//b` for negatives. |
| **Validate Stack Sequences** [M] | "Can `pushed` sequence produce `popped`?" | Simulate: push elements; pop greedily when top matches `popped[j]` | If stack is empty at end, sequences are valid. Greedy pop is always safe — no benefit to delaying. |

---

## Quick Revision Triggers

- If the problem says "next greater/smaller element" → think Monotonic Stack; brute force O(N²) → stack O(N) because each element pushed/popped once.
- If the problem says "valid brackets" or "nested structure matching" → think Stack; push on open, pop-and-verify on close.
- If the problem says "undo/redo" or "backtrack to previous state" → think Stack because LIFO naturally reverses recent actions.
- If the problem says "largest rectangle in histogram" → think Monotonic Increasing Stack; pop when a shorter bar arrives, compute width using remaining stack top.
- If the problem says "evaluate expression with parentheses" → think Stack saving `(result, sign)` context on `(` and restoring on `)`.
- If the problem says "iterative DFS" → think explicit Stack replacing the call stack; push neighbors in reverse order to preserve traversal direction.
- If the problem needs O(1) getMin with push/pop → think Parallel Min-Stack synced with main stack.

## See also

- [Queue](queue.md) — monotonic deque for sliding window max/min
- [Graph](../02-algorithms/graph.md) `⭐ Google` — iterative DFS uses an explicit stack
- [Greedy](../02-algorithms/greedy.md) — some monotonic stack problems have greedy structure
- [Patterns Master](../03-patterns/patterns-master.md) — monotonic stack pattern triggers

## Flashcards

**What is a Monotonic Stack, and why does it achieve O(N) time complexity for finding the Next Greater Element?** #flashcard
A Monotonic Stack is a stack that maintains its elements in a sorted (increasing or decreasing) order. It runs in $O(N)$ because each array element is pushed onto the stack exactly once and popped at most once, leading to an amortized $O(1)$ operations per element.

**How does a Monotonic Increasing Stack solve the "Largest Rectangle in Histogram" problem in O(N) time?** #flashcard
Maintain indices of bars in increasing height order. When a shorter bar of height $H$ at index $i$ is found:
1. Pop the top index `cur` as the rectangle height.
2. The new stack top index is the left boundary.
3. The width of the rectangle is `i - stack[-1] - 1` (or `i` if stack is empty).
4. Calculate the area and update max. Repeat until the stack top is shorter than $H$.

**Describe the Min-Stack architecture for O(1) minimum element retrieval.** #flashcard
Maintain a main stack for values and a parallel `min_stack` for running minimums.
- **Push**: Push $X$ to the main stack, and push $\min(X, \text{min\_stack}[-1])$ to `min_stack`.
- **Pop**: Pop from both stacks.
- **GetMin**: Return the top of `min_stack`.

**How do you evaluate nested arithmetic expressions containing parentheses "()" using a stack?** #flashcard
Maintain a running `result` and `sign` (1 or -1).
- When seeing `(`, push the current `(result, sign)` onto the stack and reset both.
- When seeing `)`, pop the sign and previous result, update the sub-expression value: `result = prev_result + prev_sign * result`.

**Why must neighbors be pushed onto the stack in reverse order during iterative DFS?** #flashcard
Because stacks are Last-In-First-Out (LIFO). To process nodes from left to right (same order as recursion), you must push them onto the stack from right to left so the leftmost neighbor ends up at the top of the stack and is popped first.

