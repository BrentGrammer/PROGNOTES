# Kubernetes Volumes

- We must configure k8s to configure and create volumes for us (we can't use Docker or docker-compose since k8s is creatinga and running the containers, not docker)

- By default the volume lifetime depends on the Pod lifetime
  - Volumes are Pod specific and are removed when Pods are destroyed (there is a way around this)
  - Volumes survive container restarts and removal (within the Pod)
- More Powerful than Docker Volumes

  - supports many different drivers and types (can store data on different machines, environments etc. unlike Docker where the volume is just stored on one machine, the host machine)
  - supports Local volumes on Nodes(i.e. hard drive on a machine) and also Cloud specific volumes

### Example Volume Config in a Deployment template:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: story-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: story # match container created below
  template:
    metadata:
      labels:
        app: story
    spec:
      containers:
        - name: story
          image: brentgrammer/kub-data-demo:2
          volumeMounts: # makes volumes available to the container - define where the volume mounts
            - mountPath: /app/story # path on container where the volume mounts
              name: story-volume # indicates which named volume goes to this path
      volumes: # define volumes which all containers can use
        - name: story-volume
          emptyDir: {} # Key here (emptyDir) is a volume type.  Empty object means you use the default config
```

## Volume Types

[See List of Volume Types](https://kubernetes.io/docs/concepts/storage/volumes/)

- Determines how the data is stored outside of the container

Examples:

- **emptyDir**
  - Creates a new empty directory whenever the pod starts on the machine to store data.
  - If containers in a pod are restarted or removed, the data in the dir stays alive - it does not survive a Pod restart or crash
  - Not ideal if using replicas since if one Pod crashes and data is sent to it before that point and k8s switches to another pod, that data will be lost since volumes are pod dependent by default. (see `hostPath` below as an alternative for this)
  - Good for basic use with 1 replica or for testing things
- **hostPath**
  - allows us to set a path on the Node (the host machine) and that will be exposed to the different Pods
  - Multiple pods can share one path on the host machine instead
  - Specific to a Node (host machine)
  - Similar to a BindMount with Docker
  - Does not create a dir like `emptyDir` above for each Pod - you could use it to expose and share some existing data in a path on your machine to Pods.
  - **Downside** is that it is Node Specific - so multiple Nodes in a cluster will not be able to share the data. This works fine if on `MiniKube` for instance since there is only one worker Node, but if you move to `AWS` and have multiple machines/Nodes, you will lose data as it can't be shared across Nodes
  - Example config in a deployment template yaml:
  ```yaml
  spec:
    containers:
      - name: story
        image: brentgrammer/kub-data-demo:2
        volumeMounts:
          - mountPath: /app/story # where vol mounts on container
            name: story-volume # indicates which named volume goes to this path
    volumes: # define volumes in the pod which all containers in the pod can use
      - name: story-volume
        hostPath:
          path: /data # path on host machine(not container) where data is stored (path is up to you)
          type: DirectoryOrCreate # tells how the path should be handled - options are Directory or DirectoryOrCreate (will create it if it doesn't exist )
  ```
- **csi**
  - Flexible volume type
  - "Container Storage Interface" - designed so that anyone can build or derive their own solution that use this interface
  - Prevents the need for endless volume types for different services/contexts etc. Developers and services can build their own volume type to offer off of `csi`
- **Other Service Specific Types**
  - Providedd persisting of data independent of Pods and Nodes

# Persistent Volumes

- These volumes are independent of Pods and Nodes and survive recreation and destruction
- Allow for full admin control of configuration of the volumes
- Good for use on larger projects with multiple Nodes and Pods etc. - may be overkill for small personal projects
- One time configuration that can be shared across Pods/Nodes

  - You don't need to define config for the volumes in different deployment templates/multiple yaml files etc.

- A Peristent Volume(s) exists separate from your Nodes and Pods on the cluster
  - You need a `PerstistentVolumeClaim` that exists in a Pod to reach out to the Persistent Volume to request access to them (to determine if this pod can access the particular Persistent Volume)
    - The claim is a separate yaml template file
    - You can claim volumes by name ("Static Provisioning") or by resource details, i.e. by how much storage a vol has etc. ("Dynamic Provisioning")
- There are separate types you can use for Persistent Volumes with limitations.

  - For example, the `hostPath` type has a limitation that it can only be used with a Single node setup, i.e. with MiniKube during development or for testing)
  - `emptyDir` type is not available for persistent volumes

- Note: a Storage Class in k8s is used to tell how to provision a storage type and works with the Persistent Volume. A storage class comes with MiniKube setup and is sufficient for testing

## Make a Persistent Volume Template: Example

(host-pv.yaml)

```yaml
# Template for a Persistent Volume using hostPath type as an example.
# Note: the hostPath with PVs are only good for testing and single node environments

apiVersion: v1
kind: PersistentVolume
metadata:
  name: host-pv
spec: # config for the persistent Volume
  capacity: # define capacity of the path
    storage: 1Gi # specify capacity of storage resource (make sure not to exceed your service allowance)
  volumeMode: Filesystem # Filesystem or Block - 2 different storage types, with our path we're using a file system
  storageClassName: standard # specify a storage class which helps provision resources for the storage.  The name must match your storage class. Here we use standard which matches the default one that comes with MiniKube
  accessModes: # define how this pv is accessed. Can specify all ways it can be accessed and then specify which way is allowed in the pod claim
    - ReadWriteOnce # can be mounted with 1 or more paths, but all volumes are on the same Node
    - ReadOnlyMany # can be claimed by multiple Nodes can claim access
    - ReadWriteMany # can be claimed by more than one node, and includes write permisson
  hostPath: # enter key of volume type and then the config for it (hostpath is just for example)
    path: /data # path on host machine to keep the volume
    type: DirectoryOrCreate
```

## Make a Persistent Volume Claim Ex.

- This claim can now be used by Pods to make a claim to a particular Persistent Volume

(host-pvc.yaml)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: host-pvc # important for using it in a path
spec:
  volumeName: host-pv # specify which PV you want to make a claim to (matches name in host-pv.yaml)
  accessModes:
    - ReadWriteOnce # specify which access mode you want the pod to claim
  storageClassName: standard # specify a storage class which helps provision resources for the storage.  The name must match your storage class. Here we use standard which matches the default one that comes with MiniKube
  resources: # specify which resources you want to get with this claim
    requests:
      storage: 1Gi # don't exceed what your PV has
```

## Now specify the claim in the Pod yaml template:

(deployment.yaml)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: story-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: story
  template:
    metadata:
      labels:
        app: story
    spec:
      containers:
        - name: story
          image: brentgrammer/kub-data-demo:2
          volumeMounts:
            - mountPath: /app/story
              name: story-volume
      volumes:
        - name: story-volume
          persistentVolumeClaim:
            claimName: host-pvc # specify which claim you want to use and make (matches metadata name in your claim yaml)
```

## Now, run kubectl apply on the Persistent Volume Template FIRST, and then the claim, and then the deployment for the pod:

- `kubectl apply -f host-pv.yaml`
- `kubectl apply -f host-pvc.yaml`
- `kubectl apply -f deployment.yaml`

### To find pvs and claims, run

- `kubectl get pv`
- `kubectl get pvc`

## Troubleshooting

- For troubleshooting mssql persistent volumes: https://stackoverflow.com/questions/59886014/permission-denied-when-persisting-a-container-of-mcr-microsoft-com-mssql-server
