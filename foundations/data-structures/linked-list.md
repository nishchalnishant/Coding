# Linked List — SDE-2+ Level

A linear data structure where elements (nodes) are stored in non-contiguous memory, connected via pointers. SDE-3 expects clean in-place operations, correct cycle handling, and trade-offs vs arrays.

---

## 1. Concept Overview

### Problem Space
- Reversal (full, in k-groups), reorder (e.g., L0→Ln→L1→Ln-1…).
- Finding middle, detecting cycle, finding cycle entry.
- Merge (two sorted, K sorted), copy with random pointer.
- Dummy node for unified head handling; fast/slow for middle and cycle.

### When to Use
- **Dummy node**: Insert/delete at head; merging lists (avoid null checks).
- **Fast & slow**: Middle (slow 1, fast 2); cycle (Floyd: meet then reset one to head, same step).
- **In-place reversal**: prev/curr/next; O(N) time, O(1) space.

---

## 2. Core Algorithms

### In-Place Reversal
```
prev = null, curr = head
while curr:
  next = curr.next
  curr.next = prev
  prev, curr = curr, next
return prev
```
Time O(N), Space O(1).

### Find Middle (Fast & Slow)
```
slow = fast = head
while fast and fast.next:
  slow = slow.next; fast = fast.next.next
return slow
```
Time O(N), Space O(1).

### Floyd Cycle Detection + Entry
- Phase 1: slow 1 step, fast 2 steps; if they meet → cycle.
- Phase 2: reset one to head; both move 1 step; meeting point = cycle entry.
- Time O(N), Space O(1).

---

## 3. Advanced Variations

- **Reverse in K-Group**: Reverse each k-block; connect tails; handle remainder.
- **Merge K Sorted Lists**: Min-heap of size K (first node of each list); pop min, append, push next. O(N log K).
- **Copy List with Random Pointer**: Old node → new node map; two passes (create nodes, then set next/random).
- **LRU Cache**: HashMap + doubly linked list (head = recent, tail = evict). Get: move to head; Put: add at head, evict tail if over capacity.

### Edge Cases
- Empty list; single node; two nodes; cycle at head; no cycle; even/odd length for middle.

---

## 4. Common Interview Problems

**Easy**: Reverse Linked List, Middle of Linked List, Merge Two Sorted Lists, Linked List Cycle.  
**Medium**: Add Two Numbers, Copy List with Random Pointer, Remove Nth Node From End, Reorder List.  
**Hard**: Reverse Nodes in k-Group, Merge k Sorted Lists, LRU Cache.

---

## 5. Pattern Recognition

- **Dummy node**: Any operation that might change head (delete head, merge).
- **Fast & slow**: Middle, cycle detection, palindrome (reverse second half and compare).
- **In-place reversal**: Full reverse, reverse k-group, reorder list (reverse second half then weave).
- **HashMap for copy**: Random pointer, deep copy with cycles.

---

## 6. Code Implementations

More SDE-2 reference implementations (Python): `../../google-sde2/snippets/python/linked_list.py`.

```python
def reverse_list(head):
    prev = None
    while head:
        nxt = head.next
        head.next = prev
        prev, head = head, nxt
    return prev

def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow == fast:
            return True
    return False

def detect_cycle_entry(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow == fast:
            p = head
            while p != slow:
                p, slow = p.next, slow.next
            return p
    return None
```

---

## 7. Trade-offs & Scaling (optional)

- **Trade-offs**: Linked list vs array — list: O(1) insert/delete at known node, no random access; array: O(1) access, cache-friendly. Use list when insertions/deletions in middle are dominant (e.g., LRU).
- **Memory**: In-place reversal avoids extra list; dummy node uses one extra node (negligible). Copy structures (random pointer) need O(N) map.
- **Concurrency**: Lock-free linked structures (CAS) for queues; mention if asked.

---

## 8. Interview Strategy

- **Identify**: "Reverse", "middle", "cycle", "merge" → standard patterns. "Random pointer" → copy with map.
- **Approach**: Always consider null/one node. Use dummy when head might change. For cycle, state Floyd and then find entry.
- **Common mistakes**: Off-by-one in k-group reversal; forgetting to set tail.next to None; losing reference to next before rewiring.

---

## 9. Quick Revision

- **Formulas**: Middle: fast 2x, slow 1x. Cycle entry: meet then head + meet both step 1.
- **Tricks**: Dummy node; prev/curr/next for reversal; heap for merge K.
- **Edge cases**: Empty, single node, cycle at head, k > length.
- **Pattern tip**: "From end" → two pointers (advance first by n) or stack; "random" → HashMap copy.

---

## Interview Questions — Logic & Trickiness

| Question | Core logic | Trickiness & details |
|----------|------------|----------------------|
| **Reverse Linked List** | Iterative: `prev=null, curr=head`; loop `next=curr.next; curr.next=prev; prev=curr; curr=next`. Recursive: reverse rest then fix `head.next.next`. | **Empty/single** node; **cycle** breaks naive reverse. **Stack** depth O(n) for recursion. |
| **Merge Two Sorted Lists** | Dummy node `d`; compare `l1.val` vs `l2.val`, advance smaller; attach remainder when one empty. | **In-place** vs new list; **reuse nodes** only if allowed. **Follow-up:** merge k lists (heap or divide-conquer). |
| **Remove Nth From End** | Fast pointer advances `n` ahead; then both move until fast hits null; remove `slow.next`. | **Dummy** before head handles removing **first** node. **One pass** requirement. |
| **Linked List Cycle** | Floyd: `slow` 1 step, `fast` 2 steps; meet ⇒ cycle. No meet ⇒ no cycle. | **Null** fast.next check each step. |
| **Linked List Cycle II (entry)** | After meet, move **one** pointer from **head** and one from meet, both **1 step**; meet at entry. | **Proof:** distance equality—often asked. Wrong: restarting **both** from head with different speeds. |
| **Intersection of Two Lists** | Align lengths: walk longer list by `|lenA-lenB|`; then walk both until same node. **Alt:** A+B traversal (switch at end). | **No intersection** → both reach null. **Values** can duplicate; compare **node identity**. |
| **Merge K Sorted Lists** | Min-heap `(val, id, node)`; pop smallest, push `node.next`. **Divide & conquer** pairwise merge O(N log k). | **Empty** lists in heap; **tie-break** on list id for stability. **Time:** O(N log k) heap. |
| **Copy List with Random Pointer** | **HashMap** old→new; first pass create nodes, second wire `next` and `random`. **O(1) space:** interleave clone between each node, split. | **Random** can point null or to any node; **two-pass** map is clearer in interview. |
| **Palindrome Linked List** | Find mid (slow/fast); reverse second half; compare two halves. | **Odd** length: mid is extra—skip or handle. **O(1) space** vs stack O(n). |
| **Reorder List** | Mid + reverse second half; interleave first and second halves. | **In-place** pointer surgery; don’t lose tail. |
| **LRU Cache** (list + map) | Doubly linked list order (MRU front), `map key→node`; get moves to front; evict tail if over capacity. | **O(1)** needs DLL + map; **capacity 1** edge case. |

---

## See also

- [Heap](heap.md) — merge K sorted lists  
- [Hashing](hashing.md) — copy with random pointer  
- [Stack](stack.md) — recursion uses call stack
