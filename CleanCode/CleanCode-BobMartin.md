TDD:
3 rules:
You are not allowed to write any production code unless it is to make a failing unit test pass.
You are not allowed to write any more of a unit test than is sufficient to fail; and compilation failures are failures.
You are not allowed to write any more production code than is sufficient to pass the one failing unit test.

Try to write tests that force exceptions, and then add behavior to your handler to sat-
isfy your tests. This will cause you to build the transaction scope of the try block ﬁrst and
will help you maintain the transaction nature of that scope.

FIRST: Fast, Independent, Repeatable, Self-validating, and Thorough

- separate unit tests from integration tests and only run unit tests during development - they are fast and will not slow you down.https://www.artima.com/weblogs/viewpost.jsp?thread=126923

EXCEPTIONS:

- the purpose of exceptions is to allow you to handle errors at a distance
- Checked exceptions can sometimes be useful if you are writing a critical library: You
  must catch them. But in general application development the dependency costs outweigh
  the benefits.
- Create informative error messages and pass them along with your exceptions. Men-
  tion the operation that failed and the type of failure
- Often a single exception class is ﬁne for a particular area of code. The information
  sent with the exception can distinguish the errors. Use different classes only if there are
  times when you want to catch one exception and allow the other one to pass through.
- Do not return Null in the handler - it requires null checks throughout the program and complicates logic.

wrapping third-party APIs is a best practice.
Ex:

- because we know that the work that we are doing is roughly the same
  regardless of the exception, we can simplify our code considerably by wrapping the API
  that we are calling and making sure that it returns a common exception type:
  LocalPort port = new LocalPort(12);
  try {
  port.open();
  } catch (PortDeviceFailure e) {
  reportError(e);
  logger.log(e.getMessage(), e);
  } finally {
  …
  }
- inner class to catch the api exceptions and translate them to the generic wrapper exception:
  public class LocalPort {
  private ACMEPort innerPort;
  public LocalPort(int portNumber) {
  innerPort = new ACMEPort(portNumber);
  }
  public void open() {
  try {
  innerPort.open();
  } catch (DeviceResponseException e) {
  throw new PortDeviceFailure(e);
  } catch (ATM1212UnlockedException e) {
  throw new PortDeviceFailure(e);
  } catch (GMXError e) {

FUNCTIONS:

- try to avoid returning null, instead return a default value.
- If you are tempted to return null from
  a method, consider throwing an exception or returning a SPECIAL CASE object instead. If
  you are calling a null-returning method from a third-party API, consider wrapping that
  method with a method that either throws an exception or returns a special case object.
  - Special Case Object pattern: encapsulate handling the special case that returns the expected value inside the callee
- no arguments are best, 3 arguments at most.
- avoid ambiguous boolean arguments, this suggests the function does more than one thing
- avoid passing null in your code whenever possible.
- In most programming languages there is no good way to deal with a null that is
  passed by a caller accidentally. Because this is the case, the rational approach is to forbid
  passing null by default

CLASSES:

- Avoid static methods if possible
- Hide internals and use public methods to wrap them and expose BEHAVIOR, not internal details
- Data structures can expose internals (have no functions), but classes should not

CONCURRENCY:

- Errors can occur randomly since there could be thousands of paths the concurrent code can take, very difficult to reproduce
- Testing should be done regularly and for as long as possible to catch errors that occur infrequently
- Thread Jiggling is a way of testing for errors
- 3 main problems: Deadlock, Livelock, Concurrent updates
