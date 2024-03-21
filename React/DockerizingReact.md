# Dockerize a React app

- [see video](https://www.udemy.com/course/docker-kubernetes-the-practical-guide/learn/lecture/22626687#search)
- Use a multi-stage build setup
  - We only need a node image to initially build a React application
  - If using a node server to serve the app, then in that case you do need a node image. (otherwise you can use nginx which is a more light weight server)
- You will want a development docker file and a production dockerfile

  - `Dockerfile` for dev
  - `Dockerfile.prod` for production

- using `npm ci`:
  - npm ci does install both dependecies and dev dependencies. But if you use npm ci --production or if your NODE_ENV is set to production, then it avoids installing dev dependencies.
  - see [thread](https://stackoverflow.com/questions/60065865/is-there-a-way-of-making-npm-ci-install-devdependencies-or-npm-install-not) for more information on latest commands and recommendations
  - alse see [this thread](https://stackoverflow.com/questions/65234362/should-i-copy-package-lock-json-to-the-container-image-in-dockerfile)

### Dockerfile.prod

```Dockerfile
# use the as instruction to reference the changes in this step so they are not discarded
FROM node:14-alpine as build

WORKDIR /app

COPY package.json .
# TODO: do we need package-lock as well?
# COPY package*.json .
# COPY package.json package-lock.json .
# # Run `npm ci` _before_ copying the application in
# RUN NODE_ENV=production npm ci
# # If any file in `dist` changes, this will stop Docker layer caching
# COPY ./dist ./dist

# install deps
RUN npm install

COPY . .

# create build artifact which will be served from the server
RUN npm run build

# optional: extra stage for running tests

# Every FROM statement creates a new stage even if you use the same image as in the previous step
# switch to using nginx image:
FROM nginx:stable-alpine

# copies final content/output from the build stage above
# the --from tells Docker we are not referring to our source folder to copy from, but from the stage context above. you can specify a folder to copy from (in the above stage context, i.e. where the build was ouptut in app/build)
# we copy the build artifact into a special html folder (nginx defined) that is where you put where you want to serve static content.
COPY --from=build /app/build /usr/shared/nginx/html

# nginx exposes port 80 by default, so we expose that port on our container:
EXPOSE 80

# start nginx, use the -g daemon off flag as per the documentation
# this prevents the container from stopping immediately after nginx starts and keeps nginx in the foreground so Docker can track the process properly.
CMD ["nginx","-g","daemon off;"]
```

### Dockerfile (for development)

```Dockerfile
# use the as instruction to reference the changes in this step so they are not discarded
FROM node

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

# this is the port that react app is served on in development
EXPOSE 3000

# use development command to start in development mode
CMD ["npm","start"]
```

### Docker Compose

- Used in development to orchestrate multi containers (i.e. frontend and backend) with one command.

```yaml
version: "3.8"
services:
  # example backend config if you have a node server for ex.
  backend:
    build: ./backend
    ports:
      - "80:80"
    volumes:
      - ./backend:/app
      - /app/node_modules
    env_file:
      - ./env/backend.env
  # config for react frontend:
  frontend:
    build: ./frontend # this will reference the location of the Dockerfile
    ports:
      - "3000:3000" # in development port 3000 is where react app is served
    volumes:
      - ./frontend/src:/app/src # maps source code on local machine to container so changes are reflected in development with container running
    stdin_open: true
    tty: true
    depends_on:
      - backend # react app won't work without a running backend - so ensure that container is spun up first.
```

## Building the image

- Create the image locally and push it to a container registry (i.e. Dockerhub)

### Building the image locally

- cd into the folder with your dockerfile - specify the dockerfile with -f if needed (i.e. for Dockerfile.prod)
  - Include the path to the dockerfile after the -f flag and the path for the context of the build command (i.e. where the dockerfile for it is located or **the context where the commands in the dockerfile will be executed**)
- `docker build -f ./Dockerfile.prod -t yourdockeracct/imagename .`

### Push the image to registry

- `docker push yourdockeracct/imagename`
- You can use this image to deploy

# Dockerizing NextJS

- Use a docker file provided by NextJS
  - see [video](https://www.youtube.com/watch?v=BkHULo3w13k) at timestamp 1:35 for corrections to make to it.
