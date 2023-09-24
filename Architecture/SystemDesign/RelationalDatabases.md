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

### DB Index

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
