# AWS Accounts

- Accounts are NOT users
- complex enterprise environments use many different accounts.

- An AWS Account is a container for identities and AWS resources.
  - identities: users
  - you login with users and provision resources within that account.

### Account Boundaries

- If the root user credentials are leaked or stolen, a bad actor can delete everything in that specific account, but not others.
- Businesses that have everything in one account expose themselves to high risk of disaster, so multiple accounts to segregate resources are recommended.
- By default all access from external identities is denied (i.e. external users) for an account.
  - Unless anything is explicitly allowed, everything is denied for all users except the root user.

## Requirements to create accounts:

- Name
- unique email address
  - This is used to create the account root user identity
  - These root users can only access the account they are associated with.
  - The root user always has full access and permissions to everything within that Account.
    - HIGH SECURITY RISK
  - You can create IAM users with restrictions, but they start out with no access or permissions.
- payment method (same credit card can be used for multiple accounts, but the email cannot)
  - AWS is a pay as you consume or pay as you go service
  - Some services have certain free time per month - free tier

## Account Users

- The root user always has full access and permissions to everything within that Account.
  - HIGH SECURITY RISK
- You can create IAM users with restrictions, but they start out with no access or permissions.
- Users created in the account can only access resources inside that account and not another.

### Account setups

- General setup could be Admin user, Production account

### Admin

- Instead of using the root user in an account, best practice is to create an IAM Admin user with administration priviledges.

## Setting up an Account

### Use Dynamic Aliases for Multiple emails for acccounts

- View accounts as disposable and create as many as you need
- Because the require unique email accounts - can use a gmail feature to handle this - dynamic aliases
- Use the plus sign and any text after your name - all of these are considered unique to AWS but will go to your main email address.
- yourname@gmail.com

  - yourname+AWSAccount1@gmail.com
  - yourname+AWSAccount2@gmail.com

- For the account name use kebab case: SOME-ACCOUNT-NAME
- Initially you create each account as the ROOT user.
  - You create IAM Admin user after the account is created - best practice is to stop using root user and use admin user going forward.

### Alternate Contacts

- Often you'll have different emails or contacts for billing or security etc. - you can set these in the account menu
- AWS Console > Top right dropdown for my account > Account Settings > Alternate Contacts

### IAM Access to Billing information

- You might want to enable your access to billing information when you're logged into the account as an IAM user (and you have permissions)
  - Without this even full admin permissions does not allow access to the billing console.
- In AWS Console > My Account > Account Settings > IAM User and Role Access to Billing Information > `Edit` > Check `Activate IAM Access` box > click `Update`

### Use MFA

- [video](https://learn.cantrill.io/courses/1101194/lectures/24889649)
- In AWS Console > Account Dropdown top right > `Security Credentials` > MultiFactor Authentication section > Assign MFA Device
- Setup MFA for each account/Admin IAM user
- Can use authentication apps (Authy/Google Authenticator) or the other methods offered.

## Cost Management in an Account

- Can search services in AWS console for 'Free Tier' to get overview of available free trials
- Make sure you are logged in as an account user with billing access
- AWS Console > Account dropdown (top right) > `Billing and Cost Management`
  - The left side panel has a number of pages with cost information and forecasting you can examine

### E-notices for billing

- Go to Billing and Cost Management > `Billing Preferences` on the left side panel > enable PDF invoices delivered by email
  - This will send cost breakdown to your email so you don't have to login to the aws account to see cost breakdowns. (you get a notice every month)
  - Also check Receive AWS Free Tier alerts to get noticed when run out of free trials

### AWS Budgets

- Configure alerts for spend when it reaches certain percentages.
- AWS Console > search for AWS Budgets
- Can choose a template (selections shown on Budgets page - make sure use a template is selected)
  - You need to enter an email address to receive the notification alerts at.
  - Click `Create Budget`
  - Could take 24 hours to register and start monitoring

### Create an Admin User

- Do not use the root user after the account is created and set up.
- Create an Admin IAM user for each account.
- Go to IAM service and make a new admin user
- You need to use a signin URL for IAM users.
  - Ex: `https://{accountnum}.signin.aws.amazon.com/console`
  - You can view this in the IAM dashboard on the right of the screen
- Create an Alias to make signin easier - must be globally unique and include the type of account in the name (i.e. "general" or "production")
  - AWS Console > IAM Dashboard > `Create Alias` on the right of the page.
    - enter a name: i.e. `my-admin-alias-production`
- IAM Dashboard > Users > `Create User`
  - can just use `iamadmin` for the username for each account (they will not conflict)
  - Check "Provide user access to the AWS Management Console" option to allow admin to access the console.
  - Create a password and optionally Uncheck Users must create a new password (if you're setting the account up)
  - Click Next and select `Attach policies directly` > Search `AdministratorAccess` and select it and click next > `Create User`
- You need to note or save the signin url for the admin user - you will need this to signin with that user in the future.
  - when signing in use `iamadmin` or the username you made
- After creating the Admin User - Secure it adding MFA
  - If using MFA for users, you need to add mfa for each IAM identity in the account as you did with the root user.

## Command Line Access (need access keys)

- Accessed with IAM Access Keys
  - Long term credentials in AWS (used with IAM users)
  - These creds do not rotate regularly - you have to change them manually
- Access keys can be created, deleted, made inactive or made active (active when created)
- Two Parts:
  - Access Key ID (public)
  - Secret Access Key (private)
  - if secret key is lost or you want to rotate you need to create an entire new set of credentials.
- Rotating keys: Create a brand new set and remove the old one
  - an IAM user can have two sets of keys
- Only IAM users have long term credentials like Access Keys (not recommended for root user)
  - IAM Roles do NOT use Access Keys
- iamadmin users should have access keys, for example

## Setting Up CLI and Access Keys

### Creating Access Keys

- Log in as iamadmin user for the account
- Go to AWS Console > Account Dropdown (top right) > Security and Credentials > Scroll down and click `Create Access Key`
- Specify and select use as Command Line Interface (CLI) option. Select understand confirmation box and click `Next`
- Provide a tag description, ex: `LOCAL CLI IAMADMIN-GENERAL`
- Click Create Access Key and copy them for safe keeping
  - Download the csv file - rename to reflect account, i.e. `aws_accessKeys_production`
  - Note: You can have up to two access key sets, but not more.

### Install and Configure the AWS CLI

- See online documentation from AWS for installing the CLI
- run `aws --version` to confirm installation
- `aws configure` <-basic command for configuring cli usage with accounts
  - If you run without arguments/options it configures a default profile for the CLI which will be used if you don't specify a Named Profile
  - You should configure the cli with named profiles as below

### Named Profiles

- These are used to configure the CLI for multiple AWS Accounts.
  - i.e. a named profile for the iamadmin user of the general or production accounts
- `aws configure --profile <profilename>`
  - Use a name for the profile, i.e. `iamadmin-general` for the admin user in the general account.
  - Enter the access key information created for the account user
  - enter the region - i.e. `us-east-1`
  - just press enter for default output
- Confirm usage with `aws s3 ls --profile <profilename>`
  - If you get `Unable to locate credentials. You can configure credentials by running "aws configure"` error it's because creds were set up with a named profile, so you need to add the `--profile` option
  - if you get list of buckets or empty list with no error, then you are good.
  - If you get an error try rerunning the aws configure --profile command
