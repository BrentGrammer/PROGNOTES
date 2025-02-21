# CloudWatch

- [Overview Video](https://learn.cantrill.io/courses/1101194/lectures/27914996)

- Public service in the AWS Public zone

  - This means you can use it in VPCs or on premise environments, or other cloud platforms (with network connectivity and the right AWS Permissions)
    - Usually accessed via internet gateway or interface endpoint (doesn't require a gateway to allow VPC services to publish into CloudWatch) within a VPC
      - **Note - EC2: External visible metric data only. For anything inside the instance, you need to use a Cloudwatch Agent (for monitoring disk space, CPU, memory, Requests, Latency, Errors in the instance, etc.)**
        - Once data is in CloudWatch, can be used to create alarms via SNS notifications, or a starting point to handling via EventBridge.
    - Most services are integrated with Cloudwatch without any additional user configuration required
  - Store, Monitor and Access logging data
  - For using outside AWS, Unified cloudwatch engine allows for any external sources to log data to Cloudwatch
    - For using with AWS, services can have built in AWS Integration
  - For Exam: **Anything that required internal observation of metrics requires an Agent**

- ### 3 main parts/products:
  - Metrics
  - Events
  - Logs

## Key Terms in CloudWatch

### CloudWatch Namespace

- A container within CloudWatch
  - Note: AWS uses this concept for many services (i.e. for EC2, the namespace is `AWS/EC2`, lambda is `AWS/Lambda`, etc.)
  - AWS Namespaces ALWAYS start with `AWS/`, while the namespaces you create will not start with that

### Datapoints

- Smallest component of Cloudwatch, individual points of data that are being monitored
  - they have a value (i.e. 42, or 42% of CPU usage)
  - have a timestamp to represent when the value was taken
  - (optional) Unit of Measure, i.e. "percent"

### CloudWatch Metrics

- Time ordered set of Datapoints
  - Ex: `CPUUtilization`, `NetworkIn`, `DiskWriteBytes`
- Have a Metric Name and a Namespace: Ex: `AWS/EC2 CPUUtilization`
  - This can get difficult with different EC2 instances, for example, so that's where Dimensions come in (see below)

### CloudWatch Dimensions

- A name/value pair that is provided to you when you add Datapoints into CloudWatch
  - You provide: Value, Timestamp, Unit of Measure, Namespace, Metric Name, **0 or more Dimensions**
- The purpose is to differentiate between instances of AWS Resources (i.e. EC2 instances)
  - `Name=InstanceId, Value=i-11111111`
- Allow for aggregation of data for a Metric. (i.e. for a single instance or for all instances across an AutoScaling group)

### CloudWatch Resolutions

- The minimum period specified you can get a metric value for
- By default, the Standard Resolution is 60-second granularity
  - Example: if you have a resolution of 60 seconds, a mteric that is taken when there is 42% CPU Uitilization would show that the instance had that utilization for the entire 60 seconds.
- High resolutions have a higher monetary cost. (have 1-second resolution)
  - Can retrieve high resolution metrics in periods of 1 second, 5 seconds, 10 seconds, 30 secs or any multiple of 60 seconds

#### Data Retention

- Any resolutions less than 60 seconds: Data is retained for only 3 hours
- For 60 second resolution, data is retained for 15 days
- 300 seconds (5 minutes): retained for 63 days
- 3600 seconds: retained for 455 days
- **As data ages, it is aggregated and stored for longer periods with less resolution**
  - Ex: metrics stored at 1 second resolution will be stored for 3 hours at that resolution, then they will be stored for viewing at 60 second resolution for 15 days, 5 minute resolution for 63 days, and 3600 second resolution for 455 days

Statistics: Aggregate over period of time (metric averages, minimum, maximum, etc.)
Percentiles: Indicates the relative standing of a value in a dataset (95th pecentile = 95% of data is lower than that value and 5% of the data is higher) - helps to identify a normal value or range for a percentage of a dataset

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

- Created and linked to a specific metric over a specified time period
- Triggered notifications
- Examples:
  - Auto Scaling: increase or decreast EC2 instances to desired count
  - stop or terminate reboot/recover on fail a EC2 instance
  - SNS: send a notification
  - **Set a billing alarm on CloudWatch Billing metric** (**only available in us-east-1**)
- Can choose a period to evaluate whether to send an alarm (i.e. 2 periods of 60 seconds)
- Alarm Resolutions: on high resolution metrics can set for 10 seconds or 30 seconds.
  - **The Metric Resolution determines the options of the Alarm Resolution you can select!**
  - Regular Alarm: any multiple of 60 seconds for default resolution metrics
- Specify: Period, Evaluation Period, Datapoints, Condition
- Can get access to rich data using Cloudwatch Agents or on prem.
  - Need to grant permissions for the agent to publish data into AWS

### Alarm States

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

- Public, Regional service
  - **Logs data across a fleet of resources**
  - Services send logs to Cloudwatch Logs in the same region they are in
  - Certain services like S3 (global) send the logs to us-east-1 region
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

### Ingestion

- To bring in application logs (your own logs), you need to install the Cloudwatch Agent
- Can Ingest VPC Flow logs or logs from Cloudtrail as well and other AWS services

### Log Events

- Two parts
  - timestamp: when the event occurred
  - raw message: msg sent by the app or service
- Events are collected into a Log Stream

### Log Streams

- Store **Log Events**
- A log stream is a sequence of events from the same source (i.e. an API, EC2, database etc.)
  - For EC2 instances, each log stream represents one instance
- Configuration settings are stored on the log group and apply to all log streams in that log group
  - retention
  - permissions

### Log Groups

- Containers for multiple log streams (i.e. logs per instance) for the same type of logging
  - I.e. a group of log streams for var/log events coming from different EC2 instances.
- Represents the thing being monitored, i.e. `var/log` messages for EC2 (from various instances/log streams, for example)
- Can hold streams from Lambda divided up by time periods
- Settings on the log group:

  - Retention: stores logs indefinitely by default. Can set a time limit to reduce costs
  - Permissions: choose who can access the logs
  - Encryption: at rest using KMS if desired

### Metric Filters are defined in log groups

- constantly monitors log events in the streams in the group that satisfy certain patterns
- When a event that satisfies a metric filter criteria happens, the metric is incremented
- Metrics, once created, can be used to make alarms that notify admins or other systems, or invoke Lambda functions, etc.
  - i.e. define the metric as failed ssh attempts or number of application crashes

### Delivering Logs

- Manual export to S3 with `CreateExportTask` - can take a long time (12 hours, etc.)
  - **Not realtime**
  - can only encrypt the data with SSE-S3, not SSE-KMS
- You can get logs out to other destinations in realtime on a per log group basis
  - Start with a log group, i.e. the Prod LogGroup
  - Configure a **Subscription Filter** on that log group
    - Set a pattern that determines what is handled by that filter
    - Set the destination ARN where the logs go to
    - Set the distribution to control how log data is grouped as its sent to the destination
    - Define permissions for Cloudwatch Logs to get access to the destination

#### Near Realtime delivery of Logs:

- For sending to S3 for longterm storage, use Kinesis Data Firehose as the destination and have that send the data through to S3 or any supported Firehose destination.
- This is **near realtime** - not good for true realtime delivery, only near realtime (60seconds, etc.) - very cost effective

#### For realtime delivery of logs:

- Configure a subscription filter to send logs to a Lambda or Kinesis Data Stream
- Can send to Elasticsearch, for example, via a AWS managed Lambda function
- Make a custom Lambda function to deliver to any other resource you want
- Kinesis Data Streams, alternative to using a Lambda, accepts any KCL consumers (Dashboards, etc.) and anything else that can interface with Kinesis Data Streams can get the logs in real time

### Log Aggregations with Subscription Filters

- Use the Subscription Filter to send all logs from many different accounts/regions to central Kinesis Data Stream
- Subscriptors could be monitoring this stream using KCL
- Then use Kinesis Data Firehose to persist all the logs to S3 or other logging aggregation systems

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

- Used to log and audit API/events calls or account activities made within your AWS account
  - Stopping an instance, changing a security group, create or delete S3 buckets, etc. - logs almost everything you can do in an account
- **NOT REALTIME** - up to 15 minutes delay.

### Pricing

- 90 days history enabled by default is free
- 1 copy of management events free in every region
  - Configure one trail in each region for every AWS account for free
  - Any additional trails are charged $2 per 100k events.
- Logging data events comes at a charge regardless of number - not free.
  - 10 cents per 100k events.
- NOTE: you are charged for storing events in S3 beyond the free tier.

### Cloudtrail Events

- includes logging actions taken by a user, role or service
- By default stores last 90 days of event history (available at no cost)
  - Customizing history requires creating a **Trail**

### Events

- Management EVents: info about management ops, a.k.a. control plane operations
  - Creating EC2 instance
  - Terminating EC2 instance
  - Creating a VPC etc.
- Data Events: operations performed on a resource
  - Objects uploaded or accessed in S3
  - A lambda function is being invoked
  - **By default, Cloudtrail only logs management events, data events are much higher volume**
  - You need to explicitly set and enable logging Data Events when you create a Trail if you want them.
- Insight Events

### CloudTRail Trail

- A unit of configuration within Cloudtrail
- A way to provide configuration to Cloudtrail on how to operate
- **A trail logs events for the region it is created in** Cloudtrail is a regional service
- Can be set to one region or all regions. (Single or all region trail)

  - All region trail can be thought of as a collection of trails in different region but is managed as one logical trail
    - Advantage: if new regions are added by AWS, the all region trail will automatically log events from it

### Global events for Global services

- Can configure to log in region events or global events
  - small number of services log global events - IAM, Cloudfront, STS, etc.
  - Global services always log events to us-east-1 region.
  - A trail needs to have global events enabled to log these events (as opposed to logging regional events)

### Event log Storage

- Can be stored in an S3 bucket - can be stored indefinitely as compressed JSON files - very small space taken.
- Can integrate with Cloudwatch logs and store the event log data there.

### Organizational Trail

- Create from the management account of an organization
- Logs events organization wide.

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

## Setup Cloudtrail For an organization

- [Video demo](https://learn.cantrill.io/courses/1101194/lectures/25527525)
- Need to be logged into the management account for an organization
  - You can set up individual trails locally inside an AWS account, but it is more efficient to use the management account for an org.
- Go to the Cloudtrail console in AWS Console > hamburger menu on left > `Trails`
- click `Create Trail`
- Enter a name: example - `Animals4LifeORG`
  - Note: when you create a trail, it will create one for every region in your AWS account
  - If logged into the management account of an organization, you have the option to tick select for all regions in all accounts in the org.
  - Select option to create a new S3 bucket if you want or use an existing bucket for the trail
    - Name the bucket unique - example: `cloudtrail-animals4life-{some random number}`
- If making a CloudTrail for production, check the SSE-KMS encryption option.
- Log File Validation option: adds additional security to allow you to determine if any of the log files were tampered with.
  - useful for account level audits
  - Enable for production usage.
- SNS notification delivery option: useful in production or if you need to integrate with external AWS tools/systems.
- Cloudwatch Logs: useful for event driven logging for triggers
  - can leave the name of the log group name if you want or customize it.
  - Need to give CloudTrail permissions via an IAM role to use the CloudWatch Logs service and enter data into it.
- Click Next at the bottom of the page.
- Choose the types of events to log (management events only by default). Careful of charges for Data Events.
- Leave defaults for rest of selections and click next
- Click Create

### Viewing CloudTrail Logs

- Wait 10-15 minutes for first log entries to appear.

- Open the link to the S3 bucket and you should see a folder structure created

  - CloudTrail-Digest/
  - CloudTrail/
  - Dig into the folders to see the logs (i.e. in CloudTrail/)
  - Click on `Open` button after clicking the file link
    - Depending on the browser you may need to download and decompress the log .gz file.

- For Cloudwatch go to it in AWS Console > Logs on the left > Log Groups
  - You should see the log group for cloud trail in the list.
  - The CloudWatch Streams are named as: `{Org ID}_{Account Number}_CloudTrail_{Region}`
  - The acct number can be compared with the ARN for the log group details: `arn:aws:logs:us-east-1:{acct number}:log-group:aws-cloudtrail-logs-{acct number}-ce376cd8:*` - can use this to pull logs for a specific account by it's number
- NOTE: Event History in CloudTrail service in AWS console on the left always has the last 90 days of events even if you don't have cloudtrail enabled.
  - Creating a trail allows you to get the events into an S3 Bucket/CloudWatch Logs

### To stop logging (to prevent S3 charges - probably small)

- Go to CloudTrail in AWS Console > Trails on the left > Click on trail > Stop Logging button.
- Probably will be a small charge per month (few cents or more) for org trails logging management events only.
