# Design Principles

## Program to an Interface, not an Implementation

- An "interface" does not literally mean a Java Interface, for example, it means a supertype in general of some sort.
  - This could be an abstract class or an Interface, etc.
- The declared type of the variables should be a supertype, usually an abstract class or interface, so that the objects assigned to those variables can be of any concrete implementation of the supertype, which means the class declaring them doesn’t have to know about the actual object types

```java
// BAD: programming to a concrete implementation:
Dog d = new Dog(); // Dog is a concrete implementation, forces us to code against it's implementation, it's specific methods, etc.
d.bark();

// GOOD: programming to an interface
// type the dog as a higher level Animal interface
Animal animal = new Dog(); // now we can use Animal's high level methods that function as a stable public API, separating implementation from the interface
animal.makeSound(); // allows for polymorphism to change behavior

// BETTER: no reference to a concrete implementation, just get the interface:
a = getAnimal(); // don't know if it is a dog or what concrete implementation is involved at runtime
a.makeSound(); // program against the interface, could be any animal at runtime
```

## Favor Composition over Inheritance

- Use HAS-a relationships instead of IS-a relationships between objects and classes.
  - Objects can have a certain behavior injected instead of inheriting it from a super class, for example.
    - see [Strategy Pattern](./CleanCoders-Strategy.md)

- Do NOT create and use an object in the same place.
  - Create the object outside of where it's used and pass the instance in as a dependency to where it is used to retain flexibility
