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

  property name="name";

  property name="age" type="numeric";

  /**
  * Constructor
  */
  function init( required name ){
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
```

- Note: the `new` keyword calls constructor (init) automatically, while The `createObject()` will not, you will have to call the constructor manually
  - use user = createObject( "component", "User" ).init();

## Constuctor

- The init function in a component
- You return `this` which is a reference to the instance of the class

```java
function init(){
 // prepare object state, cache data, start the engines
 return this;
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

- `variables` - private to component, all properties are placed here. `variables.myProp`
- `this` - public and visible outside of component. contains public function references
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

### Properties

- properties are defaulted to null if a default is not provided.

### Functions

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
    
    // Static Constructor
    static {
        CACHE_KEY = "luis",
        multiplier = 4
    }
    
    
    public static function calculate( a ){
        return static.multiplier * a;
    };
    public static function getGlobalCacheKey(){
        return static.CACHE_KEY;
    }

}

// accessing static vars from a class
// Refer to the CFC by path, then use the :: and call a function or variable
MyFunkyCalculator::CACHE_KEY;
MyFunkyCalculator::calculateValues( 1 );
```