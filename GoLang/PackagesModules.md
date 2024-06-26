# Packages and Modules

### Packages

- Folder with a collection of .go files
- Variables and code can be package scoped (variables declared at the package scope in one file are accessible in other files in the same package)
- Convention is to have one main file for the package that matches the name of the package (other files in the same package can be named differently)

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

### Capitalizing methods means they are public!

- If you capitalize the first letter of a function name in a package, it can be imported by other packages/modules
- If you start it with a lowercase name, then it is private and cannot be imported outside the package.

### Importing packages

- Use fully qualified name for importing internal or local packages you created in the app:
  - ex: `"github.com/BrentGrammer/goapi/api"`
  - This was created when running go mod init: example: `go mod init github.com/BrentGrammer/goapi`
- see path to import internal packages from using `cat go.mod`
