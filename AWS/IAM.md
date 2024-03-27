# IAM

- **Global** resilient service
  - Any data is secure across all Regions
- Audit using Credential reports or Access Advisor (lists which roles/permissions have been used or not and can be removed)
  - Find access advisor in User page - it's one of the tabs
- Every Account comes with it's own IAM database instance separate from all other accounts.
- IDP - Identity Provider Platform that lets you create modify or delete identities.
- Authenticates and Authorizes Identities (Security Principals):
  - **Security Principal**: identities that are asking permissions or access to resources.
- Free no cost service
- Note: You cannot control external identities in other accounts or what they can do in external accounts, only identities within the account.

## Identity Types

### Users

- For people or applications.
- Use when you can identify individuals to grant permissions to.

### Groups

- Collections of related users.
  - i.e. a "Development team" group

### Roles

- Can be used by AWS services or to grant external access to services in account to uncertain number of entities.

## IAM Policies

- Document Objects that are used to Allow or Deny permissions to resources when they are attached to IAM Users, Groups or Roles.
