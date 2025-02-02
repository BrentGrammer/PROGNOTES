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

### EBS Types

#### GP2 - General Purpose Storage

- Good general purpose and current default (but will probably change to GP3)
  - Good for boot volumes, low latency interactive apps, dev and test environments
- General Purpose Storage (SSD) - high performance storage for a low price
- Can create a volume as small as 1GB or as large as 16TB
- Initialized with IO credit
  - A IO (input output) credit is a 16KB chunk of data - IOP = 16KB in one second
    - Example: 160KB file represents 10 IO blocks of data, if you use that on one second then that is 10 credits in one second (10 IOPS )
  - You need IO Credits to perform operations on disk - capacity is 5.4 million IO credits in a bucket
  - Baseline performance: every volume size has a minimum performance rate - at least a 100 IO Credits per second rate
    - 250 MB/s maximum throughput (vs. 1000 for GP3)
    - Baseline rate is based on size: 3 IO Credits per second, per GB of volume size.
      - Ex: 100 GB volume = 300 IO Credits per second refilling the bucket
      - Anything below 33.33 GB volume size gets the 100 IO Credits per second base rate
  - By default GP2 EBS Volumes can burst up to 3,000 IOPS (3000 x 16kb per second). This allows for small volumes with periodic heavy workloads.
  - Note: The IOPS bucket starts out full (5.4 Million IO Credits), so you could run high loads at 3000 IOPS for at least 30+ minutes
  - **If you consume more IO Credits at a rate higher than your bucket is refilling then you will eventually empty the bucket** - you need to manage your IO Credit buckets for your volumes to make sure they are not being emptied to 0
  - For Volumes greater in size than 1TB, they have a replenish rate exceeding the burst rate of 3000 IO Credits per second
    - MAX rate is 16,000 IOPS (any volumes above 5.33 TB in size gets this rate constantly)

#### GP3 - General Purpose Storage

- Generally simpler and cheaper than GP2 type volumes (even including higher IOPS and higher max throughput extras)
  - Useful for virtual desktops, medium size databases, dev and test environments, etc.
- Newer SSD based EBS Volume type that removes the IO Credit architecture of GP2
  - Does not add IOPs automatically with higher size scaling - you need to pay for and add extra IOPS capability manually
- Every GP3 volume starts with 3000 IOPS (3000 x 16KB operations per second) by default
  - can transfer 125 MB per second
- Base price is 20% cheaper than GP2 - just use GP3 if not using more than 3000 IOPS
  - If more performance is needed you can pay for up to 16,000 IOPS or up to 1,000 MB/s
  - 1,000 MB/s max throughput vs. 250 MB/s for GP2!
- Max per instance: 260,000 IOPS, 7,000 MB/s (you can have multiple volumes operating together on one instance to achieve the max performance cap)

#### io1/2 - Provisional IOPS SSDs

- Designed for super high performance scenarios where consistent low latency (sub-millisecond) is needed
  - useful for having smaller volumes but super high performance
- IOPS are configurable independent of the size and volume (as opposed to GP2/3)
- Can get maximum of 64,000 IOPS per volume, 1,000 MB/s throughput
  - io2 Block Express is newest and allows for 256,000 IOPS per volume and 4,000 MB/s througput
- Volume Sizes range from 4GB to 16TB
- Max performance ratios:
  - io1 - 50 IOPS per GB of size
  - io2 - 500 IOPS per GB of volume size
  - Block Express is 1,000 IOPS per GB of volume size
  - Max performance per EC2 Instance connected: usually you'll need multiple volumes to saturate the performance max for adv. EC2 instances (you need multiple volumes operating together per instance to achieve the max performance/limit)
    - io1 max: 260,000 IOPS per instance and 7,500 MB/s throughput (need 4 vols at max to achieve limit)
    - io2 max: 160,000 IOPS per instance at 4,750 MB/s
    - io2 block express max: 260,000 IOPS, 7,500 MB/s

#### HDD EBS Volumes

- Slower with moving parts - cheapest EBS storage available
  - Useful for holding very large sets of data (logs, big data, data warehouses, archived data) that are less frequently accessed (less than a few loads of scans per day)
- Sizes range from 125 GB to 16 TB in size
- st1: throughput optimized and cheap. Designed for cheap cost, but frequent access is needed for throughput intensive sequential workloads
  - Used for Big Data, Data Warehousing, Log processing
  - Max of 500 IOPS
  - **IO is measured in 1MB blocks on HDDS** - 500 IOPS = 500 MB/s
  - Credit buckets similar to GP2 - different values - 40 MB/s per TB of volume size
  - Burst to max of 250 MB/s for every TB of volume size
- sc1: Cold storage HDD, slower. Designed to cheaply store lots of data that is infrequently accessed (low performance)
  - Useful for anything that is not day to day accessed (otherwise use st1)
  - Max of 250 MB/s
  - 12 MB/s per TB of volume size
  - Burst of 80 MB/s per TB of volume size

## Instance Store Volumes

- Block storage physically connected directly to one EC2 instance Host that can be used as a file system by the operating system
