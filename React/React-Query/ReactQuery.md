# React Query

- [An Async State Manager](https://portal.gitnation.org/contents/thinking-in-react-query) (independent of how to fetch data)
- [crash course](https://www.youtube.com/watch?v=r8Dg0KVnfMA&t=1353s)

### Benefits

- Automatically caches data
  - Normally you would fetch in useEffect every time the component mounts unless you have caching impl. React-Query will cache fetched data and refetch from the cache.
- Automatically re-fetches stale data to update the cache
  - For example moving away from and going back to the component will trigger a refetch of the stale data automatically
  - Also moving away from a tab in the browser and back to the app tab will trigger a refetch. Refetching occurs including when the tab is unfocused/focused.
- Automatic exponential backoff and retries for failed requests.

## Best Practices

- try to keep the minimal amount of state you need in order to derive other data from the query cache.
  - for ex, just store IDs and then get the record from the query cache
  - This is recommended because it prevents you from having two versions of a piece of data (one in local state and one in the query cache) - that could possibly get out of sync.
- Keep side effects in event handlers (not in useEffect for ex.) - this helps with double calls with Strict mode in react 18 and is recommended best practices.

  - When the user performs an action, that's when the work is done - you don't do it afterwards (like in a useEffect etc.)

### Anti-Patterns:

- Do not set local state with the result of a query in the `onSuccess` callback - React Query is the keeper of this state and should be the source of truth by referencing the query key for that state.
- Also don't use a useEffect to dispatch an action with the query result to redux etc. React-Query is the state manager for this data so that is unnecessary.

## When does React Query refetch queries?

- Based on Triggers:
  - on window focus
  - on component mount
  - when network is regained
  - when query key changes
- Async state needs to be unpdated at some point in time and these are the events that trigger an update.
- See below - this does not happen all of the time for all queries:

### StaleTime

- NOTE: React Query does not do this for all queries, only for queries that are STALE.
- If data is considered fresh, it will be pulled from the cache without a refetch, otherwise for stale data we get cached data and then a refetch.
- **StaleTime defaults to 0** - by default React Query considers everything stale and refetches all the time.
  - You need to decide what the staleTime is.
  - Example: config settings that are stable that do not need many changes (only when server restarts), use `staleTime: Infinity`
    - or if you have a multi-user updating system that updates happen at the same time, then staleTime of 0 might be good.

#### Recommended approach to staleTime:

- Set a default globally and override it when needed.

```javascript
// set global default:
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 2 * 60 * 1000, // 2 min.
    },
  },
});

// in query to override:
useQuery({
  queryKey,
  queryFn,
  staleTime: 5 * 60 * 1000, // 5 min.
});
```

## setup

- `npm i @tanstack/react-query`
- can install dev tools for debugging: `npm i --dev @tanstack/react-query-devtools`
- linting: yarn add -D @tanstack/eslint-plugin-query
- import client and provider into entry point:

```javascript
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import App from "./App.tsx";
import "./index.css";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: Infinity, // how long do you want to cache things in millisecs, Infinity means for as long as a user is on a session
      cacheTime: Infinity, // IOW, once something is fetched, do not refetch it.
      // refetchOnWindowFocuse: false // defaults to true - can turn this off if you don't want to refetch in background when window left and returned to.
    },
  },
});

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
    {/* <BrowserRouter> would go here if using react router*/}
      <App />
      <ReactQueryDevtools />
    </QueryClientProvider>
  </React.StrictMode>
);
```

### Note on staleTime and cacheTime:

StaleTime: The duration until a query transitions from fresh to stale. As long as the query is fresh, data will always be read from the cache only - no network request will happen! If the query is stale (which per default is: instantly), you will still get data from the cache, but a background refetch can happen under certain conditions.

CacheTime: The duration until inactive queries will be removed from the cache. This defaults to 5 minutes. Queries transition to the inactive state as soon as there are no observers registered, so when all components which use that query have unmounted

### Main components

#### Queries: fetches data.

- needs a queryKey (array of values, one or more strings)
- needs a queryFn: what runs to query the data - a function that returns a promise
- Note: useQuery will show cached data first and then automatically re-fetch data in the background when the component re-renders to get most up to date data (unless caching settings have been changed to override that behavior)
  - `query.fetchStatus === 'fetching'`
  - `query.status === 'loading'` // will be fetching and loading the first time. will be "idle"/"success|error" after it's finished.
    - on refetching after getting from cache, will update fetchStatus to "fetching" again, while status continues to be "success" (and updates after the refetch if necessary)

```javascript
const myQuery = useQuery({
  queryKey: ["your-key"],
  queryFn: (obj) => {
    // you have access to context obj with a queryKey with the automatically passed in argument: obj.queryKey
    // fetch resource, return a promise, not the resolved data! (don't use await)
  },
  // refetchInterval: 1000 // optionally set the query to auto re-fetch at an interval in milliseconds
});

// You can use the .data prop to access data fetched (and automatically updated in cache)
{
  myQuery.data.map((record) => <div key={record.id}>{record}</div>);
}
```

## Query keys

- need to be unique
- can think of them as an array of strings based on path/namespace:
  - `posts/id` = ["posts",post.id]
  - `posts` = ["posts"]
  - `posts/id/comments` = ["posts",post.id,"comments"]

### Use Query keys like dependencies to sync state

```javascript
function useIssues() {
  // using global state to store a set of filters selected by user (also could use a url param)
  const filters = userStore((state) => state.filters); // manager returns new object on changes

  return useQuery({
    queryKey: ["issues", filters], // use the data in the key so updates will trigger this query
    queryFn: () => {
      const url = "...";
      return axios.get(url).then((res) => res.data);
    },
  });
}
```

## Mutations

- Mutations: used to update data

  - Requires a `mutationFn`

  ```javascript
  const queryClient = useQueryClient();

  const { isLoading, mutate } = useMutation({
    mutationFn: (someData) => {
      // return your normal fetch call, can use someData passed in
    },
    // alternatively you can use onSettled
    onSuccess: () => {
      // you could update local state to show an alert or success message here (if using onSuccess).
      queryClient.invalidateQueries(["querykey"], { exact: true }),
    },
    // onError has access to the error thrown by the request
    onError: (err) => alert(err.message)
  });
  // now you can call mutate in a click handler:
  <button onClick={() => mutate("some data")} disabled={isLoading}>
    Submit
  </button>;
  ```

##### lifecycle hooks/callbacks:

- `onSuccess`
- `onError`
- `onSettled`
- `onMutate`: good for doing something before mutation fn runs or setting data in context.

**NOTE: useMutation does not retry on failures like useQuery**

- you can pass in an optional `retry` setting to override this but it is not recommended.

- write a query in it's own file:

```javascript
// fetchpet.js
const fetchPet = async ({ queryKey }) => {
  const id = queryKey[1]; // array, the second element is the id

  const apiRes = await fetch(`http://pets-v22.dev-apis.com/pets?id=${id}`);

  if (!apiRes.ok) {
    throw new Error("details api fetch not okay.");
  }

  return apiRes.json(); // returns a promise - react-query expects you to return a promise
  // you technically do not have to await and can skip the extra tick...
};

export default fetchPet;
```

### Queries:

- You might only want to run a query if you have data from another query that you need to complete

```javascript
const postQuery = useQuery({
  queryKey: ["posts", id], // if data is read from this key elsewhere in useQuery then it will be read from the same cache
  queryFn: () => getPost(id), // queryfn needs to return a promise
});

// Disabling/enabling queries if they depend on others:
const userQuery = useQuery({
  queryKey: ["users", postQuery?.data?.userId],
  enabled: postQuery?.data?.userId != null, // boolean - whether to run the query - this will not run until the userId has been fetched above
  queryFn: () => getUser(postQuery.data.userId),
});
```

### Request states

```javascript
const {
  isLoading,
  data: posts,
  error,
} = useQuery({
  queryKey: ["posts", id], // if data is read from this key elsewhere in useQuery then it will be read from the same cache
  queryFn: () => getPost(id), // queryfn needs to return a promise
});

if (isLoading) return <Loading />;
```

### Invalidating Cache

- When you useMutation() to make an update to the backend api, you need to tell React-Query to invalidate the cache for affected resources so it will fetch the latest data.
- Note: the query key passed in will match any other keys that start with that string (i.e. ["posts", "id]). You need to pass in the { exact: true } option.
- use `queryCache.invalidateQueries(['cache-id'], { exact: true });` in the `onSettled` callback
  - you could use the `onSuccess` callback if you only want to invalidate when the query mutation succeeds. onSettled will run everytime including on failures.

```javascript
function usePostWidget() {
  const queryClient = useQueryClient(); // recommended to use the hook instead of importing it - makes for easier testing and decoupling. the hook will use the client that is passed into the nearest provider (which you can inject for tests)
  return useMutation(
    async function (widget) {
      // make post request to update backend here
    },
    {
      onSettled: () => {
        queryClient.invalidateQueries(["cache-id"]); // use the queryKey from the useQuery for fetching the resource.
      },
    }
  );
}
```

### Error handling

```javascript
const createPostMutation = useMutation({
  // what is passed in is what is when you call mutate() (see below)
  mutationFn: ({ title, body }) => createPost({ title, body }), // just the function to call your api/backend
});

function handleSubmit(e) {
  e.preventDefault();
  createPostMutation.mutate({
    title,
    body: new FormData(e.target), // passed as args to mutateFn
  });
}

return (
  <div>
    {createPostMutation.isError && JSON.stringify(createPostMutation.error)}
    <form onSubmit={handleSubmit}>
      <button disabled={createPostMutation.isLoading}>Submit</button>
    </form>
  </div>
);
```

## Extract Queries into Custom Hook

- best practice to extract query functionality into hooks for larger applications.
- You might want to consider making the query hooks close to where they are used unless they are re-usable across multiple features (in that case they should go in a hooks folder)

Example for deleting:

```javascript
// useDelete[Resource].ts
export function useDeleteCabin() {
  const queryClient = useQueryClient();

  const { isLoading: isDeleting, mutate: deleteCabin } = useMutation({
    mutationFn: apiDeleteCabin, // your api call
    onSuccess: () => {
      // show toast/UI feedback etc.
      queryClient.invalidateQueries({
        queryKey: ["cabins"],
      });
    },
    onError: (err) => //show UI error with err.message
  });

  return {isDeleting, deleteCabin};
}

// In consumer component:

const { isDeleting, deleteCabin } = useDeleteCabin();

<button onClick={() => deteleCabin(id)} disabled={isDeleting}>
  Delete
</button>
```

### Passing callback procuedures to React Query custom hooks

- If we need to call something onSuccess or in the lifecycle callbacks, but have our query logic in a custom hook, we can pass an additional argument to the mutation function (`mutate()` that is returned from useMutation())
- [video](https://www.udemy.com/course/the-ultimate-react-course/learn/lecture/38038074#content)

```javascript
export function useCreateEditCabin() {
  const queryClient = useQueryClient();

  const { mutate: createCabin, isLoading: isCreating } = useMutation({
    mutationFn: ({ newCabin, id }) => createEditCabin(newCabin, id),
    onSuccess: () => {
      toast.success("new cabin created");
      queryClient.invalidateQueries({
        queryKey: ["cabins"],
      });
      // here we need to reset the form
    },
    onError: (err) => toast.error(err.message),
  });

  return { isCreating, createCabin };
}

// in form component, can pass onSuccess in options arg when calling the mutationfn returned from the custom hook:

const { isCreating, createCabin } = useCreateEditCabin();

const onSubmit = () => {
  //...
  createCabin(newCabin, {
    // NOTE: if needed, you have access to the data returned from the api call etc. that the mutation fn returns
    onSuccess: (dataReturnedFromMutationFn) => resetForm(),
  });
};
```

### Fetching data hook:

```javascript
export function useCabins() {
  const {
    isLoading,
    data: cabins,
    error,
  } = useQuery({
    queryKey: ["cabins"],
    queryFn: getCabins,
  });

  return { isLoading, error, cabins };
}

// in component where you're fetching the data:
const { isLoading, cabins } = useCabins();

// You can also do the same as above in any other components where you need that data. it will not be refetched if it is already in the cache and has not been invalidated.
```

- Example fetching some settings for an edit settings form:

```javascript
export function useSetting() {
  const {
    isLoading,
    error,
    data: settings,
  } = useQuery({
    queryKey: ["settings"],
    queryFn: getSettings,
  });

  return { isLoading, errror, settings };
}

// in component with update settings form:
// default the settings data fetched to a default value since it will be undefined while fetching if needed
const { isLoading, settings = {} } = useSettings();

if (isLoading) return <Loading />;

// use defaultValue for the settings values in the form inputs
```

### Fetching data on click:

- use the reFetch from useQuery when button is clicked
- set enabled = false to stop it from fetching immediately

```javascript
const Comments = ({ ticker }) => {
  const {
    data: comments,
    refetch,
    isFetching,
    isError,
  } = useQuery({
    queryKey: ["comments", ticker],
    queryFn: () => fetchComments(ticker),
    enabled: false,
  });

  return (
    <div>
      {!isFetching && <button onClick={() => refetch()}>Get comments</button>}

      {isFetching ? <Loading /> : <CommentsList comments={comments || []} />}

      {isError && <ErrorMessage message="Error retreiving comments." />}
    </div>
  );
};
```

### Pagination

- use keepPreviousdData from useQuery to prevent loading when changing pages

```javascript
const [page, setPage] = useState(1);

const { status, error, data, isPreviousData } = useQuery({
  queryKey: ["posts", {page}],
  keepPreviousData: true, // add this
  queryFn: () => getPostsPaginated(page)
})

// check for next or previous pages first
<button onClick={setPage(page - 1)}>Previous</button>
<button onClick={setPage(page + 1)}>Next</button>
```

### Inifinite Scrolling (v5)

- use hook from react-query
- make requests to your endpoint as `{endpoint}/resource?page={page}`
- Make load more button that will make requests on click as long as there is more pages or limit is hit.
- flow:
  - getNextPageParam is called and gets a page number for next page
  - passes that page number into queryFn which you use to make the call to get the next page of data.
  - use fetchNextPage from the useInfiniteQuery hook in the onclick handler when you want to get more data

```javascript
import { useInfiniteQuery } from "@tanstack/react-query";

const Comments = ({ ticker }) => {
  const {
    fetchNextPage,
    hasNextPage, // if getNextPageParam returns undefined, there is no next page - this is set to false then.
    isFetchingNextPage, // builtin loading state to determine if loading new data.
    error: fetchCommentsError,
    data,
  } = useInfiniteQuery({
    enabled: startFetching,
    queryKey: ["comments", "infinite", ticker],
    getNextPageParam: (lastPage: FetchCommentsResponse) => lastPage.nextPage, // response has nextPage prop on it. this is passed into pageParam in the queryFn. will be null/empty when no next page
    initialPageParam: 1,
    queryFn: ({ pageParam }) => fetchComments(ticker, pageParam), // set pageparam to 1 by default, not 0
  });

  const comments = data?.pages.flatMap((data) => data.comments);

  return (
    <div>
      {comments?.map((comment, idx) => (
        <p key={`comment-${idx}`}>{comment}</p>
      ))}

      {!comments || comments.length === 0 || hasNextPage ? (
        <button onClick={() => fetchNextPage()} disabled={isFetchingNextPage}>
          {isFetchingNextPage ? "Loading.." : "Load Comments"}
        </button>
      ) : null}

      {fetchCommentsError && (
        <ErrorMessage message="Error retreiving comments." />
      )}
    </div>
  );
};

export default Comments;
```

### Debouncing mutation

- Can use the [debounce-fn](https://www.npmjs.com/package/debounce-fn) package

```javascript
import debounceFn from "debounce-fn";

const Notes = () => {
  const [mutate] = useMutation((updates) => updateNotes, {
    onSettled: () => queryCache.invalidateQueries("list-items"),
  });

  // Wait 300 millisecs after the user stops typing
  const debouncedMutate = React.useCallback(
    debounceFn(mutate, { wait: 300 }),
    []
  );

  function onUserTypingNotes(e) {
    debouncedMutate({ id: listItem.id, notes: e.target.value });
  }

  return (
    //...
  )
};
```

### Clearing the Cache when a user logs out

- use the client to clear the cache.
- alternative you can use the queryCache.clear() method when the user logs out (import {QueryCache} from '@tanstack/react-query')

```javascript
const client = useQueryClient();

const logout = () => {
  auth.logout();
  client.clear();
  clearReduxState();
};
```

### Clear cache for a specific query:

```javascript
const queryClient = useQueryClient();
queryClient.resetQueries({ queryKey, exact: true }); // use the same query key you used for the query
```

## Gotchas

- Make sure that you do not load different data into the same cache.

```javascript
const { data: myFetchedData } = useQuery({
  queryKey: "list-items", // <-- key and function should match wherever used in app - this is why it's a good idea to extract queries into hooks
  queryFn: () => fetchListItems, // make sure the key and the fetch function are the same everywhere the query is used - otherwise you will be making a new request (not cached) and adding new data to the same cache (very confusing)
});
```
