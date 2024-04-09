# Strings in GoLang

### Strings

- use double quotes "" or back ticks ``
- taking the length of a string is the number of bytes not chars: `len("hello")`
- Note: Runes are an alias for int32
- To get length num of chars import the utf8 package:

```go
import "unicode/utf8"
// runes represent characters in Go
var myRune rune = 'a'
utf8.RuneCountInString("hello") // 5
```

- Common string ops:

```go
//indexing
var myString = "resume"
var indexed = myString[0] // 114 - UTF-8 number for the character, note this is different than using range or runes which will give you back the expected base 10 number for the utf-8 char

// print the type of a value with %T
fmt.Printf("%v, %T", indexed, indexed)

// len returns the number of bytes in a string, not the number of chars
len(myString) // number of bytes

// cast to a runes - unicode point numbers representing the character
var myString = []rune("resume") // casting a string to runes - int32 representation of utf-8 number

// use single quotes to declare a rune type
var myRune = 'a' // is a rune with the ''

```

### Working with strings

- Strings are immutable so you should use the "strings" package in go to concatenate them etc. as it is more efficient

```go
import "strings"

var strSlice = []string{"h","e","l","l","o"}

// create a string builder
var strBuilder strings.Builder

for i := range strSlice {
    sreBuilder.WriteString(strSlice[i]) // adds each letter to a new string
}
// use the new string:
var concatedStr = strBuilder.String() // "hello"
```

### Printing strings

```go
// use Printf to format
// use %v for value (i.e. an int)
fmt.Printf("The value is %v", val)
```