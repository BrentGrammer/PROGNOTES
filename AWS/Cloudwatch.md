# CloudWatch

- Public service in the AWS Public zone

  - This means you can use it in VPCs or on premise environments, or other cloud platforms (with network connectivity and the right AWS Permissions)
  - Store, Monitor and Access logging data
  - For using outside AWS, Unified cloudwatch engine allows for any external sources to log data to Cloudwatch
    - For using with AWS, services can have built in AWS Integration

- 3 main parts/products:
  - Metrics
  - Events
  - Logs

## Cloudwatch Metrics

- Metric Filters can look for specific metrics in logs
- called "Datapoints" in AWS and are emitted over time
  - All have timestamps and a value (the metric itself)
- Provides metrics and operational data for every service in AWS
- Metric: a variable to monitor such as CPU Utilization or NetworkIN, billing etc
  - Default is metrics for every 5 minutes
    - Optional every 1 minute (Detailed Monitoring) for additional cost
  - Some metrics are automatically monitored by Cloudwatch
- Can be used to monitor metrics or perform actions based on metrics
- Can create Cloudwatch Dashboards to view all metrics at once
- Used to determine things like scaling in and out (looking at CPU utlization or network in and out)
  - NOTE: For EC2 monitoring RAM is not an available metric
- Cloudwatch can be accessed from anywhere (with permissions)

  - Can collect metrics from other cloud platforms or on prem environments with cloudwatch agents (installable)

- Metrics can be from any resources and are not user or machine specific necessarily
  - We use **Dimensions** which are name value pairs to separate things within a metric. (i.e. the EC2 instance ID and instance type sent as dimensions).
    - Use dimensions to filter metrics for particular instances etc.

### CloudWatch Namespaces

- A namespace is like a container for monitoring data.
  - A way to keep things organized and separated.
- All AWS data goes into a AWS namespace: `AWS/{servicename}` i.s. AWS/EC2
- You can make your own names (i.e. named after your app etc.) but cannot use the reserved AWS namespaces.

### Example Metrics

- EC2: CPU Utilization, Status Checks, Network (No RAM available)
- EBS Voluimes: amount of Disk Read/Writes happening
- S3 Buckets: Bucket Size Bytes, NumberOfObjects, AllRequests
- Billing: Total estimated charge (only available in us-east-1)
- Service Limits: how much you've beenusing a service API
- You can make CUSTOM METRICS

## Cloudwatch Events

- Two features:
  - If AWS service does something (terminated etc.), an event will be generated which can perform another action
  - You can generate an event to do something at a certain time of day or week.

## CloudWatch Alarms

- Created and linked to a specific metric
- Triggered notifications
- Examples:
  - Auto Scaling: increase or decreast EC2 instances to desired count
  - stop or terminate reboot/recover on fail a EC2 instance
  - SNS: send a notification
  - **Set a billing alarm on CloudWatch Billing metric** (**only available in us-east-1**)
- Can choose a period to evaluate whether to send an alarm
- Alarm States:
  - `OK` (everything is green)
  - `INSUFFICIENT_DATA` (starts in this state until enough data gathered or can't figure out whether to send alarm)
  - `ALARM` (sends alarm/sns notification/email etc.)

### Creating an Alarm

- AWS Console > Cloudwatch > All Alarms on the left > Create Alarm > Select Metric
- Example CPU for an EC2 instance:
  - Click EC2
  - Click Per Instance Metrics
  - Find the instance you want to add monitoring to and the metric (i.e. CPUUtilization for ex.)

## Cloudwatch Logs

- Regional service
- **Centralizes logs from your AWS resources**
- Can collect logs from:
  - Elastic Beanstalk - from application
  - ECS: collection from containers
  - Lambda - function logs
  - CloudTrail based on filter
  - Cloudwatch log agents: Install an agent directly onto EC2 machines or on premise servers to get the logs into AWS
    - On EC2 instances for ex., by default no logs from the instance will go to CloudWatch. You need to runa agent on EC2 to push the log files you want
    - Make sure the IAM permissions are set to allow the Cloudwatch agent
    - Hybrid agent - works on premise as well
  - Route53 - log DNS queries
- Allows for real time monitoring
- Adjustable retention - 1 week, 30 days, year, infinitely etc.

### Log Streams

- Store Log Events
- A log stream is a sequence of events from the same source (i.e. an API, EC2, database etc.)
  - For EC2 instances, each log stream represents one instance
- Configuration settings are stored on the log group and apply to all log streams in that log group
  - retention
  - permissions
- Metric Filters are defined in log groups
  - constantly monitors log events in the streams in the group that satisfy certain patterns
  - When a event that satisfies a metric filter criteria happens, the metric is incremented
  - Metrics can be associated with alarms that notify admins or other systems

### Log Groups

- Containers for multiple log streams for the same type of logging
  - I.e. a group of log streams for var/log events coming from different EC2 instances.

# Amazon EventBridge (formerly CloudWatch Events)

- Use case:
- schedule cron jobs - scheduled scripts that run every hour on a lambda, etc.
  - Can create a rule to run on a schedule (i.e. invoke lambda every hour)
- React to a service doing something (send an alert, etc.)
- Can use it to trigger lambda functions, SNS notifications, etc. from all sorts of source events from many different AWS services
- Default Event Bus - events happening from within AWS or your schedules
- You can also send events through a Partner Event Bus for events coming from external sources outside of AWS like DataDog or ZenDesk
- You can create Custom Event Bus to get events from custom sources
- Has Schema Registry where you can model the event schema
- Archive events (all/filter) sent to an event bus (indefinitely or periodically)
- can replay archived events
- You send an event and have a target
  - Example of EventBridge use: invoke an event to run a lambda function every hour. Targets can be different AWS services, in this case the target is lambda which will run on the scheduled hourly emitted event sent from EventBridge
  - EVENT PATTERN: Can also send an event whenever someone logs in to the AWS console for an account and target SNS target to send a notification whenever that happens for ex.
  - use an EVENT PATTERN: Get notified whenever a EC2 instance gets terminated - get a SNS notification

# CloudTrail

left off at 0:55

- Used to log and audit API/events calls or account activities made within your AWS account
  - Stopping an instance, changing a security group, create or delete S3 buckets, etc. - logs almost everything you can do in an account
  - These are called Cloudtrail Events
  - includes logging actions taken by a user, role or service
- Get history of calls/events made through - AWS console, SDK, CLI, AWS Services
- Can pipe logs into Cloudwatch Logs or S3
- Trails can be for all regions or region specific
- Example Use Case: Resource was terminated and you want to see the history to sxee who did it and understand why it was deleted
- 3 kinds of events:
  - Management Events: any change to AWS resource - configuring security, configuring roles, seting yup logging, etc.
    - By default, trails are configured to log Management Events ane this is free
    - Can separate read events (no modification to resource) or write events (may modify resources)
  - Data Events:
    - Not logged by default (high volume ops)
    - needs to be enabled by creating a new trail and it costs money
    - Ex., S3 objkect level activity (GetObject, PutObject etc)
    - Lambda functions execution activity
  - CloudTrail Insights events:
    - Helps you detect unusual activity in accounts
      - inaccurate resource provisioning
      - hitting service limits
      - bursts of AWS IAM actions
      - Gaps in periodic maintenance activity
    - have to enable it and it costs money
    - Analyzes activity to create a baseline and then monitors for abnormalities
    - Anomolies appear in CloudTrail console and can be sent to Amazon S3 and an EventBridge event can be automated (to send an email, notification etc)
    - Retention is 90 days. To keep longer, send them to S3 bucket and analyze them with Athena service

## Setting cloudwatch detailed monitoring on EC

- When creating an EC2 instance, you can go to Advanced Settings > Detailed Cloudwatch Monitoring > enabled
- NOTE: this comes with a cost and is not free.
