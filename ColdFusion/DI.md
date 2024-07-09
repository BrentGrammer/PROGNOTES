# Dependency Injection

- Lowers maintenance cost of making and managing objects in your application
- Using DI Frameworks reduces boilerplate code and automatically wires up objects and their dependencies needed for you.

## Wirebox

- Notes From [Talk by Grant on CFCasts](https://cfcasts.com/series/webinars/videos/grant-on-injecting-dependencies-with-wirebox)

- A dependency Injection Framework made by Ortus Solutions
- Comes with Coldbox Framework installed already
- Can add to any CFML application (including legacy)

### Installation

- `box install wirebox`
  - installs into a folder called wirebox in your project
  - should probably gitignore this folder

### Example usage

```java
<cfscript>
    // create an injector
    wirebox = new wirebox.system.ioc.Injector();

    // wirebox will find the component, auto wire it up and return it back.
    someObj = wirebox.getInstance( "someObj" );

    // coldbox usage - you do not have to create an injector:
    // someObj = getInstance( "someObj" );
</cfscript>
```

### Configuring Wirebox (Configuration Binder)

- Use the **Configuration Binder**
  - A single .cfc file that configures Wirebox's behavior
  - If using coldbox: it is in `/config/WireBox.cfc`
- Can create
  - Aliases (name object getters differently)
  - Scan locations(tell Wirebox which folders to look at to find your objects)
  - more, etc.

```java
// WireBoxConfig.cfc

// extend the wirebox binder class
component extends="wirebox.system.ioc.config.Binder" {
    function configure() {
        // config goes here

        // mapping directories
        mapDirectory(
            packagePath="models", // where your components are in
            namespace="@MYNAMESPACE"
        );
        // now you can get an object referencing the namespace: myObj = wirebox.getInstance("myComponent@MYNAMESPACE");


        //aliases
        map( "componentAlias" ).to( "myComponent" );
        // can use like: wirebox.getInstance("componentAlias"); // returns myComponent
    }
}

// pass in name of file to tell wirebox to use the configuration binder
wirebox = new wirebox.system.ioc.Injector( "WireBoxConfig" );
```

## Injecting Dependencies with WireBox

### Property Injection (recommended way to inject)

- Use the `inject=` in the property declaration
- less verbose than other ways

```java
component name="MyComponent" accessors="true" {
    // this will auto inject the object
    property name="componentName" inject="ComponentToInject";

    function init() {
        return this;
    }
}
```

### Constructor Injection

- WireBox injects dependencies into the init() constructor
- Use constructor annotations to tell WireBox to do this

```java
component name="MyComponent" accessors="true" {
    /**
     * Constructor annotation tells wirebox to inject this into the constructor
     * @componentArgName.inject ComponentToInject
     */
    function init( required componentArgName ) {
        variables.componentArgName = arguments.componentArgName;
        return this;
    }
}
```

### Setter Injection

- Setter method on your object using `inject=`

```java
component name="MyComponent" accessors="true" {

    function init( required componentArgName ) {
        inject="ComponentToInject" {
            variables.componentArgName = arguments.componentArgName;
        }
        return this;
    }
}
```

### Lifecycle methods

- Methods you can hook into in the component if needed
- `onDIComplete()` - fires after injection occurs in object instantiation

## Features

- Object Populator to populate objects (useful with form data for example)
  - see [video](https://cfcasts.com/series/webinars/videos/grant-on-injecting-dependencies-with-wirebox) at timestamp 21:23

## Scopes

- left off at 23:50
