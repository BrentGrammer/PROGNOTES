# Tomcat and Apache Servers

## Tomcat

### Checking Tomcat server configuration

- Tomcat config: `/opt/tomcat/conf/server.xml`
  - Find which directory is mapped to `/` home route:

```bash
cat /opt/tomcat/conf/server.xml | grep -A 5 '<Host'
# This will tell us where Tomcat is expecting to serve your app from.
```

- Tomcat systemd service file: `/etc/systemd/system/tomcat.service`

  - Example:

    ```
    [Unit]
    Description=Apache Tomcat Web Application Container
    After=network.target

    [Service]
    Type=forking
    Environment="JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" # has some env variable information/settings
    ExecStart=/opt/tomcat/bin/startup.sh
    ExecStop=/opt/tomcat/bin/shutdown.sh
    User=ubuntu
    Group=ubuntu
      Restart=always

    [Install]
    WantedBy=multi-user.target
    ```

### Checking Tomcat Status

#### List all services:

```bash
sudo service --status-all

# list service units
systemctl list-units

# check for more services
ls /etc/systemd/system/multi-user.target.wants
```

#### tomcat status

```bash
# check processes
ps -ef | grep tomcat

# catalina process:
pgrep -f 'catalina'

# install net tools
sudo apt install net-tools
# check port tomcat is listening on
netstat -lnp | grep 8080

# hit the server on the ec2 instance locally
curl http://localhost:{tomcatport} # usually 8080 is the port or 80 etc. if apache proxying

```

### Check where tomcat is serving the app from:

- `/opt/tomcat/webapps/ROOT` is the default directory where web apps (index.html etc) are served from.

```bash
 cat /opt/tomcat/conf/server.xml | grep -A 5 '<Host'
 # this should match where you copy your application cfml files to
```

- There is also a welcome file list entry in the tomcat web.xml configuration that should include index.cfm

```xml
 <!-- cat /opt/tomcat/conf/web.xml | grep welcome -->
 
  <!--                       is no welcome file in this directory?  [false] -->
  <!-- for a "welcome file" within that directory and, if present, to the   -->
  <!-- If no welcome files are present, the default servlet either serves a -->
  <!-- If you define welcome files in your own application's web.xml        -->
    <welcome-file-list>
        <welcome-file>index.html</welcome-file>
        <welcome-file>index.htm</welcome-file>
        <welcome-file>index.jsp</welcome-file>
    </welcome-file-list>
```

### BEWARE EDITING IN WINDOWS VIA PUTTY!!!

- Using PuTTy on windows may enter invisible characters that could cause syntax errors if editing config files like /opt/tomcat/conf/web.xml

  - Invisible Character: An empty line shouldn’t break XML, but a hidden byte-order mark (BOM) or non-printable char from editing (e.g., in Nano on Windows via PuTTY) could confuse Tomcat’s XML parser.

- **Lucee runs as a war file in Tomcat:**

```bash
ls /opt/tomcat/webapps/
# should see lucee.war and it's unpacked contents, i.e. a lucee directory
# there should be .cfc files etc. in the lucee directory
```

### Starting and stopping Tomcat

- bin path has a list of scripts you can run

```bash
sh /opt/tomcat/bin/{script_name}.sh

# stopping tomcat:
sudo /opt/tomcat/bin/shutdown.sh
# or main catalina script:
sudo /opt/tomcat/bin/catalina.sh stop


# starting tomcat:
sudo /opt/tomcat/bin/startup.sh
# or main catalina script:
sudo /opt/tomcat/bin/catalina.sh start

```

### Tomcat logs

- generally in `/opt/tomcat/logs/`

```bash
sudo tail -f /opt/tomcat/logs/catalina.out
```

## Apache

### Checking Apache configuration

- Custom Virtual Host Proxy settings and server config: `etc/apache2/sites-available/tomcat.conf`
  - This is where you can set your custom Domain
  - typically used when you're running Tomcat behind Apache. This file is specifically designed to forward incoming requests to Tomcat, using Apache as a reverse proxy.
  - When you're hosting a web app (like Lucee, a Java app) using Tomcat, you would configure Apache here to handle the HTTP requests and forward them to Tomcat running on a different port (e.g., localhost:8080).
- Apache config: `/etc/apache2/apache2.conf`
- Apache Virtual Host: `/etc/apache2/sites-available/000-default.conf`
  - This is the default Apache VirtualHost configuration that applies to all HTTP traffic if no other virtual host is specified. It's typically used for a default site or for general setups.

### Check Apache Logs

```bash
sudo journalctl -u apache2

# Error logs
sudo tail -f /var/log/apache2/error.log
```

## Installing Lucee directly into Tomcat:

```bash
# get the version you want of lucee
wget https://cdn.lucee.org/lucee-5.3.4.80.war

sudo cp lucee-5.3.4.80.war /opt/tomcat/webapps/lucee.war

# start tomcat -will unpack the WAR automatically
/opt/tomcat/bin/startup.sh

# cleanup war file

# The WAR bypasses the installer entirely, relying on Tomcat to deploy Lucee 5.3.4.80.

# OpenJDK and Tomcat  versions must be installed already and compatible with the lucee version.
```

```bash
# install lucee to Tomcat alternative after getting lucee jar and java is installed:
sudo /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java -jar lucee-5.3.4.80.jar --mode unattended --install_dir /opt/lucee --tomcat_dir /opt/tomcat --admin_password yourpassword
```

### Starting Tomcat:

```bash
sudo /opt/tomcat/bin/startup.sh
```
