# Hashing

- Function that returns a number

### Uniformity in Hashing

- Builtin methods come with gaurantees that you need when hashing.
- The hashing function must have **uniformity**
  - Ex: hash result would get evenly distributed data values around servers etc.
- Some Premade industry grade algorithms with uniformity:
  - MD5
  - SHA1
  - BCrypt

## When to use Hashing

### Caching problems

- If following a Round Robin load balancing strategy, when using a cache for computationally expensive operations, if the same client asks for the request again, there is a chance the RR load balancing will send them to a different server that does not have the cached response.
  - We can use Hashing to solve this.
  - Hash the requests that come into the load balancer
  - Based on the hash bucket the requests according to the position of the servers.
    - Can bucket the requests in the servers by performing some business logic.

### Example of hashing for cache handling

- see [video](https://www.algoexpert.io/systems/fundamentals/hashing) at timestamp 6:50
- Simple ex is to hash the client's names.
  - Ex: C1 => 11, C2 => 12, C3 => 13, C4 => 14
  - You could also hash the client's IP address, the http request, the client's username, etc.
- Simplest strategy is to modulo (%) the hash of the client name by the number of the servers you have.
  - 11 % 4 = 3, 12 => 0, 13 => 1, 14 => 2
  - This gives us the number of the server that each client should be associated with consistently (0-based)
- This maximizes cache hits and reduces cache misses.

## Hashing in Distributed Systems

- If a server dies or you add a new server to your system, the hashing logic needs to be updated to handle these changes.
- The main problem is that you lose all the mappings with the new hashing logic to accomodate the new number of servers.
- We need to use more complex hashing strategies to handle this situation so that we don't lost client/server associations to keep getting cache hits. Consistent hashing and Rendezvous hashing are needed.
  - These strategies maintain most of the mappings of client to server when changes to the system are made.

### Consistent Hashing

- Maintains some consistency in mappings between clients and servers, for ex.
- See [video](https://www.algoexpert.io/systems/fundamentals/hashing) at timestamp 16:00 for visual example and demo
- Arrange servers conceptually in a circle. Each point on the circle represents back to back numbers all the way around. Servers will fall on one of these points based on the result of a hashing function.
- Do the same with the clients, put them through a hashing function and use the result to place them at points on the circle.
- To determine where clients requests are routed to in order to maintain cache hits using hashing, start form the client on the circle and move clockwise (or counter clockwise, just stay consistent) - the first server encountered is the server that the load balancer will reroute requests to.
- This solves the problem of a server dying and having to redo hashing logic, because with this setup, the client going to the dead server is redirected to the next server on the circle.
- When a new server is added, again no redoing of the mod or hashing is necessary - the clients will simply go to the next server on the circle, whatever that is, even if it is new/inserted or the same one before.
  - Note this does mean that the cache at the original server is lost for that client, but changes in the hashing/redirect logic are not needed. Most of the previous mappings are preserved.

#### Directing more traffic to a stronger server

- If you want more traffic to a more capable server compared to others in a distributed system, you can pass that server through more hashing functions which will give server A more locations on the circle.

### Rendezvous Hashing

- see [video](https://www.algoexpert.io/systems/fundamentals/hashing) at timestamp 26:35
- For each client, rank the servers (using some formula or logic) for that client, then choose the highest ranking server.
- If servers are removed, and they are mapped to a client, then the client will just take the second highest ranked server for it.

**These strategies will optimize for keeping latency reduced when distributed systems scale by retaining client to server mappings for maximizing cache hits.**
