# Caching

- SSR has an added benefit of caching
- NextJS comes with a builtin data cache (automatic caching that you need to disable manually if you don't want it with fetch, etc.)
  - Ex: whenever `fetch` is used to get data, NextJS will store the result in a cache on the file system.
  - the next time the same url is hit, NextJS will retrieve it from the data cache, not go to the network again
  - If you have data that changes frequently you can disable caching or set a shorter expiration of cache data
- To use caching you can pass a options argument to `fetch` for example

```javascript
const res = await fetch("https://jsonplaceholder.typicode.com/users", {
  cache: "no-store", // disable caching
});

// set cache options
const res = await fetch("https://jsonplaceholder.typicode.com/users", {
  next: { revalidate: 10 }, // runs a background job to get fresh data every 10 seconds
});
```

**NOTE: caching options are only for using fetch API. If you use Axios or another third party lib you will not get these builtin options**

## Static vs. Dynamic Rendering (Server Side rendering types)

- If NextJS sees a compnent that has static data (even if you use fetch as above with caching enabled), it will render it as static html at build time and not re-serve the component if the page is refreshed.
  - if you were to set cache to 'no-store' in the fetch options, then
- To see which pages are static/dynamic you can run `npm run build` and check the output. If there is a circle next to the page it is static, if a lambda icon is next to it, it is rendered dynamically
