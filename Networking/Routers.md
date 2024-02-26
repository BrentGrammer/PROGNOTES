# Routers

- Networks that need access to the internet need a router - known as the "Internet Gateway"
- Your router connects your private network to the ISP's network, which then connects to other networks on the internet.
- The Router's Address is known as the "Default Gateway" address.

### VPN (Virtual Private Network)

- routers can connect geographically separate offices to form a single network. A pair of gateway routers can be used to create a secure virtual private network between the two separate locations.
  - the gateway routers connect each network to the internet, and the routers establish a secure tunnel between them.
  - Note that the size of the networks do not matter, a VPN is used to connect separate geographically located networks.

### Router Interfaces

- Routers have two main interfaces:
  - Internal: interface that handles private network connections
  - External: interface that handles the ISP handoff connection for comms with internet/external world
  - NOTE: interfaces can be labeled LAN (internal) or WAN (external) on a lot of gateways.

### Routing Tables

- entries that contain info on the interface, destination and subnet mask for packets sent through the network.
- NOTE: the subnet mask `255.255.255.255` means that the IP address is a specific destination, not a network.
- The network IP address `0.0.0.0` with no subnet mask (also denoted as `0.0.0.0`) means that all packets that aren’t caught by any of the other rules are forwarded out to the indicated target in the table.
  - `0.0.0.0` is a catch all for everything else
  - ex: The subnet mask 0.0.0.0 reduces the entire destination address to 0.0.0.0, which matches the destination network 0.0.0.0. Therefore, the router forwards the packet on to the ISP’s router at 107.0.65.31 via the external interface.
- Entries in the table are evaluated in order and the first match is used.

## Hosts file

- on Mac: in `/etc/hosts`
- on Windows: `C:\Windows\System32\Drivers\etc\hosts`
- You can update entries for local development (for example in a k8s setup to redirect a domain to localhost):
  - `127.0.0.1 mydomain.dev`
  - Going to ticketing.dev in the browser will redirect to localhost
  - Note that if you get a connection is not private locally you can type 'thisisunsafe' to get past it.
