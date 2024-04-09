# Control Flow

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

- Note: `select` statements are used with channels/concurrency
