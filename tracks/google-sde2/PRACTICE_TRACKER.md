# Practice Tracker (Google SDE-2)

Use this to keep practice honest and targeted. The fastest improvement comes from redoing failures.

---

## Weekly checklist (copy each week)

- [ ] 3–5 timed sessions (45–60 min)
- [ ] 1–2 full mocks (2 problems); if you have both **virtual** and **in-person** DSA rounds, include **at least one** mock in each style (see [CODING_ROUNDS.md](CODING_ROUNDS.md))
- [ ] 1 system design run-through (30–45 min) **or**, if that round is not on your loop, 1 **AI / ML** discussion / outline (see [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md))
- [ ] 1 behavioral practice (record yourself once)
- [ ] Review and redo every "fail" from the week

---

## Mistake log (append-only)

For every failed or slow problem, log:

- Date:
- Problem:
- Pattern:
- Failure mode (pick one):
  - wrong DS choice
  - wrong invariant
  - off-by-one / bounds
  - recursion/base case
  - graph visited/state
  - complexity misunderstanding
  - implementation bug
- Fix / lesson (1–2 lines):
- Redo schedule:
  - [ ] same day
  - [ ] +2 days
  - [ ] +7 days

---

## "Cold redo" rubric (use on reattempts)

- Can I state the invariant in 15 seconds?
- Can I code it cleanly without "trial and error"?
- Can I produce 2 edge cases instantly?
- Can I state correct time/space?

---

## Mistake library — common failure modes by pattern

Use this to diagnose *why* you failed, not just *that* you failed.

### Arrays / prefix sums

| Mistake | Root cause | Fix |
|---------|-----------|-----|
| Sliding window breaks on negative numbers | Assumed shrinking window works; it doesn't with negatives | Switch to prefix-sum + hash map (Subarray Sum = K pattern) |
| Off-by-one in prefix array | `prefix[0] = 0`, `prefix[i] = prefix[i-1] + a[i-1]` vs `a[i]` | Always write the base case first; verify `prefix[1] - prefix[0] = a[0]` |
| Forgot to handle "subarray starting at index 0" | Missing `prefix[0] = 0` entry in hash map | Pre-insert `{0: -1}` or `{0: 1}` depending on count vs index |
| Product array: wrong zero handling | Two zeros means row stays 0; one zero means only that index gets non-zero | Count zeros separately; handle 0, 1, 2+ zeros as three cases |

### Two pointers

| Mistake | Root cause | Fix |
|---------|-----------|-----|
| 3Sum duplicate triplets | Didn't skip duplicates after fixing the outer element and after inner pointers converge | After outer loop: `while a[i]==a[i-1]: i++`. After match: skip both `lo` and `hi` |
| Container with water: moved wrong pointer | Moved the larger-height pointer | Always move the **smaller** height pointer — only raising the shorter side can increase area |
| Missed case where both pointers should advance | Only moved one pointer when both had equal values | On match or tie, sometimes advance both; depends on problem invariant |

### Sliding window

| Mistake | Root cause | Fix |
|---------|-----------|-----|
| Shrink condition wrong | Checked `while invalid` but "invalid" was defined wrong | Write the "valid window" condition explicitly before coding the shrink |
| Window size tracked incorrectly | Used `j - i` vs `j - i + 1` | Fixed-window: `j - i + 1 == k`; variable: length is `j - i + 1` at the valid moment |
| "At most K distinct" → "exactly K" | Forgot: exactly K = at_most(K) - at_most(K-1) | Memorize this reduction; it comes up in Subarrays with K Different Integers |

### Binary search

| Mistake | Root cause | Fix |
|---------|-----------|-----|
| Infinite loop | `lo = mid` instead of `lo = mid + 1` when converging | When you've confirmed mid is not the answer, always move lo or hi past mid |
| Wrong boundary for lower bound | Used `<=` when `<` needed or vice versa | Use template: `lo=0, hi=n, while lo<hi, mid=(lo+hi)//2, if pred(mid): hi=mid else: lo=mid+1` |
| Binary search on answer: predicate wrong | "Is mid feasible?" returns True/False incorrectly | Test predicate on small examples before coding the search |
| Rotated array: picked wrong half | Didn't check which half is sorted before deciding | First check `a[lo] <= a[mid]` (left half sorted), then decide; don't assume |

### Linked list

| Mistake | Root cause | Fix |
|---------|-----------|-----|
| Lost pointer during reverse | Overwrote `curr.next` before saving it | Always: `nxt = curr.next` → rewire → `curr = nxt` |
| Off-by-one in "remove Nth from end" | Fast pointer moved N times instead of N+1 | Move fast N+1 steps so slow lands on the node *before* the target |
| Floyd's cycle detection: found meeting point, not entry | Stopped at meeting point and returned it | After meeting: reset one pointer to head, advance both 1 step at a time until they meet — that's the entry |
| Merge lists: forgot to attach remainder | Loop exits when one list is done; forgot `curr.next = l1 or l2` | After while loop: `curr.next = l1 if l1 else l2` |

### Stack / monotonic

| Mistake | Root cause | Fix |
|---------|-----------|-----|
| Monotonic stack: stored values instead of indices | Can't compute width/span without the index | Always push indices; retrieve value via `a[stack[-1]]` |
| Histogram: forgot sentinel to flush remaining stack | Stack has leftovers after the loop | Append `0` to heights array to force-flush, or handle in post-loop |
| Width calculation wrong | Used `i - stack[-1]` vs `i - stack[-1] - 1` | After popping `h`, width = `i - stack[-1] - 1` (gap between current and new top) |

### Trees

| Mistake | Root cause | Fix |
|---------|-----------|-----|
| Validate BST: compared only with parent | Used `node.val > parent.val` — fails for ancestor constraints | Pass `(lo, hi)` bounds down recursively; `-inf` and `+inf` initially |
| Tree DP: returned gain but also updated global wrong | Used max(left,right,0) for gain but forgot the global uses left+right | Global update: `ans = max(ans, left_gain + right_gain + node.val)`. Return: `node.val + max(left_gain, right_gain, 0)` |
| LCA: returned None from wrong branch | If p and q are in same subtree, the other side returns None | Return non-None value when one side is None; return the node if it equals p or q |
| Level order: appended during wrong iteration | Mixed node processing and level boundary | Use `for _ in range(len(queue))` to process exactly one level per outer loop iteration |

### Graphs

| Mistake | Root cause | Fix |
|---------|-----------|-----|
| BFS: marked visited after dequeue instead of on enqueue | Same node gets enqueued multiple times → O(V²) or wrong count | Mark visited **when you enqueue**, not when you process |
| Topo sort: edge direction wrong | Modeled `course → prereq` instead of `prereq → course` | Redraw: `"take A before B"` = edge `A → B`; in-degree of B increases |
| Grid BFS: checked bounds after enqueue | Enqueued out-of-bounds cells and crashed | Check `0 <= r < rows and 0 <= c < cols` before enqueuing |
| Clone graph: didn't handle cycles | Revisited already-cloned nodes and created duplicates | Check `if node in visited: return visited[node]` at the top of DFS |
| Dijkstra: processed stale heap entries | Didn't skip entries where `dist > current best` | `if dist > dist_map[node]: continue` at the top of the heap-pop loop |

### Dynamic programming

| Mistake | Root cause | Fix |
|---------|-----------|-----|
| Coin change: wrong impossible sentinel | Used `float('inf')` but forgot that `INF + 1 = INF` in Python (fine) vs overflow in Java | In Java/C++: use `Integer.MAX_VALUE / 2` as sentinel; check before adding |
| LIS: confused O(n²) DP with O(n log n) patience | They return the same length but different structures | O(n log n) with `bisect_left` on `tails` gives length only; reconstruct with patience sorting if sequence needed |
| 2D DP: wrong base case (first row/col) | Left `dp[0][j]` or `dp[i][0]` uninitialized | Fill row 0 and col 0 before the main nested loop |
| Knapsack: used 1D but iterated wrong direction | Forward iteration re-uses items (unbounded); backward for 0/1 | 0/1 knapsack: iterate capacity from high to low. Unbounded: low to high |
| State explosion: stored too much in state | Modeled memo as `(i, j, k, l)` when `(i, j)` was enough | Ask: "what is the minimum information I need to determine future choices from this point?" |

### Backtracking

| Mistake | Root cause | Fix |
|---------|-----------|-----|
| Duplicates in subsets/permutations | Didn't sort + skip duplicates at the same recursion level | Sort input; in the loop: `if i > start and a[i] == a[i-1]: continue` |
| Shared mutable path | Appended to `path` and added `path` to result by reference | Use `result.append(path[:])` or `result.append(list(path))` |
| Combination sum: revisiting used elements in 0/1 variant | Passed `i` instead of `i+1` when reuse is not allowed | Reuse allowed: `dfs(i, ...)`. No reuse: `dfs(i+1, ...)` |

### Heaps

| Mistake | Root cause | Fix |
|---------|-----------|-----|
| Max heap in Python | Python only has min heap | Negate values: push `-x`, pop and negate result |
| Merge K lists: re-pushed None | Didn't check if `node.next` exists before pushing | `if node.next: heappush(heap, (node.next.val, idx, node.next))` |
| Top K frequent: K=len(nums) edge case | Didn't handle when K equals number of distinct elements | `heapq.nlargest(k, count.items(), key=lambda x: x[1])` handles this cleanly |

---

## Complexity red flags (memorize these)

| Pattern | Expected | If you wrote | Problem |
|---------|----------|-------------|---------|
| Two Sum (hash map) | O(n) | O(n²) | Using nested loop without hash |
| Sliding window | O(n) | O(n²) | Nested loop instead of shrink |
| BFS shortest path | O(V+E) | O(V²) | Adjacency matrix + visited array wrong |
| Topo sort | O(V+E) | O(V²) | Rebuilding queue each iteration |
| Merge K sorted lists | O(n log k) | O(nk) | Not using heap, just re-sorting |
| LIS | O(n log n) | O(n²) | Not using patience sorting / binary search |
| Subarray Sum = K | O(n) | O(n²) | Not using prefix-sum + hash map |
