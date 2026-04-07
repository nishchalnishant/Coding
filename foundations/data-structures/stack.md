# Stack — SDE-2+ Level

LIFO (Last In, First Out) structure. SDE-3 focus: monotonic stack for "next greater/smaller", expression parsing, and when to prefer stack over other structures.

---

## 1. Concept Overview

**Problem space**: Next Greater/Smaller Element (NGE/NGSE), largest rectangle in histogram, trapping rain water, expression evaluation, valid parentheses, DFS (iterative).

**When to use**: Need "last relevant" or "nearest previous/next" element; nesting/recursion simulation; undo/redo.

---

## 2. Core Algorithms

### Monotonic Stack (Next Greater Element)
- Keep stack in decreasing order (top = smallest in stack). For each `i`: pop while `A[stack[-1]] < A[i]` → NGE of `stack[-1]` is `i`; push `i`.
- **Complexity**: O(N) time, O(N) space.

### Largest Rectangle in Histogram
- For each bar, find left and right boundaries (first smaller on left/right) via two monotonic stacks (or one pass storing indices). Area = height[i] * (right - left - 1).
- **Complexity**: O(N).

### Valid Parentheses
- Push opening; on closing, pop and check match. Final stack must be empty.

---

## 3. Advanced Variations

- **Min/Max Stack**: Auxiliary stack storing current min (or max) per level; push/pop both in sync. O(1) getMin/getMax.
- **[Trapping Rain Water](../../google-sde2/PROBLEM_DETAILS.md#trapping-rain-water)**: Monotonic stack (decreasing by height): when a higher bar appears, pop and add water level above popped bar. Alternative: two pointers (left_max, right_max).
- **Basic Calculator**: Two stacks (operands, operators); handle precedence and parentheses.

### Edge Cases
- Empty input; single element; all same height (histogram); negative numbers; overflow in expression.

---

## 4. Common Interview Problems

**Easy**: Valid Parentheses, Implement Queue using Stacks, Min Stack.  
**Medium**: Evaluate RPN, Next Greater Element II, Daily Temperatures, Decode String.  
**Hard**: Largest Rectangle in Histogram, Trapping Rain Water, Maximum Frequency Stack, Basic Calculator.

---

## 5. Pattern Recognition

- **Monotonic stack (decreasing)**: NGE, next greater to right; (increasing): next smaller.
- **Monotonic stack + area**: Histogram rectangle — extend while top >= current, then compute width from stored indices.
- **Matching/nesting**: Parentheses, tags — push open, pop on close and validate.
- **Expression**: Infix → postfix (shunting-yard) or direct two-stack calculator.

---

## 6. Code Implementations

More SDE-2 reference implementations (Python): `../../google-sde2/snippets/python/stack_queue.py`.

```python
def next_greater_element(nums):
    n = len(nums)
    result = [-1] * n
    stack = []
    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            result[stack.pop()] = nums[i]
        stack.append(i)
    return result

def largest_rectangle_area(heights):
    stack = []
    best = 0
    for i, h in enumerate(heights + [0]):
        while stack and heights[stack[-1]] > h:
            j = stack.pop()
            width = i if not stack else i - stack[-1] - 1
            best = max(best, heights[j] * width)
        stack.append(i)
    return best
```

---

## 7. Trade-offs & Scaling (optional)

- **Trade-offs**: Monotonic stack gives O(N) for "next greater" vs O(N²) brute force. Two pointers for rain water can be O(1) space; stack is more general for "bounded by next greater" thinking.
- **Scalability**: Stack depth = at most N; consider recursion limit (use iterative stack for deep DFS).
- **Memory**: One stack for NGE O(N); two stacks for min-stack O(N).

---

## 8. Interview Strategy

- **Identify**: "Next greater/smaller" → monotonic stack. "Largest rectangle" → histogram + NSE both sides. "Matching pairs" → stack.
- **Approach**: Explain why stack maintains "candidates" and why popped elements have found their answer.
- **Common mistakes**: Wrong monotonic order; off-by-one in width calculation; forgetting sentinel (e.g., 0 at end for histogram).

---

## 9. Quick Revision

- **Tricks**: Decreasing stack → NGE; increasing → NSE. Histogram: pop and compute width using current index and new top.
- **Edge cases**: Empty, single bar, all equal, duplicate values (use indices, not values).
- **Pattern tip**: "Next greater" / "previous smaller" → monotonic stack; "valid brackets" → push/pop match.

---

## Interview Questions — Logic & Trickiness

| Question | Core logic | Trickiness & details |
|----------|------------|----------------------|
| **[Daily Temperatures](../../google-sde2/PROBLEM_DETAILS.md#daily-temperatures)** | **Monotonic decreasing stack of indices**; for each `i`, while stack top has lower temp, pop `j` and set `answer[j]=i-j`. | **Indices** on stack; **no warmer** → 0. **O(n)** each index pushed/popped once. |
| **Next Greater Element I** | Monotonic **decreasing** value stack; when see greater, assign NGE for popped. **Circular:** iterate `2n` or modulo. | **Per-query** vs preprocess; **-1** if none. |
| **[Largest Rectangle in Histogram](../../google-sde2/PROBLEM_DETAILS.md#largest-rectangle-in-histogram)** | Stack of **increasing** indices; on lower bar, pop `h`; width = `i - stack.top - 1` (after pop). Append **0** sentinel at end. | **Empty stack** after pop → width `i`; **equal** heights—index stack handles. |
| **Maximal Rectangle** (matrix) | For each row, build **heights** histogram; run **largest rectangle** per row. | **O(n*m)**; compress matrix to 1D histogram sweep. |
| **[Valid Parentheses](../../google-sde2/PROBLEM_DETAILS.md#valid-parentheses)** | Push on `(` `[` `{`; on close, pop must match type. | **Early** invalid if stack empty; **only one type** in easy version. |
| **Min Stack** | **Aux stack** of mins, or store `(val, min_so_far)` per node. | **Pop** must restore min; **duplicate** min values in aux stack. |
| **[Decode String](../../google-sde2/PROBLEM_DETAILS.md#decode-string)** | Stack of `(prefix_string, repeat_k)` at `[`; on `]` pop and repeat. **Recursion** also works. | **Multi-digit** `k`; **nested** brackets. |
| **Exclusive Time of Functions** | Stack of `(id, start)`; on **end**, add `timestamp - start + 1` to id; pause inner on nested start. | **Timestamp** inclusive; **nested** functions subtract overlap correctly. |
| **Simplify Path** | Split `/`; stack for `..` (pop if non-empty), ignore `.` and empty. | **Root** `..` doesn’t pop; **trailing** slash. |
| **[Trapping Rain Water](../../google-sde2/PROBLEM_DETAILS.md#trapping-rain-water)** (stack) | Stack of **decreasing** heights; pop and compute water between popped and current with boundary. | Equivalent insight to **two pointers**; good for “why stack” explanation. |

---

## See also

- [Queue](queue.md) — monotonic deque for sliding window max  
- [Graph](../algorithms/graph.md) — DFS uses implicit stack  
- [Greedy](../algorithms/greedy.md) — some stack problems have greedy structure
