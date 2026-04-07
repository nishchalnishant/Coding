# Stack — SDE-3 Level

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
- **Trapping Rain Water**: Monotonic stack (decreasing by height): when a higher bar appears, pop and add water level above popped bar. Alternative: two pointers (left_max, right_max).
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

## 7. SDE-3 Level Thinking

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

| Question | Core logic | Trickiness |
|----------|------------|------------|
| **Daily Temperatures** | Decreasing index stack; warmer day pops and assigns | Store **indices**, not temps; end of array |
| **Largest Rectangle Histogram** | Pop when lower bar; width = `i - new_top - 1` | Sentinel `0` height at end; empty stack width |
| **Valid Parentheses** | Push opens; pop match on close | `[{` type mismatch; only `()` in easy variant |
| **Decode String** | Stack of `(string, k)` at `[`; repeat on `]` | Multi-digit `k`; nested `a2[b3[c]]` |
| **Trapping Rain Water** (stack) | Pop when current higher; compute water between | Same as array two-pointer but stack mental model |

---

## See also

- [Queue](queue.md) — monotonic deque for sliding window max  
- [Graph](../algorithms/graph.md) — DFS uses implicit stack  
- [Greedy](../algorithms/greedy.md) — some stack problems have greedy structure
