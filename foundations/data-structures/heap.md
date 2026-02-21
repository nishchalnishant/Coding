# Heap / Priority Queue

A specialized tree-based data structure that satisfies the **heap property**, typically used to implement Priority Queues.

## Key Concepts
- **Heap Property**: 
  - *Max-Heap*: Parent $\ge$ Children. Root is the maximum element.
  - *Min-Heap*: Parent $\le$ Children. Root is the minimum element.
- **Representation**: Usually implemented as a 0-indexed array.
  - *Left Child*: `2i + 1`
  - *Right Child*: `2i + 2`
  - *Parent*: `(i - 1) // 2`
- **Operations**:
  - *Peek*: $O(1)$.
  - *Insert/Push*: $O(\log N)$ (add to end, bubble up).
  - *Pop/Extract*: $O(\log N)$ (swap root with last element, bubble down).
  - *Heapify*: $O(N)$ to build a heap from an unsorted array bottom-up.

## Core Techniques
- **Top K Elements**: Track the "K largest" elements using a *Min-Heap* of size K. Track the "K smallest" using a *Max-Heap* of size K.
- **K-Way Merge**: Merge $K$ sorted lists efficiently in $O(N \log K)$ by pushing the first element of each list into a Min-Heap.
- **Two Heaps**: Used for tracking dynamic medians. A Max-Heap stores the smaller half, a Min-Heap stores the larger half.

## Common SDE-3 Heap Problems
- *Easy*: Kth Largest Element in a Stream.
- *Medium*: K Closest Points to Origin, Top K Frequent Elements, Reorganize String, Task Scheduler.
- *Hard*: Find Median from Data Stream, Merge K Sorted Lists, Sliding Window Median, IPO.
