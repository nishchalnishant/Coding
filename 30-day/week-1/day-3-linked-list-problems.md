# Day 3: Linked List Problems

Here are the detailed notes for **Day 3: Linked List Problems**. The focus is on understanding how linked lists work, their operations, and practicing key problems like reversing a linked list, detecting cycles, and merging lists.

#### 1. **Linked Lists Overview**

* **Definition**: A linked list is a linear data structure in which each element, called a **node**, contains:
  * **Data**: The value stored in the node.
  * **Next**: A pointer/reference to the next node in the sequence (in the case of singly linked lists).

#### Types of Linked Lists

1. **Singly Linked List**:
   * Each node points to the next node.
   * The last node points to `null` (or `None` in Python), marking the end of the list.
2. **Doubly Linked List**:
   * Each node has two pointers:
     * **Next**: Points to the next node.
     * **Prev**: Points to the previous node.
3. **Circular Linked List**:
   * In a circular linked list, the last node’s next pointer points back to the head, forming a loop.

***

#### 2. **Common Operations**

* **Traversal**: Iterating through the linked list from head to the last node (or back to the head in circular lists).
  * Time Complexity: O(n) for a list of size `n`.
* **Insertion**:
  * **At the head**: Insert a node at the beginning of the list.
    * Time Complexity: O(1).
  * **At the tail**: Insert a node at the end of the list.
    * Time Complexity: O(n) in singly linked lists, O(1) in doubly linked lists.
* **Deletion**:
  * **From the head**: Remove the first node.
    * Time Complexity: O(1).
  * **From the tail or middle**: Remove any node.
    * Time Complexity: O(n), as you need to traverse the list to find the node.

***

#### 3. **Key Problems and Solutions**

**1. Reversing a Linked List**

* **Problem Statement**: Given the head of a singly linked list, reverse the list and return the new head.
* **Approach**:
  * Traverse the list and change the `next` pointers to point to the previous node.
  * Maintain three pointers: `prev`, `curr`, and `next`. At each step, adjust the `next` pointer of `curr` to point to `prev`, then move forward.
* **Time Complexity**: O(n), where `n` is the number of nodes.
* **Space Complexity**: O(1), since the reversal is done in place.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseList(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev
```

**2. Detecting a Cycle in a Linked List**

* **Problem Statement**: Given the head of a linked list, determine if the linked list contains a cycle.
* **Approach**:
  * Use **Floyd’s Cycle Detection Algorithm (Tortoise and Hare)**:
    * Maintain two pointers: `slow` and `fast`.
    * Move `slow` one step at a time and `fast` two steps at a time.
    * If there is a cycle, they will eventually meet; if not, `fast` will reach the end of the list.
* **Time Complexity**: O(n).
* **Space Complexity**: O(1).

```python
def hasCycle(head):
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

**3. Merging Two Sorted Linked Lists**

* **Problem Statement**: Given two sorted linked lists, merge them into one sorted linked list.
* **Approach**:
  * Use a two-pointer technique to compare nodes from both lists and build the result by attaching smaller nodes first.
  * Recursion can also be used, but an iterative solution is more space-efficient.
* **Time Complexity**: O(n + m), where `n` and `m` are the lengths of the two lists.
* **Space Complexity**: O(1) for the iterative solution.

```python
def mergeTwoLists(l1, l2):
    dummy = ListNode()
    current = dummy
    
    while l1 and l2:
        if l1.val < l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    
    # Attach the remaining nodes
    if l1:
        current.next = l1
    else:
        current.next = l2
    
    return dummy.next
```

**4. Remove N-th Node from the End of the List**

* **Problem Statement**: Given the head of a linked list, remove the n-th node from the end of the list and return its head.
* **Approach**:
  * Use a two-pointer technique:
    * Move one pointer `n` steps ahead.
    * Then move both pointers one step at a time until the first pointer reaches the end. The second pointer will now point to the node just before the node to be removed.
* **Time Complexity**: O(n).
* **Space Complexity**: O(1).

```python
def removeNthFromEnd(head, n):
    dummy = ListNode(0)
    dummy.next = head
    first = second = dummy
    
    # Move first n+1 steps ahead, so there's a gap of n between first and second
    for _ in range(n + 1):
        first = first.next
    
    # Move both pointers
    while first:
        first = first.next
        second = second.next
    
    # Remove the nth node
    second.next = second.next.next
    return dummy.next
```

**5. Intersection of Two Linked Lists**

* **Problem Statement**: Given the heads of two singly linked lists, find the node where the two lists intersect.
* **Approach**:
  * Traverse both lists and calculate their lengths. Find the length difference and move the pointer of the longer list by that difference. Then traverse both lists together until they meet.
* **Time Complexity**: O(n + m).
* **Space Complexity**: O(1).

```python
def getIntersectionNode(headA, headB):
    if not headA or not headB:
        return None
    
    p1, p2 = headA, headB
    
    # Traverse both lists, and if one list ends, switch to the other list
    while p1 != p2:
        p1 = p1.next if p1 else headB
        p2 = p2.next if p2 else headA
    
    return p1
```

***

#### 4. **Key Linked List Techniques**

1. **Two-pointer Approach**:
   * Many linked list problems like cycle detection, finding the middle, or removing the nth node from the end can be solved using two-pointer techniques (fast and slow pointers).
2. **Dummy Nodes**:
   * Using a dummy node as a placeholder is a common trick when merging lists, deleting nodes, or handling edge cases like deleting the head of the list.
3. **Reversing Linked Lists**:
   * Many problems (such as in-place reversal of sublists) rely on reversing parts of a linked list. Practice reversing the whole list first, then extend this to reversing portions of the list.
4. **Handling Edge Cases**:
   * Always consider cases like:
     * Empty list (`head = None`).
     * Single node list (`head.next = None`).
     * Lists with only two nodes.
     * Removing the head node.

***

#### Recommended Practice Problems

1. **LeetCode**:
   * [Reverse Linked List](../../google-sde2/PROBLEM_DETAILS.md#reverse-linked-list)
   * Linked List Cycle
   * [Merge Two Sorted Lists](../../google-sde2/PROBLEM_DETAILS.md#merge-two-sorted-lists)
   * Remove N-th Node From End of List
   * Intersection of Two Linked Lists
2. **HackerRank**:
   * Print the Elements of a Linked List
   * Insert a Node at a Specific Position
   * Compare Two Linked Lists

By understanding these key linked list problems and techniques, you'll be well-prepared for more complex problems involving linked lists in coding interviews.
