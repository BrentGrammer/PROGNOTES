# CloudHSM (Hardware Security Module)

- Similar to KMS for storing managing keys
- KMS is a SHARED service (other accounts within AWS also can use KMS as a service)
  - AWS have a certain level of access to the product as well
  - Uses HSM (Hardware Security Module) behind the scenes which are industry standard hardware for managing keys and cryptographic operations

#### CloudHSM is a Single Tenant HSM

- For high security environments, CloudHSM offers a true single tenant on-premise Hardware Security Module that is hosted in the cloud.
- AWS provisions this and is responsible for the hardware maintenance/software updates etc, but they have no access to the parts of the unit where the keys are stored and managed.
  - physically tamper resistant and areas are partitioned so only you can access them
  - If access to it is lost by the customer, there is no way to recover the data
- Follows **FIPS 140-2 Level 3** Standard (Federal Information Processing Standard)
  - Can determine effectiveness of an HSM module based on their compliance with this standard.
  - by comparison, KMS is Level 2 overall with some Level 3 compliance
  - **If you need Level 3 compliance, you NEED TO USE CloudHSM or on-premise HSM Device**
- Access CloudHSM via Industry Standard APIs: `PKCS#11`, Java Cryptography Extensions (`JCE`), Microsoft CryptoNG (`CNG`) libraries
  - If any of these standards are required, you need an HSM on premise of CloudHSM
- KMS can use Custom Key Store which uses CloudHSM under the hood
  - This option allows for benefits of AWS Integration that KMS has along with some of the security of CloudHSM

## Architecture

- CloudHSM is not deployed into a VPC that you control
  - deployed into a AWS Managed Cloud HSM VPC which you have no visibility of
  - They are injected into your VPC via Elastic Network Interfaces
    - A elastic network interface is injected for each CloudHSM in a cluster
- Need to deploy to multiple AZs for high availability
  - Each CloudHSM is a physicial device available in only one AZ
  - Need to create a Cluster of CloudHSMs, with one in each AZ that is used in your VPC
  - CloudHSMs in a cluster have all keys and data replicated between them automatically by default
  - EC2 Instances need to be configured to access to all the different Elastic NEtwork Interfaces created for true high availability
- Any service inside your VPC can access the CloudHSM in a cluster by using the Elastic Network Interface injected automatically
  - An agent needs to be installed in EC2 instances to access the ENIs - a background process called The CloudHMS Client
    - After client is installed, can use industry standard APIs mentioned above to access the HSM cluster

## Use Cases for CloudHSM vs. KMS

### Considerations

- There is no native integration between CloudHSM and AWS services
  - i.e. cannot use it in conjuction with S3 Server Side Encryption for example
  - by default cannot access CloudHSM via standard AWS APIs
- For things that require AWS native integration, CloudHMS is NOT suitable, use KMS

### Uses

- Client Side Encryption
  - i.e. a crypto library is on a local machine and you want to encrypt objects before uploading to S3 (again, not integrated with S3, just using the lib on your machine to encrypt before sending)
- Offload SSL and TLS processing from web servers
  - Web service can benefit from not having to perform those operations
  - HSM is a piece of hardware optimized to perform those operations more efficiently vs. doing it on a EC2 instance
    - KMS cannot do this
- Enable Transparent Data Encryption (TDE) for products that can access Industry Standard APIs mentioned above like Oracle Database
  - this is a feature Oracle offers and it can then use CloudHSM for performing encryption operations and managing the keys.
  - This means since you have the keys, AWS has no way to decryupt that data
- Useful in very high security situations
- CloudHSM can be used to protect private keys for an Issuing Certificate Authority
  - i.e. if you're running you're own certificate authority
- Basically anything that has to use standards (FIPS 140-2 Level 3) and has to integrate with products which aren't AWS
