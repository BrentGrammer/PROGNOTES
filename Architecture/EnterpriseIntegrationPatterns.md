# Enterprise Integration Patterns (Messaging)

- Coupling: measure of how many assumptions systems make about each other during communication.
  - Example: RPC (Remote Procedure Calls) - the caller machine assumes function signature on the remote callee system will not change. Communicating with a specific address assumes the address won't change, There is also the assumption that the remote system will be up and operating and network hops will be functional without errors, etc.

## Terms

- Channel: Logical address that multiple systems can agree on without having to identify each other. (it's like an interface or layer in between systems that they can communicate on without having to know IP addresses of each other, for example.)

### Four main ways to integrate applications:

- File Transfer
- Shared Database
- Remote Procedure Invocation
- Messaging

## Messaging

- Asynchronous communication (similar to voice mail) that allows consumer to read from a queue of messages after they've been sent to a common channel.
- Messages typically have a header and a body. The header is meta info (destination and origin etc.) and the body has the data that the application consumer uses.

### Messaging System

- A messaging system is needed to manage sending messages reliably between computers.
- Similar to a database used for persisting data - requires defining a schema

### Transmission of a Message

1. Create
1. Send - message is added to a channel
1. Deliver - messaging system moves the message to the receiving computer, making it available to the reciever
1. Receive
1. Process - data extraction by the reciever

### Two principles of messaging:

- Send and Forget: sending a message to a channel means that the sender can move on to other work while the messaging system transmits in the background. The sender can be confident the message will make it to the reciever without waiting for confirmation.
- Store and Forward: When a message is sent to a channel, the messaging system stores the message on the sender's computer (disk or in memory, this is step 2 above). In step 3 (Deliver), the messaging system stores the message on the reciever's computer. This store and forward process can be repeated until the message makes it to it's final destination.

The reason to use this system is to make the message atomic and delegate delivery to the messaging system. This ensures that delivery can be retried and that only one copy of the data is received by the reciever.
