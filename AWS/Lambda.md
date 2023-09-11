# Lambda
- **Pricing is based on number of calls and duration**
  - Pay per request and compute time
    - 20 cents per 1 million requests after that
  - 1M invocations free per month with 400000GB of compute time
    - after that $1.00 per 600,000 GB
  - charged by the time run multiplied by RAM provisioned
- EVENT DRIVEN - invoked whem needed - a REACTIVE type of service
- Up to 10GB of RAM
- **Can run containers - must implement the Lambda Runtime API though**
  - **ECS and Fargate are the preferred ways of running containers**
  - Does not support arbitrary docker images
  - You can run without those services if you use the Lambda Runtime API in the image
- Lambda scales with the load automatically
- By default console will create a role with Cloudwatch logs permissions so you can view logs for the lambda.


## Common use cases
- Create a CRON Job serverless
  - i.e. from a Cloudwatch Event
- Create thumbnails for images uploaded to S3

- If you want to expose the function to the outside world, use API Gateway