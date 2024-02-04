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

# Leader Election

- [video](https://www.algoexpert.io/systems/fundamentals/leader-election)

## Example in a Subscription System

- A system where users have a monthly fee for a subscription to a service.
- You'd have a database to store info about user subscriptions (whether user is currently subscribed, the date of renewal, the price, etc.)
- You'd have a third party service taking care of actually charging the users (paypal, stripe etc.) that needs to communicate with the database to get subscription info
- You might not want the third party service to connect directly to the database (security, etc.) so you'd have a service in the middle of the two.
  - This middle service is in charge of talking to the database to get sub information, and then communicates with the 3rd party payment service and tell them to charge the user.
  - If this single machine service fails then the entire system fails - we need Redundancy of the middle service - so we need multiple servers.

### The Problem

- If we have multiple servers in the middle service between the payment and database services, how do we ensure that the request to tell the 3rd party service to charge a user only happens once and is not duplicated?

### The Solution: Leader Election

- With multiple servers handling logic where you only want something to happen one time, you can have the servers elect a Leader and that Leader service will be the only one executing the action (i.e. a request to the third party system to charge the customer).
  - The Followers: The other servers will just be on standby in case something happens to the leader.

### Difficulty (Consensus)

- The main difficulty in implementing leader election is figuring out how to gain consensus on sharing state/deciding who the leader is among the machines/servers.
- You need to use a Consensus Algorithm to achieve this.
  - these allow for multiple nodes in a cluster to reach consensus on some single data value (for ex., who the leader is in the cluster).
  - Popular Consensus algos are Paxos and Raft
    - very complicated and will not be expected to implement them
- you usually use a third party service that use Paxos or Raft under the hood:
  - Zookeeper
  - Etcd: a key val store that is highly available and strongly consistent (reading and writing to same keyval pair is gauranteed to return the correct value), uses Raft to acheive this.
    - You could store a keyval pair stating who the leader is and because it is strongly consistent, at any given point in time if any machine reads from it, they will get the correct answer to who the current leader is.
    - A leader has a lease that it refreshes say every 5 seconds. if that leader gets disconnected then the lease expires and a new leader is elected.
- These tools allow you to implement leader election in an easier way.
