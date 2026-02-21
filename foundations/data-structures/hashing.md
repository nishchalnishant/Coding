# Hashing

A technique to uniquely map data to an array index using a **hash function**, enabling $O(1)$ average time complexity for lookups, insertions, and deletions.

## Key Concepts
- **Hash Function**: Maps a key to an integer index. Must be deterministic, uniform (minimizes collisions), and fast to compute.
- **Load Factor**: $\frac{\text{Number of elements}}{\text{Number of buckets}}$. High load factor = high collisions. Triggers resizing (rehashing).

## Collision Handling
- **Chaining**: Buckets contain a Linked List (or balanced tree). Colliding elements are appended to the list.
- **Open Addressing**: If a bucket is full, probe for the next empty bucket.
  - *Linear Probing*: Check next slot ($i+1$).
  - *Quadratic Probing*: Check slots at $i+1^2, i+2^2$, etc.
  - *Double Hashing*: Use a second hash function to determine step size.

## Applications
- **Frequency Maps**: Counting occurrences (e.g., Anagrams, Majority Element).
- **Sets**: $O(1)$ existence checks (e.g., detecting cycles, finding duplicates).
- **Caching**: LRU Cache (HashMap + Doubly Linked List).
- **String Matching**: Rabin-Karp algorithm uses rolling hashes.

## Common SDE-3 Hashing Problems
- *Easy*: Two Sum, Valid Anagram, First Unique Character.
- *Medium*: Group Anagrams, Subarray Sum Equals K, Longest Consecutive Sequence, LRU Cache.
- *Hard*: Minimum Window Substring, Max Points on a Line, Substring with Concatenation of All Words.
