# CLEAN ARCHITECTURE (Bob Martin)

- example with code: https://fullstackmark.com/post/11/better-software-design-with-clean-architecture
- full implementation example: http://www.plainionist.net/Implementing-Clean-Architecture-Overview/

The goal of clean architecture is to minimize resources needed for building and maintaining software.

The basic idea is very simple. You separate the UI from the business rules by passing simple data structures between the two. You don’t let your controllers know anything about the business rules. Instead, the controllers unpack the HttpRequest object into a simple vanilla data structure, and then pass that data structure to an interactor object that implements the use case by invoking business objects. The interactor then gathers the response data into another vanilla data structure and passes it back to the UI. The views do not know about the business objects. They just look in that data structure and present the response.

It is more important to have software that is easy to change than software that works.
Logical way of reasoning: looking at the extremes:
If a program works but is impossible to change, it becomes useless
If a program does not work but it's easy to change, you can change it to make it work and adhere to future change requirements.

Software is more like science than math. You cannot prove a program is correct. You can only prove it is incorrect (it is falsifiable) by using the scientific method via tests.
This is only possible if your is testable and made up of components you can in tests (argument for TDD)

Paradigms (3) of programming
Structured - if then else replaces goto, discipline on control flow
Object oriented - inheritance, polymorphism, encapsulation
Functional - discipline of assignment (immutability)

OO:
Polymorphism: pointers to functions (ex a vtable holding virtual functions)

Example on Linux: every io operation must implement functions: open close seek read ??

Inheritance: simply the redeclaration of member variables.

Programs should be device independent
Device is plug

End of track 9 **\*** listen to this again

Interfaces
Whole point is to control dependency flow

Functional programming:

Primary advantage is it avoids concurrency problems like deadlocks and races conditions since no variable should change.
Requires infinite processing and storage,it is only practical within limits.

Track 23 defer examples

Low level policies should function as plugins to high level policies.
What defines a high level policy is how far away from inputs and outputs the policy is.
Ex: readchar, writechar, translate -> translate is the high level policy because it is furthest from inputs and outputs,unlike read and writechar.
Good examples in ch 25.

Entities/models are high level policies. They should not depend on anything and be plain old objects.
\*\*\*\*Your system should be testable without needing a database, UI or framework. You should be able to unit test the business rules and use cases.
Use cases are a path that a user would take in the system.
Business rules should be the most independent and reusable code.
Business rules are lower level than entities but still high level relatively.
Business rules are what the business needs to make money, esp critical business rules.
The architecture of a system should scream what the system is not what framework it uses. Folders and files should obviously indicate it is a healthcare system or an accounting system etc.
Review track 28 or 27.

Good architecture is divided into layers:
Entities
Business rules
Database
Ui
\*From high level at top to low level at bottom

Track 28
Entities can be data classes or have functions. There are the high level inner circle and no change in the application should affect

Use cases orchestrate the flow of data to and from the entities. We don't expect changes to this layer to affect the entities.
Changes to the function of the application will affect this layer.
Use case classes are typically suffixed with the word Interactor.

One key aspect of the request/response messages that flow in and out of use case interactors and across boundaries is that they are simple data structures meaning they contain no special types: ie. entities, or types provided by 3rd party libs etc. - they are pure C# objects.

Interfaces adapter layer, concrete format from data in the use cases to use in other layers, I.e. the database. Controllers etc.
use of \_authService, \_studentRepository and \_courseRepository in the Interactor/Use Case. These services are typically referred to as Gateways within clean architecture and get injected into the Use Case layer as per the dependency rule. These are the things that deal with the database, rest services or other external agencies and their implementation belongs in the Interface Adapters layer. Interactors only know what behavior these gateways offer by way of their interface definition. They have no idea how they do their work because those details are encapsulated in an outer layer which the Use Cases know nothing about.

Next layer is frameworks and tools, like the database and drivers.

Presenter layer - Ui

Source. Code dependencies always move inwards to the higher level policy

Example of Boundary:
There's embedded software in your mouse that communicates with your operating system. Yet the details are hidden from your applications. Your spreadsheet accepts standardized input without knowing or caring what kind of mouse you are using. Then when someone invents a new input device like the touchpad it works with your spreadsheet automatically.
That's just one of the boundaries in your computer (between the spreadsheet application and the input device that delivers info to it).

- you might also want to save it to disk, save it to PDF, save it as a CSV, or print it. So, maybe one of the boundaries in your spreadsheet program is to have an internal data structure that represents each spreadsheet. And then you pass that structure to different code to display, save, or print it in the desired format.
  If you keep the data structure completely unaware of how it is displayed, saved, or printed, then you can add a "save to XML" feature down the road without digging through all the code related to the spreadsheet data structure

Crossing boundaries means using dependency inversion.
I.e. use cases calling the presenter - must not be direct, the use case calls an interface in the inner circle and have the presenter in the outer circle implement it.
The higher level policy cannot mention the name of the lower level in it.

Interfaces are implemented by lower level users and owned by higher level component being used

Humble objects and boundaries, track 31 or 30, review

Main is the lowest level component, should be thought of as a plug in to the system ? Track 33

Micro services decoupling fallacy - services can actually be coupled through shared data. If the schema changes then the multiple services consuming it need to be rebuilt.

Buffer: a slice of memory (ram) that holds data which you can manipulate or use temporarily.

Firmware: you need a hardware access layer to separate business logic from low level hardware details.

Basic operations of a component:
Accept input
Process input
Produce output

Types of architecture approaches:
Horizontally layered (web,business logic, data layers)

- not recommended though you may start with this, see later chapter on why bad as application grows. More needs to be made public

Layer by feature, also not ideal and has problems

Package by component - similar to layer by feature and recommended by bob Martin. The difference is that dependencies are carefully separated accord to dependency rule and decoupling is carefully adhered to.

\*\*\*\*Program against polymorphic interfaces.
Hide low level details.
With frameworks, defer decision on which to use as long as possible before commiting. You are married to the framework and life of app is tied to it.
