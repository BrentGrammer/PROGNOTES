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

- Primary use case is to store configuration information (DB connection strings, usernames, passwords, etc.) which your application uses or needs to lookup
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

### Using Parameter Store

- [Video Demo](https://learn.cantrill.io/courses/1101194/lectures/27895415)
- Parameter Store is a sub product of Systems Manager (SSM)
- AWS Console > Systems Manager > left menu Application Tools > Parameter Store option
- click Create Parameter
- Standard vs. Advanced option
  - Standard meets most needs, should default to this - can make up to 10,000 parameters in the standard tier
    - No additional charge for standard parameters unless you have more than 10k or use higher throughput options
  - Advanced: can create more than 10k parameters, parameter length can be longer than 4KB at 8KB max length
- Select a name, i.e. `/my-app/dbstring`
  - NOTE: you need the forward leading slash if making heirarchical names!
  - If you use folder syntax, that establishes a heirarchy (for grouping parameters if needed under a name space, i.e. 'my-app' here)
  - Set the value
- Set the type
  - For passwords, use `SecureString` so that it encrypts the parameter value
    - uses KMS to encrypt the parameter
    - Need to select the key source which is the key to perform the cryptographic operations
    - By default the key used is the default key for SSM (AWS Secrets Manager service) with the key ID `alias/aws/ssm`
      - In most cases you can just use the default key just fine
      - You can change that if you want to use a customer managed KMS key to configure rotation or set advanced key policies
      - The default SSM key does not support rotation configuration

### Interacting with Parameter Store via CLI`

- `aws ssm get-parameters --names /your-param-namespace/dbstring`
  - gets a list of parameters under a heirarchical namespace or the specific parameter if specified:
  ```json
  {
    "Parameters": [
      {
        "Name": "/your-param-namespace/dbstring",
        "Type": "String",
        "Value": "db.thisisprettyrandom.com:3306",
        "Version": 1,
        "LastModifiedDate": "2025-03-18T01:35:49.080000+00:00",
        "ARN": "arn:aws:ssm:us-east-1:905418086398:parameter/your-param-namespace/dbstring",
        "DataType": "text"
      }
    ],
    "InvalidParameters": []
  }
  ```
- To get a group of parameters under a namespace, use the `--paths` option
  - `aws ssm get-parameters-by-path --path /my-param-namespace/`
- To get decrypted parameters add the `--with-decryption` option:
  - `aws ssm get-parameters-by-path --path /my-param-namespace/ --with-decryption`
  - NOTE: **The permissions to interact with the parameter store to get decrypted parameters are DIFFERENT than those for interacting with KMS**
    - the `--with-decryption` option will decrypt ONLY if the user has KMS permissions to interact with the KMS key chosen when creating the parameter AND parameter store permissions! They need BOTH
      - (admin users have permissions already on KMS and parameter store)
