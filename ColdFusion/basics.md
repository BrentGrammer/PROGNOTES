# ColdFusion Basics

ColdFusion (CFML) is an interpreted and dynamic ECMA Script like language that compiles to Java Bytecode directly, thus running in the Java Virtual Machine (JVM) and in almost every operating system.

- [good intro](https://www.youtube.com/watch?v=3dKZ7KEHhAk)
- [cffiddle](cffiddle.org) - fiddle playground for CFML online
- [trycf](www.trycf.com) - allows you to run code against lucee online

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
