# Structures

- [docs](https://modern-cfml.ortusbooks.com/cfml-language/structures)

- All CFML structures are passed to functions as memory references, not values. Keep that in mind when working with structures.

### creating a struct literal

- Note no quotes for keys (see note on case sensitivity below)

```java
produce = {
    grapes     = 2,
    lemons     = 1,
    eggplants  = 6
};
```

- note that `=` sign and `:` are interchangeable in CFML. So you can use any to define your structures

### Case insensitive - keys are all caps

- CFML is a case-insensitive language, the above structure will store all keys in uppercase. If you want the exact casing to be preserved in the structure, then surround the keys with quotes (").

```java
produce = {
    "grapes"     = 2,
    "lemons"     = 1,
    "eggplants"  = 6
};
```

- **Use double quotes to preserve case if desired!**

## Safe getting

### Safe Navigation using ?

```java
user = { age : 40 }

echo( user.age ) // 40
echo( user.salary ) // throws exception
echo( user?.salary ) // nothing, no exception
echo( user?.salary ?: 0 ) // 0
```

### structFind() - allows for default value

- use `structFind()` and provide a default value.
  - Default value which will be returned if the key does not exist or if null was found. Currently only supported by Lucee.
- **recommend using array notation as the case is preserved in array notation, while in dot notation, it does not.**

```java
countries = {
    "USA"="Washington D.C.",
    "Germany"="Berlin",
    "Japan"="Tokio"
};
writeOutput(structFind(countries, "Germany", "Not Found"));
```

### structGet() - USE WITH CAUTION

- See also [structGet()](https://cfdocs.org/structget)

  - If there is no structure or array present in the path, this function creates structures or arrays to make it a valid variable path.

- Get a value in a structure using structGet

```java
x = { y = { z=8 } };
writeDump( structGet("x.y.z") );
```

- Accidentally Modifying a Structure
  - The structGet function will modify the variable x by adding a new structure x.a and also adds a key x.a.b to satisfy the path.

```java
x = { y = { z=8 } };
writeDump( structGet("x.a.b") );
writeDump(x);
```

- Accidentally Overwriting a variable using structGet
  - The value of x.y.z[2] will be set to an empty struct.

```java
x = { y = { z=[1,2,3] } };
writeDump( structGet("x.y.z[2]") );
writeDump(x);
```

### Looping over keys

```java
for( var key in produce ){
 systemOutput( "I just had #produce[ key ]# #key#" );
}

produce.each( function( key, value ){
  systemOutput( "I just had #value# #key#" );
} );

// produce list of keys if needed
produce.keyArray()
    .each( (item) => echo( item ) )

writeOutput( "My shopping bag has: #produce.keyList()# " )
writeOutput( "Do you have carrots? #produce.keyExists( 'carrots' )#" )
```

### Created ordered n different types of structs

- [docs](https://cfdocs.org/structnew)

```java
ordered = structNew( "ordered" ); // ordered, linked, soft, synchronized, weak
ordered.a = 1;
ordered.b = 2;
ordered.c = 3;
writeDump( ordered );
```

- In Lucee:
  `StructNew( type=string, onMissingKey=function );`
- pass in function to call if missing key. see [docs](https://docs.lucee.org/reference/functions/structnew.html)
