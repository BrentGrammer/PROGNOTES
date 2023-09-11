- 9Disaster Recovery
- Lower Latency closer to users
- Better for security - harder to attack

Regions: deploy apps and infrastructure
Availability Zones: Made for multiple data centers
Edge Locations (Points of Presence): for content delivery as close as possible to user

# Route 53
- Managed DNS
- **Routing Policies**:
  - Simple Routing Policy: simple routing has no health checks, simple call with a url string to get the ip address, for example (NOTE: all other policies have health checks)
  - Weighted Routing Policy: set weights for different EC2 instances (like load balances) - set percentages. distributes traffic
  - Latency Routing Policy: Sends back which server is closest to the user to minimize latency - used for users who are dispersed geographically
  - Failover Routing Policy: Have a primary and failover instance - Route53 does a health check on the primary EC2 instance and if bad, reroutes to the failover instance
- Example:
  - A record created to tie a web url string to a IP address
  - Client gets response from Route53 with the IP Addr and uses it to make a call to the server using it.
- Cost: about 12 dollars a year for domain and 0.50 per month for hosted zone
- can use Route53 geolocation routing policy to to block certain geographies.


# AWS CloudFront
- CDN - uses Edge Locations to cache data
- Available globally not by region.
- Improves perf and is cached at the edge to improve user experience
- DDoS protection from distribution globally
- integrates with Shield and AWS Web Application Firewall
  - can use AWS WAF web access control lists (web ACLs) to help limit DDoS attacks
- Client makes request to distant server (database) and the response is returned and cached at the edge location closest to them for future calls.
- Can cache from origins such as S3 Buckets or Custom HTTP

Difference between Cloudfront and S3 Cross Region replication
Cloudfront:
- CloudFront has global network
- files are cached in each location for a day (TTL)
- **Great for static content that must be available everywhere**
S3 Replication:
- Must be setup for each region you want replication - not available everywhere by default
- No caching - files are updated in near real time
- Read only
- **Great for dynamic content that needs to be available in certain regions at low latency (not everywhere and not for static content)**

# S3 Transfer Acceleration
- Used to increase transfer speed **over long distances** by sending a file to an Edge Location over a fast public network which will forward the file to an S3 bucket over a fast private AWS network in the target region
- The key is that AWS private network is faster and reliable than the public internet - so sending it to the edge and then to S3 on that private network is faster
- Used when you want to upload or download a file to from an S3 bucket that is far away from the users/client
- You can test speed gain by using the Amazon S3 Transfer Acceleration Speed Comparison tool

# AWS Global Acceleration
- Improves availability and performance using the AWS global network by leveraging AWS internal network to optimize the route to your application (60% improvement est.)
- Clients connect to an Edge location closest to them which then routes the traffic to the distant
 server or Load Balancer through the internal AWS network.
   - Uses Anycast IP static addresses which the client hits and is then redirected to the correct edge location
   - can use Global Accelerator Speed Comparison tool to see gains

# AWS Outposts
- Outpost Server Racks that AWS sets up on premise that come preloaded with AWS services
- Used for companies that are Hybrid Cloud and want to have some on premise servers and infrastructure as well as Cloud services.
- You are responsible then for the physical security of the rack, not AWS
- Low latency since it is on prem
- Fully managed service 

# AWS Wavelength
- Wavelength Zones - infrastructure deployments embedded in telecomm data centers at the edge of **5G Networks**
- Can deploy AWS services to the edge of the 5G Networks
  - The Zone belongs to the 5G network itself
- Purpose is to have ultra-low latency applications on 5G networks. 
  - I.e. you can deploy EC2 instances to the Wavelength zone
- No additional charges for using Wavelength
- Use Cases: Smart Cities, ML assisted diagnostics, Connected Vehicles, Interactive live video streams, AR/VR, Real time Gaming
-  application traffic from 5G devices can reach application servers running in Wavelength Zones without leaving the telecommunications network. This avoids the latency that would result from application traffic having to traverse multiple hops across the Internet to reach their destination, enabling customers to take full advantage of the latency and bandwidth benefits offered by modern 5G networks.

# AWS Local Zones
- allows you to define more granular locations within a region to launch instances from
- Selected services such as compute, storage and databases that are closer to end users to run latency-sensitive applications
- used as a extension to VPC AWS Region
- Ex:
  - Region: us-east-1 (N Virginia)
  - Local Zone: Boston, Chicago, Dallas, Houston, Miami...
    - Can extend the AZs from us-east-1 to one of the cities above and launch an EC2 instance into one of those local zones


# ARCHITECTURE:
- **Single Region** - instance in one region, easy to setup, but low latency due to one region
- **Multi Region** - instances across regions - lower latency improvement from more regions
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