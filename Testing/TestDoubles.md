# Test Doubles

### 5 kinds of test doubles:

#### Dummy (hard coded null or string value for ex.)

- Needed when you need to pass something to a unit class or method under test
- Usually it is None/Null or an empty set/collection.
- Indicates a design smell of too many compulsory arguments (you can use a default argument set to Null to remove the need to pass a dummy in)
- The dummy is a placeholder and not used in the case you are testing.

#### Stub (configured dependency that returns values based on different scenarios)

- Simple controlled replacement, use these when it is easier to use this over the real collaborator object in tests.
- Has the same interface as the object that it is replacing in the test.

#### Fake (usually implemented to replace a dependency that doesn't exist yet, similar to stubs).

- Fakes have an implementation that works and is suitable to the test env, as opposed to stubs which return fixed values
- Ex: File in python can be replaced with io.StringIO (same interface and avoids working with file system in tests)
- A real database can be replaced with an in memory database
- A real webserver can be replaced with a lightweight one.
- Purpose is to make tests run faster and not have to write as much code using fakes as you would if you used a stub.

#### Spy

- Unlike a stub, makes assertions about what happens in the test case
- used in Method Call assertions: check that a function got called. (Uses Mock or Spies)
- **Records any interactions, so you can make assertions on what happened afterwards** - it "spies" on the object and what happens to it.

#### Mock

- Unlike a stub, makes assertions about what happens in the test case
- see [demo](https://app.pluralsight.com/ilx/video-courses/5a80aa07-b192-4111-a612-473392f6bdf9/ee9ce99a-d229-4203-a798-7f8bc834e40c/107da86b-4c34-4556-97b1-6cf089bfafcc) of a mock.
- Method Call assertions: check that a function got called. (Uses Mock or Spies)
- A mock is set up in advance with expectations for the calls that should happen, but if they don't happen as expected, then it raises an exception inside the mock implementation that occurs during the act part of the test (a spy raises the error afterwards in the assert phase of the test).

### These can be consolidated into two basic types:

- Mocks (Mock and Spy)
- Stubs (Dummy, Stub, Fake)

- From simplest to moving towards aactually replacing the collaborator in the test: Dummy > Stub > Fake > Spy > Mock

### When to use Test Doubles:

- When the unit of code you are testing has a dependency on some other code and you don't want to use the real dependency.
- If you have a collaborator that is awkward to use in a test, replace it with a Dummy, Stub or Fake. (Stub is a good choise most of the time)
- If you want to test the contract between a unit under test and a collaborator, use a Spy or a Mock.
  - Spies and Mocks ensure that interactions are correct.
  - **Mocks check that method calls happen in the right order or with the correct arguments.**

### Disadvantages of Test Doubles:
- Add complexity, make tests harder to understand, can lead you to think you're testing something that you are not.
- Test Doubles get out of sync with the real objects they replace (the real object can change causing the code to no longer work, but the test will pass since it is using an old mock that still works.)
- Hinders refactoring - doubles can be tied to the implementation details of your source code.

## Mocks

A mock is a test double that allows you to examine interactions between the system under test (SUT) and its collaborators.

- Mocks can make tests fragile and should be used with discretion

### Mocks vs. Spies

- Spies and mocks are similar in that they both check for correct interactions.
- A mock will explode EARLIER in the test which can be helpful if you want to stop execution as soon as something goes wrong (you will get a stack trace that points to the heart of the production code). A spy will only tell you something went wrong afterwards.
- Spies are simpler to implement and easier to understand.

### Mocks vs. Stubs

- Mocks deal with outcoming interactions (those calls made by the SUT to dependencies that have a side effect such as sending an email or updating an external service)
- Stubs deal with incoming interactions (calls that the SUT makes to dependencies that have no side effects, for example, getting data from the database)
- **Mocks are used to emulate and EXAMINE interactions while stubs only emulate the interactions.**

Example of a Mock (for an outcoming interaction):

```c#
[Fact]
public void Sending_a_greetings_email()
{
    var mock = new Mock<IEmailGateway>();
    var sut = new Controller(mock.Object);
    sut.GreetUser("user@email.com");
    mock.Verify(
        x => x.SendGreetingsEmail(
        "user@email.com"),
    Times.Once);
}
```

Example of a Stub (incoming interaction):

```c#
[Fact]
public void Creating_a_report()
{
    var stub = new Mock<IDatabase>();
    stub.Setup(x => x.GetNumberOfUsers())
        .Returns(10);
    var sut = new Controller(stub.Object);
    Report report = sut.CreateReport();
    Assert.Equal(10, report.NumberOfUsers);
}
```

#### Spies

- Serve the same role as mocks, but are written manually (mocks are made using a mocking framework). AKA "Hand written mocks"

### Mocking guidelines

- **never assert interactions with stubs**. (Stubs only emulate interactions but are not used for examination). A call from the SUT to a stub is not part of the end result the SUT produces. Such a call is only a means to produce the end result: a stub provides input from which the SUT then generates the output.
  - Asserting on stubs makes for fragile tests and is an anti-pattern. The goal of tests is to verify the end result, ideally meaningful to a non developer, not implementation details.
  - asserting on a stub does not verify an outcome - the stub is a detail in how the outcome is eventually acheived and therefore makes the test brittle if that detail changes.
    - This anti-pattern is called OVERSPECIFICATION, most commonly occurs when examining interactions - tests shouldn't check any interactions with stubs.
  - Example of a brittle test (verifying a stub that retrieves data):
  ```c#
  [Fact]
  public void Creating_a_report()
  {
      var stub = new Mock<IDatabase>();
      stub.Setup(x => x.GetNumberOfUsers()).Returns(10);
      var sut = new Controller(stub.Object);
      Report report = sut.CreateReport();
      Assert.Equal(10, report.NumberOfUsers);
      stub.Verify(
          x => x.GetNumberOfUsers(),
          Times.Once); // This is asserting on a stub that retreives number of users, which is an anti-pattern
  }
  ```
  - Sometimes you can have double that acts as both a mock and a stub:
  ```c#
  [Fact]
    public void Purchase_fails_when_not_enough_inventory()
    {
    var storeMock = new Mock<IStore>();
    storeMock
        .Setup(x => x.HasEnoughInventory(  // storeMock is a stub here - sets up a canned answer/interaction
            Product.Shampoo, 5))
            .Returns(false);
    var sut = new Customer();
    bool success = sut.Purchase(
    storeMock.Object, Product.Shampoo, 5);
    Assert.False(success);
    storeMock.Verify(
        x => x.RemoveInventory(Product.Shampoo, 5), // storeMock is a mock here, a different method on the object is verified that is a desired outcome and result.
        Times.Never);
    }
  ```

#### CQS (Command Query Separation)

- every method should be a command (with side effects) or a query (no side effects), but not both
- Command methods should not return a result, they should return void. Query methods return a result and has no side effect.
  - This is a general rule of thumb, sometimes there are exceptions. Stack.pop() for example returns a value and has the side effect of modifying the target structure.
- Test Doubles that substitute a command are Mocks, and doubles that substitute a query are stubs:

```c#
// mock - side effect command of sending email
var mock = new Mock<IEmailGateway>();
mock.Verify(x => x.SendGreetingsEmail("user@email.com"));

// stub - no side effect, query of number of users.
var stub = new Mock<IDatabase>();
stub.Setup(x => x.GetNumberOfUsers()).Returns(10);
```

### Mocks and Test Fragility

- Production code divided into categories:
  - Public or Private API
    - Ideally the public API should coincide with the system's observable behavior, with private api hidden from clients
  - Observable behavior or implementation details
- **Observable Behavior**: The end result that the code produces.
  - For a piece of code to be part of observable behavior, it needs to help the client achieve one of its goals. For a domain class, the client is an application service; for the application service, it’s the external client itself.
  - Code that is not implementation but part of observable behavior satisfies two conditions:
    1. Exposes an operation that helps the client achieve one of its goals and has an immediate connection to those goals. An operation is a method that performs a calculation or incurs a side effect or both.
    2. Exposes a state that helps the client achieve one of its goals. State is the current condition of the system.
  - A client could be from the same code base, an external application, or the user interface
  - Ideally public API methods cooincide with observable behavior and private APIs cooincide with implementation details

#### Leaking implementation details into public API

- Example: A User controller (the client) that needs to call `user.NormalizeName(newName);` and then `user.Name = normalizedNewName;`
  - user's API exposes an invariant of normalizing the name (i.e. restricting to max of 50 chars) which is not IMMEDIATELY related to the client controllers goal of changing a user name.
  - _invariant_: A condition that should be held true at all times.
- Do not leak implementation details to clients. User should hide normalizing the name in the setter so that UserController can just call `user.Name = newName;` and then save to the database.
- **Rule of thumb** - do determine if you are leaking details to clients, a rule of thumb is to check that ideally, any individual goal should be achieved with a single operation. In the above example, UserController had to call `user.normalizeName()` and `user.Name = normalizedName` to achieve it's goal - in the cleaner version, the controller only calls one set operation to set the new name. (UserController's goal was not to normalize the name, but to change it).
  - especially holds for majority of cases where business logic is involed.
- You should only be verifying and testing the only output that the client using the code would care about. A well designed API will automatically make your tests better because you leave the test no choice but to use the public operation directly related to the goal and desired output.

#### Encapsulation

- A well designed API will conform to the best practice of encapsulation (the act of protecting your code against inconsistencies, also known as invariant violations. An invariant is a condition that should be held true at all times.)
  - exposing implementation details often leads to invariant violations. (you shouldn't allow the client, i.e. UserController, to bypass setting a normalized name as above)
- Encapsulation is crucial for managing complexity of the system
- The API should guide you on what is and what is not allowed to do with the code.
- Means of acheiving encapsulation:
  - bundle functions/operations and data together ("Tell don't ask") - to make sure the operations don't violate invariants.
  - hide implementation details to remove internals from eyes of clients so they can't use them to corrupt internal state or data.

#### Hexagonal Architecture Layers

- External Client -> Application Services layer -> Domain/Business logic layer
- Separation of concerns, the Client provides a goal, the application layer orchestrates translating that goal into a domain object to run operations to achieve it
- Testing application and domain layer is fractal - the Client provides use cases, which you test the observable behavior of the application layer to acheive those, and then test that the domain layer's observable behavior achieves the sub-goals necessary to tie back to the Client's use case.
- The client of the application layer is the External Client, the client of the domain layer is the application layer
  - Ex: the CustomerController class is an application service that
    orchestrates the work between domain classes (Customer, Product, Store) and the
    external application (EmailGateway, which is a proxy to an SMTP service).

#### Intra- vs. Inter-system communication

- Intra-system comms is communication between classes in a layer, inter-system comms is communication with an exterrnal API or service
- Intra-system communications are implementation details because the collaborations your domain classes go through in order to perform an operation are not part of their observable behavior. These collaborations don’t have an immediate connection to the client’s goal. Thus, coupling to such collaborations leads to fragile tests.
- Inter-system communication is observable behavior - how your application talks with the external world
  - One of the main principles of such an evolution is maintaining backward compatibility. Regardless of the refactorings you perform inside your system, the communication pattern it uses to talk to external applications should always stay in place, so that external applications can understand it

**MOCKS can be used to verify the communication pattern between your system and external applications**
**MOCKS should NOT be used to verify communication between classes in your system (probably in the same layer?), this ties them to implementation details and makes them brittle**

### Mocking Inter-system communication

- Example would be a customer purchase use case where an email receipt is sent on success. This is an observable outcome and involves communicating with the external email service

```c#
[Fact]
public void Successful_purchase()
{
    var mock = new Mock<IEmailGateway>(); // mock communication with external service
    var sut = new CustomerController(mock.Object);
    bool isSuccess = sut.Purchase(
    customerId: 1, productId: 2, quantity: 5);
    Assert.True(isSuccess); // isSuccess is also needed by the client (the external client) and so is an observable outcome that helps the client achieve it's goal and verified.
    mock.Verify(
        x => x.SendReceipt(
        "customer@email.com", "Shampoo", 5),
        Times.Once);
}
```

- Note in the test we aren't verifying anything about the intra-system communication (i.e. between Customer and Store which checks inventory before allowing success)
- The `Store.removeInventory` method that occurs when product is purchased is an intermediate step and not directly related to the CustomerController's goal of making a purchase or getting information about the state in order to achieve it's goal.

### When to Mock

#### Types of Dependencies:

- Shared dependency—A dependency shared by tests (not production code)
- Out-of-process dependency—A dependency hosted by a process other than the pro-
  gram’s execution process (for example, a database, a message bus, or an SMTP
  service)
- Private dependency—Any dependency that is not shared

#### Mock (some) shared out of process dependencies

- A shared out of process dependency that is shared like a database could? be mocked or stubbed. (see notes below for caveat though)
  - If a shared dependency is not out-of-process, then it’s easy to avoid reusing it in tests by providing a new instance of it on each test run.
- DO NOT verify (mock) shared out of process dependencies that are only available in the application since they are not externally observable. (stub them or have a shared instance like a test database, but do not verify on them as you would a mock - they are implementation details)
  - A good example here is an application database: a database that is used only by
    your application. No external system has access to this database. Therefore, you can
    modify the communication pattern between your system and the application database
    in any way you like, as long as it doesn’t break existing functionality. Because that data-
    base is completely hidden from the eyes of the clients, you can even replace it with an
    entirely different storage mechanism, and no one will notice.
  - The use of mocks for out-of-process dependencies that you have a full control over
    also leads to brittle tests.
- Mocks are often said to verify behavior. In the vast majority of cases, they don’t. The
  way each individual class interacts with neighboring classes in order to achieve some
  goal has nothing to do with observable behavior; it’s an implementation detail.
- The client doesn’t care what neurons in your brain light up
  when they ask you to help. The only thing that matters is the help itself—provided by
  you in a reliable and professional fashion, of course. Mocks have something to do with
  behavior only when they verify interactions that cross the application boundary and
  only when the side effects of those interactions are visible to the external world.

**Mocking is legitimate only when it’s used for inter-system communications—communications that cross the application boundary—and only when the side effects of those communications are visible to the external world.**

### Further Resources

- Recommended mocking tool for C#/XUnit: Moq
