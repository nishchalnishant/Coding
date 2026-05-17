# SDE Interview Click Logic: Pattern Recognition Master Hub

Identify the underlying DSA pattern within 60 seconds. Focus on the trigger, not the full solution.

---

## 0. The Big Tech Evaluator Mindset
Interviewers at Google/Meta aren't just looking for a "Passed" result. They evaluate:
- **Problem Solving**: Can you optimize from O(N²) to O(N log N)?
- **Communication**: Do you state your assumptions and invariants?
- **Code Quality**: Are your indices clean? Do you handle `empty` and `null`?
- **Speed**: Can you reach the "Click Moment" in under 60 seconds?

---

## 1. The "Click" by Constraint (Input Size N)

Constraints are the biggest hint the interviewer gives you.

| Constraint | Expected Complexity | Likely Pattern |
| :--- | :--- | :--- |
| N <= 10 | O(N!) | Permutations, Travelling Salesman |
| N <= 20 | O(2^N) | Backtracking, Subsets, Bitmask DP |
| N <= 500 | O(N^3) | Floyd-Warshall, 3D DP, Interval DP (Burst Balloons) |
| N <= 2000 | O(N^2) | 2D DP, Nested Loops, Matrix pathfinding |
| N <= 10^5 | O(N log N) or O(N) | Sorting, Binary Search, Heaps, Two Pointers, Sliding Window |
| N <= 10^6 | O(N) or O(log N) | Single pass, Greedy, Math, Binary Search |

---

## 2. The "Click" by Keyword

| If you hear/see... | It almost always means... | Why? |
| :--- | :--- | :--- |
| **"Contiguous subarray"** | Sliding Window / Prefix Sum | Window covers a range; prefix sum calculates any range in O(1) |
| **"Subsequence"** | DP (take/skip) / LIS | Elements aren't contiguous; decide for each element |
| **"Sorted array"** | Binary Search / Two Pointers | Sorting enables O(log N) or O(N) search/convergence |
| **"Top K / Frequent"** | Heap / Hash Map | Map counts frequency; heap maintains top order dynamically |
| **"Dependencies / Ordering"** | Topological Sort (DAG) | Node A must happen before Node B |
| **"Shortest path" (unweighted)** | BFS | BFS explores layers equally; first hit = shortest |
| **"Shortest path" (weighted)** | Dijkstra | Priority queue always expands cheapest known node |
| **"Maximize the minimum"** | Binary Search on Answer | Guess a limit, check feasibility (monotonicity) |
| **"All possible ways"** | Backtracking (list) / DP (count) | Backtrack to enumerate; DP if you only need the count |
| **"Subarray sum = K"** | Prefix Sum + Hash Map | `prefix_count[running_sum - K]` gives count of valid subarrays |
| **"Next greater/smaller"** | Monotonic Stack | Store indices; pop while current element breaks monotonicity |
| **"Connectivity / cycles"** | Union-Find | Union two nodes; find detects if already connected (cycle) |
| **"Stream / running median"** | Two Heaps | Max-heap (lower half) + min-heap (upper half); rebalance to size diff <= 1 |
| **"Kth smallest in sorted matrix"** | Min-Heap or Binary Search on Answer | Binary search on value range; count elements <= mid |

---

## 3. The "If-Not-X-Then-Y" Logic

Use this to pivot when your first idea is too slow.

- **Array, O(N^2) is too slow:**
  - Hash Map (trade space for time)
  - Sort first, then Two Pointers
  - Sliding Window (if contiguous)
  - Prefix Sums
- **Tree problem, stuck:**
  - Answer depends on children? → Post-order (Tree DP)
  - Need to pass info down? → Pre-order with state variable
- **Graph, weights are 0 or 1:**
  - Skip Dijkstra; use BFS or 0-1 BFS (deque) for O(V+E)
- **DP state too large:**
  - Reduce 2D to 1D (space optimization — only previous row needed)
  - Is N small (<= 20)? → Bitmask DP
- **Can't find DP recurrence:**
  - Try greedy (prove exchange argument)
  - Try binary search on answer + feasibility check

---

## 4. Mental Models: The "Shift"

Rephrase the problem into a canonical one you already know:

| Problem phrasing | Canonical form |
|-----------------|----------------|
| "Meeting rooms — can all fit?" | Merge Intervals |
| "Meeting rooms — minimum rooms needed?" | Intervals + sort by start; min-heap of end times |
| "Word transformation: ladders" | BFS on graph (words = nodes, 1-char diff = edge) |
| "Assigning tasks to workers" | Bin packing (backtracking/bitmask) or flow (advanced) |
| "Collecting gold in a grid" | 2D DP pathfinding |
| "Next greater temperature" | Monotonic Stack |
| "Group words by same letters" | Sorted string as hash key (anagram grouping) |
| "Earliest time all nodes connected" | Union-Find + sort edges by weight (Kruskal) |

---

## 5. 60-Second Blitz: Clarifying Questions

Before writing a single line of code, ask:

1. **Duplicates?** — affects hash map/set logic and deduplication in backtracking
2. **Sorted?** — enables binary search, two pointers
3. **Empty / null input?** — base case for recursion, pointer init
4. **Memory constraints?** — O(1) space may be required
5. **Negative values?** — breaks naive sliding window (use prefix sum), breaks Dijkstra

---

## 6. Critical Gotchas (Last-Minute Check)

| Gotcha | Rule |
|--------|------|
| Sliding window + negatives | Can't shrink window on negatives; use prefix sum + map instead |
| Duplicates in backtracking | `if i > start and nums[i] == nums[i-1]: continue` |
| Binary search mid overflow | `mid = lo + (hi - lo) // 2`, not `(lo + hi) // 2` |
| BFS visited mark | Mark visited **when enqueuing**, not when dequeuing — prevents duplicates in queue |
| Topo sort cycle detection | If processed nodes < total nodes after Kahn's, there's a cycle |
| Tree DP return vs global | Return the single-arm gain upward; update global max with both arms at current node |
| Dijkstra with negative edges | Does not work — use Bellman-Ford |
---

## 7. Complexity & Communication Sound Bites

### Complexity Sound Bites
- **DFS/BFS**: "We visit each node and edge exactly once, so the time complexity is O(V + E)."
- **Sorting**: "The sorting step dominates the complexity, resulting in O(N log N)."
- **Hash Map**: "Using a hash map allows for O(1) average lookup, bringing the overall time to O(N)."
- **Binary Search on Answer**: "We perform O(log Range) checks, each taking O(N) time, for a total of O(N log Range)."

### The 4-Step Communication Template
1. **Clarify**: "Let me restate: we need to find X. Can the input be empty? Are there duplicates?"
2. **Brute Force**: "A naive O(N²) approach would be... but we can do better by..."
3. **Optimized Logic**: "I'll use a [Pattern] because it allows us to [Action] in O(N) time."
4. **Dry Run**: "Let's trace this with a small case: `[1, 2, 3]`. At step 1, `left` is 0..."

---

## 8. Final Edge Case Checklist
- [ ] **Empty/Null**: `if not nums: return`
- [ ] **Single Element**: Does your window logic handle `len=1`?
- [ ] **Duplicates**: Did you sort and skip?
- [ ] **Negatives**: Does your sliding window break? (Use prefix sum instead).
- [ ] **Overflow**: `mid = lo + (hi - lo) // 2`.
