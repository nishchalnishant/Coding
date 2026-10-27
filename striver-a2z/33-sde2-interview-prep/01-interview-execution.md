---
module: striver-a2z/33-sde2-interview-prep
topic: Coding interview execution
tags: [interview, coding, communication, testing]
---
# 01. Coding Interview Execution

← [Part 33](README.md) · [Pattern triggers](../../03-patterns/patterns-master.md)

A strong interview answer makes the reasoning visible, produces working code, and checks it against meaningful cases. Practice in the language you intend to use, including writing code without relying on autocomplete or a debugger.

## A repeatable 40-minute loop

| Phase | Approx. time | Actions |
|---|---:|---|
| Understand | 3–5 min | Restate the task; clarify input size, duplicates, ordering, mutation, invalid input, and expected output |
| Model | 3–5 min | Work a small example; identify invariants and edge cases; propose a baseline |
| Choose | 3–5 min | Compare approaches and complexity; explain why the chosen one fits the constraints |
| Implement | 15–20 min | Write readable, complete code; narrate decisions without narrating every keystroke |
| Verify | 5–8 min | Dry-run a normal case, a boundary case, and an adversarial case; check complexity |

Use this as a flexible guide, not a stopwatch script. If the problem is simpler, spend the saved time verifying and discussing follow-ups.

## Clarifying questions worth asking

- What are the input bounds, value ranges, and expected complexity?
- Can the input be empty, contain duplicates, or be modified in place?
- Is output order significant? Is any valid answer acceptable?
- How should malformed or impossible input be handled?
- Is the data static, or can updates arrive between queries?

Ask only questions that affect the solution. State sensible assumptions when the prompt already implies them.

## Verification checklist

- Empty and single-element input
- Duplicate values and repeated operations
- Minimum and maximum constraints; integer overflow
- Already sorted, reverse sorted, or all-equal data where relevant
- Disconnected, cyclic, or unreachable cases for graph problems
- Boundary indices and off-by-one conditions
- Correct return value and mutation behavior
- Time and auxiliary-space complexity, including recursion depth

## How to communicate trade-offs

State the simple approach first, then its bottleneck. Introduce the optimization by naming the repeated work it removes. Give complexity in terms of input parameters, and call out assumptions that make it valid. If stuck, share the invariant or subproblem you are working on and test a smaller example.

## Practice prompts

1. Solve a familiar medium problem in 25 minutes while speaking the reasoning aloud.
2. Re-solve it with a changed constraint (streaming input, memory limit, or frequent updates).
3. Review a deliberately buggy solution: find a counterexample, fix it, and explain the regression test.
