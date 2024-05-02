# Elastic Cloud Compute
- IaaS - Infrastructure as a Service
- Bootstrapping: running commands when a machine starts and boots up
  - Script is run ONCE on machine start
  - Bootstrapping script commands run with root user priveledges
  - EC2 setup - advanced options -> **EC2 User Data** script. Runs on startup of EC2 instance
- By default it is a private service (deployed into a subnet in a VPC in the private zone).
  - If you want to allow public access you need to configure that.
- IaaS - Infrastructure as a Service
- EC2 is AZ Resilient: If an AZ that the EC2 instance is in fails, then the instance will be taken down with it.

## Instance types:

See [instances.vantage.sh] for list of instances, est cost and reference

Naming convention: [instanceClass][generation-number].[size within the class]

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
