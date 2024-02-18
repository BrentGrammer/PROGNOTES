# Deploying to Production

## Note on Bind Mounts:

- You should NOT use bind mounts in production. You need a COPY step in the Dockerfile to copy the latest snapshot of source files to the container when it's built
  - We need to copy files that are needed in the container for deployment and not just set a bindmount which is good for development. We should copy a snapshot of the files in a dockerfile config so they are available in the container for deployment.
- For single container apps without docker-compose, the bind mounts are set in the docker run command (`-v`) during development, so in production a different command is used that does not do this.

# Remote machine (on AWS EC2 instance for example) - most manual process:

- Create and launch instance, Ex AWS: VPC and security group
- configure security group to expose ports to the internet
- SSH into the remote server and install Docker and run container
  - install Docker on the remote machine
    - update system, ex on aws: `sudo yum update -y`
    - install docker (for example on amazon ec2 instance they have a built in tool: `sudo amazon-linux-extras install docker`)
      - (See instructions for various OS here)[https://docs.docker.com/engine/install/#server]
    - start docker (ex aws ec2: `sudo service docker start`), and then you can run docker commands

# Building image and running the container

- Best to build image outside of remote machine and just run it on the remote.
  - Build your image and push it to a registry like Dockerhub
    - remember to rename it with `docker tag <originalimagename> <dockeruser/reponame>` so you can push it to dockerhub if you want (`docker push dockeruser/reponame`).
  - Pull the image from the registry and run it on the remote machine
- Make sure you have a dockerignore file to prevent copying or using your secrets like a .pem file for aws or node_modules
  - ```
    node_modules
    Dockerfile
    *.pem
    ```

## Updating your code on the remote machine

- Build the new image on local machine
- rename/tag it to match your repo (i.e. dockerhub repo) with `docker tag`
- Push the image to your remote image repo with `docker push ...`
- Pull the latest version of the image on the remote machine with `docker pull <imagetag>`
- Shut down the container running the old image
- Start the container using the latest pulled image with `docker run ...`
