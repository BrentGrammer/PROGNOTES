# How to Delete k8s Resources from AWS

https://docs.aws.amazon.com/eks/latest/userguide/delete-cluster.html

In such situations, you will need to manually delete the resources that are causing the "delete failure" and then try the delete command again.

A good way to find such resources is to look in the Network Interfaces section of the EC2 management console. Make sure that there are no interfaces connected to the VPC.
from (https://stackoverflow.com/questions/55624583/cloudformation-stack-deletion-failing-to-remove-vpc)

# with eksctl

- install eksctl cli tool
- delete services with external ips via kubectl
- delete cluster with eksctl
  - `eksctl delete cluster --name <name>`

Ex:
(first delete services with an external IP address assigned with kubectl):

`kubectl get svc --all-namespaces` (check which ones have external IP values)

`kubectl delete svc users-service` (whatever names have an external ip value)

`eksctl delete cluster --name kub-dep-demo`
