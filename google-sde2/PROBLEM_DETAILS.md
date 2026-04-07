# Problem Details (Descriptions + Pseudocode) — Google SDE-2

This file expands every coding question mentioned in this folder into:
- a short **problem description**
- **pseudocode** for a standard interview solution

Notes:
- Titles are canonical; use any platform (LeetCode/EPI/etc.) to find the exact statement.
- Pseudocode uses generic helpers like `HashMap`, `Deque`, `Heap`, `DSU`.

---

## Arrays / Prefix Sums / Hashing

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

---

## Design-Heavy / Data Structures (Still Asked in Coding Rounds)

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

---

## Two Pointers

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

---

## Sliding Window

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

## Binary Search

### Find First and Last Position of Element
**Problem:** In sorted array, return first and last index of target.  
**Pseudocode:**
```
left = lower_bound(nums, target)          // first >= target
right = lower_bound(nums, target+epsilon) // first > target (or upper_bound)
if left == n or nums[left] != target: return [-1,-1]
return [left, right-1]
```

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

---

## Linked List

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

### LRU Cache
**Problem:** Design an LRU cache with O(1) get/put.  
**Pseudocode:**
```
map = HashMap(key -> node)
DLL with head/tail sentinels (most recent near head)
get(key):
  if key not in map: return -1
  move node to front
  return node.value
put(key,value):
  if key in map: update node.value; move node to front
  else:
    add new node at front; map[key]=node
    if size > capacity:
      lru = tail.prev
      remove lru from DLL; delete map[lru.key]
```

---

## Trees / BST

### Maximum Depth of Binary Tree
**Problem:** Return maximum depth (height) of a binary tree.  
**Pseudocode:**
```
dfs(node):
  if node == null: return 0
  return 1 + max(dfs(node.left), dfs(node.right))
return dfs(root)
```

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

---

## Graphs (BFS/DFS/Topo)

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

---

## Advanced Graphs (Occasionally in Google L4/L5)

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

---

## DP (Hard / Classic)

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

---

## Backtracking

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

---

## Union-Find

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

---

## Bit Manipulation

### Single Number
**Problem:** Every element appears twice except one; find the single.  
**Pseudocode:**
```
x=0
for v in nums: x = x XOR v
return x
```

### Counting Bits
**Problem:** For i=0..n, compute number of set bits in i.  
**Pseudocode:**
```
bits[0]=0
for i in [1..n]:
  bits[i] = bits[i>>1] + (i&1)
return bits
```

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

---

## Maths

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

---

## Sorting

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

---

## Concurrency (Sometimes appears as “coding” round)

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
