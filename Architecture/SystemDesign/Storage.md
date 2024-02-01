# Storage

## Databases

- Database is just a server. A computer/machine.

### Persistence

- Persistence through a power outage etc. is not gauranteed with a database.
- If data is written to Disk, then the data will persist even if the database server goes down. (barring catastrophic machine failure
- If data is just in memory when server goes down, then the data is lost (i.e. when data is being put in a hash table or array etc. before written to disk.)

## Specialized Storage

## Blob Store

- Stores Binary Large Objects (Blob)
  - Really refers to any arbitrary piece of unstructured data
    - video files, image files, large text files, a binary/compiled code, etc.
  - Data that is not tabular
- Blob stores specialize in storing massive amounts of unstructured data.
- Complicated to implement - almost always you will rely on an enterprise solution already built
- Access to blobs are via a key (though not the same as a key value store. optimized differently.)

### Common Blob stores:

- S3 (AWS)
- GCS (Google Cloud Storage)
- Azure Blob Storage

## Time Series DB

- Specialized for storing time series data (large amounts of data relevant to time, i.e. events at a given time every second, every millisecond etc.)
  - Useful for getting rolling averages, aggregating data bw two time periods, etc.
- Less commonly used, don't need to dig deep into them, just mention them for things like logging.

### Common use cases:

- Often used for monitoring/logging purposes
- IoT systems can use Time Series DB (lots of devices sending telemetry data etc.)
- Stock prices that change frequently every second etc.

### Common Time Series DB

- InfluxDB
- Prometheus

## Graph Databases

- Useful for data with a lot of individual data point relationships within the dataset.
- Built on top of a graph data model.
- The relationship of individual data points is primary in Graph dbs, whereas in Relational databases it is more just implied.
- Useful in social networks with highly interrelated data.

### Common Graph DBs

- Neo4j
