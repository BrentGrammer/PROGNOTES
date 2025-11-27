# Cyber Security Fundamentals

## The Basics

- Never trust any input (SQL injection, XSS, URL Parameters)
- Manage dependencies (via SCA (Software Composition Analysis) and with package managers that keep track and check for known vulnerabilities)
- Firewalls - manage incoming and outbound connections - there should be a "wall" between your application and the public internet which is well defined.
- Secret Leaks - do not hard code or commit any secrets or passwords in Application code.

### SCA (Software Composition Analysis)

- A manifest list of dependencies is checked against a known list of vulnerabilities
- Automated way to check vulnerabilities in dependencies

### The CDE List

- A central database for documenting known vulnerabilities
- Note: other databases are also tracking these and alternative resources should be consulted due to CDE not having all vulnerabilities all the time


## Firewalls

- Layer 7 Firewalls can access, packets, segments, sessions and HTTP and are a good level of firewall to have in place
    - Layer 7 Firewalls understand the HTTP protocol including things like headers, data, hosts, etc.
    - Can identify normal or abnormal elements of a Layer 7 protocol - can identify attacks etc.
    - Can access DNS elements, rates of flow (connections per second), content or headers that lower layers cannot access.
    - Some understand certain protocols: HTTP, SMTP, etc. based on what the firewall software supports
- When a client connects to a server using a Layer 7 Firewall, the HTTPS connection is terminated at the Firewall point. 
  - The HTTPS Tunnel is stripped away, leaving just HTTP which the Firewall can then analyze
  - A NEW HTTPS connection is created between the Firewall and the backend server after analyzation
  - **The Firewall sees an unencrypted HTTP Connection** - i.e. it becomes Plain Text (adhering to the HTTP protocol)
  - The server and client are unaware of this transition and analysis the firewall does
- Data at Layer 7 can be:
  - Inspected
  - Replaced
  - Blocked
  - Tagged
- You can restrict where data goes (do not allow to DropBox, for ex.)