# Scope

- See [overview](https://modern-cfml.ortusbooks.com/cfml-language/variable-scopes)
- default scope is `variables` (i.e. in a cfc or template/cfm files)
- Scopes change with context: i.e. in a CFC, in a function, tag, thread or in a template

### Globals

These scopes persist between requests, i.e. a value can be set during one request then retrieved in a subsequent one:

- `application` Holds elements that relate to the application as a whole.
- `client` Contains elements that persist indefinitely for this particular client (browser).
- `cookie` Refers to the scope of the calling page when a custom tag or module is called
- `server` Used to store data that is accessible from any application on a particular server.
- `session` Holds data pertaining to the user's session.
  cluster

#### NOTE

- Scopes are always invoked first, which means all scope names, e.g. variables, url, form, session, application... are effectively reserved words. Lucee resolves scopes before a variable with the same name, so they can't be referenced/reached.

### Scoping

**Because ColdFusion must search for variables when you do not specify the scope, you can improve performance by specifying the scope for all variables. It can also help you avoid nasty lookups or unexpected results.**

- see [docs](https://docs.lucee.org/guides/developing-with-lucee-server/scope.html)
- Order of scope chain:
  - `local`
  - `queries`
  - `variables`
    - private scope (only seen from the cfc or cfm file)
    - Note - this is in queries scope and can be disabled if needed for performance in query code: This (slow) lookup can be disabled (for better performance) in the Lucee admin or via the Application.cfc setting this.searchResults = false;
- `arguments` - in a function:
```java
function getData( filter ){

    if( isNull( arguments.filter ) ){
      // then do this
    } else {
      // use the filter
    }

}
```