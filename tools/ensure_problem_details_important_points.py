#!/usr/bin/env python3
"""
Ensure every problem section in google-sde2/PROBLEM_DETAILS.md contains an
`**Important points:**` block.

Design goals:
- deterministic, repo-local (no network)
- minimal diffs: only touch sections that are missing Important points
- human-friendly bullets (revision-focused)
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple


CATALOG_PATH = Path("google-sde2/PROBLEM_DETAILS.md")


def _bullets(*items: str) -> List[str]:
    return [i.strip() for i in items if i and i.strip()]


IMPORTANT_POINTS: Dict[str, List[str]] = {
    # Arrays / Hashing / Prefix sums
    "Two Sum": _bullets(
        "Check-before-store to avoid using the same element twice (when target = 2*x).",
        "Time O(n), space O(n) with `value -> index` hash map.",
        "If multiple answers exist, the first found is fine unless asked otherwise.",
    ),
    "Subarray Sum Equals K": _bullets(
        "Works with negative numbers because it counts prefix-sum frequencies (not a sliding window).",
        "Seed `countByPrefix[0] = 1` to count subarrays starting at index 0.",
        "Use 64-bit for prefix sums if values can be large.",
    ),
    "Product of Array Except Self": _bullets(
        "Two passes: prefix products then suffix products; avoids division and handles zeros naturally.",
        "Extra space O(1) excluding output array.",
        "Watch overflow in languages with 32-bit ints if constraints are large.",
    ),
    "Maximum Subarray (Kadane)": _bullets(
        "Define invariant: `cur` is best sum of a subarray ending at i; reset when extending hurts.",
        "Must handle all-negative arrays (initialize to nums[0], not 0).",
        "Time O(n), space O(1).",
    ),
    "Maximum Subarray": _bullets(
        "Alias for Kadane; same invariants and edge cases (all-negative).",
    ),
    "Merge Intervals": _bullets(
        "Sort by start; merge by extending the last interval’s end.",
        "Be explicit about overlap rule (typically `next.start <= cur.end`).",
        "Time O(n log n) for sorting; scan is linear.",
    ),
    "Insert Interval": _bullets(
        "Three phases: add left (non-overlapping), merge overlaps, add right.",
        "In-place merge by expanding `newInterval` as long as it overlaps.",
        "Time O(n), space O(n) for output.",
    ),
    "Next Permutation": _bullets(
        "Pivot is the first index from the right where `a[i] < a[i+1]`.",
        "Swap pivot with the smallest number greater than it in the suffix (scan from right).",
        "Reverse suffix to get the minimal next permutation.",
    ),
    "Majority Element": _bullets(
        "Boyer–Moore finds a candidate in O(n) / O(1); relies on a guaranteed majority.",
        "If majority is not guaranteed, add a second pass to verify the candidate.",
    ),
    # Design-heavy
    "LRU Cache": _bullets(
        "Use `HashMap(key -> node)` + doubly linked list for O(1) get/put/move/evict.",
        "On both `get` and `put(existingKey)`, move the node to MRU position.",
        "Sentinel head/tail nodes remove null-edge cases.",
    ),
    "LFU Cache": _bullets(
        "Maintain `freq -> DLL` plus `minFreq` so eviction is O(1).",
        "On access, move node from freq f to f+1 and update `minFreq` when a bucket empties.",
        "Tie-break within same freq by LRU ordering inside each freq-list.",
    ),
    "Rate Limiter": _bullets(
        "Know common implementations: fixed window, sliding window log, sliding window counter, token bucket.",
        "Clarify requirements: per-user vs global, distributed vs single node, burstiness, and correctness vs latency.",
        "In distributed setups, discuss shared state (Redis) and clock skew / eventual consistency.",
    ),
    # Two pointers / sorting
    "3Sum": _bullets(
        "Sort then fix i; use two pointers on the suffix; skip duplicates for i/left/right.",
        "Early break when `nums[i] > 0` (after sorting) if target is 0.",
        "Time O(n^2); space O(1) extra (excluding output).",
    ),
    "Container With Most Water": _bullets(
        "Two pointers; move the shorter side because area is limited by min(height[l], height[r]).",
        "Proof idea: moving the taller side cannot increase the limiting height.",
        "Time O(n), space O(1).",
    ),
    "Trapping Rain Water": _bullets(
        "Two-pointer variant maintains `leftMax`/`rightMax`; fill based on the smaller bound.",
        "Alternative: monotonic stack for ‘next greater’ boundaries.",
        "Time O(n), space O(1) (two-pointer) or O(n) (stack).",
    ),
    "Remove Duplicates from Sorted Array": _bullets(
        "Slow/fast pointers; slow tracks next write position for unique values.",
        "Works because input is sorted; for unsorted you need a set/map.",
        "Return new length; elements beyond it are irrelevant.",
    ),
    "Sort Colors (Dutch Flag)": _bullets(
        "`low..mid-1` are 0s, `mid..high` unknown, `high+1..end` are 2s.",
        "When swapping with `high`, do not increment `mid` (needs re-check).",
        "One pass O(n), in-place O(1).",
    ),
    "Sort Colors": _bullets(
        "Alias for Dutch National Flag; same invariants about `low/mid/high`.",
    ),
    # Sliding window
    "Longest Substring Without Repeating Characters": _bullets(
        "Maintain a window with last-seen indices; move left with `left = max(left, last[c]+1)`.",
        "Store indices, not just counts, to jump left efficiently.",
        "Time O(n), space O(min(n, alphabet)).",
    ),
    "Longest Substring Without Repeating": _bullets(
        "Alias for the standard ‘no repeating characters’ sliding window (use last index jump).",
    ),
    "Longest Repeating Character Replacement": _bullets(
        "Track `maxFreq` of any char in the window; window valid if `len - maxFreq <= k`.",
        "`maxFreq` can be stale (not decreased) and correctness still holds; avoids O(σ) recompute.",
        "Time O(n), space O(σ).",
    ),
    "Minimum Window Substring": _bullets(
        "Need counts: `needCount` and `haveCount`, plus `formed` vs `required` distinct chars.",
        "Shrink left while valid to minimize; update best when valid.",
        "Time O(n) with two pointers; careful with repeated letters in `t`.",
    ),
    "Find All Anagrams in a String": _bullets(
        "Fixed-size window of length |p| with char counts; slide one step at a time.",
        "Optimize by tracking a ‘matches’ counter instead of comparing full maps each time.",
        "Time O(n), space O(σ).",
    ),
    "Sliding Window Maximum": _bullets(
        "Monotonic deque of indices; values decreasing from front to back.",
        "Pop front when index is out of window; pop back while new value is larger.",
        "Each index pushed/popped once → O(n).",
    ),
    "Implement strStr / KMP": _bullets(
        "Build LPS/prefix function for pattern; use it to avoid re-checking characters.",
        "Time O(n+m); handles overlaps like pattern `abab` correctly.",
        "Edge cases: empty needle, single char, repeated chars.",
    ),
    # Binary search
    "Find First and Last Position of Element": _bullets(
        "Do two binary searches: lower_bound(target) and lower_bound(target+ε)-1 (or upper_bound-1).",
        "Always write invariant-based templates to avoid off-by-one bugs.",
        "If lower_bound points outside array or not equal to target, target is absent.",
    ),
    "Lower/Upper Bound": _bullets(
        "Lower bound: first index with `a[i] >= x`; upper bound: first with `a[i] > x`.",
        "Prefer half-open intervals `[lo, hi)` to keep invariants clean.",
        "Works on monotonic predicate functions for ‘search on answer’ problems.",
    ),
    "Search in Rotated Sorted Array": _bullets(
        "At each step, one half is sorted; decide which half to keep based on target range.",
        "Assumes no duplicates; duplicates require extra handling and can degrade to O(n).",
        "Time O(log n).",
    ),
    "Find Minimum in Rotated Sorted Array": _bullets(
        "Compare `mid` with `right`: if `a[mid] > a[right]`, min is right half; else left half.",
        "Assumes no duplicates; with duplicates, shrink boundaries cautiously.",
        "Time O(log n).",
    ),
    "Koko Eating Bananas": _bullets(
        "Binary search on speed k; predicate `canFinish(k)` is monotone decreasing.",
        "Use ceiling division `hours += (pile + k - 1) // k`.",
        "Bounds: `lo=1`, `hi=max(piles)`.",
    ),
    "Koko Eating Bananas (Search on Answer)": _bullets(
        "Alias: standard ‘binary search on answer’ with a monotone feasibility predicate.",
    ),
    "Split Array Largest Sum": _bullets(
        "Binary search the minimal possible maximum subarray sum.",
        "Greedy check: count partitions by cutting when running sum would exceed `mid`.",
        "Time O(n log(sumRange)).",
    ),
    "Median of Two Sorted Arrays": _bullets(
        "Binary search on partition of the smaller array; enforce `leftMax <= rightMin`.",
        "Handle edges with ±∞ when partition touches ends.",
        "Time O(log min(m, n)); common off-by-one source—test tiny arrays.",
    ),
    # Stack
    "Valid Parentheses": _bullets(
        "Stack of opening brackets; pop and match on closing.",
        "Reject early when stack empty on closing; stack must be empty at end.",
        "Time O(n), space O(n).",
    ),
    "Decode String": _bullets(
        "Use stacks: one for repeat counts, one for previous string builders.",
        "Parse multi-digit numbers; on `]`, pop count and concatenate.",
        "Beware nested encodings and empty substrings.",
    ),
    "Daily Temperatures": _bullets(
        "Monotonic decreasing stack of indices; when a warmer temp arrives, resolve previous indices.",
        "Each index pushed/popped once → O(n).",
        "Store indices (not values) to compute day differences.",
    ),
    "Largest Rectangle in Histogram": _bullets(
        "Monotonic increasing stack of indices; compute area when current height breaks monotonicity.",
        "Use sentinel 0 height at end to flush the stack.",
        "Width uses next smaller on right and previous smaller on left.",
    ),
    "Largest Rectangle Histogram": _bullets(
        "Alias for ‘Largest Rectangle in Histogram’; same monotonic stack + sentinel trick.",
    ),
    "Evaluate Reverse Polish Notation": _bullets(
        "Use a stack; on operator pop `b` then `a` and push `a op b` (order matters).",
        "Define integer division behavior (typically truncate toward zero).",
        "Time O(n).",
    ),
    # Linked list
    "Reverse Linked List": _bullets(
        "Iterative pointer flip: keep `prev`, `cur`, `next`.",
        "Don’t lose the remainder: store `next` before rewiring.",
        "Time O(n), space O(1).",
    ),
    "Linked List Cycle II": _bullets(
        "Floyd’s tortoise/hare to find meeting point; then reset one pointer to head to find entry.",
        "Proof uses distance equations; works with O(1) space.",
        "Handle no-cycle case cleanly.",
    ),
    "Cycle II": _bullets(
        "Alias for ‘Linked List Cycle II’; same Floyd entry-finding step.",
    ),
    "Copy List with Random Pointer": _bullets(
        "Either use a map `old -> new` (simple) or interweave nodes (O(1) extra).",
        "When mapping, create nodes lazily so `random/next` pointers always resolve.",
        "Be careful with null random pointers.",
    ),
    "Merge Two Sorted Lists": _bullets(
        "Use a dummy head and stitch by picking the smaller head each step.",
        "Stable merge: if equal, either order is fine unless specified.",
        "Time O(m+n), space O(1).",
    ),
    "Remove Nth From End": _bullets(
        "Use a dummy head; advance `fast` by n+1 then move both pointers.",
        "When `fast` hits null, `slow.next` is the node to delete.",
        "Covers deleting the head cleanly via dummy.",
    ),
    # Trees / BST
    "Maximum Depth of Binary Tree": _bullets(
        "DFS recursion: `1 + max(left, right)`; BFS level-order also works.",
        "For very deep trees, iterative avoids recursion depth limits.",
        "Time O(n), space O(h) recursion stack.",
    ),
    "Validate BST": _bullets(
        "Use bounds recursion (`low < val < high`) or inorder strictly increasing sequence.",
        "Use 64-bit bounds to avoid overflow at int limits.",
        "Duplicates: clarify whether allowed; typical LeetCode requires strict ordering.",
    ),
    "Lowest Common Ancestor (BST + general)": _bullets(
        "BST: walk down using value comparisons; general tree: postorder recursion returning matches.",
        "In general tree, if both sides return non-null, current node is LCA.",
        "Clarify if both nodes are guaranteed to exist in the tree.",
    ),
    "Lowest Common Ancestor (BST)": _bullets(
        "BST-specific: if both targets < root go left; if both > root go right; else root is LCA.",
        "Time O(h), space O(1) iterative.",
    ),
    "LCA (binary tree)": _bullets(
        "General binary tree: postorder recursion; return node if it matches p/q or is LCA.",
        "Time O(n); recursion stack O(h).",
        "If nodes may be missing, track found flags to validate.",
    ),
    "Binary Tree Level Order Traversal": _bullets(
        "Queue BFS; process `levelSize` nodes per level to group outputs.",
        "Time O(n), space O(width).",
    ),
    "Kth Smallest in BST": _bullets(
        "Inorder traversal visits nodes in sorted order; stop when count reaches k.",
        "Iterative stack avoids recursion depth issues.",
        "If updates are frequent, discuss augmenting nodes with subtree sizes.",
    ),
    "Binary Tree Maximum Path Sum": _bullets(
        "Postorder: return max gain to parent (`max(0, leftGain, rightGain) + val`).",
        "Global answer considers splitting at node: `val + leftGain + rightGain`.",
        "Must handle all-negative trees (initialize best to -inf).",
    ),
    "Max Path Sum": _bullets(
        "Alias for ‘Binary Tree Maximum Path Sum’; same gain-vs-global split logic.",
    ),
    "Serialize and Deserialize Binary Tree": _bullets(
        "Pick a traversal (preorder/BFS) and include null markers to preserve structure.",
        "Deserialize must consume tokens in the same order; recursion is simplest for preorder.",
        "Define separators and handle empty tree.",
    ),
    "Serialize / Deserialize Binary Tree": _bullets(
        "Alias for ‘Serialize and Deserialize Binary Tree’; keep traversal + null markers consistent.",
    ),
    "Serialize/Deserialize": _bullets(
        "Alias for binary tree serialize/deserialize; emphasize null markers and order consistency.",
    ),
    # Graphs
    "Number of Islands": _bullets(
        "DFS/BFS flood-fill; mark visited (or mutate grid to ‘0’) to avoid revisits.",
        "Time O(R*C); recursion depth can be large—iterative BFS is safer.",
    ),
    "Alien Dictionary": _bullets(
        "Build edges from first differing char in adjacent words; invalid if prefix order violated (e.g., `abc` before `ab`).",
        "Topological sort (Kahn/DFS) with cycle detection.",
        "Multiple valid orders possible; return any unless specified.",
    ),
    "Rotting Oranges": _bullets(
        "Multi-source BFS from all rotten oranges simultaneously; each level = 1 minute.",
        "Track fresh count; if any remain at end, return -1.",
        "Time O(R*C).",
    ),
    "Course Schedule": _bullets(
        "Detect cycle in directed graph via Kahn’s algorithm (indegree) or DFS colors.",
        "If processed nodes == n, schedule possible; else cycle exists.",
        "Time O(V+E).",
    ),
    "Course Schedule (Topo + cycle)": _bullets(
        "Alias: topological sort + cycle detection (Kahn or DFS colors).",
    ),
    "Clone Graph": _bullets(
        "BFS/DFS with a map `original -> clone` to avoid duplicating nodes and to handle cycles.",
        "Create clone nodes lazily when first seen.",
        "Time O(V+E).",
    ),
    "Word Ladder": _bullets(
        "BFS for shortest path in unweighted graph; consider bidirectional BFS for speed.",
        "Precompute generic patterns (`h*t`) to find neighbors efficiently.",
        "Mark visited per level to avoid revisiting and to preserve shortest distance.",
    ),
    "Cheapest Flights Within K Stops": _bullets(
        "Common safe approach: Bellman–Ford limited to k+1 edges (k stops).",
        "If using a PQ, state must include stops; classic Dijkstra alone isn’t sufficient with stop limits.",
        "Time O(k*E) for BF; good for interview clarity.",
    ),
    "Network Delay Time (Dijkstra)": _bullets(
        "Dijkstra with min-heap; skip outdated heap entries when `d > dist[u]`.",
        "Requires non-negative weights.",
        "Answer is `max(dist)` if all reachable else -1.",
    ),
    "Network Delay Time": _bullets(
        "Alias: Dijkstra on directed weighted graph with non-negative edges.",
    ),
    "Dijkstra": _bullets(
        "Min-heap of (dist, node); relax edges; skip stale entries for performance.",
        "Only valid with non-negative edge weights.",
        "Time O((V+E) log V) with adjacency list.",
    ),
    "Critical Connections (Bridges)": _bullets(
        "Tarjan’s algorithm: track discovery time and low-link values in DFS.",
        "Edge (u,v) is a bridge if `low[v] > disc[u]`.",
        "Undirected graph; watch parent edge handling.",
    ),
    # Heaps / streaming
    "Top K Frequent Elements": _bullets(
        "Count with hash map; then use min-heap of size k (or bucket sort).",
        "Heap approach: O(n log k); bucket: O(n) time and space.",
        "Clarify if output order matters (usually not).",
    ),
    "Merge K Sorted Lists": _bullets(
        "Min-heap of current list heads; pop smallest and push its next.",
        "Time O(N log k) where N is total nodes; heap holds up to k nodes.",
        "Alternative divide-and-conquer merge is also O(N log k).",
    ),
    "Find Median from Data Stream": _bullets(
        "Two heaps: max-heap for lower half, min-heap for upper half.",
        "Maintain size invariant (difference ≤ 1) and ordering invariant (maxLower ≤ minUpper).",
        "Median from heap tops; O(log n) per insert.",
    ),
    # DP
    "House Robber": _bullets(
        "DP: `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`.",
        "Space optimize to two variables (prev1, prev2).",
        "Edge cases: empty, single house.",
    ),
    "Coin Change (min)": _bullets(
        "Unbounded knapsack DP on amount: `dp[a] = min(dp[a], dp[a-coin]+1)`.",
        "Initialize dp with INF and dp[0]=0; unreachable amounts remain INF.",
        "Time O(amount * #coins).",
    ),
    "Coin Change": _bullets(
        "Alias for min-coin DP; distinguish from ‘number of ways’ variant.",
    ),
    "Longest Increasing Subsequence": _bullets(
        "Patience sorting: maintain `tails[len] = min tail value` and binary search updates.",
        "Gives length in O(n log n); reconstructing sequence needs parent pointers.",
        "For strict vs non-decreasing LIS, adjust binary search (lower vs upper bound).",
    ),
    "LIS": _bullets(
        "Alias for ‘Longest Increasing Subsequence’; mention patience sorting + strictness choice.",
    ),
    "Longest Common Subsequence": _bullets(
        "Classic 2D DP on prefixes; `dp[i][j]` length for first i and first j chars.",
        "Space optimize to 2 rows if only length needed.",
        "Don’t confuse with substring (contiguous) which uses different DP.",
    ),
    "Edit Distance": _bullets(
        "DP with operations: insert/delete/replace; base cases `dp[i][0]=i`, `dp[0][j]=j`.",
        "Transition uses min of 3 neighbors; if chars match, take diagonal.",
        "Space optimize to 2 rows for length only.",
    ),
    "LCS / Edit Distance": _bullets(
        "Alias entry: know both DP tables and how transitions differ (match vs edit ops).",
    ),
    "Word Break": _bullets(
        "Boolean DP: `dp[i]=True` if some `dp[j]` and `s[j:i]` in dict.",
        "Optimize by limiting j to max word length; use a hash set for O(1) lookup.",
        "Worst-case O(n^2) substrings; mention trie optimization if asked.",
    ),
    "Regular Expression Matching": _bullets(
        "DP on i,j for s-prefix and p-prefix; `*` means zero or more of previous token.",
        "For `*`, consider: skip token (`dp[i][j-2]`) or consume one char if matches (`dp[i-1][j]`).",
        "Edge cases: patterns like `a*`, leading `*` (usually invalid), empty strings.",
    ),
    "The Skyline Problem": _bullets(
        "Sweep line over x with start/end events; maintain active heights in a max-heap + counter map.",
        "Be careful about event ordering at same x (starts before ends; higher starts first).",
        "Lazy deletions keep heap operations amortized efficient.",
    ),
    "Longest Valid Parentheses": _bullets(
        "Stack of indices with a base `-1`; on ')' pop and update length as `i - stack.top`.",
        "When stack becomes empty after pop, push current index as new base.",
        "Alternative DP exists; stack is simplest in interviews.",
    ),
    "Burst Balloons": _bullets(
        "Interval DP: choose the last balloon to burst in (l,r) to avoid dependency issues.",
        "Add virtual boundaries of 1 at both ends to simplify edge multiplication.",
        "Time O(n^3), space O(n^2); acceptable for n ~ 300? typically n <= 500 is heavy.",
    ),
    # Backtracking
    "Permutations": _bullets(
        "Backtrack with swap-in-place or `used[]` array; revert state on return.",
        "Time O(n·n!) and output size dominates; focus on correctness and pruning when possible.",
    ),
    "Subsets": _bullets(
        "Backtracking include/exclude; each element either chosen or not → 2^n subsets.",
        "Often asked to produce in any order; recursion is simplest.",
    ),
    "Subsets II": _bullets(
        "Sort first; skip duplicates on the same recursion level (`if i>start and a[i]==a[i-1]`).",
        "Still 2^n worst-case, but avoids duplicate outputs.",
    ),
    "Combination Sum": _bullets(
        "Backtracking with reuse: keep index `i` the same after choosing candidate i.",
        "Sort to prune when remaining < candidate.",
        "Avoid duplicates by enforcing non-decreasing choice order.",
    ),
    "Word Search": _bullets(
        "DFS backtracking from each cell; mark visited (temporary) and restore on return.",
        "Prune early when char mismatch; optionally pre-check letter frequency.",
        "Time can blow up; mention constraints and pruning tricks.",
    ),
    # DSU / Bits / Greedy / Math
    "Redundant Connection": _bullets(
        "DSU/Union-Find: the first edge where `find(u)==find(v)` forms a cycle.",
        "Use path compression + union by rank/size for near O(1) amortized.",
        "Graph is undirected with n nodes and n edges (tree + 1 extra).",
    ),
    "Single Number": _bullets(
        "XOR cancels pairs: `a^a=0`, `0^b=b` → XOR all numbers to get the unique.",
        "Variants exist (appear 3 times, two uniques) — clarify which version you’re solving.",
    ),
    "Counting Bits": _bullets(
        "DP: `bits[i] = bits[i>>1] + (i&1)` or `bits[i] = bits[i&(i-1)] + 1`.",
        "Linear time; great to mention bit trick `i&(i-1)` clears lowest set bit.",
    ),
    "Total Hamming Distance": _bullets(
        "Sum per bit position: ones * zeros across all numbers.",
        "Assume 32-bit or 64-bit width depending on constraints.",
        "Time O(32*n) and O(1) extra space.",
    ),
    "Maximum XOR of Two Numbers": _bullets(
        "Use a bitwise trie (0/1) from MSB to LSB; greedily try opposite bit to maximize XOR.",
        "Alternatively, iterative prefix-set approach also works (bit by bit).",
        "Time O(W*n) where W is bit width (e.g., 32).",
    ),
    "Maximum XOR Pair": _bullets(
        "Alias for ‘Maximum XOR of Two Numbers’; same trie/prefix-set approach.",
    ),
    "Jump Game II": _bullets(
        "Greedy BFS-level idea: expand current range, track farthest reach for next step.",
        "Increment steps when you finish the current range (`i==end`).",
        "Time O(n), space O(1).",
    ),
    "Gas Station": _bullets(
        "If total gas < total cost, impossible (return -1).",
        "Greedy: when tank drops below 0, next station becomes the new start.",
        "Single pass O(n) proof relies on deficit cancellation.",
    ),
    "Non-overlapping Intervals": _bullets(
        "Greedy by earliest end time keeps maximum number of non-overlapping intervals.",
        "To minimize removals: removals = n - maxNonOverlap.",
        "Sort by end (not start) for the classic greedy proof.",
    ),
    "Non-overlapping Intervals (min removals)": _bullets(
        "Alias: minimize removals = keep as many as possible by sorting by end and greedily selecting.",
    ),
    "Task Scheduler": _bullets(
        "Math approach: let max frequency be f; answer is max(len(tasks), (f-1)*(n+1)+countMax).",
        "Counts ties among most frequent tasks; idle slots may disappear if enough other tasks exist.",
        "If asked to output schedule, use a max-heap simulation instead.",
    ),
    "GCD / LCM": _bullets(
        "Euclid’s algorithm for gcd; `lcm(a,b)=a/gcd(a,b)*b` (divide first to reduce overflow).",
        "For multiple numbers, fold gcd/lcm pairwise.",
        "Sign/zero edge cases: gcd(a,0)=|a|; lcm(0,*)=0.",
    ),
    "Count Primes": _bullets(
        "Sieve of Eratosthenes: mark multiples starting at i*i.",
        "Stop at sqrt(n); time ~ O(n log log n).",
        "Handle n<=2 (answer 0).",
    ),
    "Trailing Zeroes in Factorial": _bullets(
        "Count factor 5s in n!: `sum_{k>=1} floor(n/5^k)`.",
        "2s are plentiful, so 5s determine trailing zeros.",
        "Time O(log_5 n).",
    ),
    "Trailing Zeroes": _bullets(
        "Alias for trailing zeros in factorial; count 5s via repeated division by 5.",
    ),
    "Kth Largest Element": _bullets(
        "Quickselect average O(n) is common; heap of size k is O(n log k).",
        "Careful with partition implementation and duplicates.",
        "Clarify 1-indexed vs 0-indexed k.",
    ),
    "Kth Largest": _bullets(
        "Alias for Kth Largest Element; quickselect vs heap tradeoffs.",
    ),
    # Concurrency classics
    "Print FooBar Alternately": _bullets(
        "Use two semaphores/condition variables so `foo` signals `bar` and vice versa.",
        "Avoid busy-waiting; ensure correct initialization (foo allowed first).",
        "Interview focus: correctness under concurrency and clean shutdown.",
    ),
    "Dining Philosophers (Deadlock-free)": _bullets(
        "Prevent deadlock via resource ordering (always pick lower-numbered fork first) or a semaphore of N-1.",
        "Discuss starvation vs deadlock: ordering prevents deadlock but not necessarily starvation.",
        "Keep critical sections small; release both forks reliably (finally/defer).",
    ),
    # Graph / Eulerian path
    "Reconstruct Itinerary": _bullets(
        "Eulerian path in directed graph; Hierholzer’s algorithm builds route by postorder.",
        "Use min-heap (or sorted list with pointer) per node to get lexical smallest itinerary.",
        "Reverse the built path at the end.",
    ),
}


def generate_fallback_points(title: str, section: str) -> List[str]:
    t = title.lower()
    s = section.lower()

    if "alias for" in s:
        return _bullets("Alias entry: use the canonical solution and edge cases from the referenced problem.")

    # Lightweight heuristic fallbacks (should be rare).
    if any(k in t for k in ["tree", "bst", "binary tree"]):
        return _bullets("Clarify base cases and recursion return value (what does the helper return?).", "Time O(n); recursion stack O(h).")
    if any(k in s for k in ["heap", "priority", "dijkstra"]):
        return _bullets("State invariant for heap entries and skip stale entries when needed.", "Give time/space complexity clearly.")
    if "dp" in s or "dynamic" in s:
        return _bullets("Define DP state and transition explicitly.", "Mention time and space; discuss 1D optimization if applicable.")
    if any(k in s for k in ["stack", "monotonic"]):
        return _bullets("State the monotonic invariant and what each stack element represents (index vs value).", "Each element pushed/popped once → linear scan.")
    if any(k in s for k in ["two pointers", "left", "right"]):
        return _bullets("State the pointer-move rule and why it’s safe.", "Watch off-by-one in inclusive/exclusive windows.")

    return _bullets(
        "State constraints and confirm the intended optimal complexity.",
        "List 2–3 edge cases (empty input, duplicates, negatives, overflow) and how the algorithm handles them.",
    )


SECTION_RE = re.compile(r'(?ms)(<a id="[^"]+"></a>\n### [^\n]+\n.*?)(?=\n<a id="|\Z)')


def add_important_points_to_section(section: str) -> Tuple[str, bool]:
    if "**Important points:**" in section:
        return section, False

    # Extract title
    m = re.search(r"^### ([^\n]+)$", section, flags=re.MULTILINE)
    if not m:
        return section, False
    title = m.group(1).strip()

    points = IMPORTANT_POINTS.get(title)
    if not points:
        points = generate_fallback_points(title, section)

    important_md = "**Important points:**\n" + "\n".join(f"- {p}" for p in points) + "\n"

    idx_ps = section.find("**Pseudocode:**")
    if idx_ps == -1:
        return section.rstrip() + "\n" + important_md, True

    idx_open = section.find("```", idx_ps)
    if idx_open != -1:
        idx_close = section.find("```", idx_open + 3)
        if idx_close != -1:
            insert_at = idx_close + 3
            # ensure newline after fence
            if insert_at < len(section) and section[insert_at] != "\n":
                important_md = "\n" + important_md
            else:
                important_md = "\n" + important_md
            return section[:insert_at] + important_md + section[insert_at:], True

    # No code fence; insert after the pseudocode line.
    eol = section.find("\n", idx_ps)
    if eol == -1:
        return section.rstrip() + "\n" + important_md, True
    return section[: eol + 1] + important_md + section[eol + 1 :], True


def ensure_catalog(path: Path, check_only: bool) -> int:
    text = path.read_text(encoding="utf-8")
    out_parts: List[str] = []
    last = 0
    changed_sections = 0

    for m in SECTION_RE.finditer(text):
        start, end = m.span(1)
        out_parts.append(text[last:start])
        updated, changed = add_important_points_to_section(m.group(1))
        out_parts.append(updated)
        if changed:
            changed_sections += 1
        last = end

    out_parts.append(text[last:])
    out = "".join(out_parts)

    if check_only:
        missing = 0
        for sec in SECTION_RE.findall(text):
            if "**Important points:**" not in sec:
                missing += 1
        print(f"Sections missing Important points: {missing}")
        return 0 if missing == 0 else 2

    if changed_sections:
        path.write_text(out, encoding="utf-8")
    print(f"Updated sections: {changed_sections}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="Only report missing sections")
    ap.add_argument("--path", default=str(CATALOG_PATH), help="Path to PROBLEM_DETAILS.md")
    args = ap.parse_args()

    path = Path(args.path)
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")
    return ensure_catalog(path, args.check)


if __name__ == "__main__":
    raise SystemExit(main())

