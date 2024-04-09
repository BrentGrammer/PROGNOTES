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
