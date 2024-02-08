# Designing Data Intensive Applications (by M. Klepmann)

## Goals:

Reliability
Scalability
Maintainability

### Reliability

- fault tolerant (continues to work when things go wrong)
- impossible to reduce faults to zero, it is best to design fault tolerance mechanisms that prevent faults from causing pafailures.

Performance response time- the median is better than the mean. For median sort response times from fastest to slowest and the middle time means half users got response quicker than that and half got response slower than that. (Outliers throw off the mean so you don't get a good idea of how many users experience a delay)

### Scaling

Scaling up (vertical) - more powerful machine
Scale out (horizontal) - more machines you spread the load out over multiple machines.

### DB types

- Document model (nosql) works well if data is one to many relationships (i.e. tree structure) but not for Many to many relationships (requiring joins perhaps)

  - Denormalization is a problem with document databases, duplication of fields.
    Many to many relationships are a problem.
    Highly interconnected data makes for awkward schemas in nosql

Case for document model:
If application data has document like structure (tree of one to many relationships where tree is loaded once)
Schema flexibility
Data locality-if you need large parts of the document at the same time, nosql model is good.

- Relational model:. Good if data is many to many relationships, good for simple cases.

- Graph model: good for complex many to many relationship data. Use vertices(nodes/entities) and edges(relationships/arcs)
  Examples: web graph, social graph (people who know each other), road or rail network.
  You can think of a graph store as consisting of two relational tables, one for vertices and one for edges. The head and tail vertex are stored for each edge; if you want the set of incoming or outgoing edges for a vertex, you can query the edges table by head_vertex or tail_vertex, respectively.
  Head: vertex at which edge starts
  Tail : vertex at which edge ends

```sql
CREATE TABLE vertices (
vertex_id integer PRIMARY KEY,
properties json
);

CREATE TABLE edges (
edge_id integer PRIMARY KEY,
tail_vertex integer
head_vertex integer
label text,
properties json
);
```

Graphs are easily extensible as data evolves.

Data has a tendency of becoming more interconnected as features are added to apps.
Ex: Perhaps fields in a record should be references to other entities (I.e. a recommender on LinkedIn is a user entity to keep profile pic etc linked and up to date).

Pure functions:. Only use the data passed to them (i.e. they don't make a call to the database to get anything else or use side effects)

#### Summary on models:

Historically, data started out being represented as one big tree (the hierarchical model), but that wasn't good for representing many-to-many relationships, so the relational model was invented to solve that problem. More recently, developers found that some applications don't fit well in the relational model either. New nonrelational "NoSQL" datastores have diverged in two main directions:

1. Document databases target use cases where data comes in self-contained docu ments and relationships between one document and another are rare.

2. Graph databases go in the opposite direction, targeting use cases where anything is potentially related to everything.
   One thing that document and graph databases have in common is that they typical don't enforce a schema for the data they store, which can make it easier to ada applications to changing requirements.

## STORAGE:

- log: an append-only sequence of records. Ex: in a simple db,. a set record that updates the same Id, the new changes are appended to the end of the lig so the get retrieves the latest/last entry of the record.

- Index: used to avoid searching entire db for a record (O(n)). - efficiently find a key in the db; basic idea is to keep extra metadata on the sides which acts as a signpost to help you located data you want.
  \*Tradeoff: speeds up reads, but slows down writes since extra data has to be written. Must index wisely based on typical queries for your app.

- Compaction: method for solving infinite log of keys (if appending data entries to end of file for example). We segment the log file off when log reaches a certain size and then remove duplicate keys keeping only the latest to create a new condensed log file.

Storing hash map of index in memory has limitations: num of keys must fit and range queries are not efficient (ex. Lookup of key in kitty0000 through kitty9999, you have to scan the whole range of keys). Alternative index is SsTables and LSM-trees.

- SSTables: Sorted String Table - the sequence of key value pairs in a SSTable segment is sorted by key. Makes compacting and merging of segments very efficient even on disk (so more keys can be stored)
  Also, can use an in memory index even with limited memory if the indexes point to offset of a block of bytes. Since data is sorted, you can find the block before your desired data exists and search from there. Saves space and I/O bandwidth use.

- LSM Tree: Log structured merge tree. Indexing structure a type of log structured index. Based on principle of merging and compacting sorted files. Lucene uses similar pattern for term dictionary in elastic search. Basic idea of LSM Tree is to keep a cascade of SSTables that are merged in the background.

- Memtable: a in memory tree structure of sorted data by key. When gets to certain size, data is copied to disk in segment files.

Branching factor: how many references fort ranges are in a page. Could be several hundred.

LSM trees vs. B-Trees for indexing: LSM trees are slower on reads than B-Trees but faster on writes.
Cons for LSM trees: compaction can interfere with high write throughout, needs monitoring. B-Trees are reliable and store keys in one place.

Note : most common type of index is B-trees. Also keep key value pairs sorted by key fort efficiently lookup and range queries. They break the database down into fix sized blocks or pages and read or write one page at a time. Pages contain references to other pages to narrow down search to ranges that encompass the key.

Write amplification: multiple writes per disk per one write to the database over the database's lifetime. Particular of concern on SSDs which limit overwriting of blocks before wearing out.

Multi dimensional index: used to search on multiple columns simultaneously. I.e. a latitude and longitude for a location. LSM trees and B-Trees cannot do this. The key is a concatenation indicating field/column order of the value.

- In memory databases: performance hits come from working with writing to disks. In memory dbs can give performance gains because they don't need to encode the days in a form that has to be written to disk.

#### OLTP: "online transaction processing". transactions for small number of records and access pattern based on interactive user actions (based on the users input), I.E. transaction processing. Payments, sale if items, etc.

#### OLAP: "online analytics processing". analytics, reading columns of larger number of records and aggregating them for business analytics.

### Data Warehouses

- Data warehouse: separate database used for analytics OLAP type queries separate from OLTP database. Purpose was to keep OLTP database low latency for business critical operations and separate large reads for analytics to prevent performance hits.

- ETL: Extract-Transform-Load. Process of getting readonly copy of OLTP data into warehouse so analysts can query it to their hearts contents without doing it on the OLTP database. On OLTP operation, data is extracted, transformed to analytics friendly format and loaded into the data warehouse.  
   Enterprise companies have data warehouse s, but smaller companies do not since their data sets are a lot smaller, they can do analytics on the same database.
  Typically sql relational data models are best for analytics.  
  Database vendors usually focus on supporting either transaction processing or analytics workload s but not both because the different types of processing need to be optimized differently.
  (OLTP process rows, where analytics db would use column compression and column oriented storage since the tables are so wide and we don't want to have to load entire rows and filter for queries.)

#### Storage Schemas

- Star schema: used for analytics data model. Central facts table containing records of say user events (very large). Facts have foreign keys or references to dimensional tables with extra info on the fact(who what when why how etc.). The facts table is the center of the star and the dimensional tables are the rays of the star.

- Snowflake schema: variation on the star schema. The dimensional tables have subdimensional tables. More normalized than star schemas, but analysts prefer star schemas since they are simpler to work with.

Fact Tables in data warehouses are typically very wide with many columns.

Column oriented storage, p 98-101. Good for compression and data warehouses vs. type oriented storage. Good for reading with advantages of sorting with compression, bit more difficult for writing

Materialized views for caching common aggregations of data, p101. Different from virtual view because an actual copy of the data is written to disk and cached. A virtual view just expands a query for execution.
More common in data warehouses or readonly situations since they are expensive for writes

OLTP VS OLAP database storage and retrieval summary: p 103

Encoding - p113, (serialization, marshalling) - translation of data from the in memory representation to a byte sequence for the purpose of sharing data with another process with which you don't share memory like sending data over a network, writing it to a file or database, etc (it must be a self contained sequence of bytes).  
Ex of Bute sequence binary encoded data p 116.
Avro is a more compact encoding than Json for example.

The Schema determines some of howdata is encoded,i.e. what type annotations are sent with the bytes of data like fields etc

Backwards and forwards compatibility with schema changes, p 121. To maintain backwards compatibility, every new field your add after initial deployment of the schema must be optional or have a default value!
You can only remove old fields that are optional, never remove a required field, and you can't use the same field tag ever again.
Forward compatibility: when old code can read new data.
Backwards: when new code can read old data.

Avro, p 122-124. Key idea is that the traders schema and writers schema do not have to be the same for future schema evolution.
Dynamic schema generation with avro, p. 126

A database of schema versions is useful and can be pulled but the reader to get a schema for decoding a record.

Message passing data flow , p. 137
Sender sends message to a broker which temporarily stores the message.
Decouples sender from receiver since sender does not need to know address of receivers, only the intermediary broker which remains constant.

Actor model, p. 138

Distributed data:
Reasons - scalability(spread read and write load over several machines), fault tolerance and availability (continues working if a machine goes down), latency (nodes spread out close to users)

## REPLICATION ch 5:

### 3 main algorithms:

- Single-leader
- Multi-leader
- Leaderless

#### Leader based replication (aka active/passive or master slave replication) - one of the replicas is the primary, clients send write requests to that, it writes to it's local storage then sends a REPLICATION log/change stream to follower replicas which make the same writes in the same order.

Client can only write to leader, but can read from any of the followers.
Built-in feature of postgres, Kafka, mongodb, MySQL etc.
Synchronous (all followers update before leader responses) is usually bad and has disadvantage of blocking a write if all nodes are synchronous
Usually configuration is set to be synchronous or semi synchronous (only one node is synchronous)
Dependent on leader not failing (chain replication can remedy this)

Failover: leader node fails and a follower needs to be assigned a new leader. Failure is determined by a timeout (i.e. 30secs). This is not fool proof and sometimes teams opt for manual failover to combat problems that occur when switching leaders.

Write Ahead Log: log of bytes representing changes is created before it is forwarded to followers. Used by postgres among others. Requires downtime if update to db software is made.
Postgres uses this, disadvantage is that the log is coupled to storage engine, so if you change databases you lose zero downtime upgrades.

Alternative is logical logs for replication. Decouples log from storage software. It is separate log for replication from a log for the storage engine.
The logical log just records information at row level for inserts deletes(just the primary key) and updates(just key and updates).  
This decoupling allowed leader and follower to run different versions of software or different engines.
Useful for external sending to data warehouses- change data capture.

Web apps commonly have many reads and fewer writes. In leader based replication option is to spread writes to followers to reduce load on leader.

Eventual Consistency , p 162: followers catch up to leaders data. Ex if you query the follower and leader at same time will get different data, but if you stop writing to database and wait a while, followers catch up and are consistent with leader.
\*This can be a problem with replication lag.

Poss solutions to replication lag problems:

- read after writes consistency: users can see any updates they made guarantee (does not guarantee other users can at that time). Reassures user their data was saved correctly.
  See p 163-4 for implementations.

Problem of asynchronous lag, multiple requests to random followers in different states (state appears to go back in time to user).
Solution: monotonic reads,p. 165. Guaranteed that user reads in a sequence will not go back in time (not that the data is the latest). Ensure user always reads from same replica.

Consistent prefix reads, p. 166, guarantees order of reads on a sequence of writes. solves problem of
Client receiving order dependent sequence of data reads out of order(because the first write had long lag on follower longer than another follower which received the second write update faster and sends it back to client sooner).

P 172
Conflicts: with asynchronous writes/multi leader

- conflict avoidance is simplest, i.e. ensure single leader implementation,if user edits profile send all writes to one data center.  
  -Converging to consistent state. Each write has ID, last write wins - this is dangerous and can result in loss of data. Alternative is to log conflict data and write custom code to resolve it later(or prompt user to choose resolution)
  \*\*\*Conflict resolution in multi leader systems is very difficult and poorly implemented if at all in popular replication software

#### P 177, Leaderless Replication

- used by Amazon dynamo (not AWS dynamodb which uses single leader architecture).
  Any replica accepts writes from clients. Either client sends writes to all replicas, or a coordinator sends them but does not enforce ordering unlike a leader would.
  Reads are also sent in parallel. If there are differences in data, version numbers are used to determine latest data.
  Client makes parallel requests to numerous nodes. If nodes fails and had stale data, client uses most update data based on version numbers if the data returned from the multiple nodes. (P. 178)
  Read repair: client writes up to date data to node that is behind,good for data when frequent reads.
  -anti entropy process: background process that checks all replicas for consistency, takes more time to get data up to date. Without this, data that is not read frequently is not durable using read repair alone.

Quorum reads, p. 179. Minimum number of nodes to qualify for successful read or write - lots of edge cases and not so simple in practice.

Last write wins, p. 186. Latest timestamp of concurrent requests is taken and overwrites older writes. Not good for losing data and only works if you assign keys to each write and make immutable to prevent data loss. Could be okay in acceptable data loss situations such as caching.

Determine if operations are concurrent: there is no causal dependency and the operations don't know anything about each other and do not build upon each other in any way. P.186
It's not important whether to operations overlap in time, only that they do not know about each other, they are still concurrent even if not happening at same time. P. 187

Versioning concurrent and concurrent write example in p. 188-9. Use version numbers with write requests taken from previous reads to determine what state the wrote is based on. Merges with latest version for record key.
Tombstones (markers for deletions) are used to resolve merging concurrent writes with deletes.

## PARTITIONING: chapter 6

(Summary on p 217)

Partitioning is necessary when you have so much data that storing and detailing with it on one machine is no longer feasible.

- main purpose is scalability, large data sets distributed/spread out across many disks and query load distributed across many processors.
- partitions are like mini databases (also called shards)
- usually combined with replication so that partitions are copied to numerous nodes.

- goal is to spread data evenly across partitions and nodes.

P. 204
Key based partitioning, partitions separated by range of keys. Can result knskewing if the key is something like a timestamp - putting all keys on one partition for a day. Need prefixing to combat this.

Hash partitioning, not as used, can require loss of adjacent keys for efficient lookups since they are results of hashing.

Request routing, p. 214. Directing requests to correct partition.
Service discovery: problem of routing where to go to find a particular piece of data.  
3 approaches:
all nodes know about partitions and pass request to correct one (gossip protocol - eliminates need for external service, but adds complexity in nodes), routing layer that knows which data is on which partition,
the client knows about partitions/nodes and there is no intermediary.
Key Problem: knowing about changes in assignments of partitions.
Zookeeper, p. 215: example of a coordination service with Kafka that maintains authoritative knowledge of registered nodes and partitions. The routing layer can subscribe to it and be notified when partitions change or nodes or removed.

## TRANSACTIONS, p. 222

-purpose is to allow ignoring of certain concurrency and error scenarios (partial failures) and database takes care of them.

- safety guarantees including ACID, p. 223

#### Atomicity

Not the same in multi threaded context (an operation completes on only one thread,system can only be in state it was before or after the operation,not something in between).
In database context it means a series of writes can be aborted on error, and all changes are automatically undone. The main point is to allow for a safe retry and simplify error handling.

#### Consistency

The database is in a good state as defined by invariants (statements about the data that must always be true) in the application (not the database!). The application is responsible for ensuring data is consistent.

#### Isolation

Concurrently executed TRANSACTIONS are isolated from each other and can not step on each other's toes.
"Serializability" - each transaction can pretend that it's the only one being run. The database ensures that when the transactions have committed, the result is the same as if they had run serially (one after the other) even if they ran concurrently.
The other sees either all or none of the transactions writes, but not a subset.
Often comes with performance hit and some systems use weaker forms of isolation.

Weak isolation ,p. 234

- most basic and most popular: Read Committed -- makes 2 guarantees that you only read committed data (no dirty reads) and only overwrite data that has been committed.
  Cannot see uncommitted data.
  Preventing dirty writes: delay the second write until the other has committed or aborted. Note: does not prevent race condition problems! Low level locks on object which is only allowed for one transaction. The other transaction cannot operate until the lock is released by the original transaction.
  Preventing dirty reads,p 234-237: using locks is not recommended as above due to performance response time hits. Instead the database remembers the old and new value of an object, serves the old value while write transaction is ongoing and only serves the new value when the write transaction has committed.

#### Read skew, p. 237.

Problem is not prevented by read committed isolation. A timing anomoly on a nonrepeatable read transaction on multiple interdependent records just before and after a write transaction on them. Causes read of temporary inconsistent state of data.
Solution: Snapshot isolation, p. 238. Each transaction reads from a snapshot of all data committed at start of transaction and just uses that until the end of the transaction. Only sees old data from that particular point in time.\*readers don't block writers and writers don't block readers with locks, since the operations are on frozen consistent snapshots.

\*\*Multi version concurrency control (MVCC) - several versions of data are kept from various points on time to prevent dirty reads.
Whenever a transaction writes to db a transaction Id of the writer is attached in a created and deleted by tag. This determines which versions of the record are visible or invisible to read transactions.
Overhead for this is usually small.

#### Dirty writes and dirty reads,

good summary on .p. 266. Reading or writing to records that are operated on mid transaction (before the other transaction is committed)

#### Lost updates problem

p. 243: concurrent read-modify-write cycles that "clobber" earlier writes and updates get lost.
Solutions:

- atomic update operations if database provides that. Usually best solution, exclusive lock object when read so no other transaction can read it until the update has been applied. "Cursor stability"/force all ops on single thread.
- compare and set,p. 245: allow update to happen only if value has not changed since the last time it was read. If it has you retry the read-modify-write cycle. \*\*\*Does not work if old snapshot is used for comparison, may not be safe!

#### Write Skew,p. 247.

Not a dirty write or dirty read, but a race condition where 2 records are updated that may use stale state because of snapshot isolation (using protected state of database at time of both calls). Similar to lost updates problem and can occur when multiple transactions read the same objects and then update some of those objects. When special case of different transactions updating the same objects occur you get a dirty write or list update anomoly.
\*\*\*Usually happens when your multiple queries depend on other records or state of the database for establishing a condition on whether to run the transaction or not.

Good Summary of read skew on p. 250

One possible solution to a form of write Skew is to lock the rows that the transaction depends on so other transactions cannot read from them concurrently, or better to use true serializable isolation if possible. This only works when the condition for writing is based on rows that already exist. (See phantom problem below).

##### Phantoms, p. 251:

the effect where a write in one transaction (creating a previously nonexistent row) changes the result of a search query in another transaction. Snapshot isolation avoid this problem for read only queries, but does not protect against problems in some read write queries. The problem is that there is a check for the absence of rows to establish a condition for running a write or not, so no lock can be established on rows to prevent read skew when concurrent

A possible last resort to solving phantom problem is materializing conflicts, p. 251. You create rows to represent data to lock on to prevent concurrency problems from phantoms. It is hard to do and the better solution is serializable isolation.

### SERIALIZABLE ISOLATION:

Strongest level of isolation that guarantees parallel transactions end result is as if they ran serially one at a time.

Actual Serial Execution: eliminate concurrency and run transactions on a single thread. This might be okay since ram is cheap and all data can be stored in memory. Can be used for oltp transactions which are typically smaller reads and writes.
Requires use of stored procedures for transactions which eliminate network hops and store all data for queries in memory, see p. 254.

Two-Phase Locking, p. 257. A lock on objects under transaction operation which is very strict. There is a lock on the object if a transaction is reading or writing to it, so another transition can not even read it (as opposed to only not being able to write to it while the lock is in place). This protects against write Skew and lost updates unlike snapshot isolation which allows reads (readers never block writers and writers never block readers) 1
(Similar to mutual exclusion, mutex, in multi threaded programming).

Reads acquire a lock in shared mode (allows for multiple transactions to hold a lock on an object and multiple transactions to read that object), but a write requires an exclusive lock where only one transaction at a time can access the record.

\*\*\*\*Biggest downside of 2pl is performance, affects throughput significantly over weak isolation.

Deadlock, p. 258: transaction a is stuck waiting for transaction b to release it's lock and vice versa.
The database detects this and aborts one transaction to allow things to continue.

Predicate locks, key idea is that it's a lock that applies to even objects that don't exist yet in the database. Effective for solving problems of phantoms. Creates a lock on all objects matching a condition. In combination with 2PL, creates serial isolation. Time c ok nsyming and not performant.

Alternative is index range locks. Most databases use this which is simplified and more performant than predicate locks. Approximate a predicate lock by making the condition match more broadly (matches more objects).

\*\*Range index locks in combination with 2 phase locking provide for serial isolation in a compromised way with lower overhead.

New algorithm is serializable snapshot isolation. P. 261. Still pricing itself but could be new default way of handling concurrency problems.
It is optimistic (allows transactions to continue and try to commit, if check fails it's aborted and retried. Serial execution is an ex. Of pessimistic where is assumed everything is unsafe and transactions get a lock and everything waits until it is safe to commit.
Optimistic is good with transactions of low contention (they only write and not read for example) but is slow otherwise and pessimistic methods are better.

Combating decisions made based on outdated premise, p. 262-263. Detect reads of a stake MVCC objects version(uncommitted write occured before the read),or detect writes that affect prior reads (there write occured before the read)
Ex, p. 265, database remembers which transactions read object, when transaction is a write to it, it looks for other transactions that have read from that data recently. Similar to acquiring a write lock but does not block but acts as a tripwire: it notifies the Transactions that the data they read may not be up to date. Any transactions that have not committed after the notification are aborted, while the transactions that have committed are upheld.

Main advantage of SSI is that a transaction does not need to block waiting for locks. The locks are tripwires as opposed to stopping everything else (optimistic).

#### Durability

Ensures that once a transaction is complete the data is not lost on the event of database crash etc. I.e. it had been written to hard disk memory or a certain number of nodes in a distributed system.

### Concurrency issues in distributed systems

Partial failures: one part of the system fails while others work. In a computer partial failures are escalated to faults that crash the system by design. A incorrect or partial response or result is considered worse because it is nondeterministic.

Partial failures and fault tolerance are required in distributed systems, or making a reliable system out of unreliable parts. Ex, IP protocol can err but the TCP protocol layer built on top of it corrects those errors,p. 277

May make sense to trigger network problems or errors and see how the system responds for testing.

Super computer: assumed reliable components and fails entirely when a fault occurs.

Timeouts,p. 282. Only way to try to determine failures since nodes do not know if a request or response failed in a distributed system.

Quorum is used to determine important decisions in a distributed system since they cannot be safely made by a single node in that system.

Variability of packet delays on networks is usually caused by queueing.
when many packets are sent to the same port or destination. The queue fills up causing packets to be dropped and resent.
When destination operating system queues the requests.
When TCP performs flow control which causes queueing on the sender.

UDP vs. TCP, p. 283. UDP does not perform flow control (to prevent overloading destination work packets) like TCP does. This eliminates some problems causing variable network delays and does not resend a packet that's lost. Good for voip or video streaming.

One possible solution to determining timeouts is to measure response times and their variability and adjust timeouts based on their observed distribution.

Telephone circuits for phone calls are synchronous networks with a fixed bandwidth creating a fixed latency, very reliable since it eliminates queuing issues as space is reserved for consistent packet sizes. This is a bounded delay. Uses circuit switching protocol.

Internet TCP networks use packet switching protocol with unbounded delays because the bandwidth needed for various data sent through them is variable, and this is optimized to use as much bandwidth as possible. Results in queuing.
P. 285

The trade-off: fixed bandwidth results in fixed delays and no queuing issues, but more expensive unoptimized use of wire. Dynamically assigned bandwidth maximizes utilization of there write but results in variable delays and queuing

### Clocks, p. 288

Time of day: synced with servers but can jump back in time if sync is updated. Not reliable for measuring duration, but good for time occurred of an event.
Monotonic: guaranteed to be incremental and useful for measuring duration vs. using time of day clock. Set based on arbitrary base, do not compare monotonic clock values from two different machines, since they're based on different things.

Time if day and monotonic clocks are known as physical clocks.
Logical clocks just record the order of events and increment based on an event occurrence.

Clock drift, p. 289. Quartz clocks in computers can run faster or slower depending on heat for example. Will reset with NTP servers at intervals to correct the drift.

Can cause lost data with last write wins conflict resolution. If one node has a faster clock than another, then the earlier write is registered at a later time than the latter write because the fast clock records a later time. Silent failure. P. 292.

Possible solution is to use logical clocks that increment based on event occurrence and keep track of order of events not time.

Clock times have a degree if confidence over a range of time for accuracy, they are not precise totally. For ex, 95% chance the time is within 100ms plus or minus of the returned time. Called uncertainty bound. P. 294

Distributed system try to accounts for clock skew by making sure the confidence intervals of multiple events do not overlap. One range must be entirely before or after the other.
Googles true time API returns a confidence interbal for it's time.  
To keep interval small Google deploys a atomic clock to each data center to keep them range to around 7 Ms.

Process pauses can cause timing issues:
Garbage collection can cause timing errors since it stops the thread momentarily and when the thread is started again it doesn't know that it was asleep and for how long until the next timer sync.

Hard realtime systems are used for safety critical software and guarantee that a process must complete in a certain time or the system will crash. P. 299.impractical for data processing server side systems, too expensive

Problems in the network or problems from a node are indistinguishable in distributed systems since nodes rely on messages received for knowledge of the outside.

Frequently a system requires there's to be only one of some thing. P. 301.

If a nice or client incorrectly believes it is the leader or lock lease holder incorrectly when another is, can cause errors. A way to combat this is fencing, p. 303.
Fencing tokens are constantly incrementing monotonic tokens sent to clients when they receive a lease (on being the leader or getting a lock for ex.) And those are sent with the requests. The fencing token must not be the current token declared by the token service and not less. The resource checks the token on the last write for the record. Prevents prices pause errors due to incorrect lease expiration checks.

#### Byzantine faults, p. 304.

When nodes send arbitrary, incorrect or corrupt responses causing errors.  
Byzantine meaning complex and devious, bureaucratic. Generals problem: generals need to agree by sending messengers but some are traitors and send false messages.

Byzantine fault tolerant system continues to operate correctly even if nodes malfunction not over protocols or malicious attackers interfere with the network.
Usually more relevant to aerospace systems that cannot fail with malfunctioning nodes acting arbitrarily due to radiation, or Bitcoin Blockchain.
Data applications generally do not need to be byzantine fault tolerant. All nodes are in n one organization and can be trusted and controlled and there are not radiation issues etc. More usedkn peer to peer networks.  
Web apps rely on a central server to deteine what is allowed, so they do not use byzantine fault tolerant protocols.

Byzantine protocols require the majority of nodes to be uncompromised, so they are not useful in systems where nodes are hacked since hacking one node means you can hack them all since they run the same software. Traditional means like authentication, firewalls, encryption, access control are used instead to prevent attacks.

System models p. 307.
Partially synchronous - unbounded deals occur but are mostly bounded and eventually resolve.
Crash-recovery- nodes that crash can and will eventually recover. Nonvolatile data is preserved and persists while in memory state is lost.

Algorithms are correct if they satisfy properties/conditions specified for them. P. 308.

System models and algorithm properties that make assumptions based on them are useful for determining an algorithms correctness.
Am algorithm can be proved correct by showing that they're properties always hold in some system model.

In reality, system models are abstract and help to train about systems, but sometime s code needs to handle a situation that is impossible in the model but occurs in real life. Usually it means telling the user they need to resolve it. This is the difference between computer science and software engineering.

## Consensus: getting all nodes to agree on something.

Ch. 9 p. 321

Eventual consistency: all reads will eventually return the same result as all replicas eventually are updated with all the latest data.
Difficult to deal with since the time until consistency is unknown.

Linearizability, p. 325
Makes a distributed system appear as synchronous/one node.  
Ex: if one clients read returns a new value (due to the most recent write request updating that record), all subsequent reads from other clients on that record must return the new value, even if the write request is ongoing.
It's only important that the write was processed on the database side, even if the ok response back to the client occurs after a concurrent read has finished! Ignores network delays for write responses.

Difference between linearizability and serializability:
P. 329
Linearizability is a recency guarantee which says reads will return the most recent write. Does not prevent write Skew without additional properties (materialization)
Serializability guarantees that transactions behave asif they had been run in some serial order,not that the read returns the most recent write.

Apps that don't require linearizability can be more tolerant of network problems. CAP theorem, p. 337. Trade-off, trade recency guarantee for availability

Few systems use linearizability. Ex. Cpu cache. Fetches data from cache first and any changes written to main memory asynchronously. Linearizability is lost, but performance gain is the reason.

\*Linearizability is slow. Performance is usually preferred as a trade-off for inconsistency.

Ordering, p. 340
Cause must come before the effect.

Total order vs. partial order
Individual numbers are total order example, you can compare them and identify which one comes before the other.
Sets are partially ordered. (a,b) vs. (b,c) are not comparable since their contents can differ. You can't necessarily say that (a,b) is before or after (b,c).
P. 341.

Key idea: when a replica processes an operation, it must ensure that all causally preceding operations occurring before it) have already been processed. If some preceding operation is missing, the later must wait until the preceding has been processed. P. 343.
Causal Consistency: tracks causal dependencies across the whole database. Database needs to know which version of the data was read to ensure it's the latest.

Using sequence numbers or timestamps to maintain total order and causal Consistency: monotonic logical clock (not physical or time of day) that is applied to data to determine and maintain causal order.

Problem with multi leader, nodes: we don't know which requests are causally related since processing order across replica nodes is unknown

Lamport timestamp is a possible solution, p. 346. We include a node I'd with the timestamp/sequence number. Greater timestamp value wins, if both are same the one with the greater node ID wins.
Key to Lamport ts: every node and client keeps track of the maximum counter value it has seen so far and includes that max on every request. When a node receives a request or response with a maximum value greater than it's own maximum counter value, it increases is own maximum to that value.
Cannot tell if operations are concurrent and it enforced total ordering, the advantage over version vectors is that it is more compact.
Requires knowledge of all operations to know total order, we can't determine that immediately and need to wait for gathering timestamps of other operations.

Total Order Broadcast,p. 348. Protocol for exchanging messages between nodes that tries to resolve the problem of total ordering on a distributed system.
Algorithm must satisfy two properties:
No message losses, if delivered to one node it has to make it to all other nodes.
Messages are delivered to every node in the same order.

\*The order is fixed at the time of message delivery, anode cannot insert a message into an earlier position of subsequent messages have been delivered. This makes it Superior to timestamp ordering.
Can also serve as a fencing token of desired since it is monotonically increasing.
Different from linearizability, because it only guarantees order and not when data was written last, it is not a recency gaurantee that says the read is the most recent write since recipients can lag behind others.

Concrete ex of making a linearizable call using total order Broadcast (as an append only live) for assigning unique username, p. 350. Basically only succeed if there are no earlier messages for the same register in the log.

Key difference between total broadcast ordering and timestamp ordering is that you get a sequence with no gaps. If message 6 is received after message 4, the node knows to wait for message 5 before delivering message 6. This is not gaurantee with Lamport timestamp, p. 351-2.

#### Consensus:

P. 353, it is possible to solve consensus problem FLP, if you decide how to determine a node is failed (ex via a timeout) and to exclude it from the quorum.

2 phase commits, p. 355. Algorithm for achieving atomic transactions across multiple nodes. (Completely different from 2 phase locking which is about serializable isolation).
Involves a coordinator or transaction manager (usually a library within same application process requesting the transaction).
Coordinator request writes data to multiple nodes.

1. coordinator send a prepare request to all participants (nodes) asking if they are able to commit.
2. if all reply yes, a commit request is sent to actually make the commit, otherwise it is aborted.

\*A transaction unique global id is used with all phase requests to tie the different requests and data together. It is used in a log as well to record the commit decisions made for that whole transaction. This log is written to disk and must be done before sending requests to be used as a recovery mechanism if the coordinator crashes.
For this reason 2PC is called a blocking atomic commit since it can become stuck waiting for the coordinator to recover.

2 points of no return, participant says yes, and the coordinator commits. Even if there are crashes, those decisions are binding and the commit will be retried forever until it succeeds.

3 phase commit is an alternative which is nonblocking,but requires bounded delays n response times in the system- this is not practical in most network systems with unbounded delays. 2PC continues to be the standard because of this.

2pc/distributed transactions can cause operational and performance problems in practice, so cloud service providers can choose not to use them. Performance problems are caused by disc forcing (fsync) required for crash recovery and additional network trips.

P. 360
2 types of distributed transactions:
Database-internal transactions: all nodes are running the same database software.
Heterogeneous distributed transactions: nodes are running different software, database engines etc.

Internal distributed transactions can work well for to them being optimized for the particular engine, but heterogeneous transactions are challenging.

P. 361
XA transactions: standard (C API not a network protocol) for implementing 2 phase commits across heterogeneous technologies. Short for extended architecture, used in many relational databases. Assumes you use a network driver or client library to communicate with participant database or messaging systems to determine if an operation should be part of a distributed transaction and coordinates it all.

XA transactions solve the problem of keeping several participant data systems consistent with each other,but comes with problems and limitations. Key is that the coordinator is a kind of database where transaction outcomes are stored, so it is a critical part that cannot go down to retain availability.

Problem: if the coordinator crashes and transactions are left in doubt, this causes availability of your database to be lost until the coordinator recovers. There reason is transactions hold a lock on rows until they are committed or aborted, so other requests for those affected rows are blocked.
Orphaned in doubt transactions can occur if the transaction log written to disk is lost, so when the coordinator recovers it does not have information to resolve them. This can cause infinite blocking since the locks on those rows remain.
The only ways out of this are manual resolution by a database administrator or heuristic decision by a node participant which breaks the atomicity of the operation. These are applied only in catastrophic situations.

##### Core idea of consensus/properties, p. 365: all nodes decide on the same outcome, once a node has made a decision, that decision cannot be changed. (Uniform agreement and integrity properties)

Validity: node must decide a value, termination: if a node crashes it is assumed it will not come back and it is discounted.
2 phase commit does not satisfy termination property since it requires a coordinator node can crash and recover. Some consensus algos only satisfy agreement, validity and integrity but not termination properties.

Epoch numbering n quorums for consensus,p. 368. Nodes keep track of a monotonically increasing epoch number for each leader election to prevent split brain and determine which node is the latest leader.

Key difference between consensus algorithm and 2 phase commit: 2pc leader coordinator is not elected and consensus algos only require vote from majority of nodes while 2pc requires a yes vote from all nodes.

Consensus algorithms come with a cost:
Effect a synchronous form of replication affecting performance.
Require fixed number of nodes to determine quorum/majority and require minimum amount of functioning nodes.
Reliant on stable network since timeouts determine node crashes, can results in stopping progress and performance as work is done to repeatedly elect leaders etc due to network issues.

Coordination services, p. 370.

Zookeeper has an API similar to a database (read write vals to keys and iterate over keys) and requires consensus, but developers don't use them directly, it runs in the background.

Zookeeper is designed to hold all data in memory (writing to disk only for durability), so you don't want critical data there. It uses total order Broadcast for replication consistency writes, applying the same writes in the same order.

Zookeeper manages leaders for example and failover to other nodes if a leader goes down. It's changes are processed on timescales of minutes or hours. p. 372.

Also performs service discovery(what up addr to go to for a service).

Is part of a history of membership services which determine which nodes or members are currently active and live in a cluster. Consensus/quorum vote is key to this determination.

## PART 2

Systems that store and process data can be grouped into two broad categories:

Systems of record - source of truth with normalized representation of a fact/record

Derived Data Systems - takes data from another store and transforms or processes it in some way. You can reconstruct the data of it is lost from the source material. Usually denormalized, you can have several sets of data looking at the original from different points of view.

\*\*\*By being clear about which data is derived from which other data, you can bring clarity to an otherwise confusing system architecture.

Typed of systems,p. 389-90.
Services: wait for instruction from client and try to handle it as quickly as possible and send a response. Response time is primary measure of performance along with availability is important.

Batch processing systems (offline): jobs take a while, few minutes to several days. Takes page input of data and produces some output after processing

Stream processing systems (near realtime): consumes inputs and produces outputs instead of responding to requests ( like batch processing systems). Stream job operates on events shortly after they happen whereas batch job occurs on a fixed set of data. Has lower latency than batch processing systems.

Sorting vs. in memory aggregation for batch processing:
Working Set, p. 393: the amount of memory to which a processing job needs random access (in memory data). If the working set is small enough to fit in memory, aggregating works, otherwise sorting and spilling over to disk to operate on chunks and segments then merging them is better (i.e. MergeSort or using unix commands like sort which spills to disk and uses multiple threads for parallel processing)

Unix philosophy, p. 394: read this for review. Programs should do one thing and produce simple output intended as input to another unknown program. Sort for ex. - can be used in combo with other commands through pipes and is barely useful in isolation. It becomes powerful in combination with other small programs/commands.

Programs written by different people that can be joined together in flexible ways.

How to do this? With a uniform interface. To connect any programs output to any other programs input, all programs must use the same input output interface. (In unix that interface is a file - file descriptor which is an ordered sequence of bytes). Me re examples the n p. 395.

Separation of logic n wiring, p. 396
Separating the input/output wiring from program logic makes it easier to compose small tools into bigger systems.
Ex, unix used stdin and stdout as channels which a program can use for plugging into to get input and spit out output to. The program(s) does not worry about file paths, the input origin and output destination is abstracted so it doesn't know anything about it's specifics.

Allows for experimentation by making inputs immutable so that running an input through a pipeline to see what happens does not damage our alter the original input.

### MapReduce, p. 397

Similar to unix tools, but distributed across machines. Reads and writes files on a distributed system.

The inputs are immutable and the outputs are written once in sequential order not modifying any existing part of the destination file.

Distributed filesystem: nodes can access files on other machines while a NameNode keeps track of which files are on which machines. One big
filesystem that can use disk space on all machines in the system.

MapReduce example,p. 399
Read inputs and break them up into records
Extract key and value needed from each
Sort extracted by key (allows for easy handling of combining values)
Call reducer function to operate over each record.

- role f mapper is to prepare data so it's disable for sorting, role of reducer is to process data that has been sorted.

Key difference from unix commands is mapreduce can operate in parallel across many machines - it just handles one record at a time so it doesn't need to know where input is coming from or where is going.

Principle: putting computation near the data. Mappers are run on machines that store a replica of the data, preventing the need for copying the file over the network.

The shuffle, p. 402: data being sorted is likely to large for sorting on one machine. The mapper partitions data by key hashes and chunks are sent to different machines for parallel sorting and then merged by reducers.

MapReduce can be chained in a workflow if more than one sorting/processing round is required. Hadoop for ex. Sets the output of MapReduce to a specific path, and sets the input location as that path for other chained MapReduce instances to use. It's like a sequence of commands where each commands output is written to a temporary file and the next commands input is read from that temporary file.

Batch process joins, p. 404-405.
\*In order to achieve good throughput in a batch process, the computation should be as much as possible local to one machine.
Making network requests for every record to process is very slow. It's also nondeterministic since data on remote store could change during the process.
For example joining a activity log of users to user records for each event:
The solution is to take a copy of the user database (i.e. from a ETL backup processing data warehouse source) and keep it on the same distributed file system as the activity log is on top make processing efficient and eliminate external calls over the network to get the user data.

You could then use MapReduce on the files to make the join data.
Ex:
One mapper extracts key value of userid and event from the activity log.
In parallel another mapper extracts key value of userid and date of birth from the user database copy.
(Files are partitioned and multiple mappers could run over batches in parallel).

Mapper- extracts key value information and sorts data
Reducer- processes sorted list of data

Sort-merge algorithm, p. 406
Ex. Getting user ages for urls visited:
Mapper sorts all records by key (i.e. user id) so that events related to user are all adjacent.
Secondary sort - mapper always sees the record from the user database first, followed by activity events in timestamp order.
The reducer stores date of birth from first record in group in memory and iterates over the events for the userid to make pairs (url with user age).
**Since these are sorted, the reducer only needs to keep one user record in memory at any one time as it processes them for a particular user in one go.
Summary: map sorts by key and reducer merges together the sorted list data from both sides of the join.
(Multiple reducers could operate in parallel on each grouped list by user id possibly)
**The sorting allows for efficient processing of grouped data and memory usage.

\*The MapReduce programming model separated physical network communication aspects of computation (getting data to the machine) from application logic (processing data once you have it). P. 406 (?)
The mapper sends "messages" to the reducer and the key represents a kind of address (all key value pairs with the same key are delivered to the same destination, a reducer)

An idea of MapReduce is to bring related data to the same place.
Note: this breaks down if there is a large amount of data for a particular key (i.e. a celebrity user with millions of followers, etc). This is known as a linchpin object or hot key.
These can cause Skew or hot spots that slow down a batch job us ok ng MapReduce since a reducer will have to process a large amount of grouped data.
A skewed join can mitigate this problem by scanning for hotkeys before sending their data to multiple reducers to share the work in parallel (requires replicating the smaller part of the join to all those reducers).
An alternative is to manually identify hotkeys and designate them as such in metadata to store related records in separate files and do an map side join.

Map side joins don't use reducers or sorting and rely on ability to make assumptions about data (i.e. they are sorted or grouped a certain way by default or of a certain set size), p. 408. Useful when one side of the join is a small data set (because requires that the smaller side is loaded into memory of each of the mappers).
Ex, broadcast hash joins: smaller dataset is kept in memory of each mapper(broadcasted to all), and the larger data set is split into blocks among the various mappers to process it in n parallel with reference to keys of the smaller set in memory for joining them

Reduce side joins are most of the examples above where the join logic is in the reducers (merging etc).

\*Output of map side joins differ from reduce side joins in that output of reducer side join is partitioned and sorted by the join key, while map side output is partitioned and sorted the same way as the large input set of data.

MapReduce separate logic from wiring(configuring the input and output directories). This is good unix philosophy. Separation of concerns- one team can work on a job that does one thing well, another can work on where and when that job is run.
Inputs are immutable and no side effects.

In practice making data available quickly even if it is in a more raw format, as opposed to carefully defined and modeled, is usually more valuable.
P. 415.
Collecting data from multiple sources for processing in it's raw form and writing about the schema later allows the data collection to be speeded up (aka a data lake). Otherwise the data collection to a centralized source for the purpose of aggregation or processing is much slower.

\*This shifts the burden of interpreting/standardizing the data format from the producer to the consumer (schema on read approach).
The sushi principle, raw data is better.  
This can be a good approach of consumers have different priorities or use cases for data, since each consumer can decide how to interpret and form the raw data differently.

P. 418. MapReduce is fault tolerant because it is usually a lower priority task which can be terminated to grant resources to higher priority takes at any time. The approach is to overcommit resources to lower priority tasks for more efficiency, which can be diverted to high priority tasks as needed, instead of separating high priority resources and lower ones. This enables better resource utilization in a computing cluster.

In an environment where tasks are not are not so often terminated, MapReduce makes less sense.

P. 420. Publishing output to a well known location in a distributed system allows loose coupling so that jobs don't need to know who is producing their input or consuming their output. Another example of separating logic and wiring.

Intermediate state: the means of passing data from one job to the next.

Materialization: process of writing/assembling this intermediate state data out eagerly (before it's requested).
In contrast, unix pipes do not materialize output for the next command (i.e. assemble n write to disk, for example), they stream the output to the next command (it is held in a in memory buffer and sent incrementally to the next commands input).

MapReduce fully materializes output before the next job can use it as input. This slows processes down since unlike a unix pipe, output can n be consumed incrementally as soon as part of it is produced

Deterministic: given the same input data, the operators always produce the same output.
P. 423
Desired is a deterministic processing algorithm since it is then more fault tolerant and can reuse inputs produced at an intermediate stage of the process on failure and pick up where it left off.
Nondeterministic processes include operations with a physical time clock, random numbers and iterating of a hash table where order of keys is not guaranteed.

recovering from faults by recomputing data is sometimes a solution for long running jobs that fail in a stage.
Not always - it can be better/cheaper to materialize the intermediate data at different points in the job to files instead of recomputing it all from the beginning.

Distributed graph data algorithms differ from performance overhead of communication between machines and partitions.
Parallellizing graph algorithms efficiently is still being researched.
If your graph data can fit on one machine, even if it needs to be stored on disk, is better to run algorithm s on one thread vs. on a distributed system.

P. 430, summary of batch processing.
By having immutable inputs and operations with no side effects, this allowed for robust and simpler fault tolerance, since processes can be rerun at various stages with the same end output effect (previous output from failed jobs is discarded)

In batch processing jobs, the data is bounded(it has a fixed size for ex.). Because of this a job can know when it's operation is complete.
(This is different from streams where data is unbounded and a job never completes).

"A complex system that works invariable evolves from a simple system that works. The increase is also true."

### Streams, p. 439-40:

Batch processing artificially divides data into durations for processing (i.e. once a day for a days worth of data, or once an hour) and deals with bounded data so it knows when it's complete and how to sort correctly.

Stream processing simply processes every event as it happens.

A stream refers to data that is incrementally made available over time.

An event is a self contained record that is produced once and consumed by consumers.
A group of related records is called a topic or a stream (equivalent of a collection or table in a database).

One approach is to produce an event to a data store and have consumers periodically poll the store. This is not ideal and has a lot of overhead (the more often you poll, the lower percentage of events returned).
A better approach is to have consumers be notified when new events appear in contexts dealing with low delays on continual processing. P. 441.

2 questions for determining what kind of messaging system:

- what to do if producers produce messages faster than consumers can produce them: either drop messages, buffer a queue, or apply backpressure (stop block producers from producing).

- what happens if node goes offline? Are messages lost or are they made durable? If messages can be lost then latency and overhead is reduced.

Direct messaging systems are used when low latency is important. These systems make producers and consumers communicate directly with no intermediate nodes/brokers. Applications must accept possibility of message losses. Ex is UDP multicast for stock market quotes in realtime.
Also webhooks: consumer exposes a service allowing producers to make direct contact with them; a service registers a callback url with another service, and it makes a request to that URL when an event occurs.

### Message Brokers, p. 443

- a kind of database that is optimized for handling message streams. It runs a server which consumers and producers connect to as clients.

Brokers handle durability - some keep messages on memory, others write to disk. Generally they allow unbounded queuing.

Middleman allows for asynchronous consumers (the producer just gets acknowledgment from broker and the consumer can read the message at some time in the future).

Difference between brokers and databases, p. 444:

- brokers usually delete messages after they are delivered to consumer, so they are not suitable for long term storage.
- brokers notify clients when data changes (new events), while databases usually don't notify clients when a record is updated.

Handling multiple consumers:

- load balancing : brokers send each messages split to a different consumer node for shared processing.
- fan out: each message is delivered to multiple nodes.
  P. 445

Brokers use acknowledgements to prevent message lost. A consumer must tell the broker it finished processed the message until the broker can remove it from the queue.

Log based message Brokers,p. 447.

- purpose is to achieve durability and low latency notification facilities
- brokers typically delete a message after consumption, unlike a database. If a log is used (a append only sequence of records on disk), durability can be achieved.
- a producer sends a message by appending it to the log. A consumer recieves messages by reading them from the log sequentially. Once reaching the end of the log it waits for a notification that a new message has been appended.
- logs can be partitioned to different disks to improve performance (as opposed to reading from one disk drive). P. 447-8.
  Kafka uses this approach to allow for millions of messages per second to be processed.
  Messages for each offset have a monotonically increasing key (offset) per partition (note total ordering is not guaranteed across partitions)
  Note: messages that require ordering must all be processed on the same partition.

The offset of the consumer is recorded periodically which tells what messages have been seen or not (since it is monotonically increasing). This eliminates the overhead of acknowledging every single message and eliminates acknowledgements altogether.

Since log based messaging requires ordering, it is not suitable for messages that are expensive to process (since it must process in order single thread like). For small cheap messages where ordering is important, it is ideal.

In messaging systems throughout can depend on the amount of history retained, since one the buffer fills up messages need to be written to disk to save them which is slower. If all history can fit in memory than performance is faster.

The only side effect of processing messages is a offset setting on the consumer which point s to the location of the last message processed in the log.
This separates derived Data from the input as in batch processing and allows for experimentation and replaying of messages.

Problem with heterogeneous systems (multiple data stores of different types and engines) that need to be kept in sync. Writing to all can cause race condition errors and inconsistency.

Change data capture, p. 454.
Process of observing all changes written to a database and extracting them in a form in which they can be replicated to other systems.

You could have a CDC stream that captures all changes in an append only mode and all other systems can read from that log stream to be updated consistently.
System of record is the leader and other systems could be considered derived Data Systems.

CDC essentially turns one database into a leader (that captures changes in the right order). and all other data systems into followers. Reducing the change capture to a single leader source is one way to prevent the above mentioned race conditions.
Log based brokers are well suited for this since they preserve the ordering of messages.
(Kafka connect offers CDC connectors for various databases, see further ex tools on p. 455)

CDC is usually asynchronous, which does not wait for all consumers to process the change in the stream before committing it. This allows for slower consumers not to affect the system performance but the downside is that replication lag issues can occur.

The log must be truncated since disk space is limited and you can infinitely record changes, and an initial snapshot can be used. P. 455.

alternative is log compaction: a background process looks for entries with the same key and deletes all entries except the most recent update to conserve space.
Kafka does this and it eliminates the need for snapshots.

Kafka Connect is an effort to integrate change data capture tools for a wide range of database systems with Kafka. It can be used to update derived Data Systems once the stream of change events is in Kafka.

Event Sourcing, p. 457:

- involves storing all changes to application state as a log of change events.
- similar to CDC except it treats the system of record/change capture as having immutable events (deleting and updating is discouraged) in the event log. Events are designed to reflect things that occur at the application level, instead of low level state changes i.e. parsing the replication log in a database)

The point is to have more meaningful record of events by recording things such as the users actions as immutable events instead of recording the low level effect of those actions on a mutable database.

\*\*\*This makes application evolution easier as well as helps with debugging since you can understand why something happened, as opposed to just what.
The event has a descriptive name describing a business event, not just that a record was deleted it written.

In event Sourcing, you need to replay the log in a deterministic way to reconstruct state and you cannot do log compaction since every event represents a user action at a high level. You must replay all events. Entries in the event log are never deleted unlike in CDC compaction.

Command: the user request to do something. This is not an event. The application must first validate the action can complete successfully and then it can be recorded as a fact, or an event.
A command and event transaction has to happen synchronously, the command is validated and then the event is published. Consumers can then read the event asynchronously and cannot reject an event as it is immutable.

Said some of his best lieder melodies came to him when he was polishing his boots at dawn as a younger man.

Brahms could be difficult to socialize with, being quiet alot and ignoring friends in company list in thought.

Brahms teacher instilled in him a great respect of the form and traditions of the past.

The principle of immutability is what makes event Sourcing and change data capture so powerful.  
Key idea is that mutable state of an application (as represented in a database for ex.) And an append only log of immutable events that caused that end state do not contradict each other. The channels represents the evolution of state over time. P. 460.

The changelog is a source of truth and the database only holds a cached subset of entries containing the latest information.

One of the main advantages of immutable log of events is it makes data flow in the system easier to understand. If a mistake is made or bad data is inserted, it makes debugging easier to do since you can diagnose what happened and recover from the problem.

Event logging also helps with analytics and understanding user actions and patterns.

Logs also allow you to build different views of the data optimized for different systems and use cases. P. 462

Command Query Responsibility Segregation (CQRS): separating the form in which data is written from the form it is read. P. 462. Allows for flexibility since most schema evolution is caused by how data needs to be read for different use cases instead of how it needs to be stored. Allows for flexibility and creating different read views of the data.

The fallacy is that data must be written in the same form as it will be queried. Using a translation service between the event log and read optimized application state solves many problems such as denormalization since the translation from the log to various views can keep everything in sync from a central source of truth.

The main downside is that since consumers read asynchronously from the system, a consumer can make a write to the log and then makes a read from the system which does not yet include their recent write.

Event Sourcing can help with multiple object updates and concurrency since the event can be designed to have a self contained description of a user action. This only requires a single write in one place, namely appending to the log. P. 463.

Large datasets that do n not change frequently with updates and deletes and only have data added are ideal for immutable log approach. Data sets with frequent updates are not good for using this immutable approach.

Legal requirements to remove data can also make an immutable log less than ideal since you need to rewrite it's history.

Processing streams, p. 464.

- operator or job is code that processes a stream to produce other derived streams.

A processor will consume a stream in read only fashion and write the output to a different location on append only fashion.

Complex event processing (CEP), p. 465. Allows you to specify rules to search for certain event patterns of events in a stream (similar to how a regex allows searching for a string pattern in a string).
Queries for patterns are stored and registered and of a pattern is matched then a complex event is emitted by the system.

Stream analytics, p. 466. Concerned with measuring event patterns over a window of time to determine trends or anomilies. Kafka Streams is an example of this.

Searches on streams, p. 467.  
For example, queries that are stored which search for text or complex criteria on individual events (i.e. a notification service for Zillow on new properties that match a search that are listed).
Elastic search percolator feature does this.

Beware of not measuring process time vs. measuring windows based on timestamps. Can lead to misleading results, see ex. P. 470 if stream processor goes down and then reads backlog creating a spike in the window..

### Time window issues

- how to handle straggling events reported for a time window, device clocks vs server clocks and possible solutions. P. 470-472

Types of windows, p. 472
Tumbling
Hopping
Sliding
Session

Joining Streams, p. 473.

Steam-stream joins, ex. Measuring what search results are or are not clicked for a given search. You need the click events and search events. A timeout determines when a user does not click on a result by checking a index of session IDs and maintaining state of search events and click events that match the search details. If timeout expires an event is emitted saying the user did not click on the search results.

Enrichment, enriching stream data, p. 474. Adding information from a database to events. Ex, extra user info is added to the output of user action events which originally only contain an ID and the action.

Enrichment can happen in stream table joins, but since the call to the database for enrichment data can cause delays, an option is to load a local copy of the database into the stream processor to eliminate the network round trip.
As the database changes, change data capture technique could be used to forward changes from a changelog to use to update the local copy.
P. 474.

Table-table joins:
Good summary of Twitter timeline problem on p. 475.
Aggregation requiring looking up many associated records can be avoided by keeping a cache of aggregated recent related entries on the single origin record, to make one lookup instead of many.
Ex, followed users tweets are added to the followees cache everytime any of the followed users makes a tweet. This makes pulling a users timeline on load just one call and much faster.

The commonality is that they all require the stream processor to maintain some state based on one join input and query that state on messages from the other join input. P. 476.

Slowly changing dimension: when the ordering of events across streams being joined is nondeterministic resulting in a job being rerun with same input but getting different results. P. 476.
One way of solving this is putting a identifier on events at a certain time to enable deterministic reruns of jobs, but this eliminates log compaction since all records must be retained that represent state at different points in time for reference.

Fault tolerance in stream processors.

- in batch Job processing it's easy since input is immutable, jobs can just be restarted and the output of a failed job is discarded with output only being produced on successful job completion.
  This ensures that effectively data is only processed once (exactly once semantics), even though it might be processed multiple times on failures, the output appears only as if it was done one time.

It is not as straight forward in stream processing since waiting to make output visible when a task finishes is not an option since streams are infinite and processing is never finished.

microbatching: a solution is to break the stream into small blocks and run micro processing batch jobs on them. For example one second batches.

Checkpoint is ng: another option is to establish checkpoints and write to disk for recovery use. Any data after the last checkpoint is lost.

to ensure exactly once semantics, must ensure that all outputs and side effects of successful processing take effect only one time on success.
I.e. side effects such as push notifications or resetting offset in log based brokers.

All side effects must either all happen atomically or not at all.  
Apache Kafka does this and keeps the transactions internal by managing state and messaging within the framework. The overhead is amortized by processing several input messages within a single transaction. P. 478.

Idempotent: operation can be performed multiple times and it has the same effect as if you performed it only once. Can be another effective way of achieving exactly once semantics with little overhead.
Has the same outcome regardless of how many times it is performed.

Operations that are not naturally idempotent can usually be made so by using some extra bit of metadata. For ex, including the monotonic offset from kafka messages with write requests to databases, can check it and ensure the same data isn't written twice.

#### Summary, p. 480.

AMQP/JMS style message Brokers explanation vs. log based brokers.

P. 492.
Log based derived Data is the most promising approach for integrating different data systems over using distributed transactions. The drawback is the necessity for eventual consistency due to the asynchronous consumption by clients.

The key idea for dealing with distributed data is determine a total order of writes, i.e. by funneling the inputs through a single system that determines order (i.e. change data capture or event Sourcing).

##### Total order Broadcast: determining a total order of events, equivalent to consensus. P. 493.

Open problem is being able to scale total ordering on a geographically distributed system since ordering requires one node or leader to pass through for ordering. Having distributed leaders handle total ordering has not been figured out yet.

Total order Broadcast is currently a necessary bottleneck to maintain causal dependency and state consistency in applications.

Asynchrony is what makes systems based on event logs to drive state robust. It allows a fault in one part of the system to be contained locally whereas distributed transactions abort if any one participant fails. P. 495.

Having the ability to reprocess data (i.e. with stream processing or batch processing jobs) allows greater flexibility in schema evolution since you can repurpose and restructure that data as needed as output from processing. Otherwise you're limited to only optional or additional fields for schema evolution.

Gradual evolution: reprocessing data allows you to have two schemas simultaneously since you can prices one view of the data as an old schema and process another view as the new model schema. This allows you to test the new schema with the old still in place as a fallback and stable version. P. 497.

Lambda architecture, p. 497. Run two systems in parallel, batch processing and stream events.

An improvement to the lambda architecture is unifying the batch and stream processing on one system.

A database containing 10 million small records is normal (unlike a folder in a file system)

Both unix OS and databases are simply information management systems (you store data and query/update data).
Unix is low level management and databases offer high level abstracted management interfaces.
Unix offers a thin wrapper around hardware resources while relational databases offer simple query which handles concurrency optimization and joins under the hood.

What happens when you create a index in a relationship database, p. 500. Scans snapshot of database, picks out field values being indexed, sorts them and writes the index. Afterwards the backlog of new writes is scanned to add to the index and it must be maintained as new transactions are made.

This is similar to seeing up a replica or bootstrapping change data capture with an initial snapshot. The database reprocesses existing dataset and derives the index as a new view onto the existing data.

You can look at data flow across an entire organization as one huge database, p. 500.
Batches, streams or ETL processes that transport data to another place and in another form are like a database subsystem that keeps indexes or materializes views up to date.

Assumption: no single data model or storage format exists that is suitable for all access patterns.

Two avenues for a cohesive system involving different storage and processing systems:

Federated database: (unifying reads) provides a unified query interface to a wife variety of underlying storage engines and processing methods. Also called a polystore.  
Offers high level query language with a complicated implementation.
Requires mapping one data model into another.
This addresses read only queries across the system and doesn't help with synchronizing writes across a system.

Unbundled database: (unifying writes). Follows unix tradition of small tools that do one thing well, communicate through low level API and can be composed using a higher level language.
Reliably plug together storage systems (thorough change data capture or event logs for example). This is like unbundling a databases index maintenance feature.p. 501.

The point of these approaches is to compose a reliable and maintainable system out of diverse components.

The hard problem is keeping writes to several storage systems in sync.

Distributed transactions are not as robust as an asynchronous event log with idempotent writes.
It's much easier to implement when dealing with heterogeneous systems. P. 502
Primary benefits:
Loose coupling of components to the stream.if a consumer faults then it doesn't affect the rest of the system, it will catch up using a buffered list of messages when it recovers and v other consumers continue as normal. With distributed transactions, the whole system faults if one consumer faults.

The goal of unbundling it's to allow you to convince several different databases in order to achieve good performance for a much wider range of workloads.
For some specialized workloads a single database system would work better. Unbundling is for systems that require a broad range of workloads and processing strategies.
If there is a single technology that handles all of your needs your better off using that instead of trying to reimpliment it from lower level components (i.e. in an unbundling and composing different technologies fashion).

Most applications today are stateless services, the request is sent to any application server and the server forgets about the request after the response is sent. State is preserved in a database. P. 506.

Most databases don't yet have a subscribe option and you usually have to poll to get updated changes when a record changed.

Stream operators, p. 507-508. Application code that can act as versatile stream processing told. It acts like a pipe and takes stream input, processes it and products stream output.
Contrary to roc or rest micro services, stream operators have a one directional and asynchronous communication mechanism (vs. synchronous request response system).
This is called a dataflow approach vs. a micro services approach.

Example of purchase in one currency, but charged in another, p. 508.
In dataflow, the code that processes purchases subscribes to a stream of exchange rate updates and record the current rate locally whenever it updates. This helps performance since when a on purchase is made, the currency exchange rate is looked up locally as opposed to having to make a call to an external database or service in a micro services approach.

Subscribing to changes rather than querying the current state when needed, is a dataflow approach which is better since when done piece of data changes, any derived Data that depends on it can be swiftly updated.

Dataflow write path, p. 509: whenever data is written, goes through stages of batch and stream processing and eventually every derived Data set is updated to incorporate the newly written data.

Read path: reading from the derived dataset, perhaps more processing, and construct response to the user.

Difference between data flow diagram and flowcharts: show flow of data not of control. Shows situation from point of view of the data instead of those who act on the data.
Dfd shows possible paths of data.

4 symbols, p. 40. Vector, process, file/database line, source/sink (net originator or net receiver of data).

An advantage of. Data flow diagrams is errors are glaring and obvious.

Trying to break down the system by functions is to imprecise. An effective partition of a system is when the interfaces among the pieces are minimized. P. 42.

Write path: portion of data journey that is precomputed, regardless of whether anyone wants it (eager eval)
Read path: portion of data journey that happens only when someone asks for it (lazy eval)
P. 510.
Derived dataset is where the two meet and is a trade-off of work that needs to be done at either end.

Ex: full text search index splits work on write and read path. With no index to update on writes, the read becomes very expensive.

Websockets, p. 512. Open TCP connection that allows servers to push messages to browsers.

P. 513. The rain realtime systems aren't more widely implemented. Many libraries and databases in existence assume stateless clients and don't offer support yet for subscribing to changes.
Would need to move away from request response system to pub sub models.

Duplicate suppression, p. 517. I.e. TCP does this with packets before handing to recipient.
T transactions on databases do not gaurantee idempotent operations of the client connection fails and the end user retries before getting acknowledgment of commit back from server. This results in duplicate queries and incorrect data.

A solution is to uniquely identify requests. Use a hash of inputs or uuid which is sent with the requests and stored in a request IDs table for checking in the database. P. 518.

The end to end argument, p. 519: correct and complete implementation of a function is only possible with the knowledge and help of the application standing at the endpoints of the communication system.
As in the above example we cannot guarantee duplicate suppression without an end to end solution, namely a transaction identifier passed all the way from client to database.

Log gaurantee all consumers see messages in the same order (total order Broadcast, equivalent to consensus). P. 522.

Fundamental principle for avoiding conflicts in partitioned log message system is that any writes that may conflict are routed to the same partition and processed sequentially. P. 522

Timeliness: ensures users observe system in an up to date state. Cap theorem and read after write are some ways to satisfy timeliness. P. 524

Integrity, data is correct and not missing and views represent the data accurately. Consistency is impossible without integrity and loss of integrity means manual repair is required.

Violations of timeliness is eventual consistency, violations of integrity are permanent inconsistency.

Timeliness is less critical than integrity for most applications.

ACID guarantees timeliness and integrity. Though Event based systems decouple timeliness from integrity.

Exactly once semantics is a means for preserving integrity.

Compensating transaction, p. 526. Sending a new transaction to correct a mistake (i.e. a double booking or using a unique username that's taken).

Apology and compensation is acceptable in lieu of timeliness of constraints if the cost is low. Linearizability may not be necessary if apology and compensation transactions will suffice.

Temporary violations that are fixed up later as long as integrity is preserved may be acceptable in some systems. This can mean that synchronous coordination can be skipped allowing for more performance.

Clients can wait for a check to validated requests/transactions or go ahead without waiting and apologize later if there was a problem. This is a practical system to adopt and mirrors real life business practices. It is more robust and available than distributed transactions.

Coordination can either be avoided entirely or only employed in critical parts of the application where needed.

A trade-off between availability and consistency needs to be made sometimes.

#### Auditing,p. 530.

Data corruption is inevitable sooner or later. We need processes to check the integrity of the data.
Checks reading data to make sure it is there are necessary, and regular restoring of backups is not a bad idea.

ACID does not gaurantee data integrity due to edge cases and blind trust in technology. Regular Auditing is needed to ensure true integrity. Hardware faults or software bugs can and do occur.

Event Sourcing makes auditing easier, p. 531. Establishes provenance of data(origin) and why mutations occurred.

Blockchain and crypto application, p. 532. They are like distributed databases that continually check each other's integrity.

Author is skeptical of Byzantine fault tolerance of these systems, but is interested in the integrity checking aspects.

Distributed ledgers as a way of integrity checking in future data systems is a possibility in the future, P. 533

Privacy is a decision right, it means that a user can decide what they want to keep secret and what they want to reveal publicly.
Privacy policies tend to take this decision and control away from the user and transfer it to the company.

The viewpoint of the data instead of the system has the advantage that the data sees the big picture whereas the machine and organizations that work on the data only see a portion of what happens.
You attach yourself to the data and follow it through the system/operation.

#### Dfds consist of data sources/sinks, processes (bubbles), data flows and files. P. 51.

Processes are named based on the data that moves into and out of them "transform y's to z's".  
Instead of naming data flows based on processes "stuff generated by p1 for the use of p2".

Data flow: a pipeline through which packets of information of known composition flow. A packet can include more than one piece of information that travels together.

Having trouble naming a data flow pipeline is feedback on how effectively you're breaking down components of the system in to parts. You should have interfaces that are nameable, otherwise it is likely that the data flow you are trying to name is not a data flow at all.

#### Naming conventions: p. 54

No two data flows are named the same.
Names can reflect what we know about the data.

Data flows should not represent methods or operations like "get-data".  
Activators of a process are not data flow. Ex. On p. 54-55, day of week.

Flow control definitions are deferred as long as possible since they are procedural and do not contribute to the big picture.

Processes: well chosen processes to put in the dfd will always have the characteristic of being completely named in terms of their inputs and outputs (they are transformations).
A transformation of incoming data flows into outgoing data flows.

A file: temporary repository for data. Ex, databases qualify as files on dfd.

Only net flow is shown on the dfd. If input to a process is required only to n be able to do output, then net flow is out and only that is shown, not the data flow of input to the process. P. 58.
