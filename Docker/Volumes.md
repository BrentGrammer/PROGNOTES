# Volumes and Bind Mounts

---

`docker run -v /app/data ...` -> Anonymous Volume <br>
`docker run -v vol_name:/app/data ...` -> Named Volume <br>
`docker run -v /abs/path/to/src/code:/app ...` -> Bind Mount <br>

---

- Volumes are folders **on your machine** (the host machine) that you make Docker aware of
- Volumes are mapped to folders inside a Docker container
  - _Any changes made in the volume are made in the mapped Docker container folders and vice versa!_
- **Volumes are NOT Removed when a container stops**

  - Changes in a volume persist
  - Possible exception is anonymous volumes which do not survive container removal (if you use the `--rm` flag in the docker command or remove the container, they do persist if the container is simply stopped)
  - A Container can write to and read data from a volume

- Two types of Volumes:

  - **Anonymous Volumes** (added to Dockerfile in example below and only exists as long as container is running - it is recreated on each container start)
  - **Named Volumes**
    - These persist and survive container shut down and removal, but are not meant to be accessed and edited by you

- run `docker volume ls` to show docker managed volumes (you can't find the location to mess with them though)

- **BIND MOUNTS**: The folders on your host machine are managed by you and not Docker
  - Used during development to prevent having to rebuild the image after any change on the host machine folder files

# Ways to Add a Volume to the container

### ANONYMOUS VOLUME:

- NOTE: these volumes are deleted on container shut down (when `--rm` is used) and recreated on each container start
- Cannot be shared across containers - specific to one container
- Good use case is for preventing the overwriting of certain folders by Bind Mounts (i.e. the Node Modules folder) and also for managing `/tmp` folders
- Add a VOLUME instruction to the Dockerfile of the container image:

(In your Dockerfile)

```yaml
VOLUME [ "/app/folderwithdata" ]
```

(In the command, just use the path to your container folder)
`docker run -v /app/data ...`

- In this example, the path entered is the folder in your docker Container you want to map to a folder on the host machine.
  - Docker in this case manages and creates the folder on the host machine

#### GOTCHA:

- volumes are removed automatically, when a container is removed.

This happens when you start / run a container with the `--rm` option.

If you start a container without that option, the anonymous volume would NOT be removed, even if you remove the container (with docker rm ...).

- you just start piling up a bunch of unused anonymous volumes - you can clear them via `docker volume rm VOL_NAME` or `docker volume prune`

### NAMED VOLUMES

- Will not be deleted by docker when container shuts down, survives shutdown and removal
- Can be shared across containers
- Can be re-used for the same container across restarts
- use the `-v` flag to specify a volume name and a path in the container of the folder to map to your machine

- `docker run -p 3000:80 --rm --name containername -v <volumename>:/path/in/container appname:tag`

<br>

---

<br>

# BIND MOUNTS

- Again, the definition is that a bind mount is a folder on the host machine, not in the container

- Used during development since changes made on your machine will be reflected in the mapped folders in the container in real time
  - With Volumes, only a snapshot of the folder on the host machine is taken and that is copied to the container
- Where with Volumes we don't know where the folder on our host machine the volume is mapped to, in Bind Mounts we control the folder which is mapped to files in the Docker Container.
- Bind mounts are perfect for persistent and editable data
- **NOTE**: Unlike Volumes, Docker will NOT overwrite the folders/files on your local host machine when changes are made in the container files. It is one way - files in the container are overwritten/modified if changes in the Bind Mount folder (your machine) are changed.

## Note on Deployment

- The bind mount is useful for development, but the container needs the latest copies of the files when it's being built for deployment. A dockerfile should be used to copy a snapshot of the files to the container so it has the latest versions on building in addition to having a bind mount for development. (the source folders in the bind mount will not exist on the deployed environment for example)

## Adding a Bind Mount

- Use the `-v` flag and set a **absolute** path to the folder on your machine to the container path to map to.

  - You can right click the file in VS Code and select `Copy Path` to get the absolute path
  - **TIP**: If you don't always want to copy and use the full path, you can use these shortcuts:

    - macOS / Linux: `-v $(pwd):/app`

    - Windows: `-v "%cd%":/app`

- Note: you can optionally wrap the entire volume mapping in quotes to avoid errors with spaces etc.

- **NOTE**: On Mac, you may need to go into `Docker Desktop -> Preferences -> Resources -> File Sharing` and make sure that a parent folder of the folder on your machine you're mapping volume to is included in the list. (on Windows this is not necessary if option is missing)

### MAPPING A FOLDER TO A BIND MOUNT:

- `docker run -p 3000:80 --rm --name containername -v "/absolute/path/host/machine:/app" imagename:tag`
  - Example if using Windows: `docker run -d -p 3000:80 --name f-app -v /path/our/machine:/app/feedback -v ${PWD}:/app feedback-node:volumes`

### GOTCHA: Overwriting and removing Node Modules

- If you map your source code folder to the /app folder in the container, remember that it overwrites everything that might have been copied in your Dockerfile (with `COPY . .`)

  - If you're missing node modules folder for example, then your container now no longer has the node_modules folder and the app will break

- **SOLUTION**: We need to tell Docker that there are certain files in the container that we do not want to overwrite or remove if there is a clash with the outside Bind Mount
  - add another `-v` entry to the command, an anonymous volume for the folder you do not want overwritten (i.e. the node_modules folder)
    `docker run -p 3000:80 --rm --name containername -v "/absolute/path/host/machine:/app" -v /app/node_modules imagename:tag`
- The Reason this works is because if there are multiple volume mappings, and a clash occurs, Docker will retain the volume that maps to the longer, more specific path in the container (in this case `/app/node_modules` is more specific than `/app` in the first `-v` volume mapping)
  - The anonymous volume has a directory created and managed by Docker containing our node_modules files

<br>

# DEBUGGING

- Remove the `--rm` flag to remove the container after shut down if you need to look at logs with `docker logs` to find an error
