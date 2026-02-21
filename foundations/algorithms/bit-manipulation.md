# Bit Manipulation

Leveraging the binary representation of integers to perform operations efficiently using bitwise operators (`&`, `|`, `^`, `~`, `<<`, `>>`).

## Operators
- **AND (`&`)**: `1 & 1 = 1`, otherwise `0`. Used for masking/clearing bits.
- **OR (`|`)**: `0 | 0 = 0`, otherwise `1`. Used for setting bits.
- **XOR (`^`)**: `1 ^ 0 = 1`, `0 ^ 1 = 1`, otherwise `0`. (Differs = 1). Used for toggling or finding unique numbers (`A ^ A = 0`, `A ^ 0 = A`).
- **NOT (`~`)**: Flips all bits (`0` to `1`, `1` to `0`).
- **Left Shift (`<<`)**: `A << k` multiplies `A` by $2^k$.
- **Right Shift (`>>`)**: `A >> k` divides `A` by $2^k$ (integer division).

## Common Tricks
- **Check if $N$ is Even/Odd**: `(N & 1) == 0` is Even. `== 1` is Odd.
- **Check if $k$-th bit is set**: `(N & (1 << k)) != 0`
- **Set the $k$-th bit**: `N |= (1 << k)`
- **Clear the $k$-th bit**: `N &= ~(1 << k)`
- **Toggle the $k$-th bit**: `N ^= (1 << k)`
- **Clear the lowest set bit**: `N = N & (N - 1)`. Very useful for counting set bits efficiently.
- **Check if Power of 2**: `(N > 0) and (N & (N - 1)) == 0`.

## Common SDE-3 Bit Manipulation Problems
- *Easy*: Number of 1 Bits (Hamming Weight), Power of Two, Missing Number, Single Number.
- *Medium*: Bitwise AND of Numbers Range, Subsets (using bit masking), Single Number II / III, Maximum XOR of Two Numbers in an Array.
- *Hard*: Find Minimum Time to Finish All Jobs (optimizing state with bitmask DP), N-Queens (using bitmasks to track columns and diagonals).
