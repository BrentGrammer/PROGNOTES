# AWS Batch
- Fully managed batch processing
- run 100,000s batch jobs efficiently
- Batch job has a start and an end (not continuous)
- Batch auto configures the right amount of compute and memory for the jobs
- You submit a schedule and Batch manages the rest
- Jobs are defined as Docker images and run on ECS

Differneces from Lambda
- Batch is not serverless (lambda is)
  - Batch is a managed service and relies on EC2 instances being created (it creates them, though)
- Batch has no time limit (lambda has 15 minute limit)
- Batch can run any runtime as long as it's a packaged as a docker image (lambda is limited to certain runtimes)
- Relies on EBS or instance store which offers a lot more than the temp memory storage provided by Lambda
- 