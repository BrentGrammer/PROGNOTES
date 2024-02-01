# Replication

- Main database also writes to a replica
  - Replica must always be up to date with the main database
  - Writes to the main database will take a little bit longer due to having to write to the replica as well
  - If a write to the replica fails, then the original write to the main database also must fail

## Latency improvements

- In addition to providing redundancy and availability, latency can be improved via replication
- You can keep a database in one region and have a replica in a distant region to reduce latency to clients in that area.

### Asynchronous updates

- An alternative way to update the replica is to do it asynchronously. (every 5 minutes, every hour etc.)
- This prevents the overhead of making large trip to update the replica in a distant region.
  - This would mean that the clients in the distant region will not get the updates until the async replication is done.
- This is only acceptable if it is not necessary to have all replicas up to date all the time (without allowing for a delay)

# Shards

- When you have huge amounts of data and it is impractical to replicate it everywhere.
- Instead you can split up/partition the data - this is sharding.
  - Split up the database into a bunch of minidatabases called Shards.
- Shards will usually live on separate machines (not be on the same machine)

## Splitting the data

- In relational databases, one way is to split up chunks of rows in each table and store some chunks in certain shards and other chunks in other shards.
  - Example: Customers table could be split up into customers with names from A-E, F-J, etc.
  - Alternately, if you have a Payments table you might split by regions, so if customer who made payment is from North America, those go to shard #1, if from South America, shard #2 etc.
- You need to decide how to split the data up depending on the nature of the data to avoid hot spots etc.

### Hot Spots

- The potential problem of sharding is if certain shards get a lot more traffic than other shards because of the nature of the data they store. (example, if sharding by customer name in alpha ordered chunks, you'd have a lot less names starting with X Y or Z. This would not be a problem if sharding on username or uuid where the letters are equally probable)
- Use HASHING to combat hot spots.
  - Note that consistent hashing can help with adding a shard, but if a server goes down, then it will not help - you would instead need replicas of each shard that could take over if any go down.
- You will want to use a robust popular hashing function that guarantees uniformity

### Sharding logic in a Reverse Proxy

- You would probably want a reverse proxy that acts on behalf of the shards/database servers that contains the logic for which shard to deal with per requests.
  - The server would be the client in this case and request to write or read data from the database. That request would go to a reverse proxy that then has the job of figuring out which shards to interact with
