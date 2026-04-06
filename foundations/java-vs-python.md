# Java vs Python — For Interview Choice

Brief comparison to help choose and switch between Java and Python for coding interviews. Most of this repo uses **Python** in code examples; the same ideas apply in Java with different syntax and libraries.

## Java

- **Compiled + interpreted**: Source → bytecode (`.class`); runs on JVM. "Write once, run anywhere."
- **Structure**: All executable code lives in classes. Entry point: `public static void main(String[] args)`.
- **Command-line args**: Available in the `args` array passed to `main`.
- **Typing**: Statically typed; explicit types for variables and method signatures.

### Hello World (Java)

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
```

- `public static void main(String[] args)` is the program entry point; `args` holds command-line arguments.
- Requiring code to be in a class and explicitly invoked reduces accidental execution when code is imported.

---

## Python

- **Interpreted**: Run directly; no separate compile step (though bytecode is used internally).
- **Entry point**: Code runs when the script is executed. Use `if __name__ == "__main__":` so that block runs only when the file is run directly, not when imported as a module.
- **Command-line args**: Accessed via `sys.argv` (e.g. `import sys; sys.argv`).
- **Typing**: Dynamically typed by default; optional type hints (e.g. `def f(x: int) -> int:`).

### Hello World (Python)

```python
if __name__ == "__main__":
    print("Hello World")
```

- This block runs only when the script is executed directly, not when imported.

---

## For DSA Interviews

| Aspect | Python | Java |
|--------|--------|------|
| **Speed of writing** | Less boilerplate; list/dict built-in | More verbose; `ArrayList`, `HashMap` |
| **Heap** | `heapq` (min-heap only; negate for max) | `PriorityQueue` |
| **Deque** | `collections.deque` | `ArrayDeque` |
| **Recursion limit** | ~1000 (sys.setrecursionlimit) | Typically larger stack |
| **Strings** | Immutable; use list for in-place simulation | Immutable; use `StringBuilder` for many appends |

Choose one language and stick to it for practice; know its standard library for DSA (collections, heap, sort, etc.). See [algorithms](algorithms/README.md) and [data-structures](data-structures/README.md) for topic-wise content.

---

## See also

- [languages/java/README.md](../languages/java/README.md) — Java book notes  
- [GOOGLE_INTERVIEW_REVISION.md](GOOGLE_INTERVIEW_REVISION.md) — interview revision path
