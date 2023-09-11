# AWS CodeDeploy
- Used to automate deployment of application from a single interface
- **Hybrid service**
  - works for both EC2 Instances and on prem servers
- Servers must be provisioned ahead of time by you and configured with CodeDeploy Agent

# CodeCommit
- Store code in a repo on AWS (not GitHub)
- source control service that hosts Git based repo
- Fully managed, scalable and high availability
- Private secured and integrated with AWS

# AWS CodeBuild
- Build your code in the cloud
  - source  code is compiled, tests are run and packages/artifacts are produced to deploy
- Fully managed, serverless service
- scalable and secure
- Pay as you go pricing - pay for build time only when it happens

# CodePipeline
- **Pipeline tool to Orchestrate steps for deployment**
- CI/CD
- Pipeline can use CodeCommit and CodeBuild with CodeDeploy
- Compatible with GitHub and lots of other platforms

# AWS CodeArtifact
- Secure, scalable artifact management for software development
  - Typically you have to create artifact management system yourself using EC2 and S3 etc., this solves for that
- works with common management tools like Gradle, npm, yarn etc. to retrieve dependencies
- CodeBuild can retreive dependencies straight from CodeArtifact
- Helpful if team needs artifact management system or a place to store code dependencies
- AWS CodeArtifact is a fully managed artifact repository (also called code dependencies) service that makes it easy for organizations of any size to securely store, publish, and share software packages used in their software development process.

# AWS CodeStar
- Unified UI/Dashboard to manage software devellopment in one place
- **Quick way to get started while using best CI/CD practices**
  - Can use CodeCommit, CodeDeploy, CodePipeline etc all in one place instead of separately

# AWS Cloud 9
- online code IDE in the cloud
