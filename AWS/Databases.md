Advantages of NoSQL over Relational:
- Scalable - easier to scale out than Relational
- Flexible schema
- performance optimized for specific data type

# Shared Responsibility
AWS:
- Database Operating System patching
- Availablility


# Services

# Relational DB Services:

## RDS Relational Database Service
- NOTE: You  CANNOT ssh into your RDS database instance
- Can take snapshots to use to create a bigger database or copy them into another region to restore into that region database.
- Used for OLTP processing (not OLAP)
- *Not serverless

### Replication
- Up to 5 read replicas
- Writes only go to Main DB, not replicas
- Multi-AZ for high availability
  - Can have triggered Failover DB in different AZ
  - Note: Now Disaster recovery is always associated with a region failover and not AZ failover.  So when you say you are doing a disaster recovery, you are basically switching to another region as the entire primary region is down.
- Multi Region replication is available for READ dbs - for disaster recovery.  Writes still go to the one main database in it's original region

## Amazon Aurora
- proprietary - not available outside of AWS
- Supports PostgreSQL and MySQL as Aurora DBs
- Cloud optimized - 5x performance improvement for MySQL from RDS and 3x improvement over PostGRES in RDS
- Storage grows in 10GB increments up to 64 TB
- Costs 20% more than RDS and not in free tier, but is more efficient
- *Not necessarily serverless

# ElastiCache
- IN MEMORY Database (managed Redis or memcached)
- Useful to reduce load on main database using a cache for frequent and identical read requests


# DynamoDB
- NoSQL service
- key/value database
  - Records have a Partition Key and a Sort Key
- offers replication across 3 AZs
- Serverless DB - you don't need to provision instances or servers like for RDS and Elasticache Services
- Fast performance, 100s TB of data and trillions of rows
- **Single Digit millisecond low latency** retreival
- Low cost with auto scaling capqabilities
- Standard and Infrequent Access Table Classes offered`

## DAX - DynamoDB Accelerator
- Cache specifically for DynamoDB, not like Elasticache
- Cache frequently read objects
- Use DAX with DynamoDB over ElastiCache

## Global Tables
- Low latency read/write replicas available in multiple regions to serve clients closest to them.
  - Active-Active replication

# Redshift - used for data analytics and warehousing
- Postgres based
- OLAP (Analytics and data warehousing) processing, NOT OLTP like RDS
- load data every hour, not every second
- 10x better performance than other data warehouses, scales to PBs of data
- **columnar storage** instead of row based
- MPP - massively parallel Query execution
- Pay as you go based on instances provisioned
- Can integrate with Quicksight or Tableau

# Amaxon EMR (Elastic Map Reduce)
- Elastic MapReduce
- Not really a database, but is used to create Hadoop clusers for Big Data Analytics
  - Hadoop is open source that enables multiple servers to be clustered to work on data at the same time.
- Takes care of provisioning up to hundreds of EC2 instances and configuring them for joint data analytics.
- Auto scales and integrated with SPOT instances
- USE CASES: data processing, machine learning, web indexing, big data

# Amazon Athena
- *ALWAYS SERVERLESS
- Serverless SQL query service to run analytics on S3 data
- Uses SQL 
- Can use reporting such as Amazon Quicksight 
- Price is $5 per TB of data scanned

# Amazon QuickSight 
- Allows you to create dashboards so you can visually represent data insights from databases
- Used for busdiness analytics and insights
- can integrate with many different databases

# DocumentDB
- NoSQL Database AWS version of MongoDB

# Neptune
- managed graph database
- good for graph datasets like social networks
- available across 3 AZs
- good for wiki knowledge bases, recommendation engines, fraud detection and social networking

# QLDB - Quantum Ledger Database
- Useful for recording finfancial transactions in a ledger - since they can't be modified
- Serverless, managed, replication across 3 AZs
- Used to review history of all changes made to your application over time
- Immutable - no entry can be removed or modified, cryptographically verifiable
- Different from Amazon Managed Blockchain - is not decentralized.

# Amazon Managed Blockchain
- decentralized 
- can join public blockchain or create your own network
  - **Hyperledger Fabric and Ethereum compatible**

  # AWS Glue
  - Managed extract, transform and load (ETL) service
  - Useful for transforming and preparing data for analytics
  - serverless service - you just define transformations and preparations and you're done - no need to make a server for the operation etc.
    - After transforming Glue can forward the prepared data to your data store etc.
  - Glue Data Catalog: catalog of datasets in AWS infrastructure
    - has info that can be used by Athena Redshift etc to build schemas for the data.

# DMS - Database Migration Service
- Quickly secure and migrate databases to AWS
- Self healing and resilient
- Source database remains available during the migration
- supports homogeneous (Oracle to Oracle for ex) or heterogeneous migrations (SQL Server to Aurora) 
  - it is smart enough to know how to convert source to target


  # SUMMARY

  - OLTP Uses: RDS and Aurora (SQL)
  - OLAP uses (Data warehousing): Redshift (SQL)
  - Hadoop?: use EMR service
  - Query data on S3: Athena
  - Aurora: SQL capabilities but NOT necessarily serverless
  - AZ Deploments: for HIGH AVAILABILITY
  - Region Deployments: for Disaster Recovery
  - Read Replicas: for Scalability
  