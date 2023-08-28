# Mocking Http requests

- Use Mock Service Worker package
- [Basic Example of using msw](https://testing-library.com/docs/react-testing-library/example-intro/)

## Testing bad requests:

- Trick by Kent C Dodds using catch if you know what error is coming back:

```javascript
// using msw
server.use(rest.get(endpoint, async (req,res,ctx) => {
    return res(ctx.status(401), ctx.json(mockReturn))
}))

// add a catch to the client call and return the error as a resolved promise
// result is now the error
// Note: this turns a rejected promise into a resolved promise (watch out for this if testing for rejection)
const result await client(endpoint).catch(error => error)

// Kent uses toMatchInlineSnapshot() instead of toBe() here - why?
expect(result.message).toBe('my error message expected')
```

- Testing promise rejection by the client on a request error:

```javascript
// using msw
server.use(
  rest.get(endpoint, async (req, res, ctx) => {
    return res(ctx.status(400), ctx.json(mockError))
  }),
)

// don't use .catch since the res ctx above returns json and we want to confirm (in fetch in example) that the promise rejects when a 400 is returned
// when using the .catch in prev example the promise itself did not actually reject.
// the .catch with the await was resolving the promise with the error returned in the catch (const error was a resolved promise)
// XXX const result = await client(endpoint).catch(error => error)

// await the expect and use .rejects
// pass the promise that client returns to the awaited expect
// we expect the promise to reject (in the example the code uses fetch and returns a rejected promise if the request fails)
await expect(client(endpoint)).rejects.toEqual('error message')

//**NOTE*** Make sure to either await the expect or return expect if using .rejects or .resolves because that assertion does not run until the promise rejects or resolves
```
