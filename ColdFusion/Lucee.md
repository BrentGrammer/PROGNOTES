# Lucee

- open source CFML Engine
- [Good presentations](https://www.carehart.org/presentations/)

### Hot reloading

- With the introduction of [mod_cfml](https://viviotech.github.io/mod_cfml/) for Tomcat these changes in the server.xml configuration file do not have to be made anymore, therefore restarting Tomcat is no longer necessary. The changes will be picked up automatically when the web server sends an unknown host to Tomcat with the corresponding root directory.

### Function reference

- See [Functions](https://docs.lucee.org/reference/functions.html) doc

### Tag reference

- See [Tags](https://docs.lucee.org/reference/tags.html)

## Differences from Adobe ColdFusion

- If you convert a boolean value into a string Lucee generates the following values:
  true into "true"
  false into "false"

### Pass by reference

- In Lucee all arguments are pass by reference including arrays (which in CF are pass by value)

```javascript
function test(arr) {
  arr[1] = "Two";
}
arr = ["One"];
test(arr); // in ACF the passed array is not touched and still contains the value "One" at position 1. In Lucee, the array is mutated.
```

### Use Pass by Value manually if needed (to make a copy of the variable passed)

All CFML arrays in Adobe ColdFusion are passed by values, while in Lucee, they are passed by reference. Please remember this when working with arrays and passing them to functions. There is also the passby=reference|value attribute to function arguments where you can decide whether to pass by reference or value.

If you need Lucee to behave like ACF, you can use the cfargument attribute "passby" in order to pass a copy of the array to the function.

Example:

```javascript
<cffunction name="test">
<cfargument name="x" type="array" passby="value">
```

### Reserved Words

- `variables`
- `url`
- `form`
- `session`
- `application`
- `true`
- `false`
- `null`

### Directory Placeholders/globals

- See [docs](https://docs.lucee.org/guides/developing-with-lucee-server/directory-placeholders.html)

### Incrementing ++/--

- a = b++ would assign the value of b to a, then increment b. a = ++b would increment b, then assign the new value to a. In both cases, b would be incremented. [not thread safe](https://docs.lucee.org/guides/developing-with-lucee-server/operators.html)

### Comparisons

- `EQ` equals Returns true if operands are equal, e.g. "A" EQ "A" is true
- `==` equals Returns true if operands are equal, e.g. "A" == "A" is true
- `===` identical Returns true if operands are the same object in memory, false if they are not, (Note this is different than how JavaScript's === operator works. Lucee 6 === works like javascript, comparing type and value)
  - Caution using this: see https://www.bennadel.com/blog/3775-exploring-the-triple-equals-operator-in-lucee-cfml-5-3-4-77.htm
  - Only checks identity and not type (is this only for Lucee 5?)
- `CONTAINS` contains Returns true if the left operand contains the right operand, e.g. "SMILES" CONTAINS "MILE" is true
- `CT` contains Returns true if the left operand contains the right operand, e.g. "SMILES" CT "MILE" is true
  DOES NOT CONTAIN does not contain Returns true if the left operand does not contain the right operand, e.g. "SMILES" DOES NOT CONTAIN "RHUBARB" is true
- `NCT` does not contain Returns true if the left operand does not contain the right operand, e.g. "SMILES" NCT "RHUBARB" is true
- You can use <> > < >= and <= in tags, as long as they don't interfere with the tag syntax. In that case you must use the equivalent GT, LT, etc. operators instead.

### String Concatenation

- `&` concatenation Joins two strings, e.g. The result of "Hello" & "World" is "HelloWorld"
- `&=` compound concatenation A shorthand operator that joins two strings, e.g. a &= b would be equivalent to writing a = a & b

### Type Casting

Note that in Lucee values are cast to an appropriate type automatically, except when using the identical operators === and !==

For example:

```
<cfset a = "2">
<cfset b = a ^ 2>
```

### Parallelism and Concurrency

- see [Threads](https://docs.lucee.org/categories/thread.html) docs

# Running a Lucee Server

- Note not an installer for Lucee on Mac - use Command Box or alternative

## Command Box

- CLI tool to start a server - can run any version of CF or Lucee
- Commandbox can be used in production (note: but, not with ColdFusion Standard License) to start the server.

## Installing Lucee

- Can install via a script or unattended mode install with variables and settings: see [video](https://www.youtube.com/watch?v=8tnd3RQZy0w) at timesamp 32:44

### Extensions

- [Modular extensions](https://docs.lucee.org/guides/extensions.html)

## Administration

- Can automate configuration of the admin configuration with a server.json file using commandbox (the "app" section)
- Commandbox also has a `cfconfig` tool for this as well.
- Using Lucee's [configuration application.cfc](https://docs.lucee.org/guides/cookbooks/configuration-administrator-cfc.html)
- Get information on the server:

```javascript
// serverdump.cfm
<cfdump var="#server.coldfusion#">
```

### Web Server

- Use `wsconfig` (CF) or `mod_cfml` tool (Lucee) to point web connections to particular versions of the engine if needed.
  - You can also use nginx, apache etc. pointed to the lucee server, or a load balancer which just forwards requests straight to the lucee server.

## Containerization

- Commandbox and Lucee have their own docker images for versions of Lucee/CF.
  - note the environment varialbes for config will be different for each
- hub.docker.com holds lucee images
  - hub.docker.com/u/lucee
    - github.com/lucee/lucee-dockerfiles
  - Adobe: hub.docker.com/u/adobecoldfusion (also on AWS ECR, gallery.ecr.aws/adobe)
    - Need a CF Enterprise licence to deploy images in production from adobe (8 containers)
  - Commandbox: hub.docker.com/u/ortussolutions/commandbox
    - commandbox.ortusbooks.com/deploying-commandbox/docker
- See [comparing docker images for cf](https://cfcasts.com/series/itb-2022/videos/charlie-arehart-comparing-and-contrasting-docker-images-from-ortus-adobe-and-lucee)
- [Another talk on docker](https://www.carehart.org/presentations/#cfdocker_gs)
- [Docker with lucee demo](https://www.youtube.com/watch?v=uDRPTH1xq_8)
- Map a volume to `/srv/www/webapps/ROOT`

### Docker compose example

```yaml
version: "3"

services:
  lucee:
    image: lucee/lucee:latest # or ortussolutions/commandbox:lucee5 etc.
    volumes:
      - ./app:/var/www # map where your cfm etc. files are on your machine to var/www on docker machine
      # source: ./lucee-admin-password/password.txt # password on local machine
      # target: /opt/lucee/server/lucee-server/context/password.txt # copy to password on machine
    ports:
      - "8888:8888"
```

- See [Slides from presentation](./Comparing%20and%20contrasting%20Docker%20images.pdf)
- see [git repo](https://github.com/carehart/awesome-cf-compose/tree/master/cmdbox-lucee-latest) with basic docker compose examples

### Commandbox images offer more flexibility and power if needed

- Commandbox lucee image environment vars:
  - `APP_DIR`: where should server look for code in the container
  - `USER`: what user should the image run as
  - `cfconfig_[engine setting]`: name a cfconfig setting if you want
  - ...many more

### Default directories

- On lucee image, the default app dir is `/var/www`
  - if nothing is copied or mounted there, then by default it will contain index.cfm, Application.cfc, degug.cfm, favicon.ico
  - Need to set datasource and mappings etc. for admin to work.
    - Can copy lucee config files into the container: /opt/lucee/web, /opt/lucee/server/lucee-server/context
  - default port exposed is 8888
  - access the admin: `/lucee/admin/server.cfm` or `/lucee/admin/web.cfm`
  - Will use the password stored at `/opt/lucee/server/lucee-server/context`
- on commandbox lucee image:
  - /app folder is the default app dir
  - index.cfm, commandBoxLogo300.png,403.html are there by default if nothing put in there.
  - Need to set datasource and mappings etc. for admin to work.
    - use cfconfig import, via env vars:
      - BOX_SERVER_CFCONFIGFILE
      - cfconfig\_[engine setting]
  - default port exposed is 8080 and 8443
  - You can expose the admin or not via seting cfconfig env var in this image:
    - access the admin: `/lucee/admin/server.cfm` or `/lucee/admin/web.cfm`
    - for setting the password use the adminPassword property in cfconfig to set it.

## Serverless

- not formally supported
- Pete Freitag created [Fuseless](fuseless.org) for deploying Lucee on AWS Lambda.

## WAR/EAR files

- See [video](https://www.youtube.com/watch?v=8tnd3RQZy0w) at 53:59
- Archive bundles (like zip files) packaging java based apps in a single file.

### Lucee Logs

- Lucee logs are part of a WEB-INF directory which is a expected built-in dir.
- If the WEB-INF directory does not exist you need it - it will have logs folder

```bash
ls /opt/tomcat/webapps/lucee/WEB-INF/lucee/logs/
# exception.log or application.log

# for class loading errors
tail -f /opt/tomcat/logs/catalina.out

# curl the port serving lucee (not the proxy to port 80, but 8080 or 8888 etc.)
curl http://localhost:8080 # should get back dumps or the cfm output from lucee
```

# Adding Classpaths to Lucee

Add JARs to Lucee’s Classpath
Lucee needs to know where these JARs are. You have two options:
Option A: Lucee Admin (Recommended)
Open the Lucee Admin (e.g., http://localhost:8888/lucee/admin/server.cfm).

Go to “Archives & Resources” > “Class Paths” (or “Java Settings” depending on version).

Add the full path to your libs/ folder (e.g., C:\path\to\your-project\libs\).

Restart Lucee (via the admin or server restart) to reload the classpath.

Test your CFML code again.

Option B: JVM Arguments
Locate Lucee’s JVM config file (e.g., lucee.toml or jvm.config in your Lucee installation, often under lib/ or bin/).

Edit the -cp (classpath) argument to include your libs/ folder. Example:

-cp "C:\lucee\lib\*;C:\path\to\your-project\libs\*"

Restart Lucee (e.g., net stop Lucee and net start Lucee in Command Prompt as admin).

### Default directory for JARs:

#### On EC2 Ubuntu 20:

- Use this on EC2 Ubuntu box: `/opt/tomcat/webapps/ROOT/WEB-INF/lib`

#### Other Notes:

- `serverHome/WEB-INF/lib` is where classes go. Look for docker logs that say "Found WEB-INF"
- Server-Level Classpath (Applicable to all web applications):

  - Lucee's lib directory: This is the primary location for .JAR files that you want to be available to all Lucee web contexts. The typical path is:

  - `/opt/lucee/lib/` or sometimes within the Tomcat installation managed by Lucee:
  - `/opt/lucee/tomcat/lib/`

- Web Application-Specific Classpath:

`WEB-INF/lib` within your web application: If you only need the .JAR files for a specific Lucee web application, you can place them in the lib directory within that application's WEB-INF folder. For example, if your web application is in `/var/www/mywebsite`, the path would be:
`/var/www/mywebsite/WEB-INF/lib/`

## Finding missing classes in JARs

- Use jar tf and grep for the missing item:

```bash
jar tf ./libjars/aws-java-sdk-ssm-1.11.273.jar | grep com/amazonaws/services/simplesystemsmanagement/AWSSimpleSystemsManagementClientBuilder
```