# Variables

- CFML is a case-insensitive language as well. Meaning if you create a variable a and reference it as A they are the same.
- Reserved keywords (scopes) you can't use: The name of any of the internal ColdFusion engine scopes:
  - `form`, `session`, `cgi`, `client`, `url`, `application`, `function`
  - Technically you can create the variable by long scoping (local.form), but it is confusing and error-prone.
  - see [list of reserved words](https://modern-cfml.ortusbooks.com/cfml-language/variables)
- [cfparam paraming variables to set default value for variables](https://modern-cfml.ortusbooks.com/cfml-language/variables#paraming-variables)
- Get type info on a variable:

```javascript
qData = getMetadata(query);
a = now();
writedump(a.getMetadata());
```

### String Interpolation:

```javascript
a = "Hola Luis";
writeoutput("Welcome to CFML: #a#"); // use #
// Echo is the same as writeOutput but LUCEE only
echo("Welcometo CFML: #a#");
```

### Always scope variables
- Scope variables, otherwise they will be placed automatically and CFML will search a large number of scopes for them (could cause collisions, memory leaks or unexpected values to be found if the variable is defined elsewhere up the scope)
  - use `var` or `local.{var}` in functions etc. to assign or reference them.

### Logging out variables for debugging

- CFML offers one of the most used functions/tags ever: `<cfdump>`, writeDump() and `<cfabort>`, abort;. These are used to dump the entire contents of a variable to the browser, console, or even a file. You can then leverage the abort construct to abort the request and see the output of your dumped variables.
- This will work with both simple and complex variables. However,**be very careful when using it with Nested ORM objects**, as you can potentially dump your entire database and crash the server.
  - Leverage the top argument to limit dumping.

```javascript
writeDump( complex );abort;

<cfdump var="#server#" abort=true>

writeDump( var=arrayOfORM, top=5 );abort;
```

- Important: Adobe Engines have a very evil setting called Report Execution Times, make sure it is always turned OFF. If you use it with any application that leverages Components, it will slow down your application tremendously.

### Checking for existence

- Note the different syntax and quotes needed for the methods:

```javascript
// Notice the variable name is in quotes
if (isDefined("myVariable")) {
  writeOutput(myVariable);
} else {
  writeOutput("Not Defined!");
}

// Notice that the variable is NOT in quotes
if (isNull(myVariable)) {
  writeOutput("Not Defined!");
} else {
  writeOutput(myVariable);
}

// What is this variables scopes???
if (structKeyExists(variables, "myVariable")) {
  writeOutput(myVariable);
} else {
  writeOutput("Not Defined!");
}
```
