# EC2 Image Builder
- Automates setup, creation maintenance and validation of Virtual Machines or images
- Creates EC2 Instance -> creates a new AMI -> Tests EC2 Instance -> Distribute AMI (multiple regions possible)
- The service is free - you are only charged for the resources created
- Can run on a schedule (weekly, whenever packages are updated etc)
- Output can be an AMI or a Docker Container


## Implementation
- You need to create a Image Pipeline and then run it to create the image.
  - The pipeline will create built and test images while running and output an AMI or container at the end of it.  These are temporary instances that will be terminated when complete
  - Statuses for the image are Build, Test, Distributing and Available
- Permissions: Need a IAM role that has following policies attached:
  - Check the image pipeline Infreastructure configuration option for "Create Infrastructure configuration using service defaults" in the setup wizard for a list of basic policies needed for role
- After the pipeleine reports Available, launch an instance and assign the created recipe/AMI to it by selecting My AMIs for that option and selecting the created AMI