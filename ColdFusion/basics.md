# ColdFusion Basics

ColdFusion (CFML) is an interpreted and dynamic ECMA Script like language that compiles to Java Bytecode directly, thus running in the Java Virtual Machine (JVM) and in almost every operating system.

- [good intro](https://www.youtube.com/watch?v=3dKZ7KEHhAk)
- [cffiddle](cffiddle.org) - fiddle playground for CFML online
- [trycf](www.trycf.com) - allows you to run code against lucee online
- [Check this vid for resources](https://www.youtube.com/watch?v=HUcrxyCZa4w)

### Learning

- [Good modern guide on CFML](https://modern-cfml.ortusbooks.com/)
- [CFML In 100 Minutes](https://github.com/mhenke/CFML-in-100-minutes/wiki)
- [2016 Introduction to ColdFusion](https://www.youtube.com/playlist?list=PL3iywAijqFoUD31CQBLsHvJn4WAonNA7r)
- [Coding Standards/Best Practices - Ortus Solutions](https://github.com/Ortus-Solutions/coding-standards/blob/master/guides/coldfusion.md)

### Documentation

- [cfdocs](https://cfdocs.org/): Main reference for CFML
- [official docs](https://helpx.adobe.com/coldfusion)
- [LearnCFInAWeek](https://learncfinaweek.com)
- [cfcasts](https://cfcasts.com) - good video tutorials
- [cfcom forums, community list](https://www.carehart.org/cf411/#cfcommhelp)

### Command Box setup

- [setup](https://commandbox.ortusbooks.com/setup)
- [in depth guide](https://commandbox.ortusbooks.com/getting-started-guide)
- You can make the box.exe available in any Windows terminal by adding its location to the PATH system environment variable. See http://www.computerhope.com/issues/ch000549.htm

### Blogs

- [Coldfusion Community Portal](https://coldfusion.adobe.com)
- [Charlie Arehart](https://carehart.org)
- [Ben Nadel](https://bennadel.com)
- [Raymond Camden](https://raymondcamden.com)
- [Brad Wood](https://codersrevolution.com)
- [Pete Freitag](https://petefreitag.com)
- [Michaela Light](https://teratech.com/blog)

### Social

- [Adobe ColdFusion Summit](https://cfsummit.adobeevents.com)
- [Into the Box Conference](https://intothebox.org)
- [CF Camp Conference in Munich](https://cfcamp.org)
- [Ortus Community](https://community.ortussolutions.com)
- [CFML Slack Channel](https://cfml.slack.com)
- [Coldfusion Programmers Group Facebook](https://facebook.com/groups/CFprogrammers)
- Online ColdFusion Meetup

### Jobs

- CFML Slack Channel jobs channel
- ColdFusion Job Resource and ColdFusion Remote Jobs Groups on Facebook
  - facebook.com/groups/cfjobresource
  - facebook.com/groups/152353332139168
- getcfmljobs.com
- Coldfusion Summit conference

### Pre-processed and Parsed

- Coldfusion serves pre-processed content as **static content** back to the client.
- The content is not dynamically updated like in React, AJAX etc.
- The information that is parsed is on the server side, info that is on the server, not the client. (date now() is the time on the server, not the client)
- Uses JIT compiling for CFML code, no need to pre-compile

## Syntax

- [Variables](./Variables.md)

### Types

- Built on top of Java:

```javascript
a = "hello";
writeOutput(a.getClass().getName());
```

- If you run the script above in the REPL tool, you will see the output as java.lang.String. Therefore, the variable is typed as a String and can call on any method that java.lang.String implements. You can try this for the many types in CFML, like structs, arrays, objects, etc.
- [member functions](https://cfdocs.org/member) you can use on variables of different types (i.e. myArray.sort() or myArray.append())

### Tag and Script

- two syntax modes: Tags and Script mode
- A component is a .cfc file (Cold Fusion Component)

### Common

- `#` tells where to begin and end parsing code
  - Similar to `{}` in React - code/variables goes in between the delimiters

### Tags

- Common Tags include:

  - `<cfoutput></cfoutput>` - contains CFML to be processed
  - `<cfif>`, `<cfelseif>`,`<cfelse>`
  - `<cfmail to="" from="" subject="" type="text"></cfmail>` - send mail through coldfusion
  - `<cfquery name="myQuery" datasource="myDB">`- for db queries
  - `<cfloop>`
  - `<cfinclude template="myFile.cfm">` - including a file within another. no closing tag needed

- Note: for forms, libraries are recommended that are more robust and the use of `<cfform>` is not really used anymore.

### Script vs. Tag Based

### Tag:

```cfml
<cfset Colors = arrayNew(1)>
<cfset Colors.append('Red')>
<cfset Colors.append('Green')>
<cfset Colors.append('Blue')>

<ul>
    <cfoutput>
        <cfloop index="thisColor" array="#Colors#">
            <li>#thisColor#</li>
        </cfloop>
    </cfoutput>
</ul>
```

### Script:

```cfml
<cfscript>
    Colors = [ 'Red', 'Green', 'Blue' ];

    writeOutput('<ul>');
    for (thisColor in Colors) {
        writeOutput('<li>#thisColor#</li>');
    }
    writeOutput('</ul>');
</cfscript>
```

## Functions

- dateFormat(now(), 'm/d/yyyy')
- arrayNew(), structNew() - create arrays and structs
- replace() and replaceNoCase() - replace substrings, remove dashes etc.
- use the function `parseDateTime(myString)` to translate a variable or a string into a date value
  - `<cfif now() EQ parseDateTime("Wednesday, January 30, 2002 7:02:12 AM PST")>`

## Forms

- `url` is a global available to access query string params etc.
- `isDefined("url.error")` to null check variables
- `#htmlEditFormat(url.someQueryParam)#` to escape script tags and protect for XSS in

## File Extensions

- If the server sees a file with coldfusion extensions it sends them to be processed by the coldfusion server.

### 3 extensions:

- .cfm
- .cfc
- .cfml
  - no usuaslly used, most files have a .cfm or .cfc extension

## Frameworks

### Modern and still maintained:

- Coldbox - defacto standard and most popular coldfusion framework. Luis Majano of Ortus Solutions created it.
- Framework One (FW/1) - lightweight option and easy to use
- CF Wheels - open source similar to Ruby on Rails

### legacy

No longer maintained:

- Fusebox
- Mach II
- Model/Glue

## Coldfusion companies

- Epicenter Consulting
- Ortus Solutions
- Foundeo
- Tera Tech
- CF Web Tools

### Hosting companies

- Hostek (hostek.com)
- Media3 (media3.net)
- CFDynamics
- Vivio Technologies
- NewTek Technology Services
- Coalesce (via AWS)

### Open Source

- [Lucee](lucee.org) - open source ColdFusion engine

## VS Code packages

- [Recommended extenstions](https://modern-cfml.ortusbooks.com/intro/history#vscode-packages)

## Production

### Coldbox Framework

- Coldbox Framework available as a lightweight Docker image (MiniBox)
- or an AMI instance running on top of nginx or Tomcat.

## Operators

- `!===` - use 3 `=` just like in `===` to check for not equals with type strictly enforced
- `contains` `does not contain` - includes/!includes equivalent
- `?:` - null coalescing op. note that we have seen inconsistencies in both Adobe and Lucee engines regarding the implementation of this operator. I would avoid using it in Adobe 2018 as it is broken in several cases
- `user?.getSalary()` - `?` can be used as a safe navigation operator. Here if salary doesn't exist on user, or user does not exist, no error will be thrown(like the optional chain operator in typescript). undefined will be returned instead.
  - can combine with elvis operator for safe get ops: `result = var?.key?.otherKey ?: "";`
- `var variableName = [ ...myArray ]` - spread operator works the same as in JS
  - alternatively use append: `var variableName = [].append( myArray )`

## Null/Emptiness

- Engine might only have partial null support (empty value could be null or an empty string)
- activating full-null support. You can do this in the admin or programmatically via the Application.cfc file, which can be used when building web applications. You can learn more about it here

```javascript
//Application.cfc
component{
    this.nullSupport = true;
}
```

- Use the isNull() or isDefined() methods to evaluate for nothingness.
  - recommend that you use isNull() as it expresses coherently its purpose. Since isDefined() can also evaluate expressions.

```javascript
r = getMaybeData();
if (isNull(r)) {
  // do something because r doesn't exist
}

if (isDefined("r")) {
}
```

- setting null:

```java
//Lucee only function.
r = nullValue()
```

- Note: functions without a return value return null.

## Strings

- [Strings in CFML](https://modern-cfml.ortusbooks.com/cfml-language/strings)

- a new string object is always created when concatenating strings together. This is a warning that if you do many string concatenations, you will have to use a Java data type to accelerate the concatenations

### not 0 indexed

note that string and array positions in CFML start at 1 and not 0.

```java
name = "luis";
writeoutput( name[ 1 ] ) // => will produce l
```

### Trimming

- `Trim("Hello ")` or `"hello".trim()`

### Get substring

- `mid`: The mid function extracts a substring from a string. For instance, I could call `Mid("Welcome to CFML Jumpstart", 4, 12)` and it would give you back: come to CFML.

### Concatenation

- use `&` operator

```java
name = "Luis";
a = "Hello " & name & " how are you today?";
```

- use `myvar.toString()` to cast to a string

## JSON

- use `serializeJSON()` or `.toJSON()`
- NOTE: You need to wrap keys in single quotes to preserve casing!: By default CFML will convert the keys in a struct to uppercase in the result JSON document:

```java
person = { name = "Luis Majano", company = "Ortus Solutions", year = 2006};
writeOutput( serializeJSON( person ) );

// Will become
{ "NAME" : "Luis Majano", "COMPANY" : "Ortus Solutions", "YEAR" : 2006 }
If you want to preserve the key casing then wrap them in double/single quotes and define the case:


person = {
    'Name' = "Luis Majano",
    'company' = "Ortus Solutions",
    'year' = 2006
};

// Will become
{ "Name" : "Luis Majano", "company" : "Ortus Solutions", "year" : 2006 }
```

#### Careful with auto casting when serializing JSON:

Adobe ColdFusion may incorrectly serialize some strings if they can be automatically converted into other types, like numbers or booleans. One workaround is to use a CFC with cfproperty to specify types. A more formal workaround is to call setMetadata() as a member function on a struct to force a type:

```java
myStruct = { "zip"="00123" };
myStruct.setMetadata( { "zip": "string" } );
writeOutput( serializeJSON(myStruct) );
```

### Deserialize json

- [See Deserializing JSON in CFML](https://modern-cfml.ortusbooks.com/cfml-language/json#deserializ)

### Checking if a value is json

CFML has a function to test if the incoming string is valid JSON (https://cfdocs.org/isjson) or not: `isJSON()`

## Numbers

- Integer or Float type (int or double in Java) (Adobe CF)
- Lucee stores all numbers as Doubles
- CFML will do the auto-casting for you when converting between integers and doubles.
- [List of mathematical operators you can use with numbers](https://modern-cfml.ortusbooks.com/cfml-language/numbers#operators-and-functions)

### Truthy and Falsey

- 0 is falsey, any other number (including negatives) are truthy.
  - -1 is truthy etc.

### Casting to number

- cast with `toNumeric(myvar)`
- The parseNumber() is also used to convert a string number into a numeral system (https://cfdocs.org/parsenumber)
- Check numbers with `isNumeric(myvar)`

### Currency/Money

- If you are dealing with currency or tracking precision, please read about precisionEvaluate() to represent big numbers and precision results: https://cfdocs.org/precisionevaluate

### USing the numeric type:

```java
numeric function add( numeric a, numeric b ){
    return a + b;
}
```

## Arrays

- [Common array methods](https://modern-cfml.ortusbooks.com/cfml-language/arrays#common-methods)
- searched the contents of the array using the member function findNoCase() , and it gave us the index position of the element in the array.

  - `myArr.findNoCase("something");`

### Creating Arrays (Lucee)

- ArrayNew( dimension, type, synchronized:boolean )

```java
// array of strings
stringArray = arraynew( 1, "String" )
// array of numerics
numericArray = arraynew( 1, "Numeric" )
// array of User CFCs
aUsers = arraynew( 1, "User" )
```

### for..in syntax (used for arrays)

```java
for( var thisMeal in meals ){
 systemOutput( "I just had #thisMeal#" );
}
```

### .each

- Uses concurrency (use with caution)

```java
// arrayEach( array, callback, parallel:boolean, maxThreads:numeric );
// each( collection, callback, parallel:boolean, maxThreads:numeric );

myArray.each( function( item ){
   myservice.process( item );
}, true, 20 );
```

#### Caution: it is not performant and/or flexible. Under the hood, the engines use a single thread executor for each execution, do not allow you to deal with exceptions, and if an exception occurs in an element processor, good luck; you will never know about it. This approach can be verbose and error-prone

- consider using the ColdBox Futures approach (usable in ANY framework or non-framework code). You can use it by installing ColdBox or WireBox into any CFML application and leveraging our async programming constructs, which behind the scenes, leverage the entire Java Concurrency and Completable Futures frameworks.
  - see [docs](https://coldbox.ortusbooks.com/digging-deeper/promises-async-programming/parallel-computations)

## Database Queries

- [querying](./DatabaseQueries.md)

## Includes

- like a Mixin : In object-oriented programming languages, a mixin is a class that contains methods for use by other classes without having to be the parent class of those other classes; No inheritance needed.
