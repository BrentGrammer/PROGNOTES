# Channels in GoLang

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
    // Need to close the channel when done to notify other parts of the app using it
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
- 51:20 timestamp has a more elaborate example of using channels

```go
import (
    "fmt"
    "time"
)

func main() {
    var c = make(chan int, 5) // Can store multiple values - 5 ints in this channel
    // with a regular channel the process function will stay active until the main is done working
    // with buffered channels it can quickly add 5 values and immediately exit, it does not have to wait for the main func to pop out the value to make room for the next one.
    // this allows the process function to add values

    go process(c)

    for i:= range c {
        fmt.Println(i)
        // do some work before printing the value
        time.Sleep(time.Seconds+1)
    }
}

func process(c chan int) {
    defer close(c)

    for i:=0; i<5; i++ {
        c <- i
    }
}
```
