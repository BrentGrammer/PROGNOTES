# Practical React Query

- From https://tkdodo.eu/blog/practical-react-query
- November 2020 info

## Defaults

- React Query does not invoke the queryFn on every re-render, even with the default staleTime of zero. Your app can re-render for various reasons at any time so this is prevented.

- If you see a refetch that you are not expecting, it is likely because you just focused the window and React Query is doing a refetchOnWindowFocus, which is a great feature for production: If the user goes to a different browser tab, and then comes back to your app, a background refetch will be triggered automatically, and data on the screen will be updated if something has changed on the server in the meantime. All of this happens without a loading spinner being shown, and your component will not re-render if the data is the same as you currently have in the cache.

### Refetches during Development:

- During development, this will probably be triggered more frequently, especially because focusing between the Browser DevTools and your app will also cause a fetch, so be aware of that.
  - as of v5, the visibilitychange event is used exclusively. This means you'll get fewer unwanted re-fetches in development mode
- Use React Query DevTools: I have found that it helps to throttle your network connection in the browser DevTools if you want to better recognize background refetches, since dev-servers are usually pretty fast.

### Refetching stale data default

- If the query is stale (which per default is: instantly), you will still get data from the cache, but a background refetch can happen under certain conditions.

#### gcTime

- Note on gcTime (previously known as cacheTime before v5): It's the duration until inactive queries will be removed from the cache. This defaults to 5 minutes. Queries transition to the inactive state as soon as there are no observers registered, so when all components which use that query have unmounted.
- Most of the time, if you want to change one of these settings, it's the staleTime that needs adjusting. I have rarely ever needed to tamper with the gcTime. See [example](https://tanstack.com/query/latest/docs/react/guides/caching#basic-example)

## Refetching data

- Treat the query key like a dependency array.
  - We would have some local state to store that filtering, and as soon as the user changes their selection, we would update that local state, and React Query will automatically trigger the refetch for us, because the query key changes.

```javascript
type State = "all" | "open" | "done";
export const useTodosQuery = (state: State) =>
  useQuery({
    queryKey: ["todos", state], // query key changes on state change/filter selection and refetches
    queryFn: () => fetchTodos(state), // fetch todos based on filter 'all' or 'done' etc.
  });
```

### Do not put fetched data in local state

- If you get data from useQuery, try not to put that data into local state. The main reason is that you implicitly opt out of all background updates that React Query does for you, because the state "copy" will not update with it.

### Use of enabled option on queries

- Turn queries on and off
  We have one query that polls data regularly thanks to refetchInterval, but we can temporarily pause it if a Modal is open to avoid updates in the back of the screen.
- Wait for user input
  Have some filter criteria in the query key, but disable it for as long as the user has not applied their filters.

### Don't mess with queryCache for state management

- If you tamper with the queryCache (queryClient.setQueryData), it should only be for optimistic updates or for writing data that you receive from the backend after a mutation. Remember that every background refetch might override that data

## Testing

- from [article](https://tkdodo.eu/blog/testing-react-query)
- prefer to give each test its own QueryClientProvider and create a new QueryClient for each test. That way, tests are completely isolated from each other.

### Example tests:

- [Repo with small app and basic test cases](https://github.com/TkDodo/testing-react-query/tree/main/src/tests)
- Examples from test setup in [React Query source code](https://github.com/TanStack/query/blob/ead2e5dd5237f3d004b66316b5f36af718286d2d/src/react/tests/utils.tsx#L6-L17)

### Timeouts when testing error queries:

- A common gotcha: The library defaults to three retries with exponential backoff, which means that your tests are likely to timeout if you want to test an erroneous query.
- Use the query client to turn retries off in the provider
  - this will only work if your actual useQuery has no explicit retries set.
- Gives you the option to turn it off for all queries in tests in the test provider

```javascript
const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        // ✅ turns retries off
        retry: false,
      },
    },
  });

  return ({ children }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
};

test("my first test", async () => {
  const { result } = renderHook(() => useCustomHook(), {
    wrapper: createWrapper(),
  });
});
```

### Set query specific settings using the queryClient

```javascript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 2,
    },
  },
});

// ✅ use setQueryDefaults on queryClient: only todos will retry 5 times
queryClient.setQueryDefaults(["todos"], { retry: 5 });

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Example />
    </QueryClientProvider>
  );
}

// Do not do this:
// function Example() {
//   // 🚨 you cannot override this setting for tests!
//   const queryInfo = useQuery({
//     queryKey: ['todos'],
//     queryFn: fetchTodos,
//     retry: 5, // don't set explicitly on the query in the component
//   })
// }
```

### Await Results

- React Query is async by nature, when running the hook, you won't immediately get a result. It usually will be in loading state and without data to check.

```javascript
import { waitFor, renderHook } from "@testing-library/react";

test("my first test", async () => {
  const { result } = renderHook(() => useCustomHook(), {
    wrapper: createWrapper(),
  });

  // await the result from the query in tests
  // ✅ return a Promise via expect to waitFor
  await waitFor(() => expect(result.current.isSuccess).toBe(true));

  expect(result.current.data).toBeDefined();
});
```
