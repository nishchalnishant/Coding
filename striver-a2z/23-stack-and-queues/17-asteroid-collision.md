---
module: striver-a2z/23-stack-and-queues
lesson: 17
topic: Asteroid Collision
difficulty: Medium
source: https://takeuforward.org/learning/dsa/asteroid-collision?category=monotonic-stack&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, simulation]
---
# 17. Asteroid Collision

← [Next Greater Element - 2](16-next-greater-element-ii.md) · [Part 23 index](README.md) · Next → [Sum of Subarray Minimums](18-sum-of-subarray-minimums.md)

> [!abstract] Problem at a glance
> **Task:** Asteroids move right (+) or left (−) at equal speed; simulate all collisions and return the survivors.
> **Key insight:** A collision happens only when a **left-mover meets a right-mover that came before it**. Keep survivors on a stack. A new negative asteroid repeatedly smashes positive tops smaller than itself; equal sizes destroy both; a bigger positive top destroys the newcomer.
> **Difficulty:** Medium · **Pattern:** Stack simulation · **Also on:** [LC 735](https://leetcode.com/problems/asteroid-collision/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/asteroid-collision?category=monotonic-stack&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Repeated passes](#3-repeated-passes) · [4. Stack of survivors](#4-stack-of-survivors) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `asteroids`, where `|a|` is size and the sign is direction (+ right, − left), return the state after all collisions. When two meet, the smaller explodes; equal sizes both explode. Same-direction asteroids never meet.

| Input | Output | Why |
|---|---|---|
| `[5,10,-5]` | `[5,10]` | 10 destroys −5 |
| `[8,-8]` | `[]` | equal: both explode |
| `[10,2,-5]` | `[10]` | −5 destroys 2, then 10 destroys −5 |
| `[-2,-1,1,2]` | `[-2,-1,1,2]` | nothing meets |

**Constraints:** `2 ≤ n ≤ 10⁴`; `−1000 ≤ a[i] ≤ 1000`; `a[i] ≠ 0`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Repeated passes | find any adjacent (+,−) pair, resolve, repeat | O(n²) | O(n) |
| Stack of survivors | new left-mover fights right-moving tops | O(n) | O(n) |

> [!tip] Interview angle
> State the collision condition precisely: only `top > 0 and cur < 0`. Many candidates also collide `top < 0, cur > 0`, but those move apart. Then handle the three outcomes cleanly with a flag or a loop-else.

---

## 3. Repeated passes

**Intuition.** Scan for the first index where `a[i] > 0 > a[i+1]`, resolve that pair, and restart. Stop when no such pair remains.

```python
def asteroids_slow(a):
    a = list(a)
    changed = True
    while changed:
        changed = False
        for i in range(len(a) - 1):
            if a[i] > 0 > a[i + 1]:
                x, y = a[i], -a[i + 1]
                if x > y: del a[i + 1]
                elif x < y: del a[i]
                else: del a[i:i + 2]
                changed = True
                break
    return a
```

**Complexity:** time **O(n²)**, space **O(n)**.

---

## 4. Stack of survivors

**Intuition.** The stack is always a stable state: some left-movers, then some right-movers. A right-mover just gets pushed. A left-mover fights the stack's right-moving tops until it dies, ties, or reaches a left-mover or the bottom.

**Algorithm**

1. For `x` in `asteroids`: `alive = true`.
2. While alive, `x < 0`, and `st.top > 0`: if `st.top < −x` pop and continue; if equal, pop and `alive = false`; else `alive = false`.
3. If `alive`, push `x`.

**Dry run** — [10,2,−5]: push 10, push 2. −5: 2 < 5 pop; 10 > 5 → −5 dies. Result [10].

**C++**
```cpp
vector<int> asteroidCollision(vector<int> asteroids) {
    vector<int> st;
    for (int x : asteroids) {
        bool alive = true;
        while (alive && x < 0 && !st.empty() && st.back() > 0) {
            if (st.back() < -x) { st.pop_back(); continue; }
            if (st.back() == -x) st.pop_back();
            alive = false;
        }
        if (alive) st.push_back(x);
    }
    return st;
}
```

**Java**
```java
static int[] asteroidCollision(int[] asteroids) {
    int[] st = new int[asteroids.length];
    int t = 0;
    for (int x : asteroids) {
        boolean alive = true;
        while (alive && x < 0 && t > 0 && st[t - 1] > 0) {
            if (st[t - 1] < -x) { t--; continue; }
            if (st[t - 1] == -x) t--;
            alive = false;
        }
        if (alive) st[t++] = x;
    }
    return Arrays.copyOf(st, t);
}
```

**Python**
```python
def asteroid_collision(asteroids):
    st = []
    for x in asteroids:
        alive = True
        while alive and x < 0 and st and st[-1] > 0:
            if st[-1] < -x:
                st.pop()
                continue
            if st[-1] == -x:
                st.pop()
            alive = False
        if alive:
            st.append(x)
    return st
```

**Complexity:** time **O(n)**, space **O(n)** — every asteroid is pushed at most once and popped at most once.

---

## Edge cases

- Left-movers at the start never collide.
- Equal sizes: both vanish.
- One huge left-mover clears the whole stack.

---

## Common mistakes

1. Colliding when the top is negative and the new one positive: they move apart.
2. Pushing the left-mover after it tied.
3. Not continuing the fight after the left-mover wins one collision.

---

## Follow-ups

1. Return the number of survivors only?
2. Different speeds?

<details><summary>Answer sketches</summary>

**#1:** Same simulation; return the stack size.

**#2:** Then order of collisions depends on time; it's an event simulation, no longer a stack problem.
</details>

---

## Flashcards

**When do two asteroids collide?** #flashcard
Only when a right-mover is to the left of a left-mover (stack top > 0, current < 0).

**Three outcomes when a left-mover meets a right-moving top?** #flashcard
Top smaller: pop and keep fighting. Equal: pop, newcomer dies. Top bigger: newcomer dies.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
