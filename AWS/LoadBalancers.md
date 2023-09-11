# Load Balancers

Servers that forward traffic to multiple instances

- Can Expose sinble point of access (DNS) to yuour application
- Handle failures of instances transparently to user


## ELB Elastic Load Balancer
- managed load balancer
- gauranteed to work, upgrades and maintenance are taken care of by AWS, high availability ensured
- Supports health checks

### Types of ELBs:
- Application Load Balancer - for applications on the web - Layer 7 HTTP HTTPS
  - Can be used to create single address DNS domain for multiple instances (i.e. server replicas)
- Network Load Balancer - High Performance balancer - gaming, millions of requests etc.  Allows for TCP - Layer 4
- Classic Load Balancer - older generation and being retired - do not use this.  Layer 4 and 7.
- Gateway Load Balancer - newer balancer added in 2020
- Best practice when setting up load balancers is to deploy them across at least 3 Availability Zones for high availability

Target Group: when setting up a load balancer you need to specify a target group which is basically grouping the EC2 instances or endpoints you want the LB to direct traffic to.
Target groups cost no money to keep around (instances assigned to them do though)

