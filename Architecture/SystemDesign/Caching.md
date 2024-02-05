# Caching

- store items that do not change frequently in cache (ex., Redis or Memcache)
- Prefer caching static or immutable data
- Caching mutable data is more tricky and should be avoided if not necessary - dealing with stale data and keeping data in more than one place in sync

### Types of Caching

- Write Group caching: Store writes in a cache (i.e. on the server) and write to the database.
  - advantage: db and cache stay in sync, disadvantage: still writing to the db
- Write Back Cache: store writes in the cache in the server only, and immediately go back to client. System asynchronously updates the data in the database
  - disadvantage: cache is out of sync with database. Risk is losing something in the cache before the database is updated (this requires mitigation)

### Stale caches

- If a cache has not been updated recently on a server (for example in a group of servers that require time to get in sync), a client could get stale outdated data.
- One way to mitigate this is to move the cache out of the server instances and have a single source of truth for the cache, i.e. a Redis server that all servers pull from.

### Cache Eviction Policies

- LRU - Least Recently Used policy, get rid of the least recently (oldest) used pieces in the cache.
- LFU - Least Frequently Used policy, the least frequently used data is evicted
- FIFO or LIFO approach, get rid of first in/last in data

### Caching problems

- If following a Round Robin load balancing strategy, when using a cache for computationally expensive operations, if the same client asks for the request again, there is a chance the RR load balancing will send them to a different server that does not have the cached response.
  - We can use Hashing to solve this.

# CDNs (Content Delivery Network)

- An origin server (the server with the original data) holds the single source of truth and data.
- CDNs bring STATIC content closer to the end user.
  - can have hundreds or thousands of CDN servers all over the world
- **CDNs can only hold STATIC content** that is not changing (app code cannot run on the CDN servers)
  - JavaScript can be hosted on CDNs (it does not change and can be the same for all users around the world)
  - Videos and Images can be stored - they don't change themselves
  -
- Edge Servers can potentially run code and host dynamic not just static content and be distributed and closer to servers (different from CDNs and newer)

## Push vs. Pull CDNs

- PUSH CDN: When data is added/updated at the origin server, it pushes the data to all the CDNs immediately. (i.e. if a user uploads their profile pic)
  - applies when clients add or update data
- PULL CDN: Client makes request and CDN acts as a proxy and serves cached data or if a cache miss, it goes to origin server to get it and it gets cached in the CDN server.
  - Applies when clients reads/requests data
  - Lazy loading strategy - the origin server does not push data out to all CDNs - it only provides it when the CDN requests for it, and only to that particular CDN server or limited set of servers.
    - i.e. if clients in different regions have different interests and do not need that data, but other clients in another region do.
  - In order to cache static content (i.e. JavaScript for example), the `Cache-Control` header on the response from the origin server must be set to public!
    - `Cache-Control: public, max-age=86400, stale-while-revalidate=86400`
    - If it is private or not public then that means that response data is not allowed to be cached on any other server besides that which it comes from.
