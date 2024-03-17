# AWS Accounts

- Accounts are NOT users
- complex enterprise environments use many different accounts.

- An AWS Account is a container for identities and AWS resources.
  - identities: users
  - you login with users and provision resources within that account.

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

### Account Boundaries

- If the root user credentials are leaked or stolen, a bad actor can delete everything in that specific account, but not others.
- Businesses that have everything in one account expose themselves to high risk of disaster, so multiple accounts to segregate resources are recommended.
- By default all access from external identities is denied (i.e. external users) for an account.
  - Unless anything is explicitly allowed, everything is denied for all users except the root user.
