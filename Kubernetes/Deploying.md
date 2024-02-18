# Deploying to Production

- Can use your own data center (need to know how to configure everything)
- Use a managed Service

  - [kops](https://github.com/kubernetes/kops) is a tool used to install k8s software needed (ssh into your virtual machine instance)
  - Managed Services also offer full auto configuration for you to use k8s (example: AWS EKS)

## Configuring kubectl to talk to managed service

- based on a `config` file in your user folder in a `.kube` directory
- This file needs to be changed to talk to the service (i.e. AWS EKS cluster)
- You need to update this file (you can make a copy and save it as `config.minikube` to use it with MiniKube later again.)
  - Use a tool provided by your managed service to update the file (ex. AWS cli) and generate the necessary config

# Using AWS EKS

- AWS Elastic Kubernetes Service

  - different from AWS ECS (Elastic Container Service) is general for deployments not specific to k8s

## Process

- Go to EKS page in AWS page and create/name a cluster
- You need to provide a role to allow EKS to create ECS instances

  - Create a role for EKS service giving it permissions to do this
  - Go to IAM service and create a new role
    - select AWS Service
    - go down to go to EKS and select EKS cluster to create a predifined role
      - click Next: Permissions
    - click Next: Tags
    - click Next: Reviews
    - Give a role name (make it up, ex `eksClusterRole`) and click Create Role
  - Click refresh icon on select role field and select your created role
  - leave defaults and click Next
  - Create the k8s VPC network to allow for outside and internal communication of pods:
    - Click services and search for `Cloudformation` and open in a new tab
    - Select the url found on [this page](https://docs.aws.amazon.com/eks/latest/userguide/create-public-private-vpc.html#create-vpc)
      - copy and paste this into the Amazon S3 Url field on the Create Stack page and click Next
    - click Next again
    - Give the Stack name a name (make it up) and click next
    - can add tags optionally, but can leave defailts and click next
    - click Create Stack
  - Back in the EKS setup flow, click the Refresh icon next to VPC and select the one you created above
  - Under Cluster endpoint access section, select `Public and private` since we want internal protected communication as well as outside access to our pods. Click NEXT
  - Optionally configure logging and click NEXT (can leave off)
  - Review settings and click CREATE
    - this will create a k8s cluster on EKS with networking
  - Install AWS cli tool which is used to update the `<user>/.kube/config` file to talk to AWS eks with `kubectl`
    - Go to your AWS console and pull down menu on your account and select Security Credentials
    - Select Access Keys and create new access key
    - download the key file and open in text editor
    - in a terminal run `aws configure` and enter the keys in the rootkey file you downloaded from AWS, select the region you selected for your cluster (see upper right of eks screen) and select enter for default output format
    - Wait until your cluster in EKS shows `Active` and then run the command in the terminal: `aws eks --region us-east-1 update-kubeconfig --name kube-dep-demo` where kub-dep-demo is the name you assigned and us-east-1 is the matching region. This will update your `.kube/config` file for AWS EKS.
    - Now `kubectl` will be configured to talk to AWS EKS
  - Add the worker Nodes (that the cluster will live on)
    - In the EKS page for your cluster go to the `Compute` section
    - Select `Add a Node Group`
      - give the node a name (make it up)
      - Attach an IAM role to the Nodes (so they can do things like write logs and access other services and have permissions to do that etc.)
        - Open the `IAM Console` in another tab and create a role
        - Select `EC2` under Choose a use case and click Next: Permissions
        - Search for `eksworker` and add the `AmazonEKSWorkerNodePolicy` by clicking the checkbox
        - Also search for `cni` and add the `AmazonEKS_CNI_Policy` by ticking the checkbox
        - and search for `ec2containerregistry` and tick the `AmazonEC2ContainerRegistryReadOnly` policy
        - Click `Next: Tags` and `Next: Review` make sure you see the 3 policies
        - give the policy a name (`eksNodeGroup` for example) and click `Create Role`
      - Back in the EKS screen, regresh the Node IAM Role dropdown and select the role created above and click `Next`
    - Select which instances are spun up for you
      - Leave defaults but change Instances type to `t3.small` for cheaper costs if developing. (`t3.micro` causes errors)
      - optionally set scaling to number of nodes to spin up
      - click `Next`
    - On next screen you can optionally disable remote access if not needing to connect to the nodes via SSH and click `Next`
    - Review settings and click `Create`
  - Now k8s instances are setup and all software is installed on Nodes etc. for you

    - You can see your EC2 instances launched in the EC2 service page

  - Now you can apply your templates (on windows you might need to be in CMD prompt)
    - Note that a load balancer will be created by AWS for you if you used a `LoadBalancer` type in the k8s template yaml

- To find your public IP/endpoint use `kubectl get services`

## Volumes with Managed Services

- Use the `csi` volume type with managed cloud services like AWS etc.
- You can look up a package to use by searching for your cloud service/provider followed by `csi`
  - Example: "aws efs csi"
- You want to follow the install instructions to install the driver to your cluster via `kubectl`
- Remember to Create the folder you want to use before making the volume if it doesn't exist in your source code

## Using volumes with AWS EFS

- https://github.com/kubernetes-sigs/aws-efs-csi-driver
- Install the driver in your cluster via `kubectl`
  - `kubectl apply -k "github.com/kubernetes-sigs/aws-efs-csi-driver/deploy/kubernetes/overlays/stable/?ref=release-1.0"`
- Create an elastic file system for use with the volume
  - Go to AWS Console
  - Go to EC2 Management -> Security Groups
  - Click create security group
  - enter a name: i.e. `eks-efs` and enter a description
  - select the VPC you created for EKS in the dropdown field
  - Under `Inbound Rules` click `Add Rule`
    - Select `NFS` in the dropdown
  - Open Services -> VPC in another tab
    - Go to `VPCs`
    - Select your EKS VPC and select it to go to it's dashboard page
    - Copy the `IPv4 CIDR` ip address value and paste it into the Custom field back on the Add Rule/Inbound Rules section in the Security Groups page you had open
  - Leave outbound rules to default and click `Create security group`
  - Create a file system in your EFS service
    - Go to `services` -> `EFS` page and click `Create file system`
    - Give it a name and select your EKS VPC from the dropdown (so your file system is on the same network that your cluster is running on)
    - Click `customize`
      - Click Next on the first page
      - Remove the security groups selected and select your own eks-efs security group created for both availability zones
      - Click next until you get to Create and click it
      - On the list of file systems, copy the file system id
- Create the yaml template (StorageClass, PersistentVolume, PersistentVolumeClaim) and add volumes to your container:
  - Need to create a StorageClass resource: [See this example in the docs](https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/examples/kubernetes/static_provisioning/specs/storageclass.yaml)
    Example:
    (users.yaml)

```yaml
kind: StorageClass # taken from the example in the docs on their github page
apiVersion: storage.k8s.io/v1
metadata:
  name: efs-sc
provisioner: efs.csi.aws.com
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: efs-pv
spec:
  capacity:
    storage: 5Gi
  volumeMode: FileSystem
  accessModes:
    - ReadWriteMany # multiple nodes can use the volume
  storageClassName: efs-sc # need a specific storage class for Elastic File System.  Need to create this. Can create the StorageClass resource using the docs for your driver (look for the yaml file with it's config)
  csi:
    driver: efs.csi.aws.com # from the docs in the examples
    volumeHandle: fs-a7bdad52 # file system id from AWS
---
apiVersion: v1
kind: persistentVolumeClaim
metadata:
  name: efs-pvc
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: efs-sc
  resources:
    requests:
      storage: 5Gi
---
apiVersion: v1
kind: Service
metadata:
  name: users-service
spec:
  selector:
    app: users
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
---
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
        - name: users-api
          image: brentgrammer/kub-dep-users:latest
          env:
            - name: MONGODB_CONNECTION_URI
              value: "mongodb+srv://brent:youshallnotpass@cluster0.t5wfq.mongodb.net/users?retryWrites=true&w=majority"
            - name: AUTH_API_ADDRESSS
              value: "auth-service.default:3000"
          volumeMounts:
            - name: efs-vol
              mountPath: /app/users # path inside the container to mount the vol
      volumes:
        - name: efs-vol # can be any name you want
          persistentVolumeClaim:
            claimName: efs-pvc
```
