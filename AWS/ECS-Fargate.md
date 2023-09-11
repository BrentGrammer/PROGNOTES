# ECS Elastic Container Service
- Used to launch Docker containers on AWS
- You must provision and maintain the infrastructure in advance (the EC2 Instances)
  - need to create the instances in advance which will run the different docker containers registered in the ECS service
- AWS will take care of starting and stopping containers

# Fargate
- Also used to launch docker containers 
- Fully managed, serverless with no provisioning or infrastructure setup rquired
- Much simpler, runs and spins up instances and containers for you based on CPU/RAM you need 
  - You don't need to start EC2 instances yourslef to host the containers

# ECR - Elastic Container Registry
- Private Container registry on AWS
- Store images so they can be run by ECS or Fargate

