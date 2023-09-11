# EC2 Storage

## EBS: Elastic Block Storage
- Persists data even after instance is terminated. Good for long term storage
- Can only be mounted to one instance at a time
  - One instance can have multiple EBS volumes
  - it is not true for io1 and io2 volume types: this is called the EBS Multi-Attach feature.
- Bound to a specific Availability Zone
  - a volume in us-east-1a cannot be attached to us-east-1b
  - can move it if you snapshot it
- Think of it as a USB stick you can attach to instances
- network drive, NOT pyhysical - has latency
  - can be attached and detached easily
  - IF high performance is needed, use EC2 Instance Stores (see below)
- Billed by capacity
- provisioned capacity can change over time
- **ROOT** Volume has Delete on Termination attribute
  - default ticked to delete root volume, but not other attached volumes when instance is terminated
  - If you need to save data on the root volume of an instance, then you need to disable this delete attribute
  - Additional volumes attached will be set to `no` and will not be deleted by default when instance is terminated.
- After creating an EBS volume, you need to attach it to an instance 
- Remember when creating a EBS that you need to match the Availability Zone of the instance you want o attach to.
- Go to the EC2 Volumes dash in the AWS console, select the volume from the list then click `Actions` dropdown and select `Attach`
- To use multiple volumes, google `format volume EC2 attach` for links to make it available

## EBS Snapshots
- Backup of storage data at any time
- recommended to detach the volume before making a snapshot (though not necessary)
- Can copy snapshots across AZs and Regions through this procedure:
  - ex., snapshot a volume attached to instance in one region/AZ and use it to restore the data to a new volume in a different region for a different instance
- Snapshot Archive: Move a snapshot to 'archive tier' for 75% cheaper
  - useful for cheaper snapshots that you do not need quickly
  - Takes 24-72 hours to restore an archive
- Recycle Bin for EBS Snapshots
  - rules to retain deleted snapshots for recovery if deleted accidentally
  - specify retention - 1 day to 1 year
- To create a snapshot, go to volume and then Actions dropdown -> Create snapshot
  - To move it to another region, go to the Snapshots page in the left side menu and right click on the cnapshot in the list -> select Copy Snapshot and select
  

## EC2 Instance Store 
- Actual physical drive on EC2 Instance
- Used for higher performance I/O when needed
  - quicker than EBS Volumes which are network based with latency
- EPHEMERAL Store - if the instance is terminated the data is lost.  
  - Do not store critical data for long term storage
  - If you need long term storage then use a EBS Volume
- Good for buffer/cache/scratch data/temporary content
- Risk of data loss if hardware fails
  - you're responsible for backups and replication

## EFS: Elastic File System
- Managed NFS (Network File System) that can be mounted on many EC2 instances at one time (EBS can only be mounted to one instance at a time)
- Works with Linux instances in multiple Availability Zones
- Expensive, but pay as you go 
- Highly scalable, **SHARED** File system that can be shared across AZs

### EFS Infrequent Access EFS-IA
- Automatically moves files that are not accessed everyday to cost optomized storage
- EFS moves them automatically based on last access time
- Enable EFS-IA with a Lifecycle Policy (move files that are not accessed for 60 days to EFS-IA for ex.)

## FSx
- AWS service that allows access to third party file system storage solutions
- Can connect to these File Systems through your own external to AWS coporate data center or through EC2 instances
- **Two flavors are most used:**
- Amazon FSx for Windows File Server
  - fully managed, scalable Windows native shared file system
  - Supports SMB Protocol and NTFS
  - Integration with Microsoft Active Directory
- Amazon FSx for Lustre
  - Used for High Performance Computing (HPC)
  - derived from "Linux" and "Cluster"
  - Machine Learning, Analytics, Video Processing, Financial Modeling
  - sub ms latencies, 100 GB/s, millions of IOPs (IO Ops per second)
  - Stores data in background on AWS S3 buckets