# Structs in GoLang

### Structs

- Can think of structs as types and use them to create your own types
- Structs can hold mixed types by defining them in fields

```go
// Declare a type with the `type` keyword NOT var!!!
type gasEngine struct{
    mpg uint8
    gallons uint8 // 0 - 255
}

func main() {
    var myEngine gasEngine
    // access fields with dot notation
    fmt.Println(myEngine.mpg, myEngine.gallons) // 0, 0 (defaults)
}
```

#### set values

```go
type gasEngine struct{
    mpg uint8
    gallons uint8 // 0 - 255
    ownerInfo owner // fields can hold another struct
}

type owner struct{
    name string
}

// use struct literal syntax
var myEngine gasEngine = gasEngine{mpg: 25, gallons: 15, owner: owner{"Alex"}}

// or set directly:
myEngine.mpg = 20
```

#### Composing types:

```go
type gasEngine struct{
    mpg uint8
    gallons uint8 // 0 - 255
    owner // adds "name" field, not a nested owner property!
    int // if you add a type like this you have a "int" field that is of type int
}

type owner struct{
    name string
}

var myEngine gasEngine = gasEngine{mpg: 25, gallons: 15, owner: owner{"Alex"}}
fmt.Println(myEngine.name) // works - use .name, not .owner.name - "Alex"
fmt.Println(myEngine.owner.name) // still works and gives "Alex"
fmt.Println(myEngine.owner) // {Alex} - the struct with the name value in it (key is ommitted/implied)
```

#### Anonymous Structs

```go
// define struct inline and then assign values to fields (note: not reusable)
var myEngine = struct{
    mpg uint8
    gallons uint8
}{mpg: 25, gallons: 15}
```

#### Struct methods (receiver functions)

```go
type gasEngine struct{
    mpg uint8
    gallons uint8 // 0 - 255
}

// assigns the gunction milesLeft to the gasEngine type
func (e gasEngine) milesLeft() uint8 {
    // reference the gasEngine struct as e
    return e.gallons * e.mpg
}

var myEngine gasEngine = gasEngine{mpg: 25, gallons: 15}
myEngine.milesLeft() // will calculate using current vals in myEngine
```
