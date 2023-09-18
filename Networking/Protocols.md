# Protocols

## OSI Model layers:

### Physical Layer

- MAC Address: a physical unique address assigned to hardware devices. Ex: a network card installed in a computer has a MAC address (called Physical Address if looked up with ipconfig on windows)
- Logical Address (i.e. a IP Address): Logical addresses are created and used by network layer protocols, such as IP or
  IPX. The network layer protocol translates logical addresses to MAC addresses. For
  example, if you use IP as the network layer protocol, devices on the network are
  assigned IP addresses, such as 207.120.67.30. Because the IP protocol must use a
  data link layer protocol to send packets to devices, IP must know how to translate
  the IP address of a device to the device’s MAC address.
  - **IP Address**: two parts: network addr and node addr
    - In a typical IP address — say, 192.168.1.102 — the network address is 192.168.1,
      and the device address (called a host address in IP) is 102.

### Routing

- A protocol is considered routable if it uses addresses that include a network part
  and a host part. Any protocol that uses physical addresses isn’t routable because
  physical addresses don’t indicate to which network a device belongs.

### Transport Layer

- where you find two of the most well-known networking pro -
  tocols: TCP (typically paired with IP) and SPX (typically paired with IPX). As its
  name implies, the transport layer is concerned with the transportation of infor-
  mation from one computer to another.
- ensure that packets are transported
  reliably and without errors. The transport layer does this task by establishing
  connections between network devices, acknowledging the receipt of packets, and
  resending packets that aren’t received or are corrupted when they arrive.
- For some applications, speed and efficiency are more important than reliability.
  In such cases, a connectionless protocol can be used. As you can likely guess,
  a connectionless protocol doesn’t go to the trouble of establishing a connection
  before sending a packet: It simply sends the packet. TCP is a connection-oriented
  transport layer protocol. The connectionless protocol that works alongside TCP is
  User Datagram Protocol (UDP).
- You can view information about the status of TCP and UDP connections by run-
  ning the Netstat command from a command window,

### Session layer

- The session layer allows three types of transmission modes:
  » Simplex: Data flows in only one direction.
  » Half-duplex: Data flows in both directions, but only in one direction at a time.
  » Full-duplex: Data flows in both directions at the same time.

### Presentation Layer

- most common representation for representing character data today is called
  UTF-8, which uses 8-bit sets to represent most characters found in western
  alphabets. UTF-8 is compatible with an older standard called ASCII.

### Application layer

- Application programs (such as Microsoft Office or
  QuickBooks) aren’t a part of the application layer. Rather, the application layer
  represents the programming interfaces that application programs use to request
  network services.
  Some of the better-known application layer protocols are
  » Domain Name System (DNS): For resolving Internet domain names
  » File Transfer Protocol (FTP): For file transfers
  » Simple Mail Transfer Protocol (SMTP): For email
  » Server Message Block (SMB): For file sharing in Windows networks
  » Network File System (NFS): For file sharing in Unix networks
  » Telnet: For terminal emulation

## TCP/IP

- a network layer protocol responsible for delivering pack-
  ets to network devices. The IP protocol uses logical IP addresses to refer to indi-
  vidual devices rather than physical (MAC) addresses. Address Resolution Protocol
  (ARP) handles the task of converting IP addresses to MAC addresses.
  - IP addresses consist of a network part and a host part, IP is a routable
    protocol.
  - IP can forward a packet to another network if the host isn’t
    on the current network. After all, the capability to route packets across networks
    is where IP gets its name. An Internet is a just a series of two or more connected
    TCP/IP networks that can be reached by routing.
  - IP is an intentionally unreliable protocol, so it
    doesn’t guarantee delivery of information.
  - IP addresses: Two parts - the network and the host ID. The host ID can’t be 0 (the host ID is all zeros) because that
    address is always reserved to represent the network itself. And the host ID can’t be
    255 (the host ID is all ones) because that host ID is reserved for use as a broadcast
    request that’s intended for all hosts on the network.
  - The IP
    protocol defines five different address classes: A, B, C, D, and E. Each of the first
    three classes, A–C, uses a different size for the network ID and host ID portion of
    the address. Class D is for a special type of address called a multicast address. Class
    E is an experimental address class that isn’t used
    - » Class A: The first bit is zero.
      » Class B: The first bit is one, and the second bit is zero.
      » Class C: The first two bits are both one, and the third bit is zero.
      » Class D: The first three bits are all one, and the fourth bit is zero.
      » Class E: The first four bits are all one.
- TCP ensures that each packet is delivered, if at
  all possible, by establishing a connection with the receiving device and then send-
  ing the packets. If a packet doesn’t arrive, TCP resends the packet. The connection
  is closed only after the packet has been successfully delivered or an unrecoverable
  error condition has occurred
  - One key aspect of TCP is that it’s always used for one-to-one communications. In
    other words, TCP allows a single network device to exchange data with another
    single network device. TCP isn’t used to broadcast messages to multiple network
    recipients. Instead, UDP is used for that purpose.
- User Datagram Protocol (UDP) is a connectionless transport layer protocol used
  when the overhead of a connection isn’t required. After UDP has placed a packet
  on the network (via the IP protocol), it forgets about it. UDP doesn’t guaran-
  tee that the packet arrives at its destination. Most applications that use UDP
  simply wait for any replies expected as a result of packets sent via UDP. If a reply  
  doesn’t arrive within a certain period of time, the application either sends the
  packet again or gives up.
- TCP/IP is not just the pro-
  tocol of the Internet now, but it’s also the protocol on which most LANs are based.

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

  A subnet can be thought of as a range or block of IP addresses that have a com-
  mon network ID.

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
