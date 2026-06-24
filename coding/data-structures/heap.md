---
tags: [coding, data-structures, heap]
topic: heap
difficulty: mixed
---

# Heap Problems


## Heap Interview Checklist

- `heapq` in Python is a **min-heap**; negate keys when you need max-heap behavior.
- Use a single heap for repeated min-or-max extraction, and two heaps for median-style partitioning.
- Add **lazy deletion** when items can leave a heap before they reach the top.
- For k-way merge problems, seed the heap with one candidate from each sorted source.
- Tie-break rules matter; many heap bugs come from the secondary key, not the heap itself.


---

## Top-K Pattern

### Kth Largest Element in a Stream

> [!example] Problem
> You are part of a university admissions office and need to keep track of the kth highest test score from applicants in real-time. This helps to determine cut-off marks for interviews and admissions dynamically as new applicants submit their scores.
> You are tasked to implement a class which, for a given integer k, maintains a stream of test scores and continuously returns the kth highest test score after a new score has been submitted. More specifically, we are looking for the kth highest score in the sorted list of all scores.
> Implement the KthLargest class
> 
> **Example 1:**
> ```
> Input: ["KthLargest", "add", "add", "add", "add", "add"] [[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]
> Output: [null, 4, 5, 5, 8, 8]
> Explanation:
> KthLargest kthLargest = new KthLargest(3, [4, 5, 8, 2]); kthLargest.add(3); // return 4 kthLargest.add(5); // return 5 kthLargest.add(10); // return 5 kthLargest.add(9); // return 8 kthLargest.add(4); // return 8
> ```
> 
> **Example 2:**
> ```
> Input: ["KthLargest", "add", "add", "add", "add"] [[4, [7, 7, 7, 7, 8, 3]], [2], [10], [9], [9]]
> Output: [null, 7, 7, 7, 8]
> Explanation:
> ```
> 
> **Constraints:**
> - 0 <= nums.length <= 10^4
> - 1 <= k <= nums.length + 1
> - -10^4 <= nums[i] <= 10^4
> - -10^4 <= val <= 10^4
> - At most 10^4 calls will be made to add.

> [!info] Approach
> We need the `k`th largest at all times without sorting after every insert. A min-heap of size exactly `k` holds the top-`k` elements seen so far. The root (minimum of the heap) is always the `k`th largest. On each `add`, push the new value. If heap size exceeds `k`, pop the minimum. Root is the answer in O(1); each insert is O(log k).

> [!note]- Python Solution
> ```python
> import heapq
> >
> class KthLargest:
>     def __init__(self, k, nums):
>         self.k = k
>         self.heap: list[int] = []
>         for n in nums:
>             self.add(n)
> >
>     def add(self, val):
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
> You are given an array of integers stones where stones[i] is the weight of the ith stone.
> We are playing a game with the stones. On each turn, we choose the heaviest two stones and smash them together. Suppose the heaviest two stones have weights x and y with x <= y. The result of this smash is:
> At the end of the game, there is at most one stone left.
> Return the weight of the last remaining stone. If there are no stones left, return 0.
> 
> **Example 1:**
> ```
> Input: stones = [2,7,4,1,8,1]
> Output: 1
> Explanation: 
> We combine 7 and 8 to get 1 so the array converts to [2,4,1,1,1] then,
> we combine 2 and 4 to get 2 so the array converts to [2,1,1,1] then,
> we combine 2 and 1 to get 1 so the array converts to [1,1,1] then,
> we combine 1 and 1 to get 0 so the array converts to [1] then that's the value of the last stone.
> ```
> 
> **Example 2:**
> ```
> Input: stones = [1]
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= stones.length <= 30
> - 1 <= stones[i] <= 1000

> [!info] Approach
> We always need the two current maximums — repeated maximum extraction is a max-heap problem. A max-heap (negate for Python's min-heap) gives O(log n) each pop/push. Pop twice, push `abs(a - b)` if non-zero. Repeat until one or zero stones remain.

> [!note]- Python Solution
> ```python
> import heapq
> >
> def last_stone_weight(stones):
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
> Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k, return the k closest points to the origin (0, 0).
> The distance between two points on the X-Y plane is the Euclidean distance (i.e., √(x1 - x2)2 + (y1 - y2)2).
> You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).
> 
> **Example 1:**
> ```
> Input: points = [[1,3],[-2,2]], k = 1
> Output: [[-2,2]]
> Explanation:
> The distance between (1, 3) and the origin is sqrt(10).
> The distance between (-2, 2) and the origin is sqrt(8).
> Since sqrt(8) < sqrt(10), (-2, 2) is closer to the origin.
> We only want the closest k = 1 points from the origin, so the answer is just [[-2,2]].
> ```
> 
> **Example 2:**
> ```
> Input: points = [[3,3],[5,-1],[-2,4]], k = 2
> Output: [[3,3],[-2,4]]
> Explanation: The answer [[-2,4],[3,3]] would also be accepted.
> ```
> 
> **Constraints:**
> - 1 <= k <= points.length <= 10^4
> - -10^4 <= xi, yi <= 10^4

> [!info] Approach
> Want the `k` smallest by distance without fully sorting n points. Max-heap of size `k` on squared distance (no sqrt needed — monotone with distance). For each point compute `x²+y²`. Push `(-dist, x, y)` onto a max-heap. If size exceeds `k`, pop the farthest. Remaining heap contains the `k` closest.

> [!note]- Python Solution
> ```python
> import heapq
> >
> def k_closest(points, k):
>     heap = []
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

### Furthest Building You Can Reach

> [!example] Problem
> You are given an integer array heights representing the heights of buildings, some bricks, and some ladders.
> You start your journey from building 0 and move to the next building by possibly using bricks or ladders.
> While moving from building i to building i+1 (0-indexed),
> Return the furthest building index (0-indexed) you can reach if you use the given ladders and bricks optimally.
> 
> **Example 1:**
> ```
> Input: heights = [4,2,7,6,9,14,12], bricks = 5, ladders = 1
> Output: 4
> Explanation: Starting at building 0, you can follow these steps:
> - Go to building 1 without using ladders nor bricks since 4 >= 2.
> - Go to building 2 using 5 bricks. You must use either bricks or ladders because 2 = 6.
> - Go to building 4 using your only ladder. You must use either bricks or ladders because 6 < 9.
> It is impossible to go beyond building 4 because you do not have any more bricks or ladders.
> ```
> 
> **Example 2:**
> ```
> Input: heights = [4,12,2,7,3,18,20,3,19], bricks = 10, ladders = 2
> Output: 7
> ```
> 
> **Example 3:**
> ```
> Input: heights = [14,3,19,3], bricks = 17, ladders = 0
> Output: 3
> ```
> 
> **Constraints:**
> - 1 <= heights.length <= 10^5
> - 1 <= heights[i] <= 10^6
> - 0 <= bricks <= 10^9
> - 0 <= ladders <= heights.length

> [!info] Approach
> We want to save ladders for the largest jumps but can't see the future — greedy with reconsideration. Min-heap tracks the sizes of jumps where we used a ladder. When bricks run out, swap the smallest ladder-jump back to bricks if possible. For each upward jump, assign a ladder (push jump to heap). If ladders exhausted, pop the smallest ladder-jump, reclaim it as bricks. If bricks insufficient for the current jump, stop.

> [!note]- Python Solution
> ```python
> import heapq
> >
> def furthest_building(heights, bricks, ladders):
>     heap = []  # min-heap of ladder-used jump sizes
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
> Given an integer array nums and an integer k, return the kth largest element in the array.
> Note that it is the kth largest element in the sorted order, not the kth distinct element.
> Can you solve it without sorting?
> 
> **Example 1:**
> ```
> Input: nums = [3,2,1,5,6,4], k = 2
> Output: 5
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
> Output: 4
> ```
> 
> **Constraints:**
> - 1 <= k <= nums.length <= 10^5
> - -10^4 <= nums[i] <= 10^4

> [!info] Approach
> Sorting is O(n log n) but we only need one order-statistic. A size-k min-heap scans once. Min-heap of size exactly `k`. After processing all elements, the root is the k-th largest. For each number, push to heap. If heap exceeds size `k`, pop the minimum. Root after full pass is the answer in O(1).

> [!note]- Python Solution
> ```python
> import heapq
> >
> def find_kth_largest(nums, k):
>     heap = []
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
> Given an array of strings words and an integer k, return the k most frequent strings.
> Return the answer sorted by the frequency from highest to lowest. Sort the words with the same frequency by their lexicographical order.
> 
> **Example 1:**
> ```
> Input: words = ["i","love","leetcode","i","love","coding"], k = 2
> Output: ["i","love"]
> Explanation: "i" and "love" are the two most frequent words.
> Note that "i" comes before "love" due to a lower alphabetical order.
> ```
> 
> **Example 2:**
> ```
> Input: words = ["the","day","is","sunny","the","the","the","sunny","is","is"], k = 4
> Output: ["the","is","sunny","day"]
> Explanation: "the", "is", "sunny" and "day" are the four most frequent words, with the number of occurrence being 4, 3, 2 and 1 respectively.
> ```
> 
> **Constraints:**
> - 1 <= words.length <= 500
> - 1 <= words[i].length <= 10
> - words[i] consists of lowercase English letters.
> - k is in the range [1, The number of unique words[i]]

> [!info] Approach
> We need two ordering rules: higher frequency first, then lexicographically smaller word first on ties. Use `heapq.nsmallest(...)` with key `(-freq, word)`. This still uses a heap internally but keeps the tie-break rule correct. Count with `Counter`, then ask for the `k` best items under that custom key. This is safer than hand-rolling a size-`k` heap because naive tuple ordering is easy to get wrong for ties.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import Counter
> >
> def top_k_frequent_words(words, k):
>     count = Counter(words)
>     return [
>         word
>         for word, _ in heapq.nsmallest(
>             k, count.items(), key=lambda item: (-item[1], item[0])
>         )
>     ]
> ```

> [!success] Complexity
> Time O(n + m log k) where m = unique words; Space O(m).

> [!tip] Alternatives
> `Counter.most_common()` then sort by `(-freq, word)` — O(m log m), clean for interviews. If you want a fully explicit heap, you need a custom tie-break strategy; naive `(-freq, word)` overflow handling is easy to get wrong in Python.

---

## Scheduling / Reorganization

### Sliding Window Median

> [!example] Problem
> The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value. So the median is the mean of the two middle values.
> You are given an integer array nums and an integer k. There is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.
> Return the median array for each window in the original array. Answers within 10-5 of the actual value will be accepted.
> 
> **Example 1:**
> ```
> Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
> Output: [1.00000,-1.00000,-1.00000,3.00000,5.00000,6.00000]
> Explanation: 
> Window position                Median
> ---------------                -----
> [1  3  -1] -3  5  3  6  7        1
>  1 [3  -1  -3] 5  3  6  7       -1
>  1  3 [-1  -3  5] 3  6  7       -1
>  1  3  -1 [-3  5  3] 6  7        3
>  1  3  -1  -3 [5  3  6] 7        5
>  1  3  -1  -3  5 [3  6  7]       6
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,3,4,2,3,1,4,2], k = 3
> Output: [2.00000,3.00000,3.00000,3.00000,2.00000,3.00000,2.00000]
> ```
> 
> **Constraints:**
> - 1 <= k <= nums.length <= 10^5
> - -2^{31} <= nums[i] <= 2^{31} - 1

> [!info] Approach
> Naively recomputing the median per window is O(nk). We need to handle sliding-out elements efficiently. Two heaps + lazy deletion. Track elements that have left the window in a `Counter`. When they surface at heap tops during pop, discard them. Maintain `lo` (max-heap) and `hi` (min-heap). Slide window: add new element, mark removed element as "invalid". Rebalance heaps. When reading tops, skip invalid elements.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import defaultdict
> >
> def median_sliding_window(nums, k):
>     lo = []  # max-heap (negated), lower half
>     hi = []  # min-heap, upper half
>     invalid = defaultdict(int)
> >
>     def balance(size_lo, size_hi):
>         # Ensure lo has ceil(k/2) and hi has floor(k/2)
>         while size_lo > (k + 1) // 2:
>             heapq.heappush(hi, -heapq.heappop(lo))
>             size_lo -= 1
>             size_hi += 1
>         while size_hi > k // 2:
>             heapq.heappush(lo, -heapq.heappop(hi))
>             size_hi -= 1
>             size_lo += 1
>         return size_lo, size_hi
> >
>     def clean_top(heap, negate):
>         while heap:
>             val = -heap[0] if negate else heap[0]
>             if invalid[val] > 0:
>                 invalid[val] -= 1
>                 heapq.heappop(heap)
>             else:
>                 break
> >
>     # Seed first window
>     for x in nums[:k]:
>         heapq.heappush(lo, -x)
>     for _ in range(k // 2):
>         heapq.heappush(hi, -heapq.heappop(lo))
> >
>     def get_median():
>         clean_top(lo, True)
>         clean_top(hi, False)
>         if k % 2 == 1:
>             return float(-lo[0])
>         return (-lo[0] + hi[0]) / 2.0
> >
>     result = [get_median()]
>     size_lo, size_hi = (k + 1) // 2, k // 2
> >
>     for i in range(k, len(nums)):
>         out_val = nums[i - k]
>         in_val = nums[i]
>         invalid[out_val] += 1
>         # Adjust sizes
>         if in_val <= -lo[0]:
>             heapq.heappush(lo, -in_val)
>             size_lo += 1
>         else:
>             heapq.heappush(hi, in_val)
>             size_hi += 1
>         if out_val <= -lo[0]:
>             size_lo -= 1
>         else:
>             size_hi -= 1
>         size_lo, size_hi = balance(size_lo, size_hi)
>         clean_top(lo, True)
>         clean_top(hi, False)
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
> Suppose LeetCode will start its IPO soon. In order to sell a good price of its shares to Venture Capital, LeetCode would like to work on some projects to increase its capital before the IPO. Since it has limited resources, it can only finish at most k distinct projects before the IPO. Help LeetCode design the best way to maximize its total capital after finishing at most k distinct projects.
> You are given n projects where the ith project has a pure profit profits[i] and a minimum capital of capital[i] is needed to start it.
> Initially, you have w capital. When you finish a project, you will obtain its pure profit and the profit will be added to your total capital.
> Pick a list of at most k distinct projects from given projects to maximize your final capital, and return the final maximized capital.
> The answer is guaranteed to fit in a 32-bit signed integer.
> 
> **Example 1:**
> ```
> Input: k = 2, w = 0, profits = [1,2,3], capital = [0,1,1]
> Output: 4
> Explanation: Since your initial capital is 0, you can only start the project indexed 0.
> After finishing it you will obtain profit 1 and your capital becomes 1.
> With capital 1, you can either start the project indexed 1 or the project indexed 2.
> Since you can choose at most 2 projects, you need to finish the project indexed 2 to get the maximum capital.
> Therefore, output the final maximized capital, which is 0 + 1 + 3 = 4.
> ```
> 
> **Example 2:**
> ```
> Input: k = 3, w = 0, profits = [1,2,3], capital = [0,1,2]
> Output: 6
> ```
> 
> **Constraints:**
> - 1 <= k <= 10^5
> - 0 <= w <= 10^9
> - n == profits.length
> - n == capital.length
> - 1 <= n <= 10^5
> - 0 <= profits[i] <= 10^4
> - 0 <= capital[i] <= 10^9

> [!info] Approach
> Greedy — always take the most profitable project currently affordable. Projects unlock as capital grows. Sort projects by required capital. Sweep a pointer to unlock affordable projects into a max-heap of profits. Each round, pop the best available profit. Sort `zip(capital, profits)` by capital. Use a pointer `i` advancing when `projects[i][0] <= w`. Max-heap holds unlocked profits (negated). Repeat `k` times.

> [!note]- Python Solution
> ```python
> import heapq
> >
> def find_maximized_capital(k, w, profits, capital):
>     projects = sorted(zip(capital, profits))
>     available = []  # max-heap (negated profits)
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
> You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
> Merge all the linked-lists into one sorted linked-list and return it.
> 
> **Example 1:**
> ```
> Input: lists = [[1,4,5],[1,3,4],[2,6]]
> Output: [1,1,2,3,4,4,5,6]
> Explanation: The linked-lists are:
> [
>   1->4->5,
>   1->3->4,
>   2->6
> ]
> merging them into one sorted linked list:
> 1->1->2->3->4->4->5->6
> ```
> 
> **Example 2:**
> ```
> Input: lists = []
> Output: []
> ```
> 
> **Example 3:**
> ```
> Input: lists = [[]]
> Output: []
> ```
> 
> **Constraints:**
> - k == lists.length
> - 0 <= k <= 10^4
> - 0 <= lists[i].length <= 500
> - -10^4 <= lists[i][j] <= 10^4
> - lists[i] is sorted in ascending order.
> - The sum of lists[i].length will not exceed 10^4.

> [!info] Approach
> Naive pairwise merge is O(nk). We want O(n log k) by always extracting the global minimum across k list heads. Min-heap of size k holds one `(value, list_id, node)` tuple per list. Pop gives the global min; push the next node from that list. Seed heap with head of each non-null list. Use `list_id` as tie-breaker to avoid comparing `ListNode` objects (not comparable in Python).

> [!note]- Python Solution
> ```python
> import heapq
> from typing import Optional
> >
> class ListNode:
>     def __init__(self, val=0, next=None):
>         self.val = val
>         self.next = next
> >
> def merge_k_lists(lists):
>     heap = []
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
> You are given two integer arrays nums1 and nums2 sorted in non-decreasing order and an integer k.
> Define a pair (u, v) which consists of one element from the first array and one element from the second array.
> Return the k pairs (u1, v1), (u2, v2), ..., (uk, vk) with the smallest sums.
> 
> **Example 1:**
> ```
> Input: nums1 = [1,7,11], nums2 = [2,4,6], k = 3
> Output: [[1,2],[1,4],[1,6]]
> Explanation: The first 3 pairs are returned from the sequence: [1,2],[1,4],[1,6],[7,2],[7,4],[11,2],[7,6],[11,4],[11,6]
> ```
> 
> **Example 2:**
> ```
> Input: nums1 = [1,1,2], nums2 = [1,2,3], k = 2
> Output: [[1,1],[1,1]]
> Explanation: The first 2 pairs are returned from the sequence: [1,1],[1,1],[1,2],[2,1],[1,2],[2,2],[1,3],[1,3],[2,3]
> ```
> 
> **Constraints:**
> - 1 <= nums1.length, nums2.length <= 10^5
> - -10^9 <= nums1[i], nums2[i] <= 10^9
> - nums1 and nums2 both are sorted in non-decreasing order.
> - 1 <= k <= 10^4
> - k <= nums1.length * nums2.length

> [!info] Approach
> There are `m*n` possible pairs — we need the k smallest without enumerating all. Treat this as a k-way merge: each row `i` of the implicit `m x n` sum matrix is sorted (since `nums2` is sorted). Seed heap with `(nums1[i] + nums2[0], i, 0)` for each `i`. Pop smallest `(sum, i, j)`, record pair. Push `(nums1[i] + nums2[j+1], i, j+1)` if `j+1 < len(nums2)`. Stop after k pops.

> [!note]- Python Solution
> ```python
> import heapq
> >
> def k_smallest_pairs(nums1, nums2, k):
>     if not nums1 or not nums2:
>         return []
>     heap = []
>     for i in range(min(len(nums1), k)):
>         heapq.heappush(heap, (nums1[i] + nums2[0], i, 0))
>     result = []
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
> Given an n x n matrix where each of the rows and columns is sorted in ascending order, return the kth smallest element in the matrix.
> Note that it is the kth smallest element in the sorted order, not the kth distinct element.
> You must find a solution with a memory complexity better than O(n2).
> 
> **Example 1:**
> ```
> Input: matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8
> Output: 13
> Explanation: The elements in the matrix are [1,5,9,10,11,12,13,13,15], and the 8th smallest number is 13
> ```
> 
> **Example 2:**
> ```
> Input: matrix = [[-5]], k = 1
> Output: -5
> ```
> 
> **Constraints:**
> - n == matrix.length == matrix[i].length
> - 1 <= n <= 300
> - -10^9 <= matrix[i][j] <= 10^9
> - All the rows and columns of matrix are guaranteed to be sorted in non-decreasing order.
> - 1 <= k <= n2

> [!info] Approach
> Each row is a sorted list — this is K-way merge of n sorted arrays. Min-heap seeded with the first element of each row. Pop `k` times; each pop advances the column in that row. Push `(matrix[i][0], i, 0)` for all `i`. Pop k-1 times advancing `(matrix[i][j+1], i, j+1)`. The k-th pop is the answer.

> [!note]- Python Solution
> ```python
> import heapq
> >
> def kth_smallest(matrix, k):
>     n = len(matrix)
>     heap = [(matrix[i][0], i, 0) for i in range(n)]
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
> You have k lists of sorted integers in non-decreasing order. Find the smallest range that includes at least one number from each of the k lists.
> We define the range [a, b] is smaller than range [c, d] if b - a < d - c or a < c if b - a == d - c.
> 
> **Example 1:**
> ```
> Input: nums = [[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]
> Output: [20,24]
> Explanation: 
> List 1: [4, 10, 15, 24,26], 24 is in range [20,24].
> List 2: [0, 9, 12, 20], 20 is in range [20,24].
> List 3: [5, 18, 22, 30], 22 is in range [20,24].
> ```
> 
> **Example 2:**
> ```
> Input: nums = [[1,2,3],[1,2,3],[1,2,3]]
> Output: [1,1]
> ```
> 
> **Constraints:**
> - nums.length == k
> - 1 <= k <= 3500
> - 1 <= nums[i].length <= 50
> - -10^5 <= nums[i][j] <= 10^5
> - nums[i] is sorted in non-decreasing order.

> [!info] Approach
> We need a window containing one element per list. Sliding window on a sorted merged sequence won't track list coverage. K-way merge with a global max tracker. The current range is `[heap_min, current_max]`. Advance the minimum (pop from heap, push next from same list) to shrink the range. Seed heap with `(lists[i][0], i, 0)`. Track `cur_max = max of all initial first elements`. Each pop gives a new candidate min; update range if `cur_max - min` is smaller. Stop when any list is exhausted.

> [!note]- Python Solution
> ```python
> import heapq
> >
> def smallest_range(nums):
>     heap = []
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
> This is the general form of "Kth Smallest in a Sorted Matrix" — M sorted sequences, find the k-th minimum globally. Min-heap seeded with the first element of each array. Pop once per step, advance that array's pointer. After k pops, the last popped is the answer. Push `(arrays[i][0], i, 0)` for all i. Pop and push `(arrays[i][j+1], i, j+1)` until k pops done.

> [!note]- Python Solution
> ```python
> import heapq
> >
> def kth_smallest_m_arrays(arrays, k):
>     heap = []
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
> Classic interval overlap problem — need to track which jobs are active at each moment. Sort by start time. Use a min-heap keyed by end time to track active jobs. At each new job's start, evict all jobs that have ended. Sort jobs by start. For each job, pop from heap all jobs with `end <= job.start`. Push current job's end time and load. Track running sum of active loads and record maximum.

> [!note]- Python Solution
> ```python
> import heapq
> >
> def find_max_cpu_load(jobs):
>     jobs.sort(key=lambda x: x[0])
>     heap = []  # (end_time, load)
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

### Path with Minimum Effort

> [!example] Problem
> You are a hiker preparing for an upcoming hike. You are given heights, a 2D array of size rows x columns, where heights[row][col] represents the height of cell (row, col). You are situated in the top-left cell, (0, 0), and you hope to travel to the bottom-right cell, (rows-1, columns-1) (i.e., 0-indexed). You can move up, down, left, or right, and you wish to find a route that requires the minimum effort.
> A route's effort is the maximum absolute difference in heights between two consecutive cells of the route.
> Return the minimum effort required to travel from the top-left cell to the bottom-right cell.
> 
> **Example 1:**
> ```
> Input: heights = [[1,2,2],[3,8,2],[5,3,5]]
> Output: 2
> Explanation: The route of [1,3,5,3,5] has a maximum absolute difference of 2 in consecutive cells.
> This is better than the route of [1,2,2,2,5], where the maximum absolute difference is 3.
> ```
> 
> **Example 2:**
> ```
> Input: heights = [[1,2,3],[3,8,4],[5,3,5]]
> Output: 1
> Explanation: The route of [1,2,3,4,5] has a maximum absolute difference of 1 in consecutive cells, which is better than route [1,3,5,3,5].
> ```
> 
> **Example 3:**
> ```
> Input: heights = [[1,2,1,1,1],[1,2,1,2,1],[1,2,1,2,1],[1,2,1,2,1],[1,1,1,2,1]]
> Output: 0
> Explanation: This route does not require any effort.
> ```
> 
> **Constraints:**
> - rows == heights.length
> - columns == heights[i].length
> - 1 <= rows, columns <= 100
> - 1 <= heights[i][j] <= 10^6

> [!info] Approach
> Minimizing the maximum edge weight along a path — modified Dijkstra where "dist" is the bottleneck edge. Min-heap of `(effort, row, col)`. `effort` = max diff seen so far on the current path. Relax: new effort = `max(current_effort, abs(neighbor_height - current_height))`. Push `(0, 0, 0)`. For each pop, update neighbors with `max(effort, abs diff)`. Skip if already visited at a better effort.

> [!note]- Python Solution
> ```python
> import heapq
> >
> def minimum_effort_path(heights):
>     rows, cols = len(heights), len(heights[0])
>     dist = [[float('inf')] * cols for _ in range(rows)]
>     dist[0][0] = 0
>     heap = [(0, 0, 0)]
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

### Design Twitter

> [!example] Problem
> Design a simplified version of Twitter where users can post tweets, follow/unfollow another user, and is able to see the 10 most recent tweets in the user's news feed.
> Implement the Twitter class
> 
> **Example 1:**
> ```
> Input
> ["Twitter", "postTweet", "getNewsFeed", "follow", "postTweet", "getNewsFeed", "unfollow", "getNewsFeed"]
> [[], [1, 5], [1], [1, 2], [2, 6], [1], [1, 2], [1]]
> Output
> [null, null, [5], null, null, [6, 5], null, [5]]
> 
> Explanation
> Twitter twitter = new Twitter();
> twitter.postTweet(1, 5); // User 1 posts a new tweet (id = 5).
> twitter.getNewsFeed(1);  // User 1's news feed should return a list with 1 tweet id -> [5]. return [5]
> twitter.follow(1, 2);    // User 1 follows user 2.
> twitter.postTweet(2, 6); // User 2 posts a new tweet (id = 6).
> twitter.getNewsFeed(1);  // User 1's news feed should return a list with 2 tweet ids -> [6, 5]. Tweet id 6 should precede tweet id 5 because it is posted after tweet id 5.
> twitter.unfollow(1, 2);  // User 1 unfollows user 2.
> twitter.getNewsFeed(1);  // User 1's news feed should return a list with 1 tweet id -> [5], since user 1 is no longer following user 2.
> ```
> 
> **Constraints:**
> - 1 <= userId, followerId, followeeId <= 500
> - 0 <= tweetId <= 10^4
> - All the tweets have unique IDs.
> - At most 3 * 10^4 calls will be made to postTweet, getNewsFeed, follow, and unfollow.
> - A user cannot follow himself.

> [!info] Approach
> News feed merges multiple sorted tweet streams (one per followee) — this is K-way merge on recency. Store each user's tweets as a list (ordered by insertion = by time using a global counter). `get_news_feed` collects all candidate tweet lists and uses a max-heap on timestamp to extract the 10 most recent. Global `time` counter increments with each tweet. Each user has a list of `(time, tweetId)`. For feed: seed heap with latest tweet from each followee+self. Pop max; push that user's next tweet. Collect 10.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import defaultdict
> >
> class Twitter:
>     def __init__(self):
>         self._time = 0
>         self._tweets: dict[int, list[tuple[int, int]]] = defaultdict(list)
>         self._follows: dict[int, set[int]] = defaultdict(set)
> >
>     def post_tweet(self, userId, tweetId):
>         self._tweets[userId].append((self._time, tweetId))
>         self._time += 1
> >
>     def get_news_feed(self, userId):
>         heap = []  # (-time, tweetId, userId, idx)
>         users = self._follows[userId] | {userId}
>         for uid in users:
>             tweets = self._tweets[uid]
>             if tweets:
>                 idx = len(tweets) - 1
>                 t, tid = tweets[idx]
>                 heapq.heappush(heap, (-t, tid, uid, idx - 1))
>         result = []
>         while heap and len(result) < 10:
>             _, tid, uid, idx = heapq.heappop(heap)
>             result.append(tid)
>             if idx >= 0:
>                 t, next_tid = self._tweets[uid][idx]
>                 heapq.heappush(heap, (-t, next_tid, uid, idx - 1))
>         return result
> >
>     def follow(self, followerId, followeeId):
>         self._follows[followerId].add(followeeId)
> >
>     def unfollow(self, followerId, followeeId):
>         self._follows[followerId].discard(followeeId)
> ```

> [!success] Complexity
> `post_tweet` O(1); `get_news_feed` O(F log F + 10 log F) where F = followees; `follow/unfollow` O(1).

> [!tip] Alternatives
> Pre-materialized feeds with a write-fan-out — O(F) on each post, O(1) read; used in real systems for read-heavy workloads (Twitter's "fanout on write").

---

### Ugly Number II

> [!example] Problem
> An ugly number is a positive integer whose prime factors are limited to 2, 3, and 5.
> Given an integer n, return the nth ugly number.
> 
> **Example 1:**
> ```
> Input: n = 10
> Output: 12
> Explanation: [1, 2, 3, 4, 5, 6, 8, 9, 10, 12] is the sequence of the first 10 ugly numbers.
> ```
> 
> **Example 2:**
> ```
> Input: n = 1
> Output: 1
> Explanation: 1 has no prime factors, therefore all of its prime factors are limited to 2, 3, and 5.
> ```
> 
> **Constraints:**
> - 1 <= n <= 1690

> [!info] Approach
> We need to generate ugly numbers in order without iterating all integers. Min-heap seeded with `{1}`. Each pop gives the next ugly number; multiply by 2, 3, 5 to generate candidates. Use a visited set to avoid duplicates. Push 1. Pop min (= current ugly). Push `val*2, val*3, val*5` if not seen. Repeat n times.

> [!note]- Python Solution
> ```python
> import heapq
> >
> def nth_ugly_number(n):
>     heap = [1]
>     seen = {1}
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
> You have k lists of sorted integers in non-decreasing order. Find the smallest range that includes at least one number from each of the k lists.
> We define the range [a, b] is smaller than range [c, d] if b - a < d - c or a < c if b - a == d - c.
> 
> **Example 1:**
> ```
> Input: nums = [[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]
> Output: [20,24]
> Explanation: 
> List 1: [4, 10, 15, 24,26], 24 is in range [20,24].
> List 2: [0, 9, 12, 20], 20 is in range [20,24].
> List 3: [5, 18, 22, 30], 22 is in range [20,24].
> ```
> 
> **Example 2:**
> ```
> Input: nums = [[1,2,3],[1,2,3],[1,2,3]]
> Output: [1,1]
> ```
> 
> **Constraints:**
> - nums.length == k
> - 1 <= k <= 3500
> - 1 <= nums[i].length <= 50
> - -10^5 <= nums[i][j] <= 10^5
> - nums[i] is sorted in non-decreasing order.

> [!info] Approach
> To keep a valid range, we must always know the current minimum and maximum among the chosen elements from each list. Keep one pointer per list and a min-heap of the current heads. Track the current maximum separately. Pop the smallest value from the heap, update the best range, advance that list, and push the next value. Stop when one list is exhausted.

> [!note]- Python Solution
> ```python
> import heapq
> 
> def smallest_range(nums):
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
> Given a string s, rearrange the characters of s so that any two adjacent characters are not the same.
> Return any possible rearrangement of s or return "" if not possible.
> 
> **Example 1:**
> ```
> Input: s = "aab"
> Output: "aba"
> ```
> 
> **Example 2:**
> ```
> Input: s = "aaab"
> Output: ""
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 500
> - s consists of lowercase English letters.

> [!info] Approach
> Greedy: always place the most frequent remaining character, as long as it is not the same as the last placed character. A max-heap efficiently gives us the most frequent character at each step. Use a max-heap of `(-count, char)`. At each step, pop the most frequent character. If it matches the last placed character, pop the second most frequent instead (or return "" if no second exists), then push the first back. Alternate approach (cleaner): pop the top character, append it, push the previous character back (if count > 0). This naturally avoids placing the same character twice in a row.

> [!note]- Python Solution
> ```python
> import heapq
> from collections import Counter
> >
> def reorganize_string(s):
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

### Minimum Refueling Stops (LC 871)

> [!example] Problem
> A car travels from a starting position to a destination which is target miles east of the starting position.
> There are gas stations along the way. The gas stations are represented as an array stations where stations[i] = [positioni, fueli] indicates that the ith gas station is positioni miles east of the starting position and has fueli liters of gas.
> The car starts with an infinite tank of gas, which initially has startFuel liters of fuel in it. It uses one liter of gas per one mile that it drives. When the car reaches a gas station, it may stop and refuel, transferring all the gas from the station into the car.
> Return the minimum number of refueling stops the car must make in order to reach its destination. If it cannot reach the destination, return -1.
> Note that if the car reaches a gas station with 0 fuel left, the car can still refuel there. If the car reaches the destination with 0 fuel left, it is still considered to have arrived.
> 
> **Example 1:**
> ```
> Input: target = 1, startFuel = 1, stations = []
> Output: 0
> Explanation: We can reach the target without refueling.
> ```
> 
> **Example 2:**
> ```
> Input: target = 100, startFuel = 1, stations = [[10,100]]
> Output: -1
> Explanation: We can not reach the target (or even the first gas station).
> ```
> 
> **Example 3:**
> ```
> Input: target = 100, startFuel = 10, stations = [[10,60],[20,30],[30,30],[60,40]]
> Output: 2
> Explanation: We start with 10 liters of fuel.
> We drive to position 10, expending 10 liters of fuel.  We refuel from 0 liters to 60 liters of gas.
> Then, we drive from position 10 to position 60 (expending 50 liters of fuel),
> and refuel from 10 liters to 50 liters of gas.  We then drive to and reach the target.
> We made 2 refueling stops along the way, so we return 2.
> ```
> 
> **Constraints:**
> - 1 <= target, startFuel <= 10^9
> - 0 <= stations.length <= 500
> - 1 <= positioni < positioni+1 < target
> - 1 <= fueli < 10^9

> [!info] Approach
> Greedy: only refuel when you must (you've run out of fuel). When you do refuel, pick the largest available fuel among all stations you've already passed — that minimizes the number of stops. Drive as far as possible. As you pass each station, push its fuel into a max-heap. When you run out of fuel, greedily pop the largest available fuel and use it. Each pop is one stop. Walk through stations in order. While `fuel < station.position - current_position` and heap is non-empty, pop the largest fuel and add it to `fuel` (increment stops). If still can't reach the next station, return -1.

> [!note]- Python Solution
> ```python
> import heapq
> >
> def min_refuel_stops(target, start_fuel, stations):
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
