# Day 18: Bit Manipulation Techniques.

Here are detailed notes for **Day 18: Bit Manipulation Techniques**. This day focuses on understanding bit manipulation, its operations, and solving problems that involve bitwise operations.

***

#### 1. **Bit Manipulation Overview**

Bit manipulation refers to the act of algorithmically manipulating bits or binary digits, which can be very efficient in terms of performance. This technique is widely used in programming, especially in competitive programming and low-level programming tasks.

**1.1 Key Operations**

* **AND (`&`)**: Compares each bit of two numbers. If both bits are 1, the resulting bit is 1.
* **OR (`|`)**: Compares each bit of two numbers. If at least one bit is 1, the resulting bit is 1.
* **XOR (`^`)**: Compares each bit of two numbers. If the bits are different, the resulting bit is 1.
* **NOT (`~`)**: Inverts all bits.
* **Left Shift (`<<`)**: Shifts bits to the left, effectively multiplying the number by (2^n).
* **Right Shift (`>>`)**: Shifts bits to the right, effectively dividing the number by (2^n).

#### 2. **Common Bit Manipulation Techniques**

* **Checking if a number is even or odd**: Use `n & 1`.
* **Swapping two numbers**: Using XOR to swap without a temporary variable.
* **Counting the number of 1s in a binary representation**: Use `n & (n - 1)` in a loop.
* **Finding the only non-repeating element in an array**: Use XOR to cancel out duplicates.

#### 3. **Example Problems**

**3.1 Checking Even or Odd**

```python
def is_even(n):
    return (n & 1) == 0  # Returns True if n is even

# Example Usage
print(is_even(4))  # Output: True
print(is_even(5))  # Output: False
```

**3.2 Swapping Two Numbers**

```python
def swap(a, b):
    a = a ^ b
    b = a ^ b
    a = a ^ b
    return a, b

# Example Usage
x, y = 5, 10
x, y = swap(x, y)
print(x, y)  # Output: 10, 5
```

**3.3 Counting the Number of 1s**

```python
def count_ones(n):
    count = 0
    while n:
        count += 1
        n &= (n - 1)  # Remove the rightmost set bit
    return count

# Example Usage
print(count_ones(7))  # Output: 3 (binary 111)
```

**3.4 Finding the Non-Repeating Element**

```python
def find_non_repeating(arr):
    result = 0
    for num in arr:
        result ^= num
    return result

# Example Usage
print(find_non_repeating([1, 2, 3, 2, 1]))  # Output: 3
```

#### 4. **Common Problems Involving Bit Manipulation**

1. **[Single Number](../../google-sde2/PROBLEM_DETAILS.md#single-number)**: Find the element that appears only once in an array where every other element appears twice.
2. **Power of Two**: Check if a number is a power of two using the condition `n > 0 and (n & (n - 1)) == 0`.
3. **Reverse Bits**: Reverse the bits of a given 32-bit unsigned integer.
4. **Maximum XOR of Two Numbers in an Array**: Find two numbers in an array such that their XOR is maximum.

#### 5. **Practice Problems**

1. **Find Missing Number**: Given an array containing n distinct numbers taken from 0 to n, find the missing number.
2. **Subset XOR**: Given an array, find the maximum XOR subset.
3. **[Total Hamming Distance](../../google-sde2/PROBLEM_DETAILS.md#total-hamming-distance)**: Calculate the total Hamming distance between all pairs of integers in an array.

#### 6. **Tips for Mastering Bit Manipulation**

* **Understand Binary Representation**: Familiarize yourself with how numbers are represented in binary.
* **Practice Common Patterns**: Many bit manipulation problems can be solved using similar patterns.
* **Visualize Operations**: Draw the binary representations to understand how different operations affect them.

#### 7. **When to Use Bit Manipulation**

* **Performance Optimization**: In cases where speed is critical, bit manipulation can be faster than arithmetic operations.
* **Memory Efficiency**: Useful for problems with limited memory constraints, as bits allow for compact storage of information.

By mastering bit manipulation techniques, you'll enhance your programming skills and be better equipped to tackle a variety of problems, especially in coding interviews.
