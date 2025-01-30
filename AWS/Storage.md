# Storage

### Types of Storage

- Direct (local) - attached physical disk storage
  - EC2: "Instance Store" attached to the Host
  - Fast, but if disk fails or EC2 fails or moves, the storage can be lost
- Network Attached Storage - Volumes are attached over the network
  - EBS - Elastic Block Store
  - Can survive hardware failures on the EC2 Host
- Ephemeral Storage - temporary unreliable storage that is not persistent
  - Instance Store on an EC2 host
- Persistent Storage - Permanent storage
  - Network attached storage EBS (Elastic Block Store)

### Categories of Storage

- **Block Storage**: collection of addressable memory blocks (each block has a unique memory address ID)
  - **NO STRUCTURE** - a File System is created automatically later etc. by the OS, or whatever you want for example
  - On a Volume provided via network or a physical drive on the machine
  - Typically when presented to a service a File System is created on top of the block storage (NTFS or ext3 etc)
  - Mounts as a C drive in Windows or the Root volume in Linux
  - Can Mount an EBS volume, for example or Boot off of a EBS Volume
  - Most EC2 instances use EBS as a boot volume that stores the Operating System and that is what is used to boot up and start the OS
  - Used for high performance or to boot from in EC2
- **File Storage**: **STRUCTURED** - has a File System builtin that is already there
  - Can create folders and files via the folder structure
  - Can Mount a File Storage
  - Can NOT Boot from File Storage! OS does not have low level access to the Storage
  - Normally given access to File Storage over the network via another AWS product/service
  - Used for access across networks
- **Object Storage**: No Structure - just a flat collection of Objects
  - object can be anything (binary data, images, movies, pictures, etc.)
  - Provide a key to fetch an object and get the object's value (data) in return
  - The Container for this flat collection is S3
  - Very scalable - can be accessed by millions of people simultaneously
  - can NOT mount it in a file system and cannot boot from it
  - Used for storing massive amounts of data/objects

### Storage Performance

- IO (block) size
  - Wheels (size affects capable speed)
  - Sizes of a block range from Kilobytes to Megabytes sizes
    - Data is spread out over the blocks or at minimum uses the block size
- IOPS (Input Output Operations Per Second)
  - similar to Revolutions per second in a car
- Throughput (amount of data transferred in a second - MB/s)
  - End speed = IO block size x IOPS
- These 3 factors interact and affect each other
  - Higher block sizes might reduce the IOPS you can achieve
  - Throughput could be capped limiting affect of Block size x IOPS

# EBS (Elastic Block Storage)

- Volume that can be linked to EC2 instances/services
- **ONLY AVAILABLE IN ONE AZ** - An EBS Volume in one Availability Zone is different from an EBS in another
  - Resilient within the AZ (if AZ fails though, the EBS volume will fail)
- Usually attached to 1 EC2 instance at a time over a storage network
  - can be detached from one instance and attached to another
- Persistent beyond instance lifetime. If an instance moves to another EC2 Host machine, then the EBS volume follows it and is still attached to it
  - Stops and restarts of instances do not affect the volume - it is maintained and persisted until the volume specifically is deleted

### Backing up EBS Volumes
- EBS Volumes are automatically replicated in the AZ they are in, but not across AZs for the region
- You can backup an EBS volume into S3 as a **Snapshot** (snapshots in S3 are regionally resilient and replicated across all AZs in the region)
  - Can use the snapshots taken in S3 to create another EBS volume in the same region in another Availability Zone with the same data
  - Useful for migrating data between AZs
- S3 Snapshots of EBS volumes can also be copied across to another region

### Billing

- billed by Gigabyte per month metric
