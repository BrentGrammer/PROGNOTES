# Micro Services

[Pluralsight course](https://app.pluralsight.com/ilx/video-courses/b4f7ab87-3bff-4f28-847a-3af0a3db2edc/c018ca9a-08ea-4cc9-ac24-d2de738d45dd/78bda0de-683f-447f-94e1-40a2279697c8)

- [eShopOnContainers example application in microservices](https://github.com/dotnet-architecture/eShopOnContainers/tree/dev)

- [Free ebook on .NET Microservices arhitecture](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/)

- Fault tolerant than monoliths
- Reduce dependences between services and keeps application at least partially running

## Database Per Service

- Each service has their own database and does not reach into any other service's database

## Async Communication

- An event Bus or Broker keeps tracks of events emitted by services and publishes them to other services that are listening for them.

### Common library

- A common library can be used and stored in a repo between services to have reusable code, middlewares and event types in one place

# Monolith vs. Microservices

## Monolith

- Single codebase
- Single process (application runs on single process)
- Single host
- Single database
- Consistent tech stack

### Benefits of Monoliths

- Simplicity
- Easy to find things in the codebase
- Deployment involves only one application to update or replace

### NOTE: You do not need to start with Microservices

- You can start with a monolith and allow it to grow to a point where Microservices will be beneficial
- It can be difficult to decide where service boundaries are, by letting the monolith app grow it will become easier to determine what microservices are needed.

### Drawbacks of Monoliths

- Scaling is limited, works well for small applications with moderate user amount
  - Horizontal scaling often not possible (stateless)
  - Vertical scaling is, but expensive
  - Entire app is scaled together instead of individual components
  - Wedded to specific technology stack (reduces updates or adding new tools)
- As app grows larger, harder to maintain with more technical debt
- Modules become more tangled, coupled and dependent
- Deployment is riskier
  - A single line of code changed requires entire app to be redeployed
  - Requires downtime to redeploy

### Note: Services does not equal Microservices

- You can have services, but if they use the same database and are coupled then you are not using microservices architecture
  - **This is a "Distributed Monolith" and is bad** as it's the worst of both worlds of monoliths and challenges of microservices.

## Microservices

### Benefits

- Each service can be owned by a team and is easier to understand and smaller
- Offers flexibility to choose more tools that are right for the specific job of the service.
- Can be deployed individually due to loose coupling
  - Minimizes downtime
  - Possible to keep other services running while one is upgrading or deploying
  - Frequent deployments multiple times a day are possible
- Scaling
  - Scaling independence of each service
- More Agile: can adapt to changing business requirements and can be more reusable

### Drawbacks of Microservices

- Developer productivity
  - Difficult to run the entire system locally
  - More difficult to test in the context of the whole application
- Complex interactions make it difficult to understand the system as a whole
  - Verbose and chatty inefficient communications between services can get out of hand.
- Deployment needs to be automated and can be complicated with many services and deployments to do
- Monitoring and debugging is complicated - requires a good monitoring setup

## Each Microservice has its own data store

- Allows for each microservice to use its own database technology appropriate for the type of data that it needs to store.

### Limitations:

- Cannot do database joins across microservices - need to make separate calls to each db
- Database transactions are not possible
  - Usually design is made to be eventually consistent (takes time for overall state of data to be fully consistent). A business event will cause one data store to be updated, but will be a bit before other data store updates that need to be done for the event complete.
  - or need to use distributed transactions (more complex)

### Mitigation of limitations:

- Define service boundaries well: minimizes need to aggregate data across data stores/services
- Caching: a microservice owns a cache of a subset of data from another microservice. reduces network hops and improves availability (if the other service is unavailable)
- Identify "seams" in the database schema

### Denormalization

- Beware of denormalizing when the same data means different things in different contexts.
  - Example: A Ordering and Catalog Microservice that both have ProductName and Price in each of their databases.
    - The price and name of the product in the order service is that which the product had AT THE TIME of ordering, while the name and price in the catalog service is the current name and price. These are two different pieces of data and should not be normalized!

## Components of a Microservice

- Could be more than one process on one host.
  - An API codebase and database, for example, are two separate processes and on different hosts
  - a cron job or message listener are yet more processes in the same microservice
  - Note that only these components are allowed to access the data for that microservice.
- Public Interface: data for the microservice can only be accessed by other services through the public interface

### Independent Deployability

- **You must never make a breaking change to the public interface of a microservice**
  - You should be able to deploy services without having to upgrade other services
  - Only make **Additive Changes** to the API
    - New Endpoints
    - New fields to DTOs (serializers can be configured to ignore unexpected fields)
  - Versioning new APIs (make sure that support for previous version is still up)
    - Clients will still use the previous version, but over time will be updated to call the latest version.
- **Avoid having to update a service and its clients simultaneously**
  - Keeping separate teams as owners of services helps with this
    - Clients must ask the owners of a service for new feature and wait until it becomes available. Only then can they update their client service.
  - Automated testing of services that ensure that it can call previous supported versions of an API that are part of a CI build process. If they fail you know there is a problem with backwards compatibility.
- Use caution with shared code
  - Need to take care that what you add to the shared code between a service and clients does not result in tight coupling that forces them to be upgraded simultaneously and disallows independent deployability.

## Service Boundaries

- Easier if you are starting from an existing app - some modules might already be broken up suitably to turn into their own services.
- Look for seams in the database schema.
  - groups of tables that conceptually belong together?
  - Look at code that reads and writes from those tables to see if they can be extracted into a microservice
- Organize microservices around Business Capabilities. i.e. Domain Driven Design/Bounded contexts.
  - Microservices do not share models. The same thing can be represented differently in different contexts (i.e. order vs. catalog price and product name which are the same information, but used in different contexts)
- Good practice to sketch boundaries on the whiteboard and run through real world use cases to see which services would be involved.
  - Look out for **too many services** being required to coordinate and work to achieve a single business capability.

### Pitfalls/Design Smells

- Do NOT create services based off of every noun in your system
  - Anemic CRUD microservices which are just thin wrappers around the database that just have logic/methods to add and update entities.
  - The logic related to those entities remains distributed across the rest of the rest of the system.
- Cicular dependencies between services
- Chatty communications where clusters of microservices need to communicate frequently with one another.

## Hosting microservices

- Virtual Machines: Generally comes with too many drawbacks - expensive to have one per service, or all on one machine creates operational challenges
- Platform as a Service (PaaS): comes with scaling, load balancing, security and monitoring - i.e. AWS. Can use serverless for nano services (each service does a tiny simple thing i.e. hosted on cloud functions or lambdas)
- Containers: portable and can run anywhere - locally or in the cloud. good for developing locally using Docker.
  - On windows in docker desktop you might need to enable Settings > General > Use the WSL 2 based engine option.
  - May need to open firewall ports
  - For local development we can use docker-compose and pull 3rd party images for database engines etc. (in production, we would most likely not use these containers, but use cloud hosted databases)
  - [Example Docker-compose](https://github.com/dotnet-architecture/eShopOnContainers/blob/dev/src/docker-compose.yml)

## Testing Microservices

- Service level tests (Integration tests):
  - tests service in isolation
  - Usually involve deploying the microservice to a host and stubbing or mocking out collaborator services.
    - Note that it will use a real database of whatever version/engine the service uses for the data
  - Tests should call the services public API and verify responses from those endpoints.
  - Run as part of an automated build process
- Also include unit and e2e tests (even if just a smoke test that just checks key functionality)

## Standardizing services: Templates and Exemplars

- Goal is to reduce friction of local development etc.
- A service template or service exemplar should be used to help standardize services
- Logging: all services should be emitting logs and sending them to a centralized location
- Health checks
- Auth middleware
- Build scripts (i.e. docker compose or script using setup)

# Service Communication

### Event Bus

- An event bus serves to receive and send messages from/between services.
- Can run RabbitMQ, for example locally for development, or something like Azure Service Bus (or another cloud service) when running in prod in the cloud.

### API Gateway

- A layer between front end clients and services. The clients send requests to the API Gateway which routes those requests to the correct services.
- Allows for implementing Authentication at the API Gateway level
- Makes security easier to reason about if all external traffic enteres the system from a single point.
- Decouples client from the specifics of backend APIs.
  - The gateway serves as a consistent public API which allows microservices to be more flexible.

### Backend for Frontend

- Create an API Gateway for each frontend application
  - For example can turn one incoming HTTP request into two backend calls whose responses are aggregated and transformed to meet the needs of the frontend app.

### Async communication methods

- Can use HTTP for async communication
  - i.e. a request to an ordering service could respond with a 202 "Accepted" response with the resource ID instead of a 200. As further processing and shipping is completed in the future an email could be sent for notifying.
- Web hooks: microservice fires a callback when it's completed its task.
  - Client registers a callback URL where they would like to receive notifications.
- Event Bus: Services send messages to a message broker. Other services subscribe to the messages.
  - decouples services
  - Can store messages in queue so if service goes down when it comes back up, can start consuming missed messages in the queue.
  - Can scale out service instances as the message queue increases in size. Serverless lambdas etc do this automatically, with containers you can configure scaling rules and configuration.
  - Use Command ("SendEmail") and Event message types ("OrderPlaced")

## Handling errors

- Retries with exponential back-offs
  - Example in .NET you can use a library called Polly to implement this easily
  - Be careful about too many retries (could accidentally do a DDoS)
- Circuit Breaker: layer in between the client and server that can close or open to allow or disallow requests.
  - When closed requests can pass through.
  - If errors are detected (errors from server or no responses from the server etc.), it opens which makes requests fail when made from client and enables failing fast rather than passing request to server.
  - After some time has elapsed the circuit breaker closes again to allow requests to see if the downstream service has recovered.
- Caching data can allow service to remain working on other failures if stale data returned is okay.
- Message brokers come with built in retry and will put message into a DLQ after certain number of retries.

## Service Discovery

- Each service has an address, but we need to know what service has what address and where it's located.
- We cannot hard code IP addresses because that would limit our ability to dynamically move services to different hosts in the clusters (necessary as machines need to be taken down for servicing etc.)
- Service Discovery is a central registry that knows where all the services are located.
  - Can work by services reporting their location to the registry when it starts up and sends further checks to let the service regsistry know that it is still available at that address.
- When communicating with a service you ask the service registry where that service can be found.
  - Typically the registry is distributed across all the machines in the cluster (makes it simple to contact the registry)
- Hosting platforms have builtin service registry with DNS
  - When using cloud (PaaS) for hosting, all services will have a allocated DNS name that points to a load balancer in front of your microservice.
    - You just use the DNS layer for communication with the service and don't need to know IP addrs etc.
- Kubernetes or container orchestration services have names for the services and built-in DNS you use for communication with services.
