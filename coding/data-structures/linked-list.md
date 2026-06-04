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

**Interview patterns to recognize quickly:**
- Dummy node + pointer relinks for head-safe insertion/deletion.
- Slow/fast pointers for cycle detection, middle finding, and end-relative deletes.
- Reverse-then-merge for palindrome, reorder, and k-group style problems.
- Hash map + list node pairs for random pointers and LRU caches.
- Heap for merging multiple sorted lists.

**Edge cases to sanity-check:**
- Empty list, one node, and two nodes.
- Head changes after deletion/reversal.
- Odd vs even length when finding the middle.
- `k = 1`, `k > length`, or `left == right`.
- Cycles absent vs present; duplicate values vs duplicate nodes.


> [!abstract] Google Interview Legend
> `🔥 Google` — **Core** problem: extremely high frequency at Google SDE 2/3 interviews. Cover these first.
> `⭐ Google` — **Important** problem: medium frequency at Google SDE 2/3 level. Cover after core.
> Problems without a marker are good practice but less Google-specific at SDE 2/3 level.

---

## In-Place Reversal

### ==Reverse Linked List `🔥 Google`

> [!example] Problem
> Given the head of a singly linked list, reverse the list, and return the reversed list.
> 
> **Example 1:**
> ```
> Input: head = [1,2,3,4,5]
> Output: [5,4,3,2,1]
> ```
> 
> **Example 2:**
> ```
> Input: head = [1,2]
> Output: [2,1]
> ```
> 
> **Example 3:**
> ```
> Input: head = []
> Output: []
> ```
> 
> **Constraints:**
> - The number of nodes in the list is the range [0, 5000].
> - -5000 <= Node.val <= 5000

> [!info] Approach
> **Three-pointer iterative reversal.** We cannot reverse without visiting every node. The question is whether we need O(n) space (recursion stack) or O(1). Iteratively reversing edges is O(1) space. Three-pointer technique maintaining invariant: `prev` is the fully-reversed prefix, `curr` is the unprocessed suffix head. Save `nxt = curr.next` before overwriting. Set `curr.next = prev`. Advance `prev = curr`, `curr = nxt`. When `curr` is None, `prev` is the new head. Watch the order carefully: save `next` before rewiring or you lose the rest of the list.

> [!note]- Python Solution
> ```python
> from typing import Optional
> 
> class ListNode:
>     def __init__(self, val=0, next=None):
>         self.val = val
>         self.next = next
> 
> def reverse_list(head):
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

### Reverse Linked List II `🔥 Google`

> [!example] Problem
> Given the head of a singly linked list and two integers left and right where left <= right, reverse the nodes of the list from position left to position right, and return the reversed list.
> 
> **Example 1:**
> ```
> Input: head = [1,2,3,4,5], left = 2, right = 4
> Output: [1,4,3,2,5]
> ```
> 
> **Example 2:**
> ```
> Input: head = [5], left = 1, right = 1
> Output: [5]
> ```
> 
> **Constraints:**
> - The number of nodes in the list is n.
> - 1 <= n <= 500
> - -500 <= Node.val <= 500
> - 1 <= left <= right <= n

> [!info] Approach
> **Find pre-node + in-place splice-reversal.** We need to splice a reversed sublist back into the outer list. A dummy node handles the case where `left == 1` (head changes). Find `pre` (node before position `left`). Then run `right - left` iterations of in-place splice-reversal. Each iteration: save `nxt = curr.next`, detach `nxt` from its position, reattach it after `pre`. This inserts nodes one by one at the front of the reversed section. After `right - left` iterations, the segment is reversed. If `left == right`, the loop runs zero times and the list stays unchanged.

> [!note]- Python Solution
> ```python
> def reverse_between(head, left, right):
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

### Palindrome Linked List `⭐ Google`

> [!example] Problem
> Given the head of a singly linked list, return true if it is a palindrome or false otherwise.
> 
> **Example 1:**
> ```
> Input: head = [1,2,2,1]
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: head = [1,2]
> Output: false
> ```
> 
> **Constraints:**
> - The number of nodes in the list is in the range [1, 10^5].
> - 0 <= Node.val <= 9

> [!info] Approach
> **Find middle + reverse second half + compare.** Arrays allow index-based palindrome check in O(1) space. Linked lists don't. The trick: reverse the second half in-place and compare. Three-step: find middle (slow/fast pointers), skip the exact middle on odd-length lists, reverse second half, compare both halves node-by-node. Slow/fast to find middle. If the list has odd length, advance `slow` one more step to skip the middle node. Reverse from that point onward. Walk two pointers — one from `head`, one from reversed head — checking values. Restore (optional): reverse second half back.

> [!note]- Python Solution
> ```python
> def is_palindrome(head):
>     # Find middle
>     slow = fast = head
>     while fast and fast.next:
>         slow = slow.next
>         fast = fast.next.next
>     if fast:  # odd length: skip the center node
>         slow = slow.next
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
> - If you need to preserve the original list, reverse the second half back after comparison.

---

### ==Reorder List `🔥 Google`

> [!example] Problem
> You are given the head of a singly linked-list. The list can be represented as:
> Reorder the list to be on the following form:
> You may not modify the values in the list's nodes. Only nodes themselves may be changed.
> 
> **Example 1:**
> ```
> L0 → L1 → … → Ln - 1 → Ln
> ```
> 
> **Example 2:**
> ```
> L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …
> ```
> 
> **Example 3:**
> ```
> Input: head = [1,2,3,4]
> Output: [1,4,2,3]
> ```
> 
> **Example 4:**
> ```
> Input: head = [1,2,3,4,5]
> Output: [1,5,2,4,3]
> ```
> 
> **Constraints:**
> - The number of nodes in the list is in the range [1, 5 * 10^4].
> - 1 <= Node.val <= 1000

> [!info] Approach
> **Find middle + reverse second half + interleave.** We need nodes from both ends simultaneously. The structure is: first half forward, second half backward, interleaved. Three clean steps — find middle, reverse second half, interleave two halves. Slow/fast to find mid. Reverse second half. Merge two halves alternating: take one from first, one from second (reversed), repeat until second half is exhausted.

> [!note]- Python Solution
> ```python
> def reorder_list(head):
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

### Reverse Nodes in K-Group `⭐ Google`

> [!example] Problem
> Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.
> k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k then left-out nodes, in the end, should remain as it is.
> You may not alter the values in the list's nodes, only nodes themselves may be changed.
> 
> **Example 1:**
> ```
> Input: head = [1,2,3,4,5], k = 2
> Output: [2,1,4,3,5]
> ```
> 
> **Example 2:**
> ```
> Input: head = [1,2,3,4,5], k = 3
> Output: [3,2,1,4,5]
> ```
> 
> **Constraints:**
> - The number of nodes in the list is n.
> - 1 <= k <= n <= 5000
> - 0 <= Node.val <= 1000

> [!info] Approach
> **Count-verify + in-place reversal per group.** We reverse groups of exactly K. Must verify K nodes exist before reversing each group — don't reverse a partial tail. Count K nodes forward. If fewer than K remain, return head as-is. Reverse K nodes. Connect tail of reversed group to result of recursive call on the rest. Check-count loop + standard in-place reversal of exactly K nodes. After reversing, `head` (original) is the tail of the reversed group; link it to the recursive result.

> [!note]- Python Solution
> ```python
> def reverse_k_group(head, k):
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

### Linked List Cycle `🔥 Google`

> [!example] Problem
> Given head, the head of a linked list, determine if the linked list has a cycle in it.
> There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail's next pointer is connected to. Note that pos is not passed as a parameter.
> Return true if there is a cycle in the linked list. Otherwise, return false.
> 
> **Example 1:**
> ```
> Input: head = [3,2,0,-4], pos = 1
> Output: true
> Explanation: There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed).
> ```
> 
> **Example 2:**
> ```
> Input: head = [1,2], pos = 0
> Output: true
> Explanation: There is a cycle in the linked list, where the tail connects to the 0th node.
> ```
> 
> **Example 3:**
> ```
> Input: head = [1], pos = -1
> Output: false
> Explanation: There is no cycle in the linked list.
> ```
> 
> **Constraints:**
> - The number of the nodes in the list is in the range [0, 10^4].
> - -10^5 <= Node.val <= 10^5
> - pos is -1 or a valid index in the linked-list.

> [!info] Approach
> **Floyd's fast/slow pointer cycle detection.** Without Floyd's, you'd need to store all visited nodes in a hash set — O(n) space. Floyd's uses two pointers that must meet inside a cycle. Fast moves 2 steps, slow moves 1. If they ever point to the same node, a cycle exists. If fast reaches null, no cycle. Start both at `head`. Loop: `slow = slow.next`, `fast = fast.next.next`. Check `slow is fast` (identity, not equality). If `fast` or `fast.next` is None, exit — no cycle. The identity check matters whenever node values can repeat.

> [!note]- Python Solution
> ```python
> def has_cycle(head):
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
> Given the head of a singly linked list, return the middle node of the linked list.
> If there are two middle nodes, return the second middle node.
> 
> **Example 1:**
> ```
> Input: head = [1,2,3,4,5]
> Output: [3,4,5]
> Explanation: The middle node of the list is node 3.
> ```
> 
> **Example 2:**
> ```
> Input: head = [1,2,3,4,5,6]
> Output: [4,5,6]
> Explanation: Since the list has two middle nodes with values 3 and 4, we return the second one.
> ```
> 
> **Constraints:**
> - The number of nodes in the list is in the range [1, 100].
> - 1 <= Node.val <= 100

> [!info] Approach
> **Fast/slow one-pass middle finder.** Without knowing the length, we'd need two passes (one to count, one to find middle). Fast/slow achieves this in one pass. Fast moves 2 steps, slow moves 1. When fast reaches the end, slow is at the middle. `while fast and fast.next: slow=slow.next, fast=fast.next.next`. When loop exits, `slow` is the middle. For odd-length: exact middle. For even-length: second of the two middles (because fast exhausts before the last step).

> [!note]- Python Solution
> ```python
> def middle_node(head):
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

### Remove Nth Node From End of List `🔥 Google`

> [!example] Problem
> Given the head of a linked list, remove the nth node from the end of the list and return its head.
> 
> **Example 1:**
> ```
> Input: head = [1,2,3,4,5], n = 2
> Output: [1,2,3,5]
> ```
> 
> **Example 2:**
> ```
> Input: head = [1], n = 1
> Output: []
> ```
> 
> **Example 3:**
> ```
> Input: head = [1,2], n = 1
> Output: [1]
> ```
> 
> **Constraints:**
> - The number of nodes in the list is sz.
> - 1 <= sz <= 30
> - 0 <= Node.val <= 100
> - 1 <= n <= sz

> [!info] Approach
> **Two pointers with N+1 gap.** We don't know the length. One pointer can be N steps ahead — when it hits null, the other is at the target. Two pointers with a dummy head. `fast` advances N+1 steps ahead (one extra to land `slow` before the deletion target). Then both advance until `fast` is None. Dummy → head. Advance `fast` by `n+1` steps. Then `while fast: slow=slow.next, fast=fast.next`. Now `slow` is the predecessor of the node to delete. `slow.next = slow.next.next`.

> [!note]- Python Solution
> ```python
> def remove_nth_from_end(head, n):
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
> You are given the head of a linked list. Delete the middle node, and return the head of the modified linked list.
> The middle node of a linked list of size n is the ⌊n / 2⌋th node from the start using 0-based indexing, where ⌊x⌋ denotes the largest integer less than or equal to x.
> 
> **Example 1:**
> ```
> Input: head = [1,3,4,7,1,2,6]
> Output: [1,3,4,1,2,6]
> Explanation:
> The above figure represents the given linked list. The indices of the nodes are written below.
> Since n = 7, node 3 with value 7 is the middle node, which is marked in red.
> We return the new list after removing this node.
> ```
> 
> **Example 2:**
> ```
> Input: head = [1,2,3,4]
> Output: [1,2,4]
> Explanation:
> The above figure represents the given linked list.
> For n = 4, node 2 with value 3 is the middle node, which is marked in red.
> ```
> 
> **Example 3:**
> ```
> Input: head = [2,1]
> Output: [2]
> Explanation:
> The above figure represents the given linked list.
> For n = 2, node 1 with value 1 is the middle node, which is marked in red.
> Node 0 with value 2 is the only node remaining after removing node 1.
> ```
> 
> **Constraints:**
> - The number of nodes in the list is in the range [1, 10^5].
> - 1 <= Node.val <= 10^5

> [!info] Approach
> **Slow/fast with prev pointer — land before middle.** To delete a node in a singly linked list, you need the node before it. So we need slow/fast but with `slow` landing one step before the middle. Modified slow/fast: keep a `prev` pointer one behind `slow`. When fast exits, `prev.next = slow.next`. `prev = dummy`, advance `fast` two steps, `slow` one step, `prev` follows `slow`. When `fast` is None (or `fast.next` is None), `slow` is the middle node to delete; `prev.next = slow.next`.

> [!note]- Python Solution
> ```python
> def delete_middle(head):
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

### Happy Number `🔥 Google`

> [!example] Problem
> Write an algorithm to determine if a number n is happy.
> A happy number is a number defined by the following process:
> Return true if n is a happy number, and false if not.
> 
> **Example 1:**
> ```
> Input: n = 19
> Output: true
> Explanation:
> 12 + 92 = 82
> 82 + 22 = 68
> 62 + 82 = 100
> 12 + 02 + 02 = 1
> ```
> 
> **Example 2:**
> ```
> Input: n = 2
> Output: false
> ```
> 
> **Constraints:**
> - 1 <= n <= 2^{31} - 1

> [!info] Approach
> **Floyd's cycle detection on the implicit sequence.** The sequence either terminates at 1 or enters a cycle. Instead of tracking all seen numbers in a hash set (O(n) space), we apply Floyd's on the sequence `f(n), f(f(n)), ...` where `f` computes the digit-square sum. Fast pointer applies `f` twice per step, slow applies once. If they meet at 1 → happy. If they meet at any other value → cycle, not happy. Define `digit_square_sum`. Run slow/fast until `slow == fast`. If the meeting value is 1, return True. Else return False.

> [!note]- Python Solution
> ```python
> def is_happy(n):
>     def digit_square_sum(x):
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
> Time O(d) where d is the number of digits processed per iteration; in practice this is tiny and the sequence quickly enters a small cycle, Space O(1).

> [!tip] Alternatives
> - Hash set of seen values: simpler, O(k) space where k is cycle length (bounded by ~3 digits → small constant in practice).
> - Known fact: unhappy numbers always cycle through 4. Check `if fast == 4: return False` as early exit.

---

## Floyd's Cycle Detection

### Linked List Cycle II `🔥 Google`

> [!example] Problem
> Given the head of a linked list, return the node where the cycle begins. If there is no cycle, return null.
> There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail's next pointer is connected to (0-indexed). It is -1 if there is no cycle. Note that pos is not passed as a parameter.
> Do not modify the linked list.
> 
> **Example 1:**
> ```
> Input: head = [3,2,0,-4], pos = 1
> Output: tail connects to node index 1
> Explanation: There is a cycle in the linked list, where tail connects to the second node.
> ```
> 
> **Example 2:**
> ```
> Input: head = [1,2], pos = 0
> Output: tail connects to node index 0
> Explanation: There is a cycle in the linked list, where tail connects to the first node.
> ```
> 
> **Example 3:**
> ```
> Input: head = [1], pos = -1
> Output: no cycle
> Explanation: There is no cycle in the linked list.
> ```
> 
> **Constraints:**
> - The number of the nodes in the list is in the range [0, 10^4].
> - -10^5 <= Node.val <= 10^5
> - pos is -1 or a valid index in the linked-list.

> [!info] Approach
> **Floyd's two-phase cycle entry detection.** Detection alone is O(1) space. Finding the entry requires a mathematical insight from Floyd's algorithm. After slow/fast meet inside cycle, reset one pointer to head. Advance both at speed 1. Their meeting point is the cycle entry. Phase 1 — slow and fast meet after slow travels distance `d+c`, fast travels `d+c+L` (one full cycle extra), where `d` = head-to-entry, `c` = entry-to-meeting, `L` = cycle length. This implies `d = L - c = d'` (distance from meeting point back to entry). Phase 2 — slow resets to head, both advance 1 step at a time → they meet at the entry.

> [!note]- Python Solution
> ```python
> def detect_cycle(head):
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

### Find the Duplicate Number (Floyd's variant) `⭐ Google`

> [!example] Problem
> Given an array of integers nums containing n + 1 integers where each integer is in the range [1, n] inclusive.
> There is only one repeated number in nums, return this repeated number.
> You must solve the problem without modifying the array nums and using only constant extra space.
> 
> **Example 1:**
> ```
> Input: nums = [1,3,4,2,2]
> Output: 2
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,1,3,4,2]
> Output: 3
> ```
> 
> **Example 3:**
> ```
> Input: nums = [3,3,3,3,3]
> Output: 3
> ```
> 
> **Constraints:**
> - 1 <= n <= 10^5
> - nums.length == n + 1
> - 1 <= nums[i] <= n
> - All the integers in nums appear only once except for precisely one integer which appears two or more times.

> [!info] Approach
> **Floyd's on implicit linked list defined by array values.** Values in [1, n] define an implicit linked list: `next(i) = nums[i]`. Index 0 is the entry point (not part of cycle since all values ≥ 1). The duplicate value creates two pointers to the same node — the cycle entry. Floyd's cycle detection on the implicit graph. Phase 1 finds the meeting point inside cycle; Phase 2 finds the cycle entry = duplicate. Identical to Linked List Cycle II but operating on array indices. `slow = nums[slow]`, `fast = nums[nums[fast]]`. After meeting, reset `slow = nums[0]` (not 0, because the linked list starts from `nums[0]`).

> [!note]- Python Solution
> ```python
> def find_duplicate(nums):
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

### Merge Two Sorted Lists `🔥 Google`

> [!example] Problem
> You are given the heads of two sorted linked lists list1 and list2.
> Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.
> Return the head of the merged linked list.
> 
> **Example 1:**
> ```
> Input: list1 = [1,2,4], list2 = [1,3,4]
> Output: [1,1,2,3,4,4]
> ```
> 
> **Example 2:**
> ```
> Input: list1 = [], list2 = []
> Output: []
> ```
> 
> **Example 3:**
> ```
> Input: list1 = [], list2 = [0]
> Output: [0]
> ```
> 
> **Constraints:**
> - The number of nodes in both lists is in the range [0, 50].
> - -100 <= Node.val <= 100
> - Both list1 and list2 are sorted in non-decreasing order.

> [!info] Approach
> **Dummy head + two-pointer merge.** Two-pointer merge from merge sort. A dummy head eliminates the special case of "what is the initial head of the result?" Compare heads of both lists, attach the smaller, advance that pointer. Append the remaining non-empty list. `dummy → result chain`. `curr` pointer builds the result. While both `l1` and `l2` non-null: attach smaller, advance it. After loop, attach the non-null remainder.

> [!note]- Python Solution
> ```python
> def merge_two_lists(l1, l2):
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

### Sort List `⭐ Google`

> [!example] Problem
> Given the head of a linked list, return the list after sorting it in ascending order.
> 
> **Example 1:**
> ```
> Input: head = [4,2,1,3]
> Output: [1,2,3,4]
> ```
> 
> **Example 2:**
> ```
> Input: head = [-1,5,3,4,0]
> Output: [-1,0,3,4,5]
> ```
> 
> **Example 3:**
> ```
> Input: head = []
> Output: []
> ```
> 
> **Constraints:**
> - The number of nodes in the list is in the range [0, 5 * 10^4].
> - -10^5 <= Node.val <= 10^5

> [!info] Approach
> **Bottom-up merge sort on linked list.** Quicksort on linked lists has O(n²) worst case (no random access for pivot selection). Merge sort is naturally suited to linked lists — splitting is O(n) with slow/fast, merging is O(n). Bottom-up merge sort to achieve O(1) space (avoids O(log n) recursion stack). For each sublist size `size = 1, 2, 4, 8, ...`: split list into pairs of `size`-length sublists, merge each pair, connect results. One full pass per doubling of `size`, log n passes total. This is the version interviewers like when they explicitly ask for O(1) extra space.

> [!note]- Python Solution
> ```python
> def sort_list(head):
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
> def split(head, n):
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
> def merge(l1, l2):
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
> Given the head of a singly linked list, sort the list using insertion sort, and return the sorted list's head.
> The steps of the insertion sort algorithm:
> The following is a graphical example of the insertion sort algorithm. The partially sorted list (black) initially contains only the first element in the list. One element (red) is removed from the input data and inserted in-place into the sorted list with each iteration.
> 
> **Example 1:**
> ```
> Input: head = [4,2,1,3]
> Output: [1,2,3,4]
> ```
> 
> **Example 2:**
> ```
> Input: head = [-1,5,3,4,0]
> Output: [-1,0,3,4,5]
> ```
> 
> **Constraints:**
> - The number of nodes in the list is in the range [1, 5000].
> - -5000 <= Node.val <= 5000

> [!info] Approach
> **Dummy head + find-insertion-point per node.** Insertion sort builds a sorted prefix. On a linked list we can't binary search, so finding the insertion point is O(n) per element, giving O(n²) total — acceptable when asked specifically for insertion sort. Maintain a sorted prefix after a dummy head. For each new node from the original list, find where it fits in the sorted prefix and splice it in. Detach each node from the original list. Walk the sorted prefix from `dummy` until `prev.next.val > node.val` or `prev.next` is None. Insert `node` between `prev` and `prev.next`. If the input is nearly sorted, this often behaves closer to linear time.

> [!note]- Python Solution
> ```python
> def insertion_sort_list(head):
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

### Copy List with Random Pointer `🔥 Google`

> [!example] Problem
> A linked list of length n is given such that each node contains an additional random pointer, which could point to any node in the list, or null.
> Construct a deep copy of the list. The deep copy should consist of exactly n brand new nodes, where each new node has its value set to the value of its corresponding original node. Both the next and random pointer of the new nodes should point to new nodes in the copied list such that the pointers in the original list and copied list represent the same list state. None of the pointers in the new list should point to nodes in the original list.
> For example, if there are two nodes X and Y in the original list, where X.random --> Y, then for the corresponding two nodes x and y in the copied list, x.random --> y.
> Return the head of the copied linked list.
> The linked list is represented in the input/output as a list of n nodes. Each node is represented as a pair of [val, random_index] where:
> Your code will only be given the head of the original linked list.
> 
> **Example 1:**
> ```
> Input: head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
> Output: [[7,null],[13,0],[11,4],[10,2],[1,0]]
> ```
> 
> **Example 2:**
> ```
> Input: head = [[1,1],[2,1]]
> Output: [[1,1],[2,1]]
> ```
> 
> **Example 3:**
> ```
> Input: head = [[3,null],[3,0],[3,null]]
> Output: [[3,null],[3,0],[3,null]]
> ```
> 
> **Constraints:**
> - 0 <= n <= 1000
> - -10^4 <= Node.val <= 10^4
> - Node.random is null or is pointing to some node in the linked list.

> [!info] Approach
> **Hash map original→clone, two-pass wiring.** Copying `next` is easy. `random` points to arbitrary nodes — we need to map original nodes to their clones to set `random` correctly. Hash map `original → clone`. Two passes: first create all clones, second assign `next` and `random` using the map. Pass 1: iterate and create `{node: ListNode(node.val)}` for all nodes. Pass 2: for each original node, set `clone.next = map[node.next]`, `clone.random = map[node.random]`. Mapping `None → None` keeps the wiring concise.

> [!note]- Python Solution
> ```python
> class Node:
>     def __init__(self, val, next=None, random=None):
>         self.val = val
>         self.next = next
>         self.random = random
> 
> def copy_random_list(head):
>     if not head:
>         return None
>     clone_map = {None: None}
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

### LRU Cache `🔥 Google`

> [!example] Problem
> Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.
> Implement the LRUCache class:
> The functions get and put must each run in O(1) average time complexity.
> 
> **Example 1:**
> ```
> Input
> ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
> [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
> Output
> [null, null, null, 1, null, -1, null, -1, 3, 4]
> 
> Explanation
> LRUCache lRUCache = new LRUCache(2);
> lRUCache.put(1, 1); // cache is {1=1}
> lRUCache.put(2, 2); // cache is {1=1, 2=2}
> lRUCache.get(1);    // return 1
> lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
> lRUCache.get(2);    // returns -1 (not found)
> lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
> lRUCache.get(1);    // return -1 (not found)
> lRUCache.get(3);    // return 3
> lRUCache.get(4);    // return 4
> ```
> 
> **Constraints:**
> - 1 <= capacity <= 3000
> - 0 <= key <= 10^4
> - 0 <= value <= 10^5
> - At most 2 * 10^5 calls will be made to get and put.

> [!info] Approach
> **Doubly linked list + hash map.** We need O(1) access (hash map) and O(1) eviction/promotion (doubly linked list). Neither alone suffices. Doubly linked list for recency order (MRU at head, LRU at tail) + hash map for O(1) node lookup by key. Dummy head and dummy tail eliminate all edge cases in `_remove` and `_insert_front`. On `get`: remove from current position, insert at front, return value. On `put`: if key exists, remove old; create new node, insert at front, update map; if over capacity, remove LRU (tail.prev), delete from map.

> [!note]- Python Solution
> ```python
> class DLLNode:
>     def __init__(self, key=0, val=0):
>         self.key = key
>         self.val = val
>         self.prev: Optional['DLLNode'] = None
>         self.next: Optional['DLLNode'] = None
> 
> class LRUCache:
>     def __init__(self, capacity):
>         self.cap = capacity
>         self.cache: dict[int, DLLNode] = {}
>         self.head = DLLNode()  # dummy MRU sentinel
>         self.tail = DLLNode()  # dummy LRU sentinel
>         self.head.next = self.tail
>         self.tail.prev = self.head
> 
>     def _remove(self, node):
>         node.prev.next = node.next
>         node.next.prev = node.prev
> 
>     def _insert_front(self, node):
>         node.next = self.head.next
>         node.prev = self.head
>         self.head.next.prev = node
>         self.head.next = node
> 
>     def get(self, key):
>         if key not in self.cache:
>             return -1
>         node = self.cache[key]
>         self._remove(node)
>         self._insert_front(node)
>         return node.val
> 
>     def put(self, key, value):
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
> Time O(1) average for `get` and `put`, Space O(capacity).

> [!tip] Alternatives
> - `collections.OrderedDict`: great in Python interviews if allowed, but explain the underlying DLL + hash map idea first.
> - The key invariant is consistency: every cache key must have exactly one live node in the list and one entry in the map.

---

## Other Manipulation

### Add Two Numbers

> [!example] Problem
> You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.
> You may assume the two numbers do not contain any leading zero, except the number 0 itself.
> 
> **Example 1:**
> ```
> Input: l1 = [2,4,3], l2 = [5,6,4]
> Output: [7,0,8]
> Explanation: 342 + 465 = 807.
> ```
> 
> **Example 2:**
> ```
> Input: l1 = [0], l2 = [0]
> Output: [0]
> ```
> 
> **Example 3:**
> ```
> Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
> Output: [8,9,9,9,0,0,0,1]
> ```
> 
> **Constraints:**
> - The number of nodes in each linked list is in the range [1, 100].
> - 0 <= Node.val <= 9
> - It is guaranteed that the list represents a number that does not have leading zeros.

> [!info] Approach
> **Digit-by-digit addition with carry.** Reverse storage means digit-by-digit addition naturally flows head-to-tail. We just need to handle carry. Simulate grade-school addition: sum digit-by-digit with carry. Create new result nodes. `carry = 0`. While `l1` or `l2` or `carry` non-zero: sum the current digits (0 if list exhausted) + carry. New digit = sum % 10, carry = sum // 10. Append digit node to result.

> [!note]- Python Solution
> ```python
> def add_two_numbers(l1, l2):
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

### Swap Nodes in Pairs `⭐ Google`

> [!example] Problem
> Given a linked list, swap every two adjacent nodes and return its head. You must solve the problem without modifying the values in the list's nodes (i.e., only nodes themselves may be changed.)
> 
> **Example 1:**
> ```
> Input: head = [1,2,3,4]
> Output: [2,1,4,3]
> Explanation:
> ```
> 
> **Example 2:**
> ```
> Input: head = []
> Output: []
> ```
> 
> **Example 3:**
> ```
> Input: head = [1]
> Output: [1]
> ```
> 
> **Example 4:**
> ```
> Input: head = [1,2,3]
> Output: [2,1,3]
> ```
> 
> **Constraints:**
> - The number of nodes in the list is in the range [0, 100].
> - 0 <= Node.val <= 100

> [!info] Approach
> **Dummy head + iterative pair swapping.** Naive approach fails on the head node when `left=1`. Dummy node makes head swapping clean. Iterative: use dummy head, advance `curr` as the node before each pair. Swap `curr.next` and `curr.next.next`. Advance by 2. Save `first = curr.next`, `second = curr.next.next`. Then: `curr.next = second`, `first.next = second.next`, `second.next = first`. Advance `curr = first` (first is now behind second after swap).

> [!note]- Python Solution
> ```python
> def swap_pairs(head):
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
> Given the heads of two singly linked-lists headA and headB, return the node at which the two lists intersect. If the two linked lists have no intersection at all, return null.
> For example, the following two linked lists begin to intersect at node c1:
> The test cases are generated such that there are no cycles anywhere in the entire linked structure.
> Note that the linked lists must retain their original structure after the function returns.
> Custom Judge:
> The inputs to the judge are given as follows (your program is not given these inputs):
> The judge will then create the linked structure based on these inputs and pass the two heads, headA and headB to your program. If you correctly return the intersected node, then your solution will be accepted.
> 
> **Example 1:**
> ```
> Input: intersectVal = 8, listA = [4,1,8,4,5], listB = [5,6,1,8,4,5], skipA = 2, skipB = 3
> Output: Intersected at '8'
> Explanation: The intersected node's value is 8 (note that this must not be 0 if the two lists intersect).
> From the head of A, it reads as [4,1,8,4,5]. From the head of B, it reads as [5,6,1,8,4,5]. There are 2 nodes before the intersected node in A; There are 3 nodes before the intersected node in B.
> - Note that the intersected node's value is not 1 because the nodes with value 1 in A and B (2nd node in A and 3rd node in B) are different node references. In other words, they point to two different locations in memory, while the nodes with value 8 in A and B (3rd node in A and 4th node in B) point to the same location in memory.
> ```
> 
> **Example 2:**
> ```
> Input: intersectVal = 2, listA = [1,9,1,2,4], listB = [3,2,4], skipA = 3, skipB = 1
> Output: Intersected at '2'
> Explanation: The intersected node's value is 2 (note that this must not be 0 if the two lists intersect).
> From the head of A, it reads as [1,9,1,2,4]. From the head of B, it reads as [3,2,4]. There are 3 nodes before the intersected node in A; There are 1 node before the intersected node in B.
> ```
> 
> **Example 3:**
> ```
> Input: intersectVal = 0, listA = [2,6,4], listB = [1,5], skipA = 3, skipB = 2
> Output: No intersection
> Explanation: From the head of A, it reads as [2,6,4]. From the head of B, it reads as [1,5]. Since the two lists do not intersect, intersectVal must be 0, while skipA and skipB can be arbitrary values.
> Explanation: The two lists do not intersect, so return null.
> ```
> 
> **Constraints:**
> - The number of nodes of listA is in the m.
> - The number of nodes of listB is in the n.
> - 1 <= m, n <= 3 * 10^4
> - 1 <= Node.val <= 10^5
> - 0 <= skipA <= m
> - 0 <= skipB <= n
> - intersectVal is 0 if listA and listB do not intersect.
> - intersectVal == listA[skipA] == listB[skipB] if listA and listB intersect.

> [!info] Approach
> **Two pointers traversing both lists — alignment by total distance.** Lists may have different lengths before the intersection. We need pointers to align. Two pointers, each traversing both lists (A then B, B then A). After at most m+n steps, they're aligned at the same position — either the intersection or both at None. `p1` traverses A then B; `p2` traverses B then A. When one reaches None, redirect to the other list's head. They travel m+n and n+m steps respectively — equal total. They meet at the intersection (or both reach None simultaneously = no intersection).

> [!note]- Python Solution
> ```python
> def get_intersection_node(headA, headB):
>     one_back, two_back = headA, headB
>     while one_back is not two_back:
>         one_back = one_back.next if one_back else headB
>         two_back = two_back.next if two_back else headA
>     return one_back  # intersection node, or None
> ```

> [!success] Complexity
> Time O(m+n), Space O(1).

> [!tip] Alternatives
> - Equalize lengths: compute both lengths, advance the longer list by the difference, then walk together. O(m+n) time, O(1) space. Same complexity, more code.
> - Hash set of A's nodes, scan B: O(m+n) time, O(m) space.

---

### Rotate List (Circular List Trick)

> [!example] Problem
> Given the head of a linked list, rotate the list to the right by k places.
> 
> **Example 1:**
> ```
> Input: head = [1,2,3,4,5], k = 2
> Output: [4,5,1,2,3]
> ```
> 
> **Example 2:**
> ```
> Input: head = [0,1,2], k = 4
> Output: [2,0,1]
> ```
> 
> **Constraints:**
> - The number of nodes in the list is in the range [0, 500].
> - -100 <= Node.val <= 100
> - 0 <= k <= 2 * 10^9

> [!info] Approach
> **Make circular, find new tail, break circle.** Rotating by k is equivalent to making it circular and breaking at position `n - k%n` from the head (i.e., the new head is `n - k%n` steps from the current head). Find length, make circular, find new tail (n - k%n - 1 steps from head), break circle there. Walk to find length and tail. Connect tail to head (circular). Walk to position `n - k%n - 1` for new tail. `new_head = new_tail.next`. Break: `new_tail.next = None`.

> [!note]- Python Solution
> ```python
> def rotate_right(head, k):
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
> Given the head of a sorted linked list, delete all duplicates such that each element appears only once. Return the linked list sorted as well.
> 
> **Example 1:**
> ```
> Input: head = [1,1,2]
> Output: [1,2]
> ```
> 
> **Example 2:**
> ```
> Input: head = [1,1,2,3,3]
> Output: [1,2,3]
> ```
> 
> **Constraints:**
> - The number of nodes in the list is in the range [0, 300].
> - -100 <= Node.val <= 100
> - The list is guaranteed to be sorted in ascending order.

> [!info] Approach
> **Single pass: skip consecutive equal nodes.** The list is sorted, so duplicates are adjacent. One pass suffices — no need for a hash set. For each node, skip all successors with the same value by jumping `curr.next` forward. Iterate `curr`. While `curr.next` exists and `curr.next.val == curr.val`, set `curr.next = curr.next.next`. After the inner loop, advance `curr = curr.next`.

> [!note]- Python Solution
> ```python
> def delete_duplicates_i(head):
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
> Given the head of a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the original list. Return the linked list sorted as well.
> 
> **Example 1:**
> ```
> Input: head = [1,2,3,3,4,4,5]
> Output: [1,2,5]
> ```
> 
> **Example 2:**
> ```
> Input: head = [1,1,1,2,3]
> Output: [2,3]
> ```
> 
> **Constraints:**
> - The number of nodes in the list is in the range [0, 300].
> - -100 <= Node.val <= 100
> - The list is guaranteed to be sorted in ascending order.

> [!info] Approach
> **Dummy head + prev pointer skipping duplicate runs.** Unlike version I (keep one copy), we must skip all occurrences of a duplicated value. A dummy head handles the case where the head itself is a duplicate. Pointer `prev` tracks the last confirmed-unique node. When duplicates are detected, skip all of them. Dummy head. `prev = dummy`. While `curr` non-null: if `curr.next` exists and `curr.val == curr.next.val`, record `dup_val`, advance `curr` past all nodes with that value, set `prev.next = curr.next`. Else `prev = curr`. `curr = curr.next`.

> [!note]- Python Solution
> ```python
> def delete_duplicates(head):
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
> Given the head of a linked list and a value x, partition it such that all nodes less than x come before nodes greater than or equal to x.
> You should preserve the original relative order of the nodes in each of the two partitions.
> 
> **Example 1:**
> ```
> Input: head = [1,4,3,2,5,2], x = 3
> Output: [1,2,2,4,3,5]
> ```
> 
> **Example 2:**
> ```
> Input: head = [2,1], x = 2
> Output: [1,2]
> ```
> 
> **Constraints:**
> - The number of nodes in the list is in the range [0, 200].
> - -100 <= Node.val <= 100
> - -200 <= x <= 200

> [!info] Approach
> **Two dummy heads — collect two sublists, then join.** In-place partition on a linked list is tricky because pointers travel only forward. Simpler: collect "<x" nodes and ">=x" nodes into two separate chains, then concatenate. `less_dummy` heads the "<x" partition; `greater_dummy` heads the ">=x" partition. Walk the list, routing each node into the appropriate chain. Connect: `less_tail.next = greater_dummy.next`. Null-terminate the greater chain (`greater_tail.next = None`) to avoid cycles if the original tail landed in the less chain.

> [!note]- Python Solution
> ```python
> def partition(head, x):
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

### Flatten a Multilevel Doubly Linked List `⭐ Google`

> [!example] Problem
> You are given a doubly linked list, which contains nodes that have a next pointer, a previous pointer, and an additional child pointer. This child pointer may or may not point to a separate doubly linked list, also containing these special nodes. These child lists may have one or more children of their own, and so on, to produce a multilevel data structure as shown in the example below.
> Given the head of the first level of the list, flatten the list so that all the nodes appear in a single-level, doubly linked list. Let curr be a node with a child list. The nodes in the child list should appear after curr and before curr.next in the flattened list.
> Return the head of the flattened list. The nodes in the list must have all of their child pointers set to null.
> 
> **Example 1:**
> ```
> Input: head = [1,2,3,4,5,6,null,null,null,7,8,9,10,null,null,11,12]
> Output: [1,2,3,7,8,11,12,9,10,4,5,6]
> Explanation: The multilevel linked list in the input is shown.
> After flattening the multilevel linked list it becomes:
> ```
> 
> **Example 2:**
> ```
> Input: head = [1,2,null,3]
> Output: [1,3,2]
> Explanation: The multilevel linked list in the input is shown.
> After flattening the multilevel linked list it becomes:
> ```
> 
> **Example 3:**
> ```
> Input: head = []
> Output: []
> Explanation: There could be empty list in the input.
> ```
> 
> **Example 4:**
> ```
> 1---2---3---4---5---6--NULL
>          |
>          7---8---9---10--NULL
>              |
>              11--12--NULL
> ```
> 
> **Example 5:**
> ```
> [1,2,3,4,5,6,null]
> [7,8,9,10,null]
> [11,12,null]
> ```
> 
> **Example 6:**
> ```
> [1,    2,    3, 4, 5, 6, null]
>              |
> [null, null, 7,    8, 9, 10, null]
>                    |
> [            null, 11, 12, null]
> ```
> 
> **Example 7:**
> ```
> [1,2,3,4,5,6,null,null,null,7,8,9,10,null,null,11,12]
> ```
> 
> **Constraints:**
> - The number of Nodes will not exceed 1000.
> - 1 <= Node.val <= 10^5

> [!info] Approach
> **Iterative in-place child list splicing.** Each child list must be inserted between the current node and its next node. This is a pointer surgery problem — splice the child list in-place. When a `child` is encountered: find the tail of the child list, then wire: `curr.next = child`, `child.prev = curr`, `tail.next = next_node`, `next_node.prev = tail` (if next_node exists). Clear `curr.child`. Iterate `curr`. If `curr.child` exists: save `next_node = curr.next`, find child tail (walk to its end), perform 4-pointer surgery, clear `curr.child`. Continue — `curr.next` is now the start of the former child list, so we naturally continue into it.

> [!note]- Python Solution
> ```python
> class DLLNodeM:
>     def __init__(self, val=0):
>         self.val = val
>         self.prev: Optional['DLLNodeM'] = None
>         self.next: Optional['DLLNodeM'] = None
>         self.child: Optional['DLLNodeM'] = None
> 
> def flatten(head):
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

### Rotate List

> [!example] Problem
> Given the head of a linked list, rotate the list to the right by k places.
> 
> **Example 1:**
> ```
> Input: head = [1,2,3,4,5], k = 2
> Output: [4,5,1,2,3]
> ```
> 
> **Example 2:**
> ```
> Input: head = [0,1,2], k = 4
> Output: [2,0,1]
> ```
> 
> **Constraints:**
> - The number of nodes in the list is in the range [0, 500].
> - -100 <= Node.val <= 100
> - 0 <= k <= 2 * 10^9

> [!info] Approach
> A rotation just changes where the tail reconnects to the head. Once you know the list length, you can convert the problem into a cut point. Make the list circular, compute `k % n`, and cut at the new tail. Find tail and length, connect tail to head, advance to the new tail `n - k - 1` steps from the head, then break the cycle.

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

### ==LRU Cache (Doubly Linked List + Hash Map) `🔥 Google`

> [!example] Problem
> Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.
> Implement the LRUCache class:
> The functions get and put must each run in O(1) average time complexity.
> 
> **Example 1:**
> ```
> Input
> ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
> [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
> Output
> [null, null, null, 1, null, -1, null, -1, 3, 4]
> 
> Explanation
> LRUCache lRUCache = new LRUCache(2);
> lRUCache.put(1, 1); // cache is {1=1}
> lRUCache.put(2, 2); // cache is {1=1, 2=2}
> lRUCache.get(1);    // return 1
> lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
> lRUCache.get(2);    // returns -1 (not found)
> lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
> lRUCache.get(1);    // return -1 (not found)
> lRUCache.get(3);    // return 3
> lRUCache.get(4);    // return 4
> ```
> 
> **Constraints:**
> - 1 <= capacity <= 3000
> - 0 <= key <= 10^4
> - 0 <= value <= 10^5
> - At most 2 * 10^5 calls will be made to get and put.

> [!info] Approach
> A hash map gives O(1) lookup but can't track recency. A doubly linked list lets us move any node to the head (most recently used) in O(1) using pointers. Together they solve both requirements. Maintain a dict `key -> node`. The DLL has a sentinel head (most recent) and tail (least recent). On every access, unlink the node and re-insert it just after the head. `get`: if key missing return -1, else move node to front and return value. `put`: if key exists update value and move to front; if new key and at capacity, remove the node just before the tail (LRU), then insert new node at front.

> [!note]- Python Solution
> ```python
> class Node:
>     def __init__(self, key=0, val=0):
>         self.key = key
>         self.val = val
>         self.prev = None
>         self.next = None
> >
> class LRUCache:
>     def __init__(self, capacity):
>         self.cap = capacity
>         self.cache = {}
>         self.head = Node()   # most recent sentinel
>         self.tail = Node()   # least recent sentinel
>         self.head.next = self.tail
>         self.tail.prev = self.head
> >
>     def _remove(self, node):
>         node.prev.next = node.next
>         node.next.prev = node.prev
> >
>     def _insert_front(self, node):
>         node.next = self.head.next
>         node.prev = self.head
>         self.head.next.prev = node
>         self.head.next = node
> >
>     def get(self, key):
>         if key not in self.cache:
>             return -1
>         node = self.cache[key]
>         self._remove(node)
>         self._insert_front(node)
>         return node.val
> >
>     def put(self, key, value):
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

