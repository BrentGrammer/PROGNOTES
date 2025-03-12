# ECS Elastic Container Service

- Used to launch Docker containers on AWS
- You must provision and maintain the infrastructure in advance (the EC2 Instances)
  - need to create the instances in advance which will run the different docker containers registered in the ECS service
- AWS will take care of starting and stopping containers
- Accepts containers and instructions you provide. ECS then orchestrates where and how to run those containers

### ECS Modes

- **EC2 Mode**: uses EC2 instances as conatiner hosts
  - Can see these in your account - they're just EC2 hosts running ECS software
- **Fargate Mode**: SErverless way of running containers
  - AWS manages the hosts for the container

### ECS Clusters

- How ECS works is you create a cluster and then deploy Tasks or Services into that cluster
- ECS creates clusters which are where your containers run from
  - Provide ECS with an image. That image gets run in a cluster based on how you want it to run
- The images you want ECS to run must be located on a registry
  - Docker Hub or ECR (Elastic Container Registry)
- Tasks and/or Services are deployed into an ECS Cluster (EC2 or Fargate based)

### Container Definition

- See [docs](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ContainerDefinition.html)
- Defines the image (where it is, which registry, etc.) and ports exposed and used for a container
- This is what tells ECS where your container images are that you want to use
- Specifies to ECS which port your container uses (i.e. exposed port 80)
- Can be thought of as a pointer to where the container is stored and what port is exposed

### ECS Task Definitions

- see [docs](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_TaskDefinition.html)
- Represents a self contained application - stores whatever container definitions are used to make up an application
- Task can have one or many containers defined inside it (i.e. a web and database container etc.)
- Tasks store resources used by the task: CPU and memory, networking mode used by the task, compatibility with EC2 or Fargate mode and the **Task Role**
  - **Task Role** - an IAM role that any of the containers in a Task can assume and get temporary credentials which can be used to interact with AWS resources. It is best practice to use Task Roles
- Creating a task definition in AWS creates a container definition along with it (though they are architecturally seperate things)
  - Typically a task has one container
- Tasks do not scale on their own and are not highly available
  - Use an ECS Service configured via a **Service Definition**

### Service Definition

- Used to configure scaling and high availability for Tasks
- Defines how we want a Task to scale in ECS (i.e. how many copies to run), define restarts on failure, etc.
- Adds resilience since we can have multiple independent copies of the container and use a load balancer to distribute load acrosses all Tasks in a service
- Long running and business critical Tasks need to use the Service Definition to provide scalability and high availability for handling failed Tasks and distributing load

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
