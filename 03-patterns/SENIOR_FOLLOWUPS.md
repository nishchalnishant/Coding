---
module: 03-patterns
topic: Senior Follow-Up Chains
tags: [patterns, senior, sde3, follow-ups]
---

# Senior Follow-Up Chains

> [!IMPORTANT]
> **How to use this file:** These are not new problems — they're the standard **third link** in a chain, attached by reference to existing T1/T2 bases from [`03-patterns/MOCK_INTERVIEW_SET.md`](MOCK_INTERVIEW_SET.md) and [`coding/l4-sde2-delta.md`](../coding/l4-sde2-delta.md). At senior level you should propose these escalations yourself before the interviewer asks. Full tier context: [`coding/sde3-senior-delta.md`](../coding/sde3-senior-delta.md).

---

## 1. Count-vs-existence

The cheapest senior escalation: "can you also tell me *how many*, not just whether one exists?" Existence checks (any/DFS-early-exit/binary search) often can't be trivially converted — the follow-up is graded on recognizing *when* the existing structure transfers and when it forces a rewrite.

| Base (existence) | Follow-up (count) | Does the structure transfer? |
|---|---|---|
| Word Search (does word exist) | Count all occurrences | Yes — remove early exit, sum instead of return |
| Number of Islands (are there islands) | Max Area of Island / count sizes | Yes — accumulate size during flood fill |
| Course Schedule (can finish) | Count all valid orderings | **No** — becomes combinatorial, needs different approach (backtracking or DP over bitmask, out of scope — say so) |
| Two Sum (does pair exist) | Count pairs summing to target | Yes — hashmap of counts instead of indices |

---

## 2. Streaming / online

Full base structures: [`coding/data-structures/10-heap.md`](../coding/data-structures/10-heap.md), [`coding/data-structures/14-design.md`](../coding/data-structures/14-design.md).

| Base (offline, all data upfront) | Streaming follow-up | Key insight |
|---|---|---|
| Kth Largest Element in an Array | Kth Largest in a Stream | Maintain a min-heap of size k; O(log k) per insert instead of full re-sort |
| Find Median of Two Sorted Arrays | Find Median from Data Stream | Two heaps (max-heap left, min-heap right), rebalance on insert |
| Merge Intervals | My Calendar I/II (bookings arrive online) | No global sort available — check overlap against existing intervals on each insert |
| Top K Frequent Elements | Top K Frequent in a stream (bounded memory) | Exact top-k needs full counts; unbounded stream forces approximate (count-min sketch) — name the trade-off |

---

## 3. Update-heavy / deletion-heavy

| Base (static or insert-only) | Follow-up | Key insight |
|---|---|---|
| Kth Largest in a Stream | Values can be corrected/removed later (Stock Price Fluctuation) | Heap doesn't support arbitrary deletion — use **lazy deletion**: pop-and-check against a "stale" hashmap when the top is read |
| LRU Cache | Support deleting a key besides eviction | Must unlink from DLL *and* remove from hashmap — same invariant, extra edge case (key not present) |
| Union-Find (static components) | Support disconnecting an edge | Classic union-find doesn't support split — say so; requires rebuild or a different structure (link-cut tree, out of scope) |

---

## 4. Memory-constrained

| Base | Follow-up | Key insight |
|---|---|---|
| Two Sum (hashmap, O(n) space) | What if array doesn't fit in memory? | Sort externally (or if sorted already) → two pointers, O(1) extra space, trade time for space |
| BFS shortest path (visited set) | Graph too large for a visited set in memory | Bidirectional BFS reduces frontier size; or bitset instead of hashset if node IDs are dense integers |
| Sliding Window Maximum (deque) | Window is huge, deque still bounded — note it already *is* memory-efficient (O(k)) | Good place to demonstrate you recognize when no further reduction is needed |

---

## 5. Concurrency discussion

**Discussion only — never implement.** State the shared mutable state, name the hazard, name the fix at a level of "which primitive," not code.

| Structure | Shared state | Hazard | Fix (name it, don't implement) |
|---|---|---|---|
| LRU/LFU Cache | hashmap + DLL | Two threads evict + insert concurrently → corrupted list | Coarse lock around get/put, or read-write lock if reads dominate |
| Rate limiter | request counter/window | Check-then-increment race lets two requests both pass the limit | Atomic compare-and-swap, or move counter to a single-threaded owner (actor model) |
| Producer-consumer (Design Hit Counter under load) | shared counter or queue | Lost updates | Blocking queue with internal lock, or atomic increment |

---

## 6. One-vs-all

| Base (one target) | Follow-up (all targets) | Key insight |
|---|---|---|
| Shortest path to a target node | Shortest path to *all* nodes | Already what BFS/Dijkstra compute — the follow-up is free if you didn't early-exit |
| Validate one BST | Count all ways to build a BST from n nodes | Different problem class (Catalan number / DP) — recognize it's not a tweak |
| Find one anagram substring | Find all anagram substrings (Find All Anagrams) | Same sliding window, don't return early — collect all valid start indices |

---

## 7. Scale-change (100x)

The reflex being tested: does a complexity-class change trigger an unprompted redesign proposal?

| Problem | At n ~ 10^4 | At n ~ 10^7–10^9 | What changes |
|---|---|---|---|
| Any O(n²) DP | Fine | Must reduce — look for O(n log n) reformulation (e.g. LIS via binary search) or state-space reduction | Approach swap, not micro-optimization |
| Any O(n log n) sort-based | Fine | Still fine, usually | Say so and move on — don't over-engineer |
| In-memory hashmap/set of all elements | Fine | May not fit in memory | External sort, streaming, or approximate structure (bloom filter / count-min sketch) |
| Recursive DFS | Fine | Stack overflow risk | Convert to iterative with an explicit stack |

---

## See Also

- [MOCK_INTERVIEW_SET.md](MOCK_INTERVIEW_SET.md) — base problem set + L4 follow-up chains this file extends
- [coding/sde3-senior-delta.md](../coding/sde3-senior-delta.md) — senior tier definitions and bar
- [tracking/weakness-log.md](../tracking/weakness-log.md) — log which chain link you failed on
