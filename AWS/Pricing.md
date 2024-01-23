# Pricing

## Saving on Costs

- Read this article: https://usefathom.com/blog/reduce-aws-bill?s=03

# EC2

- On demand is minimum 60s and then pay for per second for linux windows or per hour for all others
- **For long term use, you should get a Reserved instance** - up to 75% less expensive and required 1-3 year commitment.

# ECS

- Pay for underlying instances that are spun up for your container cluster.
- The initial service itself is free.

# S3

- Data transfer out (retrieved) of region is pay for
- Transfer in is free (you do pay for number of and size of objects stored)

# EBS

- volume in GB per month provisioned

# Networking

- **Use a private IP instead of a public IP for inter EC2 instance communication for best savings (.01 cent per GB vs. .02)**
  - Across AZ, is free if using private IP, but more expensive if communicating across AZs
