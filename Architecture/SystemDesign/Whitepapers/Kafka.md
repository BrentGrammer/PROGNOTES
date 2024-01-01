# Kafka

- https://notes.stephenholiday.com/Kafka.pdf

- Log aggregator

## Problems solved

- High throughput needed = allows for batch processing of log messages.
  - Other systems required a message per TCP\IP connection which limited throughput.
  - Sending multiple messages in one call or hop reduces bottleneck
- High latency and throughput allows collection of events and logs in real time (traditionally logs had to be scraped in large quantities at certain times from prod servers.)

left off on page 4 