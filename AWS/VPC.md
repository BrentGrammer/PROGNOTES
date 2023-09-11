# VPC and Subnets
- Virtual Private Cloud - private network to deploy resources
- Linked to a specific region
- **SUBNETS**: A partition of your VPC network associated with and corresponds to an Availability Zone
  - Ex: you can have a public subnet accessible by the internet and a private subnet that's not
    - Public: accessible by internet
      - Public example resources: EC2 instances and Load Balancer
      - Default subnet created for VPC
    - Private: only accessible internally to AWS
      - Private subnet resources: Databases, dont need access to internet
      - Need to create a Route table and configure private subnets manually
  - use **Route Tables** to define access between the internet and between subnets
- CIDR Range: a range of IP addresses that are allowed within the VPC
  - tip:can use https://cidr.xyz to get more info on the CIDR ips to select - shows you range of addresses you'll get.  The private IPs of your EC2 instances in that VPC should be within that range (they are assigned automatically when you launch an instance into a VPC)
- Internet Gateway: helps the VPC instance/subnet connect with the internet.
  - An Internet Gateway is attached to the VPC
  - Pubic subnets have a route to the internet gateway (traffic goes through it for comms with internet and subnet)
- NAT Gateway: allows Private Subnets to access the internet, but they are still private and inbound traffic is denied
  - Used if service needs to download software or updates from the internet for ex.
  - NAT Gateway is AWS Managed
  - NAT Instances are self managed by you
  - Route from private subnet goes to NAT Gateway/Instance and that goes to the Internet Gateway

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
  - Stateful (retains request knowledge/associations): return traffic is automatically allowed regardless of rules.  any changes applied to an incoming rule will be automatically applied to the outgoing rule.

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

