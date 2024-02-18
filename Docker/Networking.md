# Kubernetes Networking

# Summary

- For pods you want exposed to the outside world use a service with `LoadBalancer` type
- For pods you only want to communicate within the cluster and not expose to outside world, use `ClusterIP` type service
- use the **CoreDNS** feature provided by k8s to hit endpoints internal to the cluster with environment variables: value should be `service-name.default:<port>` where service name is the metadata name for the service controlling the pod you want to talk to in the cluster

# INTERNAL POD COMMUNICATION

- add containers to one pod (in the same deployment file inder containers block)

- Make the endpoint a environment variable (use `environment` block in the docker-compose yaml where you use the container name to communicate and provide an `env` block where you use `localhost` in the k8s deployment yaml which is injected into your url in the source code (i.e. with `process.env.MY_VAR` for example))

- **Containers in the same Pod can access each other with `http://localhost:<container-port-exposed>` by default**

# MULTIPLE POD COMMUNICATION IN A CLUSTER

- one Pod can communicate with another in the cluster via it's internal Cluser IP address

- Need to use multiple services to allow Pod to Pod communication in a cluster

  - The services for the pods will maintain a stable IP Address for them which can be used to reach and communicate with the pod.
  - To find the IP Address of the service:
    - `kubectl get service` displays internal Cluster IPs for your services
    - **k8s provides built in environment variables to get these Cluser IP addresses when using a Service**:
      - k8s generates env variable composed of the service name (dashes are replaced with underscores) followed by `_SERVICE_HOST`. Ex: `process.env.AUTH_SERVICE_SERVICE_HOST`
      - **NOTE**: Make sure to change your environment variable name used in your docker-compose file/Dockerfile to match this generated name so that your injected var will work both in docker and k8s

- Create separate deployment templates for each container so they are in their own pods

- For the pod/container you do not exposed to outside world, use `ClusterIP` type Service for it. For the one you do want to expose to outside, use `LoadBalancer` type in the service

# CoreDNS: The preferred method for Pod to Pod communication

- Clusters by default come with built in service **CoreDNS**
  - A Domain name service that creates cluster internal domain names which are known inside the cluster
- The name you can use to communicate in a cluster is simply the service name (found in `metadata` of the service yaml template) followed by a dot `.` and the namespace
  - get namespaces with `kubectl get namespaces`
    - the `default` namespace is usually where your resources are assigned initially (i.e. if using MiniKube, that's where resources are assigned)
      - Example: `auth-service.default`
  - **NOTE**: You may need to add the port if you're not listening on the default port 80: `auth-service.default:8080`

in a deployment template then you could use an env variable to inject in the source code:

```yaml
# users-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: users-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: users
  template:
    metadata:
      labels:
        app: users
    spec:
      containers:
        - name: users
          image: brentgrammer/kub-demo-users:latest
          env: # injected into endpoint in src code to use to communicate with auth container
            - name: AUTH_ADDRESS # access with process.env.AUTH_ADDRESS for example
              value: "auth-service.default" # just use the name of the service.namespace controlling the pod you want to communicate with
```

- In your docker-compose.yaml file, remember to add a environment section

```yaml
# docker-compose.yaml
environment:
  TASKS_FOLDER: tasks
  AUTH_ADDRESS: auth # name of the other container listed in the `services` block
```

- use the env var in your source code:
  - Example: `http://${process.env.AUTH_ADDRESS}/login`

# Working with a Frontend

- Can use reverse proxying in your nginx configuration to forward requests to the cluster IP for the pod/service you want to communicate with:

```nginx
server {
  listen 80;

  # Reverse Proxy to prevent hardcoding Cluster IP in the fetch calls
  # we send a request to ourselves (the server serving the react app) and then this config forwards it to another address
  # note the TRAILING SLASHES on the routes - this is required to ensure correct forwarding
  location /api/ {
    # dedicated config for requests to this path /api
    # in the src code for react app you change your request to go to `/api/tasks` etc.
    proxy_pass http://tasks-service.default:8000/; # this evaluates to the Cluster IP to tasks pod in k8s.  If not listening on port 80, then you need to add the specific port (this service listens on port 8000)
    # Note that this configuration is parsed and runs in the container inside of the cluster unlike the React app which runs in the browser
    # so we can use cluster internal ip addresses provided by k8s CoreDNS
  }

  # all other requests use this config which serves the React app
  location / {
    root /usr/share/nginx/html;
    index index.html index.htm;
    try_files $uri $uri/ /index.html =404;
  }

  include /etc/nginx/extra-conf.d/*.conf;
}
```

- In the frontend source code:

```javascript
const fetchTasks = useCallback(function () {
	fetch("/api/tasks", {
		// path is set by the reverse proxy in the nginx config
		// reaches out to the tasks pod/service
		headers: {
			Authorization: "Bearer abc",
		},
	})
		.then(function (response) {
			return response.json();
		})
		.then(function (jsonData) {
			setTasks(jsonData.tasks);
		});
}, []);
```
