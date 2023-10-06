# Strategy and Template Pattern

- Good book for designing code to fit design patterns: Refactoring into Patterns by Joshua Kerievsky
- Strategy Pattern uses External Polymorphism
  - The polymorphism is projected through an interface to an entirely separate instance
  - you need to create two objects and figure out how to hook them together somehow (object 1: the high level policy, object 2: the low level implementation)
  - More flexible than Template because you can create the high level policy and low level implementation at different times.
    - you can create the high level policy in one part of the code, create the low level policy in another part of the code, and combine them in yet another part of the code.
    - Reduces coupling. If coupling is a concern, then Strategy pattern is a good choice.
    - You can hot swap strategies - you can change out the strategy even in the middle of a process. But if you use Template method, you're stuck with the instance for the lifetime of that instance. If you want flexibiliy and changeability, use Strategy Pattern.
    - Both low level implementation and high level policy are independent and can be deployed independently
- Template Pattern uses Internal Polymorphism
  - The polymorphism stays within the heirarchy and within the instance
  - There may be two classes but there is only one instance
  - You only need to create one object (create the right instance of the implementation)
  - Good pattern to use if ease of creation of instance is the goal
    - the cost of a few nanoseconds or bytes for ultra performance is valid here. Strategy takes a little longer performance wise
  - Less flexible and more tightly coupled than Strategy pattern.
    - the inheritance coupling is too strong to span a architecturally significant boundary

## Strategy Pattern

- The purpose of the pattern is to separate a high level policy from a set of low level details
- A level policy delegates through a strategy (interface) to accomplish some goal or operation passing the impl to derivatives.
  - the high level policy does not care about the details of what it delegates to

### Example with FTP

- An FTP class sends packets over the network:

```java
FTP implements IPacketProtocol
  +sendFile()

IPacketProtocol
  +sendPacket()

// implement the interface with derivatives
XModemPacketProtocol
YModemPacketProtocol
HDLCPacketProtocol
X25PacketProtocol
```

## Template Method Pattern

- solves the same problem the Strategy pattern does, but uses a different mechanism
- The low level implementations derive from the class that contains the high level policy
- The high level class is an abstract class
  - the high level class calls it's own method which allows for creating derivatives of the high level (abstract) class

### Example with FTP

```java
abstract class FTP
  +sendFile()
  +sendPacket

// now you can create derivatives of the abstract class
XModeemFTP
YModemFTP
HCDCFTP
X25FTP
```
