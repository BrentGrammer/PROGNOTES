# Communication

## Patterns of Application Communication
- Synchronous communication: Application to Application comms, ex. 2 applications talk directly to one another
  - Can be problematic if you get an unexpected s\ike and one of the apps is overwhelmed
- Asynchronous communication: Event based - Application -> Queue -> Application
  - decouples applications and good to avoid unexpected loads on services
    - use SQS: queue model
    - use SNS: pub/sub model
    - use Kinesis: real time data streaming
  - Services can scale independently from application

# Amazon SQS - Simple Queue Service
- Multiple producers can send messages to a queue, and consumers can poll the queue
- Consumers can share the work
- **After consumers read messages from queue and processed, they are deleted**
- Fully managed serverless service **used to decouple applkications**
- Default retention of messges is 4 days - 14 days is max
- unlimited number of messages can be queued
- Low latency - less than 10 ms on publish and receive
- Consumers share work and scale horizontally
- Ex. use case, instances which take requests for video processing are sent top the SQS queue and separate EC2 instances for processing read from it.
  - The Auto Scaling groups for each part are separate and can scale independently

# SNS - Simple Notification Service
- Solves problem of Sending one message to many receivers
  - pub sub where consumers subscribe to a topic
  - Different from SQS where consumers share work, each subscriber gets ALL messages for a topic
- Limit of 12.5 million subscriptions per topic, 100,000 topics limit
- Examples of targets/protocol for subscribers - SQS, Lambda, Kinesis, Emails, SMS n mobile notifications, HTTP endpoints.
- Key terms: **notifications, pub/sub, subscribers**

# Kinesis
- **Real time big data streaming**
- Managed service to collect, process and analyze real time data at any scale
- Don't need to know these:
    - Kinesis data streams: low latency streaming for high scale sources
    - Data Firehose: streams into S3, Redshift, send outputs to destinations for more analysis
    - Kinesis Analytics

# Amazon MQ
- NOTE: SQS and SNS use cloud native propietary protocols
- Traditional apps use open protocols (MQTT, AMQT, STOMP, Openwire, WSS)
- **Used for companies that have to do migrations to the cloud and they use open protocols, so it avoids re-engineering with SQS and SNS so they can continue to use these open protocols**
- Managed Apache ActiveMQ which has the open protocols enabled by default
- Does NOT scale as much as SQS/SNS
-   Runs on a dedicated machine (NOT serverless)
- Has queue and topic features (similar to SQS/SNS)
