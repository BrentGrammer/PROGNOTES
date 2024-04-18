# gRPC

- [grpc.io](https://grpc.io)
- Remote Procedure Call
- Popular with microservice communication in Go
- Uses Protocol Buffers to transfer code between client and server (request/responses)
- More complicated than working with JSON, but at scale having transparency on where the client and server runs and having a schema encoded within a message definition (more efficient) allows for services that are easier to work with and more maintainable.

## Protocol Buffers

- [See Documentation](https://protobuf.dev)
- A protocol for communicating between clients and servers (i.e. like XML or JSON are alternative protocols)
- At the time protocol buffers were created, the other protocols required having to include the schema for the data sent along with the data itself - this was inefficient.
  - Protocol Buffers attempted to solve this problem by:
    - Defining the schema before sending messages (the schema is not sent with the data and the client and server already know the schema)
- Messages are transmitted in a compressed format and as binary over the wire. (more efficient than the string based messages JSON uses for example)

```c
syntax = "proto3"; // define version (2 or 3 currently) - for future compatibility

package product; // package id for protocol buffer definition files comms
option go_package = "demo/productpb"; // options to control code generation for specific languages. our generated code will be in the package here "demo/productspb"
// message defines some data shape that can be sent across the protocol buffer
message Product {
    int32 id = 1; // nums are important-we send these identifiers, not the field names when the message is sent. this is field 1 repr the id.
    string name = 2;
    double usdPerUnit = 3;
    string unit = 4;
}
```

- After this configuration is defined we can use the [protoc compiler](https://protobuf.dev/downloads) to generate the code.

- When working with Go, we need an additional tool: the protoc-gen-go package: `go install google.golang.org/protobuf/cmd/protoc-gen-go@latest`
  - This package is needed and used by the protoc compiler when generating the source code.
- Generate code with protoc compiler:
  - `-I` is the include parameter to tell where the protocol buffer messages we are asking it to work with.
  - `-go_out` parameter defines where the source is rooted at
  - lastly specify the protocol buffer messages we want compiled into source code.
  - `protoc -I=. --go_out=. /product.proto`

## Installation

- [video](https://app.pluralsight.com/ilx/video-courses/afd2c488-1f4f-4398-9bef-db4050ea802a/3b4b3d66-135b-4e67-9689-9c17dbe0af2f/1e862259-7cc9-4c3f-8769-b04205d3f2f0)
- Go to [Protocol buffers repo](https://github.com/protocolbuffers/protobuf) to Current release and find the installer for your machine.
  - Go to their github page and download the binary for latest release. Place the binary file protoc in `/usr/local/bin` and the contents of include folder to `/usr/local/include`
  - After installing, test it with the command `protoc` in a terminal
- Install the go tool needed in a terminal: `go install google.golang.org/protobuf/cmd/protoc-gen-go@latest`
  - this is installed globally
  - We don't invoke this directly, but it is used by protoc to generate go code.

### Troubleshooting

- If you have a problem on mac with not allowing you to open or run protoc, [follow these steps](https://github.com/grpc/grpc-web/issues/650):
  Try to run "/usr/local/bin/protoc-gen-grpc-web --help" (or protoc --help)
  Click Cancel when notified about an unverified developer
  Go to Settings -> Security & Privacy -> General
  Click on Allow Anyway
  And it should work from now on, you will need to do this again the next time you update.

## Using gRPC

- [video demo](https://app.pluralsight.com/ilx/video-courses/afd2c488-1f4f-4398-9bef-db4050ea802a/3b4b3d66-135b-4e67-9689-9c17dbe0af2f/1e862259-7cc9-4c3f-8769-b04205d3f2f0)

### Creating a message type

- create a protocol buffer config/definition file using the `.proto` extension. Place the file directly above one level to the folder of the service you are making it for.
  - `product.proto`
- create the definition and config - use `proto3` for the syntax version which is the latest at this time and most common.

```c
syntax = "proto3"

package product; // package is required

option go_package = "productservvice/productpb"; // what package generated source code goes to. productservice is the folder the service using this is in.

message Product {
    int32 id = 1; // identifiers for each field must be unique
    string name = 2;
    double usdPerUnit = 3;
    string unit = 4;
}
```

### Generate go code from the proto config using the protoc tool

- Now use the protoc tool: `protoc -I=. --go_out=. product.proto`
  - The `go_out` param tell where the code is generated. Since we specified a package of productservice/productpb package in the config, it will install it in this case using the `.` to that folder, i.e. `./productservice/productpb` (IOW, it prepends the go_out path to the package we specified)
  - This will create a `productpb` folder underneath the existing `productservice` folder where our go source code is already and inside there will be a `product.pb.go` file created.

### Using the generated type in Go

- CD into the service or folder you are using the protocol message in (i.e. `productservice/`) and Install the protobuf package for go to Marshal and Unmarshal protocol buffer messages: `go get google.golang.org/protobuf`

```go
type Product struct{
    ID int
    Name string
    USDPerUnit float64
    Unit string
}

func main() {
    // use the package containing the created generated code and message struct
    p := productspb.Product{
        Id: int32(products[0].ID), // need to convert since message is int32 and the product record has int Id
        Name: products[0].Name,
        UsdPerUnit: products[0].USDPerUnit,
        Unit: products[0].Unit,
    }

    // Marshal into a protocol buffer using the protobuf package installed so we can send it across the network
    data, err := proto.Marshal(&p) // pass pointer to our message created above
    if err != nil{
        log.Fatal(err)
    }


    // Unmarshaling works as follows:
    var p2 productpb.Product // forward declare where we want to unmarshal to

    err = proto.Unmarshal(data, &p2) // pass in byte slice (data received from request) and a reference to where to unmarshal it to
    if err != nil{
        log.Fatal(err)
    }
    fmt.Printf("%+v", p2)
}
```

## Creating a gRPC service

- Requires another tool to generate service go code: go package needed to work with protoc to compile service code: `go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest`
  - Install this globally

### define the proto config for a service:

- create a file (or include this in an existing proto file) adjacent to the service folder in your source code (in this example adjacent to the `productservice/productpb` folder)

```c
// productservice.proto

syntax = "proto3";

package productService; // you can specify a different package (organization is based on this not the file location)

 // here we retrieve the definition of another proto file we made - the product we are working with
import "product.proto";

// where the generated code will live (the folder)
option go_package = "productservice/productpb";

// always need a request and response type - they are necessary as part of the protocol
message GetProductRequest {
    int32 productId = 1; // define fields and assign a identifier
}
message GetProductReply {
    product.Product product = 1; // the reply will return a product type we imported, assign an identifier
}
service Product {
    // here we use the type `rpc` instead of string or int etc., then specify a request and return type (created above)
    rpc GetProduct(GetProductRequest) returns (GetProductReply) {}
}
```

### Generate the go code

- Generate the service code with: `protoc -I=. --go_out=. --go-grpc_out=. ./product.proto ./productservice.proto`
  - tell the command at the end where to find your proto definition files you made. In this example it compiles the two proto files (service imports the product.proto)
  - imported code from product.proto will be in a new file called `productservice.pb.go` and the service code itself will be in a file called `productservice_grpc.pb.go`
- The go client code produced from this proto config follows this interface:

```go
type ProductClient interface {
  // takes in a go context and the request message type we defined in our proto definition file above (defines data we need to execute this command). opts are call options that are optional for flexible config
  GetProduct(ctx context.Context, in *GetProductRequest, opts ...grpc.CallOption) (*GetProductReply, error)
}
```

- This client is also implemented by the generated code, but we need to retrieve it by using a constructor function that was generated for us:

```go
// pass in a connection object that tells the client where to find the server to communicate with
client := NewProductClient({connection})
```

- On the server side, we do need to implement an interface:

```go
type ProductServer interface {
  GetProduct(context.Context, in *GetProductRequest) (*GetProductReply, error)
}
```

- After implementing this on our server we can receive requests from the client created earlier.

### Implementing the server

```go
//main.go

// Define a new type
// though we have no requirements for fields here, Go has a requirement that we embed a type that it creates for us
type ProductService struct {
  productpb.UnimplementedProductServer // required (can check the generated code to find this type if different name)
}

// now implement the interface
func(ps ProductService) GetProduct(ctx context.Context, req *productpb.GetProductRequest) (*productpb.GetProductReply, error) {
  // Now do your business logic here

  // if logic fails return error
  return nil, fmt.Errorf("Item not found with ID: %v", itemId)

  // NOTE: we call this method and return as if it is local, but gRPC will return this error to the client on the other end of the call.
}
```

### Start the server

- Multi step process for gRPC to setup the interface and networking - the server we implemented itself is just a type
- You can register a gRPC server to use a TCP port, or add it as an endpoint to an HTTP server.
- To create a gRPC server to host a service, you need to install a package to the project: `go get google.golang.org/grpc`

```go
// put everything in a func
func startGRPCServer() {
  // in this example we create the server to use a tcp port on localhost
  lis, err := net.Listen("tcp", "localhost:4001")
  if err != nil {
    log.Fatal(err)
  }

  // create the gRPC server that will host our service usig the grpc package
  grpcServer := grpc.NewServer()
  // register instance of our service within the grpc server
  // the generated go code contains a register server method on it you can use
  productpb.RegisterProductServer(grpcServer, &ProductService())
  // start listening on the TCP port
  log.Fatal(grpcServer.Serve(lis))
}
```

### The client needs to call the service

- Note: by default gRPC server expects to communicate over a secure network connection (TLS)
- Create a connection to the server
- Create a client and invoke the method on the client to send data to the server

```go
func callGRPCService() {
  // create a client that knows how to communicate with the grpc server

  // for demo purposes we can skip TLS requirement for secure connections
  opts := []grpc.DialOption{grpc.WithInsecure()}
  // dial to where the messages are sent to (destination - localhost:4001 here which is where the server is listening)
  conn, err := grpc.Dial("localhost:4001", opts...)
  if err!= nil {
    log.Fatal(err)
  }
  // remember to close the connection when done
  defer conn.Close()

  // now create a client - pass connection to the server, use the constructor generated for us
  client := productpb.NewProductClient(conn)

  res, err := client.GetProduct(context.TODO(), &productpb.GetProductRequest{ProductId: 3})
  if err != nil {
    log.Fatal(err)
  }

  fmt.Printf("%+v", res.Product)
}
```

### Start and call the grpc server

```go
//main.go

func main() {
  go startGRPCServer()

  time.Sleep(1 * time.Second)

  callGRPCService()
}
```
