# Problem Details (Descriptions + Pseudocode) — Google SDE-2

This file expands every coding question mentioned in this folder into:
- a short **problem description**
- **pseudocode** for a standard interview solution

Notes:
- Titles are canonical; use any platform (LeetCode/EPI/etc.) to find the exact statement.
- Pseudocode uses generic helpers like `HashMap`, `Deque`, `Heap`, `DSU`.

---

## Arrays / Prefix Sums / Hashing

<a id="two-sum"></a>
### Two Sum
**Problem:** Given an array and a target, return indices of two numbers that add to the target.  
**Pseudocode:**
```
map = empty HashMap(value -> index)
for i in [0..n-1]:
  need = target - nums[i]
  if need in map: return [map[need], i]
  map[nums[i]] = i
return []
```
**Important points:**
- Check-before-store to avoid using the same element twice (when target = 2*x).
- Time O(n), space O(n) with `value -> index` hash map.
- If multiple answers exist, the first found is fine unless asked otherwise.


<a id="group-anagrams"></a>
### Group Anagrams
**Problem:** Group strings that are anagrams of each other.  
**Pseudocode:**
```
groups = HashMap(key -> list)
for word in words:
  key = sort(word)          // or 26-count tuple
  groups[key].append(word)
return groups.values()
```
**Important points:** For arbitrary Unicode, sorting is simplest; for only lowercase letters, 26-count tuple is O(k).

<a id="longest-consecutive-sequence"></a>
### Longest Consecutive Sequence
**Problem:** Find length of the longest consecutive integer sequence (O(n) expected).  
**Pseudocode:**
```
set = HashSet(nums)
best = 0
for x in set:
  if (x-1) not in set:          // start of sequence
    y = x
    while y in set: y++
    best = max(best, y - x)
return best
```
**Important points:** The `if x-1 not in set` guard makes total work linear (each number is extended once).

<a id="subarray-sum-equals-k"></a>
### Subarray Sum Equals K
**Problem:** Count subarrays with sum exactly `k` (numbers may be negative).  
**Pseudocode:**
```
prefix = 0
countByPrefix = HashMap()
countByPrefix[0] = 1
ans = 0
for x in nums:
  prefix += x
  ans += countByPrefix.get(prefix - k, 0)
  countByPrefix[prefix] = countByPrefix.get(prefix, 0) + 1
return ans
```
**Important points:**
- Works with negative numbers because it counts prefix-sum frequencies (not a sliding window).
- Seed `countByPrefix[0] = 1` to count subarrays starting at index 0.
- Use 64-bit for prefix sums if values can be large.


<a id="product-of-array-except-self"></a>
### Product of Array Except Self
**Problem:** Return array where `out[i]` is product of all nums except nums[i], without division.  
**Pseudocode:**
```
out = array of 1s length n
left = 1
for i in [0..n-1]:
  out[i] = left
  left *= nums[i]
right = 1
for i in [n-1..0]:
  out[i] *= right
  right *= nums[i]
return out
```
**Important points:**
- Two passes: prefix products then suffix products; avoids division and handles zeros naturally.
- Extra space O(1) excluding output array.
- Watch overflow in languages with 32-bit ints if constraints are large.


<a id="maximum-subarray-kadane"></a>
### Maximum Subarray (Kadane)
**Problem:** Find max sum over all non-empty contiguous subarrays.  
**Pseudocode:**
```
best = nums[0]
cur = nums[0]
for i in [1..n-1]:
  cur = max(nums[i], cur + nums[i])
  best = max(best, cur)
return best
```
**Important points:**
- Define invariant: `cur` is best sum of a subarray ending at i; reset when extending hurts.
- Must handle all-negative arrays (initialize to nums[0], not 0).
- Time O(n), space O(1).


<a id="maximum-subarray"></a>
### Maximum Subarray
**Problem:** Alias for “Maximum Subarray (Kadane)”.  
**Pseudocode:** Use Kadane’s recurrence above.
**Important points:**
- Alias for Kadane; same invariants and edge cases (all-negative).

<a id="merge-intervals"></a>
### Merge Intervals
**Problem:** Given intervals, merge all overlapping intervals.  
**Pseudocode:**
```
sort intervals by start
merged = []
for (s,e) in intervals:
  if merged empty or s > merged.last.end:
    append (s,e)
  else:
    merged.last.end = max(merged.last.end, e)
return merged
```
**Important points:**
- Sort by start; merge by extending the last interval’s end.
- Be explicit about overlap rule (typically `next.start <= cur.end`).
- Time O(n log n) for sorting; scan is linear.


<a id="insert-interval"></a>
### Insert Interval
**Problem:** Insert a new interval into sorted non-overlapping intervals and merge if needed.  
**Pseudocode:**
```
res = []
i = 0
while i < n and intervals[i].end < new.start:
  res.append(intervals[i]); i++
while i < n and intervals[i].start <= new.end:
  new.start = min(new.start, intervals[i].start)
  new.end = max(new.end, intervals[i].end)
  i++
res.append(new)
while i < n:
  res.append(intervals[i]); i++
return res
```
**Important points:**
- Three phases: add left (non-overlapping), merge overlaps, add right.
- In-place merge by expanding `newInterval` as long as it overlaps.
- Time O(n), space O(n) for output.


<a id="next-permutation"></a>
### Next Permutation
**Problem:** Rearrange numbers into the next lexicographically greater permutation (in-place).  
**Pseudocode:**
```
i = n-2
while i >= 0 and nums[i] >= nums[i+1]: i--
if i < 0:
  reverse nums; return
j = n-1
while nums[j] <= nums[i]: j--
swap(nums[i], nums[j])
reverse nums[i+1..n-1]
```
**Important points:**
- Pivot is the first index from the right where `a[i] < a[i+1]`.
- Swap pivot with the smallest number greater than it in the suffix (scan from right).
- Reverse suffix to get the minimal next permutation.


<a id="majority-element"></a>
### Majority Element
**Problem:** Find element that appears more than n/2 times (assumed exists).  
**Pseudocode:**
```
candidate = None
count = 0
for x in nums:
  if count == 0: candidate = x
  count += 1 if x == candidate else -1
return candidate
```
**Important points:**
- Boyer–Moore finds a candidate in O(n) / O(1); relies on a guaranteed majority.
- If majority is not guaranteed, add a second pass to verify the candidate.


---

## Design-Heavy / Data Structures (Still Asked in Coding Rounds)

<a id="lru-cache"></a>
### LRU Cache
**Problem:** Design an LRU cache with O(1) get/put.  
**Key idea:** `HashMap(key -> node)` + doubly linked list (MRU near head, LRU near tail).  
**Pseudocode:**
```
map = HashMap(key -> node)
DLL with head/tail sentinels

get(key):
  if key not in map: return -1
  node = map[key]
  dll.remove(node); dll.add_front(node)
  return node.value

put(key, value):
  if capacity == 0: return
  if key in map:
    node = map[key]
    node.value = value
    dll.remove(node); dll.add_front(node)
    return
  node = new Node(key, value)
  map[key] = node
  dll.add_front(node)
  if map.size > capacity:
    lru = dll.remove_back()      // node before tail
    delete map[lru.key]
```
**Important points:** Use sentinels to simplify; updating an existing key must also move it to MRU.

<a id="lfu-cache"></a>
### LFU Cache
**Problem:** Design an LFU cache with O(1) get/put (evict least frequently used; tie-break by LRU).  
**Key idea:** `key -> (value, freq, node)` + `freq -> DLL of nodes`, track `minFreq`.  
**Pseudocode:**
```
keyToNode = HashMap()
freqToDLL = HashMap(freq -> doubly linked list of nodes, MRU at front)
minFreq = 0

touch(node):                  // increment frequency
  old = node.freq
  freqToDLL[old].remove(node)
  if old == minFreq and freqToDLL[old] is empty:
    minFreq++
  node.freq++
  freqToDLL[node.freq].add_front(node)

get(key):
  if key not in keyToNode: return -1
  node = keyToNode[key]
  touch(node)
  return node.value

put(key, value):
  if capacity == 0: return
  if key in keyToNode:
    node = keyToNode[key]
    node.value = value
    touch(node)
    return
  if keyToNode.size == capacity:
    victim = freqToDLL[minFreq].remove_back()   // LRU in lowest freq
    delete keyToNode[victim.key]
  node = new Node(key, value, freq=1)
  keyToNode[key] = node
  freqToDLL[1].add_front(node)
  minFreq = 1
```
**Important points:** `minFreq` maintenance is the common bug; eviction is from the back of the `minFreq` DLL.

<a id="rate-limiter"></a>
### Rate Limiter
**Problem:** Implement a basic rate limiter (commonly token bucket or sliding window counter).  
**Pseudocode (token bucket):**
```
capacity = N
refillRate = R tokens per second
tokens = N
last = now()

allow():
  nowT = now()
  tokens = min(capacity, tokens + (nowT-last)*refillRate)
  last = nowT
  if tokens >= 1:
    tokens -= 1
    return true
  return false
```
**Important points:** Token bucket allows bursts up to capacity; be careful with time units and floating vs integer tokens.

---

## Two Pointers

<a id="3sum"></a>
### 3Sum
**Problem:** Find all unique triplets that sum to 0.  
**Pseudocode:**
```
sort nums
ans = []
for i in [0..n-1]:
  if i>0 and nums[i]==nums[i-1]: continue
  l = i+1; r = n-1
  while l < r:
    s = nums[i] + nums[l] + nums[r]
    if s == 0:
      add triplet
      l++; r--
      while l<r and nums[l]==nums[l-1]: l++
      while l<r and nums[r]==nums[r+1]: r--
    elif s < 0: l++
    else: r--
return ans
```
**Important points:**
- Sort then fix i; use two pointers on the suffix; skip duplicates for i/left/right.
- Early break when `nums[i] > 0` (after sorting) if target is 0.
- Time O(n^2); space O(1) extra (excluding output).


<a id="container-with-most-water"></a>
### Container With Most Water
**Problem:** Given heights, pick two lines maximizing area.  
**Pseudocode:**
```
l=0; r=n-1; best=0
while l<r:
  best = max(best, min(h[l],h[r])*(r-l))
  if h[l] < h[r]: l++
  else: r--
return best
```
**Important points:**
- Two pointers; move the shorter side because area is limited by min(height[l], height[r]).
- Proof idea: moving the taller side cannot increase the limiting height.
- Time O(n), space O(1).


<a id="trapping-rain-water"></a>
### Trapping Rain Water
**Problem:** Given heights, compute trapped water.  
**Pseudocode (two pointers):**
```
l=0; r=n-1
leftMax=0; rightMax=0; water=0
while l<r:
  if h[l] <= h[r]:
    leftMax = max(leftMax, h[l])
    water += leftMax - h[l]
    l++
  else:
    rightMax = max(rightMax, h[r])
    water += rightMax - h[r]
    r--
return water
```
**Important points:**
- Two-pointer variant maintains `leftMax`/`rightMax`; fill based on the smaller bound.
- Alternative: monotonic stack for ‘next greater’ boundaries.
- Time O(n), space O(1) (two-pointer) or O(n) (stack).

<a id="remove-duplicates-from-sorted-array"></a>
### Remove Duplicates from Sorted Array
**Problem:** In-place remove duplicates so each element appears once; return new length.  
**Pseudocode:**
```
write = 0
for read in [0..n-1]:
  if read==0 or nums[read] != nums[read-1]:
    nums[write] = nums[read]
    write++
return write
```
**Important points:**
- Slow/fast pointers; slow tracks next write position for unique values.
- Works because input is sorted; for unsorted you need a set/map.
- Return new length; elements beyond it are irrelevant.


<a id="sort-colors-dutch-flag"></a>
### Sort Colors (Dutch Flag)
**Problem:** Sort 0/1/2 in-place.  
**Pseudocode:**
```
low=0; mid=0; high=n-1
while mid <= high:
  if nums[mid]==0: swap(nums[low],nums[mid]); low++; mid++
  elif nums[mid]==1: mid++
  else: swap(nums[mid],nums[high]); high--
```
**Important points:**
- `low..mid-1` are 0s, `mid..high` unknown, `high+1..end` are 2s.
- When swapping with `high`, do not increment `mid` (needs re-check).
- One pass O(n), in-place O(1).


<a id="sort-colors"></a>
### Sort Colors
**Problem:** Alias for “Sort Colors (Dutch Flag)”.  
**Pseudocode:** Use the Dutch National Flag pointers above.
**Important points:**
- Alias for Dutch National Flag; same invariants about `low/mid/high`.

---

## Sliding Window

<a id="longest-substring-without-repeating-characters"></a>
### Longest Substring Without Repeating Characters
**Problem:** Longest substring with all unique chars.  
**Pseudocode:**
```
lastIndex = HashMap(char -> last position)
left = 0; best = 0
for right in [0..n-1]:
  c = s[right]
  if c in lastIndex and lastIndex[c] >= left:
    left = lastIndex[c] + 1
  lastIndex[c] = right
  best = max(best, right-left+1)
return best
```
**Important points:**
- Maintain a window with last-seen indices; move left with `left = max(left, last[c]+1)`.
- Store indices, not just counts, to jump left efficiently.
- Time O(n), space O(min(n, alphabet)).


<a id="longest-substring-without-repeating"></a>
### Longest Substring Without Repeating
**Problem:** Same as “Longest Substring Without Repeating Characters” (alias name).  
**Pseudocode:** Use the same sliding window with `lastIndex` map as above.
**Important points:**
- Alias for the standard ‘no repeating characters’ sliding window (use last index jump).

<a id="longest-repeating-character-replacement"></a>
### Longest Repeating Character Replacement
**Problem:** Longest substring that can be made of same char with at most k replacements.  
**Pseudocode:**
```
freq = HashMap()
left=0; maxFreq=0; best=0
for right in [0..n-1]:
  freq[s[right]]++
  maxFreq = max(maxFreq, freq[s[right]])
  while (right-left+1) - maxFreq > k:
    freq[s[left]]--; left++
  best = max(best, right-left+1)
return best
```
**Important points:**
- Track `maxFreq` of any char in the window; window valid if `len - maxFreq <= k`.
- `maxFreq` can be stale (not decreased) and correctness still holds; avoids O(σ) recompute.
- Time O(n), space O(σ).


<a id="minimum-window-substring"></a>
### Minimum Window Substring
**Problem:** Smallest substring of `s` containing all chars of `t` (with multiplicity).  
**Pseudocode:**
```
need = Counter(t)
have = Counter()
required = number of distinct chars in need
formed = 0
left = 0
bestLen = INF; bestL = 0
for right in [0..len(s)-1]:
  have[s[right]]++
  if s[right] in need and have[s[right]] == need[s[right]]:
    formed++
  while formed == required:
    update best with window [left,right]
    have[s[left]]--
    if s[left] in need and have[s[left]] < need[s[left]]:
      formed--
    left++
return best substring or ""
```
**Important points:**
- Need counts: `needCount` and `haveCount`, plus `formed` vs `required` distinct chars.
- Shrink left while valid to minimize; update best when valid.
- Time O(n) with two pointers; careful with repeated letters in `t`.


<a id="find-all-anagrams-in-a-string"></a>
### Find All Anagrams in a String
**Problem:** Find start indices where `p`'s anagram occurs in `s`.  
**Pseudocode:**
```
need = Counter(p)
window = Counter()
left=0
ans=[]
for right in [0..len(s)-1]:
  window[s[right]]++
  if right-left+1 > len(p):
    window[s[left]]--; if window[s[left]]==0 remove; left++
  if right-left+1 == len(p) and window == need:
    ans.append(left)
return ans
```
**Important points:**
- Fixed-size window of length |p| with char counts; slide one step at a time.
- Optimize by tracking a ‘matches’ counter instead of comparing full maps each time.
- Time O(n), space O(σ).


<a id="sliding-window-maximum"></a>
### Sliding Window Maximum
**Problem:** Max of each window of size k.  
**Pseudocode (monotonic deque):**
```
dq = Deque()  // stores indices, values decreasing
ans=[]
for i in [0..n-1]:
  while dq not empty and nums[dq.back] <= nums[i]: dq.pop_back()
  dq.push_back(i)
  if dq.front <= i-k: dq.pop_front()
  if i >= k-1: ans.append(nums[dq.front])
return ans
```

---

## Strings (Pattern Matching)
**Important points:**
- Monotonic deque of indices; values decreasing from front to back.
- Pop front when index is out of window; pop back while new value is larger.
- Each index pushed/popped once → O(n).

<a id="implement-strstr-kmp"></a>
### Implement strStr / KMP
**Problem:** Find the first occurrence of `pattern` in `text` (or return -1).  
**Key idea:** KMP uses an LPS array to avoid backtracking in the text.  
**Pseudocode:**
```
buildLPS(p):
  lps[0]=0
  len=0
  i=1
  while i < |p|:
    if p[i]==p[len]:
      len++; lps[i]=len; i++
    else if len>0:
      len = lps[len-1]
    else:
      lps[i]=0; i++

kmp(text, pat):
  if pat empty: return 0
  lps = buildLPS(pat)
  i=0; j=0
  while i < |text|:
    if text[i]==pat[j]: i++; j++
    if j==|pat|: return i-j
    else if i<|text| and text[i]!=pat[j]:
      if j>0: j = lps[j-1]
      else: i++
  return -1
```
**Important points:** LPS off-by-one bugs are common; define behavior for empty pattern early.

---

## Binary Search

<a id="find-first-and-last-position-of-element"></a>
### Find First and Last Position of Element
**Problem:** In sorted array, return first and last index of target.  
**Pseudocode:**
```
left = lower_bound(nums, target)          // first >= target
right = lower_bound(nums, target+epsilon) // first > target (or upper_bound)
if left == n or nums[left] != target: return [-1,-1]
return [left, right-1]
```
**Important points:**
- Do two binary searches: lower_bound(target) and lower_bound(target+ε)-1 (or upper_bound-1).
- Always write invariant-based templates to avoid off-by-one bugs.
- If lower_bound points outside array or not equal to target, target is absent.


<a id="lower-upper-bound"></a>
### Lower/Upper Bound
**Problem:** Implement lower_bound (first >= x) and upper_bound (first > x).  
**Pseudocode (lower_bound):**
```
lo=0; hi=n
while lo < hi:
  mid=(lo+hi)//2
  if a[mid] < x: lo=mid+1
  else: hi=mid
return lo
```
**Important points:**
- Lower bound: first index with `a[i] >= x`; upper bound: first with `a[i] > x`.
- Prefer half-open intervals `[lo, hi)` to keep invariants clean.
- Works on monotonic predicate functions for ‘search on answer’ problems.

<a id="search-in-rotated-sorted-array"></a>
### Search in Rotated Sorted Array
**Problem:** Search target in rotated sorted array (distinct).  
**Pseudocode:**
```
lo=0; hi=n-1
while lo<=hi:
  mid=(lo+hi)//2
  if nums[mid]==target: return mid
  if nums[lo] <= nums[mid]:        // left sorted
    if nums[lo] <= target < nums[mid]: hi=mid-1
    else: lo=mid+1
  else:                             // right sorted
    if nums[mid] < target <= nums[hi]: lo=mid+1
    else: hi=mid-1
return -1
```
**Important points:**
- At each step, one half is sorted; decide which half to keep based on target range.
- Assumes no duplicates; duplicates require extra handling and can degrade to O(n).
- Time O(log n).


<a id="find-minimum-in-rotated-sorted-array"></a>
### Find Minimum in Rotated Sorted Array
**Problem:** Find min element in rotated sorted array (distinct).  
**Pseudocode:**
```
lo=0; hi=n-1
while lo < hi:
  mid=(lo+hi)//2
  if nums[mid] > nums[hi]: lo = mid+1
  else: hi = mid
return nums[lo]
```
**Important points:**
- Compare `mid` with `right`: if `a[mid] > a[right]`, min is right half; else left half.
- Assumes no duplicates; with duplicates, shrink boundaries cautiously.
- Time O(log n).


<a id="koko-eating-bananas"></a>
### Koko Eating Bananas
**Problem:** Minimum integer speed k such that all piles are eaten within H hours.  
**Pseudocode:** Same as “Koko Eating Bananas (Search on Answer)” below.
**Important points:**
- Binary search on speed k; predicate `canFinish(k)` is monotone decreasing.
- Use ceiling division `hours += (pile + k - 1) // k`.
- Bounds: `lo=1`, `hi=max(piles)`.

<a id="koko-eating-bananas-search-on-answer"></a>
### Koko Eating Bananas (Search on Answer)
**Problem:** Min integer speed k such that work finishes within H hours.  
**Pseudocode:**
```
lo=1; hi=max(piles)
valid(k):
  hours = sum(ceil(p/k) for p in piles)
  return hours <= H
while lo < hi:
  mid=(lo+hi)//2
  if valid(mid): hi=mid
  else: lo=mid+1
return lo
```
**Important points:**
- Alias: standard ‘binary search on answer’ with a monotone feasibility predicate.


<a id="split-array-largest-sum"></a>
### Split Array Largest Sum
**Problem:** Split array into `m` subarrays to minimize the largest subarray sum.  
**Pseudocode (binary search on answer):**
```
lo = max(nums)
hi = sum(nums)
valid(limit):
  pieces = 1
  cur = 0
  for x in nums:
    if cur + x <= limit:
      cur += x
    else:
      pieces++
      cur = x
  return pieces <= m
while lo < hi:
  mid = (lo+hi)//2
  if valid(mid): hi = mid
  else: lo = mid+1
return lo
```
**Important points:** Greedy `valid()` works because if a limit is feasible, larger limits are also feasible (monotonic).

<a id="median-of-two-sorted-arrays"></a>
### Median of Two Sorted Arrays
**Problem:** Find median of two sorted arrays in O(log(min(m,n))).  
**Pseudocode (partition):**
```
ensure A is smaller
lo=0; hi=len(A)
half=(len(A)+len(B)+1)//2
while lo<=hi:
  i=(lo+hi)//2
  j=half-i
  Aleft = -INF if i==0 else A[i-1]
  Aright= +INF if i==len(A) else A[i]
  Bleft = -INF if j==0 else B[j-1]
  Bright= +INF if j==len(B) else B[j]
  if Aleft <= Bright and Bleft <= Aright:
    if total odd: return max(Aleft,Bleft)
    else: return (max(Aleft,Bleft)+min(Aright,Bright))/2
  elif Aleft > Bright: hi=i-1
  else: lo=i+1
```

---

## Stack / Queue
**Important points:**
- Binary search on partition of the smaller array; enforce `leftMax <= rightMin`.
- Handle edges with ±∞ when partition touches ends.
- Time O(log min(m, n)); common off-by-one source—test tiny arrays.

<a id="valid-parentheses"></a>
### Valid Parentheses
**Problem:** Determine if brackets are balanced.  
**Pseudocode:**
```
stack=[]
for ch in s:
  if ch is opening: stack.push(ch)
  else:
    if stack empty or stack.top != matching_open(ch): return false
    stack.pop()
return stack empty
```
**Important points:**
- Stack of opening brackets; pop and match on closing.
- Reject early when stack empty on closing; stack must be empty at end.
- Time O(n), space O(n).


<a id="decode-string"></a>
### Decode String
**Problem:** Decode an encoded string like `3[a2[c]]` → `accaccacc`.  
**Pseudocode (stack):**
```
stack = []    // (prevString, repeatK)
cur = ""
k = 0
for ch in s:
  if ch is digit:
    k = k*10 + int(ch)
  elif ch == '[':
    stack.push((cur, k))
    cur = ""
    k = 0
  elif ch == ']':
    prev, rep = stack.pop()
    cur = prev + cur repeated rep times
  else:
    cur += ch
return cur
```
**Important points:** k can be multi-digit; nested brackets require stack.

<a id="daily-temperatures"></a>
### Daily Temperatures
**Problem:** For each day, find how many days until warmer temperature.  
**Pseudocode (monotonic stack):**
```
ans = [0]*n
stack = [] // indices with decreasing temps
for i in [0..n-1]:
  while stack not empty and temp[stack.top] < temp[i]:
    j = stack.pop()
    ans[j] = i - j
  stack.push(i)
return ans
```
**Important points:**
- Monotonic decreasing stack of indices; when a warmer temp arrives, resolve previous indices.
- Each index pushed/popped once → O(n).
- Store indices (not values) to compute day differences.

<a id="largest-rectangle-in-histogram"></a>
### Largest Rectangle in Histogram
**Problem:** Largest rectangle area in histogram.  
**Pseudocode:**
```
stack=[] // indices with increasing heights
best=0
for i in [0..n] (treat height[n]=0 sentinel):
  cur = 0 if i==n else h[i]
  while stack not empty and cur < h[stack.top]:
    height = h[stack.pop()]
    left = 0 if stack empty else stack.top+1
    best = max(best, height * (i - left))
  stack.push(i)
return best
```
**Important points:**
- Monotonic increasing stack of indices; compute area when current height breaks monotonicity.
- Use sentinel 0 height at end to flush the stack.
- Width uses next smaller on right and previous smaller on left.


<a id="largest-rectangle-histogram"></a>
### Largest Rectangle Histogram
**Problem:** Alias for “Largest Rectangle in Histogram”.  
**Pseudocode:** Use the sentinel + monotonic stack approach above.
**Important points:**
- Alias for ‘Largest Rectangle in Histogram’; same monotonic stack + sentinel trick.

<a id="evaluate-reverse-polish-notation"></a>
### Evaluate Reverse Polish Notation
**Problem:** Evaluate an expression in postfix notation.  
**Pseudocode:**
```
stack=[]
for token in tokens:
  if token is number: push int(token)
  else:
    b=pop(); a=pop()
    push apply(op, a, b)
return pop()
```
**Important points:**
- Use a stack; on operator pop `b` then `a` and push `a op b` (order matters).
- Define integer division behavior (typically truncate toward zero).
- Time O(n).


---

## Linked List

<a id="reverse-linked-list"></a>
### Reverse Linked List
**Problem:** Reverse a singly linked list.  
**Pseudocode:**
```
prev=null; cur=head
while cur:
  nxt=cur.next
  cur.next=prev
  prev=cur
  cur=nxt
return prev
```
**Important points:**
- Iterative pointer flip: keep `prev`, `cur`, `next`.
- Don’t lose the remainder: store `next` before rewiring.
- Time O(n), space O(1).


<a id="linked-list-cycle-ii"></a>
### Linked List Cycle II
**Problem:** Detect cycle and return entry node (or null).  
**Pseudocode:**
```
slow=head; fast=head
while fast and fast.next:
  slow=slow.next; fast=fast.next.next
  if slow==fast: break
if no meeting: return null
p1=head; p2=slow
while p1 != p2:
  p1=p1.next; p2=p2.next
return p1
```
**Important points:**
- Floyd’s tortoise/hare to find meeting point; then reset one pointer to head to find entry.
- Proof uses distance equations; works with O(1) space.
- Handle no-cycle case cleanly.


<a id="cycle-ii"></a>
### Cycle II
**Problem:** Alias for “Linked List Cycle II”.  
**Pseudocode:** Use Floyd’s meet + reset approach above.
**Important points:**
- Alias for ‘Linked List Cycle II’; same Floyd entry-finding step.

<a id="copy-list-with-random-pointer"></a>
### Copy List with Random Pointer
**Problem:** Deep copy a linked list where each node has `next` and `random` pointers.  
**Pseudocode (hash map):**
```
map = HashMap(oldNode -> newNode)
for node in original:
  map[node] = new Node(node.val)
for node in original:
  map[node].next = map.get(node.next)
  map[node].random = map.get(node.random)
return map[head]
```
**Important points:** Must preserve sharing/cycles via map; O(1) space interleaving trick is a follow-up.

<a id="merge-two-sorted-lists"></a>
### Merge Two Sorted Lists
**Problem:** Merge two sorted linked lists.  
**Pseudocode:**
```
dummy = Node()
tail = dummy
while a and b:
  if a.val <= b.val: tail.next=a; a=a.next
  else: tail.next=b; b=b.next
  tail=tail.next
tail.next = a if a else b
return dummy.next
```
**Important points:**
- Use a dummy head and stitch by picking the smaller head each step.
- Stable merge: if equal, either order is fine unless specified.
- Time O(m+n), space O(1).


<a id="remove-nth-from-end"></a>
### Remove Nth From End
**Problem:** Remove the n-th node from end in one pass.  
**Pseudocode:**
```
dummy.next=head
fast=dummy
repeat n times: fast=fast.next
slow=dummy
while fast.next:
  fast=fast.next; slow=slow.next
slow.next = slow.next.next
return dummy.next
```
**Important points:**
- Use a dummy head; advance `fast` by n+1 then move both pointers.
- When `fast` hits null, `slow.next` is the node to delete.
- Covers deleting the head cleanly via dummy.


---

## Trees / BST

<a id="maximum-depth-of-binary-tree"></a>
### Maximum Depth of Binary Tree
**Problem:** Return maximum depth (height) of a binary tree.  
**Pseudocode:**
```
dfs(node):
  if node == null: return 0
  return 1 + max(dfs(node.left), dfs(node.right))
return dfs(root)
```
**Important points:**
- DFS recursion: `1 + max(left, right)`; BFS level-order also works.
- For very deep trees, iterative avoids recursion depth limits.
- Time O(n), space O(h) recursion stack.


<a id="validate-bst"></a>
### Validate BST
**Problem:** Check if a binary tree satisfies BST ordering.  
**Pseudocode (bounds):**
```
dfs(node, lo, hi):
  if node==null: return true
  if not (lo < node.val < hi): return false
  return dfs(left, lo, node.val) and dfs(right, node.val, hi)
return dfs(root, -INF, +INF)
```
**Important points:**
- Use bounds recursion (`low < val < high`) or inorder strictly increasing sequence.
- Use 64-bit bounds to avoid overflow at int limits.
- Duplicates: clarify whether allowed; typical LeetCode requires strict ordering.

<a id="lowest-common-ancestor-bst-general"></a>
### Lowest Common Ancestor (BST + general)
**Problem:** Find LCA of two nodes in a BST and in a general binary tree.  
**Pseudocode (BST):**
```
cur=root
while cur:
  if p.val < cur.val and q.val < cur.val: cur=cur.left
  elif p.val > cur.val and q.val > cur.val: cur=cur.right
  else: return cur
```
**Pseudocode (binary tree):**
```
if root is null or root==p or root==q: return root
L = lca(root.left); R = lca(root.right)
if L and R: return root
return L if L else R
```
**Important points:**
- BST: walk down using value comparisons; general tree: postorder recursion returning matches.
- In general tree, if both sides return non-null, current node is LCA.
- Clarify if both nodes are guaranteed to exist in the tree.

<a id="lowest-common-ancestor-bst"></a>
### Lowest Common Ancestor (BST)
**Problem:** Find LCA in a BST (alias).  
**Pseudocode:** Use the BST loop from “Lowest Common Ancestor (BST + general)” above.
**Important points:**
- BST-specific: if both targets < root go left; if both > root go right; else root is LCA.
- Time O(h), space O(1) iterative.

<a id="lca-binary-tree"></a>
### LCA (binary tree)
**Problem:** Find LCA in a general binary tree (alias).  
**Pseudocode:** Use the recursive binary-tree method from “Lowest Common Ancestor (BST + general)” above.
**Important points:**
- General binary tree: postorder recursion; return node if it matches p/q or is LCA.
- Time O(n); recursion stack O(h).
- If nodes may be missing, track found flags to validate.

<a id="binary-tree-level-order-traversal"></a>
### Binary Tree Level Order Traversal
**Problem:** Return level-order traversal of a tree.  
**Pseudocode:**
```
queue = [root]
ans=[]
while queue not empty:
  size = queue.size
  level=[]
  repeat size times:
    node=pop_front(queue)
    level.append(node.val)
    push children if not null
  ans.append(level)
return ans
```
**Important points:**
- Queue BFS; process `levelSize` nodes per level to group outputs.
- Time O(n), space O(width).


<a id="kth-smallest-in-bst"></a>
### Kth Smallest in BST
**Problem:** Return kth smallest value in BST.  
**Pseudocode (inorder):**
```
stack=[]
cur=root
while cur or stack:
  while cur: stack.push(cur); cur=cur.left
  cur=stack.pop()
  k--
  if k==0: return cur.val
  cur=cur.right
```
**Important points:**
- Inorder traversal visits nodes in sorted order; stop when count reaches k.
- Iterative stack avoids recursion depth issues.
- If updates are frequent, discuss augmenting nodes with subtree sizes.

<a id="binary-tree-maximum-path-sum"></a>
### Binary Tree Maximum Path Sum
**Problem:** Max sum over any path (node-to-node).  
**Pseudocode:**
```
best = -INF
gain(node):
  if node==null: return 0
  L = max(0, gain(node.left))
  R = max(0, gain(node.right))
  best = max(best, node.val + L + R)
  return node.val + max(L, R)
gain(root)
return best
```
**Important points:**
- Postorder: return max gain to parent (`max(0, leftGain, rightGain) + val`).
- Global answer considers splitting at node: `val + leftGain + rightGain`.
- Must handle all-negative trees (initialize best to -inf).


<a id="max-path-sum"></a>
### Max Path Sum
**Problem:** Alias for “Binary Tree Maximum Path Sum”.  
**Pseudocode:** Use the gain + global update approach above.
**Important points:**
- Alias for ‘Binary Tree Maximum Path Sum’; same gain-vs-global split logic.

<a id="serialize-and-deserialize-binary-tree"></a>
### Serialize and Deserialize Binary Tree
**Problem:** Convert tree to string and back.  
**Pseudocode (preorder + null markers):**
```
serialize(node):
  if node==null: output "#"; return
  output node.val
  serialize(node.left)
  serialize(node.right)

deserialize():
  token = next token
  if token == "#": return null
  node = new TreeNode(int(token))
  node.left = deserialize()
  node.right = deserialize()
  return node
```
**Important points:**
- Pick a traversal (preorder/BFS) and include null markers to preserve structure.
- Deserialize must consume tokens in the same order; recursion is simplest for preorder.
- Define separators and handle empty tree.

<a id="serialize-deserialize-binary-tree"></a>
### Serialize / Deserialize Binary Tree
**Problem:** Alias name used for “Serialize and Deserialize Binary Tree”.  
**Pseudocode:** Use the preorder + null marker approach above.
**Important points:**
- Alias for ‘Serialize and Deserialize Binary Tree’; keep traversal + null markers consistent.

<a id="serialize-deserialize"></a>
### Serialize/Deserialize
**Problem:** Alias name used for “Serialize and Deserialize Binary Tree”.  
**Pseudocode:** Use the preorder + null marker approach above.
**Important points:**
- Alias for binary tree serialize/deserialize; emphasize null markers and order consistency.

---

## Graphs (BFS/DFS/Topo)

<a id="number-of-islands"></a>
### Number of Islands
**Problem:** Count connected components of 1s in a grid (4-dir).  
**Pseudocode:**
```
seen = set()
ans=0
for each cell (r,c):
  if grid[r][c]==1 and (r,c) not in seen:
    ans++
    BFS/DFS to mark all reachable 1s as seen
return ans
```
**Important points:**
- DFS/BFS flood-fill; mark visited (or mutate grid to ‘0’) to avoid revisits.
- Time O(R*C); recursion depth can be large—iterative BFS is safer.


<a id="alien-dictionary"></a>
### Alien Dictionary
**Problem:** Given sorted words in an alien language, infer a valid character order.  
**Pseudocode (build edges + topo):**
```
adj = HashMap(char -> set of chars)
indeg = HashMap(char -> 0)
add all chars from all words into indeg with 0
for i in 0..len(words)-2:
  w1, w2 = words[i], words[i+1]
  if w1 startswith w2 and len(w1)>len(w2): return ""   // invalid prefix
  find first j where w1[j] != w2[j]:
    add edge w1[j] -> w2[j] if not present; indeg[w2[j]]++
    break
queue = all chars with indeg 0
order = []
while queue:
  c = pop
  order.append(c)
  for nei in adj[c]:
    indeg[nei]--
    if indeg[nei]==0: push nei
return "" if order length != #chars else join(order)
```
**Important points:** Prefix invalid case; include isolated letters; cycle ⇒ impossible.

<a id="rotting-oranges"></a>
### Rotting Oranges
**Problem:** Minutes to rot all fresh oranges (multi-source BFS).  
**Pseudocode:**
```
queue = all rotten cells
fresh = count fresh
minutes = 0
while queue not empty and fresh>0:
  repeat queue.size times:
    cell = pop_front
    for each neighbor fresh:
      mark rotten; fresh--; push neighbor
  minutes++
return minutes if fresh==0 else -1
```
**Important points:**
- Multi-source BFS from all rotten oranges simultaneously; each level = 1 minute.
- Track fresh count; if any remain at end, return -1.
- Time O(R*C).


<a id="course-schedule"></a>
### Course Schedule
**Problem:** Determine if all courses can be finished given prerequisites.  
**Pseudocode:** Same topo/cycle detection as below.
**Important points:**
- Detect cycle in directed graph via Kahn’s algorithm (indegree) or DFS colors.
- If processed nodes == n, schedule possible; else cycle exists.
- Time O(V+E).

<a id="course-schedule-topo-cycle"></a>
### Course Schedule (Topo + cycle)
**Problem:** Determine if all courses can be finished given prerequisites.  
**Pseudocode (Kahn):**
```
build adj prereq->course and indegree[]
queue = all nodes with indegree 0
count=0
while queue:
  u=pop; count++
  for v in adj[u]:
    indegree[v]--
    if indegree[v]==0: push v
return count==n
```
**Important points:**
- Alias: topological sort + cycle detection (Kahn or DFS colors).

<a id="clone-graph"></a>
### Clone Graph
**Problem:** Deep copy a graph given a node.  
**Pseudocode:**
```
if node null: return null
map = HashMap(old -> copy)
queue=[node]
map[node]=new Node(node.val)
while queue:
  cur=pop
  for nei in cur.neighbors:
    if nei not in map:
      map[nei]=new Node(nei.val)
      push nei
    map[cur].neighbors.append(map[nei])
return map[node]
```
**Important points:**
- BFS/DFS with a map `original -> clone` to avoid duplicating nodes and to handle cycles.
- Create clone nodes lazily when first seen.
- Time O(V+E).


<a id="word-ladder"></a>
### Word Ladder
**Problem:** Shortest transformations from begin to end by changing one letter (words in dict).  
**Pseudocode:**
```
dict = set(wordList)
if end not in dict: return 0
queue=[begin]; dist=1
while queue:
  for each node in current level:
    word=pop
    if word==end: return dist
    for each neighbor one-letter change in dict:
      remove neighbor from dict
      push neighbor
  dist++
return 0
```
**Important points:**
- BFS for shortest path in unweighted graph; consider bidirectional BFS for speed.
- Precompute generic patterns (`h*t`) to find neighbors efficiently.
- Mark visited per level to avoid revisiting and to preserve shortest distance.


<a id="cheapest-flights-within-k-stops"></a>
### Cheapest Flights Within K Stops
**Problem:** Minimum cost from src to dst with at most K stops.  
**Pseudocode (Bellman-Ford for K+1 edges):**
```
dist = [INF]*n
dist[src]=0
repeat K+1 times:
  next = dist copy
  for each edge (u,v,w):
    if dist[u] + w < next[v]:
      next[v] = dist[u] + w
  dist = next
return dist[dst] if dist[dst] < INF else -1
```
**Important points:** Standard Dijkstra “visited” pruning can fail with stop constraint; BF-style relaxation per layer is safe.

<a id="network-delay-time-dijkstra"></a>
### Network Delay Time (Dijkstra)
**Problem:** Given directed weighted edges, time for signal to reach all nodes from K.  
**Pseudocode:**
```
adj = build adjacency (u -> (v,w))
dist = INF; dist[K]=0
heap = [(0,K)]
while heap:
  d,u = pop_min
  if d != dist[u]: continue
  for (v,w) in adj[u]:
    if d+w < dist[v]:
      dist[v]=d+w
      push (dist[v], v)
ans = max(dist)
return ans if ans < INF else -1
```
**Important points:**
- Dijkstra with min-heap; skip outdated heap entries when `d > dist[u]`.
- Requires non-negative weights.
- Answer is `max(dist)` if all reachable else -1.


<a id="network-delay-time"></a>
### Network Delay Time
**Problem:** Alias for “Network Delay Time (Dijkstra)”.  
**Pseudocode:** Use Dijkstra as above.
**Important points:**
- Alias: Dijkstra on directed weighted graph with non-negative edges.

<a id="dijkstra"></a>
### Dijkstra
**Problem:** Compute shortest paths from a source in a graph with non-negative edge weights.  
**Pseudocode (min-heap):**
```
dist = [INF]*n
dist[src]=0
heap = [(0, src)]
while heap:
  d,u = pop_min(heap)
  if d != dist[u]: continue         // stale
  for (v,w) in adj[u]:
    if d+w < dist[v]:
      dist[v] = d+w
      push (dist[v], v)
return dist
```
**Important points:** Doesn’t work with negative weights; “stale entry” skip is required when using a heap.

---

## Advanced Graphs (Occasionally in Google L4/L5)

<a id="critical-connections-bridges"></a>
### Critical Connections (Bridges)
**Problem:** Find all bridges in an undirected graph.  
**Key idea:** Tarjan DFS with discovery time `disc[u]` and low-link `low[u]`. Bridge if `low[v] > disc[u]`.  
**Pseudocode:**
```
time = 0
disc = array filled -1
low = array
bridges = []

dfs(u, parent):
  disc[u] = low[u] = time; time++
  for v in adj[u]:
    if v == parent: continue
    if disc[v] == -1:
      dfs(v, u)
      low[u] = min(low[u], low[v])
      if low[v] > disc[u]:
        bridges.append((u, v))
    else:
      low[u] = min(low[u], disc[v])   // back edge

for each node u:
  if disc[u] == -1: dfs(u, -1)
return bridges
```
**Important points:** Graph may be disconnected; parent-edge check avoids treating the tree edge as a back edge.

---

## Heaps

<a id="top-k-frequent-elements"></a>
### Top K Frequent Elements
**Problem:** Return k most frequent elements.  
**Pseudocode (min-heap size k):**
```
freq = count map
heap = empty min-heap of (freq, value)
for each (value,f) in freq:
  push (f,value)
  if heap.size > k: pop_min
return values in heap
```
**Important points:**
- Count with hash map; then use min-heap of size k (or bucket sort).
- Heap approach: O(n log k); bucket: O(n) time and space.
- Clarify if output order matters (usually not).

<a id="merge-k-sorted-lists"></a>
### Merge K Sorted Lists
**Problem:** Merge k sorted linked lists.  
**Pseudocode:**
```
heap = []
for each list i:
  if head exists: push (head.val, i, head)
dummy = Node(); tail=dummy
while heap not empty:
  val,i,node = pop_min
  tail.next=node; tail=tail.next
  if node.next: push (node.next.val, i, node.next)
return dummy.next
```
**Important points:**
- Min-heap of current list heads; pop smallest and push its next.
- Time O(N log k) where N is total nodes; heap holds up to k nodes.
- Alternative divide-and-conquer merge is also O(N log k).


<a id="find-median-from-data-stream"></a>
### Find Median from Data Stream
**Problem:** Support addNum and findMedian.  
**Pseudocode (two heaps):**
```
lo = max-heap (lower half)
hi = min-heap (upper half)
add(x):
  push x into lo
  move max(lo) to hi
  if size(lo) < size(hi): move min(hi) to lo
median():
  if size(lo) > size(hi): return top(lo)
  else return (top(lo)+top(hi))/2
```

---

## Dynamic Programming
**Important points:**
- Two heaps: max-heap for lower half, min-heap for upper half.
- Maintain size invariant (difference ≤ 1) and ordering invariant (maxLower ≤ minUpper).
- Median from heap tops; O(log n) per insert.

<a id="house-robber"></a>
### House Robber
**Problem:** Max sum of non-adjacent elements.  
**Pseudocode:**
```
take=0; skip=0
for x in nums:
  newTake = skip + x
  newSkip = max(skip, take)
  take=newTake; skip=newSkip
return max(take, skip)
```
**Important points:**
- DP: `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`.
- Space optimize to two variables (prev1, prev2).
- Edge cases: empty, single house.


<a id="coin-change-min"></a>
### Coin Change (min)
**Problem:** Min coins to make amount, return -1 if impossible.  
**Pseudocode:**
```
dp[0]=0; dp[1..amount]=INF
for a in [1..amount]:
  for c in coins:
    if a-c >= 0:
      dp[a] = min(dp[a], 1 + dp[a-c])
return -1 if dp[amount]==INF else dp[amount]
```
**Important points:**
- Unbounded knapsack DP on amount: `dp[a] = min(dp[a], dp[a-coin]+1)`.
- Initialize dp with INF and dp[0]=0; unreachable amounts remain INF.
- Time O(amount * #coins).


<a id="coin-change"></a>
### Coin Change
**Problem:** Alias name used for the “minimum coins” variant.  
**Pseudocode:** Use “Coin Change (min)” above.
**Important points:**
- Alias for min-coin DP; distinguish from ‘number of ways’ variant.

<a id="longest-increasing-subsequence"></a>
### Longest Increasing Subsequence
**Problem:** Length of LIS.  
**Pseudocode (tails, O(n log n)):**
```
tails=[]
for x in nums:
  i = lower_bound(tails, x)
  if i == len(tails): tails.append(x)
  else tails[i] = x
return len(tails)
```
**Important points:**
- Patience sorting: maintain `tails[len] = min tail value` and binary search updates.
- Gives length in O(n log n); reconstructing sequence needs parent pointers.
- For strict vs non-decreasing LIS, adjust binary search (lower vs upper bound).

<a id="lis"></a>
### LIS
**Problem:** Alias for “Longest Increasing Subsequence”.  
**Pseudocode:** Use the tails + lower_bound method above.
**Important points:**
- Alias for ‘Longest Increasing Subsequence’; mention patience sorting + strictness choice.

<a id="longest-common-subsequence"></a>
### Longest Common Subsequence
**Problem:** Length of LCS between strings a,b.  
**Pseudocode:**
```
dp = 2D array (m+1)x(n+1) zeros
for i in [1..m]:
  for j in [1..n]:
    if a[i-1]==b[j-1]: dp[i][j]=1+dp[i-1][j-1]
    else: dp[i][j]=max(dp[i-1][j], dp[i][j-1])
return dp[m][n]
```
**Important points:**
- Classic 2D DP on prefixes; `dp[i][j]` length for first i and first j chars.
- Space optimize to 2 rows if only length needed.
- Don’t confuse with substring (contiguous) which uses different DP.


<a id="edit-distance"></a>
### Edit Distance
**Problem:** Min insert/delete/replace to convert a to b.  
**Pseudocode:**
```
dp = 2D (m+1)x(n+1)
dp[i][0]=i; dp[0][j]=j
for i in [1..m]:
  for j in [1..n]:
    if a[i-1]==b[j-1]: dp[i][j]=dp[i-1][j-1]
    else dp[i][j]=1+min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
return dp[m][n]
```
**Important points:**
- DP with operations: insert/delete/replace; base cases `dp[i][0]=i`, `dp[0][j]=j`.
- Transition uses min of 3 neighbors; if chars match, take diagonal.
- Space optimize to 2 rows for length only.


<a id="lcs-edit-distance"></a>
### LCS / Edit Distance
**Problem:** Common DP pair in interviews: LCS measures overlap; edit distance measures transformation cost.  
**Pseudocode:** Use the 2D DP recurrences in “Longest Common Subsequence” and “Edit Distance” above.
**Important points:**
- Alias entry: know both DP tables and how transitions differ (match vs edit ops).

<a id="word-break"></a>
### Word Break
**Problem:** Can string be segmented into dictionary words?  
**Pseudocode:**
```
dp[0]=true
for i in [1..n]:
  dp[i]=false
  for each word w in dict:
    if len(w)<=i and dp[i-len(w)] and s[i-len(w):i]==w:
      dp[i]=true; break
return dp[n]
```
**Important points:**
- Boolean DP: `dp[i]=True` if some `dp[j]` and `s[j:i]` in dict.
- Optimize by limiting j to max word length; use a hash set for O(1) lookup.
- Worst-case O(n^2) substrings; mention trie optimization if asked.


---

## DP (Hard / Classic)

<a id="regular-expression-matching"></a>
### Regular Expression Matching
**Problem:** Match string `s` with pattern `p` with `.` and `*` (`*` repeats previous token 0+ times).  
**Pseudocode (DP):**
```
dp = (m+1) x (n+1) false
dp[0][0] = true

for j in 2..n:
  if p[j-1] == '*':
    dp[0][j] = dp[0][j-2]

for i in 1..m:
  for j in 1..n:
    if p[j-1] != '*':
      match = (p[j-1] == '.' or p[j-1] == s[i-1])
      dp[i][j] = match and dp[i-1][j-1]
    else:
      dp[i][j] = dp[i][j-2]                 // zero occurrences
      prev = p[j-2]
      match = (prev == '.' or prev == s[i-1])
      if match:
        dp[i][j] = dp[i][j] or dp[i-1][j]   // consume one char, stay on j
return dp[m][n]
```
**Important points:** Initialization for empty string with `a*` patterns; `*` binds to `p[j-2]`.

<a id="the-skyline-problem"></a>
### The Skyline Problem
**Problem:** Given buildings (L,R,H), output skyline key points.  
**Key idea:** Sweep line + max-heap of active buildings.  
**Pseudocode:**
```
events = []
for (L,R,H):
  events.add((L, -H, R))     // start
  events.add((R, 0, 0))      // end marker
sort events by x then height

heap = max-heap of (height, endX)
result = []
prevMax = 0
for (x, negH, R) in events:
  while heap not empty and heap.top.endX <= x:
    pop heap
  if negH != 0:
    push (height=-negH, endX=R)
  currMax = heap.top.height if heap not empty else 0
  if currMax != prevMax:
    result.add((x, currMax))
    prevMax = currMax
return result
```
**Important points:** Remove expired buildings first; handle same-x ordering (starts before ends).

<a id="longest-valid-parentheses"></a>
### Longest Valid Parentheses
**Problem:** Length of longest valid parentheses substring.  
**Pseudocode (stack of indices):**
```
stack = [-1]
best = 0
for i in 0..n-1:
  if s[i] == '(':
    stack.push(i)
  else:
    stack.pop()
    if stack empty:
      stack.push(i)     // reset base
    else:
      best = max(best, i - stack.top)
return best
```
**Important points:** Base index `-1` (or last invalid) is crucial; resetting when stack empties avoids negative lengths.

<a id="burst-balloons"></a>
### Burst Balloons
**Problem:** Max coins by bursting balloons in best order (interval DP).  
**Pseudocode:**
```
nums = [1] + nums + [1]
n = len(nums)
dp = 2D array n x n zeros
for length from 2 to n-1:
  for left from 0 to n-length-1:
    right = left + length
    for k in (left+1 .. right-1):
      dp[left][right] = max(dp[left][right], dp[left][k] + dp[k][right] + nums[left]*nums[k]*nums[right])
return dp[0][n-1]
```
**Important points:** Add sentinel 1s; choose `k` as the last balloon in `(left,right)` open interval.

---

## Backtracking

<a id="permutations"></a>
### Permutations
**Problem:** Generate all permutations of distinct nums.  
**Pseudocode:**
```
res=[]
used=[false]*n
path=[]
dfs():
  if len(path)==n: res.add(copy(path)); return
  for i in [0..n-1]:
    if used[i]: continue
    used[i]=true; path.push(nums[i])
    dfs()
    path.pop(); used[i]=false
dfs()
return res
```
**Important points:**
- Backtrack with swap-in-place or `used[]` array; revert state on return.
- Time O(n·n!) and output size dominates; focus on correctness and pruning when possible.


<a id="subsets"></a>
### Subsets
**Problem:** Generate all subsets (power set).  
**Pseudocode (include/exclude):**
```
res=[]; path=[]
dfs(i):
  if i==n: res.add(copy(path)); return
  dfs(i+1)
  path.push(nums[i])
  dfs(i+1)
  path.pop()
dfs(0)
return res
```
**Important points:**
- Backtracking include/exclude; each element either chosen or not → 2^n subsets.
- Often asked to produce in any order; recursion is simplest.

<a id="subsets-ii"></a>
### Subsets II
**Problem:** Generate all unique subsets when nums may contain duplicates.  
**Pseudocode:**
```
sort nums
res=[]
path=[]
dfs(start):
  res.add(copy(path))
  for i in [start..n-1]:
    if i>start and nums[i]==nums[i-1]: continue   // skip duplicates at this level
    path.push(nums[i])
    dfs(i+1)
    path.pop()
dfs(0)
return res
```
**Important points:** Only skip duplicates when `i>start` (same recursion level), not globally.

<a id="combination-sum"></a>
### Combination Sum
**Problem:** Find combinations summing to target (can reuse same number).  
**Pseudocode:**
```
sort candidates
res=[]; path=[]
dfs(start, remain):
  if remain==0: res.add(copy(path)); return
  for i in [start..n-1]:
    x=candidates[i]
    if x>remain: break
    path.push(x)
    dfs(i, remain-x)    // reuse i
    path.pop()
dfs(0, target)
return res
```
**Important points:**
- Backtracking with reuse: keep index `i` the same after choosing candidate i.
- Sort to prune when remaining < candidate.
- Avoid duplicates by enforcing non-decreasing choice order.


<a id="word-search"></a>
### Word Search
**Problem:** Determine if word exists in grid via adjacent cells (no reuse).  
**Pseudocode:**
```
dfs(r,c,idx):
  if idx==len(word): return true
  if out of bounds or grid[r][c]!=word[idx]: return false
  tmp=grid[r][c]; grid[r][c]='#'
  ok = dfs neighbors with idx+1
  grid[r][c]=tmp
  return ok
for each cell:
  if dfs(cell,0): return true
return false
```
**Important points:**
- DFS backtracking from each cell; mark visited (temporary) and restore on return.
- Prune early when char mismatch; optionally pre-check letter frequency.
- Time can blow up; mention constraints and pruning tricks.


---

## Union-Find

<a id="redundant-connection"></a>
### Redundant Connection
**Problem:** In an undirected graph that is a tree plus one edge, find edge that creates cycle.  
**Pseudocode:**
```
dsu = DSU(n)
last = None
for (u,v) in edges:
  if dsu.find(u) == dsu.find(v):
    last = (u,v)
  else:
    dsu.union(u,v)
return last
```
**Important points:**
- DSU/Union-Find: the first edge where `find(u)==find(v)` forms a cycle.
- Use path compression + union by rank/size for near O(1) amortized.
- Graph is undirected with n nodes and n edges (tree + 1 extra).


---

## Bit Manipulation

<a id="single-number"></a>
### Single Number
**Problem:** Every element appears twice except one; find the single.  
**Pseudocode:**
```
x=0
for v in nums: x = x XOR v
return x
```
**Important points:**
- XOR cancels pairs: `a^a=0`, `0^b=b` → XOR all numbers to get the unique.
- Variants exist (appear 3 times, two uniques) — clarify which version you’re solving.


<a id="counting-bits"></a>
### Counting Bits
**Problem:** For i=0..n, compute number of set bits in i.  
**Pseudocode:**
```
bits[0]=0
for i in [1..n]:
  bits[i] = bits[i>>1] + (i&1)
return bits
```
**Important points:**
- DP: `bits[i] = bits[i>>1] + (i&1)` or `bits[i] = bits[i&(i-1)] + 1`.
- Linear time; great to mention bit trick `i&(i-1)` clears lowest set bit.


<a id="total-hamming-distance"></a>
### Total Hamming Distance
**Problem:** Sum of pairwise Hamming distances among nums.  
**Pseudocode:**
```
ans=0
for b in [0..31]:
  ones = count of nums with bit b set
  ans += ones * (n - ones)
return ans
```
**Important points:**
- Sum per bit position: ones * zeros across all numbers.
- Assume 32-bit or 64-bit width depending on constraints.
- Time O(32*n) and O(1) extra space.


<a id="maximum-xor-of-two-numbers"></a>
### Maximum XOR of Two Numbers
**Problem:** Maximum XOR of any two numbers in an array.  
**Pseudocode:** Same as “Maximum XOR Pair” below (greedy by prefixes).
**Important points:**
- Use a bitwise trie (0/1) from MSB to LSB; greedily try opposite bit to maximize XOR.
- Alternatively, iterative prefix-set approach also works (bit by bit).
- Time O(W*n) where W is bit width (e.g., 32).

<a id="maximum-xor-pair"></a>
### Maximum XOR Pair
**Problem:** Max XOR of any two numbers.  
**Pseudocode (prefix greedy):**
```
ans=0; mask=0
for b from 31 down to 0:
  mask |= (1<<b)
  prefixes = set(x & mask for x in nums)
  candidate = ans | (1<<b)
  if exists p in prefixes such that (candidate XOR p) in prefixes:
    ans = candidate
return ans
```

---

## Greedy
**Important points:**
- Alias for ‘Maximum XOR of Two Numbers’; same trie/prefix-set approach.

<a id="jump-game-ii"></a>
### Jump Game II
**Problem:** Minimum jumps to reach last index (assume reachable).  
**Pseudocode:**
```
jumps=0; end=0; furthest=0
for i in [0..n-2]:
  furthest = max(furthest, i + nums[i])
  if i == end:
    jumps++
    end = furthest
return jumps
```
**Important points:**
- Greedy BFS-level idea: expand current range, track farthest reach for next step.
- Increment steps when you finish the current range (`i==end`).
- Time O(n), space O(1).


<a id="gas-station"></a>
### Gas Station
**Problem:** Find start index to complete circuit, or -1.  
**Pseudocode:**
```
if sum(gas) < sum(cost): return -1
start=0; tank=0
for i in [0..n-1]:
  tank += gas[i] - cost[i]
  if tank < 0:
    start = i+1
    tank = 0
return start
```
**Important points:**
- If total gas < total cost, impossible (return -1).
- Greedy: when tank drops below 0, next station becomes the new start.
- Single pass O(n) proof relies on deficit cancellation.


<a id="non-overlapping-intervals"></a>
### Non-overlapping Intervals
**Problem:** Remove minimum intervals to make the rest non-overlapping.  
**Pseudocode:** Same as “Non-overlapping Intervals (min removals)” below.
**Important points:**
- Greedy by earliest end time keeps maximum number of non-overlapping intervals.
- To minimize removals: removals = n - maxNonOverlap.
- Sort by end (not start) for the classic greedy proof.

<a id="non-overlapping-intervals-min-removals"></a>
### Non-overlapping Intervals (min removals)
**Problem:** Minimum intervals to remove to eliminate overlaps.  
**Pseudocode:**
```
sort intervals by end
end = intervals[0].end
removed = 0
for each (s,e) from second:
  if s < end: removed++
  else: end = e
return removed
```
**Important points:**
- Alias: minimize removals = keep as many as possible by sorting by end and greedily selecting.


<a id="task-scheduler"></a>
### Task Scheduler
**Problem:** Given tasks and cooldown n, find least time to finish.  
**Pseudocode (math):**
```
freq = count of each task
maxFreq = maximum freq
numMax = number of tasks with freq == maxFreq
slots = (maxFreq - 1) * (n + 1) + numMax
return max(slots, len(tasks))
```
**Important points:** The formula is capped by total tasks; heap simulation is an alternative.

---

## Maths

<a id="gcd-lcm"></a>
### GCD / LCM
**Problem:** Compute gcd and lcm of two integers.  
**Pseudocode:**
```
gcd(a,b):
  while b != 0:
    a, b = b, a % b
  return abs(a)
lcm(a,b):
  if a==0 or b==0: return 0
  return (a / gcd(a,b)) * b
```
**Important points:**
- Euclid’s algorithm for gcd; `lcm(a,b)=a/gcd(a,b)*b` (divide first to reduce overflow).
- For multiple numbers, fold gcd/lcm pairwise.
- Sign/zero edge cases: gcd(a,0)=|a|; lcm(0,*)=0.


<a id="count-primes"></a>
### Count Primes
**Problem:** Count primes < n.  
**Pseudocode (sieve):**
```
isPrime = [true]*n
isPrime[0]=isPrime[1]=false
for p from 2 while p*p < n:
  if isPrime[p]:
    for multiple from p*p step p:
      isPrime[multiple]=false
return count true in isPrime
```
**Important points:**
- Sieve of Eratosthenes: mark multiples starting at i*i.
- Stop at sqrt(n); time ~ O(n log log n).
- Handle n<=2 (answer 0).

<a id="trailing-zeroes-in-factorial"></a>
### Trailing Zeroes in Factorial
**Problem:** Count trailing zeros in n!.  
**Pseudocode:**
```
ans=0
while n>0:
  n = n//5
  ans += n
return ans
```
**Important points:**
- Count factor 5s in n!: `sum_{k>=1} floor(n/5^k)`.
- 2s are plentiful, so 5s determine trailing zeros.
- Time O(log_5 n).


<a id="trailing-zeroes"></a>
### Trailing Zeroes
**Problem:** Alias for “Trailing Zeroes in Factorial”.  
**Pseudocode:** Use the repeated divide-by-5 sum above.
**Important points:**
- Alias for trailing zeros in factorial; count 5s via repeated division by 5.

---

## Sorting

<a id="kth-largest-element"></a>
### Kth Largest Element
**Problem:** Find kth largest element in array.  
**Pseudocode (quickselect):**
```
target = n - k
while true:
  pivotIndex = choose random in [lo..hi]
  p = partition(nums, lo, hi, pivotIndex)  // returns final pivot position
  if p == target: return nums[p]
  if p < target: lo = p+1
  else: hi = p-1
```
**Important points:**
- Quickselect average O(n) is common; heap of size k is O(n log k).
- Careful with partition implementation and duplicates.
- Clarify 1-indexed vs 0-indexed k.

<a id="kth-largest"></a>
### Kth Largest
**Problem:** Alias for “Kth Largest Element”.  
**Pseudocode:** Use quickselect as above (or a min-heap of size k).
**Important points:**
- Alias for Kth Largest Element; quickselect vs heap tradeoffs.

---

## Concurrency (Sometimes appears as “coding” round)

<a id="print-foobar-alternately"></a>
### Print FooBar Alternately
**Problem:** Two threads print “foo” and “bar” alternately n times.  
**Pseudocode (two semaphores):**
```
semFoo = Semaphore(1)
semBar = Semaphore(0)

threadFoo:
  repeat n times:
    semFoo.acquire()
    print("foo")
    semBar.release()

threadBar:
  repeat n times:
    semBar.acquire()
    print("bar")
    semFoo.release()
```
**Important points:** Initial semaphore counts decide who starts; release order must be consistent to avoid deadlocks.

<a id="dining-philosophers-deadlock-free"></a>
### Dining Philosophers (Deadlock-free)
**Problem:** 5 philosophers need two forks; avoid deadlock.  
**Pseudocode (resource ordering):**
```
pickUp(i):
  left = i
  right = (i+1) % 5
  first = min(left, right)
  second = max(left, right)
  lock(fork[first])
  lock(fork[second])

putDown(i):
  unlock both forks
```
**Important points:** Total order on locks breaks circular wait; alternative is a waiter semaphore.

---

## Graph Path Construction

<a id="reconstruct-itinerary"></a>
### Reconstruct Itinerary
**Problem:** Given flight tickets (from,to), reconstruct itinerary starting at JFK using all tickets once; choose lexicographically smallest.  
**Key idea:** Hierholzer algorithm for Eulerian path; keep outgoing edges sorted (min-heap or reverse-sorted list).  
**Pseudocode:**
```
for each airport: adj[airport] = min-heap of destinations
for (a,b) in tickets: adj[a].push(b)

route = []
dfs(a):
  while adj[a] not empty:
    b = pop smallest destination
    dfs(b)
  route.append(a)        // postorder

dfs("JFK")
reverse(route)
return route
```
**Important points:** Append in postorder then reverse; duplicates are multiple edges; lexicographic requires sorted adjacency.
