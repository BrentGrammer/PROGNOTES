# GraphQL

- A **spec** that describes a declarative query language that clients can use to ask an API for exact data they want. Strongly typed schemas and flexibility in how the API resolves data acheives this.

### Main Terms

- Type Definitions: describe the entities that API can expose via queries and mutations
- Resolvers: responsible for fetching the fields on the type definitions
- Schema: combination of type definitions and resolvers
- Data Sources: work with resolvers to fetch data from REST servers, databases etc.
- Queries: Clients use to read data from grphql api
- Mutations: clients use these to mutate data on graphql api

### Tools

- graphql-js: Facebook's graphql impl of the spec - alot of tooling is built on this
- Apollo Server: most recommended server framework for graphql for Node.js
- Express: Apollo Server is build on top of express
- GraphQL Playground: app that usually comes for free to explore the API (acts as a client to test out queries and mutations etc.)
- **Allows the Client to specify what data it wants to query vs. REST APIs where the server determines what data the client gets back**

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

#### Defining Types

- You can define custom types:

```javascript
// server.js

const gql = require("graphql-tag");

const typeDefs = gql`
  type User {
    id: ID!
    name: String!
    email: String!
  }

  type Settings {
    user: User! // adds a relationship to user entities
    theme: String!
  }

// Query is a special type that graphql needs and looks for
// Defines fields that a client is able to interact with to retreive data
  type Query {
    me: User!
    settings(user: ID!): Settings!
  }
  // need input type if you want to pass an object as an argument to a field
  input NewSettingsInput {
    user: ID!
    theme: String!
  }

  type Mutation {
    settings(input: NewSettingsInput): Settings
  }
`;
```

### Resolvers

- Normally start creating resolvers for queries, then mutation, then on field levels, relationships, or special ones for converting or transforming values

```javascript
const resolvers = {
  Query: {
    me() {
      return {
        id: "234234",
        username: "coder1",
        createdAt: 23423433,
      };
    },
  },
};
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
