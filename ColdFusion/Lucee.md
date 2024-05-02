# Lucee

- open source CFML Engine

### Hot reloading

-With the introduction of [mod_cfml](https://viviotech.github.io/mod_cfml/) for Tomcat these changes in the server.xml configuration file do not have to be made anymore, therefore restarting Tomcat is no longer necessary. The changes will be picked up automatically when the web server sends an unknown host to Tomcat with the corresponding root directory.

### Function reference

- See [Functions](https://docs.lucee.org/reference/functions.html) doc

### Tag reference

- See [Tags](https://docs.lucee.org/reference/tags.html)

## Differences from Adobe ColdFusion

- If you convert a boolean value into a string Lucee generates the following values:
  true into "true"
  false into "false"

### Pass by reference

- In Lucee all arguments are pass by reference including arrays (which in CF are pass by value)

```javascript
function test(arr) {
  arr[1] = "Two";
}
arr = ["One"];
test(arr); // in ACF the passed array is not touched and still contains the value "One" at position 1. In Lucee, the array is mutated.
```

### Use Pass by Value manually if needed (to make a copy of the variable passed)

If you need Lucee to behave like ACF, you can use the cfargument attribute "passby" in order to pass a copy of the array to the function.

Example:

```javascript
<cffunction name="test">
<cfargument name="x" type="array" passby="value">
```

### Reserved Words

- `variables`
- `url`
- `form`
- `session`
- `application`
- `true`
- `false`
- `null`

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

- see [docs](https://docs.lucee.org/guides/developing-with-lucee-server/scope.html)
- Order of scope chain:
  - local
  - queries
  - variables
    - Note - this is in queries scope and can be disabled if needed for performance in query code: This (slow) lookup can be disabled (for better performance) in the Lucee admin or via the Application.cfc setting this.searchResults = false;

### Directory Placeholders/globals

- See [docs](https://docs.lucee.org/guides/developing-with-lucee-server/directory-placeholders.html)

### Incrementing ++/--

- a = b++ would assign the value of b to a, then increment b. a = ++b would increment b, then assign the new value to a. In both cases, b would be incremented. [not thread safe](https://docs.lucee.org/guides/developing-with-lucee-server/operators.html)

### Comparisons

- `EQ` equals Returns true if operands are equal, e.g. "A" EQ "A" is true
- `==` equals Returns true if operands are equal, e.g. "A" == "A" is true
- `===` identical Returns true if operands are the same object in memory, false if they are not, (Note this is different than how JavaScript's === operator works. Lucee 6 === works like javascript, comparing type and value)
- `CONTAINS` contains Returns true if the left operand contains the right operand, e.g. "SMILES" CONTAINS "MILE" is true
- `CT` contains Returns true if the left operand contains the right operand, e.g. "SMILES" CT "MILE" is true
  DOES NOT CONTAIN does not contain Returns true if the left operand does not contain the right operand, e.g. "SMILES" DOES NOT CONTAIN "RHUBARB" is true
- `NCT` does not contain Returns true if the left operand does not contain the right operand, e.g. "SMILES" NCT "RHUBARB" is true
- You can use <> > < >= and <= in tags, as long as they don't interfere with the tag syntax. In that case you must use the equivalent GT, LT, etc. operators instead.

### String Concatenation

- `&` concatenation Joins two strings, e.g. The result of "Hello" & "World" is "HelloWorld"
- `&=` compound concatenation A shorthand operator that joins two strings, e.g. a &= b would be equivalent to writing a = a & b

### Type Casting

Note that in Lucee values are cast to an appropriate type automatically, except when using the identical operators === and !==

For example:

```
<cfset a = "2">
<cfset b = a ^ 2>
```

### Parallelism and Concurrency

- see [Threads](https://docs.lucee.org/categories/thread.html) docs
