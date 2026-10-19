---
module: striver/18-recursion
lesson: 23
topic: Sort a stack using recursion
difficulty: Medium
source: https://takeuforward.org/learning/dsa/sort-a-stack?category=medium&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, stack]
---
# 23. Sort a stack using recursion

← [Expression Add Operators](22-expression-add-operators.md) · [Part 18 index](README.md) · Next → [Part 19: Linked List](../19-linked-list/README.md)

> [!abstract] Problem at a glance
> **Task:** Sort a stack so the largest element is on top, using only push/pop/top and recursion (no loops over the stack, no extra container).
> **Key insight:** Do the same thing as reverse-a-stack, but with *sorted* insertion. `sort(st)`: pop the top `x`, sort the rest recursively, then `insertSorted(st, x)`. `insertSorted`: if the stack is empty or `top ≤ x`, push `x`. Otherwise pop the top `t`, insert `x` into the remainder, then push `t` back. This is insertion sort with the call stack acting as the temporary storage.
> **Difficulty:** Medium · **Pattern:** Recursion — hypothesis / induction · **Also on:** [GfG — Sort a stack](https://www.geeksforgeeks.org/problems/sort-a-stack/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/sort-a-stack?category=medium&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Auxiliary stack (iterative)](#3-auxiliary-stack-iterative) · [4. Pure recursion (sort + insertSorted)](#4-pure-recursion-sort--insertsorted) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a stack of integers, sort it so the greatest element is on top. You may only use `push`, `pop`, `top` and `isEmpty`, plus recursion. (Here the stack is shown as a list from bottom to top.)

| Input | Output | Why |
|---|---|---|
| `[3, 1, 4, 2]  (bottom → top)` | `[1, 2, 3, 4]` | top is 4 |
| `[5]` | `[5]` |  |
| `[]` | `[]` |  |

**Constraints:** `0 ≤ n ≤ 500` (recursion depth is O(n)).

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Auxiliary stack (iterative) | move items into tmp, keeping tmp sorted | O(n²) | O(n) |
| Pure recursion (sort + insertSorted) | pop x, sort rest, insert x in place | O(n²) | O(n) call stack |

> [!tip] Interview angle
> Frame it with induction. Hypothesis: `sort(st)` sorts the stack. Induction step: pop `x`, `sort` the rest, then insert `x` in its place. Base case: an empty stack. `insertSorted` uses the same kind of argument, with base case "empty or top ≤ x". Quote O(n²) time and O(n) recursion depth. Mention that an auxiliary stack gives the same O(n²) without recursion.

---

## 3. Auxiliary stack (iterative)

**Intuition.** Pop `x` from the input. While `tmp.top > x`, move `tmp`'s top back onto the input. Then push `x` onto `tmp`. When the input is empty, `tmp` is sorted with the max on top.

```python
def sort_stack_aux(st):
    st = list(st)
    tmp = []
    while st:
        x = st.pop()
        while tmp and tmp[-1] > x:
            st.append(tmp.pop())
        tmp.append(x)
    return tmp
```

**Complexity:** time **O(n²)**, space **O(n)**.

---

## 4. Pure recursion (sort + insertSorted)

**Intuition.** Two mutually simple recursions: one peels elements off, the other drops an element into its sorted position.

**Algorithm**

1. `sort(st)`: if empty return; `x = pop`; `sort(st)`; `insertSorted(st, x)`.
2. `insertSorted(st, x)`: if empty or `top ≤ x`, push `x` and return.
3. Otherwise `t = pop`; `insertSorted(st, x)`; push `t`.

**Dry run** — [3,1,4,2]: pop 2, pop 4, pop 1, pop 3, giving []. Insert 3 → [3]. Insert 1: top 3 > 1, so pop 3, push 1, push 3 → [1,3]. Insert 4 → [1,3,4]. Insert 2: pop 4, pop 3, push 2, push 3, push 4 → [1,2,3,4].

**C++**
```cpp
void insertSorted(vector<int>& st, int x) {
    if (st.empty() || st.back() <= x) { st.push_back(x); return; }
    int t = st.back(); st.pop_back();
    insertSorted(st, x);
    st.push_back(t);
}
void sortRec(vector<int>& st) {
    if (st.empty()) return;
    int x = st.back(); st.pop_back();
    sortRec(st);
    insertSorted(st, x);
}
vector<int> sortStack(vector<int> st) {
    sortRec(st);
    return st;
}
```

**Java**
```java
static void insertSorted(Deque<Integer> st, int x) {
    if (st.isEmpty() || st.peek() <= x) { st.push(x); return; }
    int t = st.pop();
    insertSorted(st, x);
    st.push(t);
}
static void sortRec(Deque<Integer> st) {
    if (st.isEmpty()) return;
    int x = st.pop();
    sortRec(st);
    insertSorted(st, x);
}
static List<Integer> sortStack(int[] a) {
    Deque<Integer> st = new ArrayDeque<>();
    for (int v : a) st.push(v);
    sortRec(st);
    List<Integer> res = new ArrayList<>(st);
    Collections.reverse(res);
    return res;
}
```

**Python**
```python
def sort_stack(st):
    st = list(st)
    def insert_sorted(x):
        if not st or st[-1] <= x:
            st.append(x)
            return
        t = st.pop()
        insert_sorted(x)
        st.append(t)
    def rec():
        if not st:
            return
        x = st.pop()
        rec()
        insert_sorted(x)
    rec()
    return st
```

**Complexity:** time **O(n²)**, space **O(n) call stack** — Each `insertSorted` pops at most the current size, so the total is Σ k = O(n²). The recursion depth is at most n for `sort`, plus n for the nested `insertSorted`.

---

## Edge cases

- Empty stack.
- Already sorted (each insert is O(1), total O(n)).
- Reverse sorted (worst case).
- Duplicates (use `≤` so inserts stop early).

---

## Common mistakes

1. Using a loop over the stack, which the problem forbids.
2. Pushing `x` before restoring `t` in insertSorted, which puts them in the wrong order.
3. Getting the direction wrong (max on top vs. min on top).

---

## Follow-ups

1. Min on top instead?
2. Same trick on a queue?

<details><summary>Answer sketches</summary>

**#1:** Flip the comparison in insertSorted to `top ≥ x`.

**#2:** Rotate and insert, but a queue usually allows a loop of size n. Recursion still gives O(n²).
</details>

---

## Flashcards

**Sort a stack recursively?** #flashcard
pop x → sort rest → insertSorted(x); insertSorted pops larger tops, inserts, then pushes them back.

**Complexity?** #flashcard
O(n²) time, O(n) recursion depth.

**Interview track →** 
