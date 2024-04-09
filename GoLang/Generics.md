# Generics in GoLang

## Generics

```go
// Specify a T type in square brackets after func name:
func sumSlice[T int | float32 | float64](slice []T) T{ // returns type T (generic)
    var sum T
    for _,v := range slice{
        sum += v
    }
    return sum
}

var slice = []float64{1,2,3}
// now call it passing in a type for the generic
sumSlice[float64](slice)
```

- Using the any type:

```go
func isEmpty[T any](slice []T) bool{
    // makes sense using any since we want to check any type of slice
    return len(slice) == 0
}
```

### Unmarshalling JSON

- Unmarshalling a JSON object will load it into a struct

```go
import (
    "encoding/json"
    "io/ioutil"
)

func loadJSON[T contactInfo | purchaseInfo](filePath string) []T {
    // use ioutil to read a json file
    data, _ = ioutil.ReadFile(filePath)

    var loaded = []T{} // initialize empty slice of generic type

    // use json from encoding/json package
    // unmarshalling json will load it into a struct
    json.Unmarshal(data, &loaded) // note we pass a reference to loaded instead of passing it in so we don't make another copy

    return loaded
}
```

#### Loading JSON to a Struct

```json
[
  {
    "name": "Alex",
    "age": 29
  },
  {
    "name": "Jason",
    "age": 38
  }
]
```

```go
type peopleInfo struct{
    Name string
    Age int
}

// pass generic type as peopleInfo so the func knows what type struct to load into
var people []peopleInfo = loadJSON[peopleInfo]("./peopleinfo.json")

[]peopleInfo{
    {
        Name: "Alex",
        Age: 29, // note the comma needed after last entry in structs
    },
    {
        Name: "Jason",
        Age: 38,
    }
}
```

### Using generics to make a parent type

- Make a car type that can have a gas or electric engine:

```go
type gasEngine struct{
    gallons float32
    mpg float32
}

type electricEngine struct{
    kwh float32
    mpkwh float32
}

// in car we can pass a generic of T which can be gas or electric engine
type car [T gasEngine | electricEngine]struct{
    carMake string
    carModel string
    engine T // generic for the engine
}

// pass in generic when making the car
var gasCar = car[gasEngine]{
    carMake: "Honda",
    carModel: "Civic",
    engine: gasEngine{
        gallons: 12.5,
        mpg: 40
    }
}
```
