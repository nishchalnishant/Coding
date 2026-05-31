---
tags: [coding, data-structures, linked-list]
topic: linked-list
difficulty: mixed
---

# Linked List — Problem Deep Dives

**Core invariants to internalize:**
- Singly linked: each node holds `val` + `next`. No backward traversal.
- Doubly linked: each node holds `val` + `next` + `prev`.
- The dummy/sentinel head eliminates edge cases on head deletion/insertion.
- Two-pointer (slow/fast) detects cycles and finds midpoints in O(n) / O(1) space.
- Floyd's algorithm: if fast meets slow inside cycle, resetting one pointer to head and stepping both at speed 1 lands them at the cycle entry.

---

## In-Place Reversal

### ==Reverse Linked List

> [!example] Problem
> Given the head of a singly linked list, reverse it in place and return the new head.

> [!info] Approach
> **Three-pointer iterative reversal.**
> WHY: We cannot reverse without visiting every node. The question is whether we need O(n) space (recursion stack) or O(1). Iteratively reversing edges is O(1) space.
> WHAT: Three-pointer technique maintaining invariant: `prev` is the fully-reversed prefix, `curr` is the unprocessed suffix head.
> HOW: Save `nxt = curr.next` before overwriting. Set `curr.next = prev`. Advance `prev = curr`, `curr = nxt`. When `curr` is None, `prev` is the new head.

> [!note]- Python Solution
> ```python
> from typing import Optional
> 
> class ListNode:
>     def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
>         self.val = val
>         self.next = next
> 
> def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
>     prev, curr = None, head
>     while curr:
>         nxt = curr.next       # save before overwriting
>         curr.next = prev      # reverse edge
>         prev, curr = curr, nxt
>     return prev  # prev is the new head
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Recursive: elegant but O(n) call stack. `reverse(head.next)` then `head.next.next = head; head.next = None; return new_head`. Stack overflow risk on large n.

---

### Reverse Linked List II

> [!example] Problem
> Reverse nodes from position `left` to `right` (1-indexed) in a single pass.

> [!info] Approach
> **Find pre-node + in-place splice-reversal.**
> WHY: We need to splice a reversed sublist back into the outer list. A dummy node handles the case where `left == 1` (head changes).
> WHAT: Find `pre` (node before position `left`). Then run `right - left` iterations of in-place splice-reversal.
> HOW: Each iteration: save `nxt = curr.next`, detach `nxt` from its position, reattach it after `pre`. This inserts nodes one by one at the front of the reversed section. After `right - left` iterations, the segment is reversed.

> [!note]- Python Solution
> ```python
> def reverse_between(head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
>     dummy = ListNode(0, head)
>     pre = dummy
>     for _ in range(left - 1):
>         pre = pre.next
>     curr = pre.next
>     for _ in range(right - left):
>         nxt = curr.next
>         curr.next = nxt.next
>         nxt.next = pre.next
>         pre.next = nxt
>     return dummy.next
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Collect sublist values, reverse them, overwrite: O(n) time, O(right-left) space. Simpler but uses extra space.
> - Full reversal then splice: two-pass; same complexity, more code.

---

### Palindrome Linked List

> [!example] Problem
> Check if a singly linked list is a palindrome in O(n) time, O(1) space.

> [!info] Approach
> **Find middle + reverse second half + compare.**
> WHY: Arrays allow index-based palindrome check in O(1) space. Linked lists don't. The trick: reverse the second half in-place and compare.
> WHAT: Three-step: find middle (slow/fast pointers), reverse second half, compare both halves node-by-node.
> HOW: Slow/fast to find middle. Reverse from `mid` onward. Walk two pointers — one from `head`, one from reversed head — checking values. Restore (optional): reverse second half back.

> [!note]- Python Solution
> ```python
> def is_palindrome(head: Optional[ListNode]) -> bool:
>     # Find middle
>     slow = fast = head
>     while fast and fast.next:
>         slow = slow.next
>         fast = fast.next.next
>     # Reverse second half
>     prev, curr = None, slow
>     while curr:
>         nxt = curr.next
>         curr.next = prev
>         prev, curr = curr, nxt
>     # Compare
>     l, r = head, prev
>     result = True
>     while r:
>         if l.val != r.val:
>             result = False
>             break
>         l, r = l.next, r.next
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Push first half onto a stack, compare with second half: O(n) time, O(n/2) space.
> - Recursion: O(n) call stack. Use a nonlocal `left` pointer advancing from head while recursion unwinds from tail.

---

### ==Reorder List

> [!example] Problem
> Reorder list in-place: `L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → ...`

> [!info] Approach
> **Find middle + reverse second half + interleave.**
> WHY: We need nodes from both ends simultaneously. The structure is: first half forward, second half backward, interleaved.
> WHAT: Three clean steps — find middle, reverse second half, interleave two halves.
> HOW: Slow/fast to find mid. Reverse second half. Merge two halves alternating: take one from first, one from second (reversed), repeat until second half is exhausted.

> [!note]- Python Solution
> ```python
> def reorder_list(head: Optional[ListNode]) -> None:
>     if not head or not head.next:
>         return
>     # Step 1: find middle
>     slow, fast = head, head
>     while fast.next and fast.next.next:
>         slow = slow.next
>         fast = fast.next.next
>     # Step 2: reverse second half
>     prev, curr = None, slow.next
>     slow.next = None  # cut the list
>     while curr:
>         nxt = curr.next
>         curr.next = prev
>         prev, curr = curr, nxt
>     # Step 3: interleave
>     first, second = head, prev
>     while second:
>         tmp1, tmp2 = first.next, second.next
>         first.next = second
>         second.next = tmp1
>         first, second = tmp1, tmp2
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Collect nodes into an array, two-pointer reassignment: O(n) time, O(n) space. Much simpler to write, unacceptable if O(1) space required.

---

### Reverse Nodes in K-Group

> [!example] Problem
> Reverse every K consecutive nodes. Leave remaining fewer-than-K nodes unreversed.

> [!info] Approach
> **Count-verify + in-place reversal per group.**
> WHY: We reverse groups of exactly K. Must verify K nodes exist before reversing each group — don't reverse a partial tail.
> WHAT: Count K nodes forward. If fewer than K remain, return head as-is. Reverse K nodes. Connect tail of reversed group to result of recursive call on the rest.
> HOW: Check-count loop + standard in-place reversal of exactly K nodes. After reversing, `head` (original) is the tail of the reversed group; link it to the recursive result.

> [!note]- Python Solution
> ```python
> def reverse_k_group(head: Optional[ListNode], k: int) -> Optional[ListNode]:
>     # Check if k nodes exist
>     node, count = head, 0
>     while node and count < k:
>         node = node.next
>         count += 1
>     if count < k:
>         return head  # fewer than k nodes — don't reverse
>     # Reverse exactly k nodes
>     prev, curr = None, head
>     for _ in range(k):
>         nxt = curr.next
>         curr.next = prev
>         prev, curr = curr, nxt
>     # head is now the tail of reversed group; link to next group
>     head.next = reverse_k_group(curr, k)
>     return prev  # prev is new head of this group
> ```

> [!success] Complexity
> Time O(n), Space O(n/k) recursion stack.

> [!tip] Alternatives
> - Iterative with `tail_of_prev_group.next` pointer: O(1) space, more complex bookkeeping.
> - `k=2` special case (Swap Nodes in Pairs): cleaner iterative code with dummy node.

---

## Fast / Slow Pointers

### Linked List Cycle

> [!example] Problem
> Detect if a linked list has a cycle.

> [!info] Approach
> **Floyd's fast/slow pointer cycle detection.**
> WHY: Without Floyd's, you'd need to store all visited nodes in a hash set — O(n) space. Floyd's uses two pointers that must meet inside a cycle.
> WHAT: Fast moves 2 steps, slow moves 1. If they ever point to the same node, a cycle exists. If fast reaches null, no cycle.
> HOW: Start both at `head`. Loop: `slow = slow.next`, `fast = fast.next.next`. Check `slow is fast` (identity, not equality). If `fast` or `fast.next` is None, exit — no cycle.

> [!note]- Python Solution
> ```python
> def has_cycle(head: Optional[ListNode]) -> bool:
>     slow = fast = head
>     while fast and fast.next:
>         slow = slow.next
>         fast = fast.next.next
>         if slow is fast:
>             return True
>     return False
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Hash set of visited nodes: O(n) time, O(n) space. Simpler logic but extra space.
> - Critical: use `is` not `==`. Two nodes with equal values would falsely trigger `==`.

---

### Middle of the Linked List

> [!example] Problem
> Return the middle node. For even-length lists, return the second middle node.

> [!info] Approach
> **Fast/slow one-pass middle finder.**
> WHY: Without knowing the length, we'd need two passes (one to count, one to find middle). Fast/slow achieves this in one pass.
> WHAT: Fast moves 2 steps, slow moves 1. When fast reaches the end, slow is at the middle.
> HOW: `while fast and fast.next: slow=slow.next, fast=fast.next.next`. When loop exits, `slow` is the middle. For odd-length: exact middle. For even-length: second of the two middles (because fast exhausts before the last step).

> [!note]- Python Solution
> ```python
> def middle_node(head: Optional[ListNode]) -> Optional[ListNode]:
>     slow = fast = head
>     while fast and fast.next:
>         slow = slow.next
>         fast = fast.next.next
>     return slow
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Count n then walk n//2 steps: two passes, O(n), O(1). Correct but uses two passes.
> - To get the left-middle for even-length, change condition to `while fast.next and fast.next.next`.

---

### Remove Nth Node From End of List

> [!example] Problem
> Remove the Nth node from the end of the list in one pass.

> [!info] Approach
> **Two pointers with N+1 gap.**
> WHY: We don't know the length. One pointer can be N steps ahead — when it hits null, the other is at the target.
> WHAT: Two pointers with a dummy head. `fast` advances N+1 steps ahead (one extra to land `slow` before the deletion target). Then both advance until `fast` is None.
> HOW: Dummy → head. Advance `fast` by `n+1` steps. Then `while fast: slow=slow.next, fast=fast.next`. Now `slow` is the predecessor of the node to delete. `slow.next = slow.next.next`.

> [!note]- Python Solution
> ```python
> def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
>     dummy = ListNode(0, head)
>     fast = slow = dummy
>     for _ in range(n + 1):
>         fast = fast.next
>     while fast:
>         slow = slow.next
>         fast = fast.next
>     slow.next = slow.next.next
>     return dummy.next
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Find length, then walk to `length - n`: two passes. O(n) each, simpler code.
> - Recursion with counter: elegant but O(n) stack space.

---

### Delete the Middle Node of a Linked List

> [!example] Problem
> Delete the middle node of the linked list (0-indexed: node at ⌊n/2⌋).

> [!info] Approach
> **Slow/fast with prev pointer — land before middle.**
> WHY: To delete a node in a singly linked list, you need the node before it. So we need slow/fast but with `slow` landing one step before the middle.
> WHAT: Modified slow/fast: keep a `prev` pointer one behind `slow`. When fast exits, `prev.next = slow.next`.
> HOW: `prev = dummy`, advance `fast` two steps, `slow` one step, `prev` follows `slow`. When `fast` is None (or `fast.next` is None), `slow` is the middle node to delete; `prev.next = slow.next`.

> [!note]- Python Solution
> ```python
> def delete_middle(head: Optional[ListNode]) -> Optional[ListNode]:
>     dummy = ListNode(0, head)
>     prev, slow, fast = dummy, head, head
>     while fast and fast.next:
>         prev = slow
>         slow = slow.next
>         fast = fast.next.next
>     prev.next = slow.next
>     return dummy.next
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Count n, walk to n//2 - 1: two passes. Same complexity, clearer intent.

---

### Happy Number

> [!example] Problem
> Determine if a number `n` is "happy": repeatedly replace it with the sum of the squares of its digits. If the process eventually reaches 1, it is happy. Otherwise it loops forever.

> [!info] Approach
> **Floyd's cycle detection on the implicit sequence.**
> - **WHY:** The sequence either terminates at 1 or enters a cycle. Instead of tracking all seen numbers in a hash set (O(n) space), we apply Floyd's on the sequence `f(n), f(f(n)), ...` where `f` computes the digit-square sum.
> - **WHAT:** Fast pointer applies `f` twice per step, slow applies once. If they meet at 1 → happy. If they meet at any other value → cycle, not happy.
> - **HOW:** Define `digit_square_sum`. Run slow/fast until `slow == fast`. If the meeting value is 1, return True. Else return False.

> [!note]- Python Solution
> ```python
> def is_happy(n: int) -> bool:
>     def digit_square_sum(x: int) -> int:
>         total = 0
>         while x:
>             x, d = divmod(x, 10)
>             total += d * d
>         return total
> 
>     slow, fast = n, digit_square_sum(n)
>     while fast != 1 and slow != fast:
>         slow = digit_square_sum(slow)
>         fast = digit_square_sum(digit_square_sum(fast))
>     return fast == 1
> ```

> [!success] Complexity
> Time O(log n) per step, converges in O(log n) steps, Space O(1).

> [!tip] Alternatives
> - Hash set of seen values: simpler, O(k) space where k is cycle length (bounded by ~3 digits → small constant in practice).
> - Known fact: unhappy numbers always cycle through 4. Check `if fast == 4: return False` as early exit.

---

## Floyd's Cycle Detection

### Linked List Cycle II

> [!example] Problem
> Find the node where the cycle begins. Return None if no cycle.

> [!info] Approach
> **Floyd's two-phase cycle entry detection.**
> WHY: Detection alone is O(1) space. Finding the entry requires a mathematical insight from Floyd's algorithm.
> WHAT: After slow/fast meet inside cycle, reset one pointer to head. Advance both at speed 1. Their meeting point is the cycle entry.
> HOW: Phase 1 — slow and fast meet after slow travels distance `d+c`, fast travels `d+c+L` (one full cycle extra), where `d` = head-to-entry, `c` = entry-to-meeting, `L` = cycle length. This implies `d = L - c = d'` (distance from meeting point back to entry). Phase 2 — slow resets to head, both advance 1 step at a time → they meet at the entry.

> [!note]- Python Solution
> ```python
> def detect_cycle(head: Optional[ListNode]) -> Optional[ListNode]:
>     slow = fast = head
>     while fast and fast.next:
>         slow = slow.next
>         fast = fast.next.next
>         if slow is fast:
>             break
>     else:
>         return None  # no cycle
>     slow = head
>     while slow is not fast:
>         slow = slow.next
>         fast = fast.next
>     return slow
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Hash set of visited nodes: O(n) space. Return first node seen twice.
> - The `for-else` pattern catches the no-cycle case cleanly; alternatively use a boolean flag.

---

### Find the Duplicate Number (Floyd's variant)

> [!example] Problem
> Array of n+1 integers, values in [1, n]. Find the duplicate without modifying the array, O(1) space.

> [!info] Approach
> **Floyd's on implicit linked list defined by array values.**
> WHY: Values in [1, n] define an implicit linked list: `next(i) = nums[i]`. Index 0 is the entry point (not part of cycle since all values ≥ 1). The duplicate value creates two pointers to the same node — the cycle entry.
> WHAT: Floyd's cycle detection on the implicit graph. Phase 1 finds the meeting point inside cycle; Phase 2 finds the cycle entry = duplicate.
> HOW: Identical to Linked List Cycle II but operating on array indices. `slow = nums[slow]`, `fast = nums[nums[fast]]`. After meeting, reset `slow = nums[0]` (not 0, because the linked list starts from `nums[0]`).

> [!note]- Python Solution
> ```python
> def find_duplicate(nums: list[int]) -> int:
>     slow = fast = nums[0]
>     # Phase 1: find intersection
>     while True:
>         slow = nums[slow]
>         fast = nums[nums[fast]]
>         if slow == fast:
>             break
>     # Phase 2: find cycle entry (duplicate)
>     slow = nums[0]
>     while slow != fast:
>         slow = nums[slow]
>         fast = nums[fast]
>     return slow
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Binary search on value range (pigeonhole): O(n log n) time, O(1) space. Count values ≤ mid; if count > mid, duplicate is in [1..mid].
> - XOR / sum math: only works if exactly one number appears exactly twice; fails for multiple duplicates.

---

## Merge / Sorting

### Merge Two Sorted Lists

> [!example] Problem
> Merge two sorted linked lists into one sorted list. Return the head of the merged list.

> [!info] Approach
> **Dummy head + two-pointer merge.**
> WHY: Two-pointer merge from merge sort. A dummy head eliminates the special case of "what is the initial head of the result?"
> WHAT: Compare heads of both lists, attach the smaller, advance that pointer. Append the remaining non-empty list.
> HOW: `dummy → result chain`. `curr` pointer builds the result. While both `l1` and `l2` non-null: attach smaller, advance it. After loop, attach the non-null remainder.

> [!note]- Python Solution
> ```python
> def merge_two_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
>     dummy = ListNode(0)
>     curr = dummy
>     while l1 and l2:
>         if l1.val <= l2.val:
>             curr.next = l1
>             l1 = l1.next
>         else:
>             curr.next = l2
>             l2 = l2.next
>         curr = curr.next
>     curr.next = l1 or l2
>     return dummy.next
> ```

> [!success] Complexity
> Time O(m+n), Space O(1).

> [!tip] Alternatives
> - Recursive: elegant, O(m+n) stack space. `return l1 if not l2 else l2 if not l1 else ...`
> - Creating new nodes: O(m+n) space — never do this; just relink existing nodes.

---

### Merge K Sorted Lists

> [!example] Problem
> Merge k sorted linked lists into one sorted list.

> [!info] Approach
> **Min-heap of size k.**
> WHY: Naively merging one by one is O(nk) — repeatedly touching each node. Min-heap always extracts the globally smallest remaining node in O(log k).
> WHAT: Min-heap of `(val, list_index, node)`. Extract minimum, push its successor. The `list_index` tie-breaks to avoid comparing `ListNode` objects.
> HOW: Initialize heap with heads of all non-null lists. While heap non-empty: pop min node, attach to result, push `node.next` if non-null.

> [!note]- Python Solution
> ```python
> import heapq
> 
> def merge_k_lists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
>     dummy = ListNode(0)
>     curr = dummy
>     heap: list[tuple[int, int, ListNode]] = []
>     for i, node in enumerate(lists):
>         if node:
>             heapq.heappush(heap, (node.val, i, node))
>     while heap:
>         val, i, node = heapq.heappop(heap)
>         curr.next = node
>         curr = curr.next
>         if node.next:
>             heapq.heappush(heap, (node.next.val, i, node.next))
>     return dummy.next
> ```

> [!success] Complexity
> Time O(N log k) where N = total nodes, Space O(k) heap.

> [!tip] Alternatives
> - Divide-and-conquer pairwise merge: O(N log k) time, O(log k) stack. Same asymptotic; avoids heap setup.
> - Sequential merge: O(Nk) — never use when k > 2.

---

### Sort List

> [!example] Problem
> Sort a linked list in O(n log n) time and O(1) space.

> [!info] Approach
> **Bottom-up merge sort on linked list.**
> WHY: Quicksort on linked lists has O(n²) worst case (no random access for pivot selection). Merge sort is naturally suited to linked lists — splitting is O(n) with slow/fast, merging is O(n).
> WHAT: Bottom-up merge sort to achieve O(1) space (avoids O(log n) recursion stack).
> HOW: For each sublist size `size = 1, 2, 4, 8, ...`: split list into pairs of `size`-length sublists, merge each pair, connect results. One full pass per doubling of `size`, log n passes total.

> [!note]- Python Solution
> ```python
> def sort_list(head: Optional[ListNode]) -> Optional[ListNode]:
>     if not head or not head.next:
>         return head
> 
>     # Get length
>     length, node = 0, head
>     while node:
>         length += 1
>         node = node.next
> 
>     dummy = ListNode(0, head)
>     size = 1
>     while size < length:
>         curr = dummy.next
>         tail = dummy
>         while curr:
>             left = curr
>             right = split(left, size)
>             curr = split(right, size)
>             merged_head, merged_tail = merge(left, right)
>             tail.next = merged_head
>             tail = merged_tail
>         size *= 2
>     return dummy.next
> 
> def split(head: Optional[ListNode], n: int) -> Optional[ListNode]:
>     """Cut first n nodes, return the rest."""
>     for _ in range(n - 1):
>         if not head:
>             break
>         head = head.next
>     if not head:
>         return None
>     rest = head.next
>     head.next = None
>     return rest
> 
> def merge(l1: Optional[ListNode], l2: Optional[ListNode]) -> tuple[Optional[ListNode], Optional[ListNode]]:
>     """Merge two sorted lists, return (head, tail)."""
>     dummy = ListNode(0)
>     curr = dummy
>     while l1 and l2:
>         if l1.val <= l2.val:
>             curr.next = l1; l1 = l1.next
>         else:
>             curr.next = l2; l2 = l2.next
>         curr = curr.next
>     curr.next = l1 or l2
>     while curr.next:
>         curr = curr.next
>     return dummy.next, curr
> ```

> [!success] Complexity
> Time O(n log n), Space O(1).

> [!tip] Alternatives
> - Top-down recursive merge sort: O(n log n) time, O(log n) stack. Simpler to write; acceptable unless O(1) space is required.

---

### Insertion Sort List

> [!example] Problem
> Sort a linked list using insertion sort. Return the sorted head.

> [!info] Approach
> **Dummy head + find-insertion-point per node.**
> - **WHY:** Insertion sort builds a sorted prefix. On a linked list we can't binary search, so finding the insertion point is O(n) per element, giving O(n²) total — acceptable when asked specifically for insertion sort.
> - **WHAT:** Maintain a sorted prefix after a dummy head. For each new node from the original list, find where it fits in the sorted prefix and splice it in.
> - **HOW:** Detach each node from the original list. Walk the sorted prefix from `dummy` until `prev.next.val > node.val` or `prev.next` is None. Insert `node` between `prev` and `prev.next`.

> [!note]- Python Solution
> ```python
> def insertion_sort_list(head: Optional[ListNode]) -> Optional[ListNode]:
>     dummy = ListNode(float('-inf'))
>     curr = head
>     while curr:
>         nxt = curr.next          # save next before relinking
>         prev = dummy
>         while prev.next and prev.next.val <= curr.val:
>             prev = prev.next
>         curr.next = prev.next    # insert curr between prev and prev.next
>         prev.next = curr
>         curr = nxt
>     return dummy.next
> ```

> [!success] Complexity
> Time O(n²), Space O(1).

> [!tip] Alternatives
> - Optimization: if `curr.val >= last sorted node.val`, skip the inner scan — useful for nearly-sorted input.
> - For O(n log n), use Sort List (LC 148) with merge sort instead.

---

## Copy / Design

### Copy List with Random Pointer

> [!example] Problem
> Deep copy a linked list where each node has `next` and `random` pointers. `random` may point to any node or null.

> [!info] Approach
> **Hash map original→clone, two-pass wiring.**
> WHY: Copying `next` is easy. `random` points to arbitrary nodes — we need to map original nodes to their clones to set `random` correctly.
> WHAT: Hash map `original → clone`. Two passes: first create all clones, second assign `next` and `random` using the map.
> HOW: Pass 1: iterate and create `{node: ListNode(node.val)}` for all nodes. Pass 2: for each original node, set `clone.next = map[node.next]`, `clone.random = map[node.random]`.

> [!note]- Python Solution
> ```python
> class Node:
>     def __init__(self, val: int, next: Optional['Node'] = None, random: Optional['Node'] = None):
>         self.val = val
>         self.next = next
>         self.random = random
> 
> def copy_random_list(head: Optional[Node]) -> Optional[Node]:
>     if not head:
>         return None
>     clone_map: dict[Optional[Node], Optional[Node]] = {None: None}
>     curr = head
>     while curr:
>         clone_map[curr] = Node(curr.val)
>         curr = curr.next
>     curr = head
>     while curr:
>         clone_map[curr].next = clone_map[curr.next]
>         clone_map[curr].random = clone_map[curr.random]
>         curr = curr.next
>     return clone_map[head]
> ```

> [!success] Complexity
> Time O(n), Space O(n) for the map.

> [!tip] Alternatives
> - O(1) space interleave trick: Insert each clone right after its original (`A → A' → B → B'`). Set `clone.random = orig.random.next`. Detach clones. Three passes, O(n) time, O(1) space.

---

### LRU Cache

> [!example] Problem
> Implement a Least Recently Used cache with O(1) `get` and `put` operations.

> [!info] Approach
> **Doubly linked list + hash map.**
> WHY: We need O(1) access (hash map) and O(1) eviction/promotion (doubly linked list). Neither alone suffices.
> WHAT: Doubly linked list for recency order (MRU at head, LRU at tail) + hash map for O(1) node lookup by key.
> HOW: Dummy head and dummy tail eliminate all edge cases in `_remove` and `_insert_front`. On `get`: remove from current position, insert at front, return value. On `put`: if key exists, remove old; create new node, insert at front, update map; if over capacity, remove LRU (tail.prev), delete from map.

> [!note]- Python Solution
> ```python
> class DLLNode:
>     def __init__(self, key: int = 0, val: int = 0):
>         self.key = key
>         self.val = val
>         self.prev: Optional['DLLNode'] = None
>         self.next: Optional['DLLNode'] = None
> 
> class LRUCache:
>     def __init__(self, capacity: int):
>         self.cap = capacity
>         self.cache: dict[int, DLLNode] = {}
>         self.head = DLLNode()  # dummy MRU sentinel
>         self.tail = DLLNode()  # dummy LRU sentinel
>         self.head.next = self.tail
>         self.tail.prev = self.head
> 
>     def _remove(self, node: DLLNode) -> None:
>         node.prev.next = node.next
>         node.next.prev = node.prev
> 
>     def _insert_front(self, node: DLLNode) -> None:
>         node.next = self.head.next
>         node.prev = self.head
>         self.head.next.prev = node
>         self.head.next = node
> 
>     def get(self, key: int) -> int:
>         if key not in self.cache:
>             return -1
>         node = self.cache[key]
>         self._remove(node)
>         self._insert_front(node)
>         return node.val
> 
>     def put(self, key: int, value: int) -> None:
>         if key in self.cache:
>             self._remove(self.cache[key])
>         node = DLLNode(key, value)
>         self.cache[key] = node
>         self._insert_front(node)
>         if len(self.cache) > self.cap:
>             lru = self.tail.prev
>             self._remove(lru)
>             del self.cache[lru.key]
> ```

> [!success] Complexity
> Time O(1) per get/put, Space O(capacity).

> [!tip] Alternatives
> - Python `OrderedDict`: `move_to_end` and `popitem(last=False)` give LRU in fewer lines. But you're expected to implement from scratch in interviews.
> - Array-based circular buffer: complex eviction logic. DLL is canonical.

---

## Other Manipulation

### Add Two Numbers

> [!example] Problem
> Two non-empty linked lists represent non-negative integers in reverse order (each node = one digit). Return the sum as a linked list in reverse order.

> [!info] Approach
> **Digit-by-digit addition with carry.**
> WHY: Reverse storage means digit-by-digit addition naturally flows head-to-tail. We just need to handle carry.
> WHAT: Simulate grade-school addition: sum digit-by-digit with carry. Create new result nodes.
> HOW: `carry = 0`. While `l1` or `l2` or `carry` non-zero: sum the current digits (0 if list exhausted) + carry. New digit = sum % 10, carry = sum // 10. Append digit node to result.

> [!note]- Python Solution
> ```python
> def add_two_numbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
>     dummy = ListNode(0)
>     curr = dummy
>     carry = 0
>     while l1 or l2 or carry:
>         val = carry
>         if l1:
>             val += l1.val
>             l1 = l1.next
>         if l2:
>             val += l2.val
>             l2 = l2.next
>         carry, digit = divmod(val, 10)
>         curr.next = ListNode(digit)
>         curr = curr.next
>     return dummy.next
> ```

> [!success] Complexity
> Time O(max(m,n)), Space O(max(m,n)) for result.

> [!tip] Alternatives
> - Extract numbers, add, convert back to list: works but requires O(n) extra computation to reconstruct; also overflows for very long lists.

---

### Swap Nodes in Pairs

> [!example] Problem
> Swap every two adjacent nodes in-place. Return the new head.

> [!info] Approach
> **Dummy head + iterative pair swapping.**
> WHY: Naive approach fails on the head node when `left=1`. Dummy node makes head swapping clean.
> WHAT: Iterative: use dummy head, advance `curr` as the node before each pair. Swap `curr.next` and `curr.next.next`. Advance by 2.
> HOW: Save `first = curr.next`, `second = curr.next.next`. Then: `curr.next = second`, `first.next = second.next`, `second.next = first`. Advance `curr = first` (first is now behind second after swap).

> [!note]- Python Solution
> ```python
> def swap_pairs(head: Optional[ListNode]) -> Optional[ListNode]:
>     dummy = ListNode(0, head)
>     curr = dummy
>     while curr.next and curr.next.next:
>         first = curr.next
>         second = curr.next.next
>         first.next = second.next
>         second.next = first
>         curr.next = second
>         curr = first  # first is now the second node in the pair
>     return dummy.next
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Recursive: `swap_pairs(head.next.next)` as the tail. O(n/2) stack frames. Elegant, acceptable.
> - This is Reverse K-Group with k=2.

---

### Intersection of Two Linked Lists

> [!example] Problem
> Find the node where two singly linked lists intersect. Return None if no intersection.

> [!info] Approach
> **Two pointers traversing both lists — alignment by total distance.**
> WHY: Lists may have different lengths before the intersection. We need pointers to align.
> WHAT: Two pointers, each traversing both lists (A then B, B then A). After at most m+n steps, they're aligned at the same position — either the intersection or both at None.
> HOW: `p1` traverses A then B; `p2` traverses B then A. When one reaches None, redirect to the other list's head. They travel m+n and n+m steps respectively — equal total. They meet at the intersection (or both reach None simultaneously = no intersection).

> [!note]- Python Solution
> ```python
> def get_intersection_node(headA: Optional[ListNode], headB: Optional[ListNode]) -> Optional[ListNode]:
>     p1, p2 = headA, headB
>     while p1 is not p2:
>         p1 = p1.next if p1 else headB
>         p2 = p2.next if p2 else headA
>     return p1  # intersection node, or None
> ```

> [!success] Complexity
> Time O(m+n), Space O(1).

> [!tip] Alternatives
> - Equalize lengths: compute both lengths, advance the longer list by the difference, then walk together. O(m+n) time, O(1) space. Same complexity, more code.
> - Hash set of A's nodes, scan B: O(m+n) time, O(m) space.

---

### Rotate List (Circular List Trick)

> [!example] Problem
> Rotate the linked list to the right by `k` places.

> [!info] Approach
> **Make circular, find new tail, break circle.**
> WHY: Rotating by k is equivalent to making it circular and breaking at position `n - k%n` from the head (i.e., the new head is `n - k%n` steps from the current head).
> WHAT: Find length, make circular, find new tail (n - k%n - 1 steps from head), break circle there.
> HOW: Walk to find length and tail. Connect tail to head (circular). Walk to position `n - k%n - 1` for new tail. `new_head = new_tail.next`. Break: `new_tail.next = None`.

> [!note]- Python Solution
> ```python
> def rotate_right(head: Optional[ListNode], k: int) -> Optional[ListNode]:
>     if not head or not head.next or k == 0:
>         return head
>     # Find length and tail
>     tail = head
>     n = 1
>     while tail.next:
>         tail = tail.next
>         n += 1
>     k %= n
>     if k == 0:
>         return head
>     # Make circular
>     tail.next = head
>     # Find new tail at position n - k - 1
>     steps = n - k - 1
>     new_tail = head
>     for _ in range(steps):
>         new_tail = new_tail.next
>     new_head = new_tail.next
>     new_tail.next = None
>     return new_head
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Collect nodes into an array, index with modulo: O(n) space. Simple but wasteful.

---

### Remove Duplicates from Sorted List

> [!example] Problem
> Given a sorted linked list, remove all duplicates so each value appears at most once. Return the sorted list.

> [!info] Approach
> **Single pass: skip consecutive equal nodes.**
> - **WHY:** The list is sorted, so duplicates are adjacent. One pass suffices — no need for a hash set.
> - **WHAT:** For each node, skip all successors with the same value by jumping `curr.next` forward.
> - **HOW:** Iterate `curr`. While `curr.next` exists and `curr.next.val == curr.val`, set `curr.next = curr.next.next`. After the inner loop, advance `curr = curr.next`.

> [!note]- Python Solution
> ```python
> def delete_duplicates_i(head: Optional[ListNode]) -> Optional[ListNode]:
>     curr = head
>     while curr and curr.next:
>         if curr.val == curr.next.val:
>             curr.next = curr.next.next  # skip duplicate
>         else:
>             curr = curr.next
>     return head
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - No dummy head needed here — we always keep the current node and only skip successors.
> - Contrast with LC 82 (Remove Duplicates II): there we skip ALL occurrences including the first; here we keep one copy.

---

### Remove Duplicates from Sorted List II

> [!example] Problem
> Remove all nodes that have any duplicate values (keep only nodes that appear exactly once).

> [!info] Approach
> **Dummy head + prev pointer skipping duplicate runs.**
> WHY: Unlike version I (keep one copy), we must skip all occurrences of a duplicated value. A dummy head handles the case where the head itself is a duplicate.
> WHAT: Pointer `prev` tracks the last confirmed-unique node. When duplicates are detected, skip all of them.
> HOW: Dummy head. `prev = dummy`. While `curr` non-null: if `curr.next` exists and `curr.val == curr.next.val`, record `dup_val`, advance `curr` past all nodes with that value, set `prev.next = curr.next`. Else `prev = curr`. `curr = curr.next`.

> [!note]- Python Solution
> ```python
> def delete_duplicates(head: Optional[ListNode]) -> Optional[ListNode]:
>     dummy = ListNode(0, head)
>     prev = dummy
>     curr = head
>     while curr:
>         if curr.next and curr.val == curr.next.val:
>             dup_val = curr.val
>             while curr and curr.val == dup_val:
>                 curr = curr.next
>             prev.next = curr
>         else:
>             prev = curr
>             curr = curr.next
>     return dummy.next
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Recursion: `if head.val == head.next.val: skip all then return delete_duplicates(curr)`. Elegant, O(n) stack.
> - Do not advance `prev` when a duplicate is found — `prev` stays to potentially connect to the next valid node.

---

### Partition List

> [!example] Problem
> Given a linked list and a value `x`, partition it so all nodes with values less than `x` come before nodes with values >= `x`. Preserve relative order within each partition.

> [!info] Approach
> **Two dummy heads — collect two sublists, then join.**
> - **WHY:** In-place partition on a linked list is tricky because pointers travel only forward. Simpler: collect "<x" nodes and ">=x" nodes into two separate chains, then concatenate.
> - **WHAT:** `less_dummy` heads the "<x" partition; `greater_dummy` heads the ">=x" partition. Walk the list, routing each node into the appropriate chain. Connect: `less_tail.next = greater_dummy.next`.
> - **HOW:** Null-terminate the greater chain (`greater_tail.next = None`) to avoid cycles if the original tail landed in the less chain.

> [!note]- Python Solution
> ```python
> def partition(head: Optional[ListNode], x: int) -> Optional[ListNode]:
>     less_dummy = ListNode(0)
>     greater_dummy = ListNode(0)
>     less = less_dummy
>     greater = greater_dummy
>     curr = head
>     while curr:
>         if curr.val < x:
>             less.next = curr
>             less = less.next
>         else:
>             greater.next = curr
>             greater = greater.next
>         curr = curr.next
>     greater.next = None          # must terminate — curr may have had .next set
>     less.next = greater_dummy.next
>     return less_dummy.next
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - In-place pointer manipulation: find a "<x" node after a ">=x" node and move it forward. Harder to write correctly; same complexity.
> - The `greater.next = None` line is critical — without it you can create a cycle if the last node ended up in the less chain.

---

### Flatten a Multilevel Doubly Linked List

> [!example] Problem
> Flatten a doubly linked list where some nodes have a `child` pointer to another doubly linked list. The child lists may themselves have children. Flatten into a single-level doubly linked list.

> [!info] Approach
> **Iterative in-place child list splicing.**
> WHY: Each child list must be inserted between the current node and its next node. This is a pointer surgery problem — splice the child list in-place.
> WHAT: When a `child` is encountered: find the tail of the child list, then wire: `curr.next = child`, `child.prev = curr`, `tail.next = next_node`, `next_node.prev = tail` (if next_node exists). Clear `curr.child`.
> HOW: Iterate `curr`. If `curr.child` exists: save `next_node = curr.next`, find child tail (walk to its end), perform 4-pointer surgery, clear `curr.child`. Continue — `curr.next` is now the start of the former child list, so we naturally continue into it.

> [!note]- Python Solution
> ```python
> class DLLNodeM:
>     def __init__(self, val: int = 0):
>         self.val = val
>         self.prev: Optional['DLLNodeM'] = None
>         self.next: Optional['DLLNodeM'] = None
>         self.child: Optional['DLLNodeM'] = None
> 
> def flatten(head: Optional[DLLNodeM]) -> Optional[DLLNodeM]:
>     curr = head
>     while curr:
>         if curr.child:
>             child = curr.child
>             next_node = curr.next
>             # Find tail of child list
>             tail = child
>             while tail.next:
>                 tail = tail.next
>             # Splice
>             curr.next = child
>             child.prev = curr
>             tail.next = next_node
>             if next_node:
>                 next_node.prev = tail
>             curr.child = None
>         curr = curr.next
>     return head
> ```

> [!success] Complexity
> Time O(n) where n = total nodes across all levels, Space O(1).

> [!tip] Alternatives
> - DFS with a stack: push `next_node` before recursing into `child`. O(depth) stack space. Conceptually cleaner but O(1) iterative is preferred.
> - Recursion: `flatten(child)` returns child_tail; splice. O(depth) call stack.

---

### ==LFU Cache

> [!example] Problem
> Implement a Least Frequently Used cache with O(1) `get` and `put`. On a tie in frequency, evict the least recently used among tied entries.

> [!info] Approach
> **Two hash maps + one frequency-keyed map of doubly linked lists.**
> - **WHY:** LRU is frequency=1-only. LFU needs per-frequency ordering. A `freq → OrderedDict` (or DLL) groups nodes by frequency; `min_freq` tracks the lowest frequency bucket for O(1) eviction.
> - **WHAT:** `key_map: {key → (val, freq)}`. `freq_map: {freq → OrderedDict[key]}` (OrderedDict preserves insertion order = LRU within each frequency). `min_freq` is the current minimum.
> - **HOW:** On `get`: increment freq, move key from old freq bucket to new freq bucket, update `min_freq` if old bucket is now empty and `min_freq` was that old freq. On `put`: if over capacity, evict from `freq_map[min_freq]` (popitem from the front = LRU). Then insert at freq=1, set `min_freq = 1`.

> [!note]- Python Solution
> ```python
> from collections import OrderedDict
> 
> class LFUCache:
>     def __init__(self, capacity: int):
>         self.cap = capacity
>         self.min_freq = 0
>         self.key_map: dict[int, list] = {}          # key -> [val, freq]
>         self.freq_map: dict[int, OrderedDict] = {}  # freq -> OrderedDict{key: None}
> 
>     def _update(self, key: int) -> None:
>         val, freq = self.key_map[key]
>         self.key_map[key] = [val, freq + 1]
>         self.freq_map[freq].pop(key)
>         if not self.freq_map[freq]:
>             del self.freq_map[freq]
>             if self.min_freq == freq:
>                 self.min_freq += 1
>         self.freq_map.setdefault(freq + 1, OrderedDict())[key] = None
> 
>     def get(self, key: int) -> int:
>         if key not in self.key_map:
>             return -1
>         self._update(key)
>         return self.key_map[key][0]
> 
>     def put(self, key: int, value: int) -> None:
>         if self.cap <= 0:
>             return
>         if key in self.key_map:
>             self.key_map[key][0] = value
>             self._update(key)
>             return
>         if len(self.key_map) >= self.cap:
>             evict_key, _ = self.freq_map[self.min_freq].popitem(last=False)
>             if not self.freq_map[self.min_freq]:
>                 del self.freq_map[self.min_freq]
>             del self.key_map[evict_key]
>         self.key_map[key] = [value, 1]
>         self.freq_map.setdefault(1, OrderedDict())[key] = None
>         self.min_freq = 1
> ```

> [!success] Complexity
> Time O(1) per get/put, Space O(capacity).

> [!tip] Alternatives
> - Two DLLs per frequency (like LRU but nested): avoids OrderedDict; pure pointer operations. More code, same complexity.
> - Segment tree / heap-based: O(log n) per op; overkill.
> - Key insight: `min_freq` only resets to 1 on `put` of a new key; on `get`/`update` it can only increase by 1.

---

## See Also

[[two-pointers]] | [[heap]] | [[tree]]
### Rotate List

> [!example] Problem
> Rotate a linked list to the right by `k` places.

> [!info] Approach
> - **WHY:** A rotation just changes where the tail reconnects to the head. Once you know the list length, you can convert the problem into a cut point.
> - **WHAT:** Make the list circular, compute `k % n`, and cut at the new tail.
> - **HOW:** Find tail and length, connect tail to head, advance to the new tail `n - k - 1` steps from the head, then break the cycle.

> [!note]- Python Solution
> ```python
> def rotate_right(head, k):
>     if not head or not head.next or k == 0:
>         return head
>     tail = head
>     n = 1
>     while tail.next:
>         tail = tail.next
>         n += 1
>     k %= n
>     if k == 0:
>         return head
>     tail.next = head
>     steps = n - k - 1
>     new_tail = head
>     for _ in range(steps):
>         new_tail = new_tail.next
>     new_head = new_tail.next
>     new_tail.next = None
>     return new_head
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> The same “make circular then break” trick is useful for other rotation-style linked list problems.

---

## Design

### ==LRU Cache (Doubly Linked List + Hash Map)

> [!example] Problem
> Design a data structure that supports `get(key)` and `put(key, value)` in O(1). When capacity is exceeded on `put`, evict the least recently used key (LC 146).

> [!info] Approach
> - **WHY:** A hash map gives O(1) lookup but can't track recency. A doubly linked list lets us move any node to the head (most recently used) in O(1) using pointers. Together they solve both requirements.
> - **WHAT:** Maintain a dict `key -> node`. The DLL has a sentinel head (most recent) and tail (least recent). On every access, unlink the node and re-insert it just after the head.
> - **HOW:** `get`: if key missing return -1, else move node to front and return value. `put`: if key exists update value and move to front; if new key and at capacity, remove the node just before the tail (LRU), then insert new node at front.

> [!note]- Python Solution
> ```python
> class Node:
>     def __init__(self, key: int = 0, val: int = 0):
>         self.key = key
>         self.val = val
>         self.prev = None
>         self.next = None
>
> class LRUCache:
>     def __init__(self, capacity: int):
>         self.cap = capacity
>         self.cache = {}
>         self.head = Node()   # most recent sentinel
>         self.tail = Node()   # least recent sentinel
>         self.head.next = self.tail
>         self.tail.prev = self.head
>
>     def _remove(self, node: Node) -> None:
>         node.prev.next = node.next
>         node.next.prev = node.prev
>
>     def _insert_front(self, node: Node) -> None:
>         node.next = self.head.next
>         node.prev = self.head
>         self.head.next.prev = node
>         self.head.next = node
>
>     def get(self, key: int) -> int:
>         if key not in self.cache:
>             return -1
>         node = self.cache[key]
>         self._remove(node)
>         self._insert_front(node)
>         return node.val
>
>     def put(self, key: int, value: int) -> None:
>         if key in self.cache:
>             self._remove(self.cache[key])
>         node = Node(key, value)
>         self.cache[key] = node
>         self._insert_front(node)
>         if len(self.cache) > self.cap:
>             lru = self.tail.prev
>             self._remove(lru)
>             del self.cache[lru.key]
> ```

> [!success] Complexity
> Time O(1) per get/put, Space O(capacity).

> [!tip] Alternatives
> - Python `OrderedDict`: `move_to_end` + `popitem(last=False)` gives the same O(1) behavior in 10 lines, but interviewers expect you to implement the DLL.
> - Array-based approaches: O(n) per operation — too slow.

---

### Flatten a Multilevel Doubly Linked List

> [!example] Problem
> A doubly linked list node may have a `child` pointer to another doubly linked list. Flatten the list so all child lists are inserted inline after their parent node (LC 430).

> [!info] Approach
> - **WHY:** The structure is like a tree where `child` is a subtree. DFS naturally processes each child list before continuing the main list.
> - **WHAT:** Use a stack. When a node has a child, push `node.next` onto the stack (to return to later), then walk into `child` as the new `next`. After the child chain ends (next is None), pop from the stack.
> - **HOW:** Walk the list. At each node with a `child`: push `node.next` to stack, set `node.next = node.child`, fix prev pointers, clear `node.child`. When `node.next` is None and stack is non-empty, pop and link.

> [!note]- Python Solution
> ```python
> class Node:
>     def __init__(self, val=0, prev=None, next=None, child=None):
>         self.val = val
>         self.prev = prev
>         self.next = next
>         self.child = child
>
> def flatten(head: Node | None) -> Node | None:
>     if not head:
>         return None
>     stack = []
>     curr = head
>     while curr:
>         if curr.child:
>             if curr.next:
>                 stack.append(curr.next)
>             curr.next = curr.child
>             curr.next.prev = curr
>             curr.child = None
>         if not curr.next and stack:
>             nxt = stack.pop()
>             curr.next = nxt
>             nxt.prev = curr
>         curr = curr.next
>     return head
> ```

> [!success] Complexity
> Time O(n) where n = total nodes, Space O(d) where d = maximum nesting depth.

> [!tip] Alternatives
> - Recursive DFS: recurse into child, get the tail of the flattened child list, then reconnect — elegant but O(d) call stack.
> - Both approaches are O(n) time; iterative stack is preferred when depth could be large.

---

## See Also

[[two-pointers]] | [[heap]] | [[tree]]
