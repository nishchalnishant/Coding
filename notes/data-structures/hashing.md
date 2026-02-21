# Hashing

#### **Detailed Summary of Hashing (Data Structures)**

**Hashing** is a technique used to efficiently store and retrieve data by transforming a given key into an index in a fixed-size table known as a **hash table**. Hashing allows for nearly constant time complexity, O(1), for basic operations like insertion, deletion, and search. The goal of hashing is to map large datasets to a smaller fixed size (the hash table) using a **hash function**.

**Key Concepts:**

1. **Hash Function**:
   * A **hash function** converts a key into a hash code, which is then used to determine the index where the data should be stored in the hash table.
   * **Ideal Hash Function Properties**:
     * **Deterministic**: A given input should always generate the same output.
     * **Uniformity**: It should distribute the keys uniformly across the hash table to minimize collisions.
     * **Efficiency**: The function should compute the hash value quickly.
2. **Hash Table**:
   * A **hash table** is an array of fixed size where each index holds the actual data or a pointer to it. The index is determined by the hash function.
   * Hash tables are used in many applications like databases (for indexing), caching, and dictionary implementations.
3. **Collision Handling**: Collisions occur when two different keys produce the same hash value. There are several methods to handle collisions:
   * **Chaining**: Each slot in the hash table points to a linked list (or another data structure) of values that hashed to the same index. When a collision occurs, the new key is appended to the list at that index.
   * **Open Addressing**: When a collision occurs, the algorithm tries to find another open slot in the hash table by probing.
     * **Linear Probing**: Sequentially checking the next available slot.
     * **Quadratic Probing**: Checking slots with increasing intervals.
     * **Double Hashing**: Using a second hash function to determine the step size for probing.
4. **Rehashing**:
   * When the hash table becomes full or the load factor (ratio of entries to table size) exceeds a certain threshold, **rehashing** is performed. This involves creating a larger hash table and re-inserting all existing elements using a new hash function.
5. **Load Factor**:
   * The **load factor** of a hash table is defined as the ratio of the number of elements in the table to the table’s size. A load factor too high can result in excessive collisions, and rehashing may be triggered.
6. **Applications of Hashing**:
   * **Dictionaries/Maps**: Hashing is widely used in the implementation of associative arrays (e.g., `HashMap` in Java, `HashTable` in Python).
   * **Database Indexing**: Hash tables are used for efficient lookups in databases.
   * **Caching**: Used in caches to quickly retrieve data.
   * **Symbol Tables in Compilers**: For storing variables and function names.
   * **Cryptography**: Hash functions are used to secure data by converting it to a fixed size, making it hard to reverse.
7. **Perfect Hashing**:
   * In some cases, it's possible to design a **perfect hash function** that produces no collisions for a particular set of inputs. This is often used when the entire set of inputs is known beforehand.
8. **Common Hashing Algorithms**:
   * **Modulo Hashing**: Often used in simple hash functions where the key is divided by the size of the hash table, and the remainder is the index.
   * **Multiplicative Hashing**: A constant fraction of the key is multiplied and then modded to get the hash value.
   * **Cryptographic Hash Functions**: Functions like MD5 and SHA are used in cryptography, ensuring data integrity and security.

***

#### **List of Important Questions for Hashing**:

**Easy:**

1. **Implement a hash table with chaining**.
2. **Check if two arrays contain the same set of elements using a hash map**.
3. **Find the first non-repeating character in a string using hashing**.
4. **Check if two strings are anagrams using a hash map**.
5. **Find the intersection of two arrays using hashing**.
6. **Count the frequency of each element in an array using a hash map**.

**Medium:**

1. **Design and implement a hash table with open addressing**.
2. **Find all pairs in an array whose sum is equal to a given number using a hash map**.
3. **Implement a LRU (Least Recently Used) cache using a hash map and a doubly linked list**.
4. **Find the longest subarray with a sum equal to 0 using a hash map**.
5. **Find the longest consecutive subsequence in an unsorted array using hashing**.

**Hard:**

1. **Design a perfect hash function for a given set of inputs**.
2. **Implement a consistent hashing algorithm for distributing loads across servers**.
3. **Find the number of subarrays with a sum divisible by k using hashing**.
4. **Design a system that uses a hash table to efficiently store and retrieve URLs**.
5. **Solve the two-sum problem in O(n) time using hashing**.

***

These questions cover both basic and advanced aspects of hashing, helping you develop a strong foundation in hash tables, hash functions, and collision handling techniques. Let me know if you'd like detailed explanations or solutions for any specific problem!







Here are some tips and tricks to help you solve hashing problems effectively in software engineering interviews:

#### 1. **Understand Hash Tables**

* A **hash table** (or hash map) is a data structure that provides average O(1) time complexity for insertions, deletions, and lookups.
* It uses a **hash function** to map keys to indices in an array.
* Know how to handle **collisions**, which occur when two keys hash to the same index:
  * **Chaining**: Store multiple elements in a list at the same index.
  * **Open addressing**: Find another open slot by probing (e.g., linear probing or quadratic probing).

#### 2. **Hashing Functions**

* Understand the importance of good **hash functions** that distribute keys uniformly to minimize collisions.
* For interviews, you may not need to implement a hash function, but be aware that bad hash functions can degrade performance.

#### 3. **Common Hashing Problems**

* Hashing is often used to solve problems like:
  * **Frequency counting**: Counting occurrences of elements (e.g., finding the majority element).
  * **Checking for duplicates**: Determine if there are duplicates in an array.
  * **Finding complements**: Solving problems like two-sum where you need to check if two elements sum up to a target.
  * **Anagram detection**: Checking if two strings are anagrams by comparing character frequencies using a hash map.
  * **Set operations**: Using a hash set to check for membership, union, or intersection.

#### 4. **Handling Collisions**

* Be familiar with common strategies to resolve collisions in hash tables:
  * **Chaining**: Each array element points to a list of elements that hash to the same index.
  * **Linear Probing**: If a collision occurs, check the next available slot.
  * **Quadratic Probing**: Use a quadratic function to find the next slot.
  * **Double Hashing**: Use a second hash function to calculate a step size for probing.

#### 5. **Dealing with Large Keys**

* In cases where the key is a **large object** (e.g., a string or composite object), compute its hash code once and store it for efficient lookups.
* For strings, use hashing to efficiently compare or index substrings (e.g., in **Rabin-Karp** algorithm for substring search).

#### 6. **Key Problems Solved with Hashing**

* **Two Sum Problem**: Store elements in a hash map as you iterate through the array. For each element, check if the complement (target - current element) exists in the hash map.
* **Group Anagrams**: Use a hash map where the key is a sorted version of each string (or its character frequency count), and the value is a list of anagrams.
* **Subarray with Given Sum**: Store cumulative sums in a hash map and check if the sum of any subarray is equal to the target.
* **Find Duplicates**: Store elements in a hash set. If you encounter an element that’s already in the set, it’s a duplicate.
* **Longest Consecutive Sequence**: Use a hash set to store elements and then check, for each element, whether it starts a sequence.

#### 7. **Hashing for String Matching**

* **Rabin-Karp Algorithm**: Uses hashing to compare substrings. Hash the pattern and compare it with the hash of substrings of the text.
* This reduces the time complexity of pattern matching to O(n) on average by avoiding character-by-character comparisons.

#### 8. **Designing a Good Hash Function**

* For integer keys, a simple **modulo operation** (`key % size`) works well.
* For string keys, combine the ASCII values of characters and use modulo or a prime base (e.g., `31`) to reduce collisions.
* Avoid hash functions that create too many collisions by spreading values uniformly across the hash table.

#### 9. **Hash Table Resizing**

* When the load factor (number of elements / size of the table) exceeds a certain threshold (usually 0.7 or 0.75), rehashing is necessary.
* Understand how **rehashing** works:
  * A new larger table is created, and all elements are reinserted into the new table using their hash values modulo the new table size.

#### 10. **Time Complexity**

* Average case time complexity for insertions, deletions, and lookups in a hash table is O(1), but the worst-case can degrade to O(n) when collisions occur.
* Be mindful of edge cases where many collisions could lead to performance issues, and consider alternatives like balanced trees (O(log n) operations) in such cases.

#### 11. **Space Complexity**

* Hash tables generally require more space than other data structures due to the use of an underlying array and potentially storing multiple elements at each index (in case of chaining).
* Be conscious of the trade-off between time efficiency and space usage, especially when dealing with large datasets.

#### 12. **Practice Problems**

* **Two Sum**: Given an array of integers, return indices of two numbers such that they add up to a target.
* **Subarray Sum Equals K**: Find the total number of continuous subarrays whose sum equals to a given number k.
* **Group Anagrams**: Given an array of strings, group the anagrams together.
* **Longest Consecutive Sequence**: Given an unsorted array, find the length of the longest consecutive elements sequence.
* **Word Pattern Matching**: Given a pattern and a string, determine if the string follows the same pattern.

#### 13. **Handling Collisions Gracefully**

* Be prepared to explain how you would handle edge cases where many keys hash to the same index (e.g., how chaining works in case of multiple collisions).
* In open addressing, explain your approach to resizing the table and ensuring that the load factor remains balanced.

#### 14. **Hashing for Caching and Deduplication**

* Hashing is used in systems for **caching** results (e.g., using memoization) and **deduplicating** data (e.g., hashing files to check for duplicates).
* In interviews, you might encounter system design problems where you have to explain how to use hashing for efficient lookups or caching.

By mastering these techniques and practicing a variety of hashing-related problems, you'll be well-prepared for hashing questions in your software engineering interviews. Would you like to explore specific hashing problems in more detail?
