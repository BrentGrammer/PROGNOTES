# Kafka

- https://notes.stephenholiday.com/Kafka.pdf

- Log aggregator
- used for processing huge volume of log data streams. Like a messaging system, Kafka employs a pull-based consumption model that allows an application to consume data at its own rate and rewind the consumption whenever needed.
  - pull based consumption differs from polling in that consumers decide when to pull data and it is not necessarily at a set interval.

## Problems solved

- High throughput needed = allows for batch processing of log messages.
  - Other systems required a message per TCP\IP connection which limited throughput.
  - Sending multiple messages in one call or hop reduces bottleneck
- High latency and throughput allows collection of events and logs in real time (traditionally logs had to be scraped in large quantities at certain times from prod servers.)

### Goal

- goal is to divide the messages stored in the brokers evenly among the consumers, without introducing too much coordination overhead.

### Implementation

- first decision is to make a partition within a topic the smallest
  unit of parallelism. This means that at any given time, all
  messages from one partition are consumed only by a single
  consumer within each consumer group. Had we allowed multiple
  consumers to simultaneously consume a single partition, they
  would have to coordinate who consumes what messages, which
  necessitates locking and state maintenance overhead. In contrast,
  in our design consuming processes only need co-ordinate when
  the consumers rebalance the load, an infrequent event. In order for
  the load to be truly balanced, we require many more partitions in a
  topic than the consumers in each group. We can easily achieve
  this by over partitioning a topic.

  - Consumers "own" specific partitions

- Zookeeper: responsible for the following tasks: (1) detecting the
  addition and the removal of brokers and consumers, (2) triggering
  a rebalance process in each consumer when the above events
  happen, and (3) maintaining the consumption relationship and
  keeping track of the consumed offset of each partition

- When rebalancing, the consumer begins a thread to pull data from each owned partition, starting
  from the offset stored in the offset registry. As messages get
  pulled from a partition, the consumer periodically updates the
  latest consumed offset in the offset registry

### At least once delivery

- Kafka gaurantees at least once delivery but not exactly once delivery
- If consumers do not have a clean shutdown, the consumers that take over their partition may get duplicate messages due to the time the last commit of the offset was made.
- For exactly once delivery apps need to implement their own deduplication logic to gaurantee this (does Kafka Connect take care of this?).
- Ordering of messages is gauranteed within a partition, but not across partitions

### Tradeoffs

- Kafka brokers do not send an ack back to producers/publishers which greatly increases throughput compared to other messaging systems that do this.
  - For many types of log data, it is desirable to trade durability for throughput, as long as the number
    of dropped messages is relatively small.

### Efficiencies

- No ack as mentioned above
- Smaller header info on messages compared to other systems resulting in less storage and fewer bytes needing to be transferred over the wire
- Batching messages greatly increases throughput (say batching 50 instead of sending message 1 at a time) due to the reduced RPC overhead.
