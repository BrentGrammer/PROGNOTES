# ECS Elastic Container Service

- Used to launch Docker containers on AWS
- You must provision and maintain the infrastructure in advance (the EC2 Instances)
  - need to create the instances in advance which will run the different docker containers registered in the ECS service
- AWS will take care of starting and stopping containers
- Accepts containers and instructions you provide. ECS then orchestrates where and how to run those containers

### When should a business use ECS?

- If you use containers for anything (for production usage with a container)
- When using EC2 natively for an app (as a virtual machine)
- Using ECS in EC2 Cluster mode
- Using a containerized app but in Fargate mode

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

### When to use EC2 Mode or Fargate

- EC2 mode:

  - Pick EC2 cluster mode when the business has a large consistent workload/heavily using containers and the business is price conscious
    - Less price, but more effort (look at spot pricing or reserve pricing)

- Fargate Mode:
  - If you want to minimize overhead and admin, then Fargate makes more sense to use
    - Especially makes sense for small or burst workloads, or batch workloads, since you only pay for the container during usage
    - Having to manage a fleet of EC2 instances running for non-consistent workloads does not make sense in this scenario

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

# Cluster Modes

### Management Components

- These are components that are common to both EC2 and fargate cluster modes
- Handle high level tasks:
  - SchedulingandOrchestration
  - ClusterManager
  - PlacementEngine (which container hosts to host containers)
- Task and service definitions are also common to both cluster modes
  - (define the images, ports and resources to be used, etc.)

## EC2 Cluster Mode

- Not serverless (like Fargate) and requires some management (capacity awareness and availability of the cluster)
- Use if you need to host containers, but need to manage the capacity, availability.
  - i.e. if you have reserved EC2 instances or spot pricing deals, then you can use those EC2 instances to host your containers.
- You are expected to manage the container hosts (EC2 instances) in a EC2 Cluster
- Good middleground if you need some flexibility vs. a serverless option

### EC2 Cluster Mode notes

- An EC2 Mode Cluster runs within a VPC in your account
  - Benefits from multiple Availability Zones available in a VPC
- EC2 Instances are used to run containers in EC2 Cluster Mode
  - When creating a cluster, the initial size you choose controls the number of instances used (handled by an ASG (Auto-Scaling Group))
  - You can see the EC2 instances used in the account, you'll be billed for them and you can ssh into them, etc.
    - **NOTE**: You are billed for the instances REGARDLESS if there are containers running on them or not!
  - ECS provisions the instances for hosting your containers but YOU are responsible for managing them (typically via ECS tooling)
- Container images are stored in ECS container registries (Docker hub or ECR etc.)
- Basic arch:
  - Tasks and services use images (hosted on registries)
  - ECS deploys the images as containers into container hosts (EC2 instances)
  - If you use services and service definitions, ECS will handle the number of tasks deployed for you

# Fargate

- Also used to launch docker containers
- Fully managed, serverless with no provisioning or infrastructure setup rquired
- Much simpler, runs and spins up instances and containers for you based on CPU/RAM you need
  - You don't need to start EC2 instances yourslef to host the containers
  - The resources defined in your task/service definitions are allocated to the Shared Fargate Platform
  - These resources are "injected" into your VPC from a networking perspective (even though they are running on dedicated Fargate internal infra)
  - Each Task is injected into the VPC and given a Elastic Network Interface which has an IP address within the VPC which can be accessed from within the VPC or from the public internet if the VPC is configured that way.
  - Key takeway: **Tasks and Services are running on the shared Fargate infrastructure platform, but they are injected into your VPC (given network interfaces in your vpc) - you access these resources via the network interface**
- You only pay for containers you're actually using on the shared Fargate infra based on the resources they consume (only if they have containers running on them, etc.)
  - There is no visibility to you for host costs and you don't need to manage hosts, provision hosts or think about capacity or availability, etc.

## Fargate Cluster Mode

- You don't have to manage EC2 instances like with EC2 Cluster mode for hosts
  - This eliminates the possibility of paying for EC2 instances whether you're running containers on them or not.
- Your containers are hosted on a dedicated Fargate Shared Infrastructure (unlike with EC2 mode where you are running on EC2 instances)
  - This is separate and separates customers in that infrastructure just like you can be separated from other customers using EC2 instances.
-

### Creating a Fargate Cluster

[Deploying a container into a Fargate Cluster Demo](https://learn.cantrill.io/courses/1101194/lectures/36185027)

- Note: if creating a Fargate cluster for the first time in an AWS account you'll probably get an error. There is an approval process that must take place the first time, so just wait a few minutes and recreate the cluster the same way again and it should work the second time
- ECS > Clusters (left side menu) > Create Cluster
- Create a task - Task Definitions in the left menu > Create a new Task Definition (dropdown option)
- After creating the task definition go to Clusters > Tasks tab > Run Task to deploy the image
  - Make sure Fargate is selected in the Launch Type Dropdown (select Launch type first)
  - Set the Task Definition Family to what you named the cluster you created
  - Select the LATEST revision (1) to use the latest version
- When created an Elastic Network Interface will be created in the VPC and it will have a security group
  - Make sure the Security Group is appropriate and allows you to access the container
    - Select create a new security group - name and description should be the same - `somename-SG`
    - Add a rule (i.e. Type = HTTP, Source = Anywhere) to allow access publicly
    - Make sure the Public IP is toggled on for public internet access

### Stopping a container and deleting a cluster

- See timestamp 11:59 in https://learn.cantrill.io/courses/1101194/lectures/36185027

# ECR - Elastic Container Registry

- Managed Container Registry Service (like Docker Hub but for AWS)
  - Hosts images
- Private Container registry on AWS - Permissions are required for any Read or Write operation (unlike public registries where Reads are open to the public)
  - In public image registries (docker hub) anyone can read, but they need permissions to push and write to the repos.
- Store images so they can be run by ECS, EKS or Fargate
- In a ECR you can have numerous repos (similar to repos in a version control system)
  - In a repo you can have many container images
  - Images can have numerous tags (each tag must be unique within the repository)
- Integrated with IAM for permissions
- Basic Image Scanning
- Enhanced Image scanning (Inspector product) - can scan for issues in both the operating system and software packages
- Offers near real time metrics delivered to Cloudwatch (pull push operations are logged etc.)
- Delivers Events delivered to Event Bridge (can form part of an event driven workflow with images)
- Provides Replication across regions and across accounts
- For using ECR, all you need to do is specify the Amazon ECR repository in your task or pod definition for Amazon ECS or Amazon EKS to retrieve the appropriate images for your applications.

# Containers

### EC2 vanilla (no containers):

- EC2 Host on the AWS Hypervisor (NITRO)
  - This facilitates running multiple virtual machines on one host
- Each Virtual Machine is an Operating System with its own allocated resources
  - The Operating system takes a large amount of each VMs resources
  - Each virtual machine has it's own Operating System which could be the same as other VM operating system's on the host causing duplication

### Using Containers

- With containers on the other hand, a container engine runs on top of the Host Operating System and runs as a process in that host operating system
  - This is different from Virtualization using the NITRO Hypervisor where each VM has its own complete operating system
  - The container engine can isolate containers but use the host operating system for many things like networking and File I/O
- Each container has its own File System and can spawn its own child processes
- A container uses much less resources and is much lighter than a virtual machine on NITRO hypervisor because they do not need to run their own Operating Systems. All it needs is memory and disk for the application and the application's specific dependencies, i.e. runtime libraries and dependencies
  - **You can run many more containers on the same host and hardware than you can run virtual machines**
- Containers are very fast to start and stop

### Docker Image Construction

- Each line in a Dockerfile creates a new File System Layer inside the Docker image being created by it
  - For example, the base image is the first layer, and then installation of software is another subsequent layer stacked on top of it when that line in the Dockerfile runs
- Layers can be thought of as partitions and are Read Only and they contain the differences made when creating that Layer (only the changes for that layer are in that layer created)
- The end result is an image which consists of individual File System Layers
- Containers are just a running copy of an image, but it has an **additional Read/Write File System Layer**
  - The layers of the Image itself are Read Only and never change after they're created.
  - Docker containers have this additional layer added so it can run. Anything that happens like logs being written or I/O is all stored in this layer of the Docker container File System
  - All of the layers stacked up make what the container sees as a File System
  - Each container has its own individual Read/Write layer added when it's created from the same image and is what's keep things separate and isolated.
- Disk usage is minimized using layers (the common layers are shared except the read/write layer)
  - Many containers made from an image could be sharing the same base file system layer, for example
  - Large environments can benefit with less cost by using containers

# Comparison of ECS (EC2 Mode) with Containers vs. Direct EC2 Instance usage:

- Direct EC2 usage vs. using ECS in EC2 mode should be about the same cost, but you get more benefits using containers with ECS with less admin overhead and maintenance

#### ECS (EC2 Launch Type):

- ECS manages your Docker containers—handles deployment, restarts, and health checks automatically.
- You define a task definition (e.g., your Lucee app container) and ECS ensures it runs on your m5.large instance.

#### Direct EC2:

- You manually manage the Lucee app deployment—installing Tomcat, Apache, and Lucee, handling updates, and restarting services yourself (manual startup scripts, etc.).

### Scaling:

#### ECS (EC2 Launch Type):

- ECS can scale containers based on demand (e.g., run multiple Lucee containers on the same m5.large instance or add more instances via Auto Scaling).
- You define scaling policies (e.g., CPU usage > 70%).

#### Direct EC2:

- Scaling requires manually launching new instances, configuring them, and updating load balancers—more error-prone and time-consuming.

### Updates and Rollbacks:

#### ECS (EC2 Launch Type):

- Rolling updates are built-in.
- You update the task definition with a new container image, and ECS deploys it with zero downtime, rolling back if the new version fails.

#### Direct EC2:

- You manually deploy updates (e.g., copy new WAR files, restart Tomcat), risking downtime if something fails, with no automatic rollback.

### Monitoring and Recovery:

#### ECS (EC2 Launch Type):

- ECS monitors container health and restarts failed containers automatically.
- You can integrate with CloudWatch for logs and metrics.

#### Direct EC2:

- You must set up monitoring (e.g., CloudWatch) and recovery (e.g., scripts to restart Tomcat) yourself, which is more effort.

#### Why ECS EC2 is Same Cost:

- You’re using the same m5.large instance (~$71.62/month).
- ECS itself doesn’t add cost with the EC2 launch type.
