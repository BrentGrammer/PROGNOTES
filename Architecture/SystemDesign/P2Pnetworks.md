# Peer to Peer Networks

- Useful in scenarios where you need to deploy/transfer large files to thousands of machines at once.

## What is a Peer network?

- Group of machines (peers) in a network that hold chunks of some complete data.
- The peers each get the missing chunks from each other and make the chunks they have accessible to other peers.
- Chunks are numbered so peers can know how to put them together to make a complete piece of data/ complete file.

### Peer Discovery and Peer Selection

- The ways that peers know what peers to communicate with next (to get or give data)
- Tracker: This can be accomplished with a machine that orchestrates how peers communicate.
  - While peers are communicating with each other they will be checking in the central database or machine
  - The machine is known as a Tracker.
- Gossip or Epidemic protocol: Instead of a central tracker, the peers orchestrate between themselves (check what chunk they need and tell the peer they don't have this other peers chunk so they should go there next etc. - they "gossip" about what's going on to each other)
  - Every peer has information about what peer carries which chunk
  - They carry mappings that map certain peers to certain chunks (i.e. {IpAddr: ChunkNumber} for themselves and other peers)
  - this is a **DHT** A Distributed Hash Table
    - Holds info on what peers hold what pieces of data

### Example of p2p networks:
- Kraken - used at Uber