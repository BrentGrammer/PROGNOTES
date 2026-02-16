# AWS CloudFront

- CDN a content delivery network - uses Edge Locations to cache data
- Available globally not by region.
- Improves perf and is cached at the edge to improve user experience
- DDoS protection from distribution globally
  - Note that some users did not have luck with this and just switched to using a VPS with Cloudflare or using cloudflare tunnels and got off of AWS
- integrates with Shield and AWS Web Application Firewall
  - can use AWS WAF web access control lists (web ACLs) to help limit DDoS attacks
- Client makes request to distant server (database) and the response is returned and cached at the edge location closest to them for future calls.
- Can cache from origins such as S3 Buckets or Custom HTTP

Difference between Cloudfront and S3 Cross Region replication
Cloudfront:

- CloudFront has global network
- files are cached in each location for a day (TTL)
- **Great for static content that must be available everywhere**
  S3 Replication:
- Must be setup for each region you want replication - not available everywhere by default
- No caching - files are updated in near real time
- Read only
- **Great for dynamic content that needs to be available in certain regions at low latency (not everywhere and not for static content)**

# Learn Cantrillo CloudFront

- Content Delivery Network

### Distributions

- Distributions are the unit of configuration in Cloudfront

#### Distribution Settings

- Price Class: where your distribution is deployed to (country/region etc)
  - It is slightly cheaper to select "Use Only North America and Europe" vs. more locations or "all locations"
- Associate a AWS WAF firewall.
  - First, create a WAF in AWS and then you can associate it with the CloudFront Distribution
- Can configure an alternate Domain name on the distribution (the default domain is a unique string like `jq7yudijske.cloudfront.net`)
- SSL Type can be configured on the distribution.
  - If using the default domain name, you can use a default AWS certificate
  - If you use a alternate domain name for the distribution, you need to use a custom SSL certificate
    - Custom SSL cert is defined at the distribution level and uses ACM, you pick SNI or non-SNI
  - Select the security policy to use. _NOTE: picking the newest security policy may affect customers with older browsers!_
- HTTP version (2/3)
- Logging on or off

### Behaviors

- See [video](https://learn.cantrill.io/courses/1101194/lectures/27887477)
- Behaviors determine how requests matching a pattern are handled
- A cloudfront distribution can have multiple behaviors
- Behaviors work by pattern matching any requests that come in to that location against a `Path pattern`
  - The path patterns match anything for it that is not matched by a more specific path pattern in another behavior
  - When a path pattern is matched, the request is subject to the options specified in the Behavior (most important: which Origin and origin groups to use)
    - Origin/origin group - Origins can be an S3 Bucket or a custom origin in your application
    - Viewer protocol policy (redirect http to HTTPS, use HTTPS only, etc.)
    - Caching policy - based on headers, legacy or newer versions, min/max/default TTL
    - Restict Viewer Access - requires signed cookies and URLs to access the content. Trusted key groups is the newer way, Trusted signer is legacy.
      - NOTE: some behaviors should be NON-restricted (sign-in, public landing pages, etc). The restricted behaviors are for pages with sensitive content
    - Compress objects automatically
    - Lambda at edge functions can be associated at the behavior level
  - Allowed HTTP methods
  - Field level encryption - encrypt data from the point it enters the edge location through the Cloudfront network
- Distributions always have at least one default Behavior
  - The default behavior matches requests against a wild card `*` path pattern

### TTL and Cache Invalidations

- see [video](https://learn.cantrill.io/courses/1101194/lectures/27887478)
- General rule: the more cache hits (edge location serves an object), the lower the load on the origin storing the objects and better the performance for users. The goal is to minimize Origin Fetches (see below) of edge locations.

- Request made to edge location.
  - resource not cached? Origin Fetch is made to the resource location, the request is forwarded to the origin
  - then the object from the origin is stored in the edge location (cached version)
  - if the resource is cached at the edge location, it is returned in the response immediately
- Expiration:
  - Based on the TTL (Time To Live) period of an object (default is 24 hours on the behavior level config)
  - Edge location objects cached Expire after some time.
    - When the object expires, it is considered "Stale"
    - A request is again made to the origin of the object from the edge location
    - If the version at the edge location matches the origin location, then it is marked back to "Current" and `304 Not Modified` is returned from the origin to the edge location. The object is then returned from the edge location to the client
    - If the origin has a new version of the object, a `200 OK` response is returned with the new object which is then cached at the edge location to replace the stale version

#### Cache Invalidation

- PROBLEM: If an object is changed at the origin, but the edge location still has a cached object that has not expired yet, the client will get the old "current" object from the edge location and not the new object in the origin.
- Cache Invalidations can be run and apply across an entire Cloudfront Distribution
  - NOTE: this takes some time to be applied! It is done for ALL edge locations
- A cache invalidation will immediately expire all objects regardless of their TTL based on a pattern you specify
  - `/images/whiskers1.jpg` - invalidates any objects for this path
  - `/images/whiskers*.jpg` - invalidates any objects in any path that starts with /image/whisers... (/images/whiskers1.jpg, /images/whiskers2.jpg, etc.)
  - `/images/*` - affects any objects in the path, /images/whiskers.jpg, /images/somethingelse.jpg
  - `/*` - every object at every path is invalidated
- IMPORTANT: Cache Invalidation has a cost and is something that should only be used on occasion to correct errors if needed. If you are doing this regularly, you should change to using filenames with version numbers instead: `myfile_v1.jpg`, `myfile_v2.jpg`, etc. If you want to replace a file at the origin, add a NEW object with the \_v2 appended. Update your app to point at the new version - this then requires no invalidation to be run in Cloudfront
  - NOTE: this is not the same as S3 Object versioning - S3 object versions all have the same filename, but the versioning is on the metadata level
  - Using versioned filenames that are separate objects are a better strategy in general for cache management

### TTL

- Default is 24 hours for objects stored on the edge location (defined on the behavior of the distribution)
- TTLs can be set as a minimum, maximum or per object
- Origins can use Headers to control the Object TTL values (custom origins inject these headers via your app or web server, on S3 these are defined on objects using object metadata settings in S3):
  - `Cache-Control max-age`: value in seconds
  - `Cache-Control s-maxage`: value in seconds - directs Cloudfront to apply a TTL in seconds for a particular object, after which the object expires
  - `Expires`: value is a Date and Time - specific time that Cloudfront should use to view an object as expired at.
  - **NOTE**: The Minimum and Maximum TTL specified on the Behavior options in Cloudfront will determine if the values set in the above headers are valid - if they are outside of those limits, Cloudfront will automatically change them to the minimum or maximum value specified on that behavior

## CloudFront Origins

- see [video](https://learn.cantrill.io/courses/1101194/lectures/27887480)
- Origins are where CloudFront goes to get content (when it is not cached at an edge location)
- Origins are selected at the Behavior level

### Origin Groups

- Allow for adding resiliency (in case your origin fails or goes down)
- Two or more origins created within a distribution, you can make a group to group them together which is used by a CloudFront Behavior

### Types of Origins

- **S3 Buckets**
  - Simplest to integrate with CloudFront.
  - Advanced Features:
    - Origin path: specify a nested path in the origin instead of the top level (of the s3 bucket, i.e. use a prefix/folder etc. for where an origin fetch looks)
    - Origin Access - restrict access to the origin so it's only accessible via the CloudFront distribution, recommended new way is using Origin access control
    - Origin Custom Headers - pass through your custom headers to the origin on an origin fetch
  - With s3 origins, the Viewer side protocol and the Origin side protocol are automatically matched and the same (http/https etc)
  - Note if you use S3 as a static store for a website, then it is viewed as a CUSTOM ORIGIN by CloudFront and has different restrictions of features for those
- **AWS Media Package Channel package endpoints**
- **AWS Media Store Container endpoints**
- **CUSTOM ORIGINS: Web Servers (everything else)**
  - see timestamp 6:20 in [video](https://learn.cantrill.io/courses/1101194/lectures/27887480)
  - Much more configuration options: protocol, port settings, ssl version, etc.
  - To secure custom origins, you need to use Custom Headers (instead of origin access control like with S3)
    - Create a custom header in the config that only you are aware of and your custom origin checks for that header to only accept connections from CloudFront

# SSL and Certificates with CloudFront

- [video](https://learn.cantrill.io/courses/1101194/lectures/27887479)
- Cloudfront provides a Default Certificate which uses `*.cloudfront.net` as the certificate name
  - Each CloudFront Distribution comes with a default Domain Name (a CNAME DNS Record) - ex: `dwwwdddw.cloudfront.net`
  - The default certificate covers all of the Cloudfront distributions that use the default DNS name
- To use a custom DNS name, you need to use **Alternate Domain Names**, which are CNAMES you can specify, i.e. `cdn.catagram.com`
  - Use the Alternate Domain Name feature to add custom domain names, make them active and then point the custom name at a CloudFront distribution using a DNS provider like Route53

### Adding an SSL Certificate

- If using https, you need a certificate applied to the Cloudfront Distribution that matches the custom DNS name
- You need a way of verifying that you own and control the domain by adding a SSL certificate that matches the alternate domain name you are adding to the Cloudfront distribution

#### AWS Certificate Manager (ACM) - to get the cert

- Generate or import a certificate using AWS Certificate Manager
- **IMPORTANT NOTE ON CERT CREATION FOR CLOUDFRONT:** ACM is a regional service
  - the certificate NORMALLY must be created in the same region of the resource you are allocating it to
    - Ex: a Load Balancer in us-east-1 must also need a certificate created within ACM in the us-east-1 region.
  - the exception to this rule is for any global service (like CloudFront): _the certificates must always be generated in us-east-1 region!_
- For configuration in Cloudfront you can redirect any http requests to https
  - You can restrict to https only, but that means http requests will fail entirely

## Understanding Certificates

### The Viewer and Origin Protocol

- There are two connections for Cloudfront distributions
  - The Viewer to the Cloudfront edge location (Viewer Protocol)
  - The Cloudfront edge to the Origin (Origin protocol)
    - Origins can be an S3 bucket, Application Load Balancer, or EC2 instance, etc.
- **Both** connections each need PUBLIC valid certificates as well as any intermediate certs in the chain

  #### Viewer Connection Certificates
  - The certs installed in the edge locations must be PUBLIC - self-signed certificates will not work! They must be publicly trusted certs which web browsers know about and trust.
    - Should be from Certificate Authorities such as Comodo, DigiCert, Symantec or AWS Certificate Manager
    - again, the certificate must match the name of the Cloudfront distro (a custom DNS name must point to cloudfront distro, and the certificate needs to match the custom DNS name)

  #### Origin Connection Certificates
  - Also must be publicly trusted certs from major CA Authorities or ACM
  - **For S3 Origins (both viewer connection and origin must have a certificate), S3 handles the certs natively and you don't need to add one** - very simple to use SSL, just point Behavior from your Cloudfront distro at the S3 origin and everything will work.
  - Application Load Balancers origins need a certificate - can use external or use ACM to generate one for you.
  - **For Custom origins like EC2 instances without a ALB**: You CANNOT use ACM to generate certificates and must apply them manually.
  - For origins, the certificate must match the DNS name Cloudfront is using to contact the origins

### How SSL Works

- See timestamp 5:35 in [here](https://learn.cantrill.io/courses/1101194/lectures/27887479)
- Historically every SSL enabled website needed it's own IP adress(before 2003)
- Encryption with SSL happens at the TCP layer, which is much lower level than the HTTP layer (which is application layer protocol)
- It is possible to host multiple many sites using different names on a single webserver with one ip address
  - Servers using http know which site to serve based on Host Headers in the request coming from a browser
  - This reading of the host header happens at Layer 7 after the connection has been established
  - TLS (the encrypted part of https) happens BEFORE this point where the browser sends the server the information about the site it wants to access
- PArt of what TLS does is allow a webserver to validate its identity
  - Before you start an HTTP connection (layer 7), the web server identifies itself
  - in the past there was no way to tell the web server which site the browser is trying to access at this stage, so the server doesn't know which one and could only provide one certificate

#### SNI (Server Name Indication)

- In 2003, an extension was added to TLS called SNI (Server Name Indication) to address this limitation of not being able to host multiple https sites on one webserver
- This allows the client to tell the server which domain name it is attempting to access during the TLS handshake (before HTTP layer gets involved)
  - The server can then provide the certificate for the particular site requested, proving it's identity to the client
- Note: Cloudfront needs to provide separate IP addresses to support older browsers (which don't support SNI)
  - SNI Mode on your distribution is default and free at no cost. In SNI mode, all you need to do is install the certificate
  - **Dedicated IP Mode** is not free and needs to be set to give the edge locations each an IP address, and this will come with a charge - currently $600/month per distribution
