# RDS (Relational Database Service)

- NOT A DBaaS (Database as a service)
  - In a DBaaS you pay for a database
- It is also NOT AWS Aurora (a custom database engine created by AWS with compatibility with some existing engines)

### A DB Server as a Service

- It is a Managed Database SERVER as a Service
  - You don't get a database with RDS, you get a Database Server
  - You can have multiple databases on this server
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
