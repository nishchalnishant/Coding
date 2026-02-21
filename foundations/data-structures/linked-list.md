# Linked List

A linear data structure where elements (nodes) are stored in non-contiguous memory, connected via pointers.

## Key Concepts
- **Structure**: Node contains `Data` and `Next` pointer.
- **Memory**: Dynamic allocation. No wasted space, but extra overhead for pointers.
- **Operations**:
  - *Insertion/Deletion* at known node: $O(1)$.
  - *Lookup/Search*: $O(N)$. No random access.

## Types
- **Singly Linked**: `Next` pointer only.
- **Doubly Linked**: `Prev` and `Next` pointers (allows backward traversal, easier deletion).
- **Circular**: Last node points to the first node.

## Core Techniques
- **Dummy Node**: A fake head node to simplify edge cases when inserting/deleting at the true head.
- **Two Pointers (Fast & Slow)**: 
  - *Find Middle*: Fast moves by 2, Slow by 1.
  - *Detect Cycle*: Floyd’s Tortoise and Hare.
- **In-place Reversal**: Maintain `prev`, `curr`, and `next` pointers to reverse links iteratively in $O(N)$ time and $O(1)$ space.

## Common SDE-3 Linked List Problems
- *Easy*: Reverse Linked List, Middle of Linked List, Merge Two Sorted Lists, Linked List Cycle.
- *Medium*: Add Two Numbers, Copy List with Random Pointer, Remove Nth Node From End, Reorder List.
- *Hard*: Reverse Nodes in k-Group, Merge k Sorted Lists, LRU Cache.
