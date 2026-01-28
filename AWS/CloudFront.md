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
- IMPORTANT: Cache Invalidation has a cost and is something that should only be used on occasion to correct errors if needed. If you are doing this regularly, you should change to using filenames with version numbers instead: `myfile_v1.jpg`, `myfile_v2.jpg`, etc. If you want to replace a file at the origin, add a NEW object with the _v2 appended. Update your app to point at the new version - this then requires no invalidation to be run in Cloudfront
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
