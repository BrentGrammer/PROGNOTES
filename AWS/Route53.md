# Route 53

- Managed DNS (i.e. like "DNS as a Service")
- Global service with a single database (no need to pick a region)
- Globally resilient and automatically replicated between regions

## Costs

- Domains range from $14/year and up (.io is the most expensive)
- There is a small monthly cost for every hosted zone created
  - Every domain that you have and register will need one hosted zone

## **Routing Policies**:

- Simple Routing Policy: simple routing has no health checks, simple call with a url string to get the ip address, for example (NOTE: all other policies have health checks)
- Weighted Routing Policy: set weights for different EC2 instances (like load balances) - set percentages. distributes traffic
- Latency Routing Policy: Sends back which server is closest to the user to minimize latency - used for users who are dispersed geographically
- Failover Routing Policy: Have a primary and failover instance - Route53 does a health check on the primary EC2 instance and if bad, reroutes to the failover instance
- Example:
  - A record created to tie a web url string to a IP address
  - Client gets response from Route53 with the IP Addr and uses it to make a call to the server using it.
- Cost: about 12 dollars a year for domain and 0.50 per month for hosted zone
- can use Route53 geolocation routing policy to to block certain geographies.

## Uses

### Register Domains

- Has relationship with all the major domain registries (companies that manage top level domains i.e.
  .com, .io, .net etc.)
  - These companies have been delegated this ability by IANA who manage the root zone for DNS. .org is managed by an organization called PIR (Public Interest Registry) for example, or .com is managed by Verisign.
  - Each tld represents a zone: a .com zone, a .net zone and so on

### Domain Registration Steps (Hosted Zones/Name servers)

- [Walkthrough video of creating a Route53 domain](https://learn.cantrill.io/courses/1101194/lectures/25301533)
- Steps when a domain is registered:
  - R53 checks the registry for the desired top level domain to see if the domain is available
  - R53 creates a Zone file for the domain being registered
    - A **Zone File** is a database that contains all the information for a particular domain (i.e. `mydomain.org`)
    - In Route53 terms this Zone file is known as a **Hosted Zone** (they are zone files that are hosted on R53 created name servers)
  - R53 creates name servers for this zone
    - it creates a number of name servers per hosted zone: generally 4 name servers to host this hosted zone and they are distributed and managed globally by Route53.
    - R53 places the Zone file (Hosted Zone) onto the created name servers
  - R53 does not register the domain, but communicates with the tld company (PIR for .org for example) and adds **name server records** (referencing the name servers just created) into the external third party zone file for the top level domain.
    - By adding the NS records to the tld zone, they establish that our name servers (created by R53) are authoritative for the domain in their registry and point back at our name servers.
    - Side note: DNS is a system of delegation (the third party company delegates to our name servers via the ns records)
    - The name servers listed in the `Registered Domain` section of the Route53 AWS Console service are the ones that are registered with the third party top level domain manager. The name servers listed in the `Hosted Zone` section in AWS console are the ones currently created for you by Route53 - these should match and need to be updated if you delete/recreate the hosted zone for example!

### Hosted Zones

- Can think of a Hosted Zone (DNS Zone) as a database where you store your dns records and contain your name servers
- Hosted Zones can be public (The name servers are listed in the AWS public zone - accessible via public internet)
  - Public zones house public services which anyone can connect to but permissions are required IAM etc.
- Private Hosted Zones can be linked to VPCs
  - Use these to host sensitive DNS records that you don't want publically accessible
- Hold DNS records (aka record sets)

### Note: Deleting/Re-creating a Hosted Zone

- If you delete a hosted zone and create another, then a new set of name servers will be created for the new hosted zone
- To prevent DNS issues, the name servers in the `Hosted Zone` section of Route53 AWS console need to match the name servers in the `Registered Domain` section, so you need to copy the Name servers in `Hosted Zone` to the `Registered Domain` section so they match and are updated.

### AWS Console:

- Search services for Route53
- Two main sections that you'll use (on the left side menu) are:
  - `Hosted Zones`
  - `Registered Domains`
    - Transfer Lock: a security feature that ensures the domain cannot be transferred away from Route53 without you disabling this lock.
    - `Requests` underneath this will show you the status of your registered domains

# DNS Record Types

- [video](https://learn.cantrill.io/courses/1101194/lectures/25301534)

### NS Records

- Name Server Records that allow delegation to occur in DNS
- These are registered in the tld company register (for .com, .org etc.) and point to name servers managed by other companies or teams
  - Ex: a .org ns record delegates control to the .org registry
- Inside the zone for the company that registered the name servers (i.e. your company) there are DNS records such as `www` which is how you can access those records as part of DNS

### A Records and AAAA Records

- These records do the same thing: Map host names to IP addresses
- The difference between them is the type of IP address they map to:
  - An A record for a given host (i.e. `www`) maps to an IPv4 Address (if you type `www.mydomain.com`)
  - An AAAA record maps the host to an IPv6 address
- As a DNS Admin you will create two records (A and AAAA) with the same host name
  - The DNS software on a client will choose the correct IP address type that it wants (AAAA if it's capable of using IPv6 or the A record if it's not and needs to use IPv4)

### CNAME record (Canonical Name)

- Allows you to create DNS shortcuts for a given hosted zone
- Maps a host to another host
- Example:
  - `A server` record (points to an IP for a server that handles ftp, mail and web services)
  - `CNAME ftp`/`CNAME mail`/`CNAME www` point to the A record `server`
    - All 3 CNAMEs will resolve to the same IP Address
      - `www.mydomain.com`, `ftp.mydomain.com` and `mail.mydomain.com` will all point to the same ip address
- Creating CNAME records can reduce overhead if an IP address changes.
  - i.e. if you need different addresses for the same server, you only have to update the A record and the CNAMEs are pointing to it, so they automatically point to the updated IP.
- **CNAME Records cannot point to IP addresses only to other host names** - this is a trick question on the exam.

### MX Record

- Important for how email works on the internet - inidicates how a server can find the mail server for a specific domain.
- An email server needs to know which server to pass an email on to
- MX Records have two main parts:
  - Priority: Numbers that determine which MX record is used for a given MX query (see below).
    - Lower numbers indicate higher priority (higher priority record will likely be the mail server inside the zone of that domain so it tells a server to send the email there.)
    - If a higher priority record is not available or does not work, then the lower priority one is used and selected in an MX query
    - The MX Query uses this one to connect to a mail server via SMTP etc.
  - Value:
    - can be a host (i.e. `mail`) if it has no dot on the right (`mail.something.etc`), then it is assumed to be part of the zone (`mail.mydomain.com`)
      - Ex: `MX 10 mail`
    - if there is a dot `.` to the right then it is a fully qualified domain name. ex: `mail.other.domain.com` - this points outside of your zone
- When an email is sent the `@gmail.com` part will be looked at and an MX query made to that server domain via DNS (root > tld(.com) > gmail...) to retreive MX records from that server
- Example:
  - In our zone we have an A record named `mail` (the name could be anything technically) pointing to an IPv4 address.
  - MX 10 mail - MX record pointing to our hosted zone mail server
  - MX 20 mail.other.domain.com - MX record pointing to some other mail server we use as a backup etc. that might be outside of our zone. higher number indicates lower priority - so use MX 10 mail if available over this one.

### TXT Record (Text)

- Allow you to add arbitrary text to a domain
- Common use case is to **prove domain ownership**
- Could be asked by a third party to add a txt record to our domain containing a specific piece of text data (a random string)
- The third party (for example imagine using Google for email services on your domain) will query for that text record and confirm that the random text matches what they asked you to add.
- Can also be used to fight spam (can add certain info to a domain indicating which entities are authorized to send mail on your behalf)

## DNS TTL (Time To Live)

- Numeric value in seconds that can be set on DNS records to indicate how long the records can be cached for.
  - Ex: TTL 3600 - 3,600 seconds which is one hour
- Will indicate how long the authoritative answer response for a query to DNS is stored in the DNS Resolver
  - A cached response is a **Non-Authoritative Answer**
- The resolver server is probably hosted on your internet provider, so responses will be much quicker than it would be if the DNS system had to resolve all the levels down the tree for a request (to www.amazon.com for example)

### Authoritative Answer

- Getting the source IP address after the DNS service (on the internet) finds the lowest level domain via the Resolver for a requested host (i.e. www.amazon.com) FROM the nameserver for the host
- We get an authoritative answer by talking to a nameserver that is authoritative for a given domain (i.e. by requesting the `www` record from a nameserver for the host we want the address for)
- Getting the authoritative answer from a nameserver for a host is preferred and is considered the single source of truth.
- Non-authoritative answers are the responses for the IP address from the name server that are cached in the DNS Resolver.

### Caching tradeoffs

- Normally DNS settings don't change, so non-authoritative and authoritative answers are identical most of the time.
- You can either keep TTL values low to take effect better when changes are made, or you can temporarily change them to a low value when making a change.
- NOTE: It is not gauranteed that the resolver will honor your TTL settings - that can be changed locally by the admin for the resolver server itself.
- CAUTION: DNS can cause project failures because of TTL values.
  - If you are doing any changes to DNS values, you need to lower the TTL values way in advance of the planned changes (up to days or weeks in advance even). This will reduce caching issues when you change the records.

# Hosted Zones

- Two zones: Public and Private

### Hosted Zone

- HOSTED ZONE: A DNS Database for a section of the Global DNS Database
  - For a domain, such as `mysite.com`
  - Globally RESILIENT: regions can be down, but Route53 still functions
  - Databases which are referenced via delegation using Name Server Records

### Public Hosted Zone

- A Zone file which is hosted by Route53 on public name servers (accessible from the public internet and from within VPCs using the Route53 Resolver)
- Hosted Zones are created automatically when you register a domain with Route53
- Monthly fee for each hosted Zone and fee for queries made against the hosted zone
- Hosted Zones host DNS Records (A records, MX records, S records etc.)
  - These are also referred to as Resource Records
- Hosted Zones are authoritative for a domain
  - When you register a domain, name server records for that domain are entered into the top level domain zone (these point at your name servers, then the name servers and the domain which they host become authoritative for that domain)
- When a hosted zone is created, 4 public name servers are allocated by Route53
  - The Zone file (database) is hosted on these servers
  - To integrate it with the public DNS system, you change the name server records for that domain to point at those 4 R53 name servers
  - R53 can be used to host Zone files for externally registered domains (from GoDaddy, etc.) - you would add the name servers from route53 to the DNS system for the host you bought the domain for externally.
- Instances in a VPC can query the Hosted Zone just as any public DNS zone can query it, using the Route53 Resolver

### DNS

- ISP Resolver Server > Root servers > TLD Servers (.org, .com, etc.) > Route53 Name servers for the hosted zone

### Private Hosted Zone

- Instead of being public, it is associated with VPCs within AWS - ONLY accessible within the VPC it is associated with
- NOT accessible from the public internet
- For accessing a private hosted zone, a service needs to be running inside a VPC that is associated with a private hosted zone

### Split Horizon

- Can have some records accessbile in the public zone and some inaccessible in a private zone behind the same domain.
- Common use case with using the same domain but controlling what is accessed or pointed to depending on if access is from public internet or inside a business network/vpc

### ALIAS RECORDS: CNAME vs. Route53 Alias Records

- A CNAME maps a name to another name: ex - `www.mysite.com` points to `mysite.com`
  - Basically it's an alternative name for something in DNS
- DNS standard does NOT support making a CNAME for the Domain APEX (a.k.a. "naked domain") DNS record (the main record, i.e. `mysite.com` cannot point to something else)
  - This is a problem because Elastic Load Balancers, for example, don't give an IP address to map to, but a DNS name.
  - Pointing an Apex domain name at an Elastic Load Balancer DOES NOT work!
- ALIAS RECORD: maps a name onto an AWS Resource
  - These must be used to point APEX domain/naked domains to an AWS Resource (i.e. an ELB)
  - An Alias is a subtype - you can have an A Record ALIAS and a CNAME Record ALIAS
    - Example: For a Load Balancer you have an A Record for it that points to an IP Address
    - To point to the Load Balancer, you need an A Record ALIAS in that case to point at the DNS name provided by the load balancer (You have to use the same Record type, A or CNAME etc., as the AWS resource provides, in this case an A record from the ELB)
    - ALIASES are commonly used when pointing at resources such as the API Gateway, CloudFront, Elastic Beanstalk, S3 Buckets, etc.
  - Use Aliases especially when you want to point to an AWS resource


### Simple Routing

- Each record can have multiple values (i.e for A Record, multiple IP addresses)
- The values are returned in the same query in a random order
- The client chooses one of the values to resolve to and connects to the server based on that value chosen
- Used when routing requests to one single service (i.e. a Web Server)
- LIMITATION: DOES NOT SUPPORT HEALTH CHECKS!
