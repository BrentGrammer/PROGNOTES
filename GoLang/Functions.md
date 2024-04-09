# Functions in GoLang

## Functions

- specify type after arg

```go
func add(x int, y int) int {
    return x + y
}

// Specify multiple return values:
func multiplyadd(x int, y int) (int, int) {
    var sum int = x + y
    var product int = x * y
    return sum, product // use comma separated return vals
}

/**
* ERRORS
*/
// import errors package (go builtin) to create errors
import "errors"

func divide(x int, y int) (int, error) {
    var err error
    if y == 0 {
        err = errors.New("Cannot divide by 0")
        // still need to return the int
        // return the error as well
        return 0, err
    }
    result := x / y
    return result, err //err will be nil
}

// when calling, check for error
var result, err = divide(5,0)

if err != nil {
    // print the error
    fmt.Printf(err.Error())
} else {
    fmt.Printf("The result is %v", result)
}
```
