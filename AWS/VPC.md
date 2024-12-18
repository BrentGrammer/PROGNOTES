# VPC and Subnets

- Regional service (Regionally resilient)
- good [intro video](https://www.youtube.com/watch?v=bGDMeD6kOz0)
- Virtual Private Cloud - private network to deploy resources
- **Custom VPCs** can be many per region.
- Linked to a specific region, but spans all availability zones in that region (subnets within the vpc only span one AZ - see below)
- Each instance in a VPC can have a public (internet accessible) and private (only within VPC accessible) IP address. (you can also turn off public ip address)

### **SUBNETS**:

- A partition of your VPC network associated with and corresponds to an Availability Zone
  - Each subnet is set to an AZ on creation and cannot be changed later.
  - Ex: you can have a public subnet accessible by the internet and a private subnet that's not
    - Public: accessible by internet
      - Public example resources: EC2 instances and Load Balancer
      - Default subnet created for VPC
    - Private: only accessible internally to AWS
      - Private subnet resources: Databases, dont need access to internet
      - Need to create a Route table and configure private subnets manually
  - use **Route Tables** to define access between the internet and between subnets
- *AWS Services use Subnets where IP addrs are allocated from. 
  - You can't just launch services in a VPC, you need to use subnets for the services
  - Subnet is one AZ, so you need to think about how many AZs you will need (depends on regions since some regions have less AZs than others...). 3 AZs is a good starting point (will work in any region) + 1 spare - 4 AZs
- You should have a subnet for each AZ per tier (Application, Database, Web tiers + a spare)

### CIDR Range:

- a range of IP addresses that are allowed within the VPC
  - **Minimum range is /28 (16 host addrs) and maximum size allowed is /16 (65,536 IP host addrs)**
    - Good starting point is to use a 10. range of IP addrs
    - avoid picking ranges in 10.0 and 10.1 up through 10.10 (since people will probably pick those already) - start with 10.16 range for example.
    - When choosing how many think about the maximum number of regions the business will operate in and add a few as a buffer. Shoot for 2 network IP ranges for each region per account.
      - see [video](https://learn.cantrill.io/courses/1101194/lectures/26950363) at timestamp 10:41
  - recommended is to use 10. addressed networks within that range (10.1 through to 10.255). try starting with 10.16
  - tip:can use https://cidr.xyz to get more info on the CIDR ips to select - shows you range of addresses you'll get. The private IPs of your EC2 instances in that VPC should be within that range (they are assigned automatically when you launch an instance into a VPC)
- Internet Gateway: helps the VPC instance/subnet connect with the internet.
  - An Internet Gateway is attached to the VPC
  - Pubic subnets have a route to the internet gateway (traffic goes through it for comms with internet and subnet)
- increasing prefix increases number of subnets: /16 to /17 creates 2 networks, /16 to /18 creates 4, to /19 creates 8 and to /20 creates 16 networks

### NAT Gateway: 
- allows Private Subnets to access the internet, but they are still private and inbound traffic is denied
- Used if service needs to download software or updates from the internet for ex.
- NAT Gateway is AWS Managed
- NAT Instances are self managed by you
- Route from private subnet goes to NAT Gateway/Instance and that goes to the Internet Gateway

### Default VPC\*\* - only ONE per region allowed and created by default.

- **default CIDR Range is preset for default VPC to 172.31.0.0/16**
- Resiliency: One subnet is configured for every AZ in the region.
- The subnets cannot overlap with others:
  - AZ 1: 172.31.0.0/20 -- 172.31.0.0 to 172.31.15.255
  - AZ 2: 172.31.16.0/20 -- 172.31.16.0 to 172.31.31.255
  - AZ 3: 172.31.32.0/20 -- 172.31.32.0 to 172.31.47.255
  - The define the ranges for the subnets that can be used within the VPC.
- Some services expect a default VPC to exist, so generally should leave it in place, but not use it for anything in production (structure and CIDR range cannot be change and is inflexible)
- Best practice is NOT to use the default VPC directly

# Security

- NACL - Network ACL
  - **Security at the subnet level**
  - Firewall that controls traffic to and from a subnet
  - Has ALLOW and DENY rules
  - Attached to a specific subnet(s) - can be assigned to one or more subnets
  - Rules can only include IP Addresses
  - Stateless (does not remember retain request knowledge): Return traffic (traffic coming back from the server you sent data to) must be explicitly allowed by the rules
    - Example: By deny rules, you could explicitly deny a certain IP address to establish a inbound connection example: Block IP address 123.201.57.39 from establishing a connection to an EC2 Instance.
- Security Groups
  - **Security at the EC2 instance level**
  - Firewall that controlls traffic to and from an ENI (Elastic Network Instance) or an EC2 instance
  - Can only have ALLOW rules
  - Rules can include IP Addresses and other security groups
  - Stateful (retains request knowledge/associations): return traffic is automatically allowed regardless of rules. any changes applied to an incoming rule will be automatically applied to the outgoing rule.

# VPC Flow Logs

- Info about IP traffic going into interfaces
  - VPC Flow Logs
  - Subnet Flow Logs
  - Elastic Network Interfce Flow Logs
- Not enabled by default - you must enable it for the VPC
- Helps to monitor and troubleshoot connectivity issues
  - Get netowrk traffic information, load balancers, RDS, other AWS Services
- Can do into S3 or cloudwatch logs

# VPC Peering:

- Connect two VPCs privately using AWS' network
- Make them behave as if they are in the same network.
- The IP address range of the two must not overlap (CIDR range)
- NOT Transitive - if you add a new VPC peering to one of the VPCs it will not be able to talk to the other one automatically (You need to pair the third with the remaining one to make that work)

# VPC Endpoints:

- Connect to AWS public services from a VPC using a private connection using the AWS network instead of the public internet
- Better security
- Less latency eliminating public network hops
- **Types**:
  - **VPC Endpoint Gateway**: connects from a VPC to S3 or DynamoDB
    - Ex, connect from an EC2 instance in a VPC to these services via the Endpoint Gateway
  - **VPC Endpoint Interface**: used to connect to any other services in AWS (besides S3 and DynamoDB)
    - Ex, connect to Cloudwatch to push a metric from instance in VPC

# VPC PrivateLink

- Part of VPC Endpoints family
- Allows you to connect a service in your VPC to other outside services privately external to AWS
  - Does not require peering (does not scale) or internet gatways etc.
  - They create a load balancer to expose the service and you create an Elastic Network Interface (ENI) and establish a private link between the two.
  - This way communication between the two does not go through the public internet, but through the established private network.
- Exam question example: The question asked which service an ISV (independent software vendor) can use to allow their customers to privately access the applications managed by the ISV, via the customers' accounts.

# Hybrid Options

## Site to Site VPN

- Connect on premise VPN to AWS
- Connection is automatically encrypted and goes over the public internet
- limited bandwidth since it's over the internet
- **Not as fast or as private as Direct Connect**
- **On prem must use a Customer Gateway (CGW) and AWS must use a Virtual Private Gateway (VGW)**
  - Once those are provisioned you then create the Site to Site VPN and that's how they're linked.

## Direct Connect (DX)

- Establish a actual physical connection between on premise machines/data center and AWS
- Much more expensive and takes a month to establish
- **Fast connection, and Private**

# AWS Client VPN

- Connect from your computer using OpenVPN to your private network in AWS and on premises
- Used if you have EC2 instances, for ex., deployed in a private IP, but from your computer you want to access them as if you were in the VPC network.
- Install the client on your computer and connect over the internet but you will be connecting as if you were in the VPC.

# AWS Transit Gateway

- Simplifies trying to manage complicated topolagies of connecting VPCs into one hub and spoke interface
- No need for managing peering, etc.
- Works with AWS VPCs, Direct Connect Gateway and all the VPN connection options
- **Way to connect hundreds or thousands of VPCs together including on premises**
