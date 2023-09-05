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
