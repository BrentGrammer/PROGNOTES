# GoRoutines and Concurrency

## Goroutines

- A way to launch multiple functions concurrently

### Concurrency

- GoLang uses the Fork-Join model for concurrency ([channels](./Channels.md) are used to join go routines back to a main func for example or communicate between concurrent go routines)
- Concurrency != parallelization (Parallel execution is a form of concurrency)
- Concurrency means multiple tasks in progress at the same time
- Two ways to achieve Concurrency:
  - Jump back and forth between tasks (not more than one running simultaneously)
  - Parallel execution (more than one task running simulatneously - using cpu cores etc)
- Using goroutines can achieve some level of parallel execution if you have multiple cpu cores.

### Go Scheduler

- Go Routines are managed by GoLang using the Go Scheduler
- The scheduler will monitor go routines and control their execution
  - When a blocking call such as an Http request is encountered, control will be released to another go routine to continue execution during the blocking call's work
  - If not blocking call is encountered, the currently running go routine will continue to execute until the end and then be exited to return control to another go routine to start/continue it's execution

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
