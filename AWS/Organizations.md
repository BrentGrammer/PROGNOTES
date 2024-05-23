# AWS Organizations

- Product for large companies to manage multiple accounts with little overhead and cost effective.
- Global service
- Allows management of **multiple AWS Accounts**
- Main account is the Master Account
- **Consolidated Billing with single payment method**
- **Pricing benefits from aggregated usage** because usage from all accounts for a service is consolidated - so you get high usage discounts
- **Pooling of Reserved EC2 instances** accross all accounts - optimal savings
- API availalbe to automate AWS account creation
- **Can restrict account priveledges using Service Control Policies(SCP)**

## Creating an Organization (with a MANAGEMENT ACCOUNT)

### Management/Master/Payer Account

- MANAGEMENT (prev. Master) AWS Account: a standard AWS account that is not within an organization which is used to create an Organization.
  - This account also has payment information for billing for the Organization and is called also the Payer Account.
  - **NOTE: The Organization is NOT WITHIN the standard account, the std account is just used to create it.**
  - There can be only 1 Management account for an Organization which can have 0 or more Member Accounts.
- A Management Account can invite other existing AWS Accounts into the Organization.
  - These accounts need to accept an invite to join the organization
  - When a standard account joins an organization they become **Member Accounts**

## Organization Structure/Heirarchy

- At the top is the Organization Root: a container that holds the management account and member accounts for an Organization.
  - NOTE: This is NOT the AWS Account Root User (This user is specific to every AWS Account and is what you log in to for unlimited permissions)
  - The Organization Root can contain "OUs" (Organizational Units)
    - Organizational Units can contain the management account, member accounts or other Organizational Units

### Multi Account Strategies:

- create accounts per department, per cost center, per dev test prod, based on regulatory restrictions, for better resource isolation (using VPC), can set up to have separate per account limits
- Can use tagging for billing standards
- Enable CloudTrail on all accounts and send logs to central S3 account
- Send Cloudwatch logs to central logging account

## Can organize accounts with Organizational Units (OU)

- Ex: business OU, Finance OU etc., sales OU
- Environment OUs (dev, prod)
- Can have OUs inside OUs

## Creating Accounts

- In addition to inviting existing accounts to an Organization, you can create new accounts within the Org - you need a unique email address for them.
- There is no invite process when creating accounts in the Organization

## Logging in

- No need for IAM users in every single Account.
- IAM roles can be used instead to allow IAM users to access other AWS Accounts.
- Best practice is to have a single account (i.e the Management Account or a separate dedicated account for logging in is used) which is used to log in with.
  - contains all the identities which are logged in
  - Larger enterprises might use Identity Federation (if they have existing identities and their own identity system already) to access the designated AWS Account for logging in.
    - Once logged into the AWS login account, identities can use a feature called Role Switch to role switch from the account to other member accounts of the Org. Behind the scenes this assumes roles in the other accounts.
- To summarize: You either login to the AWS Account dedicated to logging in directly, or you use identity federation to login to that designated login account, and then you role switch to other accounts in the organization (behind the scenes you assume a role in the other member accounts).

## Service Control Policies (SCP)

- Feature of AWS Organizations that lets you restrict what AWS Accounts in the Organization can do.
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

## Billing

- Organizations use Consolidated Billing (each account passes their bill to a Payer Account that has the payment details - the Management Account)
- Single Monthly Bill covers the Management and Member Accounts in the Organization
- Cost advantages by pooling lower cost for high use of certain services apply
