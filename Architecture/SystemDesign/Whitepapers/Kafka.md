# Kafka

- https://notes.stephenholiday.com/Kafka.pdf

- Log aggregator

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