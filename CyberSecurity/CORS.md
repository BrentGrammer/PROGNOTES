# CORS

- [Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

### The Origin

- `ORIGIN`: The site that you visit, i.e. "amazon.com"
  - The browser establishes the site you visit as the original origin when you go to it
  - Any requests made from that app/site to other domains require a CORS configuration to allow them to complete

### Same-Orgin Requests

- No security issues or restrictions when the request is to the site you are visiting in the browser (i.e. requests to "amazon.com")
  - Example, a request to get `index.html` might reference a JavaScript file, and so then the JavaScript file (requested and referenced from the index.html file) is on the same domain (the origin), and it is always allowed as a same-origin request

### Cross-Origin Requests

- Requests made to a different domain than the one that your browser visited to load the site
  - i.e. the site fetches images from a S3 bucket on a different domain from the website that served the index.html
- By default, Cross-origin requests are restricted and can be allowed by using a CORS Configuration

### CORS Configurations

- CORS Configurations allow cross-origin requests and are defined on the OTHER ORIGIN (i.e. the domain where the request is being made to)
- The different domains CORS Config will define directives to allow these requests
  - You can define which origins they allow requests from
  - (The original origin always allows requests automatically, the first origin your request goes to, i.e. the website you visit in your browser, etc.)
- CORS Configurations can be defined using JSON, or historically, XML
- **Processed in order and the first matching rule is used**

```json
{
  "AllowedHeaders": ["*"],
  "AllowedMethods": ["PUT","POST","DELETE"], // Allow only PUT POST and DELETE requests to this origin (catagram.io)
  "AllowedOrigins": [ "http://catagram.io" ],
  "ExposeHeaders": []
},
{
  "AllowedHeaders": [],
  "AllowedMethods": ["GET"],
  "AllowedOrigins": ["*"], // Allow all origins making a GET request
  "ExposeHeaders": []
}
```

### Types of Requests that require CORS

- Simple Request - no special setup, just need CORS Config setup on the domain where the request is going to set to allow requests from the original origin
- Preflight or Preflighted Requests: an initial http request is sent to the other origin to determine if the request is safe to send
  - Used for more complicated requests

### Headers sent back from the other origin (Preflight request response):

- `Access-Control-Allow-Origin` - contains `*` for all origins or a particular domain/origin that is allowed to make requests
- `Access-Control-Max-Age`: how long results from a preflight request can be cached (how long you can keep sending requests before you need to do another preflight request)
- `Access-Control-Allow-Methods`: either `*` or a list of http methods that can be used (GET, PUT, etc.)
- `Access-Control-Allow-Headers`: speicifies which headers can be used in requests
