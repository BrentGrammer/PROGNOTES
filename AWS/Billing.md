# AWS Organizations
- Global service
- Allows management of **multiple AWS Accounts**
- Main account is the Master Account
- **Consolidated Billing with single payment method**
- **Pricing benefits from aggregated usage** because usage from all accounts for a service is consolidated - so you get high usage discounts
- **Pooling of Reserved EC2 instances** accross all accounts - optimal savings
- API availalbe to automate AWS account creation
- **Can restrict account priveledges using Service Control Policies(SCP)**

Multi Account Strategies:
- create accounts per department, per cost center, per dev test prod, based on regulatory restrictions, for better resource isolation (using VPC), can set up to have separate per account limits
- Can use tagging for billing standards
- Enable CloudTrail on all accounts and send logs to central S3 account
- Send Cloudwatch logs to central logging account

## Can organize accounts with Organizational Units (OU)
- Ex: business OU, Finance OU etc., sales OU
- Environment OUs (dev, prod)
- Can have OUs inside OUs

## Service Control Policies (SCP)
- Does not apply to master account and **applied at the OU or Account level**
- White list or blacklist IAM actions
- **Applied to all the Users and Roles, including Root, of the account**
  - If you restrict usage of EC2 on the account then even the Admin user cannot use EC2 for that account
- Does NOT affect service-linked roles (enables other AWS services to integrate with AWS Organizations)
- By default SCPs do not allow anything - must have explicit allows
- **Use Cases:** 
  - Restrict access to certain services for accounts
  - Enforce PCI compliance by explicitly disabling services
- Inheritance:
  - Typically you assign FullAWSAccess SCP to the root OU, and for example if you add a DenyAccessAthena SCP to the Root OU Master Account, it will inherit the FullAWSAccess SCP and still allow Athena! 
  - SCP levels at the OU level takes precedence over SCPs at the Account levels.
    - Deny rules at OU level are inherited by Account levels in them and overwrite any allows set on the account if there is a conflict.
    - Deny rules at the OU level (child OU) override Allow SCPs at the parent OU

# Consolidated Billing
- Combined Usage of all accounts with pricing benefits - Shared **Volume discounts and Reserved instances sharing (Accounts have access to any remaining reserved instances of any particular account in the organization)**

# AWS Control Tower
- Easy way to set up and manage multi-account based on best practices
- Instead of organizing OUs and policies in AWS Organizations, yourself, you can setup multi-account configuration with a few clicks in an automated way
- Auto sets up AWS Organizations and SCPs

# Compute Optimizer
- Lower costs by up to 25% easily by enabling 
- Optimizes compute for cost for:
  - lambdas
  - EC2 instances and ASGs
  - EBS Volumes

# Pricing Calculator
- estimate costs in cloud

# Tracking Costs
- Billing Dashboard
- Cost Allocation Tags
- Reports

# Monitoring costs
- Billing Alarms
- AWS Budgets




