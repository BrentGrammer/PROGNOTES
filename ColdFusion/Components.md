# Components

- From [Ortus Solutions book](https://modern-cfml.ortusbooks.com/cfml-language/components)

- Classes that have properties and methods (behavior) and can be instantiated as objects.
- .cfc files (Cold Fusion Component)

### Example component

```java
 /**
 * Doc comment
 */
 component accessors="true"{ // accessors=true auto-creates getters and setters

  property name="name" type="string";

  property name="age" type="numeric";

  /**
  * Constructor
  */
  public any function init( required name ){
   variables.name = arguments.name;

   return this;
  }

  function run(){
   //...
  }

 }

 // Using the class
 // Create a new instance of the User class
user = new User( name="luis" );
// execute a function within it
user.run();

// using createObject() - need to call init to run the constructor!
user = createObject("component", "User").init();
```

- Note: the `new` keyword calls constructor (init) automatically, while The `createObject()` will not, you will have to call the constructor manually

  - use user = createObject( "component", "User" ).init();

- Best practice is to always have an init() constructor in a component and always `return this;` even if you don't do anything in the component:

```java
component {
  public any function init() {
    return this;
  }

  // other code
}
```

## Constructor

- The init function in a component
- You return `this` which is a reference to the instance of the class

```java
function init(){
 // prepare object state, cache data, start the engines

 // typically you return this at the end of an init() constructor
 return this;
}
```

### Pseudo Constructor

- Any loose lines of code in the component will be run on object creation
- Recommended to avoid pseudo constructors and put all that loose code in an init() constructor
- **NOTE: You cannot alter properties in the pseudo constructor - you need to do this in the init() constructor!**

```java
component {
  writeDump('runs on creation');

  public function someMethod() {
    // do something. just a method.
  }

  writeDump('another loose line run on object create');
}
```

### This keyword

- a ref to the object/instance
- Can return it to make methods chainable:

```java
function setValue( required val ){
 variables.value = arguments.val;
 return this;
}

obj
 .setValue( 'myvalue' )
 .setValue( 'otherValue' );
```

### Pseudo Constructors

- Code that runs before the init() constructor:

```java
component{
    // Pseudo Constructor starts here

    this.helper = now();
    static {
        staticVar : 2
    };

    // Pseudo Constructor ends here
    function init(){
        return this;
    }

}
```

## Scope in components

- `variables` - private to component, all properties are placed here. visible anywhere inside the component, but not outside the component.
- `this` - public and visible outside of component. contains public function references.

  ```java
  obj = new Component("prop");
  obj.prop = "new value"; // will not work if inside Component, you have variables.prop = arguments.prop;

  // Component.cfc
  component {
    public function init(string prop) {
      variables.prop = arguments.prop; // can't be set outside of component

      this.prop = arguments.prop; // using `this` now enables visibility and setting of obj.prop outside of the component! (not best practice)
    }
  }
  ```

  - NOTE: It is not best practice to expose properties directly with `this` - you should use getters and setters instead to safely set properties on components.

- `static` (Lucee only) - static scope methods or properties to the class and not the instance (just like static in Java)

## Attributes

- see [ortus book](https://modern-cfml.ortusbooks.com/cfml-language/components#component-attributes)

```java
component accessors="true" serializable="false" extends="BaseUser"{

}

component implements="cachebox.system.cache.ICacheProvider"{}

// can be provided in doc comment and applied as well:
/**
* My User
* @extends BaseUser
* @accessors true
* @serializable true
*/
component{

}
```

## Properties

- properties are defaulted to null if a default is not provided.

### Getters and Setters

- Adding `accessors="true"` to a component will tell CFML to automatically create getters and setters for any property defined in the component

```java
component accessors="true" {
  // acccessors=true will auto create getters and setters for any properties defined here:
  property name="myProp" type="string";

  public any function init() {
    setMyProp("some initial value"); // auto created setter with accessors=true

    return this;
  }
}
```

- You can also call getters and setters outside of the component with accessors=true:

```java
obj = new MyComponent();
obj.setMyProp("new value"); // works
```

- Note: you can override the auto created getters and setters by defining the same named method in your component if needed.

## Functions

- By default all functions in a component are public
- See [accessors for type and scope details](https://modern-cfml.ortusbooks.com/cfml-language/components/functions#function-access-types-and-scopes)
  - private functions are in the `variables` scope, public fns are in the `this` scope.
  - Components that inherit from the component with the private method have access to it as well

```java
function hello(){
  return "Hola";
}

abstract function getFile();
public static function testStatic(){}
public final function hello(){}

private function saveData(){

}

/**
 * Check for existence
 *
 * @name The key to check
 */
function boolean valueExists( required name ){
  return variables.exists( arguments.name );
}
```

### Function Arguments

```java
function sayHello( target ){
 return "Hi #target#! I'm #name#";
}

function add( required a, required b ){
 return a + b;
}


// Let's call add
calculator.add( 1, 2 );
calculator.add( a=1, b=2 );

// struct collection
values = { a = 1, b = 2 };
calculator.add( argumentCollection=values );

// array collection
values = [ 1, 2 ];
calculator.add( argumentCollection=values );
```

### Function scope

- local - A struct that contains all the variables that are ONLY defined in the functions via the var keyword.
- **var or local scope your variables**. Always plan for multi-threaded applications and make sure you var scope your variables. Why? Well, if you do not var scope a variable then your variable will end up in the implicit scope which is variables.

```java
// Sum is not var scoped, so it will be placed in the variables scope, memory leak anyone?
function hello(){
  sum = a + b;

  return sum;
}

function hello( a, b ){
 var sum = a + b;
 return sum;
}

function hello( a, b ){
 local.sum = a + b;
 return local.sum;
}
```

- Scope variables, otherwise they will be placed automatically and CFML will search a large number of scopes for them (could cause collisions, memory leaks or unexpected values to be found if the variable is defined elsewhere up the scope)

### Static methods and variables

```java
// set them in the pseudo constructor using the static keyword:
component MyFunkyCalculator{

    public any function init() {
        return this;
    }

    // Static Constructor
    static {
        CACHE_KEY = "luis",
        multiplier = 4
    }


    static public numeric function calculate( a ){
        return static.multiplier * a;
    };
    static public string function getGlobalCacheKey(){
        return static.CACHE_KEY;
    }

}

// accessing static vars from a class
// Refer to the CFC by path, then use the :: and call a function or variable
// no need to new up or init the component
MyFunkyCalculator::CACHE_KEY;
MyFunkyCalculator::calculate( 1 );
```

## Inheritance

- Components that extend/inherit from other components do not need to duplicate accessors or properties or constructors - they will get the same ones from the component they extend:

```java
// Base class component
component accessors="true" {

  property name="someProp" type="string";

  public init(string arg) {
    setSomeProp(arguments.arg);
    return this;
  }

  public function baseMethod() {
    // do something
  }

}

// component that extends base class gets all of its properties, accessor functionality and constructor without having to duplicate
// note no need to add accessors="true" to get auto getters and setters for properties - it is inherited.
component extends="BaseComponent" {
  property name="specificToThisClass" type="string";

  public function specificToThisClassFunc() {
    // do something specific in here
    var specific = getSpecificToThisClass();
  }
}
```

## Using super

- Can reduce code duplication if multiple related classes need the same initialization
- Call `super.init(...args)` in the child class to get the same initialization as the parent class in it's constructor
  - You can only go up one level, you cannot skip levels (i.e. to a grand parent with `super.super...` etc.)
- Note: you can also use super to call methods in the parent class being extended if they are common to both classes to also help with DRY

```java

component extends="Parent" {
  public function init(args) {
    super.init(arguments.args); // sets properties and initializes them same as Parent component has for this component

    return this;
  }
}

// Parent.cfc

component {
  property name="args";

  public function init(args) {
    setArgs(arguments.args);

    return this;
  }
}

```

## Abstract components

- Abstract components cannot be created with the `new` keyword
- Abstract components can only be extended by other components
- Useful for self documenting code for components that are not meant to be created/newed up, but are a foundational base class for other components that are used in the app to build on.

```java
abstract component {
  // component code
}
```

### Final components

- using the `final` keyword on a component means it cannot be inherited by any other components

```java
final component {
  // component code
}
```

## Composition

- inject components instead of using inheritance
- Allows for swapping components at runtime (inheritance does not allow for this)
- see [video](https://cfcasts.com/series/oop-series/videos/4-4-why-composition) at timestamp 2:52
- **NOTE**: When using composition, private methods of components that are injected into the other cannot be seen or used. This is not the case with inheritance as all private methods and properties are available to the component extending it.

```java
<cfscript>
  // using composition to swap out a sub component for a component using it at runtime
  var sub = new MySubComponent(arg);
  var comp1 = new MyComponent(sub=sub);

  var sub2 = new MySubComponent(differentArg);

  comp1.setSub(sub2);

  // or you can do this:

  comp1.getSub().setSubComponentProp(newArg);
</cfscript>>
```

## Interfaces

- [CFCasts OO Video](https://cfcasts.com/series/oop-series/videos/5-2-interfaces-with-ducks)
- Useful when you have multiple components that have similar methods with different behaviors and you don't want to inherit from a base class (because the components differ in some ways as well)
- Also can solve the Diamond problem with multiple inheritance (not allowed in CFML)
- In the parent class where you would have had inherited methods, remove them. This way the child classes that don't need certain methods from the parent class will not have them and only have what they need based on the interfaces they implement.

### Creating an interface

```java
// ISwimmable.cfc

// use the keyword `interface`
interface
{
  // just the method signature, but no function body
  public any function swim();
}

// IQuackable.cfc

interface
{
  public any function quack();
}
```

### Using an Interface

- use the `implements` keyword

```java
// SpecialTypeOfDuck.cfc

component extends="Duck" implements="ISwimmable, IQuackable" {

  public any function swim() {
    writeOutput("implementation of swim in special type of duck");
  }

  public any function quack() {
    writeOutput("specific behavior for quack of special type of duck");
  }

}
```

### Assigning an Interface in an Abstract Class

- use the `interface` keyword
- Note that the abstract class does not have to implement the methods on the interface, but any child components that extend it must satisfy the interface

```java
// AbstractComp.cfc
abstract component interface="ISomeInterface" {
  // code
}
```

## Types of Objects

### Transient Objects

- objects that are created and deleted during the length of a single server request
- Usually needed when you have `property` tags and they can differ between instances of objects

```java
<cfscript>

something1 = new MyComponent("first");

something2 = new MyComponent("second");

// These are in the variables scope (no use of var or scoping in declaration)
// They will be deleted from memory at the end of the request and are transient objects

</cfscript>
```

### Singleton

- Used when you do not need instances of objects that differ
  - Prevents overhead and saves space
  - Can use singletons inside transient components as well
  - It is a single instance of a component that can be shared everywhere

```java
// Utils.cfc
component {
  // Note: no properties

  public any function init() {
    return this;
  }

  public function someHandyFunc() {
    // does something handy
  }
}

/// In Application.cfc ///
component {
  any function onApplicationStart() {
    // in application start, save singleton to application scope
    application.Utils = new Utils();
  }
}

/// Usage in other component (transient)   ///

// AnotherComponent.cfc
component accessors="true" {
  property name="someProp";

  public any function init( someProp ) {
    setSomeProp( arguments.someProp );

    return this;
  }

  public string function someFunc() {
    // do stuff
    // use singleton
    var something = application.Utils.someHandyFunc();
  }
}

```

### Factory Objects
- see [video](https://cfcasts.com/series/oop-series/videos/7-2-creational-patterns) at timestamp 8:12
- Classic example is needing to support different types of databases
- Used to avoid a bunch of if/elseif statements
- **NOTE** You can probably use a singleton for the Factory component since if you're not going to switch out the parameters at runtime

```java
// SQLFactory component
component {
  // pass in different db types to determine which component to load
  public any function init( string DBType ) {
    variables.DBType = arguments.DBType;
    return this;
  }

  public any function createModel( string tableName ) {
    // build a path to different components (in folders) based on the dbtype and folder
    var pathToModel = "models.#variables.DBType#.#arguments.tableName#";
    var objModel = createObject( "component", pathToModel ).init();
    // build and return a component factory builder for the dbtype that produces a model for use
    return objModel;
  }
}

// Usage of the factory:
<cfscript>
  // create the factory based on db type (use a singleton in this case as we don't change databases during the application lifetime)
  //objFactory = new SQLFactory( "mysql" );

  // use the factory to create a component for working with mysql and some table
  objModel = application.SQLfactory.createModel( "SomeTable" );

  // use the model created by the factory
    // each of the models the factory builds could implement the same interface (i.e. CRUD for ex.)
  objModel.create('something');

</cfscript>

// In Application.cfc
component 
{
  any function onApplicationStart() {
    application.SQLfactory = new SQLFactory( "mysql" );
  }
}
```


