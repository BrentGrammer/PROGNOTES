# ECS Elastic Container Service

- Used to launch Docker containers on AWS
- You must provision and maintain the infrastructure in advance (the EC2 Instances)
  - need to create the instances in advance which will run the different docker containers registered in the ECS service
- AWS will take care of starting and stopping containers

### ECS Task

- A task is a blueprint for how you want to launch your container (i.e. not how it executes Docker run, but how the server that launches your container should be configured)
- A task can include more than one container
  - Note that if they are both web servers using the same port (i.e. port 80), you need to split them to separate tasks.
- A task can be thought of as a machine that launches one or more containers.
  - You can use Fargate by default which will launch the container in a serverless mode (an EC2 is not created immediately, but the settings are stored and when there is a request for the service, it will start up the container and stop the container afterwards which is more cost effective - i.e. lazy loading them)
  - An alternative option is to use EC2 which will spin up EC2 instances for your containers instead (they will remain up even if idle which can incur more cost)
- You can set up a load balancer for ECS which will handle the redirecting of requests to the container.
- You can have one "service" for task
- A "cluster" is a network for grouping multiple containers logically into one task/service so they can talk to each other.

# Fargate

- Also used to launch docker containers
- Fully managed, serverless with no provisioning or infrastructure setup rquired
- Much simpler, runs and spins up instances and containers for you based on CPU/RAM you need
  - You don't need to start EC2 instances yourslef to host the containers

# ECR - Elastic Container Registry

- Private Container registry on AWS
- Store images so they can be run by ECS or Fargate
