# DNS Domain Naming System

- organizes names in a tree:
  - TOP LEVEL DOMAIN: .com, .edu, .org, .gov etc
  - SUBDOMAIN under TLD: `mywebsite`(.com)
  - NOTE: Subdomains are domains that are one level down in a tree, the .com and .edu for example are actually subdomains of Root, but Top Level Domains relative to 'mywebsite' etc.
- DNS names are case insensitive (you can add cases for readability, but it ignores capital case, all names are lowercase)
- names must contain letters numbers or hyphens (no special chars)
- Constructing a Full Domain: `{host}.{...subDomains}.{topLevelDomain}`

  - You start at the bottom of the tree and move up separated by dots. (similar to a path in a file system, but reversed)

  ### Fully Qualified Domain Names

  - (aka an Absolute domain)Ends with a trailing dot which represents the root domain: `website.com.`
  - Relative Domain names: do not end with a dot and interpreted in the context of some other domain.
  - most of the time relative and absolute domains are the same since relative domains are interpreted in the context of the root domain.

  ### Top Level Domains:

  - appears immediately beneath the root domain.
  - Types:
    - GENERIC: .com, .edu,.gov,.int,.mil,.net,.org etc.
    - GEOGRAPHICAL: i.e. by country, .jp, .uk, .ca etc.

### Hosts file

- originally a text file used to map and track all of the domains on the internet, a precursor to DNS
- Machines can have a hosts file which is always read before DNS so you can override DNS if you want.
- A simple entry is a line that matches an IP address with a host name
- File location:
  - on Windows: c:\windows\system32\drivers\etc
  - on Unix/Linux: /etc/hosts
- Example usage:

```
127.0.0.1 localhost # loopback address pointing the IP to the localhost domain
# {ip addr} {domain name, i.e. google.com etc.} {shorthand alias}
192.168.168.201 server1.LoweWriter.com s1
```

### Zones

- DNS namespace is divided into zones to simplify management of the DNS database (the DNS database is a distributed database)
- Zones usually correspond directly to domains or subdomains
- A Zone delegates responsibility to a particular DNS server.
- Primary and Secondary zones (leader, follower read only setup)

#### DNS Root Servers

- authoritative for the entire internet and they provide the address of the DNS Servers that are responsible for each of the top level domains.
- DNS servers learn ohw to reach the root servers by consulting a root hints file on the server:
  - Linux: `/etc/named.root`
- Entries can be cached with a TTL (time to live in seconds)
