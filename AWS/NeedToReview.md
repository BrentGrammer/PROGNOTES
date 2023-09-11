Which services offer block level storage?
- Instance Store
  - An instance store provides temporary block-level storage for your EC2 instance. This storage is located on disks that are physically attached to the host computer. Instance store is ideal for the temporary storage of information that changes frequently, such as buffers, caches, scratch data, and other temporary content, or for data that is replicated across a fleet of instances, such as a load-balanced pool of web servers. Instance storage is temporary, data is lost if instance experiences failure or is terminated. EC2 instance store cannot be used for file sharing between instances.
- EBS

- Primary benefit of Read replica config for database deployment is SCALABILITY, not AVAILABILITY
  - Multi AZ deployment is for availability, read replicas are not multi region/AZ and all go down if region or server goes.
  - **Cross region Replication is also for DISASTER RECOVERY in addition to scaling horizontally**

- A multi-national corporation wants to get expert professional advice on migrating to AWS and managing their applications on AWS Cloud. Which of the following entities would you recommend for this engagement?
  - ANSEWR: APN Consulting Partner

Which services automatic excryption:
- Opt-in encryption:
  - for EBS volumes
  - S3 Buckets: server side encryption of objects
  - Redshift database
  - RDS database data
  - EFS: encrypt files
- Automatically enabled encryption:
  - 'cloudTrail logs
  - S3 Glacier
  - Storage Gateway

X-Ray is used for debugging across microservices

Beanstalk is a **PaaS** for web

Well architected framework

# Service Health Dashboard 
Which AWS service can be used to subscribe to an RSS feed to be notified of the status of all AWS service interruptions
- Option to subscrie to RSS feed

# what does security in the cloud vs. security of the cloud mean in shared responsibility? which one is AWS responsible for?
- AWS is responsible for security OF the cloud, which means AWS is responsible for protecting the infrastructure that runs all the services offered in the AWS Cloud.
- you are responsible for security IN the cloud
- Configuration Managemend is SHARED, not only the customers responsibility
- AWS Shield Standard for common DDoS protection is AWS responsibility and enabled for all customers - Shield Advanced is CUISTOMER's resposibility since it is opt in.

# SSM Session Manager
question:  the best way to provide secure shell access to AWS EC2 instances without opening new ports or using public IP addresses.
- let's you start a secure shell on EC2 and on prem servers without having to open port 22 and use SSH or need keys.
(Instance connect is not right - that is just used to shell into a instance in the AWS console)

# SSM - AWS Systems Manager
- **Hybrid Service** allows you to manage EC2 and on prem systems at scale
- Most important features:
  - **Get operational Insights of resources!**
  - **Automatic patching of all servers for compliance**
  - **Run commands across fleet of all servers**
  - **manage config across all servers**
  - Store param config with SSM Parameter Store
- Works both on Linux and Windows servers
- AWS Systems Manager allows you to centralize operational data from multiple AWS services and automate tasks across your AWS resources. You can create logical groups of resources such as applications, different layers of an application stack, or production versus development environments.

With Systems Manager, you can select a resource group and view its recent API activity, resource configuration changes, related notifications, operational alerts, software inventory, and patch compliance status. You can also take action on each resource group depending on your operational needs. Systems Manager provides a central place to view and manage your AWS resources, so you can have complete visibility and control over your operations.
- Difference from AWS Config: - **Config is a Central tool to manage security across MULTIPLE AWS accounts and automate security checks**


## Usage
- Install SSM Agent onto the systems that runs in the background
- Installed by deefailt on Linux AMI and some Ubuntu AMIs

Replication for RDS databases primary advantage (multi-AZ deploy):
### Replication
- Multi-AZ for high availability
  - Can have triggered Failover DB in different AZ
  - Note: Now Disaster recovery is always associated with a region failover and not AZ failover.  So when you say you are doing a disaster recovery, you are basically switching to another region as the entire primary region is down.
- Multi Region replication is available for READ dbs - for disaster recovery.  Writes still go to the one main database in it's original region
- **Retain metadata of the original objects copied**
  - Can be used if you need to copy data from production to multiple test accounts
- replication is cross region


# architecture models
- **Active-Passive**: 
  - 2 regions with instances in availability zone for each.
  - In one region, the instance is active - users can do reads and writes to it (active)
  - In another region, the instance is a replication of the data read only, but users cannot write to it (passive)
  - Reads are low latency since there are replicas around the world
  - Writes are higher latency since there is only one active instance in a particular region
- **Active-Active**
  - Each instance can take writes and reads
  - difficult to set up and configure
  - DynamoDB Global tables is an example of Active-Active

# Trusted Advisor:
- **Helps you follow best practices when provisioning resources and checks for violations**
- **Detect under-utilized and unnatached resources**
-  AWS Trusted Advisor is an online tool that provides you real-time guidance to help you provision your resources following AWS best practices on cost optimization, security, fault tolerance, service limits, and performance improvement. Whether establishing new workflows, developing applications, or as part of ongoing improvement, recommendations provided by Trusted Advisor regularly help keep your solutions provisioned optimally. All AWS customers get access to the seven core Trusted Advisor checks to help increase the security and performance of the AWS environment. Trusted Advisor cannot be used to migrate to AWS and manage applications on AWS Cloud.
- **Checked for not turning on activity logging using Cloudtrail**
- Different drom Well Architected Tool which is documentation based, Trusted Advisor actually looks at your current AWS resources and infra (Well Architected Tool takes questions and builds canned solutions based on your inputs)

# Concierge Support Team
- Concierge Support Team - The Concierge Support Team are AWS billing and account experts that specialize in working with enterprise accounts. They will quickly and efficiently assist you with your billing and account inquiries. The Concierge Support Team is only available for the Enterprise Support plan. Concierge Support Team cannot help in migrating to AWS and managing applications on AWS Cloud.

# A data analytics company is running a proprietary batch analytics application on AWS and wants to use a storage service which would be accessed by hundreds of EC2 instances simultaneously to append data to existing files. As a Cloud Practitioner, which AWS service would you suggest for this use-case?
- Answer -- EFS: concurrently-accessible storage for up to thousands of Amazon EC2 instances. It is lock storage so it supports appending to files with a file system
- Object storage (S3) does not support file appending


# U2F Security key is pluggable to computer - usb key etc
 
 
# ECS vs. ECR
- ECS is not managed and you can manage underlying servers using your containers (you don't need to have the images on ECR, for example)
  - used to run container applications
  - container management service that makes it easy to run, stop, and manage Docker containers on a cluster. 
- ECR is only for storing
  - cannot run container applications
  - used to store, manage, and deploy Docker container images. Amazon ECR eliminates the need to operate your container repositories. 

# Cloudwatch for storing hybrid logs from instances and on prem servers
- You can use Amazon CloudWatch Logs to monitor, store, and access your log files from Amazon Elastic Compute Cloud (Amazon EC2) instances, AWS CloudTrail, Route 53, and other sources such as on-premises servers.

# Servlerless:
- Serverless is the native architecture of the cloud that enables you to shift more of your operational responsibilities to AWS, increasing your agility and innovation. Serverless allows you to build and run applications and services without thinking about servers. It eliminates infrastructure management tasks such as server or cluster provisioning, patching, operating system maintenance, and capacity provisioning.
- EC2 is NOT serverless
- Fargate and Lambda are serverless examples

# Forecasting Costs
- not Budgets
- AWS Cost Explorer
- AWS Cost Explorer has an easy-to-use interface that lets you visualize, understand, and manage your AWS costs and usage over time. AWS Cost Explorer includes a default report that helps you visualize the costs and usage associated with your top five cost-accruing AWS services, and gives you a detailed breakdown of all services in the table view. The reports let you adjust the time range to view historical data going back up to twelve months to gain an understanding of your cost trends. AWS Cost Explorer also supports forecasting to get a better idea of what your costs and usage may look like in the future so that you can plan.
- **Cost explorer cannot be used to identify underutilized EC2 instancesx**

# Budgets
- Used to send alerts when a threshold for utilization is hit (that you set - it is not forecasting)
- Can allow you to see when your Reserved Instances are under-utilized via alerts based on a threshold

# Pricing Calculator
- CANNOT Forecast, only used to create an estimate based on use case

# Low latency to users in various locations (i.e. gaming and good ux)
- **AWS Local Zones** allow you to use select AWS services, like compute and storage services, closer to more end-users, providing them very low latency access to the applications running locally. AWS Local Zones are also connected to the parent region via Amazon’s redundant and very high bandwidth private network, giving applications running in AWS Local Zones fast, secure, and seamless access to the rest of AWS services.

You should use AWS Local Zones to deploy workloads closer to your end-users for low-latency requirements. AWS Local Zones have their connection to the internet and support AWS Direct Connect, so resources created in the Local Zone can serve local end-users with very low-latency communications.

Various AWS services such as Amazon Elastic Compute Cloud (EC2), Amazon Virtual Private Cloud (VPC), Amazon Elastic Block Store (EBS), Amazon FSx, Amazon Elastic Load Balancing, Amazon EMR, Amazon ElastiCache, and Amazon Relational Database Service (RDS) are available locally in the AWS Local Zones. You can also use services that orchestrate or work with local services such as Amazon EC2 Auto Scaling, Amazon EKS clusters, Amazon ECS clusters, Amazon EC2 Systems Manager, Amazon CloudWatch, AWS CloudTrail, and AWS CloudFormation. AWS Local Zones also provide a high-bandwidth, secure connection to the AWS Region, allowing you to seamlessly connect to the full range of services in the AWS Region through the same APIs and toolsets.
- NOT AWS Edge Locations - An AWS Edge location is a site that CloudFront uses to cache copies of the content for faster delivery to users at any location.
- NOT Wavelength - for 5g and is region based

# EC2 Billing:
- 60 seconds - There is a one-minute minimum charge for Linux based EC2 instances, so this is the correct option.
- Question was if user cutoff instance after 30 seconds

# Which AWS service can help you analyze your infrastructure to identify unattached or underutilized EBS volumes?
- Trusted Advisor (NOT Cloudwatch)

# AWS Acceptable Use Policy
- Document for prohibited uses of web services

# Compute Optimizer
- For services: EC2, ASGs, EBS, Lambda (not EFS)
- **AWS Compute Optimizer does not provide optimization recommendations for S3 and EFS, so these options are incorrect.**
- **optimizes resources including EC2, ASGs and Lambdas**
AWS Compute Optimizer helps you identify the optimal AWS resource configurations, such as Amazon EC2 instance types, Amazon EBS volume configurations, and AWS Lambda function memory sizes, using machine learning to analyze historical utilization metrics. AWS Compute Optimizer delivers recommendations for selected types of EC2 instances, EC2 Auto Scaling groups, EBS volumes, and Lambda functions.

Compute Optimizer calculates an individual performance risk score for each resource dimension of the recommended instance, including CPU, memory, EBS throughput, EBS IOPS, disk throughput, disk throughput, network throughput, and network packets per second (PPS).

AWS Compute Optimizer provides EC2 instance type and size recommendations for EC2 Auto Scaling groups with a fixed group size, meaning desired, minimum, and maximum are all set to the same value and have no scaling policy attached.

AWS Compute Optimizer supports IOPS and throughput recommendations for General Purpose (SSD) (gp3) volumes and IOPS recommendations for Provisioned IOPS (io1 and io2) volumes.

Compute Optimizer helps you optimize two categories of Lambda functions. The first category includes Lambda functions that may be over-provisioned in memory sizes. The second category includes compute-intensive Lambda functions that may benefit from additional CPU power.

## Advantages of Cloud
- stop guessing at capacity
- Increased speed and agility
- NOT trade opex for capex!!

# Region constraints of AMIs
- You must use an AMI from the same region as that of the EC2 instance. The region of the AMI has no bearing on the performance of the EC2 instance
- You can copy an AMI to different regions if needed, but instances a region that need it must have it present in that region

# Quick Starts (use to deploy a popular technology to the cloud quickly)
- NOT CodeDeploy - this is not quick 
- USE AWS Quick Starts references

Quick Starts are built by AWS solutions architects and partners to help you deploy popular technologies on AWS, based on AWS best practices for security and high availability. These accelerators reduce hundreds of manual procedures into just a few steps, so you can build your production environment quickly and start using it immediately.

Each Quick Start includes AWS CloudFormation templates that automate the deployment and a guide that discusses the architecture and provides step-by-step deployment instructions.

# Support Plans
- AWS offers three different support plans to cater to each of its customers - Developer, Business, and Enterprise Support plans. A basic support plan is included for all AWS customers.

- AWS Enterprise Support provides customers with concierge-like service where the main focus is on helping the customer achieve their outcomes and find success in the cloud. With Enterprise Support, you get access to online training with self-paced labs, 24x7 technical support from high-quality engineers, tools and technology to automatically manage the health of your environment, consultative architectural guidance, a designated Technical Account Manager (TAM) to coordinate access to proactive/preventative programs and AWS subject matter experts.
**This one offers online training with labs**

- Developer - AWS recommends Developer Support if you are testing or doing early development on AWS and want the ability to get technical support during business hours as well as general architectural guidance as you build and test.

- Business - AWS recommends Business Support if you have production workloads on AWS and want 24x7 access to technical support and architectural guidance in the context of your specific use-cases.

- Basic - A basic support plan is included for all AWS customers.

- **Business and Enterprise offer programmatic access to AWS Support Center features to create manage and close support cases** NOT developer

# use case for data (ex, thumbnails) that is rarely used but needs to be accessed quickly and readily
- S3 One-Zone Infrequent Access (One-Zone IA
  - **It is cheaper than S3 Standard Infrequent Access**
  - S3 Standard-IA storage class is for data that is accessed less frequently but requires rapid access when needed. S3 Standard-IA matches the high durability, high throughput, and low latency of S3 Standard, with a low per GB storage price and per GB retrieval fee. S3 One Zone-IA costs 20% less than S3 Standard-IA, so this option is incorrect.
- S3 One Zone-IA is for data that is accessed less frequently but requires rapid access when needed. Unlike other S3 Storage Classes which store data in a minimum of three Availability Zones (AZs), S3 One Zone-IA stores data in a single AZ and costs 20% less than S3 Standard-IA. S3 One Zone-IA offers the same high durability, high throughput, and low latency of S3 Standard, with a low per GB storage price and per GB retrieval fee. Although S3 One Zone-IA offers less availability than S3 Standard but that's not an issue for the given use-case since the thumbnails can be regenerated easily.  Used for data that is not critical and may not be available.

As the thumbnails are rarely used but need to be rapidly accessed when required, so S3 One Zone-IA is the best choice for this use-case.

# VPC
- linked to a specific **region** REGION BASED NOT CROSS REGION!! can span all availability zones in one region
- A subnet in a VPC is only for one Availability Zone
- **VPC Endpoint Interface**
  - Privately connect VPC to AWS services (i.e. connect VPC to SQS)
  - **only S3 and DynamoDB support VPC Endpoint Gateway** **All other services support VPC Endpoint Interface!**

# Elastic Map Reduce (EMR) Service
- run hadoop big data clusters

# Amazon Inspector
- Assess **vulnerabilites** and security on EC2 instanes and container clusters
- For assessing security vulnerabilities, use this and NOT Trusted Advisor

# AWS Storage Gateway
- Hybrid cloud solution
- Bridge on prem to S3 data storage on the cloud
- Types: Tape Gateway, Amazon S3 File Gateway, Amazon FSx file Gateway, and Volume Gateway

# Send emails after monitoring a trigger - use SNS not SQS

# SQS for sending messages and decoupling WITHOUT LOSING MESSAGES at any volume or requiring other components to be available** 
- Different from SNS which can lose messages and is pub/sub

# Support plans:
- Developer Account: allows for one contact to open unlimited cases, responses in 12-24 hours
- Business Support Plan: production workloads, 24x7 email chat, 4-24 hours response time, Architectural guidance
- Enterprise: designated Technical Account Managers, Concierge Support Team, 1-4 hours for critical response times, 15 minutes for crticial down systesm

# EBS vs EFS
- EBS
  - One Availability Zone and attached to one instance only
  - Cost: Data Transfer IN is free, charge by volume type and number of IOPs
  - BLOCK Storage, NOT File storage
- EFS
  - **Multi cross AZs, Regions and VPCs and works across many EC2 instances!**
  - Region based service, **NOT GLOBAL** - replication is a new feature which allows for cross region replication of the EFS
  - Can be attached to multiple EC2 instances
  - Can be used with **On premises** as well as instances
  - is a managed NFS (Networking File System)

  # Well Architected Framework
  - Pillars:
    - Operational Excellence
      - Small reversible changes
      - **Anticipate failure**   NOT enable tracability (security pillar)
    - Security
    - Cost Optimization
    - Performance Efficiency: Select right resource types and sizes based on **workload reqs**
    - Sustainability
    - Reliability: 
      - IAM - making sure none has too many rights to bring things down
      - Amazon VPC - Foundation for networking
      - Service Quotas - no service disruptions due to limits - inxrease it or set it not too high and not too low
      - Trusted Advisor - look at **service limits and cost optimization** and other things and get strong foundations over time

# Analytics and SQL queries on S3 data: use Athena

# Security Group and Network Access Control List
- Security Group acts as firewall at the instance level
- Access Control List acts as a firewall at the subnet level

# WAFs can be deployed on services that are used to front web apps
- ALBs, AppSync, CloudFront, API Gateway (NOT Route53!)

# AppSync
- build a backend for your mobile or web app to store and sync data in realtime
- **leverages GraphQL**
- **for storing data for your mobile and web apps using GraphQL**

# Amplify
- Similar to Elastic Beanstalk, but for web **and mobile** projects deployed and created easily in a scalable way

# VPN vs. VPC
- VPC is network segregation in the cloud
- VPN allows you to connect on premise secure connections and client devices to AWS in a private network

# Cloudwatch billing metrics are only available in US-EAST-1

#  Billing - Tags
- Can be used to create Resource Groups

# Security
- NACL (access control lists) 
  - **Stateless** (does not remember retain request knowledge, **INBOUND RULES DO NOT AFFECT OUTBPUND RULES and vice versa**): Return traffic (traffic coming back from the server you sent data to) must be explicitly allowed by the rules
    - Example: By deny rules, you could explicitly deny a certain IP address to establish a inbound connection example: Block IP address 123.201.57.39 from establishing a connection to an EC2 Instance.
    - Netowrk ACL's have ordered number of rules
    - 
- Security Groups
  - **Stateful** 
  - **CANNOT BLOCK SPECIFIC IP - NO DENY RULES, ONLY ALLOW RULES**


  - Amazon Lex is powered by same engine as Alexa - speech recognition and processing. Can be used for **CHAT BOTS**
  - Amazon Kendra and Comprehend are for text and document searching and meaning
    - **Use Kendra for searching documents for business purposes**

  # IAM required fields
  - Effect and Action

  # Cloudwatch logs can be used to centralize logs for both on prem and Ec2 instnaces - You do NOT need Lambda!

  # Billing: To get separate invoices, you need to create SEPARATE ACCOUNTS - each account gets it's own invoice - purpose is to separate costs for record keeping
  - Organizations only makes separate invoices for OUs (i.e. prod and dev) within the SAME account.

  # Organizations benefits
  - To get cost benefit from shared reserved instances, the other account needs to launch their instances in the same Availability Zone

  # Budget types with AWS Budgets:
  - Reservation Budget
  - Usage Budget
  - Cost Budget

  # regional services:
  - Lambda and Rekognition
  - GLOBAL: WAF, Route 53, CloudFront and IAm are NOT regional (they are global)


  ## Security
  - Advanced Shield for Enterprise offers protection against higher fees for DDoS attacks
  - Advanced Shield offers DDoS protection for web apps on **Cloudfront and EC2** - NOT for beanstalk
  - Application Firewall (WAF) can check for SQL code for SQL injection and block all reqs except ones you allow, and detect XSS
  - WAF Can also **inspect Cloudfront distibutions**
  - Shield Advanced can provide protection for web apps running on Route53 and Global Accelerator, EC2, ELB, CloudFront (NOT API Gateway)

  # IAM Access Advisor
  - Show and review permissions (granteed or denied) for a user and when they were last accessed

  # Moving from region to region resources
  - There is no off the shelf solution for moving resources (from Us for ex) to another region (to Europe from U.S. for example)

  # EFS Standard-IA  - reduces cost for files not accessed everyday.
  - has high availability, durability and elasticity
  - use case for audits or historical analysis/backup and recovery
  - saves on storage costs for less frequently accessed files, but maintains availability etc as mentioned above

  # Route53 Active-passive routing
  - Use FAILOVER Routing policy for active-passive setup
  - **Route 53 does NOT provide IP Routing for IP addressses specifically - just domain registration and helath checks/monitoring**

  # connecting many VPCs between departments etc.
  - Use AWS Transit Gateway!
   - Not VPN (connect on prem to cloud via tunnel, not used for internal VPCs) or VPC peering (too complicated to connect all since it is not transitive) 

  # Site to Site VPN components:
  - Virtual Private Gateway -AWS side
  - Customer Gateway - company side

  # Determine Underutilized resources:
  - Cost Explorer
  - Trusted Advisor
    (NOT Cost and Usage Reports - this only displays reports with no under utilization analysis)

  # Device Farm
  - Used to test across all different devices (mobile, desktop, etc.)
  - Test against browsers

# Reserved Instance Pricing
- Available for **RDS, DynamoDB and EC2 services** (not S3)

# S3 pricing:
- No retrieval costs: S3 Intelligent Tiering
- Offers Lifecycle storage to optimize costs
- **Data transfer IN is free**
- **Data transfered out to SAME REGION as bucket EC2 instance is FREE** Region bound!! 

# S3
- **Stores data in a flat and non-heirarchical structure!**
- No mimimum storage duration fee for S3 Standard

# Disaster REcovery strategies 
- Cheapest is Backup and Restore strategy, also has higher recovery time objective and recovery point objective
- Warm Standby - replicates data from Primary region to the recovery region.  The Recovery region runs at below prod capacity but is available to take requests and handle traffic  in the case of a disaster
- Pilot Light - similar to warm standby, but additional steps are needed to allow the Recovery region to accept requests - it sits idle, but this can be done quickly (like lighting a pilot light for a fireplace)
- 

# Load Balancer types:
- Application Load Balancer - for applications on the web - Layer 7 HTTP HTTPS
  - Can be used to create single address DNS domain for multiple instances (i.e. server replicas)
- Network Load Balancer - High Performance balancer - gaming, millions of requests etc.  Allows for TCP - Layer 4


# Global Accelerator
- good for non-HTTP use cases
- Provides static IP adddr that act as fixed entry points to your application. Eliminates having to manage different IPs across regions
- apps over TCP/UDP get perf improvement - proxies packets at the edge to multi region apps (cross region)
- Use casese are Gaming, IoT, Voice over IP, and requiring static IPs

# AWS Artifact
- central resource for compliance related info for your org and AWS compliance proof and reports.  
- on demand axes to security compliance reports and online agreements
- **PCI reports**, Seervice Organization Control reports, 
- Free portal for this info (not a service)

# Cloudwatch
- Can use Cloudwatch to set **alarms** for estimated charges.
  - Cost Explorer CANNOT set billing alarms
- **App performance and Utilization monitoring** NOT API Access or perf/availability

  # XRay Tracing
- Solves difficulty of seeing logs for debugging and testing/analyzing production and across multiple distributed services
- Get a visual analysis of your applications
  - **Distributed Tracing**
  - **Have and see a Service Graph of traces**
  - **Toubleshooting**

  # MAcie
  - Machine Learning to protect and detect sensitive data

  # AWS GLue
  - prepare data for analytics

  # Elasticache
  - can be used to reduce load on  databases by providing cached results to be served so traffic doesn't always go to the database

  # Fault injection Simulator
  - Used in Chaos engineering to run fault injection experiements (sudden increase in CPU or memory consumption etc to see how system responds)
  - Easily generate disruptions to test your system

  # Cloud development kit allows you to define infra with your own language
  - Cloud formation does not allow this and is yaml only

  # SNOWMOBILE IS FOR PETABYTES OF DATA

  # DataSync is for copying Terabytes of data between storage services
    - **accelerates data transfer as well**
    - **AUTOMATE data transfers from on prem to AWS**

    **ELB advantages are Fault Tolerance and High Availability**

    # AGILITY: reducing time to provision resources by clicking for them to create them - feature of the cloud


    - Set up cost tracking and allocation by department (not invoicing) - use TAGS, NOT creating multiple accounts

    # On prem to AWS VPN service
    - Customer Gateway device (physical) needed on customer/company's side and Virtual Private Gateway needed on AWS side

    # Quantum Ledger Database
    - Review history - immutable and centralized (unlike Blockchain)

# CloudTrail
- **Account specific audit and logs as opposed to Resource Specific (that would be AWS Config)**
- Used to audit history of API/events calls made within your AWS account
- **Can be used for compliance checks as well**
- **Management Events are logged by default**
  - Data (having to do with storage services) and CloudTrail Insights (capture unusual activity) events are charged

# Sumerian
- 3D Appplications - embed scenes

# Outposts
- Add AWS Cloud services on prem for use on prem

# Beanstalk
- **Health Monitoring: remember this for exam**
  - Full suite available within EB service
  - Health agent on each EC2 instance that pushes metrics to CloudWatch.
  - Checks for app health and publishes health events for monitoring to dashboards

  # Workspaces
  - Virtual Desktop available to you (any number of apps through a VDI)
    - different from Appstream which is for a specific app in a browser

  # Savings Plans
  - Compute Savings Plan - flexible, can change instnace families etc.
  - Instance Savings Plans - Have to stick to family of EC2 instances, less flexible