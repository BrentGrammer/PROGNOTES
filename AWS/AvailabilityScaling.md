# Availability and Scaling

## Global vs. Regional Architecture

- Good to think of architecture and your solutions as have Global components and Regional Components
- Can think of the whole as being systems in different regions that make up the whole

### Global components

- Service Location and Discovery (i.e. mapping a url entered in a browser to a destination)
  - DNS - route53 maps clients to a location
- Content Delivery (CDN) - how data gets to user globally
  - Cloudfront can cache content closer to users
- Global Health Checks and Failover - check on systems and move customers to another region as required

### Regional components

- Regional Entrypoint
- Regional Scaling & Resilience
- Application services and components

## Multi-Tier Architecture

Architectures are built with components from these various Tiers

- **Web Tier**: where clients enter your service - an API Gateway or Application Load Balancer
  - This abstracts the customers from your infracture which means the infra can scale or change without impacting customers
- **Compute Tier**: EC2, Lambda or Containers (ECS) are used by the regional entrypoint to deliver services to customers
- **Storage Tier**: EBS, EFS, S3 (media storage, CloudFront accesses S3 for media storage)
- **Data Tier**: RDS, Aurora, DynamoDB, RedShift (warehousing)
- **Cache Tier**: ElasticCache, DynamoDB Accelerator (DAX)
  - Apps don't directly access the Data Tier, they go through a caching layer to improve performance and reduce costs
  - Reads to databases are minimized, the app consults the cache first and retrieves only on misses
  - Caching is in memory - cheaper and faster than databases
- **Application Services**: Kinesis, Step Functions, SQS, SNS
  - Functionality to apps to send notifications, decouple components using SQS queues etc.

# Elastic Load Balancers

- ELB refers to the whole family of Load Balancers in AWS (3 types - CLB, ALB and NLB)
- Version 1 (Classic Load Balancer - CLB) is old and you should migrate to Version 2 products (prefer usage)
  - Ex: version 2 load balancers do not require separate ssl certs like version 1

## Version 2 Load Balancers

- Faster and support target groups and Rules
- Can use a single version 2 load balancer for multiple things or handle differently based on which customers are using it

### Application Load Balancer (ALB)

- True layer 7 devices
- Support HTTP, HTTPS and web socket protocols
- Useful for scenarios where you're using any of those protocols, web apps etc.

### Network Load Balancers (NLB)

- Supports TCP, TLS (secure version of TCP), UDP protocols
- Use case is for any applications that DON'T use HTTP or HTTPS protocols
- Email servers, SSH servers, a game with a custom protocol

### Configuring a Load Balancer

- Choose between using IPv4 or Dual Stack (use IPv4 and IPv6)
- Choose Availability Zones that will be used
  - choose one subnet in two or more AZs
  - One or more Load Balancer nodes are placed automatically into these subnets
    - **A single Load Balancer is actually multiple nodes into each of the subnets you pick under the hood**
  - Nodes are highly available - if one node fails, it is replaced automatically
  - If load increases, more nodes are created and configured in each of the subnets the ELB operates in
- Created with a single DNS A-Record
  - the A-Record points at all the ELB nodes that are created
  - The DNS name resolves to all of the individual nodes - incoming requests are distributed equally across all the nodes (located in multiple AZs and they scale within the AZs)
- Choose **Internet-facing** or **Internal**
  - controls IP addressing for the ELB nodes
  - **Internet-facing**: nodes are given public and private addresses
    - NOTE: Internet-facing ELBS can connect to both public and private addresses of EC2 instances (the instances it points to DO NOT have to be public!)
  - **Internal**: nodes are ONLY given private addresses.
    - Generally used to separate different tiers of applications - i.e. allow indpendent scaling of web and data tiers, etc.
- Listener Configuration: what protocols and ports will be accepted at the listener/front side of the ELB

### Requirements for deployment of ELBs

- Load Balancers need 8 or more free IP addresses in the subnet they are deployed into.
  - a `/28` subnet which provides 16 minus the 5 reserved by AWS (leaves 11 free), but then there is no room for backend instances...
  - `/27` or larger subnet is the recommended minimum by AWS
