# Day 5: Hash Tables

Here are the detailed notes for **Day 5: Hash Tables**. The focus is on understanding the fundamentals of hash tables (also called hash maps or dictionaries), their operations, how they handle collisions, and solving key problems like group anagrams and two-sum.

#### 1. **What is a Hash Table?**

* **Definition**: A **hash table** is a data structure that implements an associative array, mapping keys to values. It uses a **hash function** to compute an index (or hash code) into an array of buckets or slots, from which the desired value can be found.
* **Key Features**:
  * Efficient average time complexity for operations: O(1) for insertion, deletion, and lookups.
  * A hash table maps a **key** to a **value**.
* **Common Operations**:
  * **Insert(key, value)**: Store the key-value pair in the hash table.
  * **Get(key)**: Retrieve the value associated with the key.
  * **Delete(key)**: Remove the key-value pair from the hash table.
  * **Contains(key)**: Check if a key exists in the hash table.

***

#### 2. **Hash Functions**

A **hash function** takes a key and returns an integer, the **hash code**, which is used as an index to store the key-value pair in the hash table. A good hash function should:

* Distribute keys uniformly across the hash table to avoid clustering.
* Be fast to compute.
* Minimize collisions (when two keys hash to the same index).

***

#### 3. **Collision Resolution Techniques**

Collisions occur when two different keys hash to the same index. There are several techniques to handle collisions:

**1. Chaining (Separate Chaining)**

* **Idea**: Each bucket in the hash table holds a linked list (or any other data structure) of key-value pairs that map to the same hash index.
* **Advantage**: Simple to implement and handles collisions well.
*   **Disadvantage**: Performance degrades to O(n) in the worst case if many elements collide and are stored in the same bucket.

    ```python
    # Example of chaining:
    hash_table = {
        0: [("apple", 5), ("banana", 2)],
        1: [("pear", 7)],
        2: []
    }
    ```

**2. Open Addressing**

* **Idea**: Instead of storing the colliding key-value pairs in a linked list at the same index, look for another empty slot (by probing) in the hash table itself.
*   Common probing techniques:

    * **Linear Probing**: If a collision occurs, look at the next index (hash + 1, hash + 2, etc.).
    * **Quadratic Probing**: Look at increasing intervals (hash + 1², hash + 2², etc.).
    * **Double Hashing**: Use a second hash function to determine the step size for probing.

    ```python
    # Example of linear probing:
    hash_table = [None] * 7
    # Insert "apple" at index 0
    # Insert "banana" at index 1 after a collision at index 0
    ```

**3. Rehashing**

* If the load factor (the ratio of the number of elements to the number of buckets) exceeds a threshold, double the size of the hash table and rehash all existing keys.

***

#### 4. **Hash Table Performance**

* **Average Time Complexity**:
  * **Search**: O(1).
  * **Insertion**: O(1).
  * **Deletion**: O(1).
* **Worst Case Time Complexity**: O(n), due to hash collisions. However, with good hash functions and a low load factor, collisions can be minimized, keeping performance close to O(1).
* **Load Factor**:
  * The **load factor** is the ratio of the number of elements in the hash table to the total number of buckets.
  * To maintain O(1) operations, hash tables resize when the load factor exceeds a certain threshold (typically 0.75).

***

#### 5. **Key Problems and Solutions**

**1. Two Sum**

* **Problem Statement**: Given an array of integers `nums` and an integer `target`, return the indices of the two numbers that add up to the `target`.
* **Approach**:
  * Use a hash table to store the numbers you've seen so far and their indices.
  * For each number `num`, calculate the complement (`target - num`) and check if it's in the hash table.
  * If the complement is found, return the indices.
* **Time Complexity**: O(n), where `n` is the number of elements in the array.
* **Space Complexity**: O(n), for the hash table.

```python
def twoSum(nums, target):
    hash_table = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in hash_table:
            return [hash_table[complement], i]
        hash_table[num] = i
```

**2. Group Anagrams**

* **Problem Statement**: Given an array of strings, group the anagrams together.
* **Approach**:
  * Use a hash table where the key is the sorted version of the string (because anagrams, when sorted, are identical).
  * The value will be a list of all strings that match that key.
* **Time Complexity**: O(n \* k log k), where `n` is the number of strings and `k` is the maximum length of a string (sorting each string takes O(k log k)).
* **Space Complexity**: O(nk), for storing the strings in the hash table.

```python
def groupAnagrams(strs):
    hash_table = {}
    for s in strs:
        sorted_str = ''.join(sorted(s))
        if sorted_str in hash_table:
            hash_table[sorted_str].append(s)
        else:
            hash_table[sorted_str] = [s]
    return list(hash_table.values())
```

**3. Subarray Sum Equals K**

* **Problem Statement**: Given an array of integers `nums` and an integer `k`, find the total number of continuous subarrays whose sum equals `k`.
* **Approach**:
  * Use a hash table to keep track of the cumulative sum up to each index.
  * For each element, calculate the cumulative sum and check if `(cumulative sum - k)` is in the hash table (meaning there is a subarray that sums to `k`).
* **Time Complexity**: O(n), where `n` is the length of the array.
* **Space Complexity**: O(n), for the hash table.

```python
def subarraySum(nums, k):
    count = 0
    cumulative_sum = 0
    hash_table = {0: 1}  # To handle the case when subarray starts from index 0
    
    for num in nums:
        cumulative_sum += num
        if cumulative_sum - k in hash_table:
            count += hash_table[cumulative_sum - k]
        if cumulative_sum in hash_table:
            hash_table[cumulative_sum] += 1
        else:
            hash_table[cumulative_sum] = 1
    
    return count
```

**4. Longest Substring Without Repeating Characters**

* **Problem Statement**: Given a string `s`, find the length of the longest substring without repeating characters.
* **Approach**:
  * Use a sliding window approach with a hash table to track the last seen index of each character.
  * Expand the window until a repeated character is found, then slide the left pointer of the window to the right of the previous occurrence.
* **Time Complexity**: O(n), where `n` is the length of the string.
* **Space Complexity**: O(min(n, m)), where `m` is the size of the character set.

```python
def lengthOfLongestSubstring(s: str) -> int:
    char_map = {}
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        if s[right] in char_map and char_map[s[right]] >= left:
            left = char_map[s[right]] + 1
        char_map[s[right]] = right
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

**5. Top K Frequent Elements**

* **Problem Statement**: Given a non-empty array of integers, return the `k` most frequent elements.
* **Approach**:
  * Use a hash table to count the frequency of each element.
  * Sort the elements based on frequency, or use a heap/priority queue to maintain the top `k` elements.
* **Time Complexity**: O(n log k) using a heap, where `n` is the length of the array.
* **Space Complexity**: O(n), for the hash table.

```python
from collections import Counter
import heapq

def topKFrequent(nums, k):
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)
```

***

#### 6. **Key Hash Table Techniques**

1. **Choosing a Good Hash Function**:
   * Ensure the hash function distributes keys uniformly to avoid clustering and collisions.
   * For strings, a common hash function is using polynomial rolling hashing:
     * `hash = (hash * prime + char_value) % mod`.
2. **Handling Collisions**:
   * Separate chaining with linked lists is the most commonly used technique because it is simple and easy to implement.
   * Open addressing is more space-efficient but can lead to clustering, which affects performance.
3. **Optimizations**:
   * **Rehashing**: If the load factor gets too high (e.g., greater than 0.75), the table should be resized to maintain constant time complexity.
   * **Double Hashing**: When using open addressing, use double hashing to reduce clustering.

***

#### Recommended Practice Problems

1. **LeetCode**:
   * Two Sum
   * Group Anagrams
   * Subarray Sum Equals K
   * Longest Substring Without Repeating Characters
   * Top K Frequent Elements
2. **HackerRank**:
   * Frequency Queries
   * Hash Tables: Ice Cream Parlor
   * Sherlock and Anagrams

Mastering hash tables and common problems like "Two Sum" and "Group Anagrams" will give you a strong foundation in understanding how to optimize performance using this data structure.
