# DDOS Attack  (Distributed Denial of Service)
- Overwhelm server with requests from many bots and deny service to normal users
- AWS Shield Standard - provided protection by AWS enabled by default
- AWS Shield Advanced: 24/7 Premium protection from DDoS
  - Expensive - $3,000/mo
- AWS WAF: Filter requests based on rules (Firewall)
- CloudFront and Route53: Availability protection - combined with Shield provides attack mitigation at the Edge
- Being ready to scale is a counter - leverage AWS Auto Scaling

# AWS Shield
- **Standard: Free for every customer and enabled by default**
  - protects against SYN/UDP floods, Reflection Attacks and other Layer 3/4 attacks
- **Shield Advanced: Optional DDoS mitigation service - $3,000/month**
  - not enabled by default - opt in
  - Protection against more sophisticated attacks on EC2s, Load Balancers, Cloudfront, Global Accelerator and Route53
  - **24/7 access to a AWS DDoS response team (DRP)**
  - protection against higher usage fees from DDoS attacks

# AWS WAF - Web Applictaion Firewall
- Protects web apps from common web exploits (Layer 7 HTTP)
- Deployable on Layer 7 platforms like Application Load Balancer, API Gateway and CloudFront
- Can define a Web ACL (Access Control List)
  - Rules for IP addresses, HTTP headers, HTTP Body or URI Strings
  - Protects against common attacks - SQL Injection and Coross Site Scripting
  - Size contraints and geo-match (to block countries)
  - For DDoS attacks, Rate-based rules to count events (ex, user cannot make more than 5 requests per second)

# Penetration Testing
- **Customers can carry out penetration tests against infrastructure without needing prior approval for 8 services:**
  - EC2 instances, NAT Gateways and Elastic Load Balancers
  - Amazon RDS
  - CloudFront
  - Aurora
  - API Gateways
  - Lambda and Lambda Edge functions
  - Lightsail resources
  - Elastic Beanstalk environments
- Prohibited Testing:
  - DNS Zone Walking via Amazon Route53 Hosted Zones
  - DoS, DDoS or simulated Dos/DDoS attacks
  - Port flooding
  - Protocol flooding
  - Request flooding (login API flooding etc)
  - For other simulated events you need to contact aws-security-simulated-event@amazon.com
- **You can do some penttesting, but anything that resembles a DDoS attack etc. is not allowed)

# Encryption
- Two types: Data at rest, Data in transit
- Data at Rest: data stored or archived on a device
  - on a hdd, on RDS instance, in S3 Glacier Deep Archive
- Data in transit: in motion data being moved - it is transferred on the network
  - transfer from on prem to AWS, EC2 to DynamoDB etc.
- Use of **encryption keys** to encrypt data. Only those who have the keys can decrypt it.

## KMS (Key Management Service)
- **when "encryption is mentioned for a service, most likely answer is KMS**
- AWS manages the encryption keys and software for encryption for us
- Opt-in encryption:
  - for EBS volumes
  - S3 Buckets: server side encryption of objects
  - Redshift database
  - RDS database data
  - EFS: encrypt files
- Automatically enabled encryption:
  - 'cloudTrail logs
  - S3 Glacier
  - Storage Gateway

## CloudHSM (Hardware Security Module)
- Another encryption service - an actual device
-  AWS provisions encryption hardware
  - HSM = Hardware Security Module
- user manage keys entirely
- HSM device is tamper resistant - it will fail if tampered with
- Amazon manages the physical hardware, but client uses a CloudHSM client software and the AWS CloudHSM service to manage the keys

# CMK (Customer Master Keys)
- Customer Managed CMK:
  - Created, managed and used by the customer - can be enabled or disabled
  - option of rotation policy
  - option to bring customer's own key
- AWS managed CMK:
 - Keys that are created, managed and used on the customer's behalf by AWS
 - Used only by AWS resources
- AWS Owned CMK
  - Collection of CMKs that an AWS service owns and manages to use in multiple accounts
  - AWS can use them to protect resources in your account (you cannot view the keys though)
- CloudHSM Keys (Custom Keystore):
  - Keys generated from own CloudHSM hardware device
  - Cryptographic operations happen within the CloudHSM cluster (could be a secuerity req for some cos.)

# AWS Certificate Manager (ACM)
- easily provision **manage and deploy SSL/TLS Certificates**
- provides **in flight encryption** for websites (HTTPS)
- Supports both public and private TLS Certificates
- FREE for public TLS certs
- Automatic TLS cert renewal
- Integrates and loads certs on Elastic Load Balancers, CloudFront distributions, and APIs on API Gateway.

# Secrets Manager
- Newer service for storing secrets
- Can force rotation of secrets every X days
- Automate generation of secrets on rotation (using Lambda)
- Integration with RDS (MySQL, PostgreSQL, Aurora)
- Secrets are encrypted using KMS
- Paid service
- **Secret management for RDS that rotates secrets**

# AWS Artifact
- Portal that gives access to on demand AWS compliance documentation and AWS agreements
  - Not a service, just allows you to download compliance documents
- Artifact Reports: download security and compliance documents from 3rd party auditors - ISO certs, PCI, System Org and Control (SOC) reports
- Artifact Agreements: Allows you to review AWS Agreements like H HIPAA etc.
- Used to support internal audits or compliance reqs and proof for your company

# Amazon Guard Duty
- **Find malicious behavior with VPC, DNS, CloudTrail logs**
- Intelligent threat discovery using Machine Learning and third party data to protect and detect attacks on your Account
- One click enabled and you get a trial for 30 days, no software to install
- Input data:
  - Cloudtrail Event Logs - unusual API Calls, unauthorized deployments
  - CloudTrail Management Events: create VPC calls, etc.
  - S3 Data Events (get object, put delete etc)
  - VPC Flow Logs - unusual traffic, unusual IP addr
  - DNS Logs - detect EC2 instances sending encoded data within DNS queries
  - K8s Audit Logs 
- Can setup CloudWatch Event rules to be notified
- **CloudWatch Event Rules can target AWS Lambda (function to do some action) or SNS (can use this to send some emails for example)**
- **Dedicated finding for detecting Cryptocurrency attacks**

# Amazon Inspector
- Automated Security Assessments for AWS infrastructure
  - Runs continuously and automatically, but only when needed
  - **Only for EC2 Instances and Container infrastructure**
  - **automate security on EC2 instances to assess security and vulnerabilities in these instances.**
- For EC2 instances:
  - Leverage AWS System MAnager agent
  - check for unintended network accessibility
  - analyze running OS against known vulnerbilties
  - Network reachability assessments
- For Containers pushed to Amazon ECR:
  - Asssessment of containers as they are pushed
- Report delivered into AWS Security HUb
- Findings sent to Amazon Event Bridge
- After analyzing, you get a risk score with all vulnerablilities

# AWS Config
- Helps with auditing nd recording compliance of AWS resources
- View history of config changes on AWS resources and set rules for detecting non compliance (ex. unrestricted SSH access on EC2 instances)
- per-region service
- Helps record config changes over time.
- Can store config data into S3 (and have it analyzed by Athena)
- Use Cases:
  - Check for unrestricted SSH access to security groups (by creating a rule to check for that for example)
  - Check if buckets have public access
  - Check how ALB config has changed over time
- Can send SNS notifications for any config changes
- Can be aggregated across regions and accounts
- Can use CloudTrail API calls to check who made the config change
- Not free, if enabled it costs money to start recording
  - Will create a bucket where config history will be stored and you can set a topic to send changes to

# Amazon Macie
- managed data security service that uses machine learning to discover and protect your sensitive data in AWS
- alerts you to sensitive data such as Personally Identifiable Information (PII) in S3 Buckets

# AWS Security Hub
- **Central tool to manage security across MULTIPLE AWS accounts and automate security checks**
- Integrated dashboards showing compliance status to help you quickly take actions
- Aggregates alerts from services (GaurdDuty, Inspector, Macie, IAM Access Analyzer, SSM, Firewall Manager etc.)
- In order to use, you need to enable the AWS Config service

# Amazon Detective
- Quickly analyzes and identifies the root cause of a security issue or suspicious activity using ML and graphs
- Automatically collects  and processes events from VPC Flow Logs, CloudTrail and GuardDuty to create a unified view
- produces visualizations
- used for complex issues and finding the cause

# AWS Abuse
- Report AWS resources for abuse or illegal actrivity to Amazon
- AWS owned IP addr, websites and forums spammed by AWS resources, DDoS attacks, intrusion attempts, hosing illegal content etc.
- **Contact the AWS Abuse team with the form or by their email if you see this activity**

# Root User Priviledges
- Don't use for everyday tasks - create an Admin user
- Actions only can be done by Root User:
  - **Change account settings, name, addr, root pw and keys**
  - View tax invoice
  - **Close the aWS account**
  - Restore IAM permissions
  - **Change or cancel support plan**
  - **Register as a seller in the Reserved Instance marketplce**
  - Configure S3 bucket to enable MFA
  - Edit or delete S3 Bucket policy thast includes an invalid VPC ID or VPC Endpoint ID
  - Sign up for GovCloud