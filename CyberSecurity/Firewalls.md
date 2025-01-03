# Firewalls

- See also [Request Response perspectives - Outbound vs. Inbound Connections](../Networking/Protocols.md)

## Stateless Firewalls

- Stateless Firewalls need to take into account 2 rules for each request/response
  - Inbound (request) and Outbound (response)
  - The response rule always uses a random stateless ephemeral port - **need to allow the full range of ephemeral ports to any desination**
  - This makes security questionable and it is better to use STATEFUL firewalls

## Stateful Firewalls

- Can intelligently identify a response for a given request.
  - Links the ports and IP addresses
- You only need one rule instead of two (as with stateless firewalls)
  - You only need to allow or disallow the request (the response will be allowed or disallowed automatically)
- Preferrable to stateless firewall as it reduces overhead and mistakes.
  - Do not need to specify the entire ephemeral port range as the firewall will identify which port for a specific request was used and implicitly allow it on the response to a request that you've allowed.
