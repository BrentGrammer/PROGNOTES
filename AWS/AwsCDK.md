# AWS CDK (Cloud Development Kit)

[AWS CDK with Lucee Repo](https://github.com/BrentGrammer/ModernizeJSApp/tree/aws-cdk)
[AWS CDK Generic Project Repo](https://github.com/BrentGrammer/AWS-CDK)
[AWS API Documentation](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-construct-library.html)

- Infrastrcture as Code using a language of your choice (with CloudFormation, you have to use YAML)
  - JavaScript (or TypeScript)
  - Python
  - Java
  - GoLang
  - C#
- Uses and generates a CloudFormation template under the hood for you
- Advantages include much simpler syntax and all the benefits of using code like if conditionals, loops etc.
- Comes with helper functions that makes IAM management and permissions much easier to grant and control

## Constructs

- A building block in AWS which can correspond to a single AWS resource or higher level constructs (more than one AWS resource)

### L1 Constructs

- CFN Resource
- "CFN" means you are using an L1 Construct in CDK, i.e. a "CFN Bucket" is an L1 S3 Bucket
  - `new CfnBucket( ... )`
- Lowest level construct in CDK - allows you to define every setting on the resource directly
- These are only needed and useful when you need extreme control over all the settings of the resource
  - Almost never needed normally, usually used for special cases

### L2 Constructs

- Curated Constructs - applies to one single AWS Resource
  - `new Bucket( ... )`
- Medium level of abstraction and less low level than L1 constructs - easier to use
- L2 Constructs provide sensible defaults for you if you don't provide a setting

  - You can override it later if you want
  - Example: Update and Deletion policies are set to Retain automatically with L2 Constructs because if you change a resource like a S3 bucket with data, the default is to delete it, but that could result in data loss:

  ```yaml
  # set by L2 constructs by CDK
  UpdateReplacePolicy: Retain # will retain if the stack resource is updated
  DeletionPolicy: Retain # will retain if the stack is deleted
  ```

  ```javascript
  // LEVEL 2 Construct example
  const level2S3Bucket = new Bucket(this, "MyFirstLevel2ConstructBucket", {
    versioned: true, // much easier to use than level 1
    bucketName: "MyFirstLevel2ConstructBucket12345", // override the default generated name (if left out)
    removalPolicy: cdk.RemovalPolicy.DESTROY, // how to override the default retain policy -->
  });
  ```

- Come with security best practices and come out of the box with good security settings (not too lenient)
- Come with a suite of useful helper methods in CDK
- These are the most commonly used constructs in CDK

### L3 Constructs

- Construct Patterns - can contain more than one AWS resource and come as a package to solve a problem with a particular architecture solution
- Lambda paired with SQS queue or Load Balancer with a set of EC2 instances, etc. - common patterns of resources
- Control is sacrificed using these patterns and is the tradeoff
- Useful when the patterns match what you want to do and you sacrifice configuration for speed
- Very opinionated constructs and not used as often as L2 constructs

See [Constructs Hub](https://constructs.dev/) for constructs to use that are open source and made to quickly start using some patterns.

## Stacks

- Containers of Constructs that are related
- By default everything in your CDK code is under one Stack, but you can optionally separate parts into separate Stacks containing related infra and organize resources
  - i.e. a "Dashboard Stack" with CloudWatch Alerts and Alarms, etc. or a "Storage Stack" with storage related resources like S3 Buckets
- Parameters can be passed into stacks and returned out of them and passed around to other stacks

## Apps

- Collection of Stacks
- One App per project limit
  - As many stacks and constructs in it as you want - no limit there

# Adding CDK to an existing Project (resources already created)

- AWS Console > CloudFormation > IaC Generator
- IaC Generator can scan existing resources and then create a CloudFormation Template from its findings
- Bring the generated CloudFormation template into your project and then create a new CDK project from that template
  - Create an empty directory to hold the CDK project
  - cd into the new folder and run `cdk migrate --stack-name <namethestack> --language javascript --from-path path/to/template.yaml`

## Outputs

- Use `CfnOutput`
- You can see the Outputs in the CloudFormation page in AWS Console by looking at the Outputs tab

```javascript
new CfnOutput(this, "LogicalResourceName", bucket.bucket_name);
// This will put this information in the Outputs: section of the produced CloudFormation Template when you run `cdk deploy`
```

## Custom Resources

- Used to run processes during cdk deployments that might require logic (via a backed lambda) or to communicate with AWS resources such as parameter store
- CloudFormation only invokes a custom resource's Lambda when the custom resource is created, updated, or deleted. If the custom resource's properties haven't changed since the last deployment, CloudFormation reuses the previous response and doesn’t re-invoke the Lambda

### Getting a Parameter Store SecureString JSON using the Built-in Custom Resource:

```typescript
import * as cr from "aws-cdk-lib/custom-resources";

const JSON_PARAM_NAME = "/myapp/secrets/jsonsecret";

// Using builtin custom resource to get ssm param: https://docs.aws.amazon.com/cdk/api/v1/docs/custom-resources-readme.html#restricting-the-output-of-the-custom-resource
const getParameter = new cr.AwsCustomResource(this, "GetParameter", {
  onUpdate: {
    service: "SSM",
    action: "getParameter",
    parameters: {
      Name: JSON_PARAM_NAME,
      WithDecryption: true,
    },
    physicalResourceId: cr.PhysicalResourceId.of(Date.now().toString()), // Forces fetch to parameter store on each deploy
  },
  policy: cr.AwsCustomResourcePolicy.fromSdkCalls({
    resources: [
      `arn:aws:ssm:${cdk.Aws.REGION}:${cdk.Aws.ACCOUNT_ID}:parameter${JSON_PARAM_NAME}`,
    ],
  }),
});

const paramValue = getParameter.getResponseField("Parameter.Value");

const prop1Split = cdk.Fn.split('"prop1": "', paramValue);
const prop1Part = cdk.Fn.select(1, prop1Split); // Part after '"prop1": "'
const prop1 = cdk.Fn.select(0, cdk.Fn.split('",', prop1Part)); // Take value before '",'

const prop2Split = cdk.Fn.split('"prop2": "', paramValue);
const prop2Part = cdk.Fn.select(1, prop2Split); // Part after '"prop2": "'
const prop2 = cdk.Fn.select(0, cdk.Fn.split('",', prop2Part)); // Take value before '",'

new cdk.CfnOutput(this, "ConcattedParam", {
  value: cdk.Fn.join("--", [prop1, prop2]),
  description: "Parsed values from the custom resource",
});
```

### Using A Lambda to Back a Custom Resource for Custom Logic:

```typescript
// Use NodejsFunction to get properties to automatically install all packages in package.json when deploying, so you don't have to include them before running cdk deploy
import { NodejsFunction } from "aws-cdk-lib/aws-lambda-nodejs";

const customResourceLambdaHandler = new NodejsFunction(
  this,
  "SomeCustomResourceLambda",
  {
    runtime: lambda.Runtime.NODEJS_20_X,
    handler: "handler", // Name of the exported function in index.js
    entry: path.join(lambdaPath, "MyCustomLambdaFolder", "index.js"), // point to where you define the lambda and logic in your project
    timeout: cdk.Duration.seconds(300),
    bundling: {
      externalModules: [], // Specifying this as an empty array includes all packages listed in the lambda folder's package.json and installs them when deployed. include a package-lock.json in the lambda folder if you want consistent versions
      minify: true, // Minify the code to reduce bundle size
    },
  }
);
```

# Example Usage

## Prerequisites

- AWS Account
- Node.js
- AWS CLI configured with a user profile using a AWS Access Key and AWS Secret Access Key
- AWS CDK

## Set up

NOTE: Using CDK is usually done as it's own 'sub-project' and the code is kept separate in a folder, for example.

### Install AWS CDK

- `npm install -g aws-cdk`
- or `npm init -y` to initialize local package.json and `npm install aws-cdk` to install just to your project

### Initialize CDK

- CDK must be init in an empty directory, so make a new project directory subfolder if needed
- `cdk init app --language <language>`
  - ex: `npx cdk init app --language typescript`
  - Use `npx` if installed locally to your project

#### Note on Tests

- Note the tests folder in the project created - you can actually write unit tests to ensure that it is being created as you expect before it's created
- They take in a stack definition and make assertions on the template produced

### CDK Project Structure

- `bin` folder contains the **App**
- `lib` folder contains the **Stacks**
  - This is where the constructs and infra is defined

### CDK Commands

- `cdk help`
- `cdk list`: list of stack names in the project
- `cdk diff`: good for checking what has changed in your new template that will be produced from the last
- `cdk synth`: Make the CloudFormation Template for view or inspection
- `cdk bootstrap`: Required to run this if using cdk for the first time in a particular account and particular region
- `cdk deploy`: Deploys the infra to AWS
- `cdk watch`: monitors changes in IDE and auto-deploys when you save a file with changes (i.e. your stack file)
- `cdk destroy`: for cleaning up
- `cdk doctor`: diagnoses problems with CDK installation, any problems and will tell you if there is a new version and how to install etc.
- `cdk deploy --dry-run`: Careful if you are asked to deploy, this will actually deploy. It should not, but it might if you confirm and say "yes"

### CDK Bootstrap

- Required to run once per account/region you're using CDK
- Creates a CloudFormation Stack in your account called something like `CDKToolKit`

### Deploying with CDK

- `cdk synth`: generate and examine the cloud formation template
- `cdk deploy`: Will deploy all resources/stacks written in the code (bin and lib folders)
  - NOTE: `cdk deploy` runs `cdk synth` and generates the template, so that is an optional command and not required.

### Deleting a deployed Stack

- `cdk destroy`
