# Collections (Slice, Arrays, Maps etc) in GoLang

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
