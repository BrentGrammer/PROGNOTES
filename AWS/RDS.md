# RDS (Relational Database Service)

- NOT A DBaaS (Database as a service)
  - In a DBaaS you pay for a database
- It is also NOT AWS Aurora (a custom database engine created by AWS with compatibility with some existing engines)

### A DB Server as a Service

- It is a Managed Database SERVER as a Service
  - You don't get a database with RDS, you get a Database Server
  - You can have multiple databases on this server (all need to be of the same engine - only one engine supported per instance)
  - No access to the OS or SSH access (RDS Custom gives you some low level access)
- Managed Database Server so you do not have to manage hardware or maintenance of the DB Engine
- Offers a range of Database Engines to use:
  - MySQL, MariaDB, PostgreSQL, Oracle and Microsoft SQL

### RDS Architecture

- Not a public service (like S3 or DynamoDB)
- runs within a VPC and operates on subnets in a specific AWS region
- Need an **RDS Subnet Group** - create a list of subnets that RDS instances can run on
  - When launching an RDS instance you need to select a RDS Subnet Group to use
  - The subnets can be private or public
  - If in public subnets, you should NEVER make the RDS instances accessible from the public internet by giving them public IP addresses - very insecure and bad practice
- RDS instances only can be connected to within the VPC or via VPNs/DirectConnect from on-premise networks
- Best practice is generally one DB subnet group for one RDS deployment
- \*Every RDS instance has its own dedicated storage provided by EBS
- If you have replicas, you'd have one RDS instance in subnet group that spans across AZs in the same region and have one database (primary) in one AZ and another database (standby) in another AZ within the subnet group.
  - Read replicas (asynchronous replication) span across to other regions
- RDS Backups are stored to S3 (the bucket is AWS managed so you cannot see it in your own account)
  - Using backups in Multi-AZ mode means the backups occur from the standby databases, not primary - so no performance impact

### Costs

- Not billed based on usage, billed for resource allocation
- Instance size and type - larger is more expensive, billed per second
- Multi AZ or not - multi AZ has more cost depending on the architecture
- Monthly fee for storage - more storage or faster types cost more
- Data transfer cost - Per gigabyte of data transferred rate
- Backups and Snapshots - you get the same storage you pay for for the DB instance in snapshot equivalent space for free
  - Ex: if you have 2TB of storage, then you get 2TB worth of snapshots for free, after that Gigabyte per month cost is charged.
- Licensing fees for Commercial DB engines if applicable

### Creating a RDS Instance

[Video demo](https://learn.cantrill.io/courses/1101194/lectures/27894843) at timestamp 5:58

- Need a subnet group first
  - Subnets on the left menu in RDS service page in AWS Console
  - Choose a name, description and VPC
  - Choose the subnets in that VPC - select multiple AZs
- In configuration, for production select Enable storage autoscaling which will increase storage when threshold is met
- Control Access to RDS with allocating a Security Group to the RDS instance
  - Choose Create a new VPC Security Group Option
  - Can leave No Prefence set for the AZ of the Security Group and RDS will choose one
- By default no database is created on a new RDS instance
  - You can select to create and initialize a database in the setup configuration
- [Configuring a Security Group for RDS](https://learn.cantrill.io/courses/1101194/lectures/27894844) at timestamp 1:15
  - You need to add a rule that allows other EC2 instances to connect to the RDS instance

## High Availability with RDS

### Multi-AZ Instance Deployment

- [Video Demo](https://learn.cantrill.io/courses/1101194/lectures/27894848)

  - Multi AZ setup at timestamp 8:05
  - Simulate a AZ failure by going to Actions > Rebooting the instance with the failover option checked at timestamp 12:21
    - This moves the CNAME so it points at the standby instance and the primary instance is restarted

- historically the way to achieve high availability with RDS
- Primary database instance with any databases you create, when enabled it is configured to replicate its data synchronously to a Standby replica database running in another AZ.
- Only ONE standby Repica instance and it cannot be used for reads/writes
- Only works within one region - across AZs in the same region
- Replication is at the storage level
  - Less efficient than the Multi-AZ Cluster architecture
- Replication depends on the database engine you pick
  - MariaDB, MySQL, Oracle, PostgreSQL: Amazon failover
  - Microsoft SQL: SQL server database mirroring, always on availability groups
  - This is abstracted away and you just need to understand that replication is synchronous
- All access to the database is via a CNAME - a DNS name which by default points at the primary instance
  - **You always access the PRIMARY Database instance** - All reads and writes are to/from the primary instance
    - (No access to the standby database)
  - Backups can occur using the Standby (data is copied to S3 buckets across AZs)
- If the primary instance fails, RDS will automatically initiate failover to the Standby database.
  - This can be done manually for testing
  - When automatic failover occurs, the CNAME will change to point at the Standby database instead of the Primary instance.
  - Takes 60-120 seconds for the DNS change to occur in failover (brief outage) - can reduce outage by removing DNS caching in your application/client for this DNS name.
- Reasons to trigger failover: Primary failure, patching software, RDS type changes, AZ outages
  - Ex: you can failover to the standby while doing a patch update to send consumers to the standby, and then flip it back

### Multi-AZ Cluster

- Better than Instance mode and recommended
- Allows a Writer database to replicate to 2 Reader database instances all across different AZs in a region.
- Two readers ONLY - each in different AZs
- The Reader databases are usable (unlike the standby with Multi-AZ Instance deployment above)
  - The Writer/Primary DB can be used for reads and writes, while the Reader database instances can still be used, but only for reads
  - Requires application modification since it cannot use the REaders for writes: configure the app to use the Reader endpoint for reads
  - Allows for scaling workloads unlike with Multi-AZ Instance deployment
- Data sent to the Writer database is viewed as being committed when at least one of the Reader databases confirms that its been written.
- Each database instance has its own local storage
- Accessing the Cluster:
  - Cluster endpoint - similar to a CNAME DNS name that points at the Writer for reads/writes or admin functions
  - Reader endpoint - points at any available readers within the cluster (could possibly include the Writer)
  - Instance endpoint - directly points at an instance, not recommended for use since there is no failover - only used for testing and fault finding
- Runs on faster hardware using Graviton arch and NVME local storage
  - Writes are written with local storage and flushed to EBS - allows for fast local storage performance and resilience with EBS
- Failover is faster than Mutli-AZ Instance mode and can take as little as 35 seconds due to more efficient transaction logs

## Backups and Restores with RDS

[Video](https://learn.cantrill.io/courses/1101194/lectures/27894846)

- [Video Demo creating snapshots](https://learn.cantrill.io/courses/1101194/lectures/27894848)

  - Multi AZ setup at timestamp 8:05
  - Simulate a AZ failure by going to Actions > Rebooting the instance with the failover option checked at timestamp 12:21
    - This moves the CNAME so it points at the standby instance and the primary instance is restarted

- [Video Demo 2](https://learn.cantrill.io/courses/1101194/lectures/27894849)

  - Simulating Data Corruption failures and restoring from a snapshot

- Two types of backups:
  - snapshots
  - Automated Backups
- Both types are stored in S3 with AWS Managed Buckets
  - You can't see the actual buckets in the S3 AWS Console
- Backups are regionally resilient since they reside in S3
  - S3 automatically replicates data in buckets across AZs in that region
- Most backups are taken from the standby RDS instance if you have Multi AZ mode enabled
  - This prevents performance issues in your application due to I/O pauses
  - If you do NOT use Multi AZ you WILL have performance issues since the backups are taken from the only available RDS Instance

### Snapshots

- Not automatic - run explicitly or via scripts or custom app
- Similar to EBS snapshots
- Backups are of the instance (all databases within the instance, not just a single one)
- First snapshot is all data, then subsequent ones are only of data which has changed since the last snapshot
  - Initial snapshot takes a while
- Snapshots do not expire and are not removed when you delete an RDS instance they were taken from
  - You must delete snapshots yourself explicitly to remove them
  - System created (by AWS) snapshots are deleted automatically when the instance is deleted or the retention period expires.
- Can run at various frequencies - once a month, once a week, once per day, once per hour, etc.
- Taking more frequent snapshots minimizes data loss in case of system failures
- Note: restoring a snapshot creates a NEW RDS instance to restore the snapshot to!

### Automated Backups

- Basically automated snapshots
- Occur once per day during a backup window that is defined on the RDS instance
  - AWS can pick at random or you can set a time window explicitly
- First backup is full data from the entire instance, subsequent backups are only the difference in data from the last snapshot
- If using single AZ make sure to schedule backups during periods of little to no use of your app
  - Multi AZ is no problem as the backup occurs from the standby instance
- Every 5 minutes, database transaction logs are written to S3
  - Logs store the operations which change the data (i.e. operations executed on the database)
  - Allows for restoring a database to a point in time with a 5 minute granularity (5 min. recovery point objective can be reached)
- Automated backups are automatically removed and deleted by AWS for periods from 0 to 35 days
  - 0 = automated backups are disabled
  - 35 = maximum time to store a automated backup snapshot
- a backup time of 35 days means you can restore to any point in time over that 35 days using the snapshots/transaction logs
- \*When deleting a RDS instance/database you can choose to retain the automated backups, but **they still expire and are removed after the retention period set**
  - You need to create a **FINAL SNAPSHOT** if you want to retain data permanently after deleting the RDS instance (this snapshot must be manually deleted to be removed)

#### Backing up to another region (automated backups)

- Must be explicitly enabled for automated backups
- You can replicate backups to another region, both snapshots and transaction logs (automated backups)
- Charges apply for the data copy and any storage used in the destination region

### Restoring

- **AWS creates a NEW RDS instance when you restore an automated backup or manual snapshot**
  - When restoring, enter a new database identifier (i.e. `mydatabasename-restore`)
  - After restoring, you need to point your application at the new rds instance database! (see [video](https://learn.cantrill.io/courses/1101194/lectures/27894849) at timestamp 4:43)
- You need to update applications to use the new database endpoint address - it will be different from the existing one
- Restoring a manual snapshot = restoring the database to a specific point in time when the snapshot was created
  - affects the Recover Point Objective (RPO)
- Automated backups are better for RPO since you can restore within 5 minutes of a failure
  - Backups are restored from the closest snapshot and transaction logs are replayed from that point onwards to your chosen time
- Restoring a large database can take a long time and needs to be taken into consideration for disaster recovery etc.
- Using Read Replicas can improve RPO (points more close to the failure point in time)

## Read Replicas

- Read only replicas of your RDS instance
  - Unlike Multi AZ, where you can't use the standby, with Read Replicas your app can access and use them for reads
  - Note: Multi AZ Cluster mode (newer) does allow access to standbys
- Improve Recovery Time Objective as long as data corruption did not occur in a disaster scenario
- Read replicas are SEPERATE from your main database.
  - They have their own unique endpoints and addresses
  - Without app support they are useless - there is no auto failover or access builtin automatically, they just exist
- Kept in sync with Asynchronous replication
  - Asynchronous replication = first data is written to the primary and then written in a seperate operation to the Read
    - With async replication there can be a lag that needs to be accounted for due to the seperate operations to complete
  - In synchronous replication (Multi-AZ), data is written to both the primary and read instance in one transaction or commit
- Can be created in same or other region of the primary database ("cross-region read replicas")
  - Cross Region Read Replicas networking is managed by AWS and is transparent to you and data is fully encrypted in transit

### Benefits of Read Replicas

- Scale out read performance: create 5x read replica instances for your primary and you can scale read performance by 5 times.
- Read Replicas can have their own Read Replicas, but lag starts to become a problem and is a tradeoff
- Improves RPO (point close to failure restores), but NOT RTO (Recovery Time Objective) because restoring snapshots still takes a long time
  - Offer near 0 RPO because the data on the read replicat is synced from the main database instance - low potential for data loss
  - Read replicans CAN improve RTO in cases where you need to failover to a read replica if a primary instance fails - very quick process
- NOTE: Read Replicas only good for RTO recovery time from Failure scenarios, NOT data corruption (the replica will also have the corrupted data)
- Read Replicas can be promoted to be used as a normal RDS instance (not just reads, but writes)
- Globally resilient - you can create cross-region replicas that you can failover to if there is a region wide outage or disaster

# Data Security

## Encryption

### Encryption in Transit

- All Engines in RDS allow for Encryption in transit (SSL/TLS)
- Can be set to be mandatory on a per user basis

### Encrytion at Rest

- Depends on the database engine

#### EBS/KMS encryption at rest

- Standard RDS encryption method
- Supports EBS Volume encryption using KMS
- handled by the RDS Host and EBS storage
  - The RDS database engine does not know about this and thinks its just writing unencrypted data to storage. Data is encrypted by the Host that the RDS instance is running on
  - The database does not need to support native encryption itself
- You need to choose a Customer Master Key (CMK)
  - can use a customer managed CMK
  - Another option is an AWS managed CMK
  - This CMK is used to generated Data Encryption Keys (DEKs) which are used for the actual encryption operations
  - The DEKs are loaded onto the RDS host machines as needed and used to perform the encryption
  - The data is encrypted by the host and then sent to the EBS storage in its encrypted format
- All logs, snapshots, transfers between replicas and storage are encrypted using the same Customer Master Key (CMK)
- **Encryption cannot be removed once it is added**

#### TDE (Transparent Data Encryption)

- MSSQL and RDS Oracle support TDE
  - Oracle supports TDE using CloudHSM (more secure with stronger key controls)
    - CloudHSM managed by you with no key exposure to AWS
- Supported and encryption is handled within the actual database engine (not the host that the instance is running on)
- Useful for less trust environments and demanding regulatory situations since you know data is encrypted as soon as its written by the database engine (no third party handling)

## IAM Authentication for RDS

- Needs to be explicitly enabled on the RDS instance
- Can configure RDS to use IAM user authentication against a database
- On an RDS instance create a local database user account configured to allow authentication using an AWS auth token
- Users or roles have policies attached to them which have a mapping from an AWS identity (user/role) to a local RDS database user
- The policy allows the identities to run a `generate-db-auth-token` operation
  - This generates a token based on the policy attached with a 15 minute validity time
  - The token is used to login to the database user within RDS without a password
- By associating policies with IAM users/roles it can be used to generate this token to login to RDS without using a password
- **This is only for AUTHENTICATION, not AUTHORIZATION**
  - The permissions for the user are still those which are defined on the local database user, not in the policy or on the IAM identity
