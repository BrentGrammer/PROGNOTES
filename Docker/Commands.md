# CLI Commands

## Logs

- docker logs <containerid/name>

## Attach to a detached container

- docker container attach <container>

## Start in interactive mode

- docker run -it <container>

## Exec - run commands not specified in the Dockerfile

- docker exec <runningcontainername> <cmd>
  - `docker exec -it node-container npm init
    - (-it (optional) puts you in interactive mode to provide input if necessary)
- Could be useful for things like reading log files, etc. without interrupting the container CMD

## Override default CMD that runs when a container starts:

- docker run <containerimage> <cmd>
  - ex: `docker run -it node npm init`
- Overrides the CMD in the Dockerfile and replaces it.
  - use ENTRYPOINT in the dockerfile to just have it append to it and not replace it

## prune Volumes Images Containers

- docker volume prune
- docker container prune
- docker image prune

## Shell into a container:

- docker exec -it <container name> sh

## Building

- `docker build -f ./Dockerfile.prod -t yourdockeracct/imagename .`
- Target a stage in a multi-stage dockerfile: `docker build --target <stage-name> -f ./Dockerfile.prod .`
  - Useful if you want to just run a stage and stop in a dockerfile (testing etc.)

# Docker Compose

- docker-compose run --rm <service-name> <cmd>

  - **docker-sompose run will build the container if it does not exist (unlike docker run command which requires a docker build first)**
  - Runs a single service part of a docker-compose.yaml file and passes in a command (optional)
  - Removes containers after they shut down automatically --rm
