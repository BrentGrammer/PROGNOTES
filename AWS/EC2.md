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

## Purchase Options (EC2 types)

### On Demand

- Default option - start with this and only move to something else if needed, mostly okay for normal usage 99% of the time - no capacity management needed.
- Ideal for short term workloads or undetermined workloads - something you need to provision for something and then terminate or not sure of need
  - short term workload which needs the cheapest EC2 pricing but **can't tolerate interruption**
- Different customers using isolated instances can exist on the same host and use shared hardware
- Reasonable cost - per second billing while instances are running
  - When shutting an instance down you're not paying for the resources
  - Associated resources like storage still charge regardles if the instance is shut down
  - No discounts, consistent pricing.
- If there is a capacity or system failures, reserved types are receieve priority provisioning over On Demand options
  - If the business need is critical then you should consider using something other than On Demand

### Spot Purchase Option

- Per region, there is free unused capacity on EC2 Hosts - AWS takes this and offers it at a spot price which is cheap
- You set a maximum price you are willing to pay and AWS will have their own price. If their price is lower than your maximum price, you will pay only their current spot price per second.
- **If capacity needs change, AWS can raise the spot price at will** - if the raised spot price exceeds the maximum price you set to pay, your instances will be automatically terminated.
  - These instances should not be viewed as reliable
- Should not be used for workloads that cannot tolerate interruptions or are needed long term
- Good use cases are for things that are not time critical or need reliable uptime.
  - Good for broken up tasks or stateless workloads that can be re-run on failure

### Standard Reserved Instances

- For known Long term consistent usage and core parts of your system and workloads that cannot tolerate interruption
- Unused reservations are still billed!
- Locked to an AZ or region and specific instance type
  - If locked to an AZ, then reservations only apply to instances launched in that AZ
  - If you have a reservation for a smaller instance type than you provision you will get a partial cost effect
- Should be used for parts of infrastructure that are always there and never change
- Time commitment must be 1 or 3 years for a reduced per second fee.
  - All Upfront: You can optionally pay for the entire agreed term for the greatest discount - longer term means cheaper but you are locked in, but there is no per second fee this way.
  - Partial Upfront: reduced pay per second fee - good middle ground without long commitment
  - You pay whether the reservation is used or not
- Note: reserved instances are still on hosts that are shared with other customers, like On Demand

### Scheduled Reserved Instances

- Long term requrements, but it doesn't need to run consisently and constantly (i.e. only at specific times of day or specific days in a week)
- Specify the frequency, duration and time of use (i.e. daily for 5 hours)
- Get a slightly cheaper rate than On Demand, but you can only use it for that specified time
- Use cases: Sales analysis data that needs to run at steady intervals (once a day or week, etc.) for the foreseeable future
- Minimum commitment is one year

### Capacity Reservations

- USed for critical operations that cannot tolerate interruptions (AWS will allocate capacity to reserved tiers over On Demand, etc. if there is a failure)
- Billing component
- Capacity Component: can reserve capacity but no need for long term commitment to AWS
- Types of reservations - need to commit at least one year for these:
  - Regional Reservation crosses AZs - billing discounts for any instances launched into a region.
    - Note: no capacity reservation with this alone. You are at the same priority as On Demand instances in the case of a widespread failure or issue with AWS
  - Zonal Reservations: this is for a specific AZ, but also reserves capacity for that AZ
- On Demand Capacity Reservations: for a specific AZ and you always pay for the capacity whether you consume it or not - you do get higher priority from on demand capacity if system failure across AWS
  - No time commitment required
  - Need to know what capacity you require so you don't waste it if it is not used.
  - No cost reduction. If you don't need all the capacity and are doing something that is consistent, it might be cheaper to use Reserved Instances instead

### Dedicated Host

- A host allocated to one customer entirely (no shared hardware with other customers)
- The hosts are designed for a specific family - A, C or R for example
- INstances on the host have no per second charge - you pay for the entire Host
- You need to manage the host's capacity - if you run out then you cannot launch anymore instances.
  - Limited number of instances you can launch on your host
- Host Affinity: feature linking EC2 instances to certain EC2 Hosts. Stopping and starting the instance will remain on the same host.
- **Reason to use option is for socket and core licensing requirements** (for software that is bound and tied to specific hardware via a license agreement)

### Dedicated Instances

- Launch instances on a host and AWS commits to not letting any other customers using hardware on that same host - only your instances can be launched on it.
- Useful when you don't want to share hardware, but you don't want to manage the host itself.
- Pay a cost premium to ensure you will never share underlying hardware with other customers
- You do not pay for or own the host itself
- Billing: hourly fee for any regions you're using dedicated instances, regardless how many you are using in that region.

### Savings Plan

- Time based commitment on a hourly cost you will pay consistently for that time commitment (i.e. 20 dollars an hour for 3 years)
- You get a reduced cost on resources with this comittment
- Useful if migrating away from EC2 to other services like Fargate, Lambda and serverless architectures
- two types
  - General Compute amounts - can save up to 66% on the normal on demand price
    - Valid for various compute services: EC2, Fargate and Lambda
    - Savings plan rate expires after you've consumed the price usage commitment you made, afterwards you get charged normal on demand rates. You should evaluate your usage and adjust the savings commitment as needed.
  - EC2 Savings Plan - you have to use only EC2, but get up to 72% reduction in price from regular on demand charges.

## Status Checks & Auto Recovery

### Instance Status Checks

- Every EC2 instance has 2 high level status checks
  - EC2 console should show 2/2 checks passed, otherwise there is a problem
- First check: System Status
  - indicates EC2 service or host issues: loss of system power, loss of network connectivity, or software/hardware issues with the EC2 host
- Second check: Instance Status
  - Corrupt file system, networking problems (internal, bad settings set), OS kernel issues preventing correct boot up

### Auto Recovery

[Video](https://learn.cantrill.io/courses/1101194/lectures/27806478) timestamp 3:01

- Simple feature to automatically handle recover if the status checks fail or ec2/host specific problems
- Moves instance to a new host, starts it up with the same config as before (IP addressing is maintained), restarts any software configure to auto-restart
- Enables potential full recovery from any status checks issues.
- Go to EC2 instance in AWS console > Status Checks tab for instance > Actions dropdown > Create Status Check Alarm
  - Will alarm if instance fails checks
  - SNS notification sent by default if checks fail a set number of times within a selected time period
  - Alarm Action can be set to specify what to do when the alarm occurs - recover, restart, stop or terminate the instance
  - To use Auto Recovery, select the Recover option in the Alarm Action options

#### Auto Recovery considerations

- Note: does not protect against AZ wide failure - only takes action inside the AZ that the instance is provisioned in and EC2 instance host/specific instance problems.
- Requires available extra capacity - in case of major failure across AZs in a region this won't work if the entire region is down etc.
- Only works with certain instance types, see [docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-recover.html)
- Does NOT work if using instance store volumes - only works with instances that have EBS volumes attached.

### Termination Protection

[Video Demo](https://learn.cantrill.io/courses/1101194/lectures/27806479)

- Adds a layer of protection to prevent inexperienced team members from terminating an instance on accident
  - an ec2 attribute is set `disableApiTermination`
- Adds an extra permission which is required in order to terminate an instance (you need permissions to disable the protection to be able to first turn it off and then terminate an instance)
  - Allows for role separation where you can give permissions to enable/disable the protection to one group of people (i.e. only Senior Administrators) and the ability to actually terminate to another group (i.e. normal or junior Administrators)
- In AWS Console go to EC2 > right click on instance > Instance Settings > Change termination protection option. Click enable and save in the dialog that comes up.
- If you try to terminate an instance with this on, you will be presented with an error that it could not be terminated when you click on Terminate.

#### Change shutdown behavior

- Note: you can also right click on EC2 instance in console > Instance settings > Change shutdown behavior to tell AWS to terminate or stop instances.
  - the default is to stop the instance, not terminate it
  - If you don't want a bunch of stopped instances lying around for example this can be changed to just terminate on failure or shutdown.

## Instance Metadata

- Service provided to instances with data about the instance that can be used to configure an instance.
  - Accessible via an endpoint with the metadata IP address http://169.254.169.254/
- Allows the instance to access information about its environment that it wouldn't be able to access otherwise
- Accessible in all instances at IP address `169.254.169.254`
  - endpoint: `http://169.254.169.254/latest/meta-data/{attribute}`
- Environment info access: host name, events, security groups, etc.
- Allows access to Networking info (OS of an instance cannot see any of its own IPv4 public addressing, this allows the instance to see it)
  - OS only has exposure to private IPv4 addresses
  - A public IPv4 address is never configured in an instance Operating System, it is only configured by the Internet Gateway resource
  - Note: IPv6 is configured in the OS, since it is always public (no concept of private/public with IPv6)
- Authentication information access
- Used to pass in temporary ssh keys by AWS (using instance connect, for ex. behind the scenes it does this)
- User-data access. can run scripts for automation steps on the instance
- **Meta-data service has no authentication or encryption**
  - anyone who can access the instance can see the meta-data
  - assume that meta-data is exposed and treat it as public data

### Metadata commands:

- Can access the metadata endpoint with curl on the instance
- Can also download the AWS query tool

```shell
# example queries for some attributes of the instance:
curl http://169.254.169.254/latest/meta-data/public-ipv4
curl http://169.254.169.254/latest/meta-data/public-hostname # public DNS name

# Download the AWS query tool for easier use
wget http://s3.amazonaws.com/ec2metadata/ec2-metadata
chmod u+x ec2-metadata # on linux make whereever it downloaded the tool to executable

# commands with query tool
ec2-metadata --help # get list of commands
ec2-metadata -a # show AMI used to launch this instance
ec2-metadata -z # get availability zone the instance is in
ec2-metadata -s # show any security groups launched with the instance
```
