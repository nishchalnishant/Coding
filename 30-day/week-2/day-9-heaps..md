# Day 9: Heaps.

Here are detailed notes for **Day 9: Heaps**. This day focuses on understanding heap data structures, particularly min-heaps and max-heaps, and solving related problems.

***

#### 1. **What is a Heap?**

A **heap** is a special tree-based data structure that satisfies the **heap property**:

* In a **max-heap**, for any given node ( N ), the value of ( N ) is greater than or equal to the values of its children. Thus, the maximum element is at the root.
* In a **min-heap**, the value of ( N ) is less than or equal to the values of its children. Thus, the minimum element is at the root.

**Key Characteristics**:

* A heap is a complete binary tree, which means all levels are fully filled except possibly for the last level, which is filled from left to right.
* Heaps are commonly implemented using arrays for efficient memory use.

***

#### 2. **Heap Operations**

The primary operations on heaps include **insertion**, **deletion (extracting the root)**, and **heapify**.

**2.1 Insertion Operation**

To insert a new element into a heap:

1. Add the element at the end of the heap (array).
2. "Bubble up" or "percolate up" the element to restore the heap property.
   * Compare the newly added element with its parent; if it violates the heap property, swap them.
   * Repeat until the heap property is restored or the element reaches the root.

**Implementation** (Min-Heap):

```python
def insert_heap(heap, key):
    heap.append(key)  # Add the new key at the end
    index = len(heap) - 1  # Index of the newly added element

    # Bubble up
    while index > 0:
        parent_index = (index - 1) // 2
        if heap[index] < heap[parent_index]:  # Min-Heap property
            heap[index], heap[parent_index] = heap[parent_index], heap[index]
            index = parent_index
        else:
            break
```

***

**2.2 Deletion Operation (Extracting the Root)**

To remove the root element (the minimum in a min-heap or maximum in a max-heap):

1. Replace the root with the last element in the heap.
2. Remove the last element.
3. "Bubble down" or "percolate down" the new root to restore the heap property.
   * Compare the new root with its children; if it violates the heap property, swap it with the smaller child (for min-heap) or the larger child (for max-heap).
   * Repeat until the heap property is restored.

**Implementation** (Min-Heap):

```python
def extract_min(heap):
    if len(heap) == 0:
        return None
    if len(heap) == 1:
        return heap.pop()

    root = heap[0]
    heap[0] = heap.pop()  # Replace root with the last element
    min_heapify(heap, 0)  # Restore the heap property
    return root

def min_heapify(heap, index):
    smallest = index
    left = 2 * index + 1
    right = 2 * index + 2

    if left < len(heap) and heap[left] < heap[smallest]:
        smallest = left
    if right < len(heap) and heap[right] < heap[smallest]:
        smallest = right

    if smallest != index:
        heap[index], heap[smallest] = heap[smallest], heap[index]
        min_heapify(heap, smallest)
```

***

#### 3. **Heapify Operation**

The **heapify** operation is used to build a heap from an arbitrary array or to maintain the heap property after insertion or deletion.

**Bottom-Up Heap Construction**: To build a heap from an array, start from the last non-leaf node and perform heapify down to the root.

**Implementation**:

```python
def build_min_heap(array):
    n = len(array)
    # Start from the last non-leaf node
    for i in range(n // 2 - 1, -1, -1):
        min_heapify(array, i)
```

***

#### 4. **Heap Sort Algorithm**

Heap sort is an efficient sorting algorithm that uses a heap data structure to sort elements:

1. Build a max-heap from the input data.
2. The largest item is stored at the root of the heap.
3. Swap it with the last element, reduce the size of the heap by one, and heapify the root.
4. Repeat until the heap is empty.

**Implementation**:

```python
def heap_sort(array):
    build_min_heap(array)
    sorted_array = []
    while array:
        min_element = extract_min(array)
        sorted_array.append(min_element)
    return sorted_array[::-1]  # Return reversed sorted array
```

***

#### 5. **Applications of Heaps**

Heaps are useful in various applications, including:

* **Priority Queues**: Heaps are used to implement priority queues, allowing for efficient retrieval of the highest or lowest priority element.
* **Graph Algorithms**: Heaps are used in Dijkstra's algorithm for finding the shortest path.
* **Sorting Algorithms**: Heap sort provides an efficient way to sort an array with a time complexity of O(n log n).
* **Scheduling**: In operating systems, heaps can manage processes based on their priority.

***

#### 6. **Time Complexity of Heap Operations**

* **Insertion**: O(log n)
* **Deletion (extract)**: O(log n)
* **Heapify**: O(n) for building the heap from an array, O(log n) for percolating down.
* **Heap Sort**: O(n log n)

***

#### 7. **Recommended Practice Problems**

1. **LeetCode**:
   * Kth Largest Element in an Array
   * Merge K Sorted Lists
   * Top K Frequent Elements
   * Find Median from Data Stream
2. **HackerRank**:
   * Max Heap
   * Min Heap

***

#### 8. **Key Concepts to Remember**

* Understanding the properties and operations of heaps is crucial for efficient data management in priority queues and graph algorithms.
* Heap operations maintain the structure and properties efficiently, making heaps a versatile data structure in computer science.

By mastering heaps and their applications, you will enhance your problem-solving skills and be well-prepared for coding interviews involving data structures and algorithms.
