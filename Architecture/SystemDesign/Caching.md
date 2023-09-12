# Caching

- store items that do not change frequently in cache (ex., Redis)
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