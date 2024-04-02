# AMI - Amazon Machine Image

- Customizable image for EC2 instance
- The AMI must be in the same region as that of the EC2 instance to be launched. If the AMI exists in a different region, you can copy that AMI to the region where you want to launch the EC2 instance. The region of AMI has no bearing on the performance of the EC2 instance.
- Enables faster boot/configuration time because all software is prepackaged
  - Normally when you start a EC2 instance you need to set it up with the bootstrap User Data script to install packages and software for a new instance
  - When using an AMI, you can package this software so it is 'pre-installed' and the instance using the AMI will boot up and start faster since it does not have to download and install the setup software as before
- We build AMIs for a specific region, and they can be copied across regions
- Public AMIs are available by AWS or through AWS Marketplace made by third parties, or you can make custom ones you maintain yourself
- Has one volume by default

### Block Device Mapping

- EC2s have Block Device Mapping: determines which volume is a boot or data volume (maps volumes to Device IDs or how the Operating System sees volumes)

### Access for usage

- Public AMIs - created by anyone
- Owner AMIs - Only an owner can create from the AMI
- Explicit Access - specify who can use the AMI
- Connect to EC2 instances with ssh key pair
  - keep the downloaded private part safe.
  - the public key goes on the instance

## Types of Images

- Windows images
  - use rdp (remote desktop protocol) to connect on port 3389
- Linux images
  - uses ssh protocol (port 22)
