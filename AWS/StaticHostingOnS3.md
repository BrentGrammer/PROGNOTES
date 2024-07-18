# Hosting Static Site on S3


### Need 2 HTML Files (Index and Error)
- Point the Index page to an object in an S3 bucket
- The Error html file is served when a server side error is encountered (i.e. a page not found etc.)

### Enable static hosting
- Enabling the feature creates a web endpoint for your website 
- The bucket can be accessed via HTTP
- The name of the endpoint is based on the name of the bucket you store your files in and the region it is in. (The name is auto generated based on those things)
  - If you want to use your own domain name you need to name the bucket the same as the domain: the bucket needs to be: `mydomain.org` etc.

## Best Use Cases for static S3 hosting

### Offloading 
- Storing and serving static assets and media (reduces cost and compute service resources)
- Move all your assets to a S3 bucket with static website hosting enabled to offload those resources from your main website (assuming your main site requires a database etc. and is not suitable for S3 static hosting)
- When the HTML file is served from AWS Compute (EC2 etc.), it gets static assets from the s3 bucket and not the Compute service.
  - **This is much cheaper than using the compute service as storage or serving media**
- Also you can offload any large sets of data to S3 for serving (it is built for doing that at scale)

### Out of Band pages
- Useful if server or compute service has errors or is out of service, you can point your DNS to a static site hosted on S3 while those services are down.
- Used as a backup error page if compute services are down.