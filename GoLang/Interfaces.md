# Interfaces in GoLang

### Using Interfaces

- Use interfaces to use structs more generically
    - The interface{} type in Go is a special type that can hold values of any type. Similar to "any" in TypeScript 
- Interfaces ONLY allow definition of methods, not properties/fields!

```go
// Two types of engines, but we want to pass in a general engine type
type gasEngine struct{
    mpg uint8
    gallons uint8 // 0 - 255
}

type electricEngine struct{
    mpkwh uint8
    kwh uint8 // 0 - 255
}

// make an engine interface
type engine interface{
    milesLeft() uint8 // specify signature of method
}

// method implementation for each engine type
func (e gasEngine) milesLeft() uint8 {
    return e.mpg * e.gallons
}

func (e electricEngine) milesLeft() uint8 {
    return e.kwh * e.mpkwh
}

// can pass generic type into our function:
func canMakeIt(e engine, miles uint8){
    if miles <= e.milesLeft() {
        // do something
    } else {
        // warn can't make it
    }
}

// pass in any engine type now:
var myEngine gasEngine = gasEngine{ mpg: 1, gallons: 34}
canMakeIt(myEngine, 50) // can use gas or electric engine
```
