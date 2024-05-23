# Database Queries/Datasources

- From [Ortus books](https://modern-cfml.ortusbooks.com/cfml-language/queries)

## Datasource

- see [how to define a Datasource in Lucee](https://docs.lucee.org/guides/cookbooks/datasource-define-datasource.html)

You can define an infinite amount of data sources in your CFML applications in the following locations:

Global ColdFusion Engine (Adobe or Lucee) Administrator

Adobe : http://localhost:port/CFIDE/adminstrator

Lucee: http://localhost:port/lucee/admin/server.cfm

The Application.cfc, which will dictate the data sources for that specific ColdFusion application. (preferred approach as the connections are versioned controlled and more visible than in the admin)

Inline in cfquery or queryexecute calls

The datasource is then used to control the database's connection pool and allow the ColdFusion engine to execute JDBC calls against it.

## Querying with CFML

```java
// Tag syntax
<cfquery name = "qItems" datasource="pantry">
 SELECT QUANTITY, ITEM
 FROM CUPBOARD
 ORDER BY ITEM
</cfquery>

// script syntax

qItems = queryExecute(
 "SELECT QUANTITY, ITEM FROM CUPBOARD ORDER BY ITEM"
);

// Lucee datasource inline definition
queryExecute(
  "SELECT * FROM Employees WHERE empid = ? AND country = ?", // sql
  [ 1, "USA" ], // params
  { // options
    datasource : {
      class : "com.microsoft.sqlserver.jdbc.SQLServerDriver",
      connectionString : "jdbc:sqlserver://#getSystemSetting("DB_CONNECTIONSTRING")#",
      username : getSystemSetting("DB_USER"),
      password : getSystemSetting("DB_PASSWORD")
    }
  }
)
// just like the struct in Application.cfc - could be useful for testing?
```

- If you don't specify the datasource, the default defined in application.cfc will be used:

```java
component{
    this.name = "myApp";

    // Default Datasource Name
    this.datasource = "pantry";

}
```

or more complete with multiple dsns:

```java
component{
    this.datasources = {
        // Adobe Driver Approach
        mysql = {
            database : "mysql",
            host : "localhost",
            port : "3306",
            driver : "MySQL",
            username : "root",
            password : "mysql",
            options : value
        },
        // Adobe url approach
        mysql2 = {
            driver : "mysql",
            url : "jdbc:mysql://localhost:3306/test?useUnicode=true&characterEncoding=UTF-8&useLegacyDatetimeCode=true",
            username : "",
            password : ""
        },
        // Shorthand Lucee Approach
        myLuceeDNS = {
            class : "com.mysql.jdbc.Driver",
            connectionString : "jdbc:mysql://localhost:3306/test?useUnicode=true&characterEncoding=UTF-8&useLegacyDatetimeCode=true",
            username : "",
            password : ""
        },
        // Long Lucee Approach
        myLuceeDNS = {
            type : "mysql",
            database : "mysql",
            host : "localhost",
            port : "3306",
            username : "",
            password : ""
        }
    };
}
```

## CFConfig

- CFConfig allows you to manage almost every setting that shows up in the web administrator, but instead of logging into a web interface, you can manage it from the command line by hand or as part of a scripted server setup.
- see https://modern-cfml.ortusbooks.com/cfml-language/queries#portable-datasources
- see [docs](https://cfconfig.ortusbooks.com/)
- place a .cfconfig.json in the web root of your project, and if you start up a CommandBox server on any CFML engine, CFConfig will transfer the configuration to the engine's innards

## SQL Injection

- Leverage the cfqueryparam construct/tag (https://cfdocs.org/cfqueryparam) and always sanitize your input via the encode functions in CFML.
- The cfqueryparam tag or the inline cfsqltype construct will bind the value to a specific database type to avoid SQL injection

```java
<cfquery name="news">
    SELECT id,title,story
    FROM news
    WHERE id IN (<cfqueryparam value="#url.idList#" cfsqltype="cf_sql_integer" list="true">)
</cfquery>
```

```java
// Named variable holder
// automatic parameterization via inline struct definitions
queryExecute(
 "select quantity, item from cupboard where item_id = :itemID"
 { itemID = { value=arguments.itemID, cfsqltype="numeric" } }
);

// Positional placeholder
queryExecute(
 "select quantity, item from cupboard where item_id = ?"
 [ { value=arguments.itemID, cfsqltype="varchar" } ]
);
```

## Query of Queries

- see https://modern-cfml.ortusbooks.com/cfml-language/queries#query-of-queries
- note that using a query of queries can be quite slow sometimes, not all the time. An alternative approach is to use modern queryFilter() operations to actually filter out the necessary data from a query or querySort(), etc.

## Using Query Builder

- https://qb.ortusbooks.com/

```java
// qb
query = wirebox.getInstance( 'Builder@qb' );
q = query.from( 'posts' )
         .whereNotNull( 'published_at' )
         .whereIn( 'author_id', [5, 10, 27] )
         .get();
```
