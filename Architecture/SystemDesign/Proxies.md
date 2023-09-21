# Proxies

Proxy: sits between clients and servers.

- Forward Proxy: communicates with server on behalf of the client. The server receives and responds to the forward proxy. The client communicates with the forward proxy.
  - typically the source IP on the request is replaced with the proxy IP addr.
  - VPNs for example use forward proxies that sit between the client and server. (this is how clients may be able to access hidden servers by country etc.)
- Reverse Proxy: act on behalf of a server. When client issues request to server the req is forwarded to the reverse proxy (without client knowing about it, this is configured by the server entity/manager).
  - The DNS would return the IP address of the reverse proxy, not the server, for request/responses to the client.
  - Use Cases in system design:
    - filter out unwanted requests, or add/remove headers before reqs get to the server, etc.
    - Handle logging/metrics
    - use for caching to lift load off server
    - use as a load balancer (for example attacks on server can be mitigated by distributing requests so any one server doesn't get overloaded)
  - You can use tools like nginx to configure reverse proxies
