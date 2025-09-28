# NAT Gateway (Network Address Translation):

[Video](https://learn.cantrill.io/courses/1101194/lectures/26982639)
[Demo Setting up a NAT Gateway](https://learn.cantrill.io/courses/1101194/lectures/26982643)

- NAT Gateways are in AWS Console > VPC > NAT gateways in the left menu

## What is NAT?

- A set of processes that can adjust IP packets by changing their Source or Destination IP addresses.
  - Internet Gateways perform _Static NAT_ (changes the source IP address on the packet from the private IP addr to the public IPv4 addr, for example, and changes the destination addr to the private IP addr when the packet returns )
- Primary purpose is to give private instances access to the internet (but not vice versa) and AWS public Zone services like S3, etc.
- AZ Resilient (NOT Region Resilient!) - they are not regionally resilient like Internet Gateways - only in the AZ they're in
  - For regional High Availability you need to deploy one NAT Gateway per AZ in your VPC!!
  - A Route Table is needed for each AZ and must point at the NAT Gateway in that AZ as a target
  - NOTE: **COST** - cost can get expensive if you have a lot of AZs - need to think about VPC design.
    - There are **2 Charges for using NAT Gateways**:
    - **HOURLY CHARGE**: Current cost is about 4 cents per hour, partial hours billed as full hours
    - Data processing charge: in addition there is a 4 cents per Gigabyte of data processed
- Scalable
  - Can scale to 45 gigabits per second
  - Can deploy multiple NAT Gateways and split subnets across multiple provisioned products
    - Can provision heavy consumers across two different subnets in the same AZ, have two NAT Gateways in that AZ and route each subnet's traffic to a different NAT Gateway to quickly scale if more bandwidth is needed.

### IP Masquerading:

- When people say "NAT" they are usually talking about this
- A subset of NAT - hides a whole CIDR IP Block behind a single public IP address.

  - Gives a range of IP addresses **outgoing only** access to the public internet and AWS Public Zone
    - Many private IPs represented by a single public IP address does not allow for incoming connections from the outside
  - In contrast to Static NAT, this deals with multiple IP addresses converted to one IP addr.
  - Popular due to IPv4 address space running out.
    - **You can initiate connections to the outside with responses to those connections, but the outside cannot initiate connections to the IP addresses hidden behind a NAT**
    - allows Private Subnets to access the internet, but they are still private and inbound traffic is denied

### Use Cases

- In multi-tier applications, you want some components/instances which are private and not accessible by the public internet, but want to allow outgoing connections
- Used if service needs to download software or updates from the internet for ex.

### Using NAT

[Typical NAT setup in a VPC](https://learn.cantrill.io/courses/1101194/lectures/26982639) at timestamp 4:33
Also see [Video](https://learn.cantrill.io/courses/1101194/lectures/26982641)

- Private Subnet of components has route table that has a default route that points to > NAT Gateway inside a public subnet of public components (in the same AZ) > Internet Gateway
  - A private subnet has a route table of private IP addresses for the private instances used by the builtin VPC router
  - A NAT Gateway is **provisioned inside another public subnet** in the VPC that has a translation table that converts the private IP addresses of the instances into a public routable address (an _Elastic IP Address_ - a static addr that does not change and are allocated to your account)
    - The public routable address is not accessible to the internet because it is in a VPC
    - You need already setup public subnets in the VPC which include having a Internet Gateway, public IPv4 address assignment configured/turned on, and a default route in the public subnets pointing at the Internet Gateway
  - An Internet Gateway is needed to receive traffic from the NAT Gateway and change the source Address to a real public IPv4 address (that can be accessed by the internet or AWS public services such as S3)
  - The response is converted by the INternet Gateway to have the Destination address changed to the NAT Gateways routeable address
  - The NAT Gateway then changes the response packet's Destination address to be the private IP address of the instace in the private subnet (it knows what this is using the translation table holding those mappings)
- Can use an EC2 instance setup to provide NAT services (historic way)
  - NAT Instances are self managed by you
- NAT Gateway is AWS Managed that can handle NAT for you which are provisioned in a VPC
- Route from private subnet goes to NAT Gateway/Instance and that goes to the Internet Gateway

### NAT Instances vs. NAT Gateways

- See [video](https://learn.cantrill.io/courses/1101194/lectures/26982641) for tips on using NAT instances if not using a NAT Gateway.
- Recommended to use a NAT Gateway over a NAT Instance for better performance, high availability, scalability and lower maintenance
- NAT Instances (EC2 Instances) can be used for cheaper more predictable cost (at the loss of high availability and scaling), they do not scale automatically like NAT Gateways.
  - Good for test instances and Development environments
  - Cheaper
  - More flexible, ec2 instances can also be used as a bastion host or for port forwarding.
    - **NAT GATEWAYS CANNOT BE USED AS A BASTION HOST** you don't have access to manage it like an EC2 instance
  - **FOR EXAM: Nat Gateways do not support Security Groups, you can only use NACLs for filtering traffic!!**

### NAT is NOT required for IPv6

- All IPv6 addresses in AWS are publicly Routeable, so you do not need NAT when working with IPv6 addresses - the Internet Gateway works directly with IPv6
  - If you choose to make a private instance public via a default route (`::/0`) pointed to the Internet Gateway as a target, it will become a public instance (bidirectional connectivity to internet and AWS Public Zone)
  - If you only want outgoing connections from IPv6 instances, use an Egress-only Internet Gateway
- NAT is primarily used for IPv4 routing and NAT Gateways do NOT work with IPv6

## Setting up a Nat Gateway

[Video](https://learn.cantrill.io/courses/1101194/lectures/26982643)

- AWS Console > VPC > Nat gateways on the left menu > "Create NAT Gateway" button
- Name and select the Subnet/AZ in the VPC you want to deploy into (make one for each AZ in a **public** subnet)
- Allocate Elastic IP address (that does not change) by clicking on "Allocate Elastic IP"
- You can check on, manage and release the IP addresses in AWS Console > VPC > Elastic IPs in the left menu
- Configure the Route tables so private instances can communicate via the NAT Gateways
  - AWS Console > VPC > Route tables in left menu
  - Create a route table for each of the AZs
  - Create a default Route on each route table (per AZ) - select route table > Routes tab > "Edit Routes" > Add Route
    - Enter `0.0.0.0/0` for the destination (since this is for packets leaving the private instance and going to the public outside anywhere), Select NAT Gateway in Target dropdown and select the NAT Gateway for the AZ
- Associate the Route Tables with a subnet (per AZ)
  - \*Subnets in a VPC which don't have an explicit association with a Route Table are auto associated with the Main Route Table by default
  - Go to AWS Console > VPC > Route tables > select the route table > Subnet associations tab > "Edit subnet associations" button
  - Select only the **Private subnets** for the AZ, not the web/public components, and click save (repeat for all private components per AZ to associate with the custom route tables created in each AZ)

This now enables private instances to access the public internet through the NAT Gateway in the public subnets per AZ - go to connect to an instance and run `ping 1.1.1.1` to test connection.
