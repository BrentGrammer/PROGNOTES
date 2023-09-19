# Test Driven Development

### TDD Rules, the 3 laws

1. Write no production code until first writing a failing unit test.
1. Do not write more of a unit test than is sufficient to fail (not compiling is failing as well). includes you stop writing the test as soon as it does not compile.
1. Do not write more production code than is sufficient to currently pass the unit test.

This results in a cycle that lasts about 20 seconds. You bounce back and forth between the test and the code.

- The main idea is that within the last few minutes at most, the code executed successfully. This reduces debugging time because you'll usually find the bug in the code you just wrote.

### Code Rot

- Systems will degrade over time.
- Code becomes rigid, fragil and immobile. Changes require touching many places and breaking and debugging are common and complicated.
- The code is not cleaned due to fear of breaking it.
- Having a suite of good tests removes fear of changing code.

### General Principles in TDD

- You start with a preliminary design for the system, but the TDD process will not necessarily follow it - it is just a rough guide to start. You might find that by the end of Test Driving a solution the system is much simpler than originally anticipated. The tests can take you in a completely different direction.
  - You can start for example by going through classes in the initial design and try to identify behaviors to test. If you find there are no behaviors to test, move up the heirarchy until you find a part of the system with behavior you can test.
- You may write tests that you'll delete later on as cycles progress
- Start with the simplest least complicated scenario and gradually move on to slightly more complicated scenarios and cases to test
- The refactor phase also includes refactoring and cleaning up your tests as well as production code.
- Don't bother writing tests that you know will pass because they are similar to already written tests.
- If you start seeing bad design in the production code and need to refactor, ignore the current failing test to get back to a green state and refactor the production code before moving on.
- Treat the test code just as though it was production code - make it clean and refactor it following good design and principles.
- Absolute certainty that the tests prove the program is correct and bug free is impossible, but the tests provide protection enough to eliminate the fear of making changes to the production code base.

### [Refactoring exercise](https://cleancoders.com/episode/clean-code-episode-6-p1) (16:00)

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

#### Tests serve as documentation for how to use the system

- If you want to know how to create an object in the system, there are unit tests that create that object every way that it can be created.
- How do I call an API function? There are unit tests that call that API function every way it can be called.
- Tests stay in sync with the application code. They are low level documentation of the system.

#### **Writing tests first force you to write production code that is testable** - i.e. the code will be decoupled

- Writing tests first also prevents you from taking shortcuts that are tempting when writing the tests after the fact. Some code might be hard to test, and you've already tested it manually, so you take shortcuts in the test afterwards.

## [Bowling Game Demonstration](https://cleancoders.com/episode/clean-code-episode-6-p2)

- Start with a short design session to identify the main objects or partitions of the system (7:00)
- Using TDD, do not follow the design, just use it as a kind of guideline

### Process

- Start the project with something executing (a starting test):

```java
public class BowlingTest {
    @Test
    public void nothing() throws Exception {
        // call the test "nothing" just to have something to start with that executes.
    }
}
```

#### Cycle 1 (Red Green Refactor)

- Ask what test would I like to write. Ask: What test do I need to write that would force me to write the code that I know I want to run? (i.e. what would force you to write and create a public class Game?)

```java
 // TEST
public class BowlingTest {
   @Test
   public void canCreateGame() throws Exception {
       Game g = new Game(); // this does not compile so we must make it compile
   }
}
```

```java
// Production Code
// create the class game to make the test compile and pass taking us to the green phase (time to refactor, but there is nothing to refactor, so back to red phase)

public class Game {
}
```

#### Cycle 2 (Red Green Refactor)

- Now in the red phase again after making test compile and pass, write the next test

```java
@Test
public void canRoll() throws Exception {
    Game g = new Game();
    // call the method does not exist yet, test does not compile
    g.roll(0);
}
```

```java
// create the method to make the test compile:
public class Game {
    public void roll(int pins) {
        // now the test compiles and passes, so go to refactor phase, this includes refactoring the tests if applicable!

        // note that roll does not do anything but the test passes, so we stop writing any more production code!!
    }
}
```

```java
// Refactor phase - in this case we can actually refactor the tests to remove duplicate code
public class BowlingTest {
    private Game g; // extract duplicate declaration of game to before setup to DRY up tests as part of refactor phase.

    @Before
    public void setUp() throws Exception {
        g = new Game();
    }

    // can now delete empty test since the case is covered in the setup
    // NOTE: it is common to write a test just to delete it later in this cycle
    // @Test
    // public void canCreateGame() throws Exception {
    // }

    @Test
    public void canRoll() throws Exception {
        // call the method does not exist yet, test does not compile
        g.roll(0);
    }
}
```

#### Cycle 3 (Red Green Refactor)

- Back to red phase in the cycle.

##### Important Rule: When you must write real code (i.e. logic), write the simplest code you can.

- In this case we want to roll a complete game - what is the simplest game you can roll? A gutter game.

```java
@Test
public void gutterGame() throws Exception {
    // roll 20 0s for a gutter game
    for (int i=0; i<20; i++)
        g.roll(0)
    assertEquals(0, g.score()); // this does not compile now since score() does not exist, now we go into the green phase to make the test compile and pass
}
```

- Green phase:

```java
public class Game {
    //...
    public int score() {
        return -1; // first make the test compile, but fail so you can see it fail!
    }
}
```

```java
public class Game {
    //...
    public int score() {
        return 0; // Now, make the test pass by returning the correct result (note the stupid naive implementation, but it is easy and simple code)
    }
}
```

No refactoring, so move to next cycle

#### Cycle 4 (Red Green Refactor)

Move on to the next most complicated scenario (a game of all 1s - still really simple, just the next step up in complexity)

- Red Phase, test fails:

```java
@Test
public void allOnes() throws Exception {
    for (int i=0; i<20; i++)
        g.roll(1)
    assertEquals(20, g.score());
}
```

- Green Phase (make test pass)
  - simplistically you can just return 20 to make allOnes pass, but then the first test will fail, so that rules out that solution. Do something marginally intelligent to make the tests all pass.

```java
public class Game {
    private int score = 0; // add field

    public void roll(int pins) {
        score += pins; // update roll to set score to pins
    }
    public int score() {
        return score;
    }
}
```

- Refactor Phase
  - refactor the test to remove duplicate code

```java
private void rollMany(int n, int pins) {
    for (int i=0; i<n; i++) {
        g.roll(pins);
    }
}

// We also can delete the no longer needed canRoll test - remember writing tests to remove them later is not uncommon in TDD!
// public void canRoll() throws Exception {
//     g.roll(0);
// }

@Test
public void gutterGame() throws Exception {
    // extract loop to roll game into function
    rollMany(20, 0);
    assertEquals(0, g.score());
}

@Test
public void allOnes() throws Exception {
    rollMany(20, 1);
    assertEquals(0, g.score());
}
```

#### Cycle 5 (Red Green Refactor)

- Red Phase: find the next most interesting test case

  - the next case could be all 2s,3s and all 4s but you know they will pass (similar to all 1s), so you don't write tests that you know will pass.
  - In the case of all 5s, that is different because it brings in the scenario of spares, so the next test should be to write the simplest test to test spares: i.e. 1 spare followed by gutter balls

```java
@Test
public void oneSpare() throws Exception {
    g.roll(5);
    g.roll(5); // spare
    g.roll(3); // addition roll (counts toward spare bonus per rules)
    rollMany(17, 0); // roll gutter balls for rest of game
    assertEquals(16, g.score());
}
```

- Green phase

  - We'll be tempted to introduce a flag to detect when current and last roll == 10 it's a spare, but you should stop when you're driven to do this because it means there is something wrong with the design.
  - In this case there is the problem of misplaced responsibilities: the roll method is calculating the score and the score method is not. This is bad design, so **we stop and IGNORE the test that is currently failing so we can go back to the refactor phase.**

- Reverted to Refactoring phase to fix design:

```java
// Ignore the currently failing test to get back to green and into the refactoring phase of the cycle
@Ignore
@Test
public void oneSpare() throws Exception {
    // ... ignore the current failing test to get all tests passing again
}
```

```java
// refactor the prod code to fix the design problem:
public class Game {
    private int rolls[] = new int[21]; // add place to store pins from rolls
    private int currentRoll = 0; // add index to track current roll

    public void roll(int pins) {
        // just deal with rolls, not the score calculation - the responsibility for calculating the score should go in score()!
         rolls[currentRoll++] = pins; //store the pins knocked in rolls list
    }
    public int score() {
        int score = 0;
        int i=0;
        //actually calculate the score as the function says
        // also refactor the loop so it loops through rolls one frame at a time, not one ball at a time
        for (frame=0; i < 10; i++) {
            score += rolls[i] + rolls[i+1];
            i += 2;
        }
        return score;
    }
}
```

- Go back to Red Phase now (remove the @Ignore from the last test):

```java
public class Game {
    private int rolls[] = new int[21];
    private int currentRoll = 0;

    public void roll(int pins) {
         rolls[currentRoll++] = pins;
    }
    public int score() {
        int score = 0;
        int i=0;
        for (frame=0; i < 10; i++) {
            if (rolls[i] + rolls[i+1] == 10) // spare
            {
                score += 10 + rolls[i+2];
                i += 2;
            } else {
                score += rolls[i] + rolls[i+1];
                i += 2;
            }
        }
        return score;
    }
}
```

tests pass, Green, now move to:

- Refactor Phase

```java
public class Game {
    private int rolls[] = new int[21];
    private int currentRoll = 0;

    private boolean isSpare(int firstInFrame) {
        return rolls[firstInFrame] + rolls[firstInFrame+1] == 10
    }

    public void roll(int pins) {
         rolls[currentRoll++] = pins;
    }
    public int score() {
        int score = 0;
        int firstInFrame=0;
        for (frame=0; firstInFrame < 10; firstInFrame++) {
            if (isSpare(firstInFrame))
            {
                score += 10 + rolls[firstInFrame+2];
                firstInFrame += 2;
            } else {
                score += rolls[firstInFrame] + rolls[firstInFrame+1];
                firstInFrame += 2;
            }
        }
        return score;
    }
}
```

refactor the test:

```java
// extract rollspare to elminate //spare comment in test
private void rollSpare() {
    g.roll(5);
    g.roll(5);
}

@Test
public void oneSpare() throws Exception {
    rollSpare();
    g.roll(3); // addition roll (counts toward spare bonus per rules)
    rollMany(17, 0); // roll gutter balls for rest of game
    assertEquals(16, g.score());
}
```

#### Cycle 6 (Red Green Refactor)

- next most interesting test case: one strike

- Red phase:

```java
@Test
public void oneStrike() throws Exception {
    g.roll(10); // strike
    g.roll(3);
    g.roll(4);
    rollMany(16);
    assertEquals(24, g.score())
}
```

- Green phase:

```java
public class Game {
    private int rolls[] = new int[21];
    private int currentRoll = 0;

    private boolean isSpare(int firstInFrame) {
        return rolls[firstInFrame] + rolls[firstInFrame+1] == 10
    }
    public void roll(int pins) {
         rolls[currentRoll++] = pins;
    }
    public int score() {
        int score = 0;
        int firstInFrame=0;
        for (frame=0; frame < 10; frame++) {
            if (rolls[firstInFrame] == 10) // strike
            {
                score += 10 + rolls[firstInFrame+1] + rolls[firstInFrame+2];
                firstInFrame++ // only one ball in a strike frame
            }
            else if (isSpare(firstInFrame))
            {
                score += 10 + rolls[firstInFrame+2];
                firstInFrame += 2;
            } else {
                score += rolls[firstInFrame] + rolls[firstInFrame+1];
                firstInFrame += 2;
            }
        }
        return score;
    }
}
```

- Refactor Phase

```java
public class Game {
    private int rolls[] = new int[21];
    private int currentRoll = 0;

    private boolean isSpare(int firstInFrame) {
        return rolls[firstInFrame] + rolls[firstInFrame+1] == 10
    }
    private boolean isStrike(int firstInFrame) {
        return rolls[firstInFrame] == 10;
    }
    private int nextTwoBallsForStrike(int firstInFrame) {
        return rolls[firstInFrame+1] + rolls[firstInFrame+2];
    }
    private int nextBallForSpare(int firstInFrame) {
        return rolls[firstInFrame+2];
    }
    private int twoBallsInFrame(int firstInFrame) {
        return rolls[firstInFrame] + rolls[firstInFrame+1];
    }


    public void roll(int pins) {
         rolls[currentRoll++] = pins;
    }
    public int score() {
        int score = 0;
        int firstInFrame=0;
        for (frame=0; frame < 10; frame++) {
            if (isStrike(firstInFrame))
            {
                score += 10 + nextTwoBallsForStrike(firstInFrame);
                firstInFrame++ // only one ball in a strike frame
            }
            else if (isSpare(firstInFrame))
            {
                score += 10 + nextBallForSpare(firstInFrame);
                firstInFrame += 2;
            } else {
                score += twoBallsInFrame(firstInFrame);
                firstInFrame += 2;
            }
        }
        return score;
    }
}
```

```java
//extract method to eliminate strike comment
private void rollStrike() {
    g.roll(10);
}
@Test
public void oneStrike() throws Exception {
    rollStrike();
    g.roll(3);
    g.roll(4);
    rollMany(16);
    assertEquals(24, g.score())
}
```

#### Cycle 7 (Red Green Refactor)

Next most interesting test case: a perfect game (all strikes)

- Red Phase:

```java
@Test
public void perfectGame() throws Exception {
    rollMany(12, 10);
    assertEquals(300, g.score())
}
```

NOTE: this test passes without writing any prod code!
WE'RE DONE - the algorithm we have in place satisfies the rules of the bowling game.

### Conclusion from demonstration:

- The design we original had in mind (with a Frame, Roll and Tenth Frame class etc.) was much more complex than needed and we wound up not needing most of it.
  - see timestamp 39:27 in [the video](https://cleancoders.com/episode/clean-code-episode-6-p2)
- This was revealed by using TDD which drove our algorithm that wound up being a much simpler implementation than was originally anticipated.
  - The final algo solution was a for loop and two if statements, 14 lines of code. No multiple classes etc. were needed.
  - The way we snuck up on this simpler solution was by doing a set of steps that were simple and stupid not worthy of much thought.

## Objections to TDD

- "It slows you down": the debugging time that is saved by working in a clean codebase more than makes up for the time lost doing TDD.
- "Writing code stepwise instead of optimally from the start is a waste of time": Every creative effort is done iteratively and is the way the human brain works.
- "Making changes in production code and break tests causing more time to be spent fixing them": If your tests break when you make changes to production code it means there is something wrong with the tests and their design and they are too coupled to the production code implementation. Make sure to decouple the tests from the production code impl.
- "We can just write the tests after the code is written, no need to write them before": not true, if tests are written after the fact, they will not be complete and they won't be trustworthy. This is due some part to human nature - _humans consider things that come first to be more important and things that come at the end to be optional or not important._
- "The rest of the team does not want to do TDD": You don't need to convince the team to do TDD - this is a personal decision that you make to commit to following the discipline of TDD. Let other people take care of themselves. Others might notice that you're going faster, have fewer bugs and your code is cleaner. Lead by example.

### Dealing with Legacy Code (Code without tests)

- Do not try to embark on large refactoring projects
- Start with decoupling a small part of the system and adding tests little by little
- When a new feature is being implemented, Test Drive it to add tests to cover that part of the system. Month by month and little by little the system will gradually get covered by more and more tests.
- All new code in the system should be test driven and if there is an option to either modify old code or write a new module, write the new module so you can write it test first.

## Testing UIs

- For the most part you do not test drive UIs because you fiddle with them and mess around with what is seen on the screen until you like what you see.
- This only applies to the last thin outer layer of the GUI where the formatting is. There is a layer back from that that should be tested.
  - Ex: Decision to gray out a inactive button should be tested. You do not test that the button itself was rendered in gray, you need to test that the boolean that controls that state was set properly.
  - The format of a currency or date can be tested
  - The elements of a dropdown list can be enumerated and tested
  - The CONTENT of the screen can be tested even if the final format cannot.
- Separate the GUI into two components: **The Presenter** and **The View**
  - Presenter: interrogates business objects and then constructs data structures that the View then renders
    - knows which buttons are active and not active so sets appropriate booleans in those data structures
    - knows how to fetch all the dropdown items and puts them into the data structures
    - knows how to format dates and other items and puts the formatted strings in the data structures
    - The Presenter can be tested!
- You can optionally fiddle with the GUI until you have it the way you want and then write tests afterwards, but more important is to test the UI logic.

## Testing Databases

- For the most part you do not test databases.
- Databases are blackboxes
- You want to test that your schema and queries work as expected.
- You need to separate the Application from the Database layers (see episode 4 and 5)
  - This allows you to use mocks and stubs for the database and test the application without the database actually in place.
  - can test that the SQL is generated properly
  - can test that the generated queries behave properly by loading a database with a minimal number of rows and then executing those queries.

## TDD as a Discipline (a la Double entry book keeping)

- Software is a system of binary data, so a single bit set improperly can cause the system to fail. One flipped bit can crash the whole application!
- Accounting is similar to software in that a single error can invalidate the entire calculation and effort.
  - Accountants deal with this by following a DISCIPLINE called double entry book keeping.
- Test Driven Development is a similar discipline to double entry book keeping to prevent small errors from bringing the system down.
  - Everything is stated twice - once on the test side and once in the production code, their separate complimentary streams meet at a successful execution of the test (like the credits and debits meet at 0 in double entry book keeping.)
