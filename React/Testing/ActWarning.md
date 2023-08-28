# Act

## ACT WARNING:

[S Grider's video on ACT](https://www.udemy.com/course/react-testing-library-and-jest/learn/lecture/35701738#content)

- common when fetching data in `useEffect()`
- usually caused by async actions in a `useEffect`, i.e. promises
  - After the promise is resolved some state is updated - this is usually the culprit
- defines a window in time when state updates can and should occur
- originally comes from react-dom
  - react-testing-lib wraps a lot of actions for you in act automatically:
    - `waitFor`, `screen.findBy`, `screen.findAllBy`, `user.keyboard`, `user.click` are all automatically wrapped in `act`
  - without react-testing-lib you would need to wrap any code that would change the state in an act wrapper (i.e. rendering a component, clicking a button etc)
    - Wrapping in act sets up a window of time for state updates under the hood
    - React will process all updates and useEffects before exiting the 'act'
    - _Any state updates that occur **outside** of the window will result in the 'act warning' in the terminal_

## Solving the Act Warning:

[S Grider's video](https://www.udemy.com/course/react-testing-library-and-jest/learn/lecture/35701742#overview)

- If you can avoid wrapping and using `act` manually, you should ideally use a RTL method that uses act for you:
  - Try to use one of RTL's methods instead of wrapping code in your test in `act`
    - usually you want to use `screen.findBy`, `screen.findAllBy`, or `waitFor`
- Find the log in terminal that says: "An update to {componentName} inside a test was not wrapped in a act(...)."

  - Find that component
  - See if there is a useEffect with any async Promise code that updates state when the Promise resolves.
  - try to use a `findBy` or `findAllBy` in the test to detect when the state update has finished (look for something in the screen that appears when the data has fetched or the update has occurred)

    - go to the test that was throwing the warning and mark the test function as `async`
    - Basic debug method to find something to look for when the data is done fetching etc.:

    ```javascript
    const pause = () => {
        return new Promise(resolve) => {
            setTimeout(() => {
                resolve();
            }, 100)
        }
    }
    // in the test throwing act warning, pause a little between events or fetching to find something to find by
    it("my test", async () => {
        renderComponent();

        screen.debug();
        await pause();
        screen.debug();
    });
    ```

    - After seeing difference in screen output use RTL methods wrapped in act to find the elements that are on the screeen after fetching data or state update has ooccurred

    ```javascript
    it("my test", async () => {
      renderComponent();
      // find an image that appears on the screen after the useEffect state update occurred (this could alternatively be data that was fetched that shows on screen)
      await screen.findByRole("img", { name: /javascript/i });
    });
    ```

https://kentcdodds.com/blog/fix-the-not-wrapped-in-act-warning

- happens when there is an update that React did not expect in the test
  (example - a third party function calls a state updater during the course of
  the test where the state update was not called directly by you in the test).
  Prompts you to account for state updates usually when calls are made
  asynchronously for example to an API via a hook or when you manually update
  state via mock hooks etc.. Makes sure the state updates are flushed before
  moving on with the test.

the act() wrapper function is used to make sure that the state update triggered
by setReturnValue(fakePosition) is fully processed before the test continues.
This is important because if the test continues before the state update is
processed, it could lead to unexpected results or errors.

\*\*Note that userEvent and methods from testing library automatically wrap
things in act so you don't have to. You use act() when needed due to an
unexpected state update you are telling React you expect and are doing on
purpose.

"flushes" means to ensure that all pending updates to the component tree are
processed before moving on to the next step of the test. In other words, it
ensures that any state changes are fully processed before any further actions
are taken in the test.

- anytime a update occurs you need to use act, but testing library does it for
  you: . It's built-into React Testing Library. There are very few times you
  should have to use it directly if you're using React Testing Library's async
  utilities.

you're supposed to wrap every interaction you make with your component in act to
let React know that you expect updates. (testing library does some of this for
you)

From the article: So the act warning from React is there to tell us that
something happened to our component when we weren't expecting anything to
happen. So you're supposed to wrap every interaction you make with your
component in act to let React know that we expect our component to perform some
updates and when you don't do that and there are updates, React will warn us
that unexpected updates happened. This helps us avoid bugs like the one
described above.

Luckily for you and me, React automatically handles this for any of your code
that's running within the React callstack (like click events where React calls
into your event handler code which updates the component), but it cannot handle
this for any code running outside of it's own callstack (like asynchronous code
that runs as a result of a resolved promise you are managing or if you're using
jest fake timers). With those kinds of situations you typically need to wrap
that in act(...) or async act(...) yourself.

explanation of outside the callstack: code that is running outside of the React
call stack is any code that is not directly triggered by a React event or
lifecycle method. For example, if you have an asynchronous function that updates
the state of a component after a delay, that code is running outside of the
React call stack. React doesn't know when that code is going to finish running,
so it can't automatically handle updates caused by that code.
