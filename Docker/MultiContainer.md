# Multi Container Docker Apps

- Remember to use `host.docker.internal` to access your localhost domain on your machine outside of docker if apps need to communicate to an exposed port on another docker container via machine's localhost.
  - host.docker.internal translates to your machines IP (translated by Docker)

## Communication

- Containers can communicate with each other via the exposed/published ports
  - Ideally the containers should be set to a docker network
    - don't need to publish ports since containers can communicate via container name in the network(sufficient if only the containers need to talk to each other)
    - Except if you have outside applications that need to access the containers (i.e. a frontend app running in the browser), then you need to publish
  - Can use localhost on the machine, but you need to reference it from containers with the `host.docker.internal` docker keyword which translates localhost on your machine to an IP it can use.

## Creating a network

- `docker network create my-network`
- `docker run --name mycontainer --rm -d --network my-network myimage`
  - do this for all your containers. You can then communicate between them using the container name: `http://containername:port`
  - **The exception to this is if you want to expose a port to the outside to interact with** i.e. a React app in a container that publishes port 3000 to localhost so you can access it in a browser
  - **Exception** Frontend React or JavaScript code that runs in a browser cannot use the container name since it is running outside the container!
    - Need to ensure that containers are accessible to the frontend app on the browser. You need to publish the ports of target containers to the outside world.

## Volume setup

- For a backend app for example, we can create a bind mount for source code, a named volume for any other files you want to persist, and a anonymous volume for node modules so your local node_modules do not overwrite the ones on the container (if you want that)
  - `-v /path/to/src:/app -v applogs:/app/logs -v /app/node_modules`
- For react create a bind mount:
  - `-v /my/reactapp/src:/app/src`
  - Note on WSL 2 on windows: Need to create project files in linux system, not windows. See pdf in this project.

## Note on Bind Mounts for developing vs. Deployment:

- We need to copy files that are needed in the container for deployment and not just set a bindmount which is good for development. We should copy a snapshot of the files in a dockerfile config so they are available in the container for deployment.
