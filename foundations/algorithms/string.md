# Strings

Strings are essentially arrays of characters, with problems often centering around pattern matching, palindromes, sequence parsing, and window techniques.

## Key Concepts
- **Immutability**: In many languages (Java, Python, C#), strings cannot be modified in place. Use `StringBuilder` or list of characters for $O(1)$ appends.
- **Substrings vs Subsequences**: Substrings are contiguous; subsequences maintain relative order but need not be contiguous.

## SDE-3 String Algorithms
- **Rabin-Karp**: Rolling hash algorithm for $O(N+M)$ pattern matching.
- **KMP (Knuth-Morris-Pratt)**: Uses an LPS (Longest Prefix Suffix) array to skip redundant comparisons in $O(N+M)$ time. Good for repeated substrings.
- **Z-Algorithm**: Computes the Z-array storing the length of the longest substring starting at `i` which is also a prefix of the string.
- **Trie**: Building a prefix tree allows for extremely fast searches of words or prefix lookups $O(L)$, where $L$ is word length.

## Core Techniques
- **Two Pointers**: Reversing strings, Palindrome checking (expanding from center or comparing ends).
- **Sliding Window**: Longest substring without repeating characters, Minimum Window Substring.
- **Hashing/Frequency Array**: 
  - *Anagram checks*: Count frequencies of the 26 lowercase English letters.
  - *Ransom Note*: Decrement counts.
- **Dynamic Programming**: Longest Common Subsequence (LCS), Edit Distance (Levenshtein), Longest Palindromic Substring.

## Common SDE-3 String Problems
- *Easy*: Valid Palindrome, Valid Anagram, Longest Common Prefix.
- *Medium*: Longest Substring Without Repeating Characters, Longest Palindromic Substring, Group Anagrams, Find All Anagrams in a String.
- *Hard*: Minimum Window Substring, Edit Distance, Implement strStr() (KMP), Valid Number.
