# Make an API

- [Go API - Basic Example](https://github.com/BrentGrammer/go-api)

### Initialize app

- `go mod init github.com/yourname/appname`
- `mkdir api` create api folder
  - This is where parameters for specs and response types exist
  - You should put your yaml spec file here
- `mkdir cmd/api`
  - contains the `main.go` file
- `mkdir internal`
  - contains most of the code for the api
  - contains handlers in `internal/handlers/api.go`
  - contains middleware in `internal/middleware`
- create a `api.go` file in the `api` folder
  - write the parameters and responses of endpoints

### Grabbing URL params in request handler:

- Use Gorilla package to decode them

```go
	var params = api.CoinBalanceParams{} // struct is defined in api/api.go and represents the url parameters for this request

	// use gorilla package to decode
	var decoder *schema.Decoder = schema.NewDecoder()
	var error error
    // this grabs and decodes the parameters from the url and set it to the values in the params struct
	err = decoder.Decoder(&params,  r.URL.Query())
```

## net/http package

### Basic Mux Server using the net/http package:

```go
import (
  "fmt"
  "net/http"
)

func main() {
    // create a ServeMux server
    mux := http.NewServeMux()
    // create a handler with HandelFunc method
    mux.HandleFunc("/", helloWorld)

    err := http.ListenAndServe(":8080", mux)
    if err != nil {
        fmt.Println(err)
    }
}
// this is the signature for a handler - needs the response writer and pointer to Request
func helloWorld(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "Hello, World")
}
```

## Working with JSON

- using JSON allows us to conform to the Uniform Interface principle (data sent over the wire between systems should be a consistent format/interface i.e. JSON)
- Use the `encoding/json` package
- Marshal: Encoding to json - converts a struct into a JSON object that can be passed as a var to other functions for parsing or output.
- UnMarshal: Decoding from json to a Go Struct

### Marshaling vs. Encoding

- Marhaling/Unmarshaling specifically refer to encoding and decoding from a specifically textual format (like JSON)
- Encoding/Decoding is more general and refers to transforming data from/to textual or binary formats (i.e. protocol buffers).

### Example sending json response:

```go
func (app *application) healthcheck(w http.ResponseWriter, r *http.Request) {
	if (r.Method != http.MethodGet) {
		http.Error(w, http.StatusText(http.StatusMethodNotAllowed), http.StatusMethodNotAllowed)
	    return
	}

	data := map[string]string{
		"status": "available",
		"environment": app.config.env,
		"version": version,
	}

	// convert the map to JSON with Marshal
	js, err := json.Marshal(data)
	if err != nil {
		http.Error(w, http.StatusText(http.StatusInternalServerError), http.StatusInternalServerError)
		return
	}

	js = append(js, '\n') // just for formatting add a new line

	// set headers
	w.Header().Set("Content-Type", "application/json") // we need to do this for json since default header is set to plain text
	// now write to the response
	w.Write(js)
}
```

### JSON tags

- Used for converting the fields of a struct when Marshaling to JSON so that they conform to JSON standards (casing etc.)

### Reading Request Body

- use ioutil from the "io/ioutil" package

```go
import (
	"io/ioutil"
)

//...

// get the body of the request
body, err := ioutil.ReadAll(r.Body)
if err != nil {
	http.Error(w, http.StatusText(http.StatusBadRequest), http.StatusBadRequest)
	return
}
// we want to convert the body of the request to a go struct, pass in mem addr of the input struct to mutate it
err = json.Unmarshal(body, &input)
if err != nil {
	http.Error(w, http.StatusText(http.StatusBadRequest), http.StatusBadRequest)
	return
}
```

## Routing

- GET `/customers`: request for a single resource
- GET `/customers/`: request the customers collection (with ending slash)
