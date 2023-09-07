Note from pragmatic programmer: if you have writers block when writing a new module, just start writing a prototype and tell yourself it will be thrown away anyways to take the pressure off.

Unit test:

1. tests small portion of code
2. runs fast
3. isolated

Code coverage:
Line coverage - if line was run
Branch coverage - if and switch branches

Two schools
Classical: test isolated(but different from London), Martin Fowler svhool
London: mock everything all dependencies, but the class under test, nat price school

Test Double (comes from stunt double term)
Mocks are a type of test double

When to mock?
When dependencies are shared between tests (database) or are volatile (date generator or store).
Do not mock immutable dependencies (i.e. a Product value object)

In classical you only mock shared dependencies (i.e. a db)
In London you mock shared, and other injectected dependencies to completely isolate the class

Types of dependencies:
Shared, Volatile, Private (internal to test)

Collaborates: dependencies that are shared or mutable (adapter to db or a store)
Value objects are not collaboraters (they are immutable dependencies)

Author recommends classical over London style testing.
London: more mocks make for fragile tests. Advantages are you know exactly what failed and whetre when a bug happens since the tests are so isolated.
Classical unit tests will cascade failures and will be more difficult to findthe bug. But \*\*you should always run tests after each code change so if they fail you know the bug is the change you just made.

\*\*\*Test a unit of behavior, ideally in a way a business person understands the test! A unit of behavior is a meaningful business piece of behavior that can span multiple classes or be a single method. This is the primary advantage of classical unit testing (where all dependencies are not always mocked).

Primary problem with London style testing is it couples tests to implementation details.

Ch 2

TDD

Classical: inside out- start with domain and build up to something usable by the user
London: outside in, start with collaborator dependencies, define them first.

Classical unit test:

1. Tests single unit of behavior
2. Runs fast and quickly
3. Tests are isolated from one another (in London style, units of code i.e. classes are isolated from one another)

**_Tests should have only one act line, if more it is a sign of lack of encapsulation.
_**If asserts become to large in test it is a sign of missing abstraction

Shared arrangements in tests:

Fixture - a object that remains in a fixed state and is shared by tests.

Test names: generally do not put the class or method name in the test. Use the business case in plain English for the name. Avoid "should" and use "is" instead - describe a "fact" about the behavior of the system. Separate words with underscores.
This way if method changes, you don't need to change the test and it reads better.

Good test attributes:

1. resistant to regressions (catch bugs)
2. resistant to refactoring (decoupled from implementation)
3. Fast feedback
4. maintainable

Reducing coupling:
Humble object: a thin wrapper that wraps abstracted or injected complex business logic.
I.e. a controller that delegates or orchestrates and calls business logic methods from other classes that encapsulate that logic separately.

Controller
if (user.canAddEmail) user.addEmail;
// User has control flow delegated to it and controller is the humble object that just delegates or orchestrates the external abstractions with business logic.

Note: controllers orchestrate collaboraters between the domain model and out of process dependencies.

\*"Should aim to separate domain logic from out of process dependencies!
Ex: a class that uses a dispatch event class to handle what event comes in and then delegate calling the out of process dependency (ie a db or message bus) to the event dispatcher which translates the event given into a call to the out of process dep).

Integration tests:

- test the longest happy path (most interactions)and any edge cases that couldn't be covered in unit tests.
  Probably will have one or two integration tests

- do not mock managed out of process dependencies (i.e. a database that only the app uses). Only mock unmanaged out of process dependencies (async apis third party etc.)

Note on unnecessary interfaces:

- interfaces as abstractions are only necessary if there is more than one implementation they cover, otherwise they add complexity. Don't over abstract !

Observable behavior = behavior of the app that is observable by anyone outside just the developers (business users, stakeholders, customers etc).
Only test this behavior, everything else is implementation details.
Focus on the final state or outcome from a business event or action.

Logging: only test logs if they are read by others, not just the developers.

Do not test pre-conditions unless they are critical to business requirements/observable behavior

Mocks, best practices:

- mocks should only be applied to unmanaged dependencies. Interactions with such dependencies are observable by external applications.
- only mock dependencies at the edge of your app. This makes tests more resistant to refactoring and regressions.
  Ex: do not mock a higher wrapper to an external service or API. Mock the class or function that directly calls the third party API. Mock the last types ie am adapter before communication with the dep.
- mocks are for integration tests only not unit tests. Separation of business logic and orchestration. Code should either communicate with process dependencies or be complex but never both. Two layers: domain model for complexity (unit tests) and controlled for communication.
  Tests for domain model are unit tests, tests for controllers are integration tests.
  Mocks are for unmanaged dependencies only and controllers are the only code working b with those only controller integration tests should have mocks.
- Mock by the last types between your system and the unmanaged dependency. I.e. mock the adapter wrapper that calls the actual dependency.
- duplicate constants from production code, do not duplicate them

Inject time as a value or service
