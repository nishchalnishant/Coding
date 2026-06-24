---
module: 01-data-structures
topic: Segment Tree
status: awareness-only
tags: [data-structures, segment-tree]
---

← [Data structures index](./README.md)

# Segment Tree — Awareness Only

> **Not tested at Amazon SDE-2.** Do not spend implementation time here.

**What it is**: A binary tree where each node stores the aggregate (sum/min/max) of a contiguous array range. Build is O(N); point update and range query are both O(log N). Range updates require lazy propagation.

**When it appears**: Range query + point/range update on a mutable array when a prefix sum (static) is insufficient. Primarily a competitive programming / SDE-3 topic.

**Alternative for SDE-2**: If the data is static, use a prefix sum array (O(N) build, O(1) query). If you need range sum + point update at SDE-2 level, a Fenwick tree is simpler — but this scenario is rare at SDE-2.
