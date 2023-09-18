# CLEAN ARCHITECTURE (Bob Martin)

- example with code: https://fullstackmark.com/post/11/better-software-design-with-clean-architecture
- full implementation example: http://www.plainionist.net/Implementing-Clean-Architecture-Overview/
- https://www.youtube.com/watch?v=1IE8RC-IOSE

The goal of clean architecture is to minimize resources needed for building and maintaining software.

The basic idea is very simple. You separate the UI from the business rules by passing simple data structures between the two. You don’t let your controllers know anything about the business rules. Instead, the controllers unpack the HttpRequest object into a simple vanilla data structure, and then pass that data structure to an interactor object that implements the use case by invoking business objects. The interactor then gathers the response data into another vanilla data structure and passes it back to the UI. The views do not know about the business objects. They just look in that data structure and present the response.

It is more important to have software that is easy to change than software that works.
Logical way of reasoning: looking at the extremes:
If a program works but is impossible to change, it becomes useless
If a program does not work but it's easy to change, you can change it to make it work and adhere to future change requirements.

Software is more like science than math. You cannot prove a program is correct. You can only prove it is incorrect (it is falsifiable) by using the scientific method via tests.
This is only possible if your is testable and made up of components you can in tests (argument for TDD)

### Paradigms (3) of programming

- Structured - if then else replaces goto, discipline on control flow
- Object oriented - discipline of indirect transfer of control
- Functional - discipline of assignment (immutability)

### OOP

- **OO design is the ability through the use of polymorphism to gain absolute control over every source code dependency in the system**
  - Allows for _plugin architecture_ where modules with high level policies are independent of modules with low level details
  - Low level details are relegated to plugin modules that can be deployed and maintained independently from high level policy modules
- imposes discipline on indirect transfer of control
- the combination of data and function, or modeling the real world are inacurrate
- Nygard 1966 moved the function call stack frame to the heap and invented OO design
- Encapsulation: a line can be drawn around data/functions, outside of that line the data is hidden and only some functions are known (public)
- Inheritance: The redeclaration of variables and functions within a given scope

### Polymorphism:

- Ex: UNIX requires every I\O driver provide 5 standard functions: open, close, read, write and seek
  - the signature of those must be identical for every driver
  - the file data structure contains 5 pointers for those functions, the driver loads a file data structure with addresses for each of the functions
    - if STDIN is defined as a file and if it points to the console (input dev.) data structure, then getChar() might be implemented by calling the function pointed to by the read pointer of the file data structure pointed to by STDIN. This trick is the basis of all polymorphism
  - Polymorphism is an application of pointers to functions
  - There is no need to recompile source code that conforms to the interface. This enables so that the source code calling the interface does not depend on the source code on the other side of the interface.

#### Plugin Architecture

- Originally created to support input output device independence

#### Dependency Inversion

- Polymorphism allows for a high level to call a function in a mid level function through an interface
  - w/o polymorphism, main level functions call high level funcctions which call mid level functions which call lower level functions and in that calling tree, source code dependencies follow the flow of control
    - The higher level caller needs to include/import/mention the name of the module that contains the callee (the lower level module being called). Dependencies are dictated by the flow of control
  - With polymorphism the high level can call the lower level through an interface (this is a source code contrivance) - at runtime the interface does not exist, the high level function calls the mid level function indirectly without any source code dependency between the two.
    - The interface functions as a kind of "pointer" to the actual function, so the functionality is polymorphic (the function being pointed to can change and take other forms)
      - The address pointed to in the interface can change as needed and as it is implemented by modules
  - Note: the source code dependency (the inheritance relationship) between the mid level function and the interface, points from the mid level function to the interface, in other words in the opposite direction of the flow of control (against the direction of the higher level to the lower level)

### Interfaces

- Whole point is to control dependency flow.
- Higher level component defines an interface, and the lower level component implements that interface
- No matter what module is calling another module, the software architect can use interfaces to point the dependency in either direction via an interface
- This is what OO is all about from an architect's point of view: re-arranging the source code dependencies so that the db and the UI depend on the business rules rather than the other way around
  - the UI and the db can be plugins to the business rules
  - The source code of the business rules never mentions the UI or the db and can be separated into 3 separate deployable components
  - The business rules will not depend on the UI or db

### Independent deployability and developability

- If the modules can be deployed individually without requiring the compiling of the other modules (no source code dependency), then you can develop them independently

### Functional programming:

Primary advantage is it avoids concurrency problems like deadlocks and races conditions since no variable should change.
Requires infinite processing and storage,it is only practical within limits.

Track 23 defer examples

Low level policies should function as plugins to high level policies.
What defines a high level policy is how far away from inputs and outputs the policy is.
Ex: readchar, writechar, translate -> translate is the high level policy because it is furthest from inputs and outputs,unlike read and writechar.
Good examples in ch 25.

Entities/models are high level policies. They should not depend on anything and be plain old objects.
**Your system should be testable without needing a database, UI or framework. You should be able to unit test the business rules and use cases.**
Use cases are a path that a user would take in the system.
Business rules should be the most independent and reusable code.
Business rules are lower level than entities but still high level relatively.
Business rules are what the business needs to make money, esp critical business rules.
The architecture of a system should scream what the system is not what framework it uses. Folders and files should obviously indicate it is a healthcare system or an accounting system etc.
Review track 28 or 27.

### Good architecture is divided into layers:

\*From high level at the top to low level at the bottom

1. Entities
1. Business rules
1. Database
1. UI

#### Entities

Track 28

Entities can be data classes or have functions. There are at the high level inner circle in the architecture layer and no change in the application should affect them.

#### Use Cases

Use cases orchestrate the flow of data to and from the entities. We don't expect changes to this layer to affect the entities.
Changes to the function of the application will affect this layer.
Use case classes are typically suffixed with the word Interactor.

One key aspect of the request/response messages that flow in and out of use case interactors and across boundaries is that they are simple data structures meaning they contain no special types: ie. entities, or types provided by 3rd party libs etc. - they are pure C# objects.

#### Interfaces/Adapter Layer

- concrete format from data in the use cases to use in other layers, I.e. the database. Controllers etc.
  use of \_authService, \_studentRepository and \_courseRepository in the Interactor/Use Case. These services are typically referred to as Gateways within clean architecture and get injected into the Use Case layer as per the dependency rule. These are the things that deal with the database, rest services or other external agencies and their implementation belongs in the Interface Adapters layer. Interactors only know what behavior these gateways offer by way of their interface definition. They have no idea how they do their work because those details are encapsulated in an outer layer which the Use Cases know nothing about.
- we definitively do not want any DI framework specific code anywhere in the inner circles, not in the entities, not in the interactors and even not in the adapters!

#### Frameworks and tools layer

- like the database and drivers.
- Do not marry frameworks if possible and try to keep them at arms length. Keep framework specific code out of inner circles of the architecture
- **The database does not contain business objects, but it contains concrete data structures**. The boundary between the application and database should be crossed by inserting a layer which will depend on the db and translate the data structures into business objects for the application.
  - The layer should depend on the database and it should depend on the application. The Application being abstract should not depend on the layer.

#### Presenter layer - Ui

Source Code dependencies always move inwards to the higher level policy.

### Humble objects and boundaries

track 30 (partial boundaries)

track 31

- Use boundaries to isolate parts of the system based on their axis of change

  - i.e. a Game UI that can display different languages: language is not the only axis of change for a UI, we might want to vary the mechanism by which the text is communicated as well, for example a shell, text window or chat app.
    - The are different architectural boundaries defined by these axes of change (i.e. the display mechanism or the language displayed)
    - Might want to construct an API that crosses a boundary and isolates the specific language components from the specific communication mechanism components
      - the Language API could be implemented by English and Spanish components
      - the Text Delivery (communication) API is implemented by the SMSN Console component - This is dependent on the language API
      - the Data Storage API is implemented by Flash or Cloud data components
    - All three of these APIs would be dependent on Game Rules (business entities/logic at the highest level of the architecture)
    - Game rules communicates with Language through an API that Game Rules defines and Language implements
    - Language communicates with Text Delivery using an API which Language defines, but Text Delivery implements
  - **The API is defined and owned by the user rather than by the implementor** (the higher level defines the contract/what can be called by lower levels and the lower level specifies contract details/implementation it uses to call that contract)
    - Ex: In Game Rules we would find polymorphic boundary interfaces used by the code inside Game Rules and implemented by the code inside the Language Component
      - would also find polymorphic boundary interfaces used by Language and implemented by code inside Game Rules
    - The API defined by the boundary interfaces is owned by the Upstream component
      - Ex: we would expect polymorphic interfaces defined in the Language API to be implemented by the English and Spanish components
  - Game Rules would control streams of data (i.e. from the user input to data persistence, and from data persistence back to the user for the output)

- Note: boundaries are expensive and must be decided and placed with care, but they are extremely expensive to add in later and difficult to predict where they are needed precisely
- An architect must decide where boundaries are fully needed, where partial boundaries should be used or whether boundaries should be ignored completely (YAGNI).
  - As the system develops watch carefully for first signs where friction starts to reveal itself where a boundary may be needed. Weigh the cost of implementing a boundary or ignoring and review that decision frequently. goal is to implement at the inflection point where cost of implementing becomes less than the cost of ignoring.

#### Example of Boundary:

There's embedded software in your mouse that communicates with your operating system. Yet the details are hidden from your applications. Your spreadsheet accepts standardized input without knowing or caring what kind of mouse you are using. Then when someone invents a new input device like the touchpad it works with your spreadsheet automatically.
That's just one of the boundaries in your computer (between the spreadsheet application and the input device that delivers info to it).

- you might also want to save it to disk, save it to PDF, save it as a CSV, or print it. So, maybe one of the boundaries in your spreadsheet program is to have an internal data structure that represents each spreadsheet. And then you pass that structure to different code to display, save, or print it in the desired format.
  If you keep the data structure completely unaware of how it is displayed, saved, or printed, then you can add a "save to XML" feature down the road without digging through all the code related to the spreadsheet data structure

Crossing boundaries means using dependency inversion.
I.e. use cases calling the presenter - must not be direct, the use case calls an interface in the inner circle and have the presenter in the outer circle implement it.
The higher level policy cannot mention the name of the lower level in it.

Interfaces are implemented by lower level users and owned by higher level component being used.

### Services

- Services do not define an architecture. An architecture is defined by boundaries that separate components and follow the dependency rule.
- Boundaries cross through the services dividing them into components. Services must be designed with component architecture following the dependency rule. The components within the service define the architectural boundaries (not the separate services themselves)
- Main is the lowest level component, should be thought of as a plug in to the system ? Track 33

### Microservices

#### Micro services decoupling fallacy

- services can actually be coupled through shared data or shared resources on a processor or network. If the schema changes then the multiple services consuming it need to be rebuilt.
- services are only decoupled at the level of individual variables
- If a field is added to a data record that is passed between services, then every service that operates on the new field must be changed and must strongly agree about the interpretation of the data in that field. This makes them highly coupled.

Buffer: a slice of memory (ram) that holds data which you can manipulate or use temporarily.

Firmware: you need a hardware access layer to separate business logic from low level hardware details.

### Basic operations of a component:

1. Accept input
1. Process input
1. Produce output

### Types of architecture approaches:

- Horizontally layered (web,business logic, data layers)

  - not recommended though you may start with this, see later chapter on why bad as application grows. More needs to be made public

- Layer by feature, also not ideal and has problems

- Package by component - similar to layer by feature and recommended by bob Martin. The difference is that dependencies are carefully separated accord to dependency rule and decoupling is carefully adhered to.

**Program against polymorphic interfaces.**
Hide low level details.
With frameworks, defer decision on which to use as long as possible before commiting. You are married to the framework and life of app is tied to it.
