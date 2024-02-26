# Prisma

- ORM used for MySQL in this project

### Setup

#### Prerequisites

- You need a database installed and setup - MySQL, PostgreSQL etc.
- Remember the root password you enter during setup to use in the connection string with Prisma

- `npm i prisma`
- `npx prisma init`
  - this creates a prisma folder and .env with a connection string (default)
    - [consult docs for url strings](https://www.prisma.io/docs/reference/database-reference/connection-urls) - use this to configure for your database engine
- Go to the prisma/schema.prisma file to configure the provider and url if needed (should be from the .env file)

### Setup models

- go to prisma/schema.prisma to define models
  - can set the name of the field, the type and options like defaults or autoincrementing ids etc.

```prisma
model User {
  id        Int     @id @default(autoincrement())
  email     String  @unique
  name      String
  followers Int     @default(0)
  isActive  Boolean @default(true)
}
```

- Run migrations: `npx prisma migrate dev`

### Migrations

- As schema changes you need to run migrations
- migrations are used to keep the database schema in sync with the prisma schema
- run `npx prisma migrate dev` - for relational
- run `npx prisma db push` - for mongo or nosql dbs
- This will create a migrations folder (you can name the first one "Initial" when prompted)
- Whenever you make a change to the model or schema you need to run a migration and name it something meaningful

- Now you can setup a connection with your Db GUI (Data Grip, DBeaver etc.)

### Create prisma client
- Create a new folder inside prisma folder called client.ts
```javascript
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export default prisma;
// we have access to models defined in the schema: prisma.user.findMany .create etc.
// anytime you run a migration prisma automatically generates a new prisma client so it is always in sync with the models
```
- make sure you only have one instance of prisma in your app. putting it in prisma/client.ts and exporting the instance will ensure that the first time it is imported it will be created and after that the instance is cached and reused.
- In development because of fast refresh you can get an error for too many prisma clients.
  - [need to use best practices for instantiating the client](https://www.prisma.io/docs/guides/other/troubleshooting-orm/help-articles/nextjs-prisma-client-dev-practices)
  - checks if prisma is present in the global space for re-use instead of creating a new client

  