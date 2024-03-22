# TIP System design

### CDN

- pull, tell CDN where server files are, request asks, CDN checks cache if no then go to server and get the files and store them in cache. \*\*Usually preferred. (ex. AWS Cloudfront)
- push - push all your files directly to the CDN. This comes with increase in cost since you're charged by data stored - makes for fast first request at the cost of higher charges.

For websites, usually put images, static files, static html , js or css files behind a CDN.

### Caching

- Software on another server. Memcache, Redis, Cassandra
- key value pairs.

Write-through caching persists data to disk for persistent storage- comes with more overhead.

### Load Balancing

- Round Robin - just push each request one per each server registered.
- Least connection - push req to server with least load.

## Database

### SQL

Sample join statement:

```sql
Select * from Dog d,
Pet p WHERE
d.dogID = p.dogID
AND p.petID = 1
ORDER BY d.created;
```

- (Get a dog whose dog id matches one in the pets table and pet record has a person id of 1, then order by when dog was created).
  This is a join between a dog and pet tables on the dog id.
- Note: This is a slow query, requires scanning through all pets table to find dog id, then you have to scan through entire dog table to find entry for dog id, then if there is a bunch of dogs the person owns that requires sorting.

- Use simple queries in practice, complex ones are slow.

#### Optimizing the query:

Optimizing above table could be improved by making a binary search tree based on the PID on Pet table, that would make the operation logarithmic time. Same for dog table on the DID dog id.
You could create indexes on these keys.

### NoSQL

- more of a key value store. More difficult to do range queries in NoSQL databases like you can in Relational DBs. Ex: Get all dogs registered in the last 30 days

- Sharding is usually at quite a granular level, so indexing can still be useful. For instance, you can shard based on geography, and then find all users ages 18-25 using an indexed range query.

- Note: Adding indexing will over time slow down inserts and deletes, due to the overhead of maintaining it.
  having only append inserts is O(1) time, adding a B-tree index increases the cost of writes to O(log(n)) time for every index you have.

- Note: don't store binaries in database - it bogs it down. For ex. just store a filename string which you use to find it in a distributed file system.

### REDUNDANCY AND REPLICATION

- Master-Slave Replication - good for low writes and high reads applications. Alot of internet apps use this. Blogs, Facebook, News websites (occasional article publish, more reads).
  If editing records, you want most up to date data so you read from the Master, not slaves.

- Multiple Read Databases read from a master Writeable database and copy data into them.

- Can scale the write master db using Master-Master replication. i.e. multiple masters that replicate from one another.
- Cons are synchronization knowing where most up to date data is. This is very complex and the ideal solution.
