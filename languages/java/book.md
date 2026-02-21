# Book



## **Chapter 1: Introduction to Computers, Programs, and Java**

***

#### **1.1 Introduction**

* Programming = creating software (set of instructions for a computer).
* Software is everywhere: from PCs to mobile devices to appliances.
* Learning one language (like Java) helps you transition to others; the core idea is problem-solving using a programming approach.

***

#### **1.2 What is a Computer?**

* **Computer**: Electronic device that processes and stores data using hardware + software.
* **Hardware**: Physical components (CPU, memory, storage, input/output devices).
* **Software**: Invisible instructions controlling hardware (apps, OS, etc.).
* **CPU (Central Processing Unit)**:
  * "Brain" of the computer.
  * Executes instructions from memory.
  * Components: Control Unit + Arithmetic/Logic Unit.
  * Measured in GHz (e.g., 3 GHz = 3 billion pulses/sec).
  * Multicore CPUs enable parallel processing.
* **Bits and Bytes**:
  * Bit = 0 or 1 (binary digit), smallest data unit.
  * Byte = 8 bits.
* **Memory (RAM)**:
  * Volatile storage for data/instructions.
  * Each byte has a unique address.
* **Storage Devices**:
  * Non-volatile (e.g., hard disks, SSDs, USBs, CDs).
  * Used to permanently store data and programs.
* **Input/Output Devices**: Keyboard, mouse, monitor, printer, etc.
* **Communication Devices**: Modems, network cards, Wi-Fi adapters.

***

#### **1.3 Programming Languages**

* Types:
  1. **Machine Language**: Native binary code (hard to read).
  2. **Assembly Language**: Uses mnemonics like `add`, `sub`.
     * Needs an **assembler**.
  3. **High-Level Language** (e.g., Java, Python, C++):
     * English-like, platform-independent.
     * Needs a **compiler** or **interpreter**.
* **Source Program**: Code written in a high-level language.
* **Compiler**: Translates entire source code into machine code (e.g., `javac`).
* **Interpreter**: Translates and executes one line at a time.

***

#### **1.4 Operating Systems**

* Manages hardware/software.
* Examples: Windows, macOS, Linux.
* Responsibilities:
  * Control hardware.
  * Allocate resources.
  * Schedule operations (multiprogramming, multithreading).

***

#### **1.5 Java, the World Wide Web, and Beyond**

* Java was designed to be:
  * **Platform-independent**: “Write once, run anywhere.”
  * Used for: Web applications, Android apps, server-side development.
* **Applets**: Java programs that run in a browser (now largely deprecated).
* Java is used for Web, mobile, desktop, and embedded systems.

***

#### **1.6 Java Language Specification, API, JDK, and IDE**

* **Java Language Specification**: Syntax and semantics rules.
* **API (Application Programming Interface)**: Predefined Java classes and libraries.
* **JDK (Java Development Kit)**: Contains compiler, debugger, JVM.
* **IDE (e.g., Eclipse, NetBeans)**: Tools for code writing, debugging, and compiling.

***

#### **1.7 A Simple Java Program**

```java
public class Welcome {
    public static void main(String[] args) {
        System.out.println("Welcome to Java!");
    }
}
```

* **main()**: Entry point of a Java application.
* Java is case-sensitive.
* Every statement ends with `;`.

***

#### **1.8 Creating, Compiling, and Executing a Java Program**

* Save code in a `.java` file.
* Compile using: `javac FileName.java` → creates `.class` bytecode.
* Run using: `java ClassName`.
* Java uses **JVM** to execute bytecode on any OS.

***

#### **1.9 Displaying Text in a Message Dialog Box**

* Use `JOptionPane` from `javax.swing`:

```java
import javax.swing.JOptionPane;
JOptionPane.showMessageDialog(null, "Welcome to Java!");
```

***

#### **1.10 Programming Style and Documentation**

* **Good Practices**:
  * Use indentation.
  * Add comments (`//` or `/* */`).
  * Use meaningful names.
* **Comments** are ignored by the compiler but improve code readability.

***

#### **1.11 Programming Errors**

* **Syntax Errors**: Grammar mistakes (e.g., missing `;`).
* **Runtime Errors**: Occur during execution (e.g., divide by zero).
* **Logic Errors**: Program runs but gives incorrect output due to flawed logic.

***

#### ✅ **Key Terms Summary**

* **Bit, Byte, CPU, RAM, Compiler, Interpreter, JDK, JVM, API**, etc.
* Learn distinctions: low-level vs high-level languages, source vs bytecode, OS vs application software.

***

## &#x20;**Chapter 2: Elementary Programming**

***

### 📘 **Chapter 2: Elementary Programming**

This chapter introduces the **fundamental building blocks of Java programming**, focusing on writing programs that perform basic computations, process input, and display output.

***

#### **2.1 Introduction**

* You move beyond printing simple messages to writing **meaningful programs** that solve real-world problems (e.g., computing loan payments).
* Key skills:
  * Data storage (variables)
  * Computation (expressions)
  * Input/output handling

***

#### **2.2 Writing a Simple Program**

* Programs solve problems using **algorithms** (step-by-step solutions).
* Typical program development involves:
  1. Understand the problem.
  2. Design an algorithm.
  3. Translate it into code.
*   Example: Area of a circle.

    ```java
    area = radius * radius * π;
    ```

***

#### **2.3 Reading Input from the Console**

*   Java uses the `Scanner` class for input.

    ```java
    import java.util.Scanner;
    Scanner input = new Scanner(System.in);
    double radius = input.nextDouble();
    ```
* Console input allows interaction with users.

***

#### **2.4 Identifiers**

* Identifiers are names for **variables, methods, classes**, etc.
* Rules:
  * Can include letters, digits, `_`, `$`.
  * Cannot start with a digit.
  * Cannot be a Java keyword (like `int`, `class`).

***

#### **2.5 Variables**

*   Used to store data in a program.

    ```java
    int age = 25;
    double area;
    ```
* Must be **declared before use**.
*   Can be updated:

    ```java
    area = radius * radius * 3.14159;
    ```

***

#### **2.6 Assignment Statements and Expressions**

*   Use `=` to assign values:

    ```java
    x = 5;
    y = x + 2;
    ```
* Right-hand side is evaluated first.

***

#### **2.7 Named Constants**

*   Constant values are declared using `final`.

    ```java
    final double PI = 3.14159;
    ```
* Constants improve **readability** and **maintenance**.

***

#### **2.8 Naming Conventions**

* **Classes**: Capitalize each word (e.g., `ComputeArea`).
* **Variables and methods**: start lowercase, use camelCase (e.g., `area`, `computeArea`).
* **Constants**: ALL\_CAPS (e.g., `PI`, `MAX_SPEED`).

***

#### **2.9 Numeric Data Types and Operations**

* Java supports six numeric types:
  * Integer: `byte`, `short`, `int`, `long`
  * Floating point: `float`, `double`
* **Arithmetic operators**:
  * `+`, `-`, `*`, `/`, `%` (modulus)
  * `Math.pow(a, b)` for exponentiation

***

#### **2.10 Numeric Literals**

* `int`, `long` (suffix `L`), `float` (suffix `F`), `double`
* Scientific notation: `1.23e2` = 123.0

***

#### **2.11 Evaluating Expressions and Operator Precedence**

* Follow standard precedence rules:
  * `*`, `/`, `%` > `+`, `-`
* Parentheses can change precedence.

***

#### **2.12 Case Study: Displaying the Current Time**

* Use `System.currentTimeMillis()` to get milliseconds since Jan 1, 1970.
* Calculate hours, minutes, seconds using division and modulus.

***

#### **2.13 Augmented Assignment Operators**

*   Shorthand:

    ```java
    x += 1; // same as x = x + 1;
    x *= 2;
    ```

***

#### **2.14 Increment and Decrement Operators**

* `++` and `--`
  * **Pre**: `++x` (increment first)
  * **Post**: `x++` (use then increment)

***

#### **2.15 Numeric Type Conversions**

* **Widening** (safe): `int` → `double`
*   **Narrowing** (may lose data): must use **casting**

    ```java
    int x = (int) 3.14;
    ```

***

#### **2.16 Software Development Process**

Five steps:

1. Problem definition
2. Algorithm design
3. Code implementation
4. Testing and debugging
5. Maintenance

**Case study: Loan calculator**

```java
monthlyPayment = loanAmount * monthlyInterestRate /
                 (1 - 1 / Math.pow(1 + monthlyInterestRate, numberOfYears * 12));
```

***

#### **2.17 Character Data Type and Operations**

*   Use `char` to represent a single character:

    ```java
    char letter = 'A';
    ```
* Each char is a Unicode number.
* `int` and `char` are compatible (e.g., `'A' + 1 = 'B'`).

***

#### **2.18 The String Type**

*   A `String` is a sequence of characters (not a primitive).

    ```java
    String name = "John";
    ```
* Common methods:
  * `length()`
  * `toLowerCase()`, `toUpperCase()`
  * `charAt(i)`, `concat()`

***

#### **2.19 Getting Input from Input Dialogs**

*   Uses `JOptionPane` for GUI-based input/output:

    ```java
    String name = JOptionPane.showInputDialog("Enter your name");
    ```

***

### ✅ Summary Table

| Concept              | Example                                   | Notes                           |
| -------------------- | ----------------------------------------- | ------------------------------- |
| Variable Declaration | `int count;`                              | Must declare before use         |
| Constant             | `final double PI = 3.14;`                 | Value cannot change             |
| Input (Console)      | `Scanner input = new Scanner(System.in);` | Use `nextInt()`, `nextDouble()` |
| Input (GUI)          | `JOptionPane.showInputDialog(...)`        | String returned                 |
| Math                 | `Math.pow(x, y)`                          | For exponents                   |
| Char → Int           | `int code = 'A';`                         | Outputs 65                      |
| Casting              | `(int) 3.5` → `3`                         | Converts to integer             |
| Operators            | `+ - * / %`                               | Standard math ops               |

***

Here are the **detailed notes for Chapter 3: Selections** from _Introduction to Java Programming, 9th Edition by Y. Daniel Liang_:

***

### 📘 Chapter 3: Selections

This chapter introduces how to make decisions in Java programs using selection (conditional) statements such as `if`, `if-else`, `switch`, and logical operators.

***

#### **3.1 Introduction**

* Sometimes a program needs to make decisions (e.g., only compute area if radius ≥ 0).
* Java provides _selection statements_ to control program flow based on conditions.
* Conditions use **Boolean expressions** that evaluate to `true` or `false`.

***

#### **3.2 `boolean` Data Type**

*   Declares variables that hold `true` or `false`.

    ```java
    boolean isValid = true;
    ```
* **Comparison Operators**:
  * `<`, `<=`, `>`, `>=`, `==`, `!=`
  *   Example:

      ```java
      if (radius >= 0)
      ```

***

#### **3.3 `if` Statements**

*   One-way selection:

    ```java
    if (score >= 60)
        System.out.println("Passed");
    ```

***

#### **3.4 Case Study: Guessing Birthdays**

* Demonstrates using `if` to accumulate a guessed date based on user input.

***

#### **3.5 Two-Way `if-else` Statements**

*   Provides two branches:

    ```java
    if (x > 0)
        System.out.println("Positive");
    else
        System.out.println("Zero or negative");
    ```

***

#### **3.6 Nested and Multi-Way `if-else`**

*   Multiple levels of conditions:

    ```java
    if (score >= 90)
        grade = 'A';
    else if (score >= 80)
        grade = 'B';
    // etc.
    ```

***

#### **3.7 Common Errors**

* **Dangling else problem**: Always pair `else` with nearest unmatched `if`.
* Use braces `{}` to avoid ambiguity and logic errors.

***

#### **3.8 Generating Random Numbers**

*   Use `Math.random()`:

    ```java
    int number = (int)(Math.random() * 10);
    ```

***

#### **3.9 Case Study: BMI Calculator**

*   Compute BMI using:

    ```java
    bmi = weight / (height * height);
    ```

***

#### **3.10 Case Study: Tax Calculator**

* Multi-way branching based on income and filing status.

***

#### **3.11 Logical Operators**

*   Combine conditions:

    * `&&` (AND), `||` (OR), `!` (NOT)

    ```java
    if (x > 0 && x < 100)
    ```

***

#### **3.12 Case Study: Leap Year**

*   Leap year condition:

    ```java
    if ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0)
    ```

***

#### **3.13 Case Study: Lottery Game**

* Compares generated and user input digits using selection and logic.

***

#### **3.14 `switch` Statements**

*   Useful for discrete choices:

    ```java
    switch (grade) {
        case 'A': ...
        case 'B': ...
        default: ...
    }
    ```

***

#### **3.15 Conditional (Ternary) Operator**

*   Shorthand for `if-else`:

    ```java
    result = (x > 0) ? "Positive" : "Non-positive";
    ```

***

#### **3.16 Formatting Output**

*   Use `System.out.printf` for formatted output:

    ```java
    System.out.printf("Age: %d, GPA: %.2f", age, gpa);
    ```

***

#### **3.17 Operator Precedence and Associativity**

* Precedence: `*`, `/`, `%` > `+`, `-` > comparison > logical
* Use parentheses to enforce desired order.

***

#### **3.18 Confirmation Dialogs**

*   Use `JOptionPane.showConfirmDialog(...)` for user decisions:

    ```java
    int option = JOptionPane.showConfirmDialog(null, "Continue?");
    ```

***

#### **3.19 Debugging**

* Debugging involves:
  * Setting breakpoints
  * Tracing variable values
  * Stepping through code

***

#### ✅ **Key Concepts Summary**

| Topic              | Description                                 |
| ------------------ | ------------------------------------------- |
| Boolean type       | `true` or `false`                           |
| Comparison ops     | `<`, `>`, `==`, `!=`, etc.                  |
| Logical ops        | `&&`, \`                                    |
| Control structures | `if`, `if-else`, `switch`, ternary `? :`    |
| Random numbers     | `Math.random()`                             |
| Formatting         | `System.out.printf()`                       |
| Dialogs            | `JOptionPane` for input/output/confirmation |

***

Here are **detailed notes for Chapter 4: Loops** from _Introduction to Java Programming, 9th Edition by Y. Daniel Liang_:

***

### 📘 Chapter 4: Loops

Loops are fundamental constructs in programming that allow repeated execution of a set of statements.

***

#### **4.1 Introduction**

* Loops automate repetitive tasks.
*   Example:

    ```java
    int count = 0;
    while (count < 100) {
        System.out.println("Welcome to Java!");
        count++;
    }
    ```
* Loop consists of:
  * **Initialization**
  * **Condition check**
  * **Loop body**
  * **Update**

***

#### **4.2 The `while` Loop**

*   Syntax:

    ```java
    while (condition) {
        // Loop body
    }
    ```
* Condition is checked _before_ the loop body.
* Might never execute if condition is initially false.
* Used when repetitions are not known in advance.

***

#### **4.2.1–4.2.3 Loop Design Strategy**

* Steps:
  1. Identify tasks that repeat.
  2. Determine loop control structure.
  3. Design and test the loop carefully.
* Avoid **infinite loops** and **off-by-one errors**.

***

#### **4.2.4 Sentinel-Controlled Loops**

*   A **sentinel value** ends input:

    ```java
    int data = input.nextInt();
    while (data != 0) {
        sum += data;
        data = input.nextInt();
    }
    ```

***

#### **4.2.5 Input Redirection**

* Redirect input from a file using `< input.txt`.

***

#### **4.3 The `do-while` Loop**

* Executes loop body **once before** checking the condition.
*   Syntax:

    ```java
    do {
        // Loop body
    } while (condition);
    ```

***

#### **4.4 The `for` Loop**

*   Syntax:

    ```java
    for (initialization; condition; update) {
        // Loop body
    }
    ```
* Used when number of iterations is known.
* All parts (init, condition, update) are optional.
*   Example:

    ```java
    for (int i = 0; i < 10; i++) {
        System.out.println(i);
    }
    ```

***

#### **4.5 Which Loop to Use**

* Use `for` when number of iterations is known.
* Use `while` when condition is pre-evaluated.
* Use `do-while` when at least one execution is needed.

***

#### **4.6 Nested Loops**

* A loop inside another loop.
* Commonly used in tables or matrix processing.
*   Example: Multiplication table:

    ```java
    for (int i = 1; i <= 9; i++) {
        for (int j = 1; j <= 9; j++) {
            System.out.printf("%4d", i * j);
        }
        System.out.println();
    }
    ```

***

#### **4.7 Minimizing Numeric Errors**

* Floating-point operations can be imprecise.
* Example: summing from 0.01 to 1.0
  * Summing small to large gives more accurate results than large to small.

***

#### **4.8 Case Studies**

*   **GCD Calculation**:

    ```java
    int gcd = 1;
    for (int k = 2; k <= n1 && k <= n2; k++) {
        if (n1 % k == 0 && n2 % k == 0)
            gcd = k;
    }
    ```
* **Future Tuition Prediction**
* **Monte Carlo Simulation**

***

#### **4.9 `break` and `continue`**

* `break`: exits the loop immediately.
* `continue`: skips the current iteration and moves to the next.
*   Example:

    ```java
    for (int i = 0; i < 10; i++) {
        if (i == 5) continue;
        System.out.println(i);
    }
    ```

***

#### **4.10 Case Study: Prime Numbers**

* Checks if a number is divisible only by 1 and itself using loops.

***

#### **4.11 Loop Control with Confirmation Dialog**

*   GUI-based loop control using `JOptionPane`:

    ```java
    int option = JOptionPane.YES_OPTION;
    while (option == JOptionPane.YES_OPTION) {
        // input logic
        option = JOptionPane.showConfirmDialog(null, "Continue?");
    }
    ```

***

### ✅ Chapter 4 Summary

| Concept            | Description                                        |
| ------------------ | -------------------------------------------------- |
| `while` loop       | Pretest loop; repeats while condition is true      |
| `do-while` loop    | Posttest loop; always runs at least once           |
| `for` loop         | Pretest; concise form with init, condition, update |
| Sentinel value     | Special input value to terminate loop              |
| Nested loop        | Loop inside another loop                           |
| `break`            | Terminates the loop early                          |
| `continue`         | Skips to next iteration                            |
| Numeric precision  | Watch for floating-point errors                    |
| Dialog-based loops | Uses GUI for flow control                          |

***

Here's a concise **cheat sheet for Chapter 5: Methods** from _Introduction to Java Programming, 9th Edition by Y. Daniel Liang_:

***

### 🧠 **Java Methods Cheat Sheet – Chapter 5**

***

#### 📌 **5.1 What is a Method?**

* A **method** is a block of code that performs a specific task.
* Benefits:
  * Reuse code
  * Improve modularity
  * Enhance readability and debugging

***

#### 📌 **5.2 Defining a Method**

```java
public static returnType methodName(parameters) {
    // method body
}
```

* **Example:**

```java
public static int max(int num1, int num2) {
    return (num1 > num2) ? num1 : num2;
}
```

***

#### 📌 **5.3 Calling a Method**

```java
int larger = max(5, 10);
```

* Must match number, type, and order of arguments.

***

#### 📌 **5.4 `void` Method Example**

```java
public static void printMessage() {
    System.out.println("Hello!");
}
```

* Use `void` when no return value is needed.

***

#### 📌 **5.5 Passing Parameters by Value**

* Java uses **pass-by-value** for all arguments.
* Primitives: Copy of the value.
* Objects: Copy of the **reference** (not the actual object).

***

#### 📌 **5.6 Modularizing Code**

* **Modularization**: Breaking code into smaller, reusable methods.
* Increases code maintainability and clarity.

***

#### 📌 **5.7 Case Study: Decimal to Hex**

* Break the problem into sub-methods:
  * `decimalToHex(int decimal)`
  * `toHexChar(int value)`

***

#### 📌 **5.8 Method Overloading**

* Define multiple methods with the same name but different parameter lists.

```java
public static int max(int a, int b)
public static double max(double a, double b)
```

* Compiler picks the appropriate version based on arguments.

***

#### 📌 **5.9 Scope of Variables**

* **Local variable**: Declared inside a method or block; not visible outside.
* **Global (class-level)** variables not used yet (introduced in OOP chapters).

***

#### 📌 **5.10 The Math Class**

* Java's built-in class for common math operations.

```java
Math.pow(x, y);     // exponentiation
Math.sqrt(x);       // square root
Math.random();      // [0.0, 1.0)
Math.abs(x);        // absolute value
```

***

#### 📌 **5.11 Case Study: Random Characters**

* Uses `RandomCharacter` class with methods like:
  * `getRandomUpperCaseLetter()`
  * `getRandomDigitCharacter()`

***

#### 📌 **5.12 Method Abstraction & Stepwise Refinement**

* **Abstraction**: Use methods without knowing implementation details.
* **Stepwise Refinement**: Break down problems into smaller subproblems recursively.
* Think of methods as **black boxes**:
  * You know what it does, not how it works inside.

***

### ✅ Common Patterns & Syntax

| Purpose          | Syntax / Example                      |
| ---------------- | ------------------------------------- |
| Define method    | `public static int sum(int a, int b)` |
| Call method      | `sum(5, 10)`                          |
| No return        | `public static void printHello()`     |
| Return statement | `return value;`                       |
| Overloading      | Same name, different parameters       |
| Math class       | `Math.max(x, y)`                      |
| Random number    | `(int)(Math.random() * 10)`           |

***

### 🚫 Common Mistakes to Avoid

* Not matching parameter types/number in method call.
* Forgetting `return` statement for non-void methods.
* Using a variable outside its scope.

***

Here’s a **Cheat Sheet for Chapter 6: Single-Dimensional Arrays** from _Introduction to Java Programming (9th Edition) by Y. Daniel Liang_:

***

### 🧠 **Java Arrays – Chapter 6 Cheat Sheet**

***

#### 🔹 **What is an Array?**

* A **data structure** to store multiple values of the **same type**.
* Elements are stored in **contiguous memory** and accessed via an index.

```java
double[] numbers = new double[10];
numbers[0] = 1.5;
```

***

#### 🔹 **Declaring & Creating Arrays**

```java
int[] scores;                   // Declaration
scores = new int[5];           // Creation
int[] ages = new int[10];      // Combined
```

* Index starts from `0`.
* Access using `array[index]`.

***

#### 🔹 **Array Initialization**

```java
int[] list = {1, 2, 3, 4}; // array initializer
```

```java
int[] list = new int[5];  // default values: 0 for int, false for boolean, '\u0000' for char
```

***

#### 🔹 **Common Array Operations**

| Task    | Example                             |
| ------- | ----------------------------------- |
| Input   | `list[i] = input.nextInt();`        |
| Output  | `System.out.println(list[i]);`      |
| Sum     | `sum += list[i];`                   |
| Max     | `if (list[i] > max)`                |
| Shuffle | Use `Math.random()` + swap logic    |
| Shift   | Manually copy values to new indices |

***

#### 🔹 **Looping Through Arrays**

```java
for (int i = 0; i < list.length; i++) {
    System.out.println(list[i]);
}
```

#### 🔹 **Enhanced `for-each` Loop**

```java
for (int item : list) {
    System.out.println(item);
}
```

***

#### 🔹 **Passing Arrays to Methods**

```java
public static void printArray(int[] arr) {
    for (int i : arr) System.out.print(i + " ");
}
```

#### 🔹 **Returning Arrays from Methods**

```java
public static int[] createArray() {
    int[] arr = {1, 2, 3};
    return arr;
}
```

***

#### 🔹 **Variable-Length Argument Lists**

```java
public static int sum(int... numbers) {
    int total = 0;
    for (int n : numbers) total += n;
    return total;
}
```

***

#### 🔹 **Searching Arrays**

*   **Linear Search**:

    ```java
    for (int i = 0; i < arr.length; i++)
        if (arr[i] == key) return i;
    ```
*   **Binary Search** (sorted arrays only):

    ```java
    Arrays.binarySearch(arr, key);
    ```

***

#### 🔹 **Sorting Arrays**

* **Selection Sort**, **Insertion Sort**: Manual sorting methods
*   **Built-in sort**:

    ```java
    Arrays.sort(arr);
    ```

***

#### 🔹 **The `java.util.Arrays` Class**

```java
Arrays.sort(arr);                     // Sort
Arrays.binarySearch(arr, key);       // Search
Arrays.equals(arr1, arr2);           // Compare
Arrays.fill(arr, 5);                 // Fill with value
Arrays.toString(arr);                // Print array
```

***

#### 🔹 **Case Studies**

* **LottoNumbers**: Random, unique number selection.
* **DeckOfCards**: Simulate shuffling and dealing cards.
* **Counting Letters**: Count occurrences of characters using `char[]`.

***

### ✅ Quick Tips

* Index out of bounds? You’ll get `ArrayIndexOutOfBoundsException`.
* Array size is fixed once declared.
* Use `.length` to get array size (e.g., `arr.length`).
* Off-by-one errors are common—check loop bounds carefully!

***

Here's a **cheat sheet for Chapter 7: Multidimensional Arrays** from _Introduction to Java Programming, 9th Edition by Y. Daniel Liang_:

***

### 🧠 **Chapter 7: Multidimensional Arrays – Cheat Sheet**

***

#### 🔹 **Two-Dimensional Arrays (2D Arrays)**

**✅ Declaration:**

```java
int[][] matrix;
```

**✅ Creation:**

```java
matrix = new int[3][4]; // 3 rows, 4 columns
```

**✅ Initialization:**

```java
int[][] matrix = {
  {1, 2, 3},
  {4, 5, 6},
  {7, 8, 9}
};
```

**✅ Accessing Elements:**

```java
matrix[1][2] // 6 (2nd row, 3rd column)
```

***

#### 🔹 **Key Properties**

* `matrix.length` → Number of rows
* `matrix[0].length` → Number of columns (of first row)
* Java 2D arrays are arrays of arrays (ragged arrays are allowed).

***

#### 🔹 **Ragged Arrays**

```java
int[][] ragged = new int[3][];
ragged[0] = new int[2];
ragged[1] = new int[4];
ragged[2] = new int[3];
```

***

#### 🔹 **Common Operations**

**🔸 Input a 2D Array:**

```java
for (int i = 0; i < matrix.length; i++)
  for (int j = 0; j < matrix[i].length; j++)
    matrix[i][j] = input.nextInt();
```

**🔸 Print a 2D Array:**

```java
for (int[] row : matrix)
  System.out.println(Arrays.toString(row));
```

**🔸 Sum All Elements:**

```java
int total = 0;
for (int i = 0; i < matrix.length; i++)
  for (int j = 0; j < matrix[i].length; j++)
    total += matrix[i][j];
```

**🔸 Sum by Column:**

```java
for (int col = 0; col < matrix[0].length; col++) {
  int total = 0;
  for (int row = 0; row < matrix.length; row++)
    total += matrix[row][col];
  System.out.println("Sum for column " + col + " is " + total);
}
```

**🔸 Find Row with Maximum Sum:**

```java
int maxRow = 0, maxSum = 0;
for (int i = 0; i < matrix.length; i++) {
  int rowSum = Arrays.stream(matrix[i]).sum();
  if (rowSum > maxSum) {
    maxSum = rowSum;
    maxRow = i;
  }
}
```

**🔸 Shuffle Elements:**

```java
for (int i = 0; i < matrix.length; i++)
  for (int j = 0; j < matrix[i].length; j++) {
    int i1 = (int)(Math.random() * matrix.length);
    int j1 = (int)(Math.random() * matrix[i].length);
    int temp = matrix[i][j];
    matrix[i][j] = matrix[i1][j1];
    matrix[i1][j1] = temp;
  }
```

***

#### 🔹 **Passing 2D Arrays to Methods**

```java
public static void printMatrix(int[][] m) {
  for (int[] row : m)
    System.out.println(Arrays.toString(row));
}
```

***

#### 🔹 **Case Studies**

* **Grading Multiple-Choice Tests**: Rows represent students, columns represent answers.
* **Closest Pair of Points**: Use 2D array to store coordinates.
* **Sudoku Checker**: Validate 9×9 matrix with nested loops.
* **Weather Analysis**: 3D array to track temperature and humidity across time.

***

#### 🔹 **Multidimensional Arrays (3D and beyond)**

**✅ Declaration:**

```java
int[][][] data = new int[10][24][2];
```

**✅ Example:**

```java
data[day][hour][0] = temperature;
data[day][hour][1] = humidity;
```

***

### ✅ Summary Table

| Task             | Syntax                                  |
| ---------------- | --------------------------------------- |
| Declare 2D array | `int[][] m;`                            |
| Create 2D array  | `new int[3][4]`                         |
| Access element   | `m[i][j]`                               |
| Iterate rows     | `for (int i = 0; i < m.length; i++)`    |
| Iterate columns  | `for (int j = 0; j < m[i].length; j++)` |
| Ragged arrays    | Rows can have different lengths         |
| 3D arrays        | `int[][][] x = new int[5][4][3]`        |

***

Here is a **cheat sheet for Chapter 8: Objects and Classes** from _Introduction to Java Programming, 9th Edition by Y. Daniel Liang_:

***

### 🧠 Java OOP – Chapter 8: Objects and Classes Cheat Sheet

***

#### 🔹 **Object-Oriented Programming (OOP) Basics**

| Term              | Description                                                    |
| ----------------- | -------------------------------------------------------------- |
| **Object**        | Instance of a class with state (fields) and behavior (methods) |
| **Class**         | Template or blueprint to create objects                        |
| **Instance**      | An actual object created from a class                          |
| **Instantiation** | The process of creating an object using `new`                  |

***

#### 🔹 **Defining a Class**

```java
public class Circle {
    double radius = 1.0;

    public Circle() { }

    public Circle(double r) {
        radius = r;
    }

    public double getArea() {
        return radius * radius * Math.PI;
    }

    public void setRadius(double r) {
        radius = r;
    }
}
```

***

#### 🔹 **Creating Objects**

```java
Circle c1 = new Circle();         // Default constructor
Circle c2 = new Circle(5.0);      // Overloaded constructor
```

***

#### 🔹 **Accessing Members**

* **Fields/Methods**: `objectName.member`

```java
System.out.println(c2.getArea());
c2.setRadius(10.0);
```

***

#### 🔹 **Constructors**

* Special methods with the same name as the class
* No return type (not even `void`)
* Used with `new` to create objects

```java
public Circle() { ... }
public Circle(double r) { ... }
```

***

#### 🔹 **Reference Variables**

```java
Circle myCircle = new Circle();
```

* Stores a **reference** (memory address) to the object, not the object itself.

***

#### 🔹 **UML Class Diagram Format**

```
ClassName
--------------
fieldName: dataType
--------------
methodName(params): returnType
```

***

#### 🔹 **Using Standard Java Classes**

* `Date`: `new java.util.Date()`
* `Random`: `new java.util.Random()`
* `JFrame`: GUI window class in Swing

***

#### 🔹 **Static Members**

| Static Keyword | Description                 |
| -------------- | --------------------------- |
| `static`       | Shared across all instances |
| Example:       |                             |

```java
public static int count;
public static void showCount() { ... }
```

* Access: `ClassName.member` or `object.member` (prefer class style)

***

#### 🔹 **Visibility Modifiers**

| Modifier      | Access Level          |
| ------------- | --------------------- |
| `public`      | Anywhere              |
| `private`     | Inside the class only |
| (no modifier) | Package-private       |

***

#### 🔹 **Encapsulation**

* Hide data using `private` fields
* Provide **getters/setters** to access/update

```java
private double radius;

public double getRadius() { return radius; }
public void setRadius(double r) { radius = r; }
```

***

#### 🔹 **Passing Objects to Methods**

* Passes the **reference** (not copy of object)
* Object data can be changed via methods

***

#### 🔹 **Arrays of Objects**

```java
Circle[] circles = new Circle[10];
for (int i = 0; i < circles.length; i++) {
    circles[i] = new Circle(Math.random() * 100);
}
```

***

#### ✅ Summary Table

| Concept            | Example / Syntax                      |
| ------------------ | ------------------------------------- |
| Define Class       | `class ClassName { ... }`             |
| Create Object      | `new ClassName()`                     |
| Access Field       | `object.field`                        |
| Call Method        | `object.method()`                     |
| Constructor        | `ClassName(...) { ... }`              |
| Static Variable    | `static int x;`                       |
| Getter/Setter      | `getX()`, `setX()`                    |
| Reference Variable | `ClassName ref = new ClassName();`    |
| Array of Objects   | `ClassName[] arr = new ClassName[n];` |

***

Here’s a **cheat sheet for Chapter 9: Strings and Text I/O** from _Introduction to Java Programming, 9th Edition by Y. Daniel Liang_:

***

### 🧠 **Java Strings & Text I/O – Chapter 9 Cheat Sheet**

***

#### 🔹 **9.1 Introduction**

* Java provides `String`, `StringBuilder`, and `StringBuffer` for processing textual data.
* Strings in Java are **objects**, not arrays of characters like in C.

***

#### 🔹 **9.2 The `String` Class**

**✅ Creating Strings**

```java
String s1 = "Java";
String s2 = new String("Java");
char[] chars = {'J', 'a', 'v', 'a'};
String s3 = new String(chars);
```

**✅ Immutable Strings**

* Strings **cannot be changed** after creation.

```java
String s = "Java";
s = "HTML"; // new object created
```

**✅ Interned Strings**

* JVM stores **string literals in a common pool**.

```java
String s1 = "Java";
String s2 = "Java";
s1 == s2 // true (same reference)
```

***

#### 🔹 **String Operations**

| Operation     | Example                               |
| ------------- | ------------------------------------- |
| Length        | `s.length()`                          |
| Char at index | `s.charAt(i)`                         |
| Substring     | `s.substring(0, 5)`                   |
| Concatenation | `s1 + s2` or `s1.concat(s2)`          |
| Comparison    | `s1.equals(s2)` or `s1.compareTo(s2)` |
| Replace       | `s.replace('a', 'b')`                 |
| Trim spaces   | `s.trim()`                            |
| Convert case  | `s.toLowerCase()`, `s.toUpperCase()`  |
| Split         | `s.split(" ")`                        |

***

#### 🔹 **9.3 Palindrome Check**

```java
public static boolean isPalindrome(String s) {
  int low = 0, high = s.length() - 1;
  while (low < high) {
    if (s.charAt(low) != s.charAt(high)) return false;
    low++; high--;
  }
  return true;
}
```

***

#### 🔹 **9.4 Hex to Decimal**

```java
int decimal = Integer.parseInt("1A", 16);
```

***

#### 🔹 **9.5 The `Character` Class**

| Method            | Purpose          |
| ----------------- | ---------------- |
| `isLetter(ch)`    | Check if letter  |
| `isDigit(ch)`     | Check if digit   |
| `isUpperCase(ch)` | Check uppercase  |
| `isLowerCase(ch)` | Check lowercase  |
| `toUpperCase(ch)` | Convert to upper |
| `toLowerCase(ch)` | Convert to lower |

***

#### 🔹 **9.6 `StringBuilder` and `StringBuffer`**

| Feature      | StringBuilder | StringBuffer |
| ------------ | ------------- | ------------ |
| Mutable?     | ✅ Yes         | ✅ Yes        |
| Thread-safe? | ❌ No          | ✅ Yes        |
| Usage        |               |              |

```java
StringBuilder sb = new StringBuilder("Java");
sb.append(" Rocks");
```

\| Common Methods |

```java
sb.append("text");
sb.insert(0, "Hey ");
sb.delete(2, 4);
sb.reverse();
sb.toString();
```

***

#### 🔹 **9.7 Command-Line Arguments**

```java
public static void main(String[] args) {
  for (String arg : args)
    System.out.println(arg);
}
```

***

#### ✅ Summary Table

| Feature           | Key Points                                               |
| ----------------- | -------------------------------------------------------- |
| `String`          | Immutable, used for fixed text                           |
| `StringBuilder`   | Mutable, better performance in single-threaded context   |
| `StringBuffer`    | Mutable, thread-safe                                     |
| `Character`       | Static utility methods for character processing          |
| Command-line args | Passed as `String[] args` to `main()`                    |
| `String` methods  | `length()`, `charAt()`, `substring()`, `indexOf()`, etc. |

***

Here’s a **Cheat Sheet for Chapter 10: Thinking in Objects** from _Introduction to Java Programming, 9th Edition by Y. Daniel Liang_:

***

### 🧠 Java OOP Deep Dive – Chapter 10: Thinking in Objects

***

#### 🔹 **10.1 Introduction**

* Moves from procedural to **object-oriented thinking**.
* Emphasizes **class design**, encapsulation, composition, and abstraction.
* Promotes **modularity**, **reuse**, and **maintainability**.

***

#### 🔹 **10.2 Immutable Objects and Classes**

* **Immutable object**: Once created, state cannot be changed.
* Requirements for immutability:
  * All fields `private`
  * No setter methods
  * No accessors that expose mutable fields

```java
final class Student {
  private final String name;
  private final Date dateCreated; // make defensive copy
}
```

***

#### 🔹 **10.3 Scope of Variables**

* Local variables override instance variables if same name.
* Instance variables are accessible by all instance methods.
* **Block scope**: A variable declared inside `{}` is only accessible within that block.

***

#### 🔹 **10.4 The `this` Reference**

* Refers to the **current object**.
* Used when parameter name hides instance variable:

```java
this.name = name;
```

* Can invoke another constructor:

```java
this(...);
```

***

#### 🔹 **10.5 Class Abstraction & Encapsulation**

* **Abstraction**: Hide internal implementation.
* **Encapsulation**: Combine data + methods; restrict direct access.
* Only expose a class's **contract** (public methods/constants).

```java
private double balance;
public double getBalance() { return balance; }
```

***

#### 🔹 **10.6 Procedural vs Object-Oriented Thinking**

| Procedural                      | Object-Oriented            |
| ------------------------------- | -------------------------- |
| Data & methods separate         | Data + methods = object    |
| Focus on actions                | Focus on entities          |
| Example: BMI calculator in main | Better: Define `BMI` class |

***

#### 🔹 **10.7 Object Composition**

* Use **has-a** relationship (composition):

```java
public class Student {
  private Address address;
}
```

* Good for modularity and reuse.

***

#### 🔹 **10.8–10.10 Case Studies**

**✅ Designing Classes:**

* **Course Class**
* **Custom Stack Class**
* **GuessDate Class**
* Focus on:
  * Good encapsulation
  * Real-world modeling
  * Class contracts

***

#### 🔹 **10.11 Class Design Guidelines**

* One class = one clear responsibility
* Use `private` for fields
* Provide `get`/`set` only when necessary
* Favor **composition** over inheritance
* Keep class self-contained and reusable

***

#### 🔹 **10.12 Wrapper Classes**

*   Convert **primitive types to objects**:

    ```java
    Integer i = Integer.valueOf(5); // Boxing
    int n = i.intValue(); // Unboxing
    ```
* Types: `Integer`, `Double`, `Boolean`, etc.

***

#### 🔹 **10.13 Autoboxing/Unboxing**

```java
Integer i = 10; // autobox
int n = i;      // unbox
```

* Java automatically wraps/unwraps primitive types.

***

#### 🔹 **10.14 BigInteger & BigDecimal**

* For **arbitrary precision numbers**:

```java
BigInteger big = new BigInteger("123456789123456789");
BigDecimal dec = new BigDecimal("3.1415926535");
```

* Use `add`, `multiply`, `compareTo`, etc.

***

### ✅ Summary Table

| Topic                   | Key Concept                        |
| ----------------------- | ---------------------------------- |
| Immutability            | Object’s state can't change        |
| `this`                  | Refers to current object           |
| Abstraction             | Use object’s public interface only |
| Encapsulation           | Keep details private               |
| Composition             | "Has-a" relationship               |
| Wrapper Classes         | Object form of primitives          |
| BigInteger / BigDecimal | Use for large or precise values    |

***

## **Chapter 11: Inheritance and Polymorphism**&#x20;

***

#### **11.1 Introduction to Inheritance**

* **Inheritance** allows defining a new class based on an existing one.
* The **new class** is called a _subclass_ (or child class), and the existing one is a _superclass_ (or parent class).
* Promotes **code reuse**, **organization**, and **modularity**.

***

#### **11.2 Superclasses and Subclasses**

* A **superclass** contains common features.
* A **subclass** extends a superclass and inherits accessible members.
* Example: `GeometricObject` as a superclass, `Circle` and `Rectangle` as subclasses.
* Subclass inherits **methods and fields** (except constructors and private members).

***

#### **11.3 Using the `super` Keyword**

* `super` is used to:
  * Call the superclass’s constructor: `super(args);`
  * Invoke superclass methods: `super.methodName();`
* The superclass constructor call must be the _first statement_ in a subclass constructor.

***

#### **11.4 Overriding Methods**

* A method in a subclass can override a superclass method **with the same signature and return type**.
* `@Override` annotation is recommended for clarity and compile-time checking.
* Only **accessible** (non-private) methods can be overridden.

***

#### **11.5 Overriding vs. Overloading**

* **Overriding**: same method name and signature in a subclass.
* **Overloading**: same method name but different parameters (can be in the same or different classes).

***

#### **11.6 The `Object` Class and `toString()`**

* All Java classes implicitly inherit from `java.lang.Object`.
* `toString()` is defined in `Object`, but often overridden for better output.
*   Example:

    ```java
    public String toString() {
      return "created on " + dateCreated + "\ncolor: " + color + " and filled: " + filled;
    }
    ```

***

#### **11.7 Polymorphism**

* A superclass reference can refer to a subclass object.
* **Subtype**: defined by a subclass; **supertype**: defined by a superclass.
* Enables flexibility and dynamic method behavior.

***

#### **11.8 Dynamic Binding**

* The JVM determines at **runtime** which method implementation to invoke based on the **actual type** of the object.
* Declared type determines what methods can be called; actual type determines which implementation is executed.

***

#### **11.9 Casting Objects and `instanceof`**

* **Upcasting**: Subclass → Superclass: automatic.
* **Downcasting**: Superclass → Subclass: explicit and may require `instanceof` for safety.
*   Syntax:

    ```java
    if (obj instanceof Circle) {
      Circle c = (Circle) obj;
    }
    ```

***

#### **11.10 The `equals` Method**

* Default in `Object` compares memory addresses.
* Override to define **logical equality**.

***

#### **11.11 The `ArrayList` Class**

* A flexible array-like structure that holds objects.
* Methods: `add()`, `remove()`, `get()`, `size()`, etc.

***

#### **11.12 Custom Stack Class Using ArrayList**

* Demonstrates how to build a stack (LIFO) using `ArrayList`.

***

#### **11.13 The `protected` Modifier**

* `protected` members can be accessed:
  * Within the same package
  * By subclasses (even in different packages)

***

#### **11.14 The `final` Modifier**

* Final **class**: cannot be extended.
* Final **method**: cannot be overridden.
*   Example:

    ```java
    public final class Math {}
    public final void methodName() {}
    ```

***

#### **Summary of Key Concepts**

* **Inheritance** promotes reuse.
* **Overriding** and **dynamic binding** enable polymorphic behavior.
* Use `super`, `protected`, and `final` appropriately.
* Utilize **type casting** and `instanceof` for safe object manipulation.
* Understand the difference between **overloading** and **overriding**.

***

Here are detailed notes for **Chapter 12: GUI Basics** from _"Introduction to Java Programming, 9th Edition" by Y. Daniel Liang_:

***

### **Chapter 12: GUI Basics**

#### **12.1 Introduction**

* Java GUI programming illustrates core OOP principles.
* GUI components interact through objects, containers, and layout managers.
* Swing is the primary GUI toolkit used in modern Java applications.

***

#### **12.2 Swing vs. AWT**

* **AWT (Abstract Window Toolkit)**: platform-dependent, less flexible.
* **Swing**: platform-independent, lightweight, more powerful.
* Swing classes are prefixed with `J` (e.g., `JButton` vs. AWT's `Button`).

***

#### **12.3 Java GUI API Overview**

* Three types of GUI-related classes:
  * **Component classes**: `JButton`, `JLabel`, etc.
  * **Container classes**: `JFrame`, `JPanel`, `JDialog`, etc.
  * **Helper classes**: `Color`, `Font`, `Graphics`, etc.
* Class hierarchy:
  * `Object` → `Component` → `Container` → `JComponent` → Swing components.

***

#### **12.4 Frames**

* A **frame** is a window that holds components (e.g., buttons, labels).
* Created using `JFrame`.
* Must set:
  * `setTitle()`, `setSize()`, `setLocationRelativeTo(null)`, `setDefaultCloseOperation()`, `setVisible(true)`.

***

#### **12.5 Layout Managers**

* Define how components are arranged.
* **FlowLayout**: left-to-right, top-to-bottom (default for `JPanel`).
* **GridLayout**: rectangular grid.
* **BorderLayout**: divides area into five regions (NORTH, SOUTH, EAST, WEST, CENTER).
* Use `setLayout()` to apply a layout to a container.

***

#### **12.6 Using Panels**

* `JPanel`: a container that can hold a group of components.
* Useful for modular designs and nested layouts.
* Helps manage complex GUI layouts.

***

#### **12.7 The Color Class**

* Defines colors using RGB values (`new Color(r, g, b)` where 0 ≤ r,g,b ≤ 255).
* Predefined constants: `Color.RED`, `Color.BLUE`, etc.
* Set background/foreground with:
  * `setBackground(Color)`, `setForeground(Color)`.

***

#### **12.8 The Font Class**

* Fonts have `name`, `style`, and `size`.
* Created using: `new Font("Serif", Font.BOLD, 16)`.
* Styles: `Font.PLAIN`, `Font.BOLD`, `Font.ITALIC`.

***

#### **12.9 Common Features of Swing Components**

* All Swing components inherit from `JComponent`.
* Shared properties:
  * Font, color, size, tooltip text (`setToolTipText()`), borders.
* Use `setBorder()` for decorating components.

***

#### **12.10 Image Icons**

* Images can be displayed using `ImageIcon`.
*   Can be applied to `JLabel`, `JButton`, etc.

    ```java
    ImageIcon icon = new ImageIcon("image/path.png");
    JLabel label = new JLabel("Text", icon, JLabel.CENTER);
    ```

***

#### **12.11 JButton**

* A button component that can contain text, icons, or both.
* Register event listeners to respond to user actions (covered in Ch. 16).

***

#### **12.12 JCheckBox**

* A GUI element with a label and a checkbox.
* Represents binary choices.
* Use `isSelected()` to check state.

***

#### **12.13 JRadioButton**

* Represents mutually exclusive options.
*   Use `ButtonGroup` to group radio buttons.

    ```java
    ButtonGroup group = new ButtonGroup();
    group.add(rb1);
    group.add(rb2);
    ```

***

#### **12.14 JLabel**

* Displays text, icons, or both.
* Properties:
  * `horizontalAlignment`, `verticalAlignment`, `horizontalTextPosition`, `verticalTextPosition`.

***

#### **12.15 JTextField**

* Single-line text input field.
* Methods:
  * `getText()`, `setText(String)`, `setEditable(false)`.
  * Constructor options for setting initial text and column width.

***

#### **Chapter Summary Highlights**

1. Containers use layout managers to position components.
2. `JPanel` helps group components.
3. Colors are defined using RGB or named constants.
4. Fonts and tool tips enhance GUI appearance.
5. Components share common properties via inheritance.

***

## &#x20;**Chapter 13: Graphics**&#x20;

***

### **Chapter 13: Graphics**

#### **13.1 Introduction**

* Graphics programming enables custom drawings in Java GUI.
* Examples: clocks, pie charts, stop signs.
* Java graphics are based on a coordinate system: origin (0,0) is top-left, x increases right, y increases downward.

***

#### **13.2 The `Graphics` Class**

* Every GUI component has a graphics context represented by a `Graphics` object.
* Common drawing methods:
  * `drawString(String s, int x, int y)`
  * `drawLine(int x1, int y1, int x2, int y2)`
  * `drawRect`, `fillRect`, `drawOval`, `fillOval`, etc.
* Override `paintComponent(Graphics g)` in a class that extends `JPanel` to draw on it.
* Always call `super.paintComponent(g)` at the beginning to clear the drawing area.

***

#### **13.3 Drawing Strings, Lines, Rectangles, and Ovals**

* Use methods like `drawString()`, `drawLine()`, `drawRect()`, `fillRect()`, `drawOval()`, and `fillOval()`.
* Dimensions are in pixels.
* Good for rendering text and basic shapes.

***

#### **13.4 Case Study: `FigurePanel` Class**

* A reusable component to draw different shapes based on a property.
* Shapes include lines, rectangles, round rectangles, and ovals.
* Useful for building flexible GUI components.

***

#### **13.5 Drawing Arcs**

* Use `drawArc()` and `fillArc()`.
* Arc defined by bounding rectangle, start angle, and arc angle.
* Can draw pies and circular charts.

***

#### **13.6 Drawing Polygons and Polylines**

* Use `drawPolygon()`, `fillPolygon()`, `drawPolyline()`.
* Coordinates are passed as arrays of x and y values.
* Also supports the `Polygon` class.

***

#### **13.7 Using `FontMetrics` to Center Text**

* `FontMetrics` helps measure string width and height for precise positioning.
* Useful for centering or aligning text.
* Methods: `getAscent()`, `getDescent()`, `getHeight()`, `stringWidth()`.

***

#### **13.8 Case Study: `MessagePanel` Class**

* A custom component for displaying a message.
* Can set font, alignment, rotation, and other properties.
* Demonstrates use of graphics transformation and text rendering.

***

#### **13.9 Case Study: `StillClock` Class**

* A reusable analog clock component.
* Uses trigonometric formulas to draw hour, minute, and second hands.
* Updates with the current time using `Calendar`.

***

#### **13.10 Displaying Images**

* Use `ImageIcon` for basic display in `JLabel`.
* For more control, use `Graphics.drawImage()` with `Image` objects.
* Override `paintComponent()` for flexible image rendering.
* Use `getImage()` from `ImageIcon` to get a drawable `Image`.

***

#### **13.11 Case Study: `ImageViewer` Class**

* Custom component for displaying images with options like stretching or positioning.
* Properties: image, stretched, x/y coordinates.
* Uses `repaint()` to update the image dynamically.

***

#### **Java 2D Graphics (Bonus: Advanced Topics from Summary)**

* `Graphics2D` class provides enhanced rendering (rotation, scaling, transformation).
* Shapes: `Line2D`, `Rectangle2D`, `Arc2D`, `Ellipse2D`, `Path2D`, etc.
* `Stroke`, `Paint`, `GradientPaint`, `TexturePaint` for styling.
* Supports constructive area geometry (add, subtract, intersect shapes).

***

#### **Key Points Summary**

1. Use `paintComponent(Graphics g)` in custom `JPanel` subclasses for drawing.
2. Call `super.paintComponent(g)` to avoid painting issues.
3. Use `Graphics` methods for shapes and text.
4. Use `FontMetrics` for measuring and aligning text.
5. Use `drawImage()` for displaying images in a panel.
6. For advanced graphics, use `Graphics2D` and Java 2D API.

***

Here are detailed notes for **Chapter 15: Abstract Classes and Interfaces** from _"Introduction to Java Programming, 9th Edition"_ by Y. Daniel Liang:

***

### **Chapter 15: Abstract Classes and Interfaces**

#### **15.1 Introduction**

* Abstract classes and interfaces define common behavior for related or unrelated classes.
* A superclass models shared features. An **interface** provides a flexible way to define capabilities across unrelated classes.

***

#### **15.2 Abstract Classes**

* **Abstract class**: A class that cannot be instantiated.
* Contains **abstract methods** (no implementation) and **concrete methods**.
*   Example:

    ```java
    public abstract class GeometricObject {
      public abstract double getArea();
      public abstract double getPerimeter();
    }
    ```
* Used to enforce common method structure in subclasses like `Circle` and `Rectangle`.

***

#### **15.3 Case Study: Abstract `Number` Class**

* `Number` is an abstract superclass of all numeric wrapper classes (e.g., `Integer`, `Double`).
* Defines abstract methods like `intValue()`, `doubleValue()` to standardize numeric conversions.

***

#### **15.4 Case Study: `Calendar` and `GregorianCalendar`**

* `Calendar` is an abstract class for date/time.
* `GregorianCalendar` is a concrete subclass used for calendar calculations.

***

#### **15.5 Interfaces**

* **Interface**: A class-like construct with only constants and abstract methods.
* Cannot be instantiated.
*   Syntax:

    ```java
    public interface Edible {
      String howToEat();
    }
    ```
* A class **implements** an interface to agree to fulfill its contract.
* Example: `Chicken implements Edible` and overrides `howToEat()`.

***

#### **15.6 The `Comparable` Interface**

* Declares the `compareTo()` method for sorting objects.
* Classes like `String` and `Integer` implement it.
* Custom classes can implement it to define natural ordering.

***

#### **15.7 The `Cloneable` Interface**

* **Marker interface**: No methods—only marks a class as cloneable.
* Used with `Object.clone()` to allow object copying.
* If a class does not implement `Cloneable`, calling `clone()` throws `CloneNotSupportedException`.

***

#### **15.8 Interfaces vs. Abstract Classes**

| Feature      | Abstract Class      | Interface                  |
| ------------ | ------------------- | -------------------------- |
| Variables    | Any type            | `public static final` only |
| Methods      | Concrete + abstract | Only `public abstract`     |
| Inheritance  | Single              | Multiple                   |
| Constructors | Yes                 | No                         |

* Use **abstract classes** for "is-a" relationships (strong hierarchy).
* Use **interfaces** for capabilities (e.g., comparable, edible) across unrelated types.

***

#### **15.9 Case Study: The `Rational` Class**

* Models rational numbers (`a/b`).
* Implements `Comparable<Rational>` and extends `Number`.
* Methods:
  * Arithmetic operations: `add()`, `subtract()`, `multiply()`, `divide()`
  * Conversion: `intValue()`, `doubleValue()`, etc.
  * Immutability: Internal state can't change after creation.

***

#### **Key Takeaways**

1. **Abstract classes** define a base for shared design with partial implementation.
2. **Interfaces** define a contract for capabilities and support multiple inheritance.
3. Use abstract classes when behavior is shared; use interfaces when behavior is desired across types.
4. Java favors **interface-based design** for flexibility and scalability.

***

Here are detailed notes for **Chapter 16: Event-Driven Programming** from _"Introduction to Java Programming, 9th Edition"_ by Y. Daniel Liang:

***

### **Chapter 16: Event-Driven Programming**

#### **16.1 Introduction**

* In **event-driven programming**, the program responds to user actions like button clicks, key presses, or timer ticks.
* Events are **fired by source objects** and handled by **event listeners**.

***

#### **16.2 Events and Event Sources**

* An **event** is an object that signals something happened (e.g., `ActionEvent`, `MouseEvent`, `KeyEvent`).
* A **source object** is the GUI component that generates the event (e.g., a `JButton`).
* `EventObject` is the root class for all event types.

***

#### **16.3 Listeners, Registrations, and Handling Events**

* An **event listener** is an object that implements a listener interface and processes the event.
* **Registering listeners**: Source object uses `addXListener()` methods (e.g., `addActionListener()`).
* **Handler methods**:
  * `actionPerformed(ActionEvent e)` for `ActionListener`
  * `mousePressed(MouseEvent e)` for `MouseListener`
  * `keyPressed(KeyEvent e)` for `KeyListener`

***

#### **16.4 Inner Classes**

* Listener classes can be defined as **inner classes**.
* They have direct access to members of the outer class.

***

#### **16.5 Anonymous Inner Classes**

* Can define and register the listener in one step.
*   Useful for simple, one-time-use listeners:

    ```java
    button.addActionListener(new ActionListener() {
        public void actionPerformed(ActionEvent e) {
            System.out.println("Button clicked");
        }
    });
    ```

***

#### **16.6 Alternative Listener Definitions**

* You can also:
  * Let the frame class implement the listener interface directly.
  * Use a **single listener** for multiple components and differentiate via `getSource()`.

***

#### **16.7 Case Study: Loan Calculator**

* Demonstrates building a full GUI app that handles events from text fields and a button.
* Showcases how components work together in a real application.

***

#### **16.8 Mouse Events**

* Mouse events include clicks, presses, releases, enters, exits, moves, and drags.
* Two interfaces:
  * `MouseListener`: `mouseClicked()`, `mousePressed()`, etc.
  * `MouseMotionListener`: `mouseDragged()`, `mouseMoved()`

***

#### **16.9 Listener Interface Adapters**

* For interfaces with multiple methods, Java provides **adapter classes** with empty method bodies (e.g., `MouseAdapter`).
*   Use adapters to avoid implementing all methods:

    ```java
    panel.addMouseListener(new MouseAdapter() {
        public void mouseClicked(MouseEvent e) {
            // handle click
        }
    });
    ```

***

#### **16.10 Key Events**

* `KeyListener` processes:
  * `keyPressed()`
  * `keyReleased()`
  * `keyTyped()`
* To receive key events, a component must be **focusable** and have focus.

***

#### **16.11 Animation Using `javax.swing.Timer`**

* `Timer` fires `ActionEvent` at fixed intervals.
* Used for animations or periodic updates (e.g., clocks, moving objects).
*   Create a timer:

    ```java
    Timer timer = new Timer(1000, listener);
    timer.start();
    ```

***

#### **Key Concepts Recap**

1. **Event-driven programming** is driven by user and system events.
2. Components act as **event sources**; classes implement **listener interfaces** to handle events.
3. Use `addXListener()` to register listeners.
4. Timer-based animations are implemented using the `javax.swing.Timer` class.
5. Inner and anonymous classes make listener code cleaner and more modular.

***

Here are detailed notes on **Chapter 17: GUI Components** from _"Introduction to Java Programming, 9th Edition"_ by Y. Daniel Liang:

***

### **Chapter 17: GUI Components**

#### **17.1 Introduction**

* Expands GUI programming with additional Swing components.
* Builds on Chapter 16’s event-handling concepts.
* New components covered: `JTextArea`, `JComboBox`, `JList`, `JScrollBar`, `JSlider`.

***

#### **17.2 Events for `JCheckBox`, `JRadioButton`, and `JTextField`**

* GUI components can fire various event types:
  * `ItemEvent`: when state changes (checked/unchecked).
  * `ActionEvent`: triggered by pressing Enter or clicking.
* A program can use checkboxes for font styles, radio buttons for color selection, and a text field to change label content.

***

#### **17.3 `JTextArea`**

* For multi-line text input/output.
* Key methods:
  * `append(String s)`: adds text.
  * `setLineWrap(true)`: enables word wrap.
* Often embedded in a `JScrollPane` to add scrolling capabilities.

***

#### **17.4 `JComboBox`**

* Drop-down menu that lets users select one item.
* Can be editable or non-editable.
* `addItem()`, `getSelectedItem()`, and `setSelectedItem()` are common methods.

***

#### **17.5 `JList`**

* Used for selecting one or multiple items from a list.
* Configurable for single or multiple selection modes.
* Usually embedded in a `JScrollPane`.

***

#### **17.6 `JScrollBar`**

* Represents adjustable sliders with arrows.
* Can be horizontal or vertical.
* Less flexible than `JSlider`, usually used for scrolling control.

***

#### **17.7 `JSlider`**

* More versatile than `JScrollBar`.
* Can be configured with tick marks and labels.
* Allows smooth or snap-to-tick adjustments.

***

#### **17.8 Creating Multiple Windows**

* Use `JFrame` to launch multiple independent windows.
* Key tip: **you cannot add a `JFrame` to a container**, but you can create a separate frame and set it visible.
* Case Study: `MultipleWindowsDemo` uses a main frame with a text area and a button, and opens a second frame showing a histogram when the button is clicked.

***

#### **Case Study Highlights**

* **`MultipleWindowsDemo`**:
  * Inputs text in a main window.
  * Calculates letter frequency.
  * Displays results in a histogram within a new window.

***

#### **Summary of Key Concepts**

1. **JCheckBox**, **JRadioButton**, and **JTextField** events expand user input capabilities.
2. **JTextArea** handles multi-line text.
3. **JComboBox** and **JList** allow selection from a set of choices.
4. **JScrollBar** and **JSlider** provide user-controlled value ranges.
5. Multiple windows can be created using `JFrame` instances shown conditionally.

***

