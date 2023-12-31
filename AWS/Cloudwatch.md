# Cloudwatch Metrics
- Provides metrics for every service in AWS
- Metric: a variable to monitor such as CPU Utilization or NetworkIN, billing etc
  - Default is metrics for every 5 minutes
    - Optional every 1 minute (Detailed Monitoring) for additional cost
  - All have timestamps
- Can create Cloudwatch Dashboards to view all metrics at once
- Used to determine things like scaling in and out (looking at CPU utlization or network in and out)
  - NOTE: For EC2 monitoring RAM is not an available metric

  ## Example Metrics
- EC2: CPU Utilization, Status Checks, Network (No RAM available)
- EBS Voluimes: amount of Disk Read/Writes happening
- S3 Buckets: Bucket Size Bytes, NumberOfObjects, AllRequests
- Billing: Total estimated charge (only available in us-east-1)
- Service Limits: how much you've beenusing a service API
- You can make CUSTOM METRICS

# Cloudwatch Alarms
- Triggered notifications for any metric
- Examples:
  - Auto Scaling: increase or decreast EC2 instances to desired count
  - stop or terminate reboot/recover on fail a EC2 instance
  - SNS: send a notification
  - **Set a billing alarm on CloudWatch Billing metric** (**only available in us-east-1**)
- Can choose a period to evaluate whether to send an alarm
- Alarm States: 
  - OK (everything is green)
  - INSUFFICIENT_DATA (can't figure out whether to send alarm)
  - ALARM (sends alarm)

# Cloudwatch Logs
- **Centralizes logs from your AWS resources**
- Can collect logs from:
  - Elastic Beanstalk - from application
  - ECS: collection from containers
  - Lambda - function logs
  - CloudTrail based on filter
  - Cloudwatch log agents: Install an agent directly onto EC2 machines or on premise servers to get the logs into AWS
    - On EC2 instances for ex., by default no logs from the instance will go to CloudWatch.  You need to runa agent on EC2 to push the log files you want
    - Make sure the IAM permissions are set to allow the Cloudwatch agent
    - Hybrid agent - works on premise as well
  - Route53 - log DNS queries
- Allows for real time monitoring
- Adjustable retention - 1 week, 30 days, year, infinitely etc.

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
    - Example of EventBridge use: invoke an event to run a lambda function every hour.  Targets can be different AWS services, in this case the target is lambda which will run on the scheduled hourly emitted event sent from EventBridge
    -  EVENT PATTERN: Can also send an event whenever someone logs in to the AWS console for an account and target SNS target to send a notification whenever that happens for ex.
    - use an EVENT PATTERN: Get notified whenever a EC2 instance gets terminated - get a SNS notification

# CloudTrail
- Used to audit history of API/events calls made within your AWS account
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