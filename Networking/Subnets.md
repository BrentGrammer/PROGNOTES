### Subnets

- In a Class C address, the first three octets are used for the network ID, and the
  fourth octet is used for the host ID. With only eight bits for the host ID, each Class
  C network can accommodate only 254 hosts. However, with 24 network ID bits,
  Class C addresses allow for more than 2 million networks.
  The problem with Class C networks is that they’re too small. Although few orga-
  nizations need the tens of thousands of host addresses provided by a Class B
  address, many organizations need more than a few hundred. The large discrep-
  ancy between Class B networks and Class C networks is what led to the develop-
  ment of subnetting, which I describe in the next section.
- Subnetting is a technique that lets network administrators use the 32 bits available
  in an IP address (for the network ID portion) more efficiently by creating networks that aren’t limited to the
  scales provided by Class A, B, and C IP addresses. With subnetting, you can create
  networks with more realistic host limits.

  **A subnet can be thought of as a range or block of IP addresses that have a com-
  mon network ID.**

#### 2 Reasons for Subnetting:

1. more flexible way to designate which portion of an IP
   address represents the network ID and which portion represents the host ID

   - With
     standard IP address classes, only three possible network ID sizes exist: 8 bits for
     Class A, 16 bits for Class B, and 24 bits for Class C. Subnetting lets you select an
     arbitrary number of bits to use for the network ID. any
     network with more than 254 devices (class C) would need a Class B allocation and probably
     waste tens of thousands of IP addresses.

2. The second reason for subnetting is that even if a single organization has thou-
   sands of network devices, operating all those devices with the same network ID
   would slow the network to a crawl. The way TCP/IP works dictates that all the
   computers with the same network ID must be on the same physical network. The
   physical network comprises a single broadcast domain, which means that a single
   network medium must carry all the traffic for the network. For performance rea -
   sons, networks are usually segmented into broadcast domains that are smaller
   than even Class C addresses provide.

#### Subnet Masks

- used to the router must be told which portion of the host ID should
  be used for the subnet network ID
- Those IP address bits that
  represent the network ID are represented by a 1 in the mask, and those bits that
  represent the host ID appear as a 0 in the mask. As a result, a subnet mask always
  has a consecutive string of ones on the left, followed by a string of zeros. (ex: `11111111 11111111 11110000 00000000`)
- To determine the network ID of an IP address, the router must have both the IP
  address and the subnet mask.
- here’s how the network address is extracted from an IP address
  using the 20-bit subnet mask from the previous example. (the network ID for this subnet is 144.28.16.0.)

```
144 . 28 . 16 . 17
IP address: 10010000 00011100 00010000 00010001
Subnet mask: 11111111 11111111 11110000 00000000
Network ID: 10010000 00011100 00010000 00000000
 144  .  28 . 16 . 0
```

- **Note**: Don’t confuse a subnet mask with an IP address. A subnet mask doesn’t represent
  any device or network on the Internet. It’s just a way of indicating which portion
  of an IP address should be used to determine the network ID. (**You can spot a sub-
  net mask right away because the first octet is always 255, and 255 is not a valid
  first octet for any class of IP address.**)

#### Network Prefixing/CIDR (classless interdomain routing)

- Shorthand for indicating how many bits the network ID address part of the IP addr takes up.
  - Ex: the IP address 144.28.16.17 with the subnet mask 255.255.240.0 can be represented as
    `144.28.16.17/20` because the subnet mask 255.255.240.0 has 20 network ID bits.
- The default subnet masks are three subnet masks that correspond to the standard Class
  A, B, and C address assignments. .../8,.../16,.../24

#### Subnet requirements

- The minimum number of network ID bits is eight. As a result, the first octet
  of a subnet mask is always 255.
- The maximum number of network ID bits is 30. You have to leave at least
  two bits for the host ID portion of the address to allow for at least two hosts. If
  you use all 32 bits for the network ID, that leaves no bits for the host
  ID. Obviously, that won’t work. Leaving just one bit for the host ID won’t work,
  either, because a host ID of all ones is reserved for a broadcast address, and
  all zeros refers to the network itself. Thus, if you use 31 bits for the network ID
  and leave only 1 for the host ID, host ID 1 would be used for the broadcast
  address, and host ID 0 would be the network itself, leaving no room for actual
  hosts. That’s why the maximum network ID size is 30 bits.
- A subnet address can’t be all zeros or all ones

NOTE: the subnet mask `255.255.255.255` means that the IP address is a specific destination, not a network.

### Private IP Ranges

- set aside for private TCP/IP networks. Use these ranges

```
CIDR            Subnet Mask     Address Range
10.0.0.0/8      255.0.0.0       10.0.0.1–10.255.255.254
172.16.0.0/12   255.240.0.0     172.16.1.1–172.31.255.254
192.168.0.0/16  255.255.0.0     192.168.0.1–192.168.255.254
```

#### NAT (Network Address Translation)

- Firewalls use a technique to hide actual IP addr of a host from the outside world.
- The host behind the NAT device can use any address it wants, the NAT device translates it into a globally unique addr
- NAT can use a single public IP addr for more than one host. It keeps track of outgoing packets and assigns them to the correct host when incoming.
