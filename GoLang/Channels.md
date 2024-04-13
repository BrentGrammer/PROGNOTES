# Channels in GoLang

- The primary purpose of channels is to communicate between different go routines
  - Note: the main() function is a go routine as well

## Channels

- Channels are primitives that can be passed around
- Channels are typed in that they specify what type of information is shared in them.
- Function as FIFO queues
- Enable goroutines to pass around information
- Channels
  - hold data
  - are thread safe (no race conditions when reading/writing)
  - can listen when data is added or removed from a channel and block execution until one of those happens.
- Channels can be thought of as arrays. Some channels are unbuffered which means they can only contain one value.
  - NOTE: when writing to unbuffered channel, the code will block until something else reads from it - can cause deadlocks
    - Need to use channels with goroutines

### Creating a channel:

```go
func main() {
    // make a channel - use the make built in function with the chan keyword and specify the type it can hold
    var c = make(chan int) // this is an unbuffered channel with one value

    // add a val to a channel
    c <- 1 // adds 1 to the channel - this is an unbuffered channel with room for only one value.

    //retrieve the val from a channel:
    var i = <- c // pops the val from the channel i is now = 1

    // we can't print or use anything here as a deadlock will occur.
    // Channels need to be used with goroutines (see below)
}
```

### Syntax for Channels

- Send a value to a channel: `channel <- 5`
- Wait for a value to be sent to a channel and get it: `valFromChan <- channel`
  - NOTE: this is a blocking call!
- Watch and use vals from a channel as an argument to func: `fmt.Println(<- channel)`

### Using Channels with Goroutines

- to use a channel with a go routine you need to pass it in as an argument
- The go routine can use the channel to communicate with the parent function where it is defined, for example.

```go
func main() {
    var c = make(chan int) // this is an unbuffered channel with one value

    // use the func as a goroutine and then you can print
    go process(c) // sets a val to the channel

    // the execution will pause here until a value is set in the channel
    fmt.Println(<-c) // print the retreived val from the channel - no deadlock
}

// pass in the channel to the go routine and indicate the type of data for it
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

    // reading from a channel is blocking, so we need to close the channel to prevent hanging in process() since we do not specify a specific number of times to loop (and using an unbuffered channel)
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

#### Example with a for loop in the parent:

```go
func main() {
     var links = []string{"google.com","stackoverflow.com","amazon.com"}

     c := make(chan string)

     for _, link := range links {
        go checkLink(link, c)
     }

     // regular for loop to wait for channel messages expected
     for i := 0; i < len(links); i++ {
        fmt.Println(<- c) // this is a blocking call and will wait for something to be added and read from the channel
     }
}

func checkLink(link string, c chan string) {
    _, err := http.Get(link)
    if err != nil {
        log.Error("Error")
        c <- "Error" // put on channel
        return
    }

    c <- "Link is working" // add message to channel
}
```

### infinite loop process using channels

```go
func main() {
     var links = []string{"google.com","stackoverflow.com","amazon.com"}

     c := make(chan string)

     for _, link := range links {
        go checkLink(link, c)
     }

     for  {
        // because channel holds type string, you can pass it as a string to the function
        // note that the `<-c` is blocking until a value is found/inserted in the channel
        go checkLink(<-c, c)
     }

     // alternative syntax for above is to use the range loop:
       // wait for the channel to return some value and assign it to the variable `link`
     for link := range c { // easier to see as a developer instead of burying a <- in the code to show it's blocking on a channel read.
        go checkLink(link, c)
     }
}

func checkLink(link string, c chan string) {
    _, err := http.Get(link)
    if err != nil {
        log.Error("Error")
        c <- link // add the link to the channel
        return
    }

    c <- link // put link on channel
}
```

## Using Buffer Channels (more than one val)

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

## Best Practices
- Do not reference the same variable (in memory) in two different go routines
   - Go is a 'pass by value' language, so leverage this to pass copies of data into go routines from the containing or upper scope
   - Alternatively only communicate or share data via channels between go routines

```go
links := []string{"facebook.com","google.com","stackoverflow.com"}

for _, link := range links {
    go checkLink(link, c)
}

for l := range c {
    // immediately invoked function literal
    go func(){
        checkLink(l, c)
    }()
}
// This results in the three links being processed as expected and then only one link processed over and over in the for loop for the channel because `l` changes by the time checkLinks run to the last `l` (similar to how a closure in a for loop will just print the last i):
for i := 0; i < 5; i++ {
    go func() {
        fmt.Println(i)
    }()
}
// prints 5 5 5 5 5
```
- We can fix this problem by passing in a variable so that it is copied by value and remains stable:
```go
for l := range c {
    go func(link string){
        checkLink(link, c) // pass in the argument, not l in the upper scope
    }(l) // l will be copied and used instead of the changed l used when the go routine runs
}
```