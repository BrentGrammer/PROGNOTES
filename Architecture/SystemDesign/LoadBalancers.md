# Load Balancers

- distributes load of requests among servers. Helps increase latency and throughput.
- Load Balancers are reverse proxies (act on behalf of the servers)

### Configurations

Can register/deregister servers so the load balancer knows about it.

- Random Redirects: no order, random distribution - could cause problems
- Round Robin: distributes requests equally around servers.
- Weighted Round Robin: place weights on specific servers, follow order of Round Robin, but specify more requests to particular servers. (if a server is more powerful than others for ex. send more there)
- Based on Performance/Load: LB performs health checks on servers to find out how much traffic, how long to respond, resource usage to base how much traffic to send to servers.
- IP Based: useful if you have caching going on in servers, can be helpful to have requests from specific client be redirected to the same server that has their requests cached.
- Path based: distributes requests to servers according to the path of the request. Specific set of servers handles requests for a particular route or routes. Can be useful if you want to make a big change which will not affect other server execution for other features/routes/services if it breaks.

#### Likely to have multiple load balancers in a system.
- can even have multiple load balancers that communicate with each other to keep any one load balancer getting overloaded.

Nginx for example can be used for load balancing.