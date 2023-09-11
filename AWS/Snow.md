# Snow

- Physical devices AWS sends you for large data transfer jobs.
- Alternative to transfering over the network for TB or PB of data
- Use generally for scenarios that take more than a week to transfer data

## Process
- Request Snowball device and have it shipped to you
- Load data on to it and send it back to AWS
- AWS will take the data on the device and load it into S3 Bucket


Devices:

- Snowball Edge
  - Pay per transfer job
  - Provides block storage
  - Storage or Compute Optimized versions
    - Both offer local compute power, but Compute Optomized is specialized for ultra high performance
  - Used for data migrations, Decommission data center, disaster recovery by backing up data
-  Snowcone
  - Smaller device that is rugged, light and can withstand harsh environments
  - 8 TB of storage - much less than the Edge
  - Use in space constrained environments or on a drone etc.
  - Can be sent back or done over network using DataSync to send data to AWS
- Snowmobile
  - An acutal truck for exabytes of data
  - used for more than 10 PB of data
  - Climate controlled and secure truck


  # Edge Computing
  - processing data at locations that have no internet or is far from the cloud.  Mines, sea, on the road 
  - Use is to run compute power at locations where it is not available over the network.
  - Machine learning, preprocess data, transcode media 
  - Can optionally ship it back to AWS
  - Can use EC2 instances or Lambas with AWS IoT Greengrass service
  - Discount pricing for long term borrowing 1-3 years

  OpsHub: Graphical GUI you can install on your computer to make interfacing with Edge devices easier