# Docker Compose

- V2 is the new recommended version.

## Required sections:

- services
- build (underneath named service)

### Optional

- Can set a `name` at the top of docker compose file:
  - `name: myappname`

### Using image and build together:

- Allowed in v2, but be aware:
  we can use build and image together, docker compose will name the new image with the value of image option. but there's a side effect --> it always trying to "pull" the image first(which doesn't exists because it's a custom name), then print error
- If you want to name the image, you need to build locally first with `docker build...` and then the image name will be used as specified in the docker compose file without pulling from a registry first. (it will see the image locally.)

## Example Docker Compose v2

```yaml
name: goapi

services:
  api:
    build:
      context: . # where the dockerfile is (relative path)
    container_name: examplegoapi # note this is for convenience - cannot scale with a custom name (ignored in docker swarm for example)
    ports:
      - 8000:8000 # {host-machine}:{container}
```
