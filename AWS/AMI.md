# AMI - Amazon Machine Image

EC2 instances are launched with AWS provided AMIs (i.e. Linux images, etc.)

### Images

- AWS or community provided AMIs can be used
  - RedHat, Centos and Ubuntu have custom AMI images available for use to launch EC2 instances with these linux distributions
- Marketplace commercial AMIs
  - There is an extra cost for the commercial image in addition to the normal instance cost
- AMIs are regional (AMIs are only for use in one region) and each region has a set of AMIs separately
  - The image for the same distribution will have a unique ID in different regions
  - Can be copied between regions if needed
- Naming convention: `ami-0a887e401f7654935`: ami hyphen and random set of numbers and letters
- No data is contained in an AMI - it is a container that references snapshots created from an original EBS Volumes with the original device IDs
- Can use AMIs to launch new instances with exactly the same data as the source and same configured EBS volumes, etc.
- Cannot be edited. If you need a modification, use the AMI to create a new instance, update its configuration, then make a new AMI based on that new configuration.

### Permissions

- By default an AMI is set so that only your account can use it
- AMIs can be set to be Public, so everyone can access it
- Can set specific AWS Accounts for access to the AMI which only they can access it

### Creating AMIs

- Can create instances from AMIs
- "AMI Baking": Can create an AMI from an existing EC2 instance to capture the configuration of that instance

### Lifecycle

- Launch
  - An initial EC2 instance launch
- Configure
  - Add customizations to bring the EC2 into a state that is ideal for business purposes
- Create Image (from the existing instance)
  - When creating from an instance, a full snapshot is taken of any EBS volumes attached to it
  - The snapshots are referenced in the AMI via a Block Device Mapping (table mapping snapshot ID taken to the device IDs, i.e. /dev/xvda, that the original volumes had on the EC2 instace)
- Launch
  - Snapshots are used to create new EBS Volumes for the instance using the device IDs from the Block Device Mapping (see above)
  - You need to deploy the AMI into the same region the instance was in that you created it from

### Billing

- Charged for EBS Volumes (snapshots)
- Charged for only the percentage of data used
- Cost is based on storage capacity used by the EBS snapshots that the AMI references

### Update Message of the Day (motd)

```
sudo dnf install -y cowsay

sudo nano /etc/update-motd.d/40-cow

#!/bin/sh
cowsay "Message when logging in to this EC2 instance - info on image and company etc. or other info"

sudo chmod 755 /etc/update-motd.d/40-cow
sudo update-motd
sudo reboot
```

## Creating an AMI from an Instance

[Video Demo](https://learn.cantrill.io/courses/1101194/lectures/29064547)

- This should be done to reduce the admin overhead needed to launch a new instance (setup software, install dependencies etc.). You can set the EC2 Instance to a base configuration and make an image to launch with that config every time.
- First, Stop the instance you want to make a template of (should not create an AMI from a running instance)
- Right click on the stopped image in EC2 list and select Image and templates > Create image
- In the EC2 > left side menu Images/AMIs list, right click on the AMI created and select Launch instance option
- When sshing into the new instance via instance connect you might see "root" for the user, change that to "ec2-user" or whatever one you configured if necessary
- To copy an AMI to another region, just right click the AMI and select Copy AMI and select another region in the copy page.
  - The copied AMI to another region is a **different AMI** (it will have a different ami ID) since AMIs are regional
- To delete the AMI, right click in console list and select "Deregister AMI" - remember to delete the snapshot for it as well.

### AMI Permissions

- By default, AMIs are private - they are only accessible in the account in which they were created.
- Right click on the AMI in the list and select "Edit AMI Permissions"
- If you set the AMI to Public, any account can access it (not recommended)
  - Need to be careful that there is no sensitive data in the snapshot for that AMI
  - See [docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/sharing-amis.html) for best practices when sharing publicly
- A safer way to make AMI accessible is to keep it private and add explicit accounts that can access it
  - i.e. you could share the AMI with the Prod account for the organization
    - Go to Organizations in the AWS console and find the account in the org you want to share it with - copy its ID and use it to add an account ID in Edit Permissions of the AMI
    - Can alternatively share with the entire Organization (all accounts in it)
    - If sharing internally, then you should select "Add 'Create volume' permissions to associated snapshots when creating account permissions" (this gives the other account permissions to make snapshots from the volume and create additional AMIs)

---

Old Notes

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

- **Permissions**: Public Access, Owner Only, Specific AWS Accounts

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
