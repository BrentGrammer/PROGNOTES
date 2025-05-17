# Git Submodule

- Need to manually pull in submodule in pipeline:

- Git submodules are essentially pointers to other repositories. When you clone your main repository, Git doesn't automatically download the submodule's content by default. It just checks out the pointer.
  - jarssubmodule/aws_sdk exists as a directory in your local project, its contents (the actual files) aren't present until you explicitly initialize and update the submodule.
  - When you create your deployment ZIP/TAR.GZ artifact, if your build process doesn't explicitly fetch the submodule's content, then that directory will either be empty or only contain the .git file that points to the submodule's repository. CodeDeploy then tries to copy files from within it and finds nothing, leading to the "No such file or directory" error.
- To push changes to the submodule from local, cd into the folder containing the submodule files and do normal git operations, `git push`

```shell
# Assuming you are in the root of your main repository
# this command will pull the actual content of your jarssubmodule/aws_sdk into your local working directory where the script is running.
git submodule update --init --recursive
# Now create your zip file, including the submodule content
zip -r my_deployment.zip . -x "*.git*" # Exclude .git files
```

### Prerequisites

Existing Lucee project in a Bitbucket Git repository (e.g., lucee-project).
Git installed locally.
Lucee server setup (local or remote) with access to its classpath (e.g., /lib or custom path).
Basic familiarity with Git and Lucee configuration.

### Step 1: Create the Submodule Repository

Create a new repository on Bitbucket (e.g., lucee-jars).
Navigate to a separate folder (outside of lucee-project) where you want to work on the lucee-jars repository independently.
Clone the lucee-jars repository from Bitbucket:

```
cd /path/to/separate-folder
git clone <bitbucket-url>/lucee-jars.git
cd lucee-jars
```

Add JAR files (e.g., aws-java-sdk-core-<version>.jar for com.amazonaws.util.Base64):

```
mkdir lib
cp /path/to/example.jar lib/
Commit and push the changes:
```

```
git add lib/example.jar
git commit -m "Add example.jar"
git push origin main
```

### Add JAR files (e.g., example.jar):mkdir lib

```
cp /path/to/example.jar lib/
```

Commit and push:

```
git add lib/example.jar
git commit -m "Add example.jar"
git push origin main
```

### Step 2: Add Submodule to Lucee Project

```
git clone <bitbucket-url>/lucee-project.git
cd main-lucee-project
```

Add the lucee-jars repository as a submodule:

```
# use .git clone url or http url for your submodule repo
git submodule add git@bitbucket.org:mycompany/lucee-jars.git path/to/clone/submodule/to
```

This creates a folder at the specified path and clones the submodule into it.
Commit and push:

```
git commit -m "Add lucee-jars submodule"
git push origin main
```

Commits the changes staged after running git submodule add https://bitbucket.org/mycompany/lucee-jars.git lib/jars. These changes include:
The creation of the .gitmodules file, which records the submodule’s path (lib/jars) and URL (https://bitbucket.org/mycompany/lucee-jars.git).
The addition of the lib/jars directory as a special Git entry pointing to a specific commit in the lucee-jars repository.

Your local lucee-project repository now has a record of the lucee-jars submodule, including its configuration and the specific commit it references in the lucee-jars repository.
The .gitmodules file and the lib/jars entry are now part of the repository’s history.
Example .gitmodules content after the commit:
text

```
[submodule "lib/jars"]
    path = lib/jars
    url = https://bitbucket.org/mycompany/lucee-jars.git
```

#### NOTE: Submodule Content Not Pushed:

- The git push origin main command only pushes the lucee-project repository’s changes (including the .gitmodules file and the lib/jars reference).
- The actual content of the lucee-jars repository (e.g., JAR files) is managed separately in its own repository (https://bitbucket.org/mycompany/lucee-jars.git).
- Updates to lucee-jars (e.g., new JARs) must be committed and pushed in the lucee-jars repository.

### Cloning with Submodules

- After pushing, anyone cloning lucee-project needs to use:

```shell
# simpler and recommended on first clone - gets and clones all submodules automatically for project
git clone --recurse-submodules https://bitbucket.org/mycompany/lucee-project.git
```

Or, after cloning the main project:

```shell
git submodule init # gitmodule config knows the paths and repo to use
git submodule update
```

### Step 3: Configure Lucee Classpath

Identify Lucee’s classpath directory (e.g., <lucee-install>/lib or a custom path in lucee-web.xml.cfm).
Update Lucee’s configuration to include the submodule’s JARs:
Option 1: Copy JARs to Classpath (simpler for testing):
Copy lib/jars/lib/\_.jar to <lucee-install>/lib.
Example script (deploy-jars.sh):

```
#!/bin/
cp lib/jars/lib/_.jar /path/to/lucee/lib/
```

Run:
`chmod +x deploy-jars.sh && ./deploy-jars.sh.`

#### Option 2: Add Submodule Path to Classpath (more flexible):

Edit lucee-web.xml.cfm or server admin to add `<lucee-project>/lib/jars/lib` to the classpath.
Example (in lucee-web.xml.cfm):

```xml
<lucee-configuration>
    <custom-classpath>/path/to/lucee-project/lib/jars/lib</custom-classpath>
</lucee-configuration>
```

Restart Lucee to load the JARs: `/path/to/lucee/bin/restart.sh`

#### In Application.cfc:

```java
this.javaSettings = {
    loadPaths: [ "../../lib/jars/lib" ], // Adjust based on relative location
    loadColdFusionClassPath: true, // loads default class path for existing JARs app might use by default
    reloadOnChange: true, // useful for development if the path contents change
    watchInterval: 60, // development
    watchExtensions: "jar"
};
```

### Step 4: Verify Integration

Check Lucee admin or logs to confirm JARs are loaded.
Test functionality (e.g., if example.jar provides a CFML tag or function, use it in a .cfm file):

```java
<cfscript>
    // Example: Assuming example.jar adds a custom function
    result = customFunctionFromJar();
    writeOutput(result);
</cfscript>
```

### Step 5: Play with the Submodule

Update JARs in the submodule:

```
cd lib/jars
cp /path/to/new.jar lib/
git add lib/new.jar
git commit -m "Update JARs"
git push origin main
```

Update the submodule in the main project:

```
cd <lucee-project>
git submodule update --remote
git commit -m "Update lucee-jars submodule"
git push origin main
```

Redeploy JARs (run deploy-jars.sh or restart Lucee if using classpath).
Experiment with different JAR versions or roll back:

```
cd lib/jars
git checkout <commit-hash>
cd ../..
git submodule update
git commit -m "Revert to specific JAR version"
```

### Notes

Ensure .gitmodules is committed in lucee-project (created by git submodule add).
Clone with submodules: git clone --recurse-submodules <lucee-project-url>.
Remove submodule (if needed):git submodule deinit -f lib/jars
git rm lib/jars
rm -rf .git/modules/lib/jars
git commit -m "Remove submodule"

Backup lucee-jars repo to avoid losing JARs.

Example Directory Structure

```
lucee-project/
├── lib/
│ └── jars/ # Submodule (lucee-jars repo)
│ └── lib/
│ └── example.jar
├── deploy-jars.sh # Optional script to copy JARs
├── .gitmodules # Tracks submodule
└── index.cfm # Your Lucee app
```

## Misc

### Commands to Check Git Submodules

- `git submodule status`
  Lists submodules, paths, and commit hashes (e.g., lib/jars status).

- `cat .gitmodules`
  Shows submodule paths and URLs (e.g., https://bitbucket.org/mycompany/lucee-jars.git).

- `git config --get-regexp submodule\..\*`
  Lists submodule configurations (URLs, active status).

- `git submodule`
  Summarizes submodule status, similar to `git submodule status`.

- `git submodule init && git submodule update`
  Initializes and updates submodules to populate lib/jars.

## Adding a Submodule to a Deployment Pipeline (ex, BitBucket and CodeDeploy)

- you need to make sure the pipeline fetches the submodule’s content and that the appspec.yml correctly specifies the JARs for deployment. Since submodules are references in the main repository and not stored directly, the pipeline must explicitly initialize and update the submodule to include its files

# Deploying Submodule JARs with Bitbucket Pipelines and AWS CodeDeploy

This guide explains how to ensure JAR files from the `lucee-jars` submodule (in `jarssubmodule/aws_sdk`) are included in your Bitbucket Pipeline and deployed to an EC2 instance via AWS CodeDeploy. Since submodules are references in the main `lucee-project` repository, the pipeline must fetch the submodule’s content to include JARs (e.g., `aws-java-sdk-core-<version>.jar`) in the deployment bundle.

## Key Considerations

- Submodule Handling: The pipeline must run `git submodule init` and `git submodule update` to fetch `jarssubmodule/aws_sdk` content.
- Deployment Bundle: The `deploybitbucket.sh` script must include `jarssubmodule/aws_sdk` in the ZIP file for CodeDeploy.
- CodeDeploy: The `appspec.yml` must specify `jarssubmodule/aws_sdk` and its EC2 destination.
- Classpath: `Application.cfc` uses `this.javaSettings` to load JARs from `jarssubmodule/aws_sdk`.

## Steps

### 1. Update bitbucket-pipelines.yml to Fetch Submodule

Add commands to initialize and update the `lucee-jars` submodule in `bitbucket-pipelines.yml` to ensure JARs are available in the pipeline.

#### Updated bitbucket-pipelines.yml

```yaml
image: amazon/aws-cli:2.15.0

definitions:
  services:
    docker:
      memory: 2048
  caches:
    yum: /var/cache/yum

pipelines:
  branches:
    master:
      - step:
          name: Deploy to EC2 (Master)
          deployment: master
          services:
            - docker
          caches:
            - docker
            - yum
          script:
            - echo "Installing dependencies..."
            - yum install -y zip dos2unix git --setopt=metadata_expire=-1
            - aws --version
            - echo "Initializing and updating git submodule..."
            - git submodule init
            - git submodule update
            - dos2unix ./deploybitbucket.sh
            - chmod +x ./deploybitbucket.sh
            - echo "Deploying to EC2 for master branch..."
            - ./deploybitbucket.sh
            - echo "Bitbucket pipeline finished!"
    aws-codedeploy:
      - step:
          name: Deploy to AWS EC2 (aws-codedeploy branch)
          deployment: aws-codedeploy
          services:
            - docker
          caches:
            - docker
            - yum
          script:
            - echo "Installing dependencies..."
            - yum install -y zip dos2unix git --setopt=metadata_expire=-1
            - aws --version
            - echo "Initializing and updating git submodule..."
            - git submodule init
            - git submodule update
            - dos2unix ./deploybitbucket.sh
            - chmod +x ./deploybitbucket.sh
            - echo "Deploying to EC2 for aws-codedeploy branch..."
            - ./deploybitbucket.sh
            - echo "Bitbucket pipeline finished!"
```

Changes
Git Installation: Added git to yum install for git submodule commands.
Submodule Commands:
git submodule init: Registers the submodule (reads .gitmodules).
git submodule update: Fetches jarssubmodule/aws_sdk JARs.
Order: Run before deploybitbucket.sh to include JARs in the ZIP.
Submodule Authentication
For private lucee-jars:
SSH: Add an SSH key in Bitbucket Pipelines > SSH keys. Use SSH URL in .gitmodules (git@bitbucket.org:mycompany/lucee-jars.git).
HTTPS: Set BITBUCKET_USERNAME and BITBUCKET_APP_PASSWORD as repository variables and add:
yaml

Copy

- git config --global credential.helper '!f() { echo "username=$BITBUCKET_USERNAME"; echo "password=$BITBUCKET_APP_PASSWORD"; }; f'

2. Verify deploybitbucket.sh Includes Submodule Files
   Ensure deploybitbucket.sh zips jarssubmodule/aws_sdk.

Example deploybitbucket.sh
bash

Copy
#!/bin/bash
zip -r artifact.zip Application.cfc index.cfm js views model service handlers jarssubmodule/aws_sdk awstest.cfc scripts
aws s3 cp artifact.zip s3://my-bucket/artifact.zip
aws deploy create-deployment \
 --application-name MyApp \
 --deployment-group-name MyDeploymentGroup \
 --s3-location bucket=my-bucket,key=artifact.zip,bundleType=zip
Verify
Confirm jarssubmodule/aws_sdk is in the zip command.
Check ZIP contents:
bash

Copy
unzip -l artifact.zip | grep jarssubmodule/aws_sdk
Should list jarssubmodule/aws_sdk/aws-java-sdk-core-1.12.782.jar.
Troubleshoot
If missing, verify git submodule update ran successfully. Add debug:
yaml

Copy

- ls -la jarssubmodule/aws_sdk

3. Confirm appspec.yml Deploys JARs
   Your appspec.yml is correct:

yaml

Copy

- source: jarssubmodule/aws_sdk
  destination: /opt/tomcat/webapps/ROOT/jarssubmodule/aws_sdk
  Verify
  Path: Ensure Application.cfc uses:
  cfc

Copy
this.javaSettings = {
loadPaths: [ "./jarssubmodule/aws_sdk" ],
loadColdFusionClassPath: true,
reloadOnChange: true,
watchInterval: 60,
watchExtensions: "jar"
};
Maps to /opt/tomcat/webapps/ROOT/jarssubmodule/aws_sdk on EC2.
Files: SSH to EC2 and check:
bash

Copy
ls /opt/tomcat/webapps/ROOT/jarssubmodule/aws_sdk
Should list aws-java-sdk-core-1.12.782.jar.
Lucee: Test AWS SDK:
cfc

Copy
<cfscript>
awsBase64 = createObject("java", "com.amazonaws.util.Base64");
encoded = awsBase64.encode("test".getBytes());
writeOutput(toBase64(encoded));
</cfscript>
Optional Permissions
If needed, add:
yaml

Copy
permissions:

- object: /opt/tomcat/webapps/ROOT/jarssubmodule/aws_sdk
  mode: '0755'
  owner: 'tomcat'
  group: 'tomcat'

4. Test the Pipeline
   Push: Commit changes to master or aws-codedeploy.
   Logs: Check Bitbucket Pipelines for:
   Successful git submodule init and git submodule update.
   ls jarssubmodule/aws_sdk listing JARs.
   deploybitbucket.sh including jarssubmodule/aws_sdk.
   S3: Verify artifact.zip:
   bash

Copy
aws s3 cp s3://my-bucket/artifact.zip .
unzip -l artifact.zip | grep jarssubmodule/aws_sdk
EC2: Confirm JARs in /opt/tomcat/webapps/ROOT/jarssubmodule/aws_sdk and test AWS SDK. 5. Additional Considerations
Submodule Updates:
bash

Copy
cd jarssubmodule
git pull origin main
cd ..
git add jarssubmodule
git commit -m "Update lucee-jars submodule"
git push origin main
Pipeline fetches new commit via git submodule update.
Caching: Submodule content isn’t cached, ensuring fresh JARs.
Security: Use secured repository variables for AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BITBUCKET_APP_PASSWORD.
CodeDeploy Agent: If not using a pre-baked AMI, add BeforeInstall hook:
yaml

Copy
hooks:
BeforeInstall: - location: scripts/install-codedeploy-agent.sh
timeout: 300
runas: root
Example install-codedeploy-agent.sh:
bash

Copy
#!/bin/bash
yum update -y
yum install -y ruby wget
wget https://aws-codedeploy-<region>.s3.amazonaws.com/latest/install
chmod +x ./install
./install auto
systemctl enable codedeploy-agent
systemctl start codedeploy-agent
Replace <region> with your AWS region (e.g., us-east-1).
