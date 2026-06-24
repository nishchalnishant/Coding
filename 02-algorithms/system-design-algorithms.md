---
module: 02-algorithms
topic: System Design Algorithms
subtopic: 
status: awareness-only
tags: [algorithms, system-design-algorithms]
---

← [Algorithms index](./README.md) · [Algorithm decision tree](./algorithm_tree.md)

> [!warning] **Amazon SDE-2 scope: awareness only.**
> These topics appear in system design discussions, not coding rounds. Do not drill implementations.

## Quick Reference

| Problem | Algorithm | Key property |
|---------|-----------|--------------|
| Count unique visitors at scale | HyperLogLog | ~2% error, O(log log n) space |
| Membership test with low false positive rate | Bloom Filter | No false negatives; no deletions |
| Top-K / frequency in stream | Count-Min Sketch + heap | Overestimates, never underestimates |
| Add/remove servers without reshuffling | Consistent Hashing + virtual nodes | Remaps only k/n keys on topology change |
| Leader election / log replication | Raft | Quorum = ⌊N/2⌋ + 1; tolerates minority failures |
| Replica diff detection | Merkle Tree | O(log n) to find differing blocks |
| Distributed membership propagation | Gossip / SWIM | O(log N) rounds to converge |
| Cross-service atomic transactions | SAGA | Compensating transactions; no global locks |
| API rate limiting | Token Bucket | Allows burst up to bucket capacity |

**System design soundbites:**
- "Unique count at scale → HyperLogLog; 2% error at ~1.5 KB per counter."
- "Consistent hashing with virtual nodes remaps k/n keys on change vs. full reshuffle."
- "SAGA over 2PC for cross-service transactions; 2PC blocks indefinitely on coordinator failure."
- "Bloom filter for cache pre-check; eliminate disk hits for keys that definitely don't exist."
