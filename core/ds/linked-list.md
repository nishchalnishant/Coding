# Linked List — SDE-3 Gold Standard

A linear data structure where nodes are stored in non-contiguous memory, connected via next pointers. SDE-3 expects: clean in-place pointer manipulation, cycle detection with proof, DLL-based design problems, and trade-offs vs arrays.

---

## Theory & Mental Models

**What it is:** A sequence of nodes where each node holds a value and a pointer to the next node. No random access — you must traverse from the head. Core invariant: `head` points to the first node; the last node's `next` is `None`.

**Why it exists:** Solves the problem of frequent insertions and deletions at arbitrary positions without shifting memory. Real-world analogy: a treasure hunt — each clue (node) tells you where the next clue is; you cannot skip ahead without following the chain.

**Memory layout:** Nodes are scattered in heap memory, linked only via pointers. No cache locality — each pointer dereference is a potential cache miss. Doubly linked lists add a `prev` pointer for O(1) delete given a node reference.

**Key invariants:**
- `head` must always point to the first node (or `None` for empty list).
- Last node's `next` is `None` (for singly linked list).
- In a doubly linked list: `node.prev.next is node` and `node.next.prev is node` must hold everywhere.
- Cycle: if a `next` pointer points to an earlier node, traversal loops forever — detect with Floyd's algorithm.

**Complexity at a glance:**

| Operation | Singly LL | Doubly LL | Notes |
| :--- | :--- | :--- | :--- |
| Access by index | O(N) | O(N) | Must traverse from head |
| Insert at head | O(1) | O(1) | Update head pointer |
| Insert at tail | O(N) / O(1)* | O(1)* | *O(1) only with tail pointer |
| Insert at known pointer | O(1) | O(1) | Pointer manipulation only |
| Delete at known pointer | O(N) singly | O(1) doubly | Singly needs prev node |
| Search | O(N) | O(N) | Linear scan |

**When to reach for it:**
- Frequent insertions/deletions at arbitrary positions (given a pointer to the node).
- Implementing stacks, queues, LRU cache (DLL + hash map).
- Merging sorted sequences (merge sort on lists, K-way merge).
- No random access needed — only sequential traversal.
- Memory allocation pattern where contiguous blocks are unavailable.

**Common mistakes:**
- Losing the `head` reference by not using a dummy node when the head may be deleted.
- Forgetting to update the `tail` pointer on insert at the tail end.
- Null-pointer dereference on empty list — always guard `if not head` before accessing `head.next`.
- Off-by-one in reversal — saving `curr.next` after overwriting it instead of before.

---

## 1. Concept Overview

### When to Use Which Technique

| Technique | Purpose | Pattern |
| :--- | :--- | :--- |
| **Dummy node** | Head may be deleted/replaced (merge, delete head) | `dummy.next = head; return dummy.next` |
| **Fast & Slow pointers** | Find middle, detect cycle, find cycle entry | `slow += 1, fast += 2` |
| **In-place reversal** | O(1) space reversal; palindrome check; reorder | `prev, curr, nxt` three-pointer dance |
| **Two-pass or two-pointer offset** | Remove Nth from end without knowing length | Advance fast by N first |

---

## 2. Core Algorithms & Click Moments

### In-Place Reversal

> [!IMPORTANT]
> **The Click Moment**: "**Reverse** the list" — OR — "**palindrome** check (reverse second half)" — OR — "**reorder** list (weave first and second half)" — OR — "reverse in **K-groups**". All require the same three-pointer dance. Master this before anything else in linked lists.

```python
def reverse_list(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next      # save next before overwriting
        curr.next = prev     # reverse the pointer
        prev, curr = curr, nxt
    return prev  # prev is the new head

def reverse_between(head, left: int, right: int):
    dummy = ListNode(0)
    dummy.next = head
    pre = dummy
    for _ in range(left - 1):
        pre = pre.next
    curr = pre.next
    for _ in range(right - left):
        nxt = curr.next
        curr.next = nxt.next
        nxt.next = pre.next
        pre.next = nxt
    return dummy.next
```

> [!CAUTION]
> **The #1 linked list bug**: Forgetting to save `curr.next` before overwriting `curr.next = prev`. Once you do `curr.next = prev`, you've lost the reference to the rest of the list. Always `nxt = curr.next` as the **first line** inside the loop.

#### Common Variants & Twists
1. **Reverse Linked List II (Range Reversal)**:
   - **What (The Problem & Goal):** Reverse only a specific sub-portion of the linked list from position `left` to `right`.
   - **How (Intuition & Mental Model):** Requires a dummy node to elegantly handle cases where `left=1` (the head changes). Traverse to find the `pre` node just before `left`. Then, run the standard pointer reversal loop exactly `right - left` times, carefully relinking the reversed sublist back into the main chain.
2. **Palindrome Linked List**:
   - **What (The Problem & Goal):** Check if a linked list reads the same forwards and backwards in O(N) time and O(1) space.
   - **How (Intuition & Mental Model):** Find the middle using Fast & Slow pointers. Reverse the second half of the list. Compare the first half and the reversed second half node-by-node. Finally (optional but good practice), reverse the second half back to its original state.
3. **Reorder List**:
   - **What (The Problem & Goal):** Interleave the list nodes: `L0 -> Ln -> L1 -> Ln-1 -> L2 -> Ln-2 ...`
   - **How (Intuition & Mental Model):** Same 3-step blueprint: Find the middle, reverse the second half, then interleave/weave the two halves by alternating pointers.

---

### Find Middle — Fast & Slow Pointers

> [!IMPORTANT]
> **The Click Moment**: "Find the **middle** node" — OR — "split the list into two halves" — OR — "check if linked list is a **palindrome**" (find middle, reverse second half, compare). The fast pointer moves twice per step; when it reaches the end, slow is at the middle.

```python
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow  # for even-length list: returns second-middle node

def is_palindrome(head) -> bool:
    if not head or not head.next:
        return True
    mid = find_middle(head)
    second_half = reverse_list(mid)
    p1, p2 = head, second_half
    result = True
    while p2:  # compare original and reversed second half
        if p1.val != p2.val:
            result = False
            break
        p1, p2 = p1.next, p2.next
    reverse_list(second_half)  # restore original structure
    return result
```

> [!TIP]
> **Which middle for odd vs even lengths?** With `while fast and fast.next`, slow lands on the **left-middle** for even-length lists. If the problem requires the right-middle (e.g., for merge sort on linked lists), use `while fast.next and fast.next.next`. Clarify with the interviewer which is needed.

#### Common Variants & Twists
1. **Remove Nth Node From End**:
   - **What (The Problem & Goal):** Delete the $N^{th}$ node from the end of the list in a single pass without knowing the length.
   - **How (Intuition & Mental Model):** Give the `fast` pointer a head start of exactly `N` steps. Then advance both `fast` and `slow` one step at a time. When `fast.next` hits null, `slow` will be sitting exactly one node *before* the target deletion node.
2. **Delete the Middle Node**:
   - **What (The Problem & Goal):** Find and delete the middle node of the list.
   - **How (Intuition & Mental Model):** Standard fast and slow pointer setup to find the middle. However, to *delete* it, you need to link the node *before* the middle to the node *after* the middle. Keep a `prev` pointer right behind `slow` to execute `prev.next = slow.next`.

---

### Floyd's Cycle Detection

> [!IMPORTANT]
> **The Click Moment**: "**Detect a cycle**" — OR — "find the **cycle entry point**" — OR — "**intersection** of two linked lists" (same idea: two pointers meet at intersection). Floyd's algorithm proves that slow and fast must meet inside the cycle, and the meeting point is exactly L steps from the cycle entry (where L = distance from head to entry).

```python
def has_cycle(head) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

def detect_cycle_entry(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None  # no cycle
    # Reset slow to head; move both one step at a time
    slow = head
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow  # cycle entry node
```

> [!CAUTION]
> **Identity check, not equality**: Use `slow is fast` (identity), **not** `slow == fast` (value equality). Two different nodes with the same value would falsely trigger `==`. This is a common Python bug that passes some test cases but fails on identical-value nodes.

#### Common Variants & Twists
1. **Linked List Cycle II**:
   - **What (The Problem & Goal):** Not just detect a cycle, but return the exact node where the cycle begins.
   - **How (Intuition & Mental Model):** Handled by the second phase of Floyd's algorithm. Once `slow` and `fast` intersect inside the cycle, reset `slow` to the `head` of the list. Advance both pointers one step at a time. The exact node where they meet again is the cycle entry point.
2. **Find the Duplicate Number**:
   - **What (The Problem & Goal):** Find the duplicate integer in an array of values `[1, N]` without modifying the array and using O(1) extra space.
   - **How (Intuition & Mental Model):** The array values act as `next` pointers (`next_node = nums[current_node]`). Because all values are in `[1, N]`, index 0 is guaranteed not to be part of the cycle. Run Floyd's Cycle Detection starting from index 0; the cycle entry point is the duplicate value.

---

### Reverse K-Group

> [!IMPORTANT]
> **The Click Moment**: "Reverse the list in **groups of K**" — OR — "K-group reversal". The key insight: check that K nodes exist before reversing; then reverse exactly K nodes, connect the tail of the reversed group to the result of the recursive (or iterative) call for the rest.

```python
def reverse_k_group(head, k: int):
    # Check if k nodes remain
    count, node = 0, head
    while node and count < k:
        node = node.next
        count += 1
    if count < k:
        return head  # fewer than k nodes remain — don't reverse

    prev, curr = None, head
    for _ in range(k):
        nxt = curr.next
        curr.next = prev
        prev, curr = curr, nxt

    head.next = reverse_k_group(curr, k)  # head is now the tail of reversed group
    return prev  # prev is the new head of this group
```

#### Common Variants & Twists
1. **Swap Nodes in Pairs**:
   - **What (The Problem & Goal):** Swap every two adjacent nodes in the linked list.
   - **How (Intuition & Mental Model):** A specific simplification of Reverse K-Group where `K=2`. While recursion works, an iterative approach with a dummy node is straightforward: repeatedly swap `curr.next` and `curr.next.next`, then advance your `curr` pointer by 2.

---

### LRU Cache — Doubly Linked List + Hash Map

> [!IMPORTANT]
> **The Click Moment**: "**LRU Cache**" — OR — "O(1) get and put with eviction of **least recently used**". The DLL maintains recency order (most recent at head, LRU at tail). The hash map provides O(1) access to any node for repositioning.

```python
class DLLNode:
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache: dict[int, DLLNode] = {}
        self.head = DLLNode()  # dummy head (MRU side)
        self.tail = DLLNode()  # dummy tail (LRU side)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: DLLNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_front(self, node: DLLNode) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._insert_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = DLLNode(key, value)
        self.cache[key] = node
        self._insert_front(node)
        if len(self.cache) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```

---

## 3. SDE-3 Deep Dives

### Scalability: Skip Lists

> [!TIP]
> A **skip list** is a probabilistic linked-list-based data structure supporting O(log N) search, insert, and delete — matching balanced BSTs without complex rotations. It uses multiple levels of "express lanes" (linked lists of increasing step size), each node randomly promoted to higher levels.
>
> Used in: Redis sorted sets (`ZSET`), LevelDB/RocksDB memtables, Java's `ConcurrentSkipListMap`. At Google scale, skip lists handle sorted-set operations in Bigtable's in-memory index.

### Concurrency: Lock-Free Linked Lists

> [!TIP]
> **Michael-Scott Lock-Free Queue** uses CAS on the `tail.next` pointer for enqueue. The key trick: if `tail.next != null`, another thread is mid-enqueue — help it by advancing `tail` before your own insert. This makes all threads cooperative, preventing starvation.
>
> For lock-free singly linked list **delete**: use **logical deletion** — mark the `next` pointer with a "deleted" bit (tagged pointer). Physical removal happens lazily during traversal. Avoids the ABA problem without versioned pointers.

> [!CAUTION]
> Python's CPython GIL makes individual `append`/`popleft` on `collections.deque` thread-safe, but multi-step operations (check-then-act) are not atomic. Use `threading.Lock` for LRU Cache or other multi-step DLL operations in concurrent Python code.

### Trade-offs: Linked List vs Array

| Operation | Singly LL | Doubly LL | Dynamic Array |
| :--- | :--- | :--- | :--- |
| Random access | O(N) | O(N) | O(1) |
| Insert at head | O(1) | O(1) | O(N) amortized |
| Insert at tail | O(N) or O(1) with tail ptr | O(1) | O(1) amortized |
| Delete (given node ptr) | O(N) for prev | O(1) | O(N) shift |
| Cache performance | Poor (pointer chasing) | Poor | Excellent (contiguous) |
| Memory overhead | 1 pointer/node | 2 pointers/node | None (contiguous) |

---

## 4. Common Interview Problems

### Easy
- [Reverse Linked List](../algo/problem-deep-dives.md#reverse-linked-list) — Three-pointer iterative; recursive is shorter but O(N) stack.
- **Linked List Cycle** — Fast & slow; `O is O` identity check.
- **Merge Two Sorted Lists** — Dummy head; two-pointer merge.

### Medium
- [Remove Nth From End](../algo/problem-deep-dives.md#remove-nth-from-end) — Fast advances N steps first; both advance together until fast.next is null.
- [Copy List with Random Pointer](../algo/problem-deep-dives.md#copy-list-with-random-pointer) — Map `old → clone`; two passes. Or: interleave clones O(1) extra space.
- **Palindrome Linked List** — Find middle, reverse second half, compare, restore.
- **Add Two Numbers** — Digit-by-digit sum with carry; handle length mismatch.
- **Reorder List** — Find middle, reverse second half, weave (merge alternating).
- **Swap Nodes in Pairs** — Reverse every two nodes; dummy node simplifies head case.

### Hard
- [Merge K Sorted Lists](../algo/problem-deep-dives.md#merge-k-sorted-lists) — Min-heap of K nodes; or divide-and-conquer pairwise merge.
- [LRU Cache](../algo/problem-deep-dives.md#lru-cache) — DLL + hash map; dummy head/tail to avoid edge cases.
- **Reverse K-Group** — Recursion or iterative; check K nodes exist before reversing.
- **Sort List** — Merge sort; find middle, split, sort each half, merge. O(N log N) time, O(log N) stack.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **[Reverse List](../algo/problem-deep-dives.md#reverse-linked-list)** | Iterative Pointer Reversal | "Flip all pointers" | `nxt = curr.next; curr.next = prev; prev, curr = curr, nxt` | Save `nxt` first — overwriting `curr.next` loses the rest of the list. |
| **[Remove Nth From End](../algo/problem-deep-dives.md#remove-nth-from-end)** | "Nth from end without length" | Fast advances N steps; then both advance; fast.next=null → slow is before target | Use dummy head: handles removing the actual head node (N = length). |
| **[Merge K Lists](../algo/problem-deep-dives.md#merge-k-sorted-lists)** | "Smallest of K heads at all times" | Min-heap `(val, list_idx, node)` | Tie-break: include unique `list_idx` to prevent comparing `ListNode` objects. |
| **[LRU Cache](../algo/problem-deep-dives.md#lru-cache)** | "O(1) get and put with LRU eviction" | DLL for recency + hash map for O(1) node access | Dummy head/tail eliminate all edge cases in `_remove` and `_insert_front`. |
| **Detect Cycle Entry** | "Where does the cycle begin?" | Two-pointer meet inside cycle; reset slow to head; advance both by 1 | The math: meeting point is exactly `L` steps from entry — derive it once, remember it. |
| **Palindrome LL** | "Is the list a palindrome?" | Find middle, reverse second half, compare | Restore the second half after comparison — mutation side effect trap. |
| **Reverse K-Group** | "Reverse every K nodes" | Count K nodes; reverse; connect tail to result of recursive call | Fewer than K nodes at end — don't reverse; just return `head`. |
| **Copy List with Random Pointer** | "Deep copy with random pointers" | Map `old → clone`; two passes | Without the map: interleave clones between originals — O(1) extra space trick. |
| **Sort List** | "Sort linked list efficiently" | Merge sort: find middle, split, sort each, merge | Unlike arrays, finding middle is O(N); overall still O(N log N) with O(log N) stack. |
| **Add Two Numbers** | "LL represents number, add two" | Digit-by-digit sum with carry tracking | Handle different lengths; handle final carry (create extra node if carry=1 at end). |
| **Middle of Linked List** [E] | "Find middle node" | Fast/slow pointers; fast moves 2, slow moves 1 | For even-length lists, `slow` lands on the second middle — clarify which middle is wanted. |
| **Linked List Cycle** [E] | "Detect if cycle exists" | Fast/slow pointers — they meet iff cycle exists | No need to find entry point for detection only; O(1) space. |
| **Merge Two Sorted Lists** [E] | "Merge without extra space" | Dummy head; compare `l1.val` vs `l2.val`; attach smaller | Always use a dummy node — avoids special-casing the empty-head edge case. |
| **Intersection of Two Linked Lists** [M] | "Find node where two lists merge" | Two pointers; redirect each to other list's head on exhaustion; meet at intersection | They traverse `A+B` and `B+A` total — equal regardless of individual lengths. `null == null` handles no-intersection case. |
| **Reorder List** [M] | "L0→Ln→L1→Ln-1→..." | Find middle; reverse second half; merge alternating | Three steps must be clean: find mid (slow/fast), reverse (iterative), merge. Mess up pointer order and you get infinite loops. |
| **Swap Nodes in Pairs** [M] | "Swap every two adjacent nodes" | Dummy head; swap `curr.next` and `curr.next.next`; advance by 2 | Save `next_pair = curr.next.next.next` before relinking or you lose the rest of the list. |
| **Rotate Linked List** [M] | "Rotate right by K places" | Find length; make circular; break at `length - k % length` | `k % length` handles k > length; break from the tail, not the head. |
| **Remove Duplicates from Sorted List II** [M] | "Remove all nodes with any duplicate value" | Dummy head; detect duplicate run; skip entire run | Unlike version I (keep one), skip ALL nodes with that value — continue until `curr.next.val != val`. |
| **Flatten Multilevel Doubly Linked List** [M] | "Flatten nested child pointers" | On `child`: insert child list between curr and curr.next; update prev/next | Update `prev` pointer on re-attach — doubly linked lists require both directions. |
| **Merge K Sorted Lists** [H] | "Merge K lists efficiently" | Min-heap of `(val, list_index, node)`; pop and push next | Tie-breaking: include list index to avoid comparing ListNode objects directly. |

---

## Quick Revision Triggers

- If the problem needs O(1) insert/delete at a known position without shifting → think Linked List because pointer relinking is O(1).
- If the problem says "detect cycle" or "find cycle entry" → think Floyd's fast & slow pointers; use `is` not `==` for identity.
- If the problem says "find middle" or "check palindrome" → think Fast & Slow pointers; slow lands at left-middle for even-length lists.
- If the problem says "LRU Cache" or "O(1) eviction" → think Doubly Linked List + Hash Map; dummy head/tail eliminate edge cases.
- If the problem says "merge K sorted lists" → think Min-Heap of K nodes with tie-breaking by list index.
- If the problem says "reverse in K-groups" → think count K nodes first, reverse exactly K, recurse on remainder.
- If the problem says "remove Nth from end without knowing length" → think Two-pointer with N-step head start.

## See also

- [Heap](heap.md) — Merge K sorted lists via min-heap
- [Hashing](hashing.md) — Copy list with random pointer; LRU cache hash map component
- [Stack](stack.md) — Recursion uses call stack; iterative reversal eliminates it
- [Patterns Master](../../reference/patterns/patterns-master.md) — fast & slow pointer pattern triggers
