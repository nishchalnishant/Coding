# Leet code practice

* \[Easy] \[Strings] [https://leetcode.com/problems/valid-parentheses/](https://leetcode.com/problems/valid-parentheses/)
  1. Push only opening brackets
  2.  For a closing bracket:

      * Stack must NOT be empty
      * Top of stack must match the closing bracket


*   \[Easy] {linked list] [https://leetcode.com/problems/merge-two-sorted-lists/description/](https://leetcode.com/problems/merge-two-sorted-lists/description/)



```python
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode().        ##create a new node
        cur = dummy                # point a variable to that new

        while list1 and list2:        #simpley put the list name which we are iterating onto
            if list1.val > list2.val: #
                cur.next = list2
                list2 = list2.next
            else:
                cur.next = list1
                list1 = list1.next   ##point to the next one
            
            cur = cur.next
        
        if list1:
            cur.next = list1
        else:
            cur.next = list2
        
        return dummy.next
```

or we can do&#x20;

```python
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        if not list1 or not list2:
            return list1 if list1 else list2

        if list1.val > list2.val:
            list1, list2 = list2, list1

        list1.next = self.mergeTwoLists(list1.next, list2)
        return list1
```

* Easy, Binary search \[ [https://leetcode.com/problems/search-insert-position/description/](https://leetcode.com/problems/search-insert-position/description/)]

```python
def searchInsert(self, nums: List[int], target: int) -> int:
        l, h = 0, len(nums) - 1

        while l <= h:
            mid = l + (h - l) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                l = mid + 1
            else:
                h = mid - 1

        return l
```

* Binary to int&#x20;

```python
return bin(int(a,2)+int(b,2))[2:]

```

* stairs (DP)

```python3
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 3: return n

        prev1 = 3
        prev2 = 2
        cur = 0

        for _ in range(3, n):
            cur = prev1 + prev2
            prev2 = prev1
            prev1 = cur
        
        return cur

        
```

* linekd list&#x20;

don't use while(temp.next), instead of this use while temp and temp.next:

* [https://leetcode.com/problems/merge-sorted-array/description/](https://leetcode.com/problems/merge-sorted-array/description/)
  *   don't do sorting as&#x20;



      Swapping:

      * Breaks the sorted order of nums2
      * Requires re-sorting after every swap
      * Becomes O((m+n) log (m+n)) or worse
      * Violates the problem constraint
* [https://leetcode.com/problems/same-tree/description/](https://leetcode.com/problems/same-tree/description/)
  * inorder traversal not enough for checking if trees are same or not
  * we need to do this

```python
class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not p and not q:
            return True
        if not p or not q:
            return False
        if p.val != q.val:
            return False

        return (
            self.isSameTree(p.left, q.left) and
            self.isSameTree(p.right, q.right)
        )
```

* For recursion don't pass values which are changing into the recursive function, instead use this&#x20;

```python
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:

        def build(head):
            if not head:
                return ""
            return str(head.val) + build(head.next)

        s = build(head)
        return s == s[::-1]
```

for two pointers this should be the case

while i < len(nums) - 2:



* train arrival time \[ sorting 2 arrays which are dependent on each]

#### Steps

1. Sort arrival times
2. Sort departure times
3. Use two pointers:
   * i → arrival
   * j → departure
4. Traverse events in time order

```python
class Solution:
    def minimumPlatform(self, n, arr, dep):
        arr.sort()
        dep.sort()

        i = 0  # arrival pointer
        j = 0  # departure pointer

        curr = 0
        ans = 0

        while i < n and j < n:
            if arr[i] <= dep[j]:
                curr += 1
                ans = max(ans, curr)
                i += 1
            else:
                curr -= 1
                j += 1

        return ans
```



* power calculation
  * while calculating for power just calculate for the half and then multiply them , this saves calculations

```python
class Solution:    
    def myPow(self, x, n):
        #your code goes here

        if(n<0):
            x=1/x
            n=n*(-1)

        if(n==0):
            return 1



        def calc(x,n):
            if(n==0):
                return 1

            half=calc(x,n//2)

            if(n%2==0):
                return half*half
            else:
                return x*half*half

        return calc(x,n)
```

these two functions give the left most and right most occurance of the number\
<br>

```python
class Solution:
    def searchRange(self, nums, target):
        
        def findLeft():
            l, h = 0, len(nums) - 1
            ans = -1
            while l <= h:
                mid = (l + h) // 2
                if nums[mid] >= target:
                    h = mid - 1
                else:
                    l = mid + 1
                if nums[mid] == target:
                    ans = mid
            return ans

        def findRight():
            l, h = 0, len(nums) - 1
            ans = -1
            while l <= h:
                mid = (l + h) // 2
                if nums[mid] <= target:
                    l = mid + 1
                else:
                    h = mid - 1
                if nums[mid] == target:
                    ans = mid
            return ans

        return [findLeft(), findRight()]

```

* classic binary search to find no of rotations\
  <br>



```python
    class Solution: 
        def findKRotation(self, nums): 
            l, r = 0, len(nums) - 1 
            ans = float('inf') idx = 0
            
            while l <= r:
                # If subarray is sorted
                if nums[l] <= nums[r]:
                    if nums[l] < ans:
                        ans = nums[l]
                        idx = l
                    break
        
                mid = (l + r) // 2
        
                # Left half sorted
                if nums[l] <= nums[mid]:
                    if nums[l] < ans:
                        ans = nums[l]
                        idx = l
                    l = mid + 1
                else:
                    # Right half sorted
                    if nums[mid] < ans:
                        ans = nums[mid]
                        idx = mid
                    r = mid - 1
        
            return idx
```

level order traversal\
<br>

```python
while q:
        len_q = len(q)
        res.append([])

        for _ in range(len_q):
            # Add front of queue and remove it from queue
            node = q.pop(0)
            res[curr_level].append(node.data)

            # Enqueue left child
            if node.left is not None:
                q.append(node.left)

            # Enqueue right child
            if node.right is not None:
                q.append(node.right)
        curr_level += 1
    return res


def levelOrderRec(root, level, res):
    # Base case
    if root is None:
        return

    # Add a new level to the result if needed
    if len(res) <= level:
        res.append([])

    # Add current node's data to its corresponding level
    res[level].append(root.data)

    # Recur for left and right children
    level_order_rec(root.left, level + 1, res)
    level_order_rec(root.right, level + 1, res)

# Function to perform level order traversal
def levelOrder(root):
    # Stores the result level by level
    res = []
    level_order_rec(root, 0, res)
    return res
```
