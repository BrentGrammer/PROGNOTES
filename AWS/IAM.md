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
- [Create an IAM User demo](https://learn.cantrill.io/courses/1101194/lectures/25335803)
  - Includes Cloudformation template at 3:20

#### Limits:

- **Only max of 5,000 users allowed per account** (IAM is global so not per region)
- IAM User can be a member of at max 10 groups
- Design implications: cannot have more than 5k user using a IAM user
  - Internet scale with millions of users
  - Large orgs with more than 5k needed.
  - IAM users are not the right identity to use for these cases, instead you need to use IAM roles or federation

### Groups

- Collections of related users.
  - i.e. a "Development team" group

### Roles

- Can be used by AWS services or to grant external access to services in account to uncertain number of entities.

## IAM Policies

- Document Objects that are used to Allow or Deny permissions to resources when they are attached to IAM Users, Groups or Roles.

### Policy Documents

- A policy document is one or more statements
- AWS knows which authenticated identities have which policies (an identity can have multiple policies)
  - AWS will move through each of the statements one by one to determine if any apply to interacting with a particular resource in a particular way.
- Interactions with resources in AWS is a combination of two main things:
  - The resource you're interacting with
  - The action you're taking on that resource. (example interacting with an AWS s3 bucket and the action is adding a object to it)
  - **Statements only apply if the resource and the action being taken on it match**

### Actions

- actions are in the format: `{service}:{action}`

### Example policy:

```jsonc
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "FullAccess", // Sid: optional field to identify what the statement does, best practice to always use these
      "Effect": "Allow",
      "Action": ["s3:*"],
      "Resource": ["*"]
    },
    {
      "Sid": "DenyCatBucket",
      "Effect": "Deny",
      "Action": ["s3:*"],
      "Resource": ["arn:aws:s3:::catgifs", "arn:aws:s3:::catgifs/*"]
    }
  ]
}
```

### Statement Priority

- If there is overlap in the statements, all statements are processed, and priorities are given.
- First Priority: explicit Denys
  - Denys for a specific resource will overrule everything else - in the above example, the Deny overrides the Allow s3:\* statement.
- Second Priority: Explicit Allows
  - Take affect UNLESS there is also an explicit DENY.
- Third Priority: Default Implicit DENY
  - If you're attempting to do something not specified in the statements, then it is Deny by default and not permitted.

### Policy Aggregation

- If there are multiple policies involved for an action (a user policy, a group policy that the user belongs to, and a resource policy for example), then all statements are evaluated and if there is any explicit DENY in any of them - that wins.
  - Same priority rules listed above apply across all statements and policies.

### Only Root user has access by default

- All Identities are denied access to all resources by default except the account root user.
- If there are not ALLOW statements, then the user has no access.

### 2 Types of Policies

- Inline policies: i.e. policies per user, not good practice for many users
  - Should only be used for Special or exceptional individual cases (i.e. applied to one user)
  - see [demo](https://learn.cantrill.io/courses/1101194/lectures/25335803) at 8:26 for creating an inline policy for a user.
- Managed Policies: it's own object that you can attach to multiple users. Best practice is to use managed policies.
  - Reusable
  - Low management overhead
  - Example: `IAMUserChangePassword` - allows an IAM user to change their own password or reset it.
  - see [demo](https://learn.cantrill.io/courses/1101194/lectures/25335803) at 11:43 for attaching a managed policy to a user.
    - IAM > Users > Add permission > Attach policy directly

#### Resource Policies

- attached to a resource (i.e. s3) and allows or denys actions for a particular principal or IAM identity for that resource.
- references the IAM identity via an ARN.
  - Note: A IAM Group is NOT an identity and cannot be referenced as a principal

### IAM Users

- an identity used for anything requiring long term AWS access
  - Humans, Applications or service accounts
- If you can picture one thing or a named thing/user that needs to access resources, then the correct identity to select for that should be an IAM User.

### Principal

- An entity trying to access an AWS account
  - Starts as unidentified
  - Can be individuals, copmuters, services or groups any of those things
- In order for a principal to do anything, it needs to be authenticated and authorized.

#### Authentication

- A Principal needs to prove that it is who it claims to be and authenticate against an IAM identity (i.e. an IAM User)
  - with Username and Password
    - a human user
  - with Access Keys (using the secret access key)
    - an application
    - a human using the cli tools
- After a principal is authenticated, AWS checks IAM policy statements for that identity to determine if they can perform an action etc. (Authorization)

## ARNS

- Amazon Resource Names
- Uniquely identify resources (in the same account or different accounts)
- `arn:partition:service:region:account-id:resource-id`
- `arn:partition:service:region:account-id:resource-type/resource-id`
- `arn:partition:service:region:account-id:resource-type:resource-id`
  - Example:
    - `arn:aws:s3:::catgifs` - this specifies a bucket (not the objects in it)
    - `arn:aws:s3:::catgifs/*` - this specifies everything in that bucket (not the bucket itself)
    - note the double colons are because you don't need to specify the region etc. for s3 buckets or the account id since s3 is global accross accounts, this is not a wildcard \* or the same thing as that.

### Can be attached to users

- ARNs can be defined for IAM users and identities

## IAM Groups

- Containers for IAM Users
- Soley for managing large sets of IAM Users and adding policies/permissions for them
  - i.e. Developers and a QA group
  - make groups that represent teams or projects etc.
- **Note: groups have no credentials of their own and you cannot log in to a group**
- **The same IAM User can be a member of multiple groups**
- Groups can have IAM policies attached to them.

### Limits

- 300 groups per account (can be increased with a support ticket)
- There is NO LIMIT for number of users in a IAM group (5,000 is the IAM user limit for an account)
- Note: there is NO All Users group built in (trick question on exam)
  - You could optionally create a group with all the users in it, but it does not exist natively
- There can be NO NESTING of groups (i.e. groups within groups)
- **A IAM Group is NOT an Identity and cannot be referenced by ARN etc. as a Principal in a policy**
  - i.e. you can't reference a group in a IAM resource policy.
