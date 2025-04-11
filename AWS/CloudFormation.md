# CloudFormation

- Create update and delete AWS Infrastructure using templates.
- Its purpose is to keep Logical and Physical resources in sync
- Written in YAML or JSON

## Components of a Template

### Resources

- **Logical Resources**: What you want to create (not how you want them created)
- CouldFormation Templates create Stacks
  - One template can create many Stacks
  - Templates should be portable - you can use them in many regions and accounts
    - Example of a non-portable template is hard coding a bucket name: the second template creation action will fail because Bucket names are unique!!!
    - Hard coding a AMI Image ID (they are unique per region, so if you move the stack to create in another region, it will fail because the ID does not exist in that region)
    - Use Template or psuedo parameters and do not hard code things!
  - Contained and defined in the `Resources` section of a CloudFormation Template (yaml file)
- The STACK creates physical resources based on the logical resources defined in the template

  - The Stack keeps the physical and logical resources in sync (if the logical resource in the template changes, the stack makes sure the physical resources are updated to it)
  - If the Stack is deleted, the physical resources are also deleted.
  - Once the logical resources enter a Create Complete state, other logical resources can reference physical properties on them (their ID etc.)
  - If the Stack is updated, the physical resources will be added or deleted automatically to keep in sync with it.

- lists resources to create, if they are removed then they are deleted
- The only mandatory part of a template
- Example creating EC2 instance and security group resources:

```yaml
Resources:
  EC2Instance: # Name of the logical resource - you can name this anything you want!
    Type: AWS::EC2::Instance # the physical type of the logical resource
    Properties: # resources will have properties which are what is used to configure them
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

- NOTE: it is rare that you create a template from scratch - usually you will consult resources
  - AWS has a CloudFormation [User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html) which includes lots of Template definitions for re-use or examples
    - Type the name of the resource you want to configure in the search box to get examples, etc.
    - Wrapping values in single quotes is safer
- **Logical Resources**: Resources inside a CloudFormation template.
  - i.e. `Instance`
  - have properties that are used to configure them in a certain way
- **Stack**: When a template is given to CloudFormation it creates a stack which contains all the logical resources that the template tells it to contain.
  - The purpose of a Stack is to keep logical and physical resources in sync
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

## Troubleshooting

- To find errors in the CloudFormation process, in the CloudFormation dashboard/page, click the Events Tab and then click the L9ogical ID (Stack name) > Click the Events tab and look at the Status reason column for the time you want to see what failed.
- ![alt text](cloudformationdebugging.png)

## Template and Psuedo Parameters

- Used to prevent hard coding values in templates so the templates remain portabile
- Parameters accept input
  - Input can be provided via the console or CLI when a Stack is updated or created and is used in these parameters
    - Env for the template (Dev, Test, Prod), the Size of the instances, etc.
- Can define constraints or configuration for the parameters:
  - `Defaults`: what to use if input is missing
  - `AllowedValues`: a list of valid inputs, i.e. a list of instance types that are accepted
  - Restrictions such as `Min` and `Max` lengths of input allowed or `AllowedPatterns`
  - `NoEcho` for passwords or secrets to hide the input when it's being typed
  - `Type`: the type of the input - String, Number, List, or AWS specific types (you can populate this so you can have an interactive prompt to choose the type from a list of types)

### Template Parameters Example

```yaml
Parameters: # params go under this section in the template yml
  InstanceType: # name of the parameter
    Type: String # type of the param
    Default: "t3.micro" # define a default if no input
    AllowedValues: # only allow these values for the param
      - "t3.micro"
      - "t3.medium"
      - "t3.large"
    Description: "Pick a supported Instance Type." # could be useful for UI or hint to a user when loaded into the AWS Console UI or console etc.
  InstanceAmiId: # another name of another parameter
    Type: String # this parameter has no validation or restrictions as above so it is free text (anything can be entered for the AMI ID)
    Description: "AMI ID for Instances"
```

### Pseudo Parameters

- [AWS Documentation - Pseudo Parameters](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/pseudo-parameter-reference.html)
- Provided by AWS (instead of input like Template Parameters above)
  - These parameters exist even if you don't define them and are built-in. They can be referenced in the Template at will. They are injected by AWS into the Template/Stack
    - `AWS:Region` - the value of this always matches whichever region the template is being applied in.
    - `AWS:StackId`: populated with the ID of the Stack being applied
    - `AWS:StackName`: The name of the stack being applied
    - `AWS:AccountId`: populated with the account number the stack is being created in

## CloudFormation Intrinsic Functions

[List of Functions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html)

- Allow you to gain access to data at Run Time
  - Allows you to take action based on how things are when a template is being used to create a stack

### Commonly Used Functions

- `Ref` and `Fn:GetAtt` (Get Attribute): Allows you to reference a logical resource from another one
  - Ex: making sure that a subnet goes into a specific VPC, you can reference it
  - Can use `GetAtt` to access Primary and Secondary values returned from logical resources (i.e. their Physical IDs)
- `Fn::Join` and `Fn::Split`: Join or split strings
  - Ex: Can take the name/IP of an EC2 instance to create a web url for people to access it (?)
- `Fn::GetAZs` and `Fn::Select`: Get a list of Availability Zones and Select one from that list (i.e. get AZs from a region and pick one out)
- `IF`, `And`, `Equals`, `Not`, `Or`: Conditionals you can use
  - Ex: If the environment is Production, then deploy a bigger instance type or if Development, then deploy smaller ones etc.
- `Fn::Base65`: Accepts non-encoded text and outputs base64 encoded text
  - Many inputs to AWS need to be in Base64 (ex: user data scripts)
- `Fn::Sub`: Allows you to substitute things in text based on runtime information.
  - Ex: Passing build information into EC2 and you want to provide a value from the Template Parameters
- `Fn::Cidr`: build CIDR ranges for networking
- `Fn::ImportValue`
- `Fn::FindInMap`
- `Fn::Transform`

### Using The Functions

- Place a bang `!` before the function name

#### Ref

- Every logical resource and parameter has a main value that it returns
  - i.e. the main value returned from creating a logical EC2 instance resource is it's ID
  - Note: The Physical ID for a resource is usually returned as its primary value which can be accessed with the `GetAtt` function
  - Some resources have both primary values and secondary values that they return
- The `Ref` function can be used to reference this main value of a parameter or a logical resource

```yaml
Resources:
  Instance:
    Type: "AWS::EC2::Instance"
    Properties:
      ImageId: !Ref LatestAmiId # using ref with a parameter
      InstanceType: "t3.micro"
      KeyName: "A4L"
```

#### GetAtt

- When an instance reaches Create Complete state, it makes available a range of data (including the primary value it returns - it's ID)
- `!GetAtt LogicalResource.Attribute`
  - i.e. `PublicIp` or `PublicDnsName` attributes

#### GetAZs

- Environmental Awareness function - useful for avoiding hard-coding AZ names you want to deploy resources into so that your template is portable
- Ex: get a List of AZ names for a specified region, or use the Region pseudo parameter, or leave the region blank (will default to using the current region used to create the current stack)
  - `!GetAZs "us-east-1"` - returns a list of AZ names that exist in the region
  - **NOTE**: The list of AZs is only those where the Default VPC has subnets in that AZ
    - Normally, this is fine unless you have configured or deleted subnets from your Default VPC (those AZs with no subnets will not be returned in the list!) - also, you NEED a default VPC!
- After retrieving the list, use the `!Select` function to get one from the list returned
  - Accepts a list and a index number (0-based) and will select the numbered index from the list

```yaml
Instance:
  Type: "AWS::EC2::Instance"
  Properties:
    ImageId: !Ref LatestAmiId
    InstanceType: "t3.micro"
    AvailabilityZone: !Select [0, !GetAZs ""] # Get the list, pass it into Select and specify the index
```

#### Split

- Accepts a delimiter to split on and a single string value. Returns a list

```yaml
!Split ["|", "str1|str2|str3|str4"] # returns ["str1", "str2", "str3", "str4"]
```

#### Join

- Accepts a delimiter and a list of values

```yaml
WordpressURL:
  Description: Instance Web  URL
  Value: !Join ["", ["http://", !GetAtt Instance.DNSName]] # returns 'http://dnsname.com
```

#### Base64 with Sub

- Base64 needed for things like user data scripts to convert the plain text to the accepted required base64 encoded text
- Sub can be used to interject parameters into the text by wrapping them in `${paramName}`
  - **YOU CANNOT SELF REFERENCE WITH SUB** - i.e. you can't reference the Instance.InstanceId for example since that resource is not created yet

```yaml
UserData:
  Fn::Base64: !Sub |
    #!/bin/bash -xe
    yum -y update
    yum -y install httpd
    echo "${someParameter}"
```

#### Cidr

- Can reference a CIDR range of a VPC (`!GetAtt VPC.CidrBlock`), tell it how many subnets to allocate and the size of the subnets and you will get an output of a list of CIDR ranges which you can use within subnets within a VPC (this way you don't have to manually allocate the ranges otherwise)
  - Combine this with the `!Select` function to allocate those ranges to subnets individually
- Allows you to assign CIDR ranges to subnets in a automated portable way
- Limitations:
  - Cannot allocate or unallocate ranges (advanced techniques can get around this)
    - Based on the Parent VPC CIDR Range

```yaml
VPC:
  Type: AWS::EC2::VPC
  Properties:
    CidrBlock: "10.16.0.0/16"
Subnet1:
  Type: AWS::EC2::Subnet
  Properties:
    # Pass Cidr function the CIDR range of the VPC, tell it 16 ranges total, with a range size of 12
    # Use Select to pick out the first range returned in the list of possible ranges we can use
    CidrBlock: !Select ["0", !Cidr [!GetAtt VPC.CidrBlock, "16", "12"]]
    VpcId: !Ref VPC
Subnet2:
  Type: AWS::EC2::Subnet
  Properties:
    # for subnet 2 select the second CIDR range we can use from the list
    CidrBlock: !Select ["1", !Cidr [!GetAtt VPC.CidrBlock, "16", "12"]]
    VpcId: !Ref VPC
```

## CloudFormation Mappings

- `Mappings` is a top level key in a CloudFormation template (along with `Resources` and `Parameters` for ex.)
- Useful for making Cloudformation Templates portable
- Contains many mappings of logical resources
  - Each mapping maps keys to values allowing information lookup
  - i.e. map 'Production' environment to a particular database configuration or specific SSH key
- Can have top or second level keys
  - ex: mapping of AMI IDs which have `region` and `architecture` keys
- Use `!FindInMap` instrinsic function to lookup a value in the Mapping
  - `!FindInMap [ MapName, ToplevelKey, SendlevelKey]`
- Typical use case is to store an AMI lookup table you can use to use a particular AMI for a given AWS region and architecture/app/environment type etc.
- Example of `RegionMap` in a cloudformation template under the `Mappings` top level key

```yaml
Mappings:
  RegionMap:
    us-east-1:
      HVM64: "ami-12345"
      HVMG2: "ami-456789"
    us-west-1:
      HVM64: "ami-j1k2j3"
      HVMG2: "ami-udih33"

# Use FindInMap to get the value:
!FindInMap [ "RegionMap", !Ref 'AWS::Region', 'HVM64'] # retrieves the ami id in us-east-1 using HVM64 arch for example
```
