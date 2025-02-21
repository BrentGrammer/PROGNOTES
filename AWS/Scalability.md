# Scalability

- Adding or removing resources to a system based on customer load

## Verical Scaling

- Increasing the size of the server - resizing an EC2 instance
  - t3.large > t3.xlarge > t3.2xlarge
- Comes with downtime (i.e. restart of the instance) which can cause distruption
- Can only scale during pre-agreed planned times due to the downtime
- LArger and larger resources price increase is nonlinear
- Maximum possible ceiling to upgrade to.

### Benefits of Vertical Scaling

- Very simple to implement
- Works for all applications (including monolithic ones) since the app runs on an instance which can just be increased in size

## Horizontal Scaling

- Adds more instances instead of increasing size
- Means you will have more copies of your application running on smaller instances
- The load needs to be distributed among the instances with a Load Balancer
  - Shifts load between instances constantly
- No customer disruptions while scaling - constant up time
- Cheaper than vertical scaling (no large instance premiums, for ex.)
- Allows for granular scaling (with vertical increasing size can just automatically double the compute power, etc. which might not be as much needed)
- No limit to scaling like with vertical scaling ceiling

### Off-Host Sessions

- Sessions are very important in Horizontal scaling and must be stored somewhere else outside the instance
- Sessions represent the state of interaction of a user and the application
- You can't store sessions on one server/instance with horizontal scaling like you can with vertical scaling
  - Customer sequential actions could be split up to different instances by the load balancer, so sessions can't be stored on the instance
- In off-host sessions, the sessions are stored in an external database
  - The servers for your app become stateless

Vertical Scaling:

- ex upgrading hardware or a single component - like a t2.micro to a xlarge machine
  - Increasing instance size or decreasing it

Horizontal Scaling:

- Increasing the number of instances/systems for your application
- Implies distributed systems
- Load Balancers and autoscaling groups make scaling easy in AWS
- Scaling out is increasing, scaling in is decreasing

High Availability:

- related to horizontal scaling
- Running your application/system in at least 2 Availability Zones
  - i.e. to survive a disaster or data center failure

Elasticity: a system is scalable but has auto scaling based on load. Matches demand and is cost omptimized

Agility: not related to scaling - allows for easy access to IT systems that decrease development change time.
