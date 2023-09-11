# Auto Scaling Groups
- Handles real time load variations
- Integrates with Load Balancers
- Goal is to Scale out or Scale in to match the current load.
- Ensures a minimum and max number of machiones running at one time
- Automatically spins up a desired number of instances based on a launch template
- Automatically registers or deregisters instances into a load balancer 
  - As you add more instances the ASG will add them to the load balancer registratrion
- Automatically replaces unhealthy instances with healthy ones
- Results in cost savings from running at optimal capacity depending on load.

### Setup for auto scaling groups:
- Requires a launch template for EC2s so it knows how to launch new instances
- Best practice is to set launch options for 3 availability zones (subnets in a VPC)
- Attach to a load balancer
- Assign a target group (create one if necessary) to the ASG
- Enable ELB Health Check

## Scaling Strategies:
- Manual scaling - update the size of a ASG manually
- Dynamic Scaling - auto scale based on load
  - Simple/Step Scaling: Set Cloudwatch Alarm for certain CPU usage threshold for a time and when that happens, add a number of instances to desired target
  - Target Tracking Scaling: Set a CPU usage goal (i.e. 40%) and ASG will automatically add or remove instances to meet and maintain this goal
  - Scheduled Scaling: Anticipate scaling based on known usage patterns (i.e. set the max capacity to 10 at 5pm on Friday in your setup)
  - Predictive Scaling: Uses machine learning to forecast and predict traffic and scale based on that.
    - useful for predictable time based patterned traffic scenarios