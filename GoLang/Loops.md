# Loops in GoLang

### For Loops

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
