# ColdFusion Basics

- [good intro](https://www.youtube.com/watch?v=3dKZ7KEHhAk)

### Documentation

- [cfdocs](https://cfdocs.org/)
- [official docs](https://helpx.adobe.com/coldfusion)
- [LearnCFInAWeek](https://learncfinaweek.com)
- [cfcasts](https://cfcasts.com) - good video tutorials

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
