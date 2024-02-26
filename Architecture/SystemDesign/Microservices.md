# Micro Services

- Fault tolerant than monoliths
- Reduce dependences between services and keeps application at least partially running

## Database Per Service

- Each service has their own database and does not reach into any other service's database

## Async Communication

- An event Bus or Broker keeps tracks of events emitted by services and publishes them to other services that are listening for them.

### Common library

- A common library can be used and stored in a repo between services to have reusable code, middlewares and event types in one place
