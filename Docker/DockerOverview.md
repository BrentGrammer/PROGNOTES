# Docker

## Virtual Machines vs. Docker Containers

### Virtual Machines

- Spinning up a virtual machine requires more resources and memory space than using containers
  - If you need multiple virtual machines, then each machine must spin up the OS, etc. (if you have multiple VMs that have the same OS like Linux, then all those machines need to spin up a Linux OS multiple times - redundant duplication and wastes space)
  - Virtual machines may have tools installed by default that you may not necessarily need - waste of resources and space
  - Machines are running on top of your machine
  - Requires configuration of the virtual machines in different environments (i.e. dev and prod)
  - Slower than containers due to larger resource use

### Containers

- Running Instances of an image
- Use built in emulated container support provided by OS (you do not spin up more machines inside your machine)
  - Docker engine is run on top of this support (the engine is one small lightweight tool used to spin up containers)
- Containers have a minimal OS layer and tools needed to run (much less than a Virtual Machine would require to be spun up)
- Can describe containers with a shareable config file or an image which can be shared across platforms and machines
  - (does not require additional config as you would need with virtual machines)
- Encapsulate environments, not whole machines like VMs do. (more lightweight)
- Run containers with the `docker run` command
  - **NOTE**
    - `docker run` creates a new container each time you use it.
      - when you run you need to expose the port of the container to access: `docker run -p 8080:8080 test` (your machine port is first then the container port)
    - `docker start` starts an existing container
  - `docker stop` command to stop a container
  - `docker rm` to remove a container
  - `docker rm $(docker ps -aq)` removes all containers
- Containers are a thin layer (i.e. a node process etc.) that uses the code and environment from an image (it is not a copy of the image code and files)

### Images

- Contain the code and required tools/runtimes/environment (the container executes these)
- Has the setup instructions which can be used to run the application/environment on multiple containers (i.e. on different machines and servers, etc.)
- Pre-existing images can be gotten from Docker Hub
- Create your own images with a Dockerfile
- Build images with `docker build` command
  - **\*\*\* Images are locked when you build them** (i.e. updating files that were copied will not update the image until you rebuild it - volumes are a solution to this)
- **IMAGE LAYERS**

  - Each command in a Dockerfile is a image layer which is cached. If you build the same image again, the result of each command or layer will be checked to see if it needs to be run again or if the cached result can be used
  - **GOTCHA**: When one layer is changed and needs to be re-run instead of using the cached result, all following subsequent layers (commands in the dockerfile) are re-run in full whether they need to be or not.
  - Common optimization is to `COPY package.json /app` and do `RUN npm install` **BEFORE** the `COPY . /app` command so that npm install layer is not invalidated on a srouce code change and is re-run everytime there is a change.

  ```yaml
  WORKDIR /app

  COPY package.json /app

  RUN npm install

  COPY . /app
  ```

  # Miscellaneous/Tips

  - Inspect a container to get info like IP Address of the container:
    - `docker container inspect <containerName>`
      - See IP in `NetorkSettings.IPAddress`

### Playground

- For experimenting without needing to use your machine: (https://labs.play-with-docker.com/)
