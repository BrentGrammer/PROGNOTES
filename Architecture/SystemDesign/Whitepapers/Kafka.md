# Kafka

- https://notes.stephenholiday.com/Kafka.pdf

- Log aggregator
- used for processing huge volume of log data streams. Like a messaging system, Kafka employs a pull-based consumption model that allows an application to consume data at its own rate and rewind the consumption whenever needed.
  - pull based consumption differs from polling in that consumers decide when to pull data and it is not necessarily at a set interval.
- Primarily used in Microservices architectures and streaming data pipelines.

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

# Serialization

- Tranforming data into bytes or strings for sending to other services on other machines.

  - When recieved, the reciever de-serializes the data.

- Most popular with Kafka: Avro, JSON, Protobuf, Thrift
  - Note: JSON is not recommended if you need high throughput. (couple hundred messages per minute is fine, otherwise choose more efficient formats)
- By default, Kafka uses StringSerializer which uses UTF-8

### Schema-IDL

- Used by Avro, Protobuf and Thrift
- **If data does not match schema defined, the serialization process will fail.**
- Enables fine grained control of data structure and establishment of contracts to describe data.

## AVRO

- Binary data that is not human readable.
  - Binary data is more compact than string format like JSON for example.
  - The result of serialization using Avro is a series of bytes
- Uses a JSON formatted schema.
- Has first class support with languages like Java using a Schema Registry
- Natively supports Schema-IDL (Good for data evolution at high pace)
- Uses UTF-8 to encode strings
- Can serialize simple and complex data types.
- Language agnostic

### Types supported

- Primitve: null, boolean, int, long, float, double, string, bytes
- Complex: record, enums, arrays, maps, union (combo of multiple types - i.e. val can be either null or int- used for optional fields), fixed (hashes, fixed known size etc.)

Examples:

- Enum

```avro
"fields": [
  {
    "name": "dayOfWeek",
    "type": "enum",
    "symbols": ["MON","TUES","WED","TH","FRI","SAT","SUN"]
  }
]
```

- Union (for optional vals)

```avro
{
  "fields": [
    {
      "name": "middlename",
      "type": ["null","string"]
    }
  ]
}
```

- Fixed (i.e. for md5 data of 16 bytes)

```avro
"fields": [
  {
    "name": "md5",
    "type": "fixed",
    "size": 16
  }
]
```

- Array

```avro
{
  "fields": [
    {
      "name": "weatherDetailsList",
      "type": {
        "type": "array",
        "items": {
          "name": "weatherDetails",
          "type": "WeatherDetails" # a complex record type extracted in another file
        }
      }
    }
  ]
}
```

### Dealing with complex schemas

- For nested records, etc. you can extract parts into their own schema `.avsc` file and reference them by name
- Make sure to make the namespace of the nested extracted record the same as the namespace of the parent schema it is used in!

```avro
# in Main.avsc
{
  "name": "Main",
  "namespace": "com.some.namespace.same.as.parent",
  "type": "record",
  "fields": [
    {
      "name": "temp",
      "type": "float"
    },
    {
      "name": "pressure",
      "type": "int"
    }
  ]
}
```

```avro
# in parent avsc file to use it
{
  "name": "Weather",
  "namespace": "com.some.namespace",
  "type": "record",
  "fields": [
    {
      "name": "id",
      "type": "long"
    },
    {
      "name": "main",
      "type": "Main" # <-- use the name of the extracted schema here!
    }
  ]
}
```

### Schema Registry

- Each producer and consumer potentially have a different schema they agree on.
- A Schema Registry is used as a schema repository to store all the schemas in a centralized location.
- Should create schema repositories and not embed them into applications.
  - Create `.avsc` files containing the schema for each topic (i.e. in a `schemas/src/main/avro` folder)
  - Use the name of the record and avsc extension: Ex: `Command.avsc`
  ```avro
  {
    "name": "TopicName",
    "namespace": "com.somedomain.avro.somenamespace",
    "type": "record",
    "fields": [
      {
        "name": "command",
        "type": "string"
      }
    ]
  }
  ```
  - `name`: Add a name for the schema to identify it
  - `namespace`: Optional. will add more structure and recommended to add and use java naming conventions for namespaces.
  - `type`: Usually "record" is a good complex type to use.
  - `fields`: composed of primitives (its possible to nest records)
  - You can generate schema classes or language files i.e. java classes with the tooling. You can use these to build messages for example with a builder pattern.
- Create the schema by cd'ing into the schemas folder and running `mvn install` after creating the avsc file.

## Kafka Docker setup

- See [video](https://app.pluralsight.com/ilx/video-courses/577e5197-1135-4243-acf8-5784459c459c/abe27065-9bc4-4f80-9e43-5e8b0c9825ff/4fa3460e-f26a-4841-82f0-9bf675614861)
- Messages are persisted in log files and can be found at: `/var/lib/kafka/data`

### With Avro

- A broker is run in a schema-registry container and no longer in its own docker container.
- The producer, for example becomes a `kafka-avro-console-producer` instead of the regular `kafka-console-producer`
- a `value.schema` property needs to be specified and point to your avro schema for messages in that topic.

## Schema Registry

- Holds reference to schemas (with a numbered id)
- Confluent library with license to use unless creating a competing SaaS product
- Use KafkaAvroSerializer in the producer and KafkaAvroDeSerializer in the client.
  - These are classes/packages maintained by Confluent
  - Note: to use specific types and classes (get an error about `GenericData$Record cannot be cast...`) use the SPECIFIC_AVRO_URL_CONFIG property set to true (see [video](https://app.pluralsight.com/ilx/video-courses/577e5197-1135-4243-acf8-5784459c459c/6cff53d8-c901-4d2c-8598-905d14513f11/449d3be0-d100-4b8b-8416-726f5949b887) at timestamp 5:15)
- Uses producer to persist schemas and consumer to retrieve them.
  - The topic `__schemas` has the schemas

### Communicate with Schema Registry via HTTP

- `http://localhost:8081/subjects/`: see what schemas are registered.
  - 2 subjects are created per topic, one for the key and one for the value
  - default behavior of naming subjects are to add a suffix ("value"or "key") to the topic - i.e. `weather-topic-value`
  - To create the subjects, you need to produce and consume one or more messages setup with the avro schema/serializer/deserializer
  - Hitting this endpoint will show registered schema subjects (should have key and value per topic for example): (sr = schema registry)
    ```json
    [
      "weather-sr-value",
      "weather-sr-key",
      "city-weather-sr-key",
      "city-weather-sr-value"
    ]
    ```

### Record Name Strategy

- Naming the subject
- topic Name Strategy: name of topic and add a suffix:
  - {topicname}-key
  - {topicname}-value
  - This is the default subject name strategy
  - unique Subject/Topic (unlike Record Name Strategy)
  - Forces one record type per topic (handy when we want to produce the same data in a single topic)
- Record Name Strategy: The name for the key and the value will be represented by the fully qualified schema name
  - Ex: `com.pluralsight.avro.weather.city`
- Topic Record Name Strategy: combines topic name with schema name to get a subject name.
  - unique Subject/Topic (unlike Record Name Strategy)

### Confluent Wire Format

- A serialized avro file using KafkaAvroSerializer has 5 extra bytes prefixing the data with metadata.
  - A normal avro serialized file just has the data in bytes with no prefix
- You need to handle this if using tools like Java Spark with Kafka Avro Serializer.
- [video](https://app.pluralsight.com/ilx/video-courses/577e5197-1135-4243-acf8-5784459c459c/6cff53d8-c901-4d2c-8598-905d14513f11/0973956d-1a88-4211-9293-4953b9e26af9)
