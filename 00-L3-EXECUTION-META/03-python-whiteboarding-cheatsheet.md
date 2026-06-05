# Python Whiteboarding Cheatsheet `⚡ T1`

> [!warning] No Autocomplete at Google
> Google uses a plain-text editor for coding interviews. You cannot rely on IDE suggestions. You must memorize these core Python standard library functions.

## 1. Heaps (`heapq`)
Python only has a **min-heap** by default. To simulate a max-heap, multiply values by `-1`.
```python
import heapq

heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 2)
min_val = heapq.heappop(heap)  # Returns 2

# Max-heap simulation
max_heap = []
heapq.heappush(max_heap, -5)
max_val = -heapq.heappop(max_heap) # Returns 5

# Heapify an existing array in O(N) time
arr = [5, 7, 1, 3]
heapq.heapify(arr)
```

## 2. Queues & Deques (`collections.deque`)
Never use `list.pop(0)` for a queue! It is $O(N)$. Always use `deque`.
```python
from collections import deque

q = deque([1, 2, 3])
q.append(4)       # O(1) push right
q.appendleft(0)   # O(1) push left

right = q.pop()   # O(1) pop right (returns 4)
left = q.popleft()# O(1) pop left (returns 0)
```

## 3. Hash Maps & Counters (`collections`)
```python
from collections import Counter, defaultdict

# Defaultdict prevents KeyError
adj_list = defaultdict(list)
adj_list['A'].append('B') # Automatically creates empty list if 'A' not present

# Counter tallies frequencies
freq = Counter("banana") # Counter({'a': 3, 'n': 2, 'b': 1})
most_common = freq.most_common(1) # [('a', 3)]
```

## 4. Sorting Tricks
```python
# Sort a list of tuples by the second element, then by the first
arr = [(1, 5), (2, 3), (1, 2)]
arr.sort(key=lambda x: (x[1], x[0]))

# Sort a dictionary by its values
d = {'a': 3, 'b': 1, 'c': 2}
sorted_items = sorted(d.items(), key=lambda item: item[1]) # [('b', 1), ('c', 2), ('a', 3)]
```

## 5. Binary Search (`bisect`)
```python
import bisect

arr = [1, 3, 3, 3, 5]
# Find insertion point to maintain sorted order
left_idx = bisect.bisect_left(arr, 3)  # Returns 1 (first 3)
right_idx = bisect.bisect_right(arr, 3) # Returns 4 (after last 3)
```

## 6. Infinity and Beyond
```python
# Initialize min/max trackers
max_val = float('-inf')
min_val = float('inf')
```
