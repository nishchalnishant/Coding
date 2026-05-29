---
module: 02-algorithms
topic: Two Pointers
subtopic: 
status: unread
tags: [algorithms, two-pointers]
---
## First-Principles Map

```text
WHY Two Pointers exists
├── Brute-force pair enumeration is O(n²) — too slow for n ≥ 10⁵
│   ├── Sorted order creates monotone structure: moving one pointer predictably affects the other
│   └── Eliminate invalid pairs in O(1) instead of checking all combinations
WHAT it is
├── Two indices moving through a sequence, together encoding the current candidate
│   ├── Opposite ends: left=0, right=n-1, converge inward (2-sum, container with most water)
│   └── Same direction: slow/fast (cycle detection, remove duplicates, nth-from-end)
HOW it works
├── Opposite-ends pattern (sorted array required)
│   ├── sum < target → move left rightward (increase sum)
│   ├── sum > target → move right leftward (decrease sum)
│   └── sum == target → record; advance both
├── Fast/slow pattern (linked list or array)
│   ├── fast advances 2, slow advances 1 → meet in cycle if one exists
│   └── Separate by k: advance fast k steps first, then move both
WHEN to use
├── "pair / triplet summing to target in sorted array" → opposite-ends O(n)
├── "detect cycle in linked list" → Floyd's fast/slow O(n) O(1)
└── "remove duplicates / partition in-place" → slow/fast write pointer O(n)
WHAT can go wrong
├── Using on unsorted array for sum problems → correctness breaks (sort first)
├── Infinite loop: forgetting to advance both pointers on match
└── Triplet/k-sum: not deduplicating pointers → duplicate results
DECISION
└── Sorted array + pair/triplet constraint → two pointers O(n); unsorted + O(n) needed → hashmap instead
```

## First-Principles Breakdown

- **Root problem**: Find pairs or partition a sequence in O(n) without nested loops, by exploiting sorted order or pointer separation.
- **Core insight**: In a sorted array, the sum of arr[left] + arr[right] is monotonically controlled — moving one pointer has a guaranteed directional effect on the sum.
- **Invariant**: At every step, all pairs that could involve indices already passed have been correctly handled (accepted or rejected).
- **Why it works**: Each pointer moves at most n steps in one direction → O(n) total comparisons for the whole search.
- **Where it breaks**: Unsorted data (sort first, adding O(n log n)); problems requiring non-contiguous or multi-pass pairing where pointer convergence doesn't cover all candidates.

---

# Two Pointers

```
[TWO POINTERS — MINDMAP]
├── WHY IT EXISTS
│   ├── Brute force nested loops → O(N²) for pair/subarray problems
│   ├── Sorted structure allows reasoning about element relationships
│   └── Moving pointers inward/outward eliminates impossible pairs in O(1)
├── WHAT IT IS
│   ├── Core invariant: two indices (left, right) traversing a structure
│   ├── Pointers move toward each other (opposite ends) OR in same direction
│   └── Decision at each step: move left, move right, or record answer
├── HOW IT WORKS
│   ├── Variant A — Opposite ends (sorted array)
│   │   ├── Step 1: left = 0, right = len-1
│   │   ├── Step 2: check condition (sum vs target, palindrome, etc.)
│   │   ├── Step 3: if too small → left++; if too large → right--
│   │   └── Step 4: stop when left >= right
│   ├── Variant B — Same direction (fast/slow, partition)
│   │   ├── Step 1: slow = 0, fast = 0 (or fast = 1)
│   │   ├── Step 2: fast advances every iteration
│   │   ├── Step 3: slow advances only when condition is met
│   │   └── Step 4: slow marks "last valid" position
│   └── Variant C — Two arrays / merge
│       ├── Step 1: pointer on each sorted array
│       └── Step 2: advance the pointer with smaller element
├── COMPLEXITY
│   ├── Time:  O(N) — each pointer moves at most N steps total
│   └── Space: O(1) — no auxiliary structure
├── TRIGGER PATTERNS (when to use)
│   ├── "Sorted array" + "find pair with sum = target" → opposite ends
│   ├── "Remove duplicates / move zeros in-place" → slow/fast same dir
│   ├── "Palindrome check" → opposite ends meeting middle
│   ├── "Container with most water / trapping rain water" → opposite ends
│   ├── "3Sum / 4Sum" → fix outer loop, two-pointer inner
│   ├── "Linked list: cycle, middle, kth from end" → fast/slow pointers
│   └── "Merge two sorted arrays" → two-pointer merge
└── GOTCHAS
    ├── Only works on sorted input for pair-sum variant — sort first if needed
    ├── Duplicate handling: skip duplicates after recording answer to avoid repeats
    ├── Linked list cycle: Floyd's — fast moves 2, slow moves 1; meet ≠ cycle start
    ├── Off-by-one: use left < right (not <=) to avoid processing same element twice
    └── 3Sum time is O(N²) — sort + two-pointer inner; not O(N)
```

## When to Use

**Trigger keywords:** sorted array, pair/triplet sum, palindrome check, partition, remove duplicates, container/water, cycle detection, linked list middle.

**Use when:** you need O(n) over O(n²) brute force on a linear structure, especially with sorted data or when searching for a pair satisfying a constraint.

---

## Variant 1: Converging Pointers (Opposite Ends)

**Use for:** pair sum in sorted array, 3Sum, container with most water, palindrome check, trapping rain water.

```python
def converging(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        s = arr[lo] + arr[hi]
        if s == target:
            return (lo, hi)      # found
        elif s < target:
            lo += 1              # need larger sum
        else:
            hi -= 1              # need smaller sum
    return (-1, -1)
```

**3Sum template:**
```python
def three_sum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]:  # skip duplicate anchors
            continue
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s == 0:
                result.append([nums[i], nums[lo], nums[hi]])
                while lo < hi and nums[lo] == nums[lo+1]: lo += 1  # skip dups
                while lo < hi and nums[hi] == nums[hi-1]: hi -= 1  # skip dups
                lo += 1; hi -= 1
            elif s < 0: lo += 1
            else: hi -= 1
    return result
```

**Complexity:** O(n) per pass (O(n²) for 3Sum due to outer loop).

---

## Variant 2: Fast / Slow Pointers (Floyd's)

**Use for:** cycle detection in linked list, find cycle entry point, middle of linked list, happy number, duplicate in array.

```python
# Middle of linked list
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow  # slow is at middle (upper-mid for even length)

# Cycle detection (Floyd's)
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

# Cycle entry point
def cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None  # no cycle
    slow = head       # reset one pointer to head
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow       # meeting point is cycle start
```

**Why cycle entry works:** Distance from head to cycle start equals distance from meeting point to cycle start (mathematical proof via modular arithmetic).

**Complexity:** O(n) time, O(1) space.

---

## Variant 3: Same-Direction Pointers

**Use for:** remove duplicates (in-place), sliding window-like partition, valid palindrome with skip, array partitioning, Dutch National Flag.

```python
# Remove duplicates from sorted array (in-place)
def remove_duplicates(nums):
    if not nums: return 0
    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[read - 1]:
            nums[write] = nums[read]
            write += 1
    return write  # new length

# Partition: move all zeros to end
def move_zeros(nums):
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write] = nums[read]
            write += 1
    for i in range(write, len(nums)):
        nums[i] = 0

# Dutch National Flag (sort 0s, 1s, 2s)
def sort_colors(nums):
    lo, mid, hi = 0, 0, len(nums) - 1
    while mid <= hi:
        if nums[mid] == 0:
            nums[lo], nums[mid] = nums[mid], nums[lo]
            lo += 1; mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[hi] = nums[hi], nums[mid]
            hi -= 1  # don't increment mid — newly swapped element unchecked
```

**Complexity:** O(n) time, O(1) space.

---

## Complexity Summary

| Variant | Time | Space | Notes |
|---------|------|-------|-------|
| Converging | O(n) | O(1) | Requires sorted input |
| Fast/Slow | O(n) | O(1) | Works on linked lists and arrays |
| Same-direction | O(n) | O(1) | In-place modification |

---

## Canonical Problems

| Problem | Variant | Key Insight | Common Mistake |
|---------|---------|-------------|----------------|
| Two Sum II (sorted) | Converging | Move pointer based on sum vs target | Using hash map when sorted → two pointers is O(1) space |
| 3Sum | Converging + anchor | Sort first; skip duplicates at anchor AND inner pointers | Forgetting to skip dups after finding a valid triplet |
| Container With Most Water | Converging | Always move the shorter side (taller side can't improve min) | Moving taller side — never improves result |
| Valid Palindrome II | Converging | On mismatch, try skipping either left or right char | Not checking both skip options |
| Linked List Cycle | Fast/Slow | Fast moves 2x; if cycle exists they must meet | Not handling `fast.next` null check |
| Find Cycle Start | Fast/Slow | Reset one pointer to head after meeting; single-step both | Resetting wrong pointer or continuing from meeting point |
| Middle of Linked List | Fast/Slow | Even length: `fast and fast.next` → slow stops at upper-mid | Off-by-one on even-length list |
| Remove Duplicates (Sorted) | Same-direction | Write pointer only advances on new value | Comparing wrong index pair |

---

## Edge Cases

- **Empty array / single element:** Check `len < 2` before initializing both pointers.
- **All same elements:** Converging — loop terminates immediately. Duplicate-skip in 3Sum must handle `[0,0,0,0]`.
- **Negative numbers in 3Sum:** Sort handles this; don't assume non-negative.
- **Even vs odd length list:** Middle of linked list — `fast and fast.next` terminates correctly for both.
- **Cycle at head:** Cycle entry point algorithm handles this; do not special-case.
- **`while lo < hi` vs `while lo <= hi`:** Use `<` for pair-search (lo == hi is same element). Use `<=` only when you want to process that case.
