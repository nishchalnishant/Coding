---
tags: [coding, data-structures, heap]
topic: heap
difficulty: mixed
---

# Heap Problems

---

## Top-K Pattern

### Kth Largest Element in a Stream

> [!example] Problem
> Design a class that finds the `k`th largest element in a stream. `add(val)` inserts a new value and returns the current `k`th largest.

> [!info] Approach
> - **WHY:** We need the `k`th largest at all times without sorting after every insert.
> - **WHAT:** A min-heap of size exactly `k` holds the top-`k` elements seen so far. The root (minimum of the heap) is always the `k`th largest.
> - **HOW:** On each `add`, push the new value. If heap size exceeds `k`, pop the minimum. Root is the answer in O(1); each insert is O(log k).

> [!note]- Python Solution
> ```python
> import heapq
>
> class KthLargest:
>     def __init__(self, k: int, nums: list[int]) -> None:
>         self.k = k
>         self.heap: list[int] = []
>         for n in nums:
>             self.add(n)
>
>     def add(self, val: int) -> int:
>         heapq.heappush(self.heap, val)
>         if len(self.heap) > self.k:
>             heapq.heappop(self.heap)
>         return self.heap[0]
> ```

> [!success] Complexity
> Time O(log k) per add; Space O(k).

> [!tip] Alternatives
> Sort the full list each time — O(n log n) per insert, too slow. QuickSelect gives O(n) one-shot but cannot handle a stream.

---

### Last Stone Weight

> [!example] Problem
> Each turn smash the two heaviest stones. If equal, both destroyed; otherwise the difference survives. Return the weight of the last stone (or 0).

> [!info] Approach
> - **WHY:** We always need the two current maximums — repeated maximum extraction is a max-heap problem.
> - **WHAT:** A max-heap (negate for Python's min-heap) gives O(log n) each pop/push.
> - **HOW:** Pop twice, push `abs(a - b)` if non-zero. Repeat until one or zero stones remain.

> [!note]- Python Solution
> ```python
> import heapq
>
> def last_stone_weight(stones: list[int]) -> int:
>     heap = [-s for s in stones]
>     heapq.heapify(heap)
>     while len(heap) > 1:
>         a = -heapq.heappop(heap)
>         b = -heapq.heappop(heap)
>         if a != b:
>             heapq.heappush(heap, -(a - b))
>     return -heap[0] if heap else 0
> ```

> [!success] Complexity
> Time O(n log n); Space O(n).

> [!tip] Alternatives
> Sorted list with bisect — insert/delete O(n) due to shifting, worse in practice.

---

### K Closest Points to Origin

> [!example] Problem
> Given `n` points, return the `k` closest to the origin `(0, 0)` (Euclidean distance).

> [!info] Approach
> - **WHY:** Want the `k` smallest by distance without fully sorting n points.
> - **WHAT:** Max-heap of size `k` on squared distance (no sqrt needed — monotone with distance).
> - **HOW:** For each point compute `x²+y²`. Push `(-dist, x, y)` onto a max-heap. If size exceeds `k`, pop the farthest. Remaining heap contains the `k` closest.

> [!note]- Python Solution
> ```python
> import heapq
>
> def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
>     heap: list[tuple[int, int, int]] = []
>     for x, y in points:
>         dist = -(x * x + y * y)
>         heapq.heappush(heap, (dist, x, y))
>         if len(heap) > k:
>             heapq.heappop(heap)
>     return [[x, y] for _, x, y in heap]
> ```

> [!success] Complexity
> Time O(n log k); Space O(k).

> [!tip] Alternatives
> QuickSelect O(n) average with partial sort — optimal for one-shot but harder to implement correctly; full sort O(n log n).

---

### Top K Frequent Elements

> [!example] Problem
> Given an integer array, return the `k` most frequent elements.

> [!info] Approach
> - **WHY:** Need the `k` elements by frequency, not by value.
> - **WHAT:** Count frequencies, then use a min-heap of size `k` on `(freq, element)`. Root is the least frequent among the top-`k` — pop when overflow.
> - **HOW:** Build `Counter` in O(n). Heap push `(freq, num)` for each unique num; pop when size > k. Alternatively, bucket sort by frequency for O(n).

> [!note]- Python Solution
> ```python
> import heapq
> from collections import Counter
>
> def top_k_frequent(nums: list[int], k: int) -> list[int]:
>     count = Counter(nums)
>     # Bucket sort: O(n) — index = frequency
>     buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
>     for num, freq in count.items():
>         buckets[freq].append(num)
>     result: list[int] = []
>     for freq in range(len(buckets) - 1, 0, -1):
>         result.extend(buckets[freq])
>         if len(result) >= k:
>             return result[:k]
>     return result
> ```

> [!success] Complexity
> Time O(n) with bucket sort; O(n log k) with heap. Space O(n).

> [!tip] Alternatives
> `heapq.nlargest(k, count.items(), key=lambda x: x[1])` — clean but O(n log k).

---

### Furthest Building You Can Reach

> [!example] Problem
> Given building heights, `bricks`, and `ladders`, greedily use resources to advance. Ladders handle any jump; bricks handle a jump of exactly that size. Maximize the building index reached.

> [!info] Approach
> - **WHY:** We want to save ladders for the largest jumps but can't see the future — greedy with reconsideration.
> - **WHAT:** Min-heap tracks the sizes of jumps where we used a ladder. When bricks run out, swap the smallest ladder-jump back to bricks if possible.
> - **HOW:** For each upward jump, assign a ladder (push jump to heap). If ladders exhausted, pop the smallest ladder-jump, reclaim it as bricks. If bricks insufficient for the current jump, stop.

> [!note]- Python Solution
> ```python
> import heapq
>
> def furthest_building(heights: list[int], bricks: int, ladders: int) -> int:
>     heap: list[int] = []  # min-heap of ladder-used jump sizes
>     for i in range(len(heights) - 1):
>         diff = heights[i + 1] - heights[i]
>         if diff <= 0:
>             continue
>         heapq.heappush(heap, diff)
>         if len(heap) > ladders:
>             # Swap the smallest ladder-jump to bricks
>             bricks -= heapq.heappop(heap)
>         if bricks < 0:
>             return i
>     return len(heights) - 1
> ```

> [!success] Complexity
> Time O(n log ladders); Space O(ladders).

> [!tip] Alternatives
> Binary search on the answer + greedy check — O(n log n) but more complex. The heap approach is canonical.

---

### Kth Largest Element in an Array

> [!example] Problem
> Find the `k`th largest element in an unsorted array (not the `k`th distinct element).

> [!info] Approach
> - **WHY:** Sorting is O(n log n) but we only need one order-statistic. A size-k min-heap scans once.
> - **WHAT:** Min-heap of size exactly `k`. After processing all elements, the root is the k-th largest.
> - **HOW:** For each number, push to heap. If heap exceeds size `k`, pop the minimum. Root after full pass is the answer in O(1).

> [!note]- Python Solution
> ```python
> import heapq
>
> def find_kth_largest(nums: list[int], k: int) -> int:
>     heap: list[int] = []
>     for n in nums:
>         heapq.heappush(heap, n)
>         if len(heap) > k:
>             heapq.heappop(heap)
>     return heap[0]
> ```

> [!success] Complexity
> Time O(n log k); Space O(k).

> [!tip] Alternatives
> QuickSelect — O(n) average, O(n²) worst; in-place, no extra memory. `heapq.nlargest(k, nums)[-1]` is idiomatic but O(n log k) internally.

---

### Top K Frequent Words

> [!example] Problem
> Given a list of words, return the `k` most frequent words sorted by frequency (descending), with ties broken lexicographically.

> [!info] Approach
> - **WHY:** Two sort keys — frequency (desc) and lexicographic (asc) — make a plain max-heap awkward. A min-heap with negated frequency and regular string comparison handles both.
> - **WHAT:** Min-heap of `(-freq, word)`. Python compares tuples element-by-element: ties on frequency fall through to lexicographic comparison, keeping the lexicographically larger word at the top (to be evicted first).
> - **HOW:** Count with `Counter`. Push `(-freq, word)` for each unique word. When heap exceeds `k`, pop. Collect remaining `k` entries and reverse-sort for output order.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import Counter
>
> def top_k_frequent_words(words: list[str], k: int) -> list[str]:
>     count = Counter(words)
>     heap: list[tuple[int, str]] = []
>     for word, freq in count.items():
>         heapq.heappush(heap, (-freq, word))
>         if len(heap) > k:
>             heapq.heappop(heap)
>     # heap has k entries; sort for correct output order
>     result = sorted(heap, key=lambda x: (x[0], x[1]))
>     return [word for _, word in result]
> ```

> [!success] Complexity
> Time O(n + m log k) where m = unique words; Space O(m).

> [!tip] Alternatives
> `Counter.most_common()` then sort by `(-freq, word)` — O(m log m), clean for interviews. The heap version is O(m log k) which matters when k << m.

---

## Scheduling / Reorganization

### Task Scheduler

> [!example] Problem
> Given tasks (letters) and a cooldown `n`, find the minimum time to finish all tasks. Same task must have at least `n` intervals gap.

> [!info] Approach
> - **WHY:** The bottleneck is the most frequent task — it forces idle gaps.
> - **WHAT:** Math formula: `(max_freq - 1) * (n + 1) + count_of_tasks_with_max_freq`, capped at `len(tasks)`. When variety fills all slots, there's no idle time.
> - **HOW:** Count frequencies. Compute `max_freq`. The formula models "frames" of size `n+1` with the most frequent task anchoring each frame. Return `max(formula, len(tasks))`.

> [!note]- Python Solution
> ```python
> from collections import Counter
>
> def least_interval(tasks: list[str], n: int) -> int:
>     freq = Counter(tasks)
>     max_freq = max(freq.values())
>     count_max = sum(1 for v in freq.values() if v == max_freq)
>     # Frames: (max_freq-1) full frames + last partial frame
>     formula = (max_freq - 1) * (n + 1) + count_max
>     return max(formula, len(tasks))
> ```

> [!success] Complexity
> Time O(n); Space O(1) — only 26 task types.

> [!tip] Alternatives
> Simulation with max-heap + queue for cooldown tracking — O(t log 26) but matches the intuition more directly. Use for follow-ups requiring the actual schedule order.

---

### Reorganize String

> [!example] Problem
> Rearrange a string so no two adjacent characters are the same. Return `""` if impossible.

> [!info] Approach
> - **WHY:** To prevent repeats, always place the most frequent remaining character that isn't equal to the last placed.
> - **WHAT:** Max-heap by frequency. Each step, pop the most frequent, append it. If it equals the last placed character, pop the second most frequent instead, then push the first back.
> - **HOW:** Impossible if `max_freq > (len(s) + 1) // 2`. Otherwise, greedily fill from the heap.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import Counter
>
> def reorganize_string(s: str) -> str:
>     freq = Counter(s)
>     heap = [(-cnt, ch) for ch, cnt in freq.items()]
>     heapq.heapify(heap)
>     result: list[str] = []
>     prev_cnt, prev_ch = 0, ''
>     while heap:
>         cnt, ch = heapq.heappop(heap)
>         result.append(ch)
>         if prev_cnt < 0:
>             heapq.heappush(heap, (prev_cnt, prev_ch))
>         prev_cnt, prev_ch = cnt + 1, ch  # increment (negated, so +1 = less frequent)
>     return ''.join(result) if len(result) == len(s) else ''
> ```

> [!success] Complexity
> Time O(n log k) where k ≤ 26; Space O(k).

> [!tip] Alternatives
> Interleave approach — place most frequent chars at even indices first (O(n), simpler). Heap approach generalizes to arbitrary constraints.

---

## Two Heaps

### Find Median from Data Stream

> [!example] Problem
> Design a data structure supporting `add_num(num)` and `find_median()` on a dynamic stream.

> [!info] Approach
> - **WHY:** Finding the median requires the middle element(s). Sorting after each insert is O(n log n).
> - **WHAT:** Two heaps partition at the median: `lo` (max-heap, lower half) and `hi` (min-heap, upper half). Invariant: `max(lo) <= min(hi)` and `|len(lo) - len(hi)| <= 1`.
> - **HOW:** Always push to `lo`, then move `lo`'s max to `hi` to maintain order. Rebalance sizes so `lo` is never smaller than `hi`. Median is either `lo[0]` or the average of both tops.

> [!note]- Python Solution
> ```python
> import heapq
>
> class MedianFinder:
>     def __init__(self) -> None:
>         self._lo: list[int] = []  # max-heap (negated)
>         self._hi: list[int] = []  # min-heap
>
>     def add_num(self, num: int) -> None:
>         heapq.heappush(self._lo, -num)
>         heapq.heappush(self._hi, -heapq.heappop(self._lo))
>         if len(self._lo) < len(self._hi):
>             heapq.heappush(self._lo, -heapq.heappop(self._hi))
>
>     def find_median(self) -> float:
>         if len(self._lo) > len(self._hi):
>             return float(-self._lo[0])
>         return (-self._lo[0] + self._hi[0]) / 2.0
> ```

> [!success] Complexity
> Time O(log n) per add, O(1) find_median; Space O(n).

> [!tip] Alternatives
> Order statistics tree (AVL with rank augmentation) — O(log n) all ops but complex to implement. Segment tree on compressed values for integer streams.

---

### Sliding Window Median

> [!example] Problem
> Given array `nums` and window size `k`, return the median of each sliding window.

> [!info] Approach
> - **WHY:** Naively recomputing the median per window is O(nk). We need to handle sliding-out elements efficiently.
> - **WHAT:** Two heaps + lazy deletion. Track elements that have left the window in a `Counter`. When they surface at heap tops during pop, discard them.
> - **HOW:** Maintain `lo` (max-heap) and `hi` (min-heap). Slide window: add new element, mark removed element as "invalid". Rebalance heaps. When reading tops, skip invalid elements.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import defaultdict
>
> def median_sliding_window(nums: list[int], k: int) -> list[float]:
>     lo: list[int] = []  # max-heap (negated), lower half
>     hi: list[int] = []  # min-heap, upper half
>     invalid: dict[int, int] = defaultdict(int)
>
>     def balance(size_lo: int, size_hi: int) -> tuple[int, int]:
>         # Ensure lo has ceil(k/2) and hi has floor(k/2)
>         while size_lo > (k + 1) // 2:
>             heapq.heappush(hi, -heapq.heappop(lo))
>             size_lo -= 1; size_hi += 1
>         while size_hi > k // 2:
>             heapq.heappush(lo, -heapq.heappop(hi))
>             size_hi -= 1; size_lo += 1
>         return size_lo, size_hi
>
>     def clean_top(heap: list[int], negate: bool) -> None:
>         while heap:
>             val = -heap[0] if negate else heap[0]
>             if invalid[val] > 0:
>                 invalid[val] -= 1
>                 heapq.heappop(heap)
>             else:
>                 break
>
>     # Seed first window
>     for x in nums[:k]:
>         heapq.heappush(lo, -x)
>     for _ in range(k // 2):
>         heapq.heappush(hi, -heapq.heappop(lo))
>
>     def get_median() -> float:
>         clean_top(lo, True); clean_top(hi, False)
>         if k % 2 == 1:
>             return float(-lo[0])
>         return (-lo[0] + hi[0]) / 2.0
>
>     result = [get_median()]
>     size_lo, size_hi = (k + 1) // 2, k // 2
>
>     for i in range(k, len(nums)):
>         out_val = nums[i - k]
>         in_val = nums[i]
>         invalid[out_val] += 1
>         # Adjust sizes
>         if in_val <= -lo[0]:
>             heapq.heappush(lo, -in_val); size_lo += 1
>         else:
>             heapq.heappush(hi, in_val); size_hi += 1
>         if out_val <= -lo[0]:
>             size_lo -= 1
>         else:
>             size_hi -= 1
>         size_lo, size_hi = balance(size_lo, size_hi)
>         clean_top(lo, True); clean_top(hi, False)
>         result.append(get_median())
>     return result
> ```

> [!success] Complexity
> Time O(n log k) amortized; Space O(k).

> [!tip] Alternatives
> SortedList (Python `sortedcontainers`) — O(n log k) clean but not available in interviews. Segment tree on coordinate-compressed values — O(n log n).

---

### IPO (Maximize Capital)

> [!example] Problem
> Given `k` project slots, initial capital `w`, and lists of `profits` and `capital` requirements, maximize final capital by picking at most `k` projects.

> [!info] Approach
> - **WHY:** Greedy — always take the most profitable project currently affordable. Projects unlock as capital grows.
> - **WHAT:** Sort projects by required capital. Sweep a pointer to unlock affordable projects into a max-heap of profits. Each round, pop the best available profit.
> - **HOW:** Sort `zip(capital, profits)` by capital. Use a pointer `i` advancing when `projects[i][0] <= w`. Max-heap holds unlocked profits (negated). Repeat `k` times.

> [!note]- Python Solution
> ```python
> import heapq
>
> def find_maximized_capital(k: int, w: int, profits: list[int], capital: list[int]) -> int:
>     projects = sorted(zip(capital, profits))
>     available: list[int] = []  # max-heap (negated profits)
>     i = 0
>     for _ in range(k):
>         while i < len(projects) and projects[i][0] <= w:
>             heapq.heappush(available, -projects[i][1])
>             i += 1
>         if not available:
>             break
>         w += -heapq.heappop(available)
>     return w
> ```

> [!success] Complexity
> Time O(n log n) sort + O(k log n) heap ops; Space O(n).

> [!tip] Alternatives
> No fundamentally better approach — the two-structure design (sorted array + heap) is optimal. DP would be O(nk), much worse.

---

## K-Way Merge

### Merge K Sorted Lists

> [!example] Problem
> Merge `k` sorted linked lists into one sorted linked list.

> [!info] Approach
> - **WHY:** Naive pairwise merge is O(nk). We want O(n log k) by always extracting the global minimum across k list heads.
> - **WHAT:** Min-heap of size k holds one `(value, list_id, node)` tuple per list. Pop gives the global min; push the next node from that list.
> - **HOW:** Seed heap with head of each non-null list. Use `list_id` as tie-breaker to avoid comparing `ListNode` objects (not comparable in Python).

> [!note]- Python Solution
> ```python
> import heapq
> from typing import Optional
>
> class ListNode:
>     def __init__(self, val: int = 0, next: 'Optional[ListNode]' = None):
>         self.val = val
>         self.next = next
>
> def merge_k_lists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
>     heap: list[tuple[int, int, ListNode]] = []
>     for i, node in enumerate(lists):
>         if node:
>             heapq.heappush(heap, (node.val, i, node))
>     dummy = ListNode(0)
>     cur = dummy
>     while heap:
>         val, i, node = heapq.heappop(heap)
>         cur.next = node
>         cur = cur.next
>         if node.next:
>             heapq.heappush(heap, (node.next.val, i, node.next))
>     return dummy.next
> ```

> [!success] Complexity
> Time O(n log k) where n = total nodes; Space O(k) heap.

> [!tip] Alternatives
> Divide-and-conquer pairwise merge — same O(n log k) but simpler to reason about; no heap needed.

---

### Find K Pairs with Smallest Sums

> [!example] Problem
> Given two sorted arrays `nums1` and `nums2`, find the `k` pairs `(u, v)` with the smallest `u + v`.

> [!info] Approach
> - **WHY:** There are `m*n` possible pairs — we need the k smallest without enumerating all.
> - **WHAT:** Treat this as a k-way merge: each row `i` of the implicit `m x n` sum matrix is sorted (since `nums2` is sorted). Seed heap with `(nums1[i] + nums2[0], i, 0)` for each `i`.
> - **HOW:** Pop smallest `(sum, i, j)`, record pair. Push `(nums1[i] + nums2[j+1], i, j+1)` if `j+1 < len(nums2)`. Stop after k pops.

> [!note]- Python Solution
> ```python
> import heapq
>
> def k_smallest_pairs(nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
>     if not nums1 or not nums2:
>         return []
>     heap: list[tuple[int, int, int]] = []
>     for i in range(min(len(nums1), k)):
>         heapq.heappush(heap, (nums1[i] + nums2[0], i, 0))
>     result: list[list[int]] = []
>     while heap and len(result) < k:
>         s, i, j = heapq.heappop(heap)
>         result.append([nums1[i], nums2[j]])
>         if j + 1 < len(nums2):
>             heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
>     return result
> ```

> [!success] Complexity
> Time O(k log min(m, k)); Space O(min(m, k)).

> [!tip] Alternatives
> Generate all pairs, sort — O(mn log mn), not feasible for large inputs.

---

### Kth Smallest Element in a Sorted Matrix

> [!example] Problem
> Given an `n x n` matrix where each row and column is sorted, find the `k`th smallest element.

> [!info] Approach
> - **WHY:** Each row is a sorted list — this is K-way merge of n sorted arrays.
> - **WHAT:** Min-heap seeded with the first element of each row. Pop `k` times; each pop advances the column in that row.
> - **HOW:** Push `(matrix[i][0], i, 0)` for all `i`. Pop k-1 times advancing `(matrix[i][j+1], i, j+1)`. The k-th pop is the answer.

> [!note]- Python Solution
> ```python
> import heapq
>
> def kth_smallest(matrix: list[list[int]], k: int) -> int:
>     n = len(matrix)
>     heap: list[tuple[int, int, int]] = [(matrix[i][0], i, 0) for i in range(n)]
>     heapq.heapify(heap)
>     val = 0
>     for _ in range(k):
>         val, i, j = heapq.heappop(heap)
>         if j + 1 < n:
>             heapq.heappush(heap, (matrix[i][j + 1], i, j + 1))
>     return val
> ```

> [!success] Complexity
> Time O(k log n); Space O(n).

> [!tip] Alternatives
> Binary search on value range — O(n log(max - min)) with O(n) count function. Better when k is close to n².

---

### Smallest Range Covering Elements from K Lists (Heap Variant)

> [!example] Problem
> Find the smallest range `[a, b]` such that at least one element from each of `k` lists lies in the range.

> [!info] Approach
> - **WHY:** We need a window containing one element per list. Sliding window on a sorted merged sequence won't track list coverage.
> - **WHAT:** K-way merge with a global max tracker. The current range is `[heap_min, current_max]`. Advance the minimum (pop from heap, push next from same list) to shrink the range.
> - **HOW:** Seed heap with `(lists[i][0], i, 0)`. Track `cur_max = max of all initial first elements`. Each pop gives a new candidate min; update range if `cur_max - min` is smaller. Stop when any list is exhausted.

> [!note]- Python Solution
> ```python
> import heapq
>
> def smallest_range(nums: list[list[int]]) -> list[int]:
>     heap: list[tuple[int, int, int]] = []
>     cur_max = float('-inf')
>     for i, lst in enumerate(nums):
>         heapq.heappush(heap, (lst[0], i, 0))
>         cur_max = max(cur_max, lst[0])
>     best = [heap[0][0], int(cur_max)]
>     while True:
>         val, i, j = heapq.heappop(heap)
>         if j + 1 == len(nums[i]):
>             break  # list exhausted — can't cover all lists anymore
>         nxt = nums[i][j + 1]
>         heapq.heappush(heap, (nxt, i, j + 1))
>         cur_max = max(cur_max, nxt)
>         cur_min = heap[0][0]
>         if cur_max - cur_min < best[1] - best[0]:
>             best = [cur_min, cur_max]
>     return best
> ```

> [!success] Complexity
> Time O(n log k) where n = total elements; Space O(k).

> [!tip] Alternatives
> Merge all lists with source tags, sort, then sliding window to find minimum range with all k sources — same O(n log n) but simpler to reason about at the cost of O(n) extra space.

---

### K-th Smallest in M Sorted Arrays

> [!example] Problem
> Given `m` sorted arrays of total `n` elements, find the `k`th smallest element across all arrays.

> [!info] Approach
> - **WHY:** This is the general form of "Kth Smallest in a Sorted Matrix" — M sorted sequences, find the k-th minimum globally.
> - **WHAT:** Min-heap seeded with the first element of each array. Pop once per step, advance that array's pointer. After k pops, the last popped is the answer.
> - **HOW:** Push `(arrays[i][0], i, 0)` for all i. Pop and push `(arrays[i][j+1], i, j+1)` until k pops done.

> [!note]- Python Solution
> ```python
> import heapq
>
> def kth_smallest_m_arrays(arrays: list[list[int]], k: int) -> int:
>     heap: list[tuple[int, int, int]] = []
>     for i, arr in enumerate(arrays):
>         if arr:
>             heapq.heappush(heap, (arr[0], i, 0))
>     val = 0
>     for _ in range(k):
>         val, i, j = heapq.heappop(heap)
>         if j + 1 < len(arrays[i]):
>             heapq.heappush(heap, (arrays[i][j + 1], i, j + 1))
>     return val
> ```

> [!success] Complexity
> Time O(k log m); Space O(m).

> [!tip] Alternatives
> Binary search on value + count function — O(m log(max-min) * log(total_n)). Useful when k is large or m is huge.

---

### Maximum CPU Load

> [!example] Problem
> Given a list of jobs `[start, end, load]`, find the maximum CPU load at any point in time (jobs can overlap).

> [!info] Approach
> - **WHY:** Classic interval overlap problem — need to track which jobs are active at each moment.
> - **WHAT:** Sort by start time. Use a min-heap keyed by end time to track active jobs. At each new job's start, evict all jobs that have ended.
> - **HOW:** Sort jobs by start. For each job, pop from heap all jobs with `end <= job.start`. Push current job's end time and load. Track running sum of active loads and record maximum.

> [!note]- Python Solution
> ```python
> import heapq
>
> def find_max_cpu_load(jobs: list[list[int]]) -> int:
>     jobs.sort(key=lambda x: x[0])
>     heap: list[tuple[int, int]] = []  # (end_time, load)
>     current_load = 0
>     max_load = 0
>     for start, end, load in jobs:
>         # Remove all jobs that ended before this one starts
>         while heap and heap[0][0] <= start:
>             _, ended_load = heapq.heappop(heap)
>             current_load -= ended_load
>         heapq.heappush(heap, (end, load))
>         current_load += load
>         max_load = max(max_load, current_load)
>     return max_load
> ```

> [!success] Complexity
> Time O(n log n); Space O(n).

> [!tip] Alternatives
> Sweep line with events — O(n log n), same complexity; easier to reason about when jobs have fractional times. Heap approach is more intuitive for interval problems in interviews.

---

## Dijkstra / Graph

### Network Delay Time

> [!example] Problem
> A directed weighted graph of `n` nodes; given signal source `k`, find the time for all nodes to receive the signal. Return `-1` if unreachable.

> [!info] Approach
> - **WHY:** Shortest path from a single source to all nodes — Dijkstra's algorithm.
> - **WHAT:** Min-heap of `(dist, node)`. Relax edges greedily. Once all nodes popped from heap, the maximum dist is the answer.
> - **HOW:** Build adjacency list. Push `(0, k)`. Pop min dist node; skip if already visited. Relax neighbors. Track visited set. Answer = `max(dist.values())` if `len(dist) == n` else `-1`.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import defaultdict
>
> def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
>     graph: dict[int, list[tuple[int, int]]] = defaultdict(list)
>     for u, v, w in times:
>         graph[u].append((w, v))
>     dist: dict[int, int] = {}
>     heap: list[tuple[int, int]] = [(0, k)]
>     while heap:
>         d, u = heapq.heappop(heap)
>         if u in dist:
>             continue
>         dist[u] = d
>         for w, v in graph[u]:
>             if v not in dist:
>                 heapq.heappush(heap, (d + w, v))
>     return max(dist.values()) if len(dist) == n else -1
> ```

> [!success] Complexity
> Time O((V + E) log V); Space O(V + E).

> [!tip] Alternatives
> Bellman-Ford — O(VE), handles negative weights but much slower. Floyd-Warshall — O(V³), all-pairs; overkill for single-source.

---

### Path with Minimum Effort

> [!example] Problem
> Grid of heights; move in 4 directions. Effort of a path = max absolute height difference between consecutive cells. Find min effort from top-left to bottom-right.

> [!info] Approach
> - **WHY:** Minimizing the maximum edge weight along a path — modified Dijkstra where "dist" is the bottleneck edge.
> - **WHAT:** Min-heap of `(effort, row, col)`. `effort` = max diff seen so far on the current path. Relax: new effort = `max(current_effort, abs(neighbor_height - current_height))`.
> - **HOW:** Push `(0, 0, 0)`. For each pop, update neighbors with `max(effort, abs diff)`. Skip if already visited at a better effort.

> [!note]- Python Solution
> ```python
> import heapq
>
> def minimum_effort_path(heights: list[list[int]]) -> int:
>     rows, cols = len(heights), len(heights[0])
>     dist = [[float('inf')] * cols for _ in range(rows)]
>     dist[0][0] = 0
>     heap: list[tuple[float, int, int]] = [(0, 0, 0)]
>     dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
>     while heap:
>         effort, r, c = heapq.heappop(heap)
>         if r == rows - 1 and c == cols - 1:
>             return int(effort)
>         if effort > dist[r][c]:
>             continue
>         for dr, dc in dirs:
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < rows and 0 <= nc < cols:
>                 new_effort = max(effort, abs(heights[nr][nc] - heights[r][c]))
>                 if new_effort < dist[nr][nc]:
>                     dist[nr][nc] = new_effort
>                     heapq.heappush(heap, (new_effort, nr, nc))
>     return 0
> ```

> [!success] Complexity
> Time O(m*n log(m*n)); Space O(m*n).

> [!tip] Alternatives
> Binary search on effort + BFS/DFS reachability check — O(m*n log(max_height)). Union-Find on edges sorted by weight — O(E log E), finds the answer when source and dest become connected.

---

### Swim in Rising Water

> [!example] Problem
> Grid where `grid[i][j]` is the elevation. Rain rises uniformly — at time `t` you can swim from any cell with elevation ≤ `t` to an adjacent one. Find minimum `t` to reach bottom-right from top-left.

> [!info] Approach
> - **WHY:** Same bottleneck-path structure as "Path with Minimum Effort" — minimize the maximum elevation encountered.
> - **WHAT:** Min-heap of `(elevation, row, col)`. The answer is the max elevation on the optimal path, i.e. when we reach `(n-1, n-1)` via Dijkstra-style expansion.
> - **HOW:** Push `(grid[0][0], 0, 0)`. Pop min elevation; if it's the destination return it. Mark visited. Push unvisited neighbors with `max(current_t, grid[nr][nc])`.

> [!note]- Python Solution
> ```python
> import heapq
>
> def swim_in_water(grid: list[list[int]]) -> int:
>     n = len(grid)
>     visited = [[False] * n for _ in range(n)]
>     heap: list[tuple[int, int, int]] = [(grid[0][0], 0, 0)]
>     dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
>     while heap:
>         t, r, c = heapq.heappop(heap)
>         if r == n - 1 and c == n - 1:
>             return t
>         if visited[r][c]:
>             continue
>         visited[r][c] = True
>         for dr, dc in dirs:
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc]:
>                 heapq.heappush(heap, (max(t, grid[nr][nc]), nr, nc))
>     return -1
> ```

> [!success] Complexity
> Time O(n² log n²); Space O(n²).

> [!tip] Alternatives
> Binary search on `t` + BFS connectivity — O(n² log n). Union-Find adding edges in elevation order — O(n² α(n²)), essentially linear. All three approaches appear in interviews.

---

## Design

### Design Twitter

> [!example] Problem
> Design a simplified Twitter: `post_tweet(userId, tweetId)`, `get_news_feed(userId)` (10 most recent tweets from self + followees), `follow(followerId, followeeId)`, `unfollow`.

> [!info] Approach
> - **WHY:** News feed merges multiple sorted tweet streams (one per followee) — this is K-way merge on recency.
> - **WHAT:** Store each user's tweets as a list (ordered by insertion = by time using a global counter). `get_news_feed` collects all candidate tweet lists and uses a max-heap on timestamp to extract the 10 most recent.
> - **HOW:** Global `time` counter increments with each tweet. Each user has a list of `(time, tweetId)`. For feed: seed heap with latest tweet from each followee+self. Pop max; push that user's next tweet. Collect 10.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import defaultdict
>
> class Twitter:
>     def __init__(self) -> None:
>         self._time = 0
>         self._tweets: dict[int, list[tuple[int, int]]] = defaultdict(list)
>         self._follows: dict[int, set[int]] = defaultdict(set)
>
>     def post_tweet(self, userId: int, tweetId: int) -> None:
>         self._tweets[userId].append((self._time, tweetId))
>         self._time += 1
>
>     def get_news_feed(self, userId: int) -> list[int]:
>         heap: list[tuple[int, int, int, int]] = []  # (-time, tweetId, userId, idx)
>         users = self._follows[userId] | {userId}
>         for uid in users:
>             tweets = self._tweets[uid]
>             if tweets:
>                 idx = len(tweets) - 1
>                 t, tid = tweets[idx]
>                 heapq.heappush(heap, (-t, tid, uid, idx - 1))
>         result: list[int] = []
>         while heap and len(result) < 10:
>             _, tid, uid, idx = heapq.heappop(heap)
>             result.append(tid)
>             if idx >= 0:
>                 t, next_tid = self._tweets[uid][idx]
>                 heapq.heappush(heap, (-t, next_tid, uid, idx - 1))
>         return result
>
>     def follow(self, followerId: int, followeeId: int) -> None:
>         self._follows[followerId].add(followeeId)
>
>     def unfollow(self, followerId: int, followeeId: int) -> None:
>         self._follows[followerId].discard(followeeId)
> ```

> [!success] Complexity
> `post_tweet` O(1); `get_news_feed` O(F log F + 10 log F) where F = followees; `follow/unfollow` O(1).

> [!tip] Alternatives
> Pre-materialized feeds with a write-fan-out — O(F) on each post, O(1) read; used in real systems for read-heavy workloads (Twitter's "fanout on write").

---

### Ugly Number II

> [!example] Problem
> An "ugly number" has only prime factors 2, 3, and 5. Return the `n`th ugly number (sequence: 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, …).

> [!info] Approach
> - **WHY:** We need to generate ugly numbers in order without iterating all integers.
> - **WHAT:** Min-heap seeded with `{1}`. Each pop gives the next ugly number; multiply by 2, 3, 5 to generate candidates. Use a visited set to avoid duplicates.
> - **HOW:** Push 1. Pop min (= current ugly). Push `val*2, val*3, val*5` if not seen. Repeat n times.

> [!note]- Python Solution
> ```python
> import heapq
>
> def nth_ugly_number(n: int) -> int:
>     heap: list[int] = [1]
>     seen: set[int] = {1}
>     val = 1
>     for _ in range(n):
>         val = heapq.heappop(heap)
>         for factor in (2, 3, 5):
>             nxt = val * factor
>             if nxt not in seen:
>                 seen.add(nxt)
>                 heapq.heappush(heap, nxt)
>     return val
> ```

> [!success] Complexity
> Time O(n log n); Space O(n).

> [!tip] Alternatives
> Three-pointer DP — O(n) time and space, no set needed. Maintain indices `i2, i3, i5` into the result array; next ugly = `min(ugly[i2]*2, ugly[i3]*3, ugly[i5]*5)`. More cache-friendly and the canonical solution.

---

## See Also

[[sorting]] | [[graph-algorithms]] | [[sliding-window]] | [[two-pointers]]
### Smallest Range Covering Elements from K Lists

> [!example] Problem
> Given `k` sorted lists, find the smallest range that includes at least one number from each list.

> [!info] Approach
> - **WHY:** To keep a valid range, we must always know the current minimum and maximum among the chosen elements from each list.
> - **WHAT:** Keep one pointer per list and a min-heap of the current heads. Track the current maximum separately.
> - **HOW:** Pop the smallest value from the heap, update the best range, advance that list, and push the next value. Stop when one list is exhausted.

> [!note]- Python Solution
> ```python
> import heapq
> 
> def smallest_range(nums: list[list[int]]) -> list[int]:
>     heap = []
>     current_max = float("-inf")
>     for i, arr in enumerate(nums):
>         heapq.heappush(heap, (arr[0], i, 0))
>         current_max = max(current_max, arr[0])
>     best = [float("-inf"), float("inf")]
>     while len(heap) == len(nums):
>         current_min, list_idx, elem_idx = heapq.heappop(heap)
>         if current_max - current_min < best[1] - best[0]:
>             best = [current_min, current_max]
>         if elem_idx + 1 == len(nums[list_idx]):
>             break
>         next_val = nums[list_idx][elem_idx + 1]
>         current_max = max(current_max, next_val)
>         heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
>     return best
> ```

> [!success] Complexity
> O(N log k) time where `N` is the total number of pushed elements; O(k) space.

> [!tip] Alternatives
> Sliding a window over the flattened sorted values is harder; the heap is the canonical solution for k sorted lists.

---

## Heap Applications

### Reorganize String (LC 767)

> [!example] Problem
> Given a string, rearrange its characters so no two adjacent characters are the same. Return any valid rearrangement, or empty string if impossible.

> [!info] Approach
> - **WHY:** Greedy: always place the most frequent remaining character, as long as it is not the same as the last placed character. A max-heap efficiently gives us the most frequent character at each step.
> - **WHAT:** Use a max-heap of `(-count, char)`. At each step, pop the most frequent character. If it matches the last placed character, pop the second most frequent instead (or return "" if no second exists), then push the first back.
> - **HOW:** Alternate approach (cleaner): pop the top character, append it, push the previous character back (if count > 0). This naturally avoids placing the same character twice in a row.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import Counter
>
> def reorganize_string(s: str) -> str:
>     counts = Counter(s)
>     heap = [(-cnt, ch) for ch, cnt in counts.items()]
>     heapq.heapify(heap)
>     result = []
>     prev_cnt = 0
>     prev_ch = ''
>     while heap:
>         cnt, ch = heapq.heappop(heap)
>         result.append(ch)
>         if prev_cnt < 0:
>             heapq.heappush(heap, (prev_cnt, prev_ch))
>         prev_cnt = cnt + 1   # increment because cnt is negative
>         prev_ch = ch
>     output = ''.join(result)
>     if len(output) != len(s):
>         return ''
>     return output
> ```

> [!success] Complexity
> Time O(n log k) where k = number of distinct characters, Space O(k).

> [!tip] Alternatives
> - Interleave by frequency: sort characters by count, fill even indices first then odd indices. O(n log n) but simpler to reason about.
> - Key insight: if `max_freq > (len(s) + 1) // 2`, it is impossible — the most frequent character would have to be adjacent to itself.

---

### IPO — Maximize Capital (LC 502)

> [!example] Problem
> You have `w` initial capital. You can complete at most `k` projects. Each project has a profit and requires a minimum capital. Maximize your final capital.

> [!info] Approach
> - **WHY:** Greedy: at each step, among all projects you can currently afford, pick the one with the highest profit. A max-heap of available profits makes this O(log n) per step.
> - **WHAT:** Sort projects by required capital. Use a pointer to "unlock" projects as capital grows. At each of the `k` steps, push all newly affordable projects into a max-heap, then pop the highest profit.
> - **HOW:** Sort `(capital, profit)` pairs. Pointer `i` advances while `capital[i] <= w`. After unlocking, pop from the max-heap and add profit to `w`. Repeat `k` times.

> [!note]- Python Solution
> ```python
> import heapq
>
> def find_maximized_capital(k: int, w: int, profits: list[int], capital: list[int]) -> int:
>     projects = sorted(zip(capital, profits))
>     available = []   # max-heap (negated profits)
>     i = 0
>     for _ in range(k):
>         while i < len(projects) and projects[i][0] <= w:
>             heapq.heappush(available, -projects[i][1])
>             i += 1
>         if not available:
>             break
>         w += -heapq.heappop(available)
>     return w
> ```

> [!success] Complexity
> Time O(n log n + k log n), Space O(n).

> [!tip] Alternatives
> - No better asymptotic complexity — sorting and heap are both necessary.
> - Key insight: we never need to re-evaluate already rejected projects; once a project is unaffordable at some capital level it won't become more expensive later (projects are sorted by cost, not by time).

---

### Minimum Refueling Stops (LC 871)

> [!example] Problem
> A car starts at position 0 with `start_fuel`. Gas stations are at given positions with given amounts of fuel. Return the minimum number of refueling stops to reach the `target`, or -1 if impossible.

> [!info] Approach
> - **WHY:** Greedy: only refuel when you must (you've run out of fuel). When you do refuel, pick the largest available fuel among all stations you've already passed — that minimizes the number of stops.
> - **WHAT:** Drive as far as possible. As you pass each station, push its fuel into a max-heap. When you run out of fuel, greedily pop the largest available fuel and use it. Each pop is one stop.
> - **HOW:** Walk through stations in order. While `fuel < station.position - current_position` and heap is non-empty, pop the largest fuel and add it to `fuel` (increment stops). If still can't reach the next station, return -1.

> [!note]- Python Solution
> ```python
> import heapq
>
> def min_refuel_stops(target: int, start_fuel: int, stations: list[list[int]]) -> int:
>     heap = []   # max-heap (negated fuel amounts)
>     fuel = start_fuel
>     stops = 0
>     prev = 0
>     for position, amount in stations + [[target, 0]]:
>         fuel -= position - prev
>         while fuel < 0 and heap:
>             fuel += -heapq.heappop(heap)
>             stops += 1
>         if fuel < 0:
>             return -1
>         heapq.heappush(heap, -amount)
>         prev = position
>     return stops
> ```

> [!success] Complexity
> Time O(n log n), Space O(n).

> [!tip] Alternatives
> - DP: `dp[i]` = max distance reachable with exactly `i` stops. O(n²) — too slow for large inputs.
> - Key insight: appending `[target, 0]` to stations unifies the "can we reach the target" check into the same loop, avoiding a separate post-loop check.

---

## See Also

[[sorting]] | [[greedy]] | [[sliding-window]] | [[two-pointers]]
