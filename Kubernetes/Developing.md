# MiniKube

- Tool for testing and developing k8s cluster locally

- Requires Hyper-V for windows (run `systeminfo` in a command prompt to see if you have a Hyper Visor)
- To start a cluster

  - `minikube start --driver=drivername` Eg, you can use virtualbox or docker if you have those installed (`minikube start --driver=docker` - this will create a container with a k8s cluster)
  - on Windows 10 you might use hyperv for the driver
  - [SEE DOCS for drivers you can use and the syntax](https://minikube.sigs.k8s.io/docs/drivers/)

- Delete a cluster: `minikube delete`

- Check running cluster: `minikube status`
- Kubernetes dashboard: `minikube dashboard`

## Create a Deployment

- `kubectl create deployment first-app --image=brentgrammer/kub-first-app`
  - **NOTE**: The image needs to be from a remote image registry (i.e. docker hub) since the image will be pulled from inside the cluster. (you can't specify images you build on your local machine because they cannot be seen from inside the k8s cluster on a virtual machine)
    - build your image: `docker build -t kub-first-app .`
    - Create a image on docker hub for your account
    - retag the image: `docker tag kub-first-app brentgrammer/kub-first-app`
    - login to docker: `docker login`
    - push to docker hub: `docker push brentgrammer/kub-first-app`
- To check deployment run `kubectl get pods`
- Expose a pod for access: `kubectl expose deployment name-of-deployment --type=LoadBalancer --port=8080`
  - The expose command creates a service for you
  - The LoadBalancer exposes the pod/deployment to the outside world. Note the infrastructure you use must support a Load Balancer - MiniKube does out of the box
  - The port should match what the app in the pod is listening to - in this case a node server listening on port 8080 for example
  - Check service with: `kubectl get services`
    - (with MiniKube the external ip will show as pending - this is expected)
    - You can map/expose a port that you can access on your machine by running:
      - `minikube service service-name` (NOTE: This is only for using Minikube during development on your machine)

## Pulling latest Images

- If you push a new image with `:latest` tag to your registry, but did not change your deployment template yaml, then you need to delete it (`kubectl delete -f deployment.yaml`) and reapply with `kubectl apply -f deployment.yaml` to get the latest image pulled
- If you made a change to your deployment yaml then everytime you apply it, it will pull the image with the `:latest` tag from the registry as long as you specify `:latest` on your image name in the deployment.yaml file

### Scaling

- `kubectl scale deployment/first-app --replicas=3`

  - Will manually scale the pods and create 3 instances of them
  - If you have a load balancer (i.e. your deployment is of type LoadBalancer), then traffic will be redirected automatically
  - Useful for maintaining access to your app if one pod crashes - traffic is redirected to a running pod instance

## Updating an image on a deployment

1. Create a repo on Docker Hub or registry to push your image to.
1. Docker Build the new image (optionally changing or updated the tag of not using the 'latest' approach): Ex for Docker Hub: `docker build -t yourname/image-name .`
1. push the image to Docker Hub or your registry `docker push yourname/image-name`
1. Update the deployment file to pull the latest tag if not using `latest`
1. Apply the deployment with `kubectl apply -f deployment.yaml`

- AFter making changes in source code, rebuild and push the image to docker hub or registry
  - **NOTE**: By default you need to tag the image with a new tag or k8s will not pull the image (`docker built -t brentgrammer/kub-first-app:2 .`; `docker push brentgrammer/kub-first-app:2`)
- `kubectl set image deployment/first-app curr-image-name=new-image-to-use`
  - You can find the current image name in the kubernetes dashboard
  - Ex: `kubectl set image deployment/first-app kub-first-app=brentgrammer/kub-first-app:2`
- Check status of deployment: `kubectl rollout status deployment/first-app`
  - If there is an error, then k8s will keep retrying to make an update. You need to rollback the requested update to stop this: `kubectl rollout undo deployment/first-app`
  - To go back to a earlier deployment:
    - `kubectl rollout history deployment/first-app`
    - get details on an earlier deployment: `kubectl rollout history deployment/first-app --revision=3` where revision matches the numbered entry of the deployments shown in the rollout history command above
    - `kubectl rollout undo deployment/first-app --to-revision=2` to revert to a specific deployment

# Declarative Approach

- Uses yaml files (like docker-compose for docker) so you don't have to write the commands manually

Example deployment.yaml:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: second-app-deployment
spec: # spec for deployment
  replicas: 2
  selector: # required: used to find and select which pods to be controlled by this deployment (i.e. if pods are scaled up after deployment is created)
    matchLabels:
      app: second-app # should match labels set on your pods below, can list multiple labels(no dash)
    # matchExpressions:

  template: # template always describes pods you want created (the kind is Pod)
    metadata:
      labels:
        app: second-app # label key and value can be anything you want
    spec: # this spec is for the pod
      containers:
        - name: second-node # add a dash `-` for each container entry
          image: brentgrammer/kub-first-app:2
          imagePullPolicy: Always # optional: you can make changes to your image and push it under the same tag and k8s will pull it - otherwise k8s will not pull the changed image with the same tag. Note: By default adding :latest tag to the image value here will always pull that image (with :latest tag) *WHEN something changes about the deployment config*!!!
          livenessProbe: # optional, check health of the container if desired or needs to be defined in a custom way
            httpGet:
              path: / # send a health check request to this path
              port: 8080 # send to exposed port on container
            periodSeconds: 10 # interval to perform health check
            initialDelaySeconds: 5 # how long to wait before first check
```

- apply this with: `kubectl apply -f=deployment.yaml`

Now you need a service yaml configuration to expose the deployment

Example service.yaml:

```yaml
apiVersion: v1 # in service it's just v1 not apps/v1 like in deployments
kind: Service
metadata:
  name: backend
spec:
  selector: # indicates which other resources are connected/controlled by this resrouce- select individual pods: only matches by label so `matchLabels` is not needed here
    app: second-app # should match the labels in your metadata for the pods- these pods will be exposed by this service
  ports:
    - protocol: "TCP"
      port: 80 # port exposed to outside world
      targetPort: 8080 # requests to 80 from outside world are forwarded to this port on the pod/container (in this case a node app listening on 8080)
  # - protocol: "TCP" can expose multiple ports
  #   port: 443
  #   targetPort: 443
  # NOTE: it is not uncommon for the targetPort and port to be the same. If your container is exposing a different port then you want to put that here - traffic to the port is forwarded to targetPort
  type: LoadBalancer # ClusterIP - interal exposing, NodePort are other options, LoadBalancer gets you an address reachable from outside and automatic traffic redistribution
```

- `NodePort` - access a Node from the outside world - the cons are that it does not maintain steady IP addresses across Nodes. `LoadBalancer` does.
- `LoadBalancer` is the type for exposing a pod to the outside world (the internet)
- `ClusterIP` is for internal pod communication and will automatically load balance and redirect traffic between the pods.

- now run `kubectl apply -f service.yaml`

- If developing with MiniKube locally, expose this with `minikube service backend` to get a address to use locally and access it in the browser etc.

### Selectors

- This entry in your config yaml files denotes by label which resources are connected with or controlled by the object. i.e. a Service selects pods which are controlled by it, and a Deployment selects the pods it controls and manages etc.

## Using Environment Variables:

- add an `env` block with `name` and `value` key/value pairs
- In the source code for a node server for ex. you can access the var on `process.env.STORY_FOLDER`

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
          env:
            - name: STORY_FOLDER
              value: "story" # name of the folder, matches your mountPath - now we only need to change mountPath here and folder in app.js will change (accessing process.env.STORY_FOLDER)
          volumeMounts: # makes volumes available to the container - define where the volume mounts
            - mountPath: /app/story # path on container where persistent data exists you want to keep
              name: story-volume

      volumes:
        - name: story-volume
          persistentVolumeClaim:
            claimName: host-pvc
```

### Create a ConfigMap for storing Environment Vars you can use across templates:

(environment.yaml)

```yaml
apiVersion: v1
kind: ConfigMap # resource for creating key val pair list of configurations
metadata:
  name: data-store-env # we're storing env vars for storing data in here
data: # start listing your config/env vars here <name>: <value>
  folder: "story"
  # key2: 'value2'
  # key3: 'value3'
```

- now apply it with `kubectl apply -f environment.yaml`

- In your `deployment.yaml` template for the Pod, add the `env` block in the spec as so:

```yaml
env:
  - name: STORY_FOLDER
    valueFrom: # uses a ConfigMap(separate yaml) resource to get the value
      configMapKeyRef:
        name: data-store-env # name of configMap from metada of yaml file for it
        key: folder # gets value for 'folder' in the ConfigMap
```
