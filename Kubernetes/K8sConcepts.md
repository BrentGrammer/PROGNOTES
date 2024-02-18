# Kubernetes

- Kubernetes runs and manages containers

  - Kubernetes will run the container (we do not use docker or a docker-compose file)
  - Kubernetes runs and creates the containers from images pulled from a registry

- Pod: runs and executes a container or network/group of containers
  - When a pod is created, that means the container is executed (the pod runs the container underneath the hood)
  - Has a cluster internal IP address (this is used for communication and access within the cluster)
  - Containers inside a Pod communicate with each other via the `localhost` domain
  - Pods are **ephemeral** - data is not persisted when a pod is destroyed and all resources in the pod are lost. Volumes is one way to persist data beyond Pod destruction or shut down
- Node: A physical or virtual machine where Pods reside.

  - Worker Node: Contains pods, has Kubelet software for communicating with Master Node
  - Master Node: Manages the Worker Nodes, with Kube Control

- Cluster: The group of Nodes - Master Node with Worker Nodes

- Service:
  - an Object responsible for exposing pods to other pods in the cluster or the outside world (i.e. to the internet or network)
  - Example is a Proxy service
  - Are used to access pods both in and out of the cluster
    - When a pod is replaced, it's internal IP address changes (this can happen often via scaling etc.)
    - We need the service object to manage this and use it as a proxy for communicating and finding pods in a cluster
    - A service object groups pods together and gives them a shared IP address that won't change
    - The Service can expose this unchanging IP address inside the cluster or expose it to the outside world outside the cluster (**Services are required for reaching pods from the outside, i.e. the net)**
    - the type can be `ClusterIP` which will expose the deployment/pod inside the cluster (but not the outside world)
    - `LoadBalancer` type utilizes a load balancer(infrastructure must support one) which generates a unique address for the service and distribute traffic across all pods. This exposes the pod to the outside world.
    - The `selector` in the service.yaml must match the `label` for the template in the deployment.yaml

## All of these things are Objects

- An Object is something that contains instructions (i.e. in code) that is sent to Kubernetes to work with.
  - i.e. a `yaml` file represents an object, or the instructions embedded in an object sent to k8s

### The Deployment Object: an object that is sent to the cluster which manages and controls pods

- Manages Pods - handles crashes/restarts etc.
- It doesn't make sense to just send Pod objects to the cluster. The whole point of k8s is to manage multiple containers (i.e. pods) and orchestrate them
- A Deployment Object contains instructions on doing just that, so that is what is sent to the cluster as opposed to simply sending Pod objects.
  - Includes instructions on how many pods to create and control
  - Manages one kind of pod (multiple instances)
  - Multiple Deployments can be created
  - Is a Controller Object under the hood
- A Deployment object sets/specifies a desired state (how many pods and num of instances) and then k8s does what is necessary to reach that state
  - k8s will take the desired state of the deployment and determine which Node and resources to allocate for the creation of the Pod(s) specified by the deployment
  - k8s uses the desired state specified in the Deployment object sent to automatically manage and control the Pods
- Creates a pod with a container based on the image specified in the instructions (code) in the Deployment object. (an image needs to be specified)
