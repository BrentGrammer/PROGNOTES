# Relational DB

- Data has a strict imposed tabular structure (tables/relations)
- In contrast to nonrelational dbs where data does not have a strict structure/schema imposed on it.

### Reasons for SQL vs. NoSQL Dbs

- If you need complex querying capability (use relational over NoSQL)

### ACID

- Atomicity - transactions of multiple operations are considered a unit and they either all succeed or all fail.
- Consistency: Any transaction conforms to all rules in the db. Any future transaction is going to take into account any past transaction. (no stale state in db)
- Isolation: Multiple transactions can occur at the same time, but they will be executed as if they were put in a queue as if done sequentially
- Durability: Effects of transactions that are successful are permanent. Data is stored on disk for example.

### Transactions

- Transactions are Atomic and will be run sequentially even if they are initiated concurrently.
  Ex:
- TRANSACTION A Begin
- TRANSACTION B Begin
  - TRANSACTION A Update
    - TRANSACTION B Update (Hangs and waits for Transaction A)
      - TRANSACTION A Commit
        - TRANSACTION B resumes (to pick up new update)
          - TRANSACTION B COMMIT

### Indexing

- Some data requires linear time operation searches. This will be slow if on a big set of data over and over again.
- Index allows you to create a auxillery data structure (like another table) optimized for searching on a specific column.
- Example: index would create structure with sorted order of data that points to the row for that data.
- Indexes are ordered to make them easy to search and then have pointers to the actual data.
- TRADEOFF:
  - Takes more memory space
  - Whatever you write in the database, you also have to write in the index. Writes are a little bit slower
  - Read ops will be a lot faster though
- ex: `CREATE INDEX large_table_random_int_idx ON large_table(random_int);`
  - Query on the table: `SELECT * FROM large_table ORDER BY random_int DESC LIMIT 10`;
  - The large table for example would have millions of entries for the random_int col. The ordering and scanning of the table entries would take a long time without an index.
- Typically you create an index when you first define your Table. 
- Btree structure under the hood - fat tree that is shorter, so less steps to get to a value

## SQL vs. NOSQL

### NoSQL

- system will be read-heavy, NoSQL is a suitable choice for storing data.
  - MongoDB is good choice for fast reads. Other NoSQL databases like Cassandra, Riak, and DynamoDB need read-repair during the reading stage and hence provide slower reads to write performance.
- Flexible schema
- Not highly relational data (no complex queries needed)

### SQL

- Complex queries will be needed
- Relational data
- Strong schema requirements

## ElasticSearch

- Elasticsearch is a standalone database. Its main use case is for searching text and text and/number related queries such as aggregations. Generally, it's not recommended to use Elasticsearch as the main database, as some operations such as indexing (inserting values) are more expensive compared to other databases.

You can use Elasticsearch along with any other database such as MongoDB or MySQL, where the other databases can act as the primary database, and you can sync Elasticsearch with your primary database for the "searchable" parts of the data.

- see https://www.elastic.co/blog/found-elasticsearch-as-nosql
- Use Cases: https://bigdataboutique.com/blog/using-elasticsearch-or-opensearch-as-your-primary-datastore-1e5178

## NoSQL

## Key Value Stores

- fast lookups, lower latency
- good for caches and configuration parameters
- dynamoDB, Redis, Zookeeper, etc. are examples

### Different types of key value stores

- Some write data to disk to persist if the kv store crashes
- Other ones write only to memory (Redis is in memory)
  - In memory is acceptable for caching since you don't lose actual data, just the cache
- Strong and Eventual consistency as well

## ElasticSearch

- NoSQL
- Optimized for text searching
- Append only favoring database
  - Not ideal for frequent deletes or updates
- Not Transactional - often used with a ACID compliant Source of Truth or gauranteed consistency like another database - PostgreSQL for example.
- OLAP database (not OLTP)
- Distributed, async and concurrent database - favors speed and efficiency over correctness (see lack of guarantees above)
- Ideal for querying for aggregations over data, or sorting by Document Rank (favoring certain documents in a query over others based on same criteria)
  - less suitable for operations requiring frequent access to the entire dataset, or very large results sets (let's say over 100-200 results per query).
  - Not great for exporting data, but possible
- Schema changes can be tricky - you can add fields, but if you need to backfill them or remove/alter fields you must re-index all the data (time consuming).
  - Creating new indices to act as a view on top of ES with another database makes this less painful.
- Make sure to have a data retention policy and delete old/whatever data to cut costs in storage (or store the old data in glacier storage etc. that's cheap)

### Suitable Use Cases

- Logs, IoT Events, Metrics - append only data streams
- Kafka recommended as a gateway to make writes predictable and at a rate that won't overwhelm ES cluster.
- Do NOT use ES for:
  - systems requiring transactional gaurantees - i.e. Financial or concurrent systems with strict accuracy requirements
  - High frequency write scenarios - in ES last write wins, so this could be problematic with race conditions etc.
- For those looking for highly performant analytics engines for write-heavy workloads, it’s a good choice.
