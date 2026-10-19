---
module: striver/32-beyond-the-sheet
lesson: 4
topic: Techniques toolbox — meet in the middle, sweep line, coordinate compression, reservoir sampling, randomisation (shuffle, quickselect, hashing), interactive/streaming patterns, design-a-data-structure recipes
source: beyond the A2Z sheet (enrichment)
tags: [striver, beyond-sheet, theory, meet-in-the-middle, sweep-line, reservoir-sampling, randomisation, design]
---
# 4. Techniques Toolbox

← [Advanced trees and graphs](03-advanced-trees-and-graphs-theory.md) · [Part 32 index](README.md) · Next → [Striver course map](../README.md)

> [!abstract] What this covers
> **Core idea:** These are cross-cutting tricks that don't belong to one data structure but show up in hard rounds and senior follow-ups:
> - halving an exponential search (meet in the middle)
> - turning intervals into sorted events (sweep line)
> - sampling a stream in O(1) memory (reservoir)
> - using randomness for expected-time guarantees
> - composing structures for "design X with O(1) ops"
>
> **You'll be able to:** recognise each trigger, write the core loop, and state its complexity.
> **Source:** not in the A2Z sheet. It pulls together Parts 13, 21, 22 and 26, plus [senior follow-ups](../../03-patterns/SENIOR_FOLLOWUPS.md). · **Time:** 50 min

**Sections:** [1. Meet in the middle](#1-meet-in-the-middle) · [2. Sweep line](#2-sweep-line) · [3. Coordinate compression](#3-coordinate-compression) · [4. Reservoir sampling](#4-reservoir-sampling) · [5. Randomisation](#5-randomisation) · [6. Streaming patterns](#6-streaming-patterns) · [7. Design recipes](#7-design-recipes)

---

## 1. Meet in the middle

**Trigger:** n ≈ 30–40 with subset enumeration, where 2ⁿ is too slow but 2^(n/2) ≈ 10⁶ is fine.

1. Split the items into halves A and B.
2. Enumerate the subset sums of each half: `SA` and `SB`, each of size 2^(n/2).
3. Sort `SB`. For each `x ∈ SA`, binary search for the best partner (closest to the target, or a count equal to the target).

| Problem | Combine step |
|---|---|
| Closest Subsequence Sum (LC 1755) | Two pointers over the sorted SA and SB |
| Partition into two equal-size arrays with min difference (LC 2035) | Group by subset size, then binary search |
| 4-sum count (LC 454) | Hashmap of the a+b sums, then look up −(c+d). O(n²) |

**Cost:** O(2^(n/2) · n).

---

## 2. Sweep line

Turn intervals into **events** (x, +1 for a start, −1 for an end), sort them and scan.

| Problem | Event / state | Tie rule |
|---|---|---|
| Meeting Rooms II (min rooms) | ±1, track the max running count | End before start if `[a, b)` intervals can share an endpoint |
| Car Pooling / max overlap | ±passengers | Same |
| Merge / insert intervals (Part 14) | Sort by start, extend the end | — |
| Skyline (LC 218) | Height events plus a max-heap or multiset of active heights | Starts tallest-first, ends shortest-first |
| Employee Free Time | Merge all intervals, report the gaps | — |
| Rectangle area union | x-sweep plus a segment tree over y | Senior level |
| Points covered by intervals | Difference array if the coordinates are small | — |

**Cost:** O(n log n) for the sort.

---

## 3. Coordinate compression

`vals = sorted(unique(all coordinates))` and `rank(x) = lower_bound(vals, x)`. Ranks map values as large as 10⁹ to 0..n−1. The relative order is preserved, so BITs, segment trees and difference arrays work on the ranks. Include **every** query coordinate before compressing.

---

## 4. Reservoir sampling

Use this to pick k uniform items from a stream of unknown length in O(k) memory:

```text
for i, x in enumerate(stream):             # i from 0
    if i < k: R[i] = x
    else:
        j = rand(0, i)                     # inclusive
        if j < k: R[j] = x
```

- **Proof sketch:** item i survives with probability `k/(i+1) · ∏ (1 − 1/(t+1))` over t > i, which telescopes to k/n.
- **Linked List Random Node (LC 382)** is the k = 1 case.
- **Random Pick Index (LC 398):** reservoir over the matching indices.
- **Weighted pick (LC 528):** prefix sums of the weights plus a binary search on `rand(1, total)`.

---

## 5. Randomisation

| Tool | Use | Guarantee |
|---|---|---|
| Fisher–Yates shuffle | `for i from n−1 down to 1: swap(a[i], a[rand(0, i)])` | All n! permutations are equally likely (LC 384) |
| Random pivot | Quickselect / quicksort (Part 13, Part 26 k-th largest) | Expected O(n) / O(n log n); avoids adversarial worst cases |
| Randomised hashing | Rolling-hash base, a randomised hash seed | Defeats anti-hash tests (Part 30) |
| Random sampling in a grid / rejection | rand7 → rand10 (LC 470) | Expected O(1) |
| Insert/Delete/GetRandom O(1) (LC 380) | Array + map from value to index; delete by swapping with the last | — |

---

## 6. Streaming patterns

| Ask | Structure |
|---|---|
| Running median | Two heaps (Part 26) |
| Top-k frequent over a stream | Count map plus a size-k min-heap; Count-Min Sketch + heap at scale |
| Moving average | Queue plus a running sum |
| Sliding window max | Monotonic deque (Part 23) |
| Distinct count at scale | HyperLogLog (approximate). Mention it only in a senior discussion |
| Approximate membership | Bloom filter: false positives possible, no false negatives |
| Data stream as disjoint intervals | Sorted map, merging with the neighbours |

See [SENIOR_FOLLOWUPS](../../03-patterns/SENIOR_FOLLOWUPS.md) for streaming and scale-change follow-up chains.

---

## 7. Design recipes

| Design | Composition | Ops |
|---|---|---|
| LRU cache (Part 19/26) | Hashmap + doubly linked list | O(1) get/put |
| LFU cache | key→node, freq→DLL, `minFreq` | O(1) |
| Min stack (Part 23) | Stack of (value, current min) | O(1) |
| Max frequency stack (LC 895) | freq map plus a map from freq to stack | O(1) |
| Time-based key-value store | Map of key → sorted (time, value), binary search | O(log n) get |
| All O(1) data structure (LC 432) | DLL of count buckets plus a key→bucket map | O(1) |
| Snapshot array | Per-index list of (snap, val), binary search | O(log s) |
| Autocomplete | Trie plus top-k at each node (Part 29) | O(prefix) |
| Rate limiter | Queue of timestamps (sliding log) or token bucket | O(1) amortised |

**Recipe:**
1. List the required operations and their target complexities.
2. Pick a primary structure for each operation.
3. Add cross-indexes (maps to nodes or positions) so the structures stay consistent.
4. Check every operation updates every structure.

---

## Common mistakes

| Mistake | Fix |
|---|---|
| Sweep-line tie order wrong | Decide whether touching intervals overlap, and sort ends before or after starts accordingly |
| Reservoir with `rand(0, i−1)` | Must be inclusive of i |
| Shuffle with `swap(a[i], a[rand(0, n−1)])` | Biased; use `rand(0, i)` |
| Compressing without the query values | Include every coordinate that will be looked up |
| GetRandom delete that leaves a hole | Swap with the last element and update its index in the map |

---

## Practice

<details><summary>1. n = 36 items, closest subset sum to T. Approach?</summary>

Meet in the middle: 2 × 2¹⁸ sums, sort one side, two pointers. Roughly 10⁷ operations.
</details>

<details><summary>2. Min meeting rooms for [0,30], [5,10], [15,20]?</summary>

2.
</details>

<details><summary>3. Uniformly random line from a 50 GB log in one pass?</summary>

Reservoir with k = 1: keep line i with probability 1/i.
</details>

<details><summary>4. Why must Fisher–Yates use rand(0, i)?</summary>

That gives n! equally likely execution paths, one per permutation. Using rand(0, n−1) gives nⁿ paths, which n! does not divide, so the result is biased.
</details>

---

## Key terms

| Term | Meaning |
|---|---|
| Meet in the middle | Split an exponential search into two halves and combine |
| Event | A (coordinate, delta) pair in a sweep |
| Reservoir | Fixed-size uniform sample of a stream |
| Las Vegas / Monte Carlo | Always correct with random time / fixed time with a random error |

---

## Flashcards

**Meet-in-the-middle trigger?** #flashcard
n ≈ 30–40 with a subset search. Enumerate 2^(n/2) per half, sort, then binary search or two pointers.

**Meeting Rooms II via sweep?** #flashcard
Sort ±1 events (ends first at ties) and take the max running sum.

**Reservoir rule for item i (0-indexed)?** #flashcard
j = rand(0, i); if j < k then replace R[j].

**Fisher–Yates loop?** #flashcard
For i from n−1 down to 1: swap(a[i], a[rand(0, i)]).

**Insert/Delete/GetRandom O(1)?** #flashcard
Array plus a value→index map. Delete by swapping with the last element and popping.

---

**Interview track →** [Senior follow-ups](../../03-patterns/SENIOR_FOLLOWUPS.md) · [Interview judgment](../../03-patterns/INTERVIEW_JUDGMENT.md)
