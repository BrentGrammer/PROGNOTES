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

## Startup Order

- Use `depends_on` to control when which containers are started

## Waiting for a Database to start

### Healthchecks

- NOTE: if you need to wait for a relational database service to start before the app can start serving requests, you need to use the conditiona and a healthcheck:
  - see https://docs.docker.com/compose/startup-order/
  - Can use [healthcheck](https://github.com/peter-evans/docker-compose-healthcheck) built into docker compose
    - Need to use the conditional depends on with `service_healthy`:
    ```yaml
    depends_on:
      database:
        condition: service_healthy
    ```
- NOTE: If using another db than the default in postgres, you NEED to specify the user and db name in the health check command, otherwise you get a `FATAL: role "root" does not exist` error

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -d db-name -U db-user"]
```

In the above snippet my db name is db-name and using a user db-user. I needed to specify this despite also setting the POSTGRES_DB & POSTGRES_USER env vars.

## Secrets

- You can reference secrets as environment variables if not wanting to hardcode them in the compose file.
- Create an .env file at the same level as the docker compose file
- Reference the variables with $ syntax:

```yaml
services:
  db:
    image: postgres:latest
    environment: # these need to be used in the connection string
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    healthcheck:
      test:
        [
          "CMD-SHELL",
          "pg_isready -h db -p 5432 -U ${DB_USER} -d ${POSTGRES_DB}",
        ]
      interval: 10s
      timeout: 5s
      retries: 5
```
