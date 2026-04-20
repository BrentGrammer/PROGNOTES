# Acceptance Testing

### Main purpose
- To faciliate communication between software engineers and customers, business domain experts and stakeholders
- The tests should be in a format that can be written by customers (or business stakeholders)
- The main benficial effect of these tests is facilitating the intellectual planning and communication of what the software should do from a business perspective
- These tests are supposed to be written BEFORE the software code is written
- *** The perspective is different from TDD - instead of testing the expression of the code, the perspective shifts to that of the customer and business
  - This can replace expensive UI tests because the functionality is similar to that which would power UI E2E tests.

### Do we still need QA?
- The QAs cover all of the weird ways humans can use and break the software which automated tests are not good at covering.U

### Origin of AC
- Software for military equipment such as fighter jets and financial systems
- Uses user requirements as main driver to verify behavior
- Example: Taking the user guide for the HP35 Calculator and using that to build requirements for acceptance testing
  - tells users what they can do
  - gives enough specification for a developer to figure out what they need to do to make the software meet the requirements

## ATDD (Acceptance Test Driven Development)

- The FIXTURE: a very simple object that you simply pass input into and expect output from which is used in the tests. You might start implenting basic test passing behavior here, but the actual implementation does not exist in this object.
  - The fixture is for the purpose of testing and delegates all input to the actual class with the real implentation in prod code
- The goal to start is to get the tests to pass with the dumbest way possible (implementation details will be figured out later)


## Planning

- Too many details are not necessary or even possible in initial planning stages and meetings
- The Law of Large Numbers: results stabilize with more experiments. 
  - Think of stories as experiments which reveal more data that converges on accurate estimations, details and outcomes over time

### When to write Acceptance Criteria (Just in Time)
- The first activity for any story is writing the acceptance criteria when it is created (Just in Time requirement writing)
  - This gaurantees having the latest up to date information at that time which is less prone to error if you do it before
  - The details are also fresh and will not be forgotten or lost in the passage of time normally. The story is worked on immediately
- The Acceptance Tests are specified at the beginning up front. and When those tests pasts the work is unambiguously Done.

lef off 18:00