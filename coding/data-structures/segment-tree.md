---
tags: [coding, data-structures, segment-tree]
topic: Segment Tree
difficulty: awareness-only
---

# Segment Tree — Awareness Note

**Not tested at Amazon SDE-2.** You do not need to implement a segment tree in an Amazon coding round.

- A segment tree supports range queries (sum, min, max) and point updates in O(log n).
- Lazy propagation extends it to range updates in O(log n).
- If a range-query problem appears at SDE-2, the expected solution is usually a prefix sum array (O(n) build, O(1) query) or a Fenwick tree — not a segment tree.
- Full segment tree implementation lives in the archived Google prep track; see `coding/l3-google-roadmap.md` (archived).
