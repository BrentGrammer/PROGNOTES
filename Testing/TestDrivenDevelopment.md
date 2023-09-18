# Test Driven Development

### Code Rot

- Systems will degrade over time.
- Code becomes rigid, fragil and immobile. Changes require touching many places and breaking and debugging are common and complicated.
- The code is not cleaned due to fear of breaking it.
- Having a suite of good tests removes fear of changing code.

### [Refactioring exercise](https://cleancoders.com/episode/clean-code-episode-6-p1) (16:00)

When dealing with refactoring a messy function, try the following if applicable:

- Start by inlining all of the function calls with implementation (refactor) in order to repartition the organization of the function.
- Extract state information (ex. buffers, arguments, flags) into a class
  ex:

```java
public String html(int depth) {
    return new HtmlFormatter(depth).format(); // extracted state and logic of long function into class
}
```

```java
// class that had messy logic refactored:
private class HtmlFormatter {
    private int depth;

    public HtmlFormatter(int depth) {
        this.depth = depth;
    }
    // this method originally had flags, buffers, messy logic etc. After refactoring, the logic is broken down and reads in a logical and easy to read manner
    public String format() {
        return makeTabs() + makeHead()
            + makeTag() + makeAttributes() + makeTagEnd()
            + makeChildren() + makeEndTag() + makeTail()
            + makeLineEnd();
    }

    private String makeEndTag() {
        return hasChildren() ? "</" + tagName() + ">" : "";
    }
    // ...other extracted small functions
}
```

- in the new class with the extracted logic, rename variables if unclear to more meaningful names
- Extract pieces of logic to small functions that read logically one after the other in a predictable way.

### The need for tests
- Decreases debugging and increases devlopment speed. 
- **Eliminates fear of changing the code to prevent rot.**

### TDD Rules, the 3 laws
1. Write no production code until first writing a failing unit test
1. Do not write more of a unit test than is sufficient to fail (not compiling is failing as well). includes you stop writing the test as soon as it does not compile.
1. Do not write more production code than is sufficient to currently pass the unit test.

This results in a cycle that lasts about 20 seconds. You bounce back and forth between the test and the code.

- The main idea is that within the last few minutes at most, the code executed successfully. This reduces debugging time because you'll usually find the bug in the code you just wrote.

#### Tests serve as documentation for how to use the system
- If you want to know how to create an object in the system, there are unit tests that create that object every way that it can be created.
- How do I call an API function? There are unit tests that call that API function every way it can be called.
- Tests stay in sync with the application code. They are low level documentation of the system.

#### **Writing tests first force you to write production code that is testable** - i.e. the code will be decoupled
- Writing tests first also prevents you from taking shortcuts that are tempting when writing the tests after the fact. Some code might be hard to test, and you've already tested it manually, so you take shortcuts in the test afterwards.