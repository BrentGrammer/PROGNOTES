# GraphQL

**Allows the Client to specify what data it wants to query vs. REST APIs where the server determines what data the client gets back**

- Originally created to allow for Mobile/Web clients and their different needs. i.e. mobile clients don't need comments and all other data for a post for example due to limited real estate (they can get that only when clicking a load button, but the web client needed it all with the request)
- GraphQL is [a spec](http://spec.graphql.org/) that needs to be implemented for various languages and envuronments. You need a library or package that implements it.

### Main advantages over REST

- Fast
- Flexible: different clients can query their own way rather than being constrained by the REST APIs available endpoints/functionality
  - GraphQL can be used with SQL or NoSQL databases
- Easy to maintain

### GraphQL Types

- Scalar (hold a discrete single value)
  - String
  - Boolean
  - Int
  - Float
  - ID: use for the PK - usually required: `ID!`
- Non-Scalar (hold collections of discrete values, i.e. object or arrays)
- If you leave off the bang ! for required then it means the value can be nullable.

#### Custom Types

- You can define custom types:

```
type Query {
  me: User!
}

type User {
  id: ID!
  name: String!
  email: String!
}
```

### GraphQL API

- You defined Queries and Resolvers (to handle the queries)

## Apollo

- Used to make graphql queries and handle them
- Two sides: The client and the server
- packages like `graphql-yoga` use Apollo Server under the hood.
  - recommendation is use Graphql-yoga as it's built with apollo-server and express-graphql. And it's built and maintained by the Prisma Team.
- Apollo Boost is the recommended libary for apollo client (to make and handle responses to GraphQL server client side.)
  - typically need `apollo-boost` (to fire gql ops) and `graphql` (to write gql queries in JavaScript) packages on the client
  