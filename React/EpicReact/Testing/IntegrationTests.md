# INTEGRATION TESTING

- Should mostly use integration tests for most bang for the buck
- More setup, but worth it and saves work in the long run (also preventing tons
  of unit tests for the same coverage)

### Tradeoffs:

- We can test what is rendered but if you really need to test style changes for
  visual regression testing and things like that you need to use tools like
  percy.io and app load tools(sp?)

---

## Rendering App with all Providers

- you will need to wrap your App with necessary providers to render in tests -
  i.e. Redux store provider etc.

- If you keep your providers in one component that takes children (i.e. your
  <App>), then you can use the wrapper option with render():

```javascript
test('renders all the book information', async () => {
  render(<App />, {wrapper: AppProviders}) // AppProviders is a component with children

  // use screen debug helper to get feedback on what test is rendering
  screen.debug()
}
```

## Wait for Loading to finish on loading app:

- use waitForElementToBeRemoved() from @testing-library/react which takes a
  callback which will be called when a DOM update occurs or at a regular
  interval:

```javascript
test('renders all the book information', async () => {
  render(<App />, {wrapper: AppProviders})
  // get the loading spinner by it's aria-label and wait for it to be removed on app loads
  await waitForElementToBeRemoved(() => screen.getByLabelText(/loading/i)
}
```

## Mocking out AUTH:

- Ideally you want to do the side effect that the auth provider does so the app
  thinks you're logged in
- you could mock out your provider and the method to get tokens etc.
  alternatively

Example buildUser in test/generate module:

```javascript
function buildUser(overrides) {
  return {
    id: faker.random.uuid(),
    username: faker.internet.userName(),
    password: faker.internet.password(),
    ...overrides,
  }
}
```

```javascript
test('renders all the book information', async () => {
  // this is the side effect for ex that occurs when authed:
  window.localStorage.setItem(auth.localStorageKey, 'SOME_FAKE_TOKEN')

  //Mock out HTTP requests to the auth service:
  // safe set fetch before patching:
  const originalFetch = window.fetch
  window.fetch = async(url, config) => {
    // log out url to see what req is failing in the terminal
    console.log(url, config)

    // custom handle what we want - i.e. the success response needed after authing to load app
    if (url.endsWith('/bootstrap')) {
      return { // mock out a success response returned by fetch...
        ok: true,
        json: async () => ({user: {username: 'bob'}, listItems: []})
      }
    }

    // use real fetch by default if we don't handle it here
    return originalFetch(url, config)
  }

  render(<App />, {wrapper: AppProviders})

  await waitForElementToBeRemoved(() => screen.getByLabelText(/loading/i)
}
```

## NAVIGATE TO PAGE AND RENDER INFO:

```javascript
test('renders all the book information', async () => {
  const user = buildUser() // from a test/generate module with our builders
  window.localStorage.setItem(auth.localStorageKey, 'SOME_FAKE_TOKEN')

  const book = buildBook() // from generate module made by us - use faker etc. for model
  // use history pushstate to navigate to details page:
  window.history.pushState({}, 'Test Page', `/book/${book.id}`)

  const originalFetch = window.fetch
  window.fetch = async(url, config) => {
    if (url.endsWith('/bootstrap')) {
      return { // mock out a success response returned by fetch...
        ok: true,
        json: async () => ({...user, token: 'FAKETOKEN', listItems: []})
      }
    } else if (url.endsWith(`/books/${book.id}`)) {
	// intercept request to backend for details page and return data expected
        return {
          ok: true,
  	  json: async () => ({book})
    }
    return originalFetch(url, config)
  }

  render(<App />, {wrapper: AppProviders})

  await waitForElementToBeRemoved(() => screen.getByLabelText(/loading/i)
  screen.debug()


  // make assertions on information expected on the details page:
  // can look for roles with this to use in assertions:
  // screen.getByRole('blah') // shows you list of roles - scroll down to get specific ones in the terminal

  expect(screen.getByRole('heading', {name: book.title})).toBeInTheDocument()

  // check image url is stored in the src for the image of the details page:
  expect(screen.getByRole('img', {name: /book cover/i})).toHaveAttribute(
    'src',
    book.coverImageUrl,
  )

  // check that a button expected is there on the details page:
  expect(screen.getByRole('button', {name: /add to list/i})).toBeInTheDocument()

/// verify that you are not showing the wrong things, i.e. things that load later or after an action etc.:
  // remember to use queryByRole and not getByRole because get throws when element not found
  expect(screen.queryByRole('button', {name: /remove from the list/i})).not.toBeInTheDocument()
}
```

## CLEANUP - Clear state and cache between tests

```javascript
// clear caches (react-query for ex.) and reset logged in user state
afterEach(async () => {
  queryCache.clear() // react-query
  await auth.logout() // clear authstate
}

test('renders all the book information', async () => {
  const user = buildUser()
  window.localStorage.setItem(auth.localStorageKey, 'SOME_FAKE_TOKEN')

  const book = buildBook()
  window.history.pushState({}, 'Test Page', `/book/${book.id}`)

  const originalFetch = window.fetch
  window.fetch = async(url, config) => {
    if (url.endsWith('/bootstrap')) {
      return {
        ok: true,
        json: async () => ({...user, token: 'FAKETOKEN', listItems: []})
      }
    } else if (url.endsWith(`/books/${book.id}`)) {
        return {
          ok: true,
  	  json: async () => ({book})
    }
    return originalFetch(url, config)
  }

  render(<App />, {wrapper: AppProviders})

  await waitForElementToBeRemoved(() => screen.getByLabelText(/loading/i)
  screen.debug()

  expect(screen.getByRole('heading', {name: book.title})).toBeInTheDocument()
  expect(screen.getByRole('img', {name: /book cover/i})).toHaveAttribute(
    'src',
    book.coverImageUrl,
  )

  expect(screen.getByRole('button', {name: /add to list/i})).toBeInTheDocument()
  expect(screen.queryByRole('button', {name: /remove from the list/i})).not.toBeInTheDocument()
}
```

## USE MOCK SERVICE WORKER:

- Move fetch mocking to one place to re-use throughout test suites

Make sure you have MSW configured (check for usage with create-react-app)

// in test-server.js

```javascript
import {setupServer} from 'msw/node' // msw package
import {handlers} from './server-handlers' // we've setup handler wrappers ourselves

// initialize msw server and pass in our handlers - see server-handlers.js in epic react proj
const server = setupServer(...handlers)

export * from 'msw'
export {server}
```

```javascript
// setupTests.js
import '@testing-library/jest-dom'
import {server} from 'test/server'

beforeAll(() => server.listen()) // start server before all tests
afterAll(() => server.close()) // close the server after all tests are finished
afterEach(() => server.resetHandlers()) // resets runtime handlers in between tests to what was 							set in the first place (...handlers)
```

NOTE: if you setup msw like this you can also use it as a mock back end during
local development! see server-handlers.js in the epic react final project
codebase

- Kent Dodds mocks out the databases which you can reuse and interact with in
  the tests.

```javascript
afterEach(async () => {
  queryCache.clear() // react-query
  // clear or reset mocked or test databases as well between tests!
  Promise.all([
    auth.logout(),
    usersDB.reset(), // resets are custom from the epic react proj
    booksDB.reset(),
    listItemsDB.reset()
  ])

}

test('renders all the book information', async () => {
  const user = buildUser()
  // use faked out databases (server-handlers.js) to make a real user
  await usersDB.create(user)
  const authUser = await usersDB.authenticate(user)

  window.localStorage.setItem(auth.localStorageKey, authUser.token)
  // use a mocked out database
  const book = await booksDB.create(buildBook())
  window.history.pushState({}, 'Test Page', `/book/${book.id}`)

  render(<App />, {wrapper: AppProviders})

  /** **NOTE:
	MSW adds a little tick to the event loop which could cause more loading elements or other things to remain on the screen.
	Make sure to check for removal of all of those items to proceed when the tick has moved on to the next and loading is finished
  */
  await waitForElementToBeRemoved(() => [
    ...screen.queryAllByLabelText(/loading/i), // returns arr so spread it
    ...screen.queryAllByText(/loading/i),
  ])
  screen.debug()

  expect(screen.getByRole('heading', {name: book.title})).toBeInTheDocument()
  expect(screen.getByRole('img', {name: /book cover/i})).toHaveAttribute(
    'src',
    book.coverImageUrl,
  )

  expect(screen.getByRole('button', {name: /add to list/i})).toBeInTheDocument()
  expect(screen.queryByRole('button', {name: /remove from the list/i})).not.toBeInTheDocument()
}
```

## Adding a List Item to a List Test:

```javascript
// utility function to reuse - implicit return and returns the promise
const waitForLoadingToFinish = () =>
  waitForElementToBeRemoved(() => [
    ...screen.queryAllByLabelText(/loading/i), // returns arr so spread it
    ...screen.queryAllByText(/loading/i),
  ])
// utility for logging in a test user
async function loginAsUser(userProperties) {
  const user = buildUser(userProperties)
  await usersDB.create(user)
  const authUser = await usersDB.authenticate(user)
  window.localStorage.setItem(auth.localStorageKey, authUser.token)
  return authUser
}

test('can create a list item for the book', async () => {
  await loginAsUser()

  const book = await booksDB.create(buildBook())
  const route = `/book/${book.id}`
  window.history.pushState({}, 'Test Page', route)

  render(<App />, {wrapper: AppProviders})

  await waitForLoadingToFinish()

  const addToListButton = screen.getByRole('button', {name: /add to list/i})
  userEvent.click(addToListButton)
  // check disable after clicking while loading
  expect(addToListButton).toBeDisabled()

  //wait for loading to be removed again after click
  await waitForLoadingToFinish()

  // assert what is expected on screen
  expect(
    screen.getByRole('button', {name: /mark as read/i}),
  ).toBeInTheDocument()
  expect(
    screen.getByRole('button', {name: /remove from list/i}),
  ).toBeInTheDocument()
  // expect the notes textarea (use textbox role) to be there
  expect(screen.getByRole('textbox', {name: /notes/i})).toBeInTheDocument()

  // verify date is there, get the start date element - get by label works on aria-label attr
  const startDateNode = screen.getByLabelText(/start date/i)
  // the text is a formatted date version of date.now() ex: `Jun 20` - bring in your date formatter to use
  // normally don't bring in things like this, in this case this is easier than alternative approaches and the formatter utility is well tested
  expect(startDateNode).toHaveTextContent(formatDate(new Date()))

  // verify that certain elements are not there after adding to list
  expect(
    screen.queryByRole('button', {name: /add to list/i}),
  ).not.toBeInTheDocument()
  expect(
    screen.queryByRole('button', {name: /mark as unread/i}),
  ).not.toBeInTheDocument()
  expect(screen.queryByRole('radio', {name: /star/i})).not.toBeInTheDocument()
})
```

### Example Custom Render Utility

- For reuse in tests

```javascript
// change name of render pulled from react testing library
import {render as rtlRender, ...} from '@testing-library/react'
// reusable render - renderoptions are from react testing lib, default a route that could be passed in
const render = async (ui, {route = '/default-app-route', user, ...renderOptions} = {}) => {
  // accept an optional user passed in - allows for rending without a user logged in: i.e. render(<App />, {route, user: null})
  user = typeof user === 'undefined' ? await loginAsUser() : user
  // navigates to a specific route or the default app route (initial route)
  window.history.pushState({}, 'Test Page', route)
  // build in app providers and pass options from react test lib
  const returnValue = { ...rtlRender(ui, {wrapper: AppProviders, ...renderOptions}), user }

  await waitForLoadingToFinish()
  // return the render after loading is finished
  // return all the things that react testing lib gives you and additional data you need to use in the tests
  return returnValue
}
```

Example usage:

```javascript
const book = await booksDB.create(buildBook())
const route = `/book/${book.id}`
await render(<App />, {route})

// waits for loading etc automatically, so you can proceed in your test after calling render
```

## Global Test Utils

- \*\* You could move these utils into a global module to reuse in all tests
  like `src > test > app-test-utils.js`

```javascript
// in global module:

// ... your test utils you want to use in tests, functions etc.

// export everything including react testing library and userEvent etc. so the user can just pull in this module and get everything they might need in the test
export * from '@testing-library/react'
// export your custom render util (defined above) and other utilities like userEvent that you will reuse. Note that we override the render from rtl with our custom render function and export that (because we define render after importing it from react-testing library and alias it to rtlRender in the global utils file - this file)
export {render, userEvent, logInAsUser, waitForLoadingToFinish}
```

## Test Removing a List Item

- NOTE: don't just click on add to list item and then remove from list - that is
  over testing the add to list functionality that is already tested above.
  - instead, create a list item before you even render the app.

```javascript
test('can remove a list item for the book', async () => {
  // we need to login as our own user so that the book is associated with this user for testing
  const user = await loginAsUser()
  const book = await booksDB.create(buildBook())
  const route = `/book/${book.id}`
  // create a list item before rendering to show that we will test removing (skip clicking add to list etc):
  // this mock dev db will have the record which will show on screen when the app list page renders (it's set up in the example to pull from the mock db if in dev or testing mode)
  await listItemsDB.create(buildListItem({owner: user, route, book}))
  // render the app with the route and the user specified we created above
  render(<App />, {route, user})

  const removeFromListButton = screen.getByRole('button', {
    name: /add to list/i,
  })
  userEvent.click(removeFromListButton)
  // check disable after clicking while loading
  expect(removeFromListButton).toBeDisabled()

  await waitForLoadingToFinish()

  // assert what is expected on screen
  // add to list re appears since it's been removed and can now be added
  expect(screen.getByRole('button', {name: /add to list/i})).toBeInTheDocument()

  // remove button should not be there now
  expect(
    screen.queryByRole('button', {name: /remove from list/i}),
  ).not.toBeInTheDocument()
})
```

## Editing a List Item Test

- https://epicreact.dev/modules/build-an-epic-react-app/integration-testing-extra-credit-solution-05-03

- jest.useFakeTimers(): Every time you use this Jest will mock and fake out all
  the timers in the app like setTimeout, setInterval, requestIdleFrame callback
  with something that you can manually advance and move forward synchronously to
  change how long they take (so they take an instant)
  - from
    https://epicreact.dev/modules/build-an-epic-react-app/integration-testing-extra-credit-solution-05-04
  - **Always make sure you reenable the real timers before any other test when
    used**
  ```javascript
  // in setupTests.js
  //... other setup
  beforeEach(() => jest.useRealTimers())
  ```
  - NOTE: Fake Timers are built in to all of the asynchronous utilities we get
    from Testing Library if you use the fake timers, so instead of waiting the
    real intervals it will use the jest fake timers to advance those
    automatically in the test

```javascript
//...
import faker from 'faker'

test('can edit a note', async () => {
  // use fake timers so that the debounce timer is advanced instantly when notes are typed so the test does not take as long:
  jest.useFakeTimers()

  const user = await loginAsUser()
  const book = await booksDB.create(buildBook())
  const route = `/book/${book.id}`
  await listItemsDB.create(buildListItem({owner: user, book}))
  render(<App />, {route, user})

  // generate some text using faker for the notes
  const newNotes = faker.lorem.words()
  const notestTextarea = screen.getByRole('textbox', {name: /notes/i})

  // clear notes text area of what it had before - make value empty, can use .clear() on userEvents
  userEvent.clear(notesTextarea)
  // type in the new notes
  userEvent.type(notesTextarea, newNotes)

  /**
   *   NOTE: There is a debounce when the user types notes so the loading indicator will not show up until after 3 seconds on the screen.  waitForElementToBeRemoved checks for the element to be in the document first and if it does not exist, then it will throw an error.
   *
   *  problem with this is that the promise that comes back from findLabelByText resolves a little bit after the loading shows up and disappears immediately. so when we get to waitForLoadingToFinish() indicator is already gone.
   */
  await screen.findByLabelText(/loading/i)

  // notes editing causes loading
  /**
   * So we originally would want to wait for the loading to be removed, but because the findByLabelText above resolves afterwards, causing this wait to error out since the loading indicator is already gone (happens so fast), we remove this line to wait for loading to be removed.
   */
  // await waitForLoadingToFinish() // this is removed and can't be done due to above

  // Now that we use fakeTimers however, the findByLabelText and loading being removed doesn't happen so fast since fake timers allows for a lot more control over the timing going on, so we can more accurately test behavior and put back wait for element to be removed.
  // note that when using fakeTimers, the testing lib async methods will automatically advance them as needed:
  await waitForLoadingToFinish()

  // optionally add `await waitFor()` if you want to be extra sure this will be in the document
  await waitFor(() => expect(notesTextarea).toHaveValue(newNotes))

  // there is no feedback to check if notes were updated so we check in the database to see the notes were saved there.
  expect(await listItemsDB.read(listItem.id)).toMatchObject({notes: newNotes})
})
```

## Mocking Out Profiler (App wide non critical setup) for Tests

- https://epicreact.dev/modules/build-an-epic-react-app/integration-testing-extra-credit-solution-05-05
- When an app starts up it can have some analytics or other things start which
  are not critical and can be mocked out for tests
- This example mocks out the React Profiler an app uses on app load which runs a
  setInterval and gets and collects client information for analytics and
  performance monitoring.

1. Create a `__mocks__` folder next to the component: i.e. in
   `components/__mocks__/profiler.js` where the component being mocked is in
   `components/profiler.js`

```javascript
// empty component that just takes children
const Profiler = ({children}) => children
// exports everything that the real module exports in components/Profiler.js
export {Profiler}
```

2.  Make sure every test is mocking that. Set it up in the `setupTests.js` file

```javascript
// setupTests.js

//...imports

// This makes sure that the profiler uses the mock and not the real component that uses setInterval and collects and sends performance data etc.
jest.mock('components/profiler')
```

## Component specific renderer (renderBookScreen)

- [Lesson video](https://epicreact.dev/modules/build-an-epic-react-app/integration-testing-extra-credit-solution-06)

```javascript
async function renderBookScreen({user, book, listItem} = {}) {
  // allow for providing inputs to the book screen, if not provided then create them here and pass them to book screen
  if (user === undefined) user = await loginUser()
  if (book === undefined) book = await booksDb.create(buildBook())
  if (listItem === undefined)
    listItem = await listItemDb.create(buildListItem({owner: user, book}))

  const route = `book/${book.id}`

  const utils = await render(<App />, {route, user})

  return {...utils, user, book, listItem}
}
```

## Testing Exception Error Shown for Missing Item

```javascript
test('shows an error message when the book fails to load', async () => {
  // provide item not in the database
  const book = {id: 'BAD_ID'}
  // make the list item shown null - no list item for this book and we pass in the book not in the database
  await renderBookScreen({listItem: null, book})

  // when we render the book screen the route has the book id to find it. Since it does not exist in the database and is a bad id, we will get an error shown in the application.

  // assert that the text content is what you expect and use inline snapshot for error messages (could chage)
  // run the test once to update the snapshot which will auto generate the text expected in the test file
  expect((await screen.findByRole('alert')).textContent).toMatchInlineSnapshot(
    `text is generated after first run`,
  )
})
```

## Handling Console Errors (console.error) Logs in Tests

- [Lesson video](https://epicreact.dev/modules/build-an-epic-react-app/integration-testing-extra-credit-solution-07-02)
- mock the console to do nothing and restore the mock after
  - Note: you don't want it in BeforeAll() because it will silense other errors
    you need to see in the tests
  - You also don't want to put it in a afterAll() since it will explode if a
    test that mocks it is skipped for example.
- You want to **scope the hooks** to a specific test
  - Move the `beforeAll` and `afterAll` into a `describe`` block
  - Note: Kent C. Dodds recommends not using describe blocks normally, but just
    making separate files for tests that can gbe grouped. This has the advantage
    of running the different files in parallel

```javascript
// scope the console error mock to a describe block, so it only runs for tests that need it
describe('console errors', () => {
  beforeAll(() => {
    // whenever console.error is called, it doesn't do anything or display in terminal output
    jest.spyOn(console, 'error').mockImplementation(() => {})
  })

  afterAll(() => {
    // make sure to restore console error after you need it silenced
    console.error.mockResore()
  })

  test('test that needs console errors silent', () => {
    //...my test (i.e. an exception throwing test etc.)
  })
})
```
