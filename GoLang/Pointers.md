# Pointers in GoLang

- A special type that stores a memory address
- `*`
  - When used on the left side of assignment operator, represents and gets the memory address: `var p *int32 = new(int32)` or `*p = 10` (the value 10 is stored at the mem addr p points to)
  - When used on the right side of the assignment operator, represents de-referencing a value: `var myVar string = *myStrPtr` (assigns the value at the myStrPtr mem addr to myVar)
  - When passed in as a parameter to a func, represents a pointer (mem addr)
  - When not assigning or as a param, it is a dereferencing and accesses the value: `fmt.Println(*p)`
- `&`
  - Used to get the memory address for a pointer or variable: `p = &i`

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
