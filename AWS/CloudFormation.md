# CloudFormation

- Create update and delete AWS Infrastructure using templates.
- Written in YAML or JSON

## Components of a Template

### Resources

- lists resources to create, if they are removed then they are deleted
- The only mandatory part of a template
- Example creating EC2 instance and security group resources:

```yaml
Resources:
  EC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: "t2.micro"
      ImageId: !Ref LatestAmiId
      IamInstanceProfile: !Ref SessionManagerInstanceProfile
      SecurityGroups:
        - !Ref InstanceSecurityGroup
  InstanceSecurityGroup:
    Type: "AWS::EC2::SecurityGroup"
    Properties:
      GroupDescription: Enable SSH access via port 22 and 80
      SecurityGroupIngress: # allow ports 80 and 22 traffic in
        - IpProtocol: tcp
          FromPort: "22"
          ToPort: "22"
          CidrIp: !Ref SSHandWebLocation # references values elsewhere in the template
        - IpProtocol: tcp
          FromPort: "80"
          ToPort: "80"
          CidrIp: !Ref SSHandWebLocation
```

### Description

- Free text field to add a description of the template
- What the template does, what resources it affects etc. whatever you want the user to know about the template
- The description field must immediately follow the `AwsTemplateFormatVersion` if both fields are used
  - **This is a Exam Trick question!**
- If AwsTemplateFormatVersion is ommitted, then it is assumed.

### Metadata

- specify tags and how the UI displays your template to users

### Parameters

- Apply input, default values etc. to fields
- LatestAmiId: special parameter where you can select the latest version of a particular image (i.e. Linux etc.)

```yaml
Parameters:
  LatestAmiId:
    Type: "AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>"
    Default: "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
```

- SSHandleLocation: specify IP address range to access a resource (i.e. an EC2 instance)

```yaml
SSHandWebLocation:
  Description: The IP address range that can be used to SSH to the EC2 instances
  Type: String
  MinLength: "9"
  MaxLength: "18"
  Default: 0.0.0.0/0
  AllowedPattern: '(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})'
  ConstraintDescription: must be a valid IP CIDR range of the form x.x.x.x/x. Default is 0.0.0.0/0 and is less safe.
```

### Mappings

- optional
- allows creation of lookup tables

### Conditions

- Set things only if condition is met
- Requires creating a condition
- Condition is used in resources to determine if they are created etc.

### Outputs

- Once template is finished outputs can be created (show what's created, details about resources modified etc.)
- example outputting details (including using CloudFormation Reference functions)

```yaml
Outputs:
  InstanceId:
    Description: InstanceId of the newly created EC2 instance
    Value: !Ref EC2Instance # cloudformation reference function (references another part of the template)
  AZ:
    Description: Availability Zone of the newly created EC2 instance
    Value: !GetAtt
      - EC2Instance
      - AvailabilityZone
  PublicDNS:
    Description: Public DNSName of the newly created EC2 instance
    Value:
      !GetAtt # function to select attributes of other parts of the template resources
      - EC2Instance
      - PublicDnsName
  PublicIP:
    Description: Public IP address of the newly created EC2 instance
    Value: !GetAtt
      - EC2Instance
      - PublicIp
```

## Template basics

- **Logical Resources**: Resources inside a CloudFormation template.
  - i.e. `Instance`
  - have properties that are used to configure them in a certain way
- **Stack**: When a template is given to CloudFormation it creates a stack which contains all the logical resources that the template tells it to contain.
  - A stack can contain zero or more other stacks
  - If a stack is deleted then all logical/physical resources are deleted.
- Templates can be stored for change management.

### Goal of CloudFormation Templates:

- For any logical resources in the stack, CloudFormation makes a physical resource in the account.
- The job of CloudFormation is to keep the logical and physical resources in sync all of the time.
- You can take the same template and use it to create multiple stacks that are consistent in configuration
- You can take the same template and create stacks in different regions

## Creating a Template

- Create a stack: AWS Console > CloudFormation > `Create Stack`
  - can use a sample template or create/upload a template
  - Uploaded templates (yaml files etc.) are stored in auto created buckets prefixed with `CF`
  - Click `Next`
- Provide a name (i.e. `cfmytemplate`)
  - Parameters will be set if template has those parameters set, otherwise fill them in
  - click `Next`
- Set advanced Settings if needed and click Next
- Scroll to bottom of next page and check the capabilities warning checkbox and click Submit to run the template.
- Will take a few minutes to create resources, refresh in the console (with UI button) and look for the entire stack (look for the stack name) to say `CREATE_COMPLETE` status.
- You can view the outputs from the template in the Outputs tab

### Deleting a Template

- If you delete a template stack, AWS will delete it and the physical resources specified in it.
