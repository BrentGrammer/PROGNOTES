# Auto Scaling Groups

- Handles real time load variations
- Integrates with Load Balancers
- Goal is to Scale out or Scale in to match the current load.
- Ensures a minimum and max number of machines running at one time
- Automatically spins up a desired number of instances based on a launch template
- Automatically registers or deregisters instances into a load balancer
  - As you add more instances the ASG will add them to the load balancer registratrion
- Automatically replaces unhealthy instances with healthy ones
- Results in cost savings from running at optimal capacity depending on load.

### Setup for auto scaling groups:

- ASGs main job is keeping the number of instances at the desired number setting.
- Requires a launch template or a lauch Configuration for EC2s so it knows how to launch new instances
  - Has one template or version of it. You can change which one the ASG is associated with.
  - Min size, desired size, max size are the main parameters. Ex: 1:2:4 means 1 min, 2 desired and 4 max
- Scaling policies can be created to automate scaling based on criteria (CPU usage for example)
- Best practice is to set launch options for 3 availability zones (subnets in a VPC)
- Attach to a load balancer
- Assign a target group (create one if necessary) to the ASG
- Enable ELB Health Check

### Definition

- ASGs define where instances are launched.
  - Linked to a VPC
  - Subnets within that VPC and linked to an auto scaling group

## Scaling Strategies:

- Manual scaling - update the size of a ASG manually

### Dynamic Scaling

- auto scale based on rules:
  - Simple - a pair of rules, one to add and one to remove instances \*i.e. CPU utilization. Metrics might need Cloudwatch installed.
  - Step Scaling: set of rules to act depending on how out of normal a metric ist.
    - Set Cloudwatch Alarm for certain CPU usage threshold for a time and when that happens, add a number of instances to desired target
    - Preferrable to Simple scaling in most cases
  - Target Tracking Scaling: Set a CPU usage goal (i.e. 40%) and ASG will automatically add or remove instances to meet and maintain this goal
    - avg network in or out
    - request count per target (relevant to application load balancers)

### Cooldown Period

- Time in seconds - controls how long to wait at the end of a scaling action before doing another.
- Meant to avoid costs with constantly adding instances (since there is a minimum bill for each instance spun up)

### Health checks

- If an instance fails, the ASG will terminate it and provision a new instance to replace it. (Self Healing)
- If you terminate an instance, ASG will auto create a new one to replace it to match desired setting.
- left off at 9:32 https://learn.cantrill.io/courses/1101194/lectures/27895172

### Scheduled Scaling:

- Anticipate scaling based on known usage patterns (i.e. set the max capacity to 10 at 5pm on Friday in your setup)
  - useful for known periods of high or low usage.

### Predictive Scaling:

- Uses machine learning to forecast and predict traffic and scale based on that.
  - useful for predictable time based patterned traffic scenarios

### Simple Instance Recovery

- Use with EC2
  - Cheap simple and effective high availability
- create a launch template to auto build an instance
- Create an Auto Scaling Group using that template
- Set the ASG to use multiple subnets in different Availability Zones
- Set the min, max and desired to 1
- Doing this gives you simple instance recovery
  - Instance recreated on failure or termination
  - Instance can be re-provisioned in another AZ if the original fails.

## Integration with Load Balancers

- Use an ASG to integrate with a target group (associated with a Load Balancer)
  - Load balancers will be associated with or point to target groups of instances

### Elasticity enablement

- As instances from the ASG are provisioned, they will automatically be added to the target group for the load balancer.
- As instances are terminated, then they will be removed from the target group
- This allows for fluid scaling based on metrics as the instances for the load balancer target group are scaled dynamically.

### Load Balancer Health Checks

- ASG can be configured to use the load balancer health checks rather than the EC2 status checks.
- The LB checks are much richer as they can monitor the status of HTTP and HTTPS requests - they are application aware (unlike simple EC2 status checks).
  - Careful about using appropriate health checks: if you just check static HTML, but app has complex other logic that fails, you will not know about that failure
    - Or if you have a check for data from a database in the app, but the database fails, the health check will fail and instances terminated and re-provisioned when the problem is not with the app, but with the database.

## Scaling Processes

- Processes can be set to "Suspend" or "Resume"

### functions

- Suspend:
  - Launch - ASG won't scale if alarms fire
  - Terminate - if terminate set to suspend, then no instances will be terminated if alarms go off.
- AddToLoadBalancer: determines if any instances provisioned are added to a load balancer.
- AlarmNotification: Determines if ASG will react to any cloudwatch alarms.
- AZRebalance: determines whether instances are distributed evenly across AZs
- HealthCheck: determines whether health checks on instances are on or off.
- ReplaceUnhealthy: determines if ASG will replace instances marked as unhealthy.
- ScheduledActions: determines if ASG will perform any scheduled actions or not.
- Standby/In Service: Set a specific instance in the ASG to stop all actions if needed. (Maintenance on an instance for example if you need to do that.)

## Cost

- ASGs are Free
- Only costs are for the resources created by the ASG
- Use cooldowns in the ASG to avoid rapid scaling and reduce costs
- \*Use more smaller instances - gives you more granular control of the compute and costs of the ASG.
  - i.e. use 20 small instances instead of 2 large instances. You can increment adding compute in smaller steps etc.

## Elastic Architecture

- Use Application Load Balancer for elasticity and to abstract the resources created by ASG away.
- ASGs control the WHEN and the WHERE - when instances are launched and what SUBNETS they are launched into.
  - Launch Templates and Configurations define the WHAT - what instances are launched and what config they have.
