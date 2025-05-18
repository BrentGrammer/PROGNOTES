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
- \*AWS Services use Subnets where IP addrs are allocated from.
  - You can't just launch services in a VPC, you need to use subnets for the services
  - Subnet is one AZ, so you need to think about how many AZs you will need (depends on regions since some regions have less AZs than others...). 3 AZs is a good starting point (will work in any region) + 1 spare - 4 AZs
- You should have a subnet for each AZ per tier (Application, Database, Web tiers + a spare)

### CIDR Range:

- **The number after the slash represents the bits that cannot change, i.e. /28 means the first 3 octets (3 \* 8) do not change, so you can have 10.0.0.1-254**
- Convention for private networks (i.e. VPC networks) is `10.x.x.x`, so stick with ranges starting with `10.`
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

# Custom VPCs (Building a VPC Network)

- [Video - theory](https://learn.cantrill.io/courses/1101194/lectures/26953721)
- [Demo - creating a Custom VPC](https://learn.cantrill.io/courses/1101194/lectures/45241152)

## Some Custom VPC Security Basics

- VPCs are Regionally isolated and Regionally resilient
  - Created in a Region, and operates in all AZs of that Region
- VPCs allow you to create isolated Networks, even can have multiple isolated networks in a single account in a single region.
- Nothing is allowed IN or OUT of a VPC without explicit configuration set up.
  - A network boundary which provides an isolated blast radius
  - If a VPC is compromised, the impact is limited to that VPC or anything connected to it
- Allow for **Default** or **Dedicated** Tenancy
  - Defined whether resources in the VPC operate on shared hardware or dedicated hardware
  - **WARNING**: If choosing Dedicated tenancy at first at the VPC level, you are LOCKED IN! If you choose Default for the VPC first, then you can choose later on a per resource basis whether they go on shared or dedicated hardware.
  - Unless you really know you want Dedicated Tenancy, just pick Default (it is the default option to start)

### IP Addressing

- IP Addresses: IPv4 Private CIDR Blocks by default. Can manually make IP Addrs public to allow access from the public internet.
- Comes with a pool of IP Addresses: Allocated a mandatory Primary Private IPv4 CIDR Block, configured when you create a custom VPC, and optionally configured public IPs.
  - Must be at the smallest a /28 prefix (The entire VPC has 16 IP Addresses)
  - Largest block size is /16 prefix - 65,536 IP addresses.
  - You can optionally add secondary CIDR blocks up to a limit and more via a support ticket
- Optional: Configure IPv6 by using a assigned /56 Prefix CIDR Block to the VPC
  - Note: some features might be limited versus using IPv4
  - Must let AWS assign the IP range, or use addresses that you already own - you cannot pick a block like you can with IPv4
  - All ranges that AWS uses for IPv6 are publicly route-able by default (there is no concpet of private and public IP addresses with IPv6). Explicit access from public internet etc still must be configured.
    - This is not a security concern, just removes some admin overhead.

### DNS provided to VPCs

- Provided by Route53
- Available on the base IP Address of the VPC + 2.
  - Example: if VPC addr is `10.0.0.0`, then the DNS IP address is `10.0.0.2`
- Options for DNS:
  - `enableDnsHostnames`: Indicates whether instances with Public IPs in a VPC are given public DNS host names.
  - `enableDnsSupport`: Enables or disables DNS Resolution in the VPC. If enabled, instances in the VPC can use the DNS addr (Base IP + 2 noted above), if disabled then this is not available.
  - **Check these settings if you have DNS issues and are troubleshooting** - switch them on or off as appropriate if you are having DNS issues to start with.
- In AWS Console, the DNS settings are in Actions dropdown > Edit VPC Settings > DNS Settings section

### Creating a VPC

- Just give it a name, example, "a4l-vpc1"
- Allocate a CIDR Range (i.e. `10.16.0.0/16`) which is from your IP planning
- Under IPv6 CIDR Block, choose `Amazon-provided IPv6 CIDR Block` to make sure the VPC is enabled for IPv6
- Set Tenancy (Default is recommended)
- After creating the VPC, the DNS settings are in Actions dropdown > Edit VPC Settings > DNS Settings section
  - Enable DNS hostnames if using (it is disabled by default) - this way any resources created with public IP Addresses will also have public DNS host names

## VPC Subnets

- [Video demo - creating subnets in a VPC](https://learn.cantrill.io/courses/1101194/lectures/26953794)

- Where services run from inside a VPC, and provide structure and resilience to VPCs
- Note on diagrams: Blue colored subnets on a AWS diagram means private, green highlighted subnets means they are public
- Subnets start off as private by default in VPCs and require configuration to make them public

### What is a subnet?

- A subnetwork inside a VPC that is limited to one Availability Zone
- Created in and for only one AZ and cannot be changed from that. A subnet cannot be in multiple Availabilty Zones.
  - If the AZ fails, then the subnet in that AZ fails as well
  - **For resiliency you need to put your components in different AZs so if one fails, you have resiliency**
  - Note: An AZ can have 0 or many subnets
- IP Range is a subset of the CIDR Range allocated to the VPC
  - _The IPs have to be non-overlapping and cannot overlap with other ranges/subnets in the VPC_ (exam question)
- Ipv6 can be enabled for subnets in the /64 prefix range (a subset of the /56 IPv6 range of the VPC).
- Communication: Subnets within a VPC can communicate with other subnets within the same VPC

### Reserved IP Addresses in a Subnet

- some IPs in a VPC subnet are reserved
- There are 5 reserved IP Addresses that you cannot use in a subnet:
  - **Network Address**: The first/starting address of any subnet (example: for `10.16.16.0/20`, `10.16.16.0` is reserved)
    - Note: This is true for any IP network even outside of AWS, you never use the first addr in a network
  - **Network +1**: The first IP after the Network Address (see above). Reserved for the VPC Router which moves data around and in aor out of the VPC subnets. The network Interface of the Router uses this address. Ex: `10.16.16.1`
  - **Network +2**: The second usable IP addr in the range is reserved and used for DNS. Ex: `10.16.16.2`
  - **Network +3**: Reserved for future requirements and cannot be used. Ex: `10.16.16.3`
  - **Network Broadcast**: The last address in the subnet range (ex: `10.16.31.255`). Broadcasting is not allowed, but this address is reserved and cannot be used.
  - _Always remember to subtract 5 usable addresses from the number of addrs you need in a subnet!_

### DHCP Options Set (Dynamic Host Configuration Protocol)

- A Configuration Object Applied to VPCs - every VPC has a DHCP Options Set linked to it
- DHCP is how computers recieve IP addresses automatically
- The DHCP Object is applied once to a VPC and that configuration flows through to subnets in the VPC
  - controls DNS servers, NTP servers, net bios servers, and more
- You CANNOT CHANGE the DHCP Options Set - if you want to change the settings, you need to create a new one and link it to the VPC.
- Can optionally configure a auto assign public IPv4 Address (required for making addresses in a subnet public which make resources in the subnet public)
- Optionally give addrs in a subnet a IPv6 addr.

### Example of a Subnet plan:

- This is a plan to create 12 subnets across 3 Availability Zones
- Note how we have copies of the components across 3 Availability Zones in 3 subnets - A, B and C for resiliency

| NAME          | CIDR          | AZ  | CustomIPv6Value |
| ------------- | ------------- | --- | --------------- |
| sn-reserved-A | 10.16.0.0/20  | AZA | IPv6 00         |
| sn-db-A       | 10.16.16.0/20 | AZA | IPv6 01         |
| sn-app-A      | 10.16.32.0/20 | AZA | IPv6 02         |
| sn-web-A      | 10.16.48.0/20 | AZA | IPv6 03         |

<br>
| sn-reserved-B | 10.16.64.0/20  | AZB | IPv6 04         |
| sn-db-B       | 10.16.80.0/20  | AZB | IPv6 05         |
| sn-app-B      | 10.16.96.0/20  | AZB | IPv6 06         |
| sn-web-B      | 10.16.112.0/20 | AZB | IPv6 07         |
<br>
| sn-reserved-C | 10.16.128.0/20 | AZC | IPv6 08         |
| sn-db-C       | 10.16.144.0/20 | AZC | IPv6 09         |
| sn-app-C      | 10.16.160.0/20 | AZC | IPv6 0A         |
| sn-web-C      | 10.16.176.0/20 | AZC | IPv6 0B         |

Remember to enable auto assign ipv6 on every subnet you create.

- You would also have a AZ D set of ranges for another subnet for future growth (unknown additional requirements/components that would need addresses) - this is not shown in the table.

- See [video](https://learn.cantrill.io/courses/1101194/lectures/26953794) at timestamp 3:19 for making the IPv6 subnet ranges unique by adjusting the last values in the CIDR block numbers.

### Creating a Subnet

- Normally you do not create all the subnets manually, but you would automate the process.

- AWS Console > VPC > Subnets > "Create Subnet"
- Follow the specs in your IP plan for assigning the ranges (add a subnet for each group per AZ A, B, C for example as shown above in the table)
  - Create subnet button in VPC dashboard for each group by AZ
- Remember to enable auto-assign IPv6 addresses - VPC > Subnets > select subnet > Actions dropdown > Edit Subnet settings > Auto-assign IP Settings section > tick Enable auto-assign IPv6 address

Note: Subnets listed in the subnets page in AWS Console without a name are the default subnets. Those with a name are probably custom ones.

## VPC Routing

- Highly Available device available in all VPCs (default or custom) that moves traffic from one point to another
  - Runs in ALL Availability Zones that the VPC uses automatically
- VPC Router has a Network Interface in every subnet in the VPC at the **Network +1** address in the subnet
- By default, VPC Router routes traffic between subnets in a VPC
  - For example: An EC2 instance in one subnet wants to communicate with something in another subnet in the VPC, the Router is what moves that traffic between them.

### Route Tables

- Configurable with Route Tables to control what it does with traffic or data when it leaves a subnet
  - By default, in a subnet, a **Main Route Table** is used unless a custom route table is created.
    - When creating a custom route table for a subnet, the Main Route Table is disassociated.
  - A subnet can only have one route table associated with it
  - A Route table can be associated with many different subnets
- NOTE: Subnets in a VPC which don't have an explicit association with a Route Table are auto associated with the Main Route Table by default

#### Managing data leaving the subnet:

- A packet of data has a source, destination and data in it.
- A route table looks at the destination address of a packet leaving the subnet
- The router looks at all routes that match the destination address of the packet
  - A destination address could be a specific IP Address or an entire network (`/32` or `/60` match for ex.), or a default address (`0.0.0.0/0` matches all IPv4 IP addrs)
    - If there are multiple matches, then the higher the CIDR prefix value of the route, the higher priority it has
  - When a destination match is found in the route table, the VPC Router forwards the packet to the **Target** field in the route table.
    - The **Target** field will point to an AWS Gateway or `local` (`local` = destination is within the VPC)

#### "Local" Routes

- All Route Tables have at least one route defined - the `local` route, which maps to the VPC CIDR Range and can be delivered directly.
  - If the VPC has IPv6 enabled, it will have another default `local` route matching the IPv6 CIDR for the VPC
- `local` routes in the Route Table **take priority over everything** and have the highest priority in the case of multiple matches for the destination.
- `local` routes are not editable

#### Exam takeaways for Route Tables

- Route Tables are attached to 0 or more Subnets
- A Subnet must have a Route Table (either the Main Route Table of the VPC or a custom one you create)
- Controls what happens to data that leaves the subnet or subnets that the route table is associated with
- local routes match the VPC IPv4 or IPv6 CIDR Range
- A Route Table matches to a Destination in a data packet in the table, and directs the data to the Target field for that Destination in the table.

### Internet Gateway

- Regionally resilient gateway that can be attached to a VPC

  - You do NOT need a Gateway per Availability Zone - it is resilient across the region's AZs by design

- VPC can have 0 or 1 Gateways:
  - 0 Gateways: makes the VPC totally private!
  - 1 Gateway: makes VPC accessible to public internet
  - An Internet Gateway can only be attached to 1 VPC at a time
- Runs from the border of the VPC and the AWS Public Zone
  - Allows resources with public configured IPv4 or IPv6 IP addresses to be reached from the Internet, or to allow connection to the AWS Public Zone or the Internet.
  - The AWS Public Zone encompasses access to services like S3, SQS, SNS or any other public AWS service
- Managed Gateway: AWS handles maintenance and performance of the service

- See [Video Diagram of using an Internet Gateway in a VPC](https://learn.cantrill.io/courses/1101194/lectures/26953800) at timestamp 8:25

#### Nuances of public IPv4 Addresses

- **An EC2 instance in a VPC that is accessible from/to the outside public internet has no awareness of its public IP address - it only has a private IP, and the Internet Gateway maps the private IP to a public IP that it manages.**
  - an EC2 instance only configures a private IPv4 address and never the public address
  - IPv6 addresses are natively publicly routeable, so an EC2 instance does know the public IPv6 IP address. (The Internet Gateway does not do any translation as described below in this case)
- An instance will have an assigned subnet address within CIDR range (i.e. `10.16.16.20` and also a associated public IPv4 address, i.e. `43.250.192.20`)
  - The IPv4 public address is not directly for the EC2 instance in the subnet of the VPC
  - A record is created which the Internet Gateway maintains which links the instance's private IP address to its allocated public IP address.
  - The instance itself **is not configured with that public IP** address! Inside the Operating System on the instance - **it will NOT see or be aware of the public associated IP address inside the instance and only see the private addr!!**
- An internet gateway will intercept a packet leaving the VPC from an EC2 instance and change the source address on the packet to the public IPv4 address linked to the EC2 instance that it came from (because the EC2 instance attached its private IP address as the source on the packet since it is unaware of the public IPv4 address associated with it and only mapped in the Internet Gateway)
  - The external destinations of the packet do not know anything about the source private IP address of the EC2 instance that the packet came from, only about the public IP address the INternet Gateway maintains for that EC2 instance.
  - When the response packet is received by the INternet Gateway, it also again changes the destination address from the Public IP address for the EC2 instance to the private IP address in the VPC subnet for the instance (it has a record of the relationship between the private IP of the instance in the VPC to the public IP address registered for it)

### Bastion Hosts

- a.k.a. Jumpboxes
- An instance in a public subnet in a VPC
- Bastion Hosts are used to allow incoming management connections
  - Once connected, the user can access internal VPC private resources
- Used as a management point or entry-point for private-only VPCs
  - A private VPC will have a Bastion Host as the ONLY way to get access to that VPC
  - Can be configured to accept connections from certain IP addresses, authenticate with SSH, integrate with onprem identity servers, etc.
  - _They function as the ONLY entrypoint to a highly secure VPC_
    - Note: There are alternative ways to do this now which are recommended.

## Making VPC private subnets Public

[Video](https://learn.cantrill.io/courses/1101194/lectures/26982553)

- Subnets such as those designated for Web components can be allocated to have a public IPv4 address to have connectivity to and from the internet and the AWS Public Zone

### Steps to making a Subnet Public:

#### Attach an Internet Gateway

- AWS Console > VPC > Internet Gateways (in left side menu) > "Create Internet Gateway" button
  - Note: you will see a default Internet Gateway (with no name) that was created automatically when you created the VPC to start with.
  - You need to create a custom Internet Gateway for custom VPC/subnets
- Enter a name for the Internet Gateway creating - example `a4l-vpc1-igw` ("igw" for internet gateway)
  - Click create Internet Gateway
  - Initially IGWs are not attached (will show detached state)
- Attach the IGW to the VPC - click Actions dropdown > Attach to VPC

#### Make the subnets for the web components public

- **Create a Route Table**
  - AWS Console > VPC > Route tables (menu on the left) > "Create Route table" button
  - Name the route table (ex. {appname-vpc-rt for route table-component} -> `a4l-vpc1-rt-web`)
  - Select the VPC for it and click Create Route table
- **Associate the Route Table with the subnets**
  - AWS Console > VPC > Route tables (left menu) > Subnet associations tab > "Edit subnet associations" button
  - Select/tick the subnets to associate the route table with - i.e. your web component subnets
    - Note how subnets are by default associated with the Main route table
  - click save associations button to associate the rt with the subnets selected
- **Add Routes to the Route Table (1 for IPv4 default route, and another for IPv6 default route)**
  - Note: These routes target point to the attached Internet Gateway for the VPC
  - AWS Console > VPC > Route tables (left menu) > Routes tab
    - Note the local Routes already in the table which are the IPv4 and IPv6 CIDR ranges in the VPC - this ensures that all traffic can be routed in the range of the VPC by default (cannot be changed or removed)
  - Click "Edit routes" > "Add Route" to add 2 default routes for IPv4/6.
    - IPv4 -> `0.0.0.0/0`
      - This means any IP address. Note that it is not as specific as the local default route of the CIDR range for the VPC which will take precedence, so **any traffic that is NOT destined for the VPC CIDR range will be handled by this default IPv4 default route and sent to the target Internet Gateway**.
      - Assign the internet gateway for your VPC as the target for the route - select it in the target dropdown
    - IPv6 -> `::/0`
      - Matches all IPv6 addresses, but less specific than the local IPv6 route of CIDR Range for the VPC as above.
      - Select the same INternet Gateway for the VPC as the target and click Save Changes
- **Configure Auto-assign IPv4 public IP address for any resources launched into the web component subnets**
  - AWS Console > VPC > Subnets (left menu)
  - Select a web component's subnet > Actions dropdown > "Edit Subnet Settings"
  - tick "Enable auto-assign public IPv4 address
  - Click Save button
  - Repeat these steps for all the web component subnets

#### Creating a Bastion Host to test configuration (bad practice)

[Video](https://learn.cantrill.io/courses/1101194/lectures/27186078)

- Create an EC2 Instance (can use Linux AMI)
  - Select a key pair (SSH RSA which you need to create if you have not already)
  - Edit the Network Settings section and assign the EC2 instance to your custom VPC
    - select a web component subnet to launch the EC2 instance into
    - Select to create a security group and name it with description: Ex: `A4L-BASTION-SG`
    - Make sure SSH and auto assign public IP addresses are ticked
  - Will take a few minutes for bastion instance to initialize

# NACL (Network Access Control Lists)

- Like a traditional firewall that is available within a VPC
  - See [Firewalls notes](../CyberSecurity/Firewalls.md)
- **Associated with Subnets in a VPC**
  - Every subnet has one associated Network ACL that filters data as it crosses the boundary of that subnet (data coming in or out of a subnet)
  - Either a default NACL created with the VPC, or a custom one created by a user for the subnet
    - Note: A single NACL can be associated with many different subnets (but, a subnet can only have one NACL)
  - **IMPORTANT**: Connections between resources INSIDE the subnet are NOT AFFECTED by the Network ACLs
- Operate on traffic at the SUBNET BOUNDARY
- Have NO reference to Logical Resources - only references to IP addresses, ranges and ports

### Typical Use Case for NACLs

- Used with Security Groups to add explicit DENY rules for Bad IPs or Networks
  - Use a Security Group to Allow traffic
    - See [Security - Security Groups section](./Security.md)
  - Use the NACL to Deny traffic

### Default vs. Custom NACLs

- VPCs are created with a DEFAULT NACL - contains inbound and outbound rule sets with the default implicit Deny and a catchall Allow
  - **This means that the default for a NACL created with a VPC has NO EFFECT - all traffic is allowed!**
    - Security Groups are preferred
- Custom NACLs created for a specific VPC are initially associated with NO subnets
  - Only one rule on both Inbound and Outbound rule sets: Default Deny all traffic
  - Caution: If you associate a custom NACL with a subnet, then by default all traffic is Denied!

### Each NACL has 2 sets of Rules

- Note: Inbound and Outbound rules are only referring to the direction of traffic, not whether we are dealing with a request or response part of a connection!
- **NACLs are Stateless** - they do not know if traffic is a request or a response
  - You need two rules for each request/response - one Inbound/request rule and one Outbound/response rule!
- Rules match the Destination IP Address or IP range, Destination Port or Port range together with the protocol
  - Can **explicitly allow or deny traffic**

#### Inbound Rules

- Only affect data entering the subnet

#### Outbound Rules

- Only affect data leaving the Subnet

### Rule Processing Order

- Network ACL determines if Inbound or Outbound rules apply
- Then, start from the lowest rule number
  - Evaluate traffic against each individual rule until a match is found
  - NOTE: Rule ordering numbers are considered UNIQUE/separately for Inbound and Outbound sets of rules. (i.e. you could have two rules with the same number in Inbound and Outbound rules, but they are considered separately)
- Traffic is Allowed or Denied based on the matching rule
  - **CAUTION**: if you have a Deny rule that comes before an Allow rule for the same traffic, the Allow rule is never processed.
  - Note: There is a catchall marked by asterisk `*` with an explicit Deny - if no rule matches for the traffic, it will always be Denied.

### Disadvantages of NACLs

- Since they are stateless, require more overhead for request/response rules for traffic in and out of the VPC or traffic between subnets in the VPC - MORE COMPLICATED
  - The pairs of rules needed for each request/response with opening up ephemeral port ranges needed for the response is one contributor to the complexity and overhead
  - Additionally, requests for software updates require even more rules needed to be added
- This can become complicated with multi-tier applications
  - i.e. Rules are needed for both the boundary of a subnet and the internet and the boundary at the application level (ex: a web component in a subnet to an application component in another subnet in the same VPC)
