# Common Commands

### ARP (Address Resolution Protocol)

- list mac addrs to IP addr map: `arp -a`
- list for an IP: `arp -a {ip-addr}`
- ARP is sometimes useful when diagnosing duplicate IP assignment problems.

### hostname command

- list the machine's hostname: `hostname`
- on linux you can set parameters to set the hostname of the machine

### ipconfig

- displays information about a computer’s TCP/IP con-
  figuration. It can also be used to update DHCP and Domain Name Server (DNS) settings.
- easy way to determine a computer's ip address
- list config info: `ipconfig`
- list detailed info: `ipconfig /all`
  - can see default gateway ip (router), and DNS server IP addrs for example with this.
- to renew a IP lease (if DHCP is on only): `ipconfig /renew`
- release a lease: `ipconfig /release` (you can renew after this if needed.)
- flush the DNS cache: `ipconfig /flushdns`
  - shouldn't have to do this unless you've played around with DNS network settings or machines have a problem looking up entries. Forces the machine to reacquire fresh DNS entry mappings.

### netstat

- Useful if having http or file protocol problems. Displays connections
- display all connections: `netstat`
  - indicates the local
    port used by the connection, as well as the IP address and port number for the
    remote computer
- display connections with origin program info: `netstat -b`
  - useful for seeing what program established the connection
- display local and foreign IP addresses for the connections: `netstat -n`
- more verbose info: `netstat -a`
- protocol statistics: `netstat -e`
  - Check Discards and Errors. These numbers should be zero, or at least close to it. If not, the network may be carrying too much traffic or the connection may have a physical problem.
- more statistics: `netstat -s`

### nslookup

- useful for diagnosing DNS problems. You
  know  you’re experiencing a DNS problem when you can access a resource by
  specifying its IP address but not its DNS name.
- `nslookup google.com`
