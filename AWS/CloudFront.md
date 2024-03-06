# AWS CloudFront

- CDN a content delivery network - uses Edge Locations to cache data
- Available globally not by region.
- Improves perf and is cached at the edge to improve user experience
- DDoS protection from distribution globally
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
