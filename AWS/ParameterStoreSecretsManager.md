# Parameter Store and Secrets MAnager

## Secrets Manager

- Note: Different from the Parameter Store

## Secrets Manager vs. Parameter Store

- Secrets Manager good when Secret rotation, integration with RDS or secrets storage is needed
- Shared functionality means that for some situations you can use either
- Secrets manager designed specifically for **secrets** like Passwords or API keys
- Usually secrets manager is integrated with other apps (i.e. a web application, etc.)
  - Applications can use the Secrets Manager SDK to retrieve secrets like database credentials
  - The SDK uses IAM credentials for authentication (generally a role) to interact with the secrets manager
- Secret rotation is done automatically - uses a call to a Lambda periodically to update the secrets
  - Uses an Execution Role to access the Lambda and rotate the secrets in Secrets Manager
- Can directly integrate with RDS (to change any authentication is also changed when secrets are rotated - if lambda rotates a secret, the password inside an RSD instance is also changed in sync with it)
- Secrets are encrypted at rest and integrates with IAM to control access to the secrets
- Secrets are stored using KMS
  - No risk of leakage if hardware or host is compromised
  - Ensures role separation - permissions needed to KMS and Secrets Manager to access and decrypt secrets

## Parameter Store

- Parameter Store also stores encrypted strings - good more for things like configuration info, config for cloudwatch agents, etc.
  - License Codes
  - Database Connection Strings/Host names/Ports
  - can store Passwords/secrets (consider Secrets Manager for automatic rotation if needed)
- What sets Secrets Manager apart from Parameter store is the automatic **secret rotation** using lambda that Secrets Manager provides.
- Key value store - Parameter Name and a Parameter Value

### Types of Parameters

- Strings
- StringList
- SecureString

### Parameters

- Can be versioned and heirarchical
  - Can namespace parameters: `/wordpress/DBUser` or `/wordpress/DBPassword` (you can group and pull the namespace to get all parameters underneath that folder tree)
  - Ex: `/dev-team-passwords` - give the branch of the tree to the dev team to store their passwords in
- Can store plaintext (Database connection strings or Database users) or Ciphertext (for things like database password in encrypted form, etc. Integrates with KMS to encrypt passwords and sensitive, also permissions for the CMK inside KMS will also be required)
  - using Ciphertext via KMS means you need permissions to use KMS as well (extra layer of security)
- Public Parameters: values made available by AWS (i.e. the AMI ID for the latest version on a particular operating system which you can reference via a public parameter)

### Architecture

- Public service - anything using it must be an AWS service/in AWS or have access to the AWS public space and endpoints.
- Applications, EC2 instances, or Lambda functions can request access to parameters inside the Parameter store.
- Integrated with IAM permissions
- Any changes to any parameter can spawn and trigger events which you can use and occur in other AWS products
