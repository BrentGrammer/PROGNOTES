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