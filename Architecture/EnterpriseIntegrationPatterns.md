# Enterprise Integration Patterns

- Coupling: measure of how many assumptions systems make about each other during communication.
  - Example: RPC (Remote Procedure Calls) - the caller machine assumes function signature on the remote callee system will not change. Communicating with a specific address assumes the address won't change, There is also the assumption that the remote system will be up and operating and network hops will be functional without errors, etc.

## Terms

- Channel: Logical address that multiple systems can agree on without having to identify each other. (it's like an interface or layer in between systems that they can communicate on without having to know IP addresses of each other, for example.)
