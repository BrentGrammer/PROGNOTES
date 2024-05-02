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
- In total, there are 13 main DNS root servers, each of which is named with the letters 'A' to 'M'. They all have a IPv4 address and most have an IPv6 address.

### Types of Records:

- **SOA**: Start of Authority Identifies a zone
- **NS**: Name Server Identifies a name server that is authoritative for the zone
- **A**: Address Records - Maps a fully qualified domain name (Host) to an IP address. Ex: `www IN A 192.168.168.201` Note the host name is not fully qualified. DNS will provide the fully qualified name with the zone (which is usually indicated by the domain) added.
- **CNAME**: Canonical Name Creates an alias for a fully qualified domain name
  - The owner field in the CNAME record provides the name of
    the alias that you want to create. Then, the RDATA field provides the Canonical
    Name — that is, the real name of the host.
  - Ex: `files.lowewriter.com. IN CNAME www1.lowewriter.com.`
    - Note that IN represents Internet Protocol
- **MX**: Mail Exchange Identifies the mail server for a domain.
  - Mail Exchange (MX) records identify the mail server for a domain. The owner field
    provides the domain name that users address mail to. The RDATA section of the
    record has two fields. The first is a priority number used to determine which mail
    servers to use when several are available. The second is the fully qualified domain
    name of the mail server itself.
  - Ex: `lowewriter.com. IN MX 0 mail1.lowewriter.com.
lowewriter.com. IN MX 10 mail2.lowewriter.com.`
  - The server name specified in the RDATA section should be an actual host name,
    not an alias created by a CNAME record. Although some mail servers can handle
    MX records that point to CNAMEs, not all can. As a result, you shouldn’t specify
    an alias in an MX record.
    Be sure to create a reverse lookup record (PTR, described in the next section) for
    your mail servers. Some mail servers won’t accept mail from a server that doesn’t
    have valid reverse lookup entries.
- **PTR**: Pointer Maps an IP address to a fully qualified domain name for reverse lookups. Usually appear in special reverse lookup zones.
  - Ex: `102.129.71.64.in-addr.arpa. IN PTR www.lowewriter.com.`

### Reverse Lookups

- returns the fully qualified domain name for an IP Address (the opposite of a forward lookup)
- Reverse lookups are possible because of a special domain called the in-addr.arpa
  domain, which provides a separate fully qualified domain name for every possible
  IP address on the Internet. To enable a reverse lookup for a particular IP address,
  all you have to do is create a PTR record in a reverse lookup zone (a zone that is
  authoritative for a portion of the in-addr.arpa domain). The PTR record maps
  the in-addr.arpa domain name for the address to the host’s actual domain name.
