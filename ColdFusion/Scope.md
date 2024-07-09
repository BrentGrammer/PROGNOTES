# Scope

- see [video](https://cfcasts.com/series/oop-series/videos/1-7-var-scoping) for scope explanations.

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

### var keyword

- using `var` makes a variable only visible inside a function.
  - using `var` in a function is the same as using `local` to declare the variable - they are both on the local scope
  - You cannot access a variable declared with `var` in a function with `variables.someVar` scope.
- leaving out `var` puts a variable in the `variables` scope which would make it visible in the entire component/file scope.

  - in a function, you should use the `var` keyword always.

  ```java
  function myFunc() {

    // scoped to local, only inside the function. same as `local.someVar = "hey";`
    var someVar = "hey";

    // scoped to variables scope - variables.someVar
    someVar = "hey";

  }
  ```

  ### localmode=modern (Lucee only)

  - If you want to force variables to be local to function scope whether var is used or not, add `localmode="modern"`:

  ```java
  public function someFunc() localmode="modern" {
    // localmode="modern" will auto prepend a `var` keyword to the variable declared here to make it only locally scoped and not visible to the rest of the .cfc file
    someVar = "hey";

    writeOutput(someVar);
  }
  ```
