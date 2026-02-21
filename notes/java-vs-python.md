# Java vs python

java --

* write one and run everywhere as it gets compiles

python&#x20;

* temp



Hello world

```java
public class HelloWorld {
    public static void main(String args){
        System.out.print("Hello World");
    }
}
```

* java needs more elaborate structure for the same output
* psvmsa -— public static void main string args \[program entry point)
  * This method clearly indicates where the program's execution commences, and any command-line arguments are directly accessible through the `args` `String` array.
* By requiring all executable code to be part of a class and explicitly invoked, Java mitigates risks associated with unintended side effects or the execution of potentially malicious code during module imports.
* python has

```python
if __name__ == "__main__":
```

* this indicates that the code should only execute when the script is run directly rather than when it is imported as a module.
* command line args are accessed via sys.args
