# Queue

A linear data structure operating on the **FIFO (First In, First Out)** principle.

## Key Concepts
- **Core Operations**: Enqueue (add to rear), Dequeue (remove from front), Peek/Front, isEmpty (all $O(1)$ time).
- **Implementations**:
  - *Array-based*: Prone to wasted space at the front as elements are dequeued.
  - *Circular Queue*: Connects the end of the array to the front to reuse space.
  - *Linked List-based*: Dynamic size, no wasted space.
- **Applications**:
  - Breadth-First Search (BFS) in trees/graphs.
  - CPU & Task Scheduling, Printer Spools, Call Centers.
  - Caching (e.g., LRU Cache components).

## Important Variations
- **Priority Queue**: Elements are dequeued based on priority (usually backed by a Heap), not insertion order. Insert/Extract in $O(\log N)$.
- **Deque (Double-Ended Queue)**: Insert or remove from *both* front and rear in $O(1)$. 
  - *Crucial for*: Sliding Window Maximum problems.

## Common SDE-3 Queue Problems
- *Easy*: Implement Queue using Stacks, Moving Average from Data Stream.
- *Medium*: Design Circular Queue, LRU Cache, Rotten Oranges.
- *Hard*: Sliding Window Maximum, Maximum of Minimums of Every Window Size, Design Snake and Ladder Game.
