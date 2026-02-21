# Stack

A linear data structure operating on the **LIFO (Last In, First Out)** principle.

## Key Concepts
- **Core Operations**: Push, Pop, Peek/Top, isEmpty (all $O(1)$ time).
- **Implementation**: Array-based (fixed size or dynamic) or Linked List-based.
- **Applications**:
  - Reversing sequences (strings, lists).
  - Expression evaluation (Prefix/Postfix, Infix conversion).
  - Function call stacks (Recursion simulation).
  - Depth-First Search (DFS) iterative approach.

## Important Variations & Techniques
- **Monotonic Stack**: Keep elements in strictly increasing/decreasing order.
  - *Use Case*: Finding Next Greater/Smaller element in $O(N)$ time.
  - *Problems*: Daily Temperatures, Largest Rectangle in Histogram.
- **Min/Max Stack**: Maintain auxiliary stack to retrieve current min/max in $O(1)$ time.
- **Balanced Parentheses**: Push open brackets, pop and verify when encountering matching close brackets.
- **Undo/Redo**: Track historical states for quick reversion.

## Common SDE-3 Stack Problems
- *Easy*: Valid Parentheses, Implement Queue using Stacks, Min Stack.
- *Medium*: Evaluate Reverse Polish Notation, Next Greater Element II, Daily Temperatures, Decode String.
- *Hard*: Largest Rectangle in Histogram, Trapping Rain Water, Maximum Frequency Stack, Basic Calculator.
