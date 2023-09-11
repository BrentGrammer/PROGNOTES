# Shared Responsibility


## IAM
AWS
  - Infrastructure (global network security)
  - Config and vulnerability analysis
  - Compliance validation
  - Hardware maintenance
  - Security of managed services like S3, DynamoDB, RDS

YOU
  - Analyzing Access Patterns and Permissions review
  - monitor Users Groups Roles and Policies
  - Rotating Keys, MFA
  - Applying appropriate permissions
  - security patches and updates (on EC2 instances for ex.)
  - OS updates
  - Firewall and network configuration, IAM permissions
  - Encrypting application data

SHARED:
  - Awareness and Training for security best practices
  - Patching in general - some patching on OS etc is customer responsibility, but some patching for infrastructure is AWS' responsibility