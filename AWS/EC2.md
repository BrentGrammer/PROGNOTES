# EC2 - Elastic Cloud Compute

## Architecture

- EC2 Instances are Virtual Machines that run on **EC2 Hosts** - physical hardware machines that AWS manages.
  - Shared Hosts: shared across different AWS customers (NOTE: every customer is isolated from each other)
    - Default kind of EC2 Hosts
  - Dedicated Hosts: One customer pays for the entire host - not shared.
- **Availabilty Zone Resilient** - hosts run inside AZs. If the AZ fails, the Host and instances fail.
  - key: EC2 instances run in one Availability Zone
  - **Very AZ reliant** - everything about a EC2 instance - the host, the networking, the storage is all in the same AZ. \*All resources along with the EC2 instance MUST BE IN THE SAME AZ!
  - For resiliency across AZs, you deploy resources in multiple AZs and use a load balancer to distribute traffic across them all

### Resources for an EC2 Instance

- CPU
- Memory
- Instance Store - storage that is on a specific host. NOTE: If the instance moves off of that host, then the storage is lost.
- Networking:
  - Storage Networking
  - Data Networking
  - When an instance is provisioned into a subnet in a VPC, what happens is a primary Elastic Network Interface is provisioned in the subnet which maps to the actual hardware on the EC2 Host
  - Note: Instances can have multiple network interfaces in different subnets as long as they're in the same availability zone.
- Can connect to remote storage (EBS - Elastic Block Store). EBS runs in one Availability Zone (cannot access multiple EBS across zones)
  - You can allocate EBS Volumes (amount/area of persistent storage) to an EC2 instance in the same AZ.
- Generally instances of the same type (but could be different sizes) share the same host.
  - Hosts are associated with a date, with a certain CPU type and certain generation of hardware
  - It's logical that different types of EC2 instances that use particular features or generations of features will be grouped on the same host.

### Restarting/Stopping Instances

- Restarting EC2 Instances stay on the same EC2 Host machine unless:
  - The host fails or is taken down for maintenace by AWS
  - an instance is STOPPED and then STARTED (not re-started), then it will be relocated to a different host (in the same AZ!!)

### Use Cases for EC2

- Certain vendor requirements for support, need specific OS with specific environment and setup with a traditional application
- **Long-Running Compute capabilities**: Many other services have run time limits for compute, EC2 does not can be dedicated for long running processes and compute requirements.
- Traditional Server Style applications - i.e. a server listening for and handling requests
- Burst loads or steady state loads needed for an application requiring an operating system.
- Good for monolithic applications - Database, middleware components that need to be running on a traditional operating system
- Migrate Application workloads or provisioning a Disaster Recovery Environment
- Generally, EC2 is the default choice for compute requirements - traditional apps, etc.

## Instance types:

[Video](https://learn.cantrill.io/courses/1101194/lectures/27806425)
<br>
[AWS Docs - Instance Types](https://aws.amazon.com/ec2/instance-types/)
<br>
[Most Used Types PNG](./instancetypes.png)
<br>
[Filterable lookup of instance types overview/costs](https://instances.vantage.sh/)

- Different types allocate an amount of CPU, Memory, Local Storage Capacity and Storage type
- Types also change the ratio of those resources (i.e. more CPU vs. memory for compute optimized types)
- Influences the Storage and Network Bandwidth you get (if you use EBS volumes for example you need to make sure you have a type that allows good enough bandwidth over the network)
- System Architecture (ARM, x86) and Vendor(Intel, AMD)

### Five Main Categories of Types

- General Purpose: default workloads, equal resource ratio (use this unless specific reason)
- Compute Optimized: media processing, HPC, Scientific Modelling, gaming, Machine Learning
- Memory Optimized: large in memory datasets used, database workloads
- Accelerated Computing - Hardware GPU, field programmable gate arrays (FPGAs)
- Storage Optimized: high transfer rates or large amounts of I/O operations - high sequential and random IO is best use case

### Type Name Convention for Instance Types

- `R5dn.8xlarge`
  - `R`: Letter at start is instance family - designates type of computing/type of instance
  - `5`: The Generation number - these change as generations are updated (hardware updates, etc.) - always select the most recent generation (unless it is not in your region)
  - `dn`: Additional capabilities - series of letters that denote features available
    - `a`: signifies AMD CPUs
    - `d`: NVME storage
    - `n`: Network Optimized
    - `e`: Extra capacity of RAM or storage, etc.
  - `8xlarge`: Instance size - there are multiple sizes available for a family/generation (indicates how much memory and CPU the instance is allocated)
    - Note: usually better to scale up with larger number of smaller instance sizes due to price

### Most used types

- See [overview](./instancetypes.png)

#### General Purpose (T, A, M types):

- `A1`, `M6g`: ARM based processors are efficient and you can use smaller instances with lower cost and good performance
- `T3`, `T3a`: Burstable instances - normally low levels of CPUs but occasionally need to handle spikes of high CPU (and then return to the low level). A lot cheaper than other types of General Purpose instances
- `M5`, `M5a`, `M5n`: Steady State compute needs - i.e. load stays steady at 60% like for an email server. No bursts needed

#### Compute Optimized (C Type):

- `C5`,`C5n`: Good for general Machine Learning, gaming, scientific modelling

#### Memory Optimized (R type - i.e. Ram):

- `R5`,`R5a`: real-time memory apps, analytics, caches, some db applications
- `X1`,`X1e`: large scale in-memory apps with lowest cost per GB of memory in AWS
- High Memory series, `u-Xtb1`: Highest memory available in AWS

#### Accelerated Computing:

- `z1d`: large memory/CPU with directly connected NVMe storage
- `P3`: Good for parallel processing and machine learning (has GPU)
- `G4`: Good for graphics intensive requirements
- `F1`: FPGA to program hardware for tasks: finance analysis, big data, genomics
- `Inf1`: Machine Learning optimized for voice recongnition, forecasting, recommendation, analysis

#### Storage Optimized:

- `I3/I3en`: High performance SSD (NVMe), analytics, warehousing, NoSQL Databases
- `D2`: Dense Storage - data warehousing, HADOOP, Distributed File Systems, lowest price disk throughput
- `H1`: High throughput, Big Data, Apache Kafka

- As generation number increases, hardware improves
- _Compute Optimized_ are for high compute intensive tasks
  - Have the `c` instance class name
  - machine learning
  - game servers
  - batch processes, high workloads
- _Memory Optimized_
  - `r` series
  - Large data sets in RAM
  - Databases
  - web scale cache stores
  - large unstructured data
- \*Storage Optimized
  - `i` `d` `h1` series
  - Relational nosql databases
  - Redis
  - Cache in memory
  - Data warehouses

## SSH into EC2

- [Video](https://learn.cantrill.io/courses/1101194/lectures/27806428)
- **BAD PRACTICE TO ALLOW ALL IP ADDRESSES IN SECURITY GROUP INBOUND RULES**
  - Use the IP (ip_prefix) value from here for AWS services if needed (i.e. to allow EC2 instance connect): https://ip-ranges.amazonaws.com/ip-ranges.json
- Make sure the security group for the EC2 instance allows your IP address in the inbound rules
  - You can go to Edit inbound rules in the security group > in the Source column dropdown select My IP
- Create a key pair - EC2 > Create Key Pair on left menu > .pem key
  - Download the key to your machine
  - Go to the folder you downloaded the .pem key, chmod to 400 permissions and use the command given in SSH Connect page in AWS console to connect
  - Using this method requires admin and does not scale as every team member needs a copy of this .pem file
- Using EC2 Instance Connect
  - You need to know the user name if using a custom AMI, otherwise it is guessed automatically for connecting
  - More scalable with high number of team members than using the .pem key

<br>
<br>
<br>
<br>
<br>

# From Cloud Practicioner Notes (Old):

- IaaS - Infrastructure as a Service
- Bootstrapping: running commands when a machine starts and boots up
  - Script is run ONCE on machine start
  - Bootstrapping script commands run with root user priveledges
  - EC2 setup - advanced options -> **EC2 User Data** script. Runs on startup of EC2 instance
- By default it is a private service (deployed into a subnet in a VPC in the private zone).
  - If you want to allow public access you need to configure that.
- IaaS - Infrastructure as a Service
- EC2 is AZ Resilient: If an AZ that the EC2 instance is in fails, then the instance will be taken down with it.

### Starting and Stopping an instance

- If stopping and restarting a EC2 instance, the public IP Address can change

# Security

## SECURITY GROUPS

- Security groups determine what is allowed into an EC2 instance
- Security Group acts as firewall at the instance level
- In contrast, Access Control List acts as a firewall at the subnet level
- **Locked to region/VPC and on instances**
  - You need to create a new security group for different regions or VPCs
- Not running on the EC2 instance - they exist outside of the instance
- Governs inbound and outbound traffic
- A firewall on the instance
  - regulate access to ports and IP ranges
- Can reference other security groups
- Best practice: maintain separate security group for SSH access

## Troubleshooting

- If you get a timeout and request hangs it means the security group might have a problem with the rules
  - This means that you probably are missing an inbound rule to allow traffic to your instance
- If you get "Connection Refused" then the security group is probably working and request went through, but application had an error or wasn't launched

# COMMON PORTS

- 22: SSH for Linux instance or SFTP - file upload with SSH
- 21: FTP File transfer
- 443: HTTPS
- 80: Unsecured web
- 3389: RDP (Remote Desktop Protocol) - used to ssh into Windows instance

## SSH into EC2

- ssh -i [keyfile.pem] ec2-user@[publicIP]
- Default user for EC2 instance and Amazon provided AMIs is ec2-user.
  - Check AMI usage instructions if default user is different
- Can also use EC2 Instance Connect in AWS Console.
  - \*\*DO NOT enter your credentials while shelled into instance with `aws configure`
    - anyone else in the account can get those credentials when they shell into it
  - You need to attach a IAM role to the instance to provide credentials and permissions to the EC2 instance in Instance connect
    - In instance page, Actions dropdown -> Security -> Modify IAM Role

## EC2 States

- Running - charged for storage, CPU compute, memory and networking
- Stopped - NOTE: Storage charges are still generated when an instance is stopped!
- Terminated: stops all charges and caution: deletes any storage for it. cannot undo.

## Spend Models

- On Demand
  - useful for unpredictable usage
  - most expensive but no upfront cost
- Reserved
  - 1 and 3 years
  - Discount from on demand, option to pay up front for discount further
  - useful for steady state apps -i.e. a database
  - Convertible reserved allows you to change types and specs with a little less discount
- Savings plans
  - 1 and 3 years, discount based on reservation for usage rate
  - Tied to region
  - allow for predicted use ($10/mo) and anything over is billed at on demand rate
  - Flexible on instance size, OS and Tenancy
- Spot Instances
  - Cheapest option, up to 90% discount from on demand
  - choose a spot price and if it goes over, then you lose the instance
  - less reliable and cheap, useful for resiliant workloads
    - batch jobs, image processing, data analysis, distributed workloads, flexible start and end time jobs
    - **NOT suitable for critical jobs or databases**
- Dedicated Hosts: book an entire physical server
  - Most expensive option
  - useful for compliance regulation requirements, software that has BYOL license requirements
- Dedicated (EC2) Instances: No other customers will share your hardware
  - hardware dedicated to you, but hardware is shared between instances in your account
  - no control over instance placement
  - This means that no other AWS Account will run an instance on the same Host, but other instances (both dedicated and non-dedicated) from the same AWS Account might run on the same Host.
  - Billing is per instance, with a cost of approximately 10% more than the normal instance charge (but no extra charge if it is the largest instance in the family since it requires the whole host anyway).
- Capacity Reservations:
  - reserve capacity in any AZ for a duration.
  - No discounts, need to combine it with another plan to get discounts
  - Charged whether you use it or not (whether you launch instances or not)
  - useful for short term predictable workloads in a specific Availability Zone.

## Shared Resonsibility

- AWS
  - Infrastructure
  - Isolation on phyusical hosts
  - faulty hardware
  - compliance validation
- YOU

  - Applications and internal security
  - Security Groups and correct IAM policies
  - Security of data

  # can use Route53 geolocation routing policy to to block certain geographies.

## Creating an EC2 Instance

### Generate a key pair if needed (for access)

- AWS Console > `EC2` > `Network & Security` on the left > `Key Pairs` > click Create Pair
  - Download the private part of the key pair (only one chance to do this)
- Give pair any name and choose RSA or ED25519 type
- Choose `.pem` (good for modern windows and mac os/linux)
  - ppk is used for older windows or use with Putty
- click Create Key Pair
- You download the private part of the pair and the public pair is stored on the EC2 instance itself.

### Create an instance

- EC2 Dashboard > Launch Instances
- Name the instance: ex: `MyFirstEC2Instance`
- Select the AMI and instance type etc.
- Pick and select the Key Pair that you created for the instance
- You can assign the EC2 to the default or custom VPC and select a subnet if you want as well (Note: this is tied to an AZ).
- Select whether you want to Enable auto assign a public IP (for internet outside access allowed etc.)
- Select to create a security group if needed and name it: i.e. `MyFirstInstanceSG` and put the same for the description
- Storage: selected by default according to the AMI
- When done, click Launch Instance
  - starts in pending state and takes a few minutes to get up and running
  - NOTE: Make sure the status checks have finished (Status Check column) which means the instance is fully ready
    - Should say something like 2/2 and not `Initializing...`

### Connecting to an EC2 Instance

- [video](https://learn.cantrill.io/courses/1101194/lectures/39551633)
- AWS Console > EC2 > Select running instances and the instance > Right click on the instance and click `Connect`
- Select the `SSH Client` tab which gives you info on how to connect
- Use the ssh client on your machine
  - Navigate to the folder location where your .pem keypair is located on your machine
  - Change permissions on the keypair file if you get permission denied (usually on mac or linux) - copy the `chmod` command the SSH Client tab in AWS console tells you to use
    - If using windows need to [use different process](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-to-linux-instance.html#connection-prereqs-private-key)
  - Copy the command in the ssh client tab from the aws console to connect to the EC2 instance via ssh.

### Cleaning up or removing an Instance

- Right click on the instance in the dashboard and click terminate
- Clean up the security Group (in the left menu panel) - select it and click on `Actions` dropdown and select delete security groups.
  - May have to wait until EC2 instance is terminated before this is allowed.

# Network Interfaces

### ENI Elastic Network Interfaces

- EC2 instances always start with at least one ENI - the Primary Network Interface
- Network Interfaces must be in the same AZ (can connect secondary Network Interfaces on different subnets)
- Components such as IP addresses, Security Groups and more look like they're attached to the EC2 instance, but they are actually attached to the Network Interface
  - MAC Address: the hardware address of the interface. Visible to the OS and can be used for things like software licensing
  - Primary IPv4 private address: each network interface has this and it is in the range of the subnet that the interface is created in
    - When selecting a VPC and subnet for an EC2 instance you are actually picking those for the primary network interface
  - 0 or more secondary IP addresses
  - 0 or 1 Public IP address for the interface
  - 1 or more Elastic IP address (1 per private IPv4 address)
    - different from public address where you can only have one
  - 0 or more Ipv6 addresses (all of these are publicly routable, there is no concept of private/public with ipv6)
  - Security Groups can be attached to Network Interface and affects all IP addresses on that interface
  - Source/Destination checks can be enabled/disabled.
    - If enabled, traffic on the interface is discarded if it's not from one of the ip addresses as a source or going to one of the IP addresses on the interface marked as a destination
    - You would disable this if you need the network interface to function as a NAT gateway instance, for example
- Different instance types allow you a different number of secondary network interfaces
  - With secondary interfaces, you can detach them and move them to other EC2 instances (unlike primary interfaces~)

### IP Addresses and DNS

- EC2 Instances (via the Primary Network Interface) are given a primary private IPv4 IP Address and a DNS name associated with it.
  - These never change throughout the instances lifetime
  - Only resolvable insided the same VPC
- Private primary IPv4 address naming convention: `10.16.0.0` translates to `ip-10-16-0-0.ec2.internal`
  - ip-{ipaddr-separated-by-dashes}.ec2.internal
  - can use the private DNS name to get the internal private ip address of an instance in the same VPC
- If configuration is set to assign a public IP address, the primary network interface/ec2 instance will get one
  - This public IP is dynamic and NOT fixed
  - Stopping and Starting an instance will change the public IP address! and so will anything causing an instance to move to another EC2 host
  - stopping de-allocates the address and starting again gets a new address to be allocated for it
  - Restarting/rebooting an instance will not change the public address
- Public Addresses have a DNS name generally in this format: ip `3.87.9.136` translates to `ec2-3-87-9-136.compute-1.amazonaws.com`
  - Inside the VPC: Public DNS name translates to the internal PRIVATE IPv4 address! (remains more stable using the private address instead of the public one)
  - when referenced inside the VPC traffic never leaves the VPC (i.e. it does not go out to the internet gateway and back in)
  - Outside of the VPC: The public DNS always resolves to the public IP address, not the internal one
  - Public addresses are not attached to the network interface/instance - they are associated and handled by the Internet Gateway which handles translation
- The OS of an instance cannot ever see the public IPv4 address. That is handled by NAT via the internet gateway.
  - The OS always deals with the private IP address on the Network Interface
  - You will never configure a public IPv4 address in the OS (windows/linux etc.)

### Elastic IP Addresses

- To avoid dynamically changing public IP addresses when instances are stopped/started, you need to allocate and assign an Elastic IP Address that remains stable
- You allocate Elastic IP Addresses to your account and use them with a primary or secondary network interface
- If you associate an elastic IP with a primary network interface on an instance, the current Public IPv4 address for that instance is removed and replaced with the Elastic IP address in its place
  - If you remove the Elastic IP Address, the instance will gain a new public IPv4 address (there is no way to get the first public IP address back)

### Use cases for Network Interfaces

- Licensing via a MAC address can be moved to different hosts/instances via just moving the interface that has that MAC address
- Can have separate network interfaces for management and data
- Multiple Interfaces can be used with different Security Groups on each (Security Groups are attached to the network interfaces, not the instance itself)
  - Useful if you need different rules for different IP addresses your instance has, for example.

### Manual installation of software on EC2

- [Demo](https://learn.cantrill.io/courses/1101194/lectures/27806465) at timestamp 7:14
- [Commands](https://learn-cantrill-labs.s3.amazonaws.com/awscoursedemos/0006-aws-associate-ec2-wordpress-on-ec2/lesson_commands_AL2023.txt)
- Enabling and starting services for rebooting restarts, etc.
