# GoLang

Main syntax notes:

- typing syntax:
  - brackets BEFORE the type name for list types: `[]int`
  - type comes after name: `var myVar int`
  - arrays declared with {} instead of []: `var slice = []int32{1,2,3}`
- loops
  - No parens around the condition: `for x == y {}`
  - use range keyword: `for i, v := range myList {}`
  - traditional for: `for i:=10; i<10; i++ {}`
- Strings:
  - Avoid using `len(str)` to get the length of a string (returns number of bytes)
    - use `utf8.RuneCountInString(myStr)`
- Lists (slices)
  - Appending to a list: `append(myList, item)`

### Mod file

- Dependencies and versions are listed in the `go.mod` file

### Running a go program

- `go run path/to/main.go`
- This compiles and executes the file in one step (no build or binary produced)

### Building a binary:

- `go build path/to/main.go`
- This produces a binary file (i.e. `main`) that you can run with
  - `./main`

### Packages

- Folder with a collection of .go files

### Module:

- A collection of packages

## Creating a Go package

- You need to declare the package for every .go file at the top

  - `package main`
  - Note: main is a special package and the compiler looks for it as the entry point. There needs to be a main() function in this package

  ```go
  package main

  func main(){
    // declaring variables - you must use every variable you declare!
    var num int = 10 // int16, int32, int64, uint (only positive integers), float32 or float64
  }
  ```

### Declaring Variables

- You must use every variable that you declare!
- `var myString string = "hello"`
- `myString := "hello"`
  - Can omit the var keyword if using :=

#### constants

- `const myString string = "const string"`
  - Cannot change this variable once it is created using const keyword

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

### Numbers

- 8-bit: int8/uint8
- 16-bit: int16/uint16
- 32-bit: int32/uint32
- 64-bit: int64/uint64
- 32- or 64-bit based on system architecture: int/uint
- Synonym for int32: rune
- synonym for int8: byte
- Floating-Point Numbers
- Floating-point numbers can contain a decimal point. There are two different sizes.

#### Floats

- 32-bit: float32
- 64-bit: float64

#### Complex

- 32-bit float + imaginary number: complex64
- 64-bit float + imaginary number: complex128

#### When to use which:

- By default just use int. It's 32 bits or 64 bits depending on your arch
- If you know it might be bigger than about 2 billions, use int64. Otherwise you'll get an overflow on a 32 bits arch.
- If you know you will have a lot of them in memory, AND it's small enough to fit a int8/int16/int32, you can use that. But most of the time there is no significant gain to do so
- probably want uint32 for IDs (4 billion positive ints)
- uint8 is 0 to 255

### Booleans

- `var myBoolean bool = false`

### Default Types:

- ints/numbers/floats/rune = 0
- Booleans = false
- Strings = '' (empty string)
- error = nil

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

### Printing strings

```go
// use Printf to format
// use %v for value (i.e. an int)
fmt.Printf("The value is %v", val)
```

## Control flow

### Switch

- No `break` statements are needed and they are implied.

```go
switch {
    case err != nil:
        fmt.Printf(err.Error())
    case remainder == 0:
        fmt.Printf("The remainder is %v", remainder)
    default:
        fmt.Println("Default case fired")
}
```

- Conditional switches (insert variable after switch keyword)

```go
switch remainder {
    case 0:
        fmt.Printf("remainder is 0")
    case 1,2:
        fmt.Printf("there was 1 or 2 as remainder")
    default:
        fmt.Println("default")
}
```

## Collections

### Arrays

- Fixed length
- Indexable
- Contiguous in Memory
- Can slice with `:`

```go
// initializing a array with 3 elements
var intArr [3]int32 // initialized to default type (0s): [0,0,0]

// Slicing:
intArr[1:3] // index 1 and 2 in a new array [0,0]

// assign or reassign by index
intArr[1] = 123 // [0,123,0]

// print memory address with &
fmt.Println(&intArr[2]) // 0x140012200c (the address of the first byte of the 2nd index item)

// immediately initialize an array:
var intArr [3]int32 = [3]int32{1,2,3}
// alternatively you can initialize with the := and use [...] which will be set to the number of elements created (3)
intArr := [...]int32{1,2,3}
```

### Slices

- Wrapper around arrays
- Omit the length value in declaration and that gives you a slice

```go
var intSlice []int32 = []int32{4,5,6}

// can use the append builtin to add values:
intSlice = append(intSlice, 7) // returns new slice (array) [4,5,6,7]

// appending will increase the capacity of the array under the hood
// get length of a slice (how many elements are in it)
len(intSlice)
// get the capacity (how many els it can hold)
cap(intSlice) // note: you can't access empty slots in the slice and will get index out of range error.

// spread operator:
var intSlice2 []int32 = []int32{8,9}
intSlice = append(intSlice, intSlice2...)
```

#### Creating a slice with make

```go
var intSlice3 []int32 = make(int32[], 3, 8) // 3 is the length, 8 is optional capacity - by default the capacity is the length.
// good practice to specify the capacity if you roughly know how many els you'll need to hold in it - this prevents the underlying recalculation when more slots are needed (the re-allocation slows down performance)
```

### Maps

- A map will ALWAYS return something, even if you access a key that does not exist
  - Will return the default value for the type
  - you can use the optional second `ok` value boolean to check if key exists

```go
// can create with make function
var myMap = make(map[string]uint8)

// can initialize with values:
var myMap2 = map[string]uint8{"Adam":23, "Sarah":45}

// access a value:
myMap2["Adam"] // 23

// a map will always return default val for a key that does not exist
myMap2["Jason"] // returns 0 - default of uint8

// use the ok property to check if key exists
var age, ok = myMap2["Jason"] // ok will be false
if ok{
    fmt.Printf("The age is %v", age)
} else {
    fmt.Println("Invalid key")
}

// use builtin delete to remove a key
delete(myMap2, "Adam")
```

#### Iterate over a map with Range (using For Loops)

```go
// NOTE: ordering is not preserved or gauranteed for the keys
// can extract key (name)
for name := range myMap2 {
    fmt.Printf("Name: %v\n", name)
}

// also iterate over the vals ( for key, val ...)
for name, age := range myMap2 {
    fmt.Printf("Name: %v, Age: %v \n", name, age)
}

```

### Looping

```go
for i:=10; i<10; i++ {
    fmt.Println(i)
}

// Get the index and val using i and v
for i, v := range intArr {
    fmt.Printf("index: %v, val: %v \n", i,v)
}

// WHILE LOOP (use for with a condition)

var i int = 0

for i < 10 {
    fmt.Println(i)
    i = i + 1
}

// breaking in a loop - break will end the loop
for {
    if i > 10 {
        break
    }
    fmt.Println(i)
    i = i+1
}
```

### Structs

- Can think of structs as types and use them to create your own types
- Structs can hold mixed types by defining them in fields

```go
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

### Using Interfaces

- Use interfaces to use structs more generically

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

## Pointers

- A special type that stores a memory address

### Creating a pointer - use \*

```go
var p *int32 // p will hold the memory addr of a int32 value- this is nil if initialized this way and you can't reference or use it as is or you will get a runtime error.

// initialize p with new()
var p *int32 = new(int32) // gives a memory address that can hold an int32. p will now store a memory location which points to where the value is stored. This value will be 0 initially.
```

- Note: the value stored on initialization is `nil` and not `0` as if you were to initialize an int32 that's not a pointer!

### De-referencing a pointer with \*

```go
var p *int32 = new(int32)

// use *p to dereference and get the value
fmt.Printf("The value p points to is: %v", *p) // 0


```

### Set the value of a pointer with \*

```go
*p = 10 // set the val p mem addr is holding to 10
```

### nil reference errors

- Runtime errors that can happen with pointers if you try to assign or dereference a pointer that has not been initialized or has a memory addr:

```go
var p *int32 // not initialized
fmt.Println(*p) // nil reference error at runtime.
```

### Using the & to get a memory addr

- Can create a pointer from the address of another variable using `&`

```go
var p *int32 = new(int32)
var i int32 // non pointer initialization

p = &i // gets the mem addr of i and sets p to the memory address of i
// note this is different from p = *i which will dereference i and store the actual value in p

// if you change the value p is storing, then i is now also changed
*p = 1 // sets the value stored at the p mem addr to 1 (which i also points to)
```

### Difference when using non pointers:

```go
var i int32
var k int32 = 2 // regular assignment, 2 is stored at the memory location k
i = k // this will COPY the value to the memory location i (you have the same val stored at TWO different memory locations now)
```

#### CAUTION USING SLICES\*\*

```go
var slice = []int32{1,2,3}
var sliceCopy = slice // this is not as expected - the slice is pointers to an array, so not technically storing a new copy in a different memory address, just copying the pointers so to speak

sliceCopy[2] = 4 // modify the copy

// BOTH COPY AND ORIGINAL CHANGED! Slices contain pointers to underlying Array
fmt.Println(slice)     // 1,2,4
fmt.Println(sliceCopy) // 1,2,4
```

### Print and Check memory location of a pointer:

```go
var thing1 = [5]float64{1,2,3,4,5}

// use %p to print a pointer and the & operator to get the mem addr of a variable
fmt.Printf("The memory location of thing1 array is: %p", &thing1)
```

### Pointers and functions

- Passing in slices etc. to functions creates a COPY of the value
- You can use pointers when the things passed in are large and you don't want to waste memory and time creating copies of them.
  - Just have to be aware that you are mutating the passed in value outside the func as well.

```go
var thing1 = [5]float64{1,2,3,4,5}

func square(thing2 [5]float64) [5]float64{
    // thing2 will be a COPY of whatever slice is passed in
}
```

- You can use pointers to save memory if needed.

```go
var thing1 = [5]float64{1,2,3,4,5}

// make the func take in a pointer using * symbol instead
func square(thing2 *[5]float64) [5]float64{
    // thing2 will be the same memory location as thing1 passed in
    // no copy of the passed in slice is made.
}
```

## Goroutines

- A way to launch multiple functions concurrently

### Concurrency

- Concurrency != parallelization (Parallel execution is a form of concurrency)
- Concurrency means multiple tasks in progress at the same time
- Two ways to achieve Concurrency:
  - Jump back and forth between tasks (not more than one running simultaneously)
  - Parallel execution (more than one task running simulatneously - using cpu cores etc)
- Using goroutines can achieve some level of parallel execution if you have multiple cpu cores.

### Use the go keyword

- Run calls concurrently with `go`

```go
	for i:=0; i<len(dbData); i++ {
        // using go in front of a function call will run in parallel/concurrently
		go dbCall(i)
	}
```

- Note that the program will exit or loop will complete immediately as these processes are spawned in the background and run - it will not wait.
  - So we need a way to wait for these spawned calls to finish:

### Use wait groups to wait for tasks to complete

- If using go and concurrent runs, use the wait groups from the sync package to wait for tasks to complete so you can do something afterwards.
- Wait groups are simple counters - whenever you spawn a new goroutine you add 1 to the counter

```go
import "sync"

// create a wait group:
var wg = sync.WaitGroup()

func main() {
    var dbData = []string{"a","b","c"}

    for i:=0; i<len(dbData); i++ {
        // add one to the waitgroup counter
        wg.Add(1)
        // goroutines:
        go dbCall(i)
    }
    // call the wait method on the wait group to wait for the counter to go back to zero
    wg.Wait()
    fmt.Println("Executed calls") // will print after all calls executed
}

// Call done in the goroutine called method:
func dbCall(i int) {
    // ... do stuff
    // call done on the waitgroup at the end:
    wg.Done() // decrements the counter
}
```

### Using a mutex to control writing to the same space from multiple threads

- Use the sync package to create a mutex
- Allows you to safely modify the same slice, for example, when multiple threads are writing to it as above in a goroutine.
- Mutex is short for Mutual Exclusion
  - main methods are `m.Lock()` and `m.Unlock()`
- A goroutine will wait for a lock to be released if set on a memory space, and then set the lock to itself until it's done and then will release it.
- Be careful about where you place the lock as it can negate the concurrency benefits. see [video](https://www.youtube.com/watch?v=8uiZC0l4Ajw&t=2574s) at timestamp 44:15

```go
import "sync"

// create a wait group:
var wg = sync.WaitGroup()

// collection to store results from concurrent calls in goroutine
var results = []string{}

func main() {
    var dbData = []string{"a","b","c"}

    //

    for i:=0; i<len(dbData); i++ {
        wg.Add(1)
        go dbCall(i)
    }

    wg.Wait()
    fmt.Println("Executed calls") // will print after all calls executed
}

// Call done in the goroutine called method:
func dbCall(i int) {
    // ... do stuff

    // use a mutex to safely write to the results slice when multiple threads operating on it:
    // without this and just modifying results will lead to unexpected results/missing data etc.
    m.Lock()
    results = append(results, dbData[i])
    m.Unlock()

    wg.Done() // decrements the counter
}
```

### ReadWrite Mutex

- The standard mutex locks out other goroutines from accessing the memory space.
  - With a regular mutex lock even reads can only happen one at a time
  - With a read write mutex multiple concurrent reads can happen as long as the space isn't being written to.
- If needed you can use a read write mutex to allow for this.
  - `m.RLock()` and `m.RUnlock()` for example.
- Many goroutines can hold a read lock at the same time (this will block writes to the data)
  - The full mutex lock will prevent other reading or writing while it is in place.

```go
var results = []string{}

func main() {
    var dbData = []string{"a","b","c"}

    for i:=0; i<len(dbData); i++ {
        wg.Add(1)
        go dbCall(i) // parallel/concurrently execute
    }
    wg.Wait()
    fmt.Println("Executed calls") // will print after all calls executed
}

func dbCall(i int) {
    // ... do stuff

    save(dbData[i])
    log()

    wg.Done() // decrements the counter
}

// Example: make separate functions to read and write to a slice
func save(result string) {
    m.Lock()
    results = append(results, result)
    m.Unlock
}

// use a read lock and unlock to read results:
func log() {
    // this is a read lock and will wait if a full lock is held on results so we don't read while it's being written to.
    // this gorouting will acquire a read lock if no lock exists and proceed
    m.RLock()
    fmt.Printf("The current results are: %v", results)
    m.RUnlock()
}
```

#### Note on concurrency

- If your computation is expensive and not involving something like a external db call, then the performance increase is directly related to the number of cores you have on the machine.

## Channels

- Enable goroutines to pass around information
- Channels
  - hold data
  - are thread safe (no race conditions when reading/writing)
  - can listen when data is added or removed from a channel and block execution until one of those happens.
- Channels can be thought of as arrays. Some channels are unbuffered which means they can only contain one value.
  - NOTE: when writing to unbuffered channel, the code will block until something else reads from it - can cause deadlocks
    - Need to use channels with goroutines

```go
func main() {
    // make a channel - use the chan keyword and specify the type it can hold
    var c = make(chan int) // this is an unbuffered channel with one value

    // add a val to a channel
    c <- 1 // adds 1 to the channel - this is an unbuffered channel with room for only one value.

    //retrieve the val from a channel:
    var i = <- c // pops the val from the channel i is now = 1

    // we can't print or use anything here as a deadlock will occur. 
    // Channels need to be used with goroutines (see below)
}
```

### Using Channels with Goroutines
```go
func main() {
    var c = make(chan int) // this is an unbuffered channel with one value

    // use the func as a goroutine and then you can print
    go process(c) // sets a val to the channel

    // the execution will pause here until a value is set in the channel
    fmt.Println(<-c) // print the retreived val from the channel - no deadlock
}

func process(c chan int) {
    c <- 123 // add the val to the channel passed in
}
```

### using Channels in a loop
- Use the range keyword
- In the below example, for each iteration in the loop the value is added to a channel and printed at the same time/concurrently
  - goroutine called
  - for loop in main starts
  - goroutine func adds a value to the channel in first iteration and waits
  - loop in main continues when first val added and reads it
  - goroutine process continues to next loop after the read is complete
  - ...repeat cycle... to end of loop
  - At the end of the process you need to CLOSE THE CHANNEL! otherwise a deadlock will occur.
    - After iterating through all vals, the main function will go back to the top of the loop to wait for another value. We need to close the channel to stop this.
```go
func main() {
    var c = make(chan int)

    // start goroutine
    go process(c)

    for i:= range c {
        // at each loop we wait for something to be added to the channel (in process())
        fmt.Println(i)
    }
}

func process(c chan int) {
    // use defer to close channel right before the function exits
    defer close(c)

    for i:=0; i<5; i++ {
        // add a value which allows main func to read from the channel and wait for the read to complete before continuing to next iteration 
        c <- i
    }
}
```

### Using Buffer Channels (more than one val)
- Channels with more than one value (as in a unbuffered channel)
- 
50:52