# Rate Limiting

- Setting a threshold on operations past which the operations will return error responses (HTTP code 429 - Too Many Requests).
- Limiting the amount of operations that can be performed in a given amount of time.

- Protects against Denial of Service (DoS) attack to clog databases or overwhelm servers.
- Can rate limit based on user (i.e. headers to see authentication to id the user or something else). For a particular user you can rate limit

  - Can rate limit on IP addr
  - Can rate limit on Region
  - Can rate limit on requests to the system as a whole (no more than 10k requests per minute, etc.)

### DDoS Attacks

- DDoS attacks are more difficult to prevent (Distributed Denial of Service)
  - Tries to circumvent rate limiting by having a bunch of machines abuse service (it is hard to recognize/identify the machines are working together)
- Good approach is to use Cloudflare tunnels to expose my docker apps without opening port 80 and 443. it is faster because you can skip the caddy part and safer because no ports are exposed to the public internet
  - You definitely want to make sure to block all incoming traffic on port 443 and 80 except for cloudflare ips in a firewall like ufw on the backend server. If you dont do that, crawlers will be able to resolve your domain to your backend ip, leaking the ip, bypassing any cloudflare protection.
  - Alternatives are AWS CloudFront with WAF and Shield (Standard), though one user did not have luck with this

### Tracking request info

- To track requests (i.e. for a user for example), you need to use a separate database that all the servers can talk to in order to centralize the information for rate limiting.
  - Use Redis for example or some key value in memory database.

### Tier Based Rate Limiting

- Having multiple tiers of rate limiting is common
  - User can only click button once every 0.5s
  - User can only click button 3 times in 10s (outer time/tier)
  - User can only click button 10 times in one minute (higher tier)

### Rate Limiting in Code

```javascript
const accesses = {}; // this table would normally be on a separate database from servers like a Redis db.

app.get('/index.html', (req,res) => {
    const {user} = req.headers;
    if (user in accesses) {
        const previousAccessTime = accesses[user];

        // limit to 1 request every 5 secs:
        if (Date.now() - previousAccessTime < 5000) {
            res.status(429).send("Too many requests");
            return;
        }
    }

    // serve and store access time
    database.get('index.html', page => {
        accesses[user] = Date.now();
        res.sent(page + '\n');
    }
})
```
