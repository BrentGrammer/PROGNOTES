# Micro Services

## Resources and Further Reading:

- [Pluralsight course](https://app.pluralsight.com/ilx/video-courses/b4f7ab87-3bff-4f28-847a-3af0a3db2edc/c018ca9a-08ea-4cc9-ac24-d2de738d45dd/78bda0de-683f-447f-94e1-40a2279697c8)

- [eShopOnContainers example application in microservices](https://github.com/dotnet-architecture/eShopOnContainers/tree/dev)

- [Free ebook on .NET Microservices arhitecture](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/)
- [Building Microservices by Sam Newman](https://www.amazon.com/Building-Microservices-Designing-Fine-Grained-Systems/dp/B09RTQY7SX/ref=sr_1_2?crid=LEALOYA87RG6&dib=eyJ2IjoiMSJ9.r-azj9TSEi92CduCOEkPwk5PYG1tLk1WO1V_TlVnfDRQJrNUMGpKOukdQ9xBupb7lA6aDksmnj9WEbB2m70BxAapOTrObMIDlvkbMKikJDSLqI72ApGw43DsvMc-UeSoMsDHYpQpQxX5rzgmwokDm9brdnCptPs9kSPl8K9AOl8QKFvCdpHr20utf00uFvVTqYcKUyJrk3Mo7NCM0jsDPujdotC_09fiTF9iwq58k3GQBnZ46t9mWQPeE-KPE_uP6us9vj0nnd5DOpn8xs2Wyw2zWSIBiLpBW3GqrcCze9I.7R0pA7qi3P4FSCrCdhKuF9txI_gWIs8UCnnlDulGJwo&dib_tag=se&keywords=building+microservices&qid=1710039082&sprefix=building+microservices%2Caps%2C115&sr=8-2)

## Benefits

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

# Security

## Encrypting data (in transit and at rest)

- Sensitive data must be encrypted in transit at a minimum
  - must use industry standard algorithms (do not roll your own)
  - Use TLS (Transport Layer Security) HTTPS
    - Get SSL Certificate issued from Certificate Authorities for each of your services (you need to request this)
    - need a mechanism for updating the SSL Certs and certificate management when they expire. (cloud providers usually have a service for this)
- There may be a requirement from customer to store data encrypted at rest
  - Disks that data is stored on should be encrypted.
  - Need a secure way to manage keys
  - Cloud providers are offering encyrption at rest service for databases and files etc.
  - Remember to encrypt backups as well!

## Authentication

- Requests needs to tell us who the caller is

### Conventional Methods

- Use Authorization header in the request for HTTP requests.
  - i.e. contains username and password ("Basic Authentication")
    - this requires storing passwords (requires care for securely hashing etc.)
  - Could contain an API Key
    - each client of a service has their own API key
    - Requires more secrets to manage and rotate if they are compromised
- Use Client Certificates
  - uses public key cryptography - secure way of caller to prove their identity.
  - also requires complex management

### Use OAuth 2 and OpenID Connect

- Build on Industry standard protocols: OAuth 2.0 and OpenID Connect
- Uses an **Authorization Server**
  - Client authenticates by sending creds to Auth server
  - Auth server returns access token with limited lifetime
  - Access token is used by client (i.e. in Authorization header) with requests to services
  - the tokens are signed using public-key cryptography so its possible to verify that the token was issued by the auth server.
- Advantages:
  - Only one service has the job of identifying users and managing their credentials securely
  - Because industry standard protocols are used you don't have to write this service - you can use third party solutions. (i.e. IdentityServer4 - an OpenID Connect and OAuth 2.0 framework for .NET Core)

### resources for protocols:

- [Getting Started with OAuth 2.0](https://app.pluralsight.com/library/courses/oauth-2-getting-started/table-of-contents)

## Authorization

- What can authenticated users do? Permissions etc.

### The Confused Deputy Problem

- Requests made to downstream services that are forwarded after a user/client request are made with permissions that are too lenient because they are coming from an internal service instead of the user.
  - Example: client > Order service > Payment service -- the payment service would allow the Order service to perform more actions because the permissions are set for the service instead of the client.
  - The risk is if the client uses the request made to the order service, for example, to trick the payment service into making the order with another credit card because the payment service accepts all actions requests coming from the internal order service.
- a solution is to use **"On Behalf of" access tokens**.
  - The upstream service tells the downstream service that the request is being made on behalf of the client, so appropriate permissions and restrictions can be applied by the downstream service

## Network Security

- You can use Virtual Networks to wrap services and protect or close them off from outside traffic.
- Use an API Gateway (Backend for Frontend) pattern to handle traffic coming from the outside world in between the clients and the services.
  - Allows incoming traffic from internet, but also is connected to the Virtual Network protecting the services.
  - Can filter and be selective about which requests to allow through to the Virtual Network.
  - Cloud API Gateways can be configured with a Firewall and come with DDoS and SQL Injection protection
  - For multiple clients that are only authorized for certain users (i.e. an admin UI portal), you can apply IP Whitelisting on the API Gateway

## Defense in Depth

- Do not rely on a single layer of security, but use multiple layers and combinations of techniques.
- Use all techniques described: Encryption, Access Tokens, Network Security
- Penetration testing by a team of InfoSec experts is recommended
- Automated testing to confirm that security features are working correctly
  - run tests that confirm that unauthorized users are unable to call apis and are rejected.
- Attack Detection monitoring for patterns in real-time (can be detected in progress):
  - Port scanning
  - repeated login attempts
  - http requests fishing for sensitive files
  - SQL injection attempts
  - configure alerts when these are detected.
    - Can block the IP of the attacker or shut down service
- Auditing for all actions performed in the system
  - logs should be provided to review who did what and when they did it

# Deploying Micro Services

## Release Pipeline

- Build > Unit Tests > Deploy micro service to a cloud deployed resource/env > Service level integration Tests (service in isolation testing) > Deploy to QA env for e2e tests > Release Gate (manual or risk assessment testing) > Deploy to Prod
  - Very important to use the same procedure you used to push to QA env for pushing to Prod

## Environments

- Development
- QA
- Dedicated to Penetration testing
- Performance Testing environmment
- Prod
  - Could have multiple prod envs per customer or per region

### Parameterize deployment scripts

- JSON or Yaml files are used to express what is different about the environment we are deploying to.
  - i.e. desired state pattern: files describe the state of deployment, i.e. Kubernetes uses this and compares with what the manifests ask for and what is on the actual cluster - if difference k8s will make adjustments until matches desired state
- Often these files are used in conjuction with deployment scripts to allow deployment of specific service to specific env
  - `deploy orderingService 1.0.4 qa.yaml` or `kubectl apply -f qa_config.yaml`
  - deploy this service into the qa environment
  ```yaml
  # qa.yaml
  Name: QA
  Region: us-west-2
  VMSize: Medium
  MinInstances: 2
  MaxInstances: 5
  ```
- Use Terraform or Azure ARM Templates
  - allows to template the cloud infra you need to host the services
  - Usually involve base templates that are overriden with environment specific configuration.

### Artifact Registries

- Build artifacts are stored in a registry
  - Allows easy ability to deploy the latest version or ROLL BACK to a previous stored version quickly
- Using Containers, you can store the images in a container registry
  - Can identify which container you want to deploy
    - example of name and tag with version: `eshopcontainers/orderingservice:1.3.1`

### Deploying strategies

- Blue/Green
  - Run old and new versions of a service simulataneously
  - Use a load balancer to swap traffic from one to the other
  - No downtime while waiting for the new service to start up (no downtime)
- Rolling Upgrade
  - Gradually replace individual instances of older versions with newer versions until all instances are upgraded.
- Kubernetes is designed to host microservices and these strategies are built in
  - Also makes rolling back easy as you just point manifest files to point at the previous tagged version (image) of the service.

## Monitoring Services

- Host Metrics
  - CPU percentage usage
  - Memory usage
  - detect if we need to scale out to meet demand
  - Can setup alerts via cloud providers
- Application Metrics
  - HTTP request failures
  - Alerts for 401 (hacking attempt) or 500 errors (bugs in code)
  - Message Queue alerts for large number of messages backing up (scale out signal)
  - Dead Letter Queue alerts - indicates there is a problem processing messages
- Health Checks
  - web API that can be called to check if services are functioning
    - just report "Ok" to indicate it started successfully
    - information on what downstream deps are accessible
- Logs
  - Each service should emit logs to a centralized place
  - Containers have a standardized approach to capture logs builtin
  - ElasticSearch could be a store for logs and use Kibana to view them
  - Use Azure Application insights, AWS CloudWatch etc.
  - Can use the centralized place for logs to display dashboards and chart metrics

## Distributed Transactions

- Two methods: 2 Phase Commit (or Retry/Cancel) and SAGA

### SAGA vs. 2PC:

- From [SO post](https://stackoverflow.com/questions/48906817/2pc-vs-sagas-distributed-transactions)
- Typically, 2PC is for immediate transactions.
- Typically, Sagas are for long running transactions.
- Use cases are obvious afterwards:
  - 2PC can allow you to commit the whole transaction in a request or so, spanning this request across systems and networks. Assuming each participating system and network follows the protocol, you can commit or rollback the entire transaction seamlessly.
  - Saga allows you split transaction into multiple steps, spanning long periods of times (not necessarily systems and networks).

### Example Use Cases:

- 2PC: Save Customer for every received Invoice request, while both are managed by 2 different systems.
- Sagas: Book a flight itinerary consisting of several connecting flights, while each individual flight is operated by different airlines.

#### Further considerations:

- Saga is a domain modeling (i.e., technology-agnostic) concept, while 2PC is a technology-specific notion with some (maybe many) vendors implementing it. For an analogy, it's the same if we compare the domain events (bare objects) with message brokers (such as RabbitMQ for example).
  2PC can be a good choice if you are anyway married to platforms that implement such a protocol. Not all do, and thus I call this a limitation. I see that people found an argument that Saga is more limiting because it's harder to implement, but that's like saying orange is juicier than apple is sweet. Two different things.
  Consider the human factor too. Some people (developers, architects) are technology geeks. They call business logic or domain model a boilerplate code. another group of people who consider the domain model the most valuable piece of code. Such a preference also affects decisions between Saga and 2PC, as well as who likes what.

- 2PC prefers consistency, while Saga degrades it to "eventual consistency." If you have a situation where consistency is more important than availability (please read CAP), then maybe you do need a system transaction protocol like 2PC. Otherwise, I recommend going with business transactions such as Saga. Please read System Transactions vs Business Transactions e.g. in PEAA.
