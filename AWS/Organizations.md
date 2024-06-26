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

- Feature of AWS Organizations that lets you restrict what AWS Accounts in the Organization can do. (Account permissions boundaries limiting users and services)
  - JSON Policy documents that can be attached to the organization as a whole by attaching them to the root container, or they can be attached to one or more Organizational Units (OUs), or individual AWS Accounts.
  - Do not grant any permissions, they are just a boundary that limits which permissions etc. and what is and is not allowed in the account, but do not handle permissions - you still need IAM policies for that.
  - SCPs are inherited down the heirarchy (i.e. if they are attached to the root container of the org, then all accounts and OUs in the org inherit them.).
    - **Exception**: The management account is NEVER affected by SCPs.
    - Because Management Accounts cannot be restricted by SCPs, generally you should avoid using them for production for any AWS resources.
    - Note that root users in accounts under an SCP are restricted indirectly.
- Does not apply to master account and **applied at the OU or Account level**
- White list or blacklist IAM actions
- **Applied to all the Users and Roles, including Root, of the account**
  - If you restrict usage of EC2 on the account then even the Admin user cannot use EC2 for that account
- Does NOT affect service-linked roles (enables other AWS services to integrate with AWS Organizations)
- **SCPs override Account Policies and Permissions** (if anything is denied or not allowed in the SCP then it cannot be allowed in an Identity Policy in an account.)

### Allow List vs. Deny List

- By default SCPs do not allow anything - must have explicit allows
  - You can alternatively setup to allow everything and explicitly block some things.
  - Deny List by default. Implicit Deny is enforced for everything. Which means Allow for everything and then implicitly deny (explained in a confusing way [here](https://learn.cantrill.io/courses/1101194/lectures/25362690))
  - Deny Lists allow for everything to be allowed as new AWS services expand - low admin overhead.
- Allow List: 2 part architecture - remove AWSFullAccessPolicy (which as in the Deny list above allows everything by default), so only explicit deny policies take effect.
  - More secure, but more admin overhead. Recommended to use Deny List architecture over Allow List.

### Use Cases:

- Restrict access to certain services for accounts or certain regions.
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

## Creating an organization

- [video](https://learn.cantrill.io/courses/1101194/lectures/25362688)
- Login to a standard AWS account, i.e. your general admin (iamadmin, not root is okay) account
- AWS Console > look up Organizations in search services > Click Create Organization
  - This will start the process and convert your standard account to be the management account for the organization
  - If you get a notice about an email confirmation, you need to click the email verification link in your email to continue

### Invite another account to the organization

- Copy the Account ID for the account you want to invite (top right in AWS console if logged into that account)
- In AWS console > Organizations > Your org - click "Add an AWS Account" button
- Select Invite an existing account (or select create new acct if needed)
- Enter the account number or email of the account you want to invite
  - Optionally provide a message: "Please join the org..."
- Click Send Invitation
  - If you get an error about quotas, log a support request to increase the quota for your org.

### Setup Role Switching

Purpose: You need a role to switch to from the general/management account to login to the invited account to perform administrative functions. The new Role in an AWS Account will have a Trust Relationship that trusts the management account to assume that role and grants it admin permissions to login the account.

- If creating a new account to add to the Org, there is a role created automatically for you to role switch into.
- If you invited an existing account, you need to manually add the role to allow for role switching. You need to create a role from the invited account that can be assumed by the management account.
  - Login to the account that was added to the org. (i.e. the prod account, not the management account)
  - Go to AWS Console > IAM service page > Roles > Create Role
  - Select AWS Account for the type of trusted entity
  - Under An AWS Account section, select "Another AWS Account" and enter the Account ID of the Management Account (i.e. general admin account, for example which will be trusted to assume this role)
    - You can find the account number in the organizations page in the AWS Console underneath the list of aws accounts in the organization if you created the account (and are not inviting an existing one).
  - Click Next
  - Attach the AdministratorAccess Role (search for it in next screen) and check it and click Next.
  - Give the role a name: use `OrganizationAccountAccessRole` <- This is conventiona and is the same name AWS gives a role created automatically if the account was created and added to the org. Stay consistent.
    - Click Create Role
  - After creation if you go to the role and click Trust Relationships tab, you'll see the statement Allows a Principal of your general/management AWS Account which allows it to assume this role.
    - Note: this only allows IAM identities (i.e. iadmin user, etc.) to use the role and login to the account.

### Performing a Switch Role

- Login to the management/general iamadmin user account.
- Click top right dropdown and select Switch Role
- Enter the account number for the account you want to login to (i.e. the prod/invited account), use the OrganizationAccountAccessRole name from above and add a display name, i.e. "Prod" (see explanation at timestamp 10:50 in [video](https://learn.cantrill.io/courses/1101194/lectures/25362688))
- Select Switch Role and you'll be logged into that account assuming the role created above. (look for the display name you entered in the top right of the screen)
- You can use the dropdown in the top right to "Switch Back" to the previous account and you'll see a role switch history as well.

Role switching will grant temporary credentials by assuming the role created above and allow for logging into the account.

### Creating Organizational Units
- AWS Console > AWS Organizations
- Select/check the Root container on the Organizations AWS Accounts page.
- Select the Actions dropdown and under Organizational Units > Create New
- Input a name for the UI, u.e. "PROD" or "DEV", then click Create organizational unit
- Typically you'd have OUs for PROD and DEV and move accounts into the appropriate OU.
### Structure of OUs:
- Root
  - PROD
    - Prod accounts
  - DEV
    - Dev Accounts
  - Management Account

#### Moving Accounts into OUs
- On the main accounts page in the Organization page, select the account you want to move > Actions dropdown > Move
- Select the OU you want to move the act into and click Move.

