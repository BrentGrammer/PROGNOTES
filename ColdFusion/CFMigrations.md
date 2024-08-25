# Cf Migrations

## Install

- `box install cfmigrations` - application
- CLI: `box install commandbox-migrations`
  - This is more commonly used than cfmigrations - installs commands for use in the command line

## Command Line tools

- commandbox-migrations package
- Commandbox needs to know how to connect to the datasource - this is done with JSON files

### QBMigrationManager

- The tool that helps run the migrations and the default handler class for running migrations
  - Schema builder and Query builder are injected/passed in automatically to instances and can optionally be used.

### Init Migrations

- `migrate init` - generates a file you can use to setup the connection to your database
- `migrate install` - creates a cfmigrations table in your database to keep track of the names of migrations and when they were run
  - This is how cfmigrations knows what has been run so that it does not run the same migrations twice
  - Looks at the `cfmigrations.json` file for where to intall the new cfmigrations table to

```java
// cfmigrations.json
{
    "default": {
        "manager": "cfmigrations.models.QBMigrationManager",
        "migrationsDirectory": "resources/database/migrations/",
        "seedsDirectory": "resources/database/seeds/",
        "properties": {
            "defaultGrammar": "AutoDiscover@qb", // this works fine for MySQL
            // env var syntax, should come from .env file or environment variables set in the server
            // need commandbox-dotenv for .env file reading in local dev
            "schema": "${DB_SCHEMA}", // the schema in mysql is usually the name of the database
            "migrationsTable": "cfmigrations",
            "connectionInfo": {
                "password": "${DB_PASSWORD}",
                "connectionString": "${DB_CONNECTIONSTRING}",
                "class": "${DB_CLASS}", // com.mysql.jdbc.Driver, DRIVER=MySQL
                "username": "${DB_USER}",
                "bundleName": "${DB_BUNDLENAME}",  // lucee needs to know the bundle name and bundle version. bundle name should be "com.mysql.cj"
                "bundleVersion": "${DB_BUNDLEVERSION}"
            }
        }
    },
    // optionally add other database types, postgres, etc.
}
```

### Create a Migration

- `migrate create description_of_migration`
  - This will auto generate a datetime and prepend it to the filename to follow the convention so cfmigrations knows what order to run migrations in and if they've been run already
  - By default migration files are created in `/resources/database/migrations`

### Run Migrations

- `migrate up` - runs all migrations
  - add `--once` option to do one migration at a time (can add to up or down)
- `migrate down` - undo migrations
  - Never run this on prod, only used for development!
  - Helpful to add "If EXISTS" to alot of stuff in the down method for defense to prevent errors.

### Blowing away changes

- `migrate fresh` - only use in LOCAL DEVELOPMENT!
- blows away all migration markers and runs everything from scratch to setup a database/env fresh from start.
- Resets the database and runs all migrations up

- `migrate refresh` - rollback all committed migrations and apply all migrations in order

### Seeders

- Can be used in development environment to seed data
- Should NOT be used in production, only for testing and local dev.
  - If you need to add data to your prod database, do it with a migration (i.e. adding reference data, etc.) - do NOT use a Seeder as they generate random data!
- Seeder is a .cfc component with one method: `run()`

```java
component {
    function run( qb, mockdata ) {
        qb.table("users").insert(
            // mockdata will generate random data, array of rows for you automatically for seeding
            mockdata.mock(
                $num = 25,
                "firstName": "fName", // fName/lname etc. will generate random values
                "lastName": "lName",
                "email": "email",
                "password": "string-secure"
            )
        );
    }
}
```
