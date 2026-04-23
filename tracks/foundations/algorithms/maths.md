# Mathematics

Maths concepts frequently appear in algorithm problems to optimize naive $O(N)$ loops down to $O(\sqrt{N})$ or $O(1)$. 

## Core Theory & Algorithms

SDE-2 reference implementations (Python): `../../google-sde2/snippets/python/maths.py`.

- **Prime Numbers**:
  - *Sieve of Eratosthenes*: Find all primes up to $N$ in $O(N \log \log N)$ time.
  - *Primality Test*: Loop from $2$ to $\sqrt{N}$. If $N$ is divisible by any, it's not prime. Time: $O(\sqrt{N})$.
- **GCD & LCM**:
  - *Euclidean Algorithm*: `def gcd(a, b): return a if b == 0 else gcd(b, a % b)` in $O(\log(\min(a,b)))$ time.
  - *LCM*: `(a * b) // gcd(a, b)`
- **Modular Arithmetic**:
  - $(A + B) \mod M = ((A \mod M) + (B \mod M)) \mod M$
  - $(A \times B) \mod M = ((A \mod M) \times (B \mod M)) \mod M$

## Combinatorics & Probability
- **[Problem Details](../../google-sde2/PROBLEM_DETAILS.md#permutations)**: $N!$ ways to arrange $N$ distinct items.
- **Combinations**: $nCr = \frac{n!}{r!(n-r)!}$ ways to choose $r$ items from $n$.
- **Pigeonhole Principle**: If $N$ items are put into $M$ containers ($N > M$), at least one container must hold $> 1$ item.

## Geometry
- **Distance Formula**: $\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$

## Common SDE-3 Math Problems
- *Easy*: Count Primes, Power of Two, Roman to Integer, Excel Sheet Column Title.
- *Medium*: Pow(x,n), Factorial Trailing Zeroes, Rotate Image, Max Points on a Line.
- *Hard*: Basic Calculator, Max Points on a Line, Rectangle Area.

---

## Pattern Recognition

- **Primes** → Sieve (all primes ≤ N) or trial division up to √N for single number.
- **[Problem Details](../../google-sde2/PROBLEM_DETAILS.md#gcd-lcm)** → Euclidean algorithm; LCM = (a×b)/gcd(a,b). **Modular** → (a±b) mod M, (a×b) mod M; use mod at each step to avoid overflow.
- **Combinatorics** → nCr = n!/(r!(n-r)!); permutations n!; pigeonhole for "at least one" arguments.
- **Geometry** → Distance, slope (avoid float when possible; use cross product for collinearity). Max points on a line: group by slope (handle vertical).

## Interview Strategy

- **Identify**: "Count primes" → Sieve. "GCD" / "divisible" → Euclidean. "Ways to choose" → combinations. "Same line" → slope or cross product.
- **Approach**: State formula or algorithm; handle overflow (mod, or use long). Edge cases: zero, negative, large N.
- **Common mistakes**: Integer overflow in (a×b) before mod; division by zero in slope; forgetting 0 and 1 for primes.

## Quick Revision

- **Sieve**: Mark multiples of primes; O(N log log N). **Primality**: Check 2..√N. **GCD**: gcd(a,b)=gcd(b,a%b); O(log min(a,b)).
- **LCM**: (a×b)/gcd(a,b). **Mod**: (a+b) mod M = ((a mod M)+(b mod M)) mod M; same for product.
- **Trailing zeroes in n!**: Count of 5 in 1..n (each 5 contributes at least one 0).

---

## Interview Questions — Logic & Trickiness

| Question | Core logic | Trickiness & details |
|----------|------------|----------------------|
| **Pow(x, n)** | Binary exponentiation: square `x` while halving `n`; multiply result when `n` odd. | **`n < 0`** take reciprocal; **`n = INT_MIN`**—use `long` or halve positive carefully. |
| **Sqrt(x) / Integer Sqrt** | Binary search `ans` in `[0,x]` with `mid <= x // mid`; or **Newton** `x_{k+1} = (x_k + n/x_k)/2`. | **`mid*mid`** overflow—compare with division; **floor** vs **ceil** sqrt. |
| **[Problem Details](../../google-sde2/PROBLEM_DETAILS.md#gcd-lcm)** | **Euclidean** gcd; **LCM** = `a / gcd(a,b) * b` to reduce overflow. | **`gcd(0,a)=a`**; **coprime** check `gcd==1`. |
| **[Problem Details](../../google-sde2/PROBLEM_DETAILS.md#count-primes)** | **Sieve:** mark multiples from each prime `p` starting `p*p`. | **`sqrt(n)`** bound for primes to sieve; **space** O(n)—**segmented** sieve for huge n. |
| **Factorial Trailing Zeroes** | Count **factors of 5** in n! (each 5,25,125…). | **More 2s than 5s**—only count 5s; **legendre** style sum. |
| **Max Points on a Line** | For each anchor, map **reduced slope** `(dy/g, dx/g)` with `g=gcd(|dy|,|dx|)`; handle **vertical** and **duplicates**. | **Same point** add to duplicate counter; **use gcd** to normalize `-2/3` vs `2/-3`. |
| **Random Pick with Weight** | **Prefix sums** `P[i]`; draw `r` in `[0, P[last])`; **binary search** first `P[i] > r`. | **Inclusive/exclusive** random range; **zero** weights excluded. |
| **Integer Break** | For `n≥4`, break into **3s** (maximize product); handle small n by table. | **Greedy** proof via calculus / AM-GM intuition; **DP** for variant constraints. |
| **Arranging Coins** | Find max `k` with `k(k+1)/2 ≤ n` → **binary search** or quadratic formula. | **Integer** overflow in `k*(k+1)`. |
| **Bulb Switcher** | Only bulbs with **square** indices stay on after n toggles—`floor(sqrt(n))`. | **Divisor pairs**—squares have odd # of divisors. |

---

## See also

- [Bit manipulation](bit-manipulation.md) — powers of two, parity  
- [Greedy](greedy.md) — some math scheduling problems  
- [Miscellaneous](miscellaneous.md) — number-theory style mix problems
