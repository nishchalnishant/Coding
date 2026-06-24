---
tags: [data-structures, sde2, amazon, audit]
topic: Amazon SDE-2 DSA Completeness Checklist
difficulty: reference
---

# Amazon SDE-2 Data Structures — Completeness Checklist

Use this to identify gaps before your loop. Check off each item when you can implement it from scratch in an interview setting.

---

## Arrays & Strings
- [ ] Two pointers — opposite ends (two sum sorted, container with most water)
- [ ] Two pointers — same direction / fast-slow (remove duplicates in-place)
- [ ] Sliding window — variable (longest substring without repeat, min window substring)
- [ ] Sliding window — fixed (find all anagrams)
- [ ] Prefix sum — range query (subarray sum equals K with hash map)
- [ ] Difference array — range update (apply many [l,r] increments, read final array)
- [ ] Kadane's algorithm — max subarray (init to nums[0], not 0)
- [ ] Dutch National Flag — 3-way partition (sort colors)
- [ ] Frequency map / counter — anagram, group anagrams, character substitution window

## Linked Lists
- [ ] Fast/slow pointer — cycle detection (Floyd's)
- [ ] Fast/slow pointer — find middle
- [ ] Fast/slow pointer — find cycle entry
- [ ] Reverse in-place — single linked list (three-pointer: prev, curr, next)
- [ ] Reverse in groups — reverse K groups iteratively
- [ ] Merge two sorted lists — dummy head technique
- [ ] Intersecting lists — equalize lengths, walk together
- [ ] LRU Cache — HashMap + doubly linked list, O(1) get/put

## Stacks
- [ ] Monotonic decreasing stack — next greater element, daily temperatures
- [ ] Monotonic increasing stack — next smaller element, largest rectangle in histogram
- [ ] Balanced parentheses — push open, pop and match on close
- [ ] Min stack — auxiliary stack tracking current min, O(1) getMin
- [ ] Evaluate RPN / infix-to-postfix

## Queues & Deque
- [ ] BFS — single source, level-order traversal
- [ ] Multi-source BFS — seed all sources at step 0 (rotting oranges, 0-1 matrix)
- [ ] Monotonic deque — sliding window maximum, O(N) total
- [ ] Implement queue with two stacks

## Hash Maps & Sets
- [ ] Complement lookup — two sum, three sum
- [ ] Frequency counting — valid anagram, top K frequent elements
- [ ] Grouping — group anagrams by sorted key or count tuple
- [ ] Prefix sum + map — subarray sum = K, subarray sum divisible by K
- [ ] Set for O(1) membership — longest consecutive sequence

## Trees (Binary Tree + BST)
- [ ] Inorder traversal — recursive and iterative
- [ ] Preorder traversal — recursive and iterative
- [ ] Postorder traversal — recursive and iterative
- [ ] Level-order (BFS) — with and without level separators
- [ ] Tree depth / height — recursive post-order
- [ ] Diameter of binary tree — post-order, pass height up
- [ ] LCA of binary tree — recursive, null-bubbling
- [ ] LCA of BST — use BST property to navigate
- [ ] Validate BST — pass (min, max) bounds down recursively
- [ ] Path sum problems — root-to-leaf, any path (use signed carry)
- [ ] Serialize / deserialize — preorder + null markers
- [ ] BST insert, delete, search — O(h) each
- [ ] Convert sorted array to balanced BST — mid as root, recurse

## Heaps / Priority Queues
- [ ] Top-K largest — min-heap of size K, O(N log K)
- [ ] Top-K smallest — max-heap of size K
- [ ] Merge K sorted lists — min-heap of (value, list_index, element_index)
- [ ] Median of stream — max-heap (lower half) + min-heap (upper half)
- [ ] Task scheduling / CPU scheduling (LC 621) — frequency-based greedy with heap

## Tries
- [ ] Insert, search, startsWith — TrieNode with children dict + is_end flag
- [ ] Word search II — Trie + DFS backtracking on grid
- [ ] Replace words / shortest root — trie for prefix lookup
- [ ] Word break — BFS/DP aided by trie for fast prefix check

## Graphs (representation only; algorithms live in 02-algorithms/)
- [ ] Build adjacency list from edge list — defaultdict(list)
- [ ] Build adjacency list from grid — implicit 4-directional neighbors
- [ ] Adjacency matrix vs list trade-offs — when to use each
- [ ] Understand in-degree / out-degree for directed graphs

---

## What is NOT needed at SDE-2

| Structure | Why skip |
|-----------|----------|
| Segment trees | Competitive programming / SDE-3 only |
| Fenwick / BIT | Same; prefix-sum covers SDE-2 range query cases |
| Persistent data structures | SDE-3 and above |
| Treaps, skip lists | Implementation depth not expected; know they exist |
| AVL / Red-Black tree implementation | Know they exist and guarantee O(log N); no coding |
| Aho-Corasick, suffix arrays | SDE-3+ string matching depth |

---

## Gaps most commonly missed at SDE-2

1. **LRU cache** — many candidates know the concept but fumble the DLL + HashMap combination under time pressure. Practice until it's automatic.
2. **Reverse K groups** — iterative pointer surgery; common follow-up to linked list reversal.
3. **Median of stream** — two-heap balancing logic (when left > right, push to right and pop back to left).
4. **Multi-source BFS** — forgetting to seed all sources simultaneously at step 0 gives wrong shortest distances.
5. **BST LCA vs Binary Tree LCA** — different algorithms; mixing them up under pressure is common.
6. **Sliding window with exact-K constraint** — use `atMost(K) - atMost(K-1)`, not a direct window.
