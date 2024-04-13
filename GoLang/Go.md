# GoLang

- [Go Basics Video](https://www.youtube.com/watch?v=8uiZC0l4Ajw)
- [Go API - Basic Example](https://github.com/BrentGrammer/go-api)
- See [How to Write Go Code](https://go.dev/doc/code)

## Sub topics:

- [Channels](./Channels.md)
- [Collections](./Collections.md)
- [Control Flow](./ControlFlow.md)
- [Functions](./Functions.md)
- [Generics](./Generics.md)
- [Goroutines/Concurrency](./GoroutinesConcurrency.md)
- [Interfaces](./Interfaces.md)
- [Loops](./Loops.md)
- [Numbers](./Numbers.md)
- [Packages and Modules](./PackagesModules.md)
- [Pointers](./Pointers.md)
- [Basic REST API](./RestAPI.md)
- [Strings](./Strings.md)
- [Structs](./Structs.md)
- [Variables](./Variables.md)

### Project Structure:

- See [example of how to structure go app](https://github.com/golang-standards/project-layout)

### Main syntax notes:

- typing syntax:
  - brackets BEFORE the type name for list types: `[]int`
  - type comes after name: `var myVar int`
  - arrays declared with {} instead of []: `var slice = []int32{1,2,3}`
- Variables
  - use `var` or `const` keywords to declare followed by optional type: `var myString string = 'string'`
    - Note: if you leave out the type then type is inferred.
  - Use inference operator to infer type: `:=` - omit var keyword if using
- loops
  - No parens around the condition: `for x == y {}`
  - use range keyword: `for i, v := range myList {}`
  - traditional for: `for i:=10; i<10; i++ {}`
- Strings:
  - Need to use double quotes `"` for strings
  - Single quotes `'` are used for Runes (can only put one char in them 'a')
  - Back ticks are for string literals: \``This will print \n the backslash with n`\`
  - Avoid using `len(str)` to get the length of a string (returns number of bytes)
    - use `utf8.RuneCountInString(myStr)`
- Lists (slices)
  - Appending to a list: `append(myList, item)`
- Maps
  - use "comma ok" syntax to check the value:
  ```go
  // inline with if statement defining a var you can use for the check. Vars are scoped to the if block
  if seconds, ok := timeZone[tz]; ok {
    return seconds
  }
  log.Println("unknown tz:", tz)
  ```
- Trailing commas required in structs:
  - You cannot leave off a trailing comma on the last field definition for a struct literal for example. This will result in syntax errors.
- Public exportable methods
  - Use a capital letter to make functions importable in other packages: `MyPublicFunc()...` vs. `myPrivateFunc()...`

### Importing

- One of the heuristics to determine if it should look for a local package vs an external module package is the presence of dot in the import path. If the import starts with github.com, it is considered a module. ??
- Prefix imports of local packages using the string you chose with `go mod init {thisstring}`: `github.com/myname/path/mylocalpackage`

### Mod file

- Dependencies and versions are listed in the `go.mod` file
- `go init my-app` creates mod file
- `go get {package-name}` installs a package
- `go mod tidy` - [use to install standard packages imported in main.go](https://go.dev/ref/mod#go-mod-tidy)
  - go mod tidy ensures that the go.mod file matches the source code in the module. It adds any missing module requirements necessary to build the current module’s packages and dependencies, and it removes requirements on modules that don’t provide any relevant packages. It also adds any missing entries to go.sum and removes unnecessary entries.

## Running a go program

- `go run path/to/main.go`
- This compiles and executes the file in one step (no build or binary produced)

## Building a binary:

- `go build path/to/main.go`
- This produces a binary file (i.e. `main`) that you can run with
  - `./main`

### Default Types:

- ints/numbers/floats/rune = 0
- Booleans = false
- Strings = '' (empty string)
- error = nil

### Booleans

- `var myBoolean bool = false`
