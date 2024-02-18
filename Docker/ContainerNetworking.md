# Cross Container Network and Communication

## Http Requests from a Container:

- Works out of the box. No setup or config needed for WWW http requests sent from a container

## Communicating with non-containerized Services on the host machine (localhost)

- Replace requests to `localhost` with `host.docker.internal`
  - `http://host.docker.internal:<port>`
- requests to `localhost` from a container will fail
- the built in internal is translated to the ip address of your local host machine as seen from the docker container

## Container to Container Communication

- Use the IP Address of the container to communicate with for requests made **FROM The Container**:
  - Inspect a container to get info like IP Address of the container:
    - `docker container inspect <containerName>`
      - See IP in `NetorkSettings.IPAddress`
      - In source code of container making the cross container request: `http://<containerIPAddress>:<port>`

## USE DOCKER NETWORKS

- Elegant way of cross container communication
- Containers on the same network can communicate with each other

- Create a Network: `docker network create <network-name>`
  - `docker network ls`: inspect networks
- Run containers on the created network:

  - `docker run --name mycontainer1 --network <network-name> <image>`
  - `docker run --name mycontainer2 --network <network-name> <image>`

- Use the name of the container on the network created in the request url:

  - `http://<container-name>:<port>` (used in the source code of the container wanting to access another container on the same network)
  - The name resolves to the IP Address of the container

### NOTES/TIPS

- **Docker does not replace source code when resolving IP Addresses**

  - Only requests that are leaving the container are checked by Docker and resolved. Any requests that do not leave the container or are generated, for example, by the browser when a user makes a request from it, are not resolved.

- The default network driver used for docker networks is `bridge`

  - You can specify a different driver with `docker network create --driver <driver-name> <network-name>`
  - `bridge` network is used for most cases, but other options are:

    - `host`: For standalone containers, isolation between container and host system is removed (i.e. they share localhost as a network)

    - `overlay`: Multiple Docker daemons (i.e. Docker running on different machines) are able to connect with each other. Only works in "Swarm" mode which is a dated / almost deprecated way of connecting multiple containers

    - `macvlan`: You can set a custom MAC address to a container - this address can then be used for communication with that container

    - `none`: All networking is disabled.

    - Third-party plugins: You can install third-party plugins which then may add all kinds of behaviors and functionalities
