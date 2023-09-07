https://cleancoders.com/episode/clean-code-episode-18

Component Design Project

- Note: diagrams are usually drawn and made if at all after a lot fo the code is already written.
  - If you're making rules, then make them on something concrete like the code, otherwise the diagrams are like castles in the air.
  - Component level decisions should be made after the application is written, works and is tested so that they are based off of reality.

Side note: program against interfaces, put layers like the database behind interfaces and outside consumers utilize those and know nothing about the internals of the db layer for example.

- Payroll system

- the whole point of a component architecture is to enable indepentent deployability and independent developability

- ***Use cases are the most likely to change and least stable.

*problems of MVC 23:30:
  - you don't want controllers depending on use cases. or use cases depending on the view (every time you change the view you have to rebuild everything)
  - The views are really concrete and eveything depends upon them a lot (violation of the stable abstraction principle)
  - eliminating cycles is not enough, you want the components to be independently deployable


Good Design case:
assuming the project is in an active development state (close to common reuse and common closure principles, not the release reuse equivalence principle)

First question: Which of these classes change for similar reasons and which ones are closed against similar kinds of changes?

- Controllers have a many to one relationship with Use Cases (each use case can be called by many different controllers)

- Low level policies should depend on high level policies

- Moving classes between components will occur with refactoring as you develop systems. That is one of the goals of refactoring.

Goal:
- To have multiple components that are independently deployable and can be composed into many different kinds of systems
  - It may not be bad to have many components (dozens for example).If they are truly independent, they can be composed to allow for great flexibility of building systems.