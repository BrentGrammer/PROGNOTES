# Security Tools Provided By AWS

### Acceptable Use Policy (UAP)

- Defines what you can and can't do with a service (AWS)

### Abuse Reports

- Email or AWS Health Dashboard provide notices of abuse
- AWS Trust & Safety Team will contact you with what is happening and what abuse is suspected as occurred
  - DDOS
  - Scam attempts, etc.
- **Must act on the notification** - within 24 hours, the account will be suspended otherwise
  - Respond with the Report Abuse Form
  - Be sure to provide detailed accurate date and times and timezones in the report

## GaurdDuty

- Security Service for continuous monitoring for identifying unauthorized or unexpected activity on an account
  - Once enabled - it is running ALL THE TIME monitoring for issues
- Possible to use for event-driven automatic Security Response
- Integrated with supported data sources
- Uses AI/ML and threat intelligence feeds
  - Tries to spot odd activity
  - Learns patterns of what happens normally to judge against
- Supports multiple accounts via a master and member account architecture
  - Whatever account enables GuardDuty becomes the master GuardDuty account
  - Can invite other AWS accounts which can become member GuardDuty Accounts
  - This provides for a central management location for GuardDuty with multiple accounts

### FINDINGS

- **FINDING** - the logical entity when something is found worthy of attention
- Can be configured to notify or initiate event-driven protection process when a Finding is found.
  - Could be Lambda that performs some kind of remediation
  - Event driven workflows via Cloudwatch Events to perform some series of operations is possible as well

### GuardDuty Architecture

- Logs are received from supported Data Sources
  - DNS Logs from Route53
  - VPC Flow Logs (traffic metadata flowing through a VPC)
  - CloudTrail Event Logs (logs API calls within the account)
  - CloudTrail Management Events ( control plane level event logs)
  - CloudTrail S3 Data Events (any interactions with objects in S3)
- These are combined with Intelligence Feeds to generate Findings which show unusual or unexpected behavior
  - The findings can be sent to Cloudwatch Events (EventBridge now) for automatic remediation via event driven processes
  - Can use SNS notifications to team members etc.
  - Can invoke Lambda functions to remediate (ex: add DENY actions to a ACL based on the finding of potential intrusion)

## AWS Security Hub

- Single location for managing security and remediation tasks
  - Various security-related services can all plug in to Security Hub
  - Information generated from these services is consolidated in one place
- Regional Service
  - Must be enabled in ALL REGIONS so events from all regions can be captured
- AWS Console or Security Hub API access
- NOT retroactive - only works from the point it is enabled onwards
- Provides scores and findings based on established security standards
  - CIS AWS Foundations
  - PCI DSS
  - AWS Foundational Security Best Practices
  - Your account will be compared against these standards to generate a score and findings for attention
- Supports EventBridge for auto remediation

### Security Hub Architecture

- Administrator and Member Accounts
  - Independent of the AWS Organizations accounts
  - An account becomes a Admin account if it invites other accounts to become associated with it or is designated as the Admin account by the organization
- Regional Service
  - Can define an aggregation region - receives data from other linked regions allowing multi-account, multi-account consolidation
- Functions by integrating with other security tools in AWS (not just taking data from AWS generally)
  - Config
  - Macie
  - Inspector
  - GuardDuty
  - IAM
  - Firewall Manager
  - more... see [Docs](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-findings-providers.html)


### AWS Security Findings Format Standard (ASFF)

- JSON-based format for anything which Security Hub ingests or generates

