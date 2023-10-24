# Testing:

*Behave like the user in your tests - how do they find a button on the page
(with their eyes, by text, or with a screen reader, by Role and name). *If I
were a manual tester, how would I test this? Make the test do the answer to that
question.

\*The more your tests resemble the way your software is used, the more
confidence they can give you. (ex: how does a user use the app)

## Basic Testing:

Testing library docs:
https://testing-library.com/docs/react-testing-library/api/

- Note: React testing library is a react version of dom-testing-library and
  built on top of it.

- Jest uses JS-DOM which is a simulated DOM and has some
  limititations/differences between the real browser. If you need to test things
  that really depend on browser APIs like drag and drop for example then you
  would be better off testing in Cypress with a real browser.

- You should use testing library's jest-dom package for assertions that give you
  better error messages.
  - install with npm
  - setup instructions: https://github.com/testing-library/jest-dom#usage
    - Add setupFilesAfterEnv: ['<rootDir>/jest-setup.js'] to setup file
    - see video at 1:50 in Epic React Testing section 3, "Assertions"
      - note: CRA does not allow configuration of jest in this way, see below:
    - for create-react-app, create setupTests.js in src folder, add
      `import '@testing-library/jest-dom/extend-expect';`
  - ex: expect(message).toHaveTextContent('content'); <-- toHaveTextContent is
    provided by jest-dom

Example setup:

```javascript
import {render} from '@testing-library/react'

test('basic test', () => {
  const {container} = render(<MyComponent />)
// render returns a view/utils object that has the component's container element on it (to use for query selecting if needed).

  const [myButton] = container.querySelectorAll('button')
}
```

### PATTERN FOR GETTING ELS/ROLES etc:

1. Select element in browser dev tools inspect
2. Check Accessibility tab -> computed properties (check role, name etc.)
3. Use Testing Playground site or extension to get a suggested query.

In the test you can also do: const myEl = screen.getByRole('blah') // this will
show an error message that will list available roles to choose and what element
they are for(ignore general at the top)

## CLEANUP:

- You need to make sure your tests are isolated and that you clean up
  after/before each test.
  - ex, remove elements from the DOM or clear it in a beforeEach() call
- React testing library used with Jest automatically cleans up components that
  were rendered with the library's 'render()' function and you don't need to
  manually clean those up.

## Principles and tips:

- Avoid testing implementation details.
  - Think about how the user would find a button
  - Can go to dev tools, click chevron and go to Accessibility- 0:38 on Screen
    Utility video under section 4 - Avoid Implementation Details (Testing
    videos)
    - The idea is to find the elements the way a user would, in this case a
      screen reader.
    - The Accessibility tree shows you what element is selected (select it with
      inspect etc)
    - Under Computed Properties, you can see the browser builtin Role and name
      which you can use to grab it in the test using React-Testing-Library's
      screen utility

Setup: import utilities for testing and render the component:

```javascript
import {render, screen, fireEvent} from '@testing-library/react'
```

... render(<App />);

Example: user finding a button:

```javascript
const incrementButton = screen.getByRole('button', {name: /increment/i}) // case insensitive - the user does not care about the case, just the word.
// this is what the screen reader looks for and is from computed properties in Accessibility dev tools when you select the element.
```

Example getting a screen element by text (instead of query selecting the
element):

```javascript
// don't do this!! this is implementation details and could break with changes.
const message = container.firstChild.querySelector('div')
// Do this instead:
const message = screen.getByText(/current count/i)
//the user looks for this text to find the message.
```

## TESTING TOOLS AND UTILITIES:

\*\*Good site: https://testing-playground.com/

- Allows you to input html and it will suggest what query to use to select the
  element in your test!

\*\*Testing playground has an extension you can install as well to use directly
in the devtools after selecting an element.

Use `screen.debug()` to check the html of the rendered component.

**Seeing ALL output in terminal if cut off**:
- `screen.debug(undefined, Infinity);`

// Deferred helper

- use `queryBy` instead of `getBy` (ex. queryByLabelText()) when asserting
  something is not in the document (getBy will throw an error if the element is
  not found)
  - `expect(screen.queryByLabelText(/loading/i)).not.toBeInTheDocument()`

### PROMISES:

- example in Mock Geolocation video in the testing section videos., lesson 7
  Mocking Browser APIs and Modules.
- can make a deferred helper which returns a promise and refs to resolve and
  reject to use

```javascript
let resolve
let reject
const promise = new Promise((res, rej) => {
  resolve = res
  reject = rej
})
```

- call resolve on the promise to tell it to resolve
- then use `await promise` to wait for it to resolve: resolve(); await promise;
- can be useful if you're testing a component that shows loading while a
  promise/call resolves and then want to test that the loading is gone after
  resolution and screen is updated.

You may need to make an async act wrapper (see Add an async act to Resolve a
Promise video under Testing Hooks and Components section in the final project of
Epic React).

await act(async () => { resolve() await promise // the promise the next tick
depends on, i.e. that a hook calls for ex. then you want to check the after
effects })

- If you are testing the rejection of a promise, you may need to catch it in the
  test since a promise rejection will cause an error in a jest test (see Call
  Run with a Promise that Rejected video under Testing hooks section of Epic
  React final project).

```javascript
const rejectedValue = Symbol('rejected')
await act(async () => {
  reject(rejectedValue)
  // catch the rejected promise to prevent error in jest test, since we know we are rejecting on purpose:
  await promise.catch(() => {
    // ignore error
  })
})
```

-- within helper --

- Scope queries to an element or component:

```javascript
//...imports
import {render,screen,within} from '@testing-library/react'

// within functions as screen but scopes queries to search within scope passed
const inModal = within(modal) expect(inModal.getByRole('heading', {name: 'Modal
Title'})).toBeInTheDocument()
```

### Asymmetric Matchers

Use when you don't care about the actual value ex: `expect.any(Function)` //
value can be a function, any function

#### using Symbol to check for object matches --

- if you need to confirm an object inside an object is something and not just a
  copy, use Symbol: (from add an Async act to Resolve a Promise video under
  testing hooks and components section of epic react final proj)

```javascript
const resolvedValue = Symbol('resolved value') // instead of {data: 'something'}
// this would be something returned from a hook for example, like an object


// now when we ran the hook and check after effects:
expect(result.current).toEqual({ ...other props, data: resolvedValue, })
// original returns object - we don't want to just })
```

### Asserting on console errors

- turn console into a mock/spy - from No State Updates if Unmounted video in
  final Epic React project under Testing Hooks section:

- put the spy and restore setup in beforeEach and afterEach because if a test
  fails before the console spy is restored, then it will not restore the console
  spy for the following tests.

```javascript
beforeEach(() => {
  jest.spyOn(console, 'error')
})

afterEach(() => {
  // restore console at end of tests:
  console.error.mockRestore()
})

// ...
// ... in test:
expect(console.error).not.toHaveBeenCalled() // if checking that a hook console errors something for example when things go wrong.
```

## Web browser events

Gotcha: Act warnings: fireEvent is already wrapped in act, so if you see a
warning about needing `act`, the solution is NOT to wrap the fireEvent in act.

- fireEvent from react-testing-library does not fire all native events (i.e.
  fireEvent.click() does not fire onMouseDown for example).
- You should use user-event from the library to simulate all events as they
  would fire in production on the browser.

Example:

```javascript
import userEvent from '@testing-library/user-event'

userEvent.click(incrementButton)
// fires all native events that normally come with click (this avoids testing implementation details which would break if we use onMouseDown instead of onClick for example)
```

## TESTING FORMS:

- Note: password fields do not have roles for security reasons, so you can't use
  getByRole() to select them. You probably use getByLabelText(/password/i)
  instead.

Example test - test that typing into fields and submitting calls onSubmit with
the right data:

```javascript
import {render, screen} from '@testing-library/react'
//use faker to indicate that values typed are not constant and can change
import faker from 'faker'

// reusable Object Mother/Test Object Factory function to use in tests:
function buildLoginForm(overrides) {
  return {
    username: faker.internet.userName(),
    password: faker.internet.password(),
    ...overrides,
  }
}

test('submitting the form calls onSubmit with the username and password', () => {
  const mockSubmit = jest.fn() // mock to keep track of calls
  render(<Login onSubmit={handleSubmit} />)
  const {username, password} = buildLoginForm()

  userEvent.type(screen.getByLabelText(/username/i), username)
  userEvent.type(screen.getByLabelText(/password/i), password)
  expect(mockSubmit).toHaveBeenCalledWith({username, password})

  // make sure it's only called once as well - multiple submits would be problematic on the form
  expect(mockSubmit).toHaveBeenCalledTimes(1)
})
```

## Mocking HTTP Calls:

- use Mock Service Worker package:

```javascript
import {rest} from 'msw'
import {setupServer} from 'msw/node'
import {render,screen,waitForElementToBeRemoved} from '@testing-library/react'

const server = setupServer(
  rest.post('https://url/your/app/calls',
    // anytime post req to this endpoint this handler is called:
    (req, res, ctx) => {
        // return what the endpoint should and use ctx json util for the body
	if (!req.body.password) return res(ctx.status(400), ctx.json('password required'))
	// simulate what the backend does (i.e. if invalid request sent)
	if (!req.body.username) return res(ctx.status(400), ctx.json('username required'))
	return res(ctx.json(usernamne: req.body.username))
    }
)

// start the server before tests run and cleanup after all tests are finished
beforeAll(() => server.listen())
afterAll(() => server.close())

test('logging in displayes the username', async () => {
  render(<Login />)
  const {username,password} = buildLoginForm()

  userEvent.type(screen.getByLabelText(/username/i), username)
  userEvent.type(screen.getByLabelText(/password/i), password)

  userEvent.click(screen.getByRole('button', {name: /submit/i}))
  // use waitForElementToBeRemoved while loading is showing
  await waitForElementToBeRemoved(() => screen.getByLabelText(/loading/i))

  expect(screen.getByText(username)).toBeInTheDocument()
})

// NOTE:
//  You can use msw to simulate server responses and share that for use across the app in development or test:

// - use ctx.delay if you need to simulate time fetching the request.

const handlers = [
  rest.post('url',
    async (req,res,ctx) => {
        ...include checking invalid bodies and sending back 400 etc.
	return res(ctx.delay(delay),ctx.status(200),ctx.json('success'))
    }
  ),
  // ...more handlers
]

// in test file:
const server = setupServer(...handlers);

// Test unhappy path in login form:
test('ommitting password results in error', async () => {
  render(<Login />)
  const {username} = buildLoginForm()

  userEvent.type(screen.getByLabelText(/username/i),username))

  userEvent.click(screen.getByRole('button', {name: /submit/i}))

  await waitForElementToBeRemoved(() => screen.getByLabelText(/loading/i))

  expect(screen.getByRole('alert')).toHaveTextContent('password required');
})
```

## USING SNAPSHOTS:

- Useful for testing checking error messages and similar situations where the
  text can change slightly, but you don't want the test to break

Example:

```javascript
test('ommitting password results in error', async () => {
  render(<Login />)
  const {username} = buildLoginForm()

  userEvent.type(screen.getByLabelText(/username/i),username))

  userEvent.click(screen.getByRole('button', {name: /submit/i}))

  await waitForElementToBeRemoved(() => screen.getByLabelText(/loading/i))

// make sure to specify in expect which specific element aspect to snapshot that's important:
  expect(screen.getByRole('alert').textContent).toMatchInlineSnapshot(`leave arg emtpy - code will update automatically on running test.`);
})
/*
To use:
1. run the test to create the snapshot - this will update the expect result automatically
2. if the code changes in the future, test will fail.  you will be prompted to update the snapshot with pressing `u` - press that toupdate.

*Now your messages will be updated to the snapshot automatically if they change in the future using this process and you won't have to change the test if the message changes slightly.
*/
```

### THROWING ERROR EXPECTS USING SNAPSHOT:

```javascript
const {result} = renderHook(() => useAsync())

expect(() => result.current.run()).toThrowErrorMatchingInlineSnapshot(
  `this will be populated by jest to auto-match your error msg`,
)
// press `u` to update the snapshot if the error message changes in the future when running this test..
```

## OVERRIDE MSW SERVER HANDLER:

- You may need to override your handler for a specific test only (i.e. throw a
  random 500 error)

```javascript
beforeAll(() => server.listen()) afterAll(() => server.close()) // cleanup the
handlers to reset them to what you originally assigned before each test
beforeEach(() => server.resetHandlers())

test('unknown server error displays the error message', async () => { const
testErrorMessage = "error" // override handler for endpoint to return a 500
server.use( rest.post( 'url', async (req,res,ctx) => { return
res(ctx.status(500), ctx.json(testErrorMessage)) } ) );

render(<Login />) const {username,password} = buildLoginForm()

userEvent.click(screen.getByRole('button', {name: /submit/i}))

await waitForElementToBeRemoved(() => screen.getByLabelText(/loading/i))

expect(screen.getByRole('alert')).toHaveTextContent(testErrorMessage)
// wed don't use snapshot here since we override the call with our own message in the test
```

## TESTING STYLES:

- use `.toHaveStyle()`

```javascript
render(<Button />) const button = screen.getByRole('button', {name:
/button-title/i})
expect(button).toHaveStyle(` background-color: white; color: black;`)
```

## MOCKING MODULES:

- jest.mock will look at for all the imports from the path/module passed in and
  if any of them are functions, it will make them jest mock functions.

Example:

```javascript
// import from the module
import {useCurrentPosition} from 'react-geo-location'

jest.mock('react-use-geolocation')

test('displays current location', () => {
  const fakePosition = { coords: {lattitude: 33,longitude: 44} }

// mock out the function from the package - it returns an array (value and setter)
  // expose the state setter from the package hook to use later to update
  let setReturnValue;
  function useMockCurrentPosition() {
    const state = React.useState([])
    setReturnValue = state[1] // setter
    return state[0] // actual state value
  }

  useCurrentPosition.mockImplementation(useMockCurrentPosition)

  render(<Location />)

  // note: if hook takes args, assert that toHaveBeenCalledWith matches the args
  // expect(useCurrentPosition).toHaveBeenCalledWith(args)

  // check for spinner/pending state when component loads since we set the initial state to empty (this triggers a spinner in the component)
  expect(screen.getByLabelText(/loading/i)).toBeInTheDocument()

  // note that in this case the act is not asynchronous not needed await (?)
  // we wrap in act because we're calling a state updater function, we want to make sure that React flushes all of the side effects that are going to be triggered from the state update before continuing with the rest of the test to ensure all updates are done.
  act(() => {
    setReturnValue([fakePosition]) // module api return value is an array.
  })
})

// *** use queryByLabelText because getByLabelText will throw an error if not in the document!
// queryBy... returns null if it is not found.
expect(screen.queryByLabelText(/loading/i).not.toBeInTheDocument()

expect(screen.getByText(/latitude/i).toHaveTextContent(`Latitude: ${fakePosition.coords.latitude}`
)
expect(screen.getByText(/longitude/i).toHaveTextContent(`Longitude: ${fakePosition.coords.longitude}`
)

```

## ACT WARNING:

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

## CONTEXT TESTING

- Wrap the component being tested in the context that it needs:

```javascript
test('renders with the light styles for the light theme', () => { // create a
wrapper so you can reuse it for rendering const Wrapper = ({children}) => (
<ThemeProvider initialTheme="light">{children}</ThemeProvider> )

// pass in wrapper option using the context wrapper as second arg to render
render(<EasyButton>Easy</EasyButton>, {wrapper: Wrapper})

const button = screen.getByRole('button', {name: /easy/i})

expect(button).toHaveStyle(` background-color: white; color: black; `) })
```

\*\* You can make a reusable render with provider function and pass in the ui
component that needs provider access:

// pass in optional args if you want to use builtin options with render in
addition to wrapper (like hydrate: etc.)

```javascript
function renderWithThemeProvider(ui, {theme = 'light', ...options} = {}) {
  const Wrapper = ({children}) => (
    <ThemeProvider initialTheme="light">{children}</ThemeProvider>
  )
  // return render so you can get things like {container} etc. if needed
  return render(ui, {wrapper: Wrapper, ...options})
}

test('renders with the light styles for the light theme', () => {
  renderWithThemeProvider(<EasyButton>Easy</EasyButton>)

  const button = screen.getByRole('button', {name: /easy/i})

  expect(button).toHaveStyle(` background-color: white; color: black; `)
})
```

## MAKING YOUR OWN TEST UTILS

- Kent Dodds recommends making your own module with custom wrappers (like for
  providing context) instead of directly importing @testing-library/react into
  your test files

- all your tests should be using your own render method (that wraps in context
  etc.) since that is an implementation detail of your components. The
  components in your tests will have all the providers they're going to have
  when you ship the actual app.

1. Create a test-utils.js file that will house react-testing-library exports

```javascript
import React from 'react' import {render as testingLibRender} from
'@testing-library/react' import {ThemeProvider} from 'components/theme'

function render(ui, {theme = 'light', ...options} = {}) {
  const Wrapper = ({children}) => ( <ThemeProvider initialTheme="light">{children}</ThemeProvider>
)

return render(ui, {wrapper: Wrapper, ...options}) }

// export everything from react testing library
export * from '@testing-library/react'

// export your render function that provides all providers the components need
export {render}
```

2. (optional) configure jest configuration so that you can import your test
   utils like a module:

- include the moduleDirectories includes the src folder to treat imports as if
  they are a npm module with
  `moduleDirectories: ['node_modules', path.join(__dirname, 'src')]`.

```javascript
// In jest.config.js at the top level of project (same level as src folder):
module.exports = {
  testEnvironment: 'jest-environment-jsdom',
  setupFilesAfterEnv: [
    '@testing-library/jest-dom/extend-expect',
    path.join(__dirname, 'src/test/setup'),
  ],
  resetMocks: true,
  moduleDirectories: ['node_modules', path.join(__dirname, 'src')],
  ...otherprops,
}
```

3. In your test use the test-utils and render as needed:

```javascript
// in test file:

import React from 'react' import {render, screen} from 'test/test-utils' import
EasyButton from '../../components/easy-button'

test('renders with the light styles for the light theme', () => { // use render
from test-utils that provides app providers for components automatically
render(<EasyButton>Easy</EasyButton>)

const button = screen.getByRole('button', {name: /easy/i})

expect(button).toHaveStyle(`background-color: white; color: black;`) })
```

## TESTING CUSTOM HOOKS:

- Note most hooks should be tested in integration tests, not individual
  component tests.

  - The individual tests should only be used for hooks that are reusable.

- how are they used? they are used in a component so that's how they should be
  tested

  - usually you create a test component in the test that uses the custom hook
    and you test that component instead.

- \*\*Testing custom hooks is something you probably should NOT do.

  - usually the custom hooks are used by a couple components and you should just
    test those components and the hook is tested as an implementation detail of
    those things.
  - If you're building a library of hooks or a reusable hook, then that is a
    good reason to test the hooks

- Put the hook into a test component that resembles the way that people would
  nromally use the real component with the custom hook and test the compohnent
  to test the hook indirectly.
  - test the test component as a user would use it which causes the custom hook
    to run and expect things that the user would expect after interacting with
    the component.

-- Test Component for Difficult complex Hooks --

- If it is difficult to test a component in a way that users typically use your
  hook, you can make a dummy test component and just make assertions on a simple
  result of the hook usage

test('exposts count and increment/decrement functions', () => { let result;
function TestComponent() { result = useCounter() return null; }

render(<TestComponent />) expect(result.count).toBe(0) // wrap in act since
unexpected state updates occur calling the hook: // it tells I'm going to do
something to trigger an update and once it is finished, flush all the side
effects/useEffect callbacks etc. so that the component is stable act(() =>
result.increment()) expect(result.count).toBe(1) })

**NOTE ON ACT**

- Get used to wrapping hook function calls in act() in tests if the hook
  function updates state - this is normal and expected.

-- use react-hooks library --

- use renderHook helper to render custom hooks inside a test component
  automatically (since hooks cannot be called directly in tests, but need to be
  rendered in a react component)

```javascript
import {renderHook, act} from '@testing-library/react-hooks'

test('exposts count and increment/decrement functions', () => {
  // pass in the hook you want to test (under hood this creates a test component similar to above)

  // renderHook returns utilities you can destructure
  const { result, rerender } = renderHook(useCounter, {initialProps: {step: 3}});
  // use .current to solve referential equality problem where result is assigned to new obj on rerendering under the hood. expect(result.current..count).toBe(0)

  act(() => result.increment()) expect(result.current.count).toBe(3)

  // rerender hook with different props for testing further rerender({step: 2})
  act(() => result.decrement()) expect(result.current.count).toBe(1)
})
```

NOTE: other examples show using renderHook as calling the hook inside a
function:

`const {result} = renderHook(() => useAsync(initialState))`

## TESTING COMPOUND COMPONENTS (with children):

See Modal Compound Components video under Testing Hooks section in Epic React
final project

- copy the component as it is used in the app to the test to render it
- make the children and props generic
- operate on the component(s) as a user would to test it (i.e. opening and
  closing a modal and verifying the content/children are in the document or
  not).

## TROUBLESHOOTING:

- If you get error about 'toHaveAttribute' or the like is not a function, you
  may need to install jestdom to get these helpers:

  - go to setupTests.js
  - import '@testing-library/jest-dom' (create-react-app may do this for you, so
    this is for manual setup of jest)
