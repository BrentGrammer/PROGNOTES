# Strategy and Template Pattern

- Good book for designing code to fit design patterns: Refactoring into Patterns by Joshua Kerievsky

**All patterns provide a way to let some part of a system vary independently of all other parts.**

## Strategy Pattern

- The purpose of the pattern is to separate a high level policy from a set of low level details
- A level policy delegates through a strategy (interface) to accomplish some goal or operation passing the impl to derivatives.
  - the high level policy does not care about the details of what it delegates to
- Especially useful if you need to change behavior for objects at RUNTIME

### Compared to Template Pattern:

- Strategy Pattern uses External Polymorphism
  - The polymorphism is projected through an interface to an entirely separate instance
  - you need to create two objects and figure out how to hook them together somehow (object 1: the high level policy, object 2: the low level implementation)
  - More flexible than Template because you can create the high level policy and low level implementation at different times.
    - you can create the high level policy in one part of the code, create the low level policy in another part of the code, and combine them in yet another part of the code.
    - Reduces coupling. If coupling is a concern, then Strategy pattern is a good choice.
    - You can hot swap strategies - you can change out the strategy even in the middle of a process. But if you use Template method, you're stuck with the instance for the lifetime of that instance. If you want flexibiliy and changeability, use Strategy Pattern.
    - Both low level implementation and high level policy are independent and can be deployed independently

### Example with FTP

- An FTP class sends packets over the network:

```java
FTP implements IPacketProtocol
  +sendFile()

IPacketProtocol
  +sendPacket()

// implement the interface with derivatives
XModemPacketProtocol
YModemPacketProtocol
HDLCPacketProtocol
X25PacketProtocol
```

## Template Method Pattern

- solves the same problem the Strategy pattern does, but uses a different mechanism
- The low level implementations derive from the class that contains the high level policy
- The high level class is an abstract class
  - the high level class calls it's own method which allows for creating derivatives of the high level (abstract) class

### Compared to Strategy Pattern:

- Template Pattern uses Internal Polymorphism
  - The polymorphism stays within the heirarchy and within the instance
  - There may be two classes but there is only one instance
  - You only need to create one object (create the right instance of the implementation)
  - Good pattern to use if ease of creation of instance is the goal
    - the cost of a few nanoseconds or bytes for ultra performance is valid here. Strategy takes a little longer performance wise
  - Less flexible and more tightly coupled than Strategy pattern.
    - the inheritance coupling is too strong to span a architecturally significant boundary

### Example with FTP

```java
abstract class FTP
  +sendFile()
  +sendPacket

// now you can create derivatives of the abstract class
XModeemFTP
YModemFTP
HCDCFTP
X25FTP
```

# Use Case for Strategy Pattern

- Duck Example from Head First Design Patterns

## The Problem

- Having a superclass that all sub types inherit from, but behavior changes across the sub types
  - but subtypes may have such a variety of different implementations and behaviors, that the superclass can't cover them all
  - or if it does, it will become a bloated class
  - For every new subtype added, they will have to override many methods that they don't use or need because they inherit from the superclass with those builtin methods

```java
// The super class Duck that all sub types of ducks inherit from
abstract class Duck {
  fly() {

  }
  quack() {

  }
}

// This type of Duck works fine with the superclass inheritance
class MallardDuck extends Duck {
  fly() {
    // mallard duck fly impl.
  }

  quack() {
    // mallard duck quack noise impl.
  }
}

// Requirements change and you need to have a new type of Duck - a Rubber Duck, but it has different behavior and implementation requirements than the other duck subtypes:
class RubberDuck extends Duck {
  fly() {
    // Rubber ducks do not fly!!
    // Do nothing. This is part of the problem that strategy pattern addresses.
  }

  quack() {
    // rubber ducks don't quack, but squeak.
  }
}

// Requirements change again and now we need a Wooden Decoy Duck
class WoodenDecoyDuck extends Duck {
  // now the problem is we need to override all the Duck superclass methods we don't need or use for this specific sub type:
  fly() {
    // do nothing, override because wooden ducks don't fly
  }

  quack() {
    // override again to do nothing, wooden ducks don't quack.
  }

  // wooden duck methods that are actually used...
}
```

## The Solution: Use the Strategy Pattern

- At first glance, you might add a Flyable interface and Quackable interface, but this only solves half the problem.
  - The types that fly and quack will implement the interface, but because there is no implementation in the interface, if that behavior changes you have to go into each subclass and type and update the implementation there - we lose code duplication with this approach.
- Use the Strategy Pattern and pull out behaviors into classes that have their implementation
  - Various behavior implementations will each get their own class to encapsulate that specific behavior

### Encapsulate Behavior to classes which implement stable interfaces:

```java
// interfaces that the behavior classes will implement:
public interface FlyBehavior {
  public void fly();
}
// concrete behavior class that encapsulates this type of flying and implements the Fly behavior interface
public class FlyWithWings implements FlyBehavior {
  public void fly() {
    System.out.println("I'm flying");
  }
}
public class RocketPoweredFly implements FlyBehavior {
  public void fly() {
    System.out.println("Rockets firing and flying");
  }
}

// interface the Quack behavior classes will implement:
public interface QuackBehavior {
  public void quack();
}

public class Quack implements QuackBehavior {
  public void quack() {
    System.out.println("Quack");
  }
}
// another behavior class that encapsulates silent quacking behavior (and implements again the QuackBehavior interface)
public class MuteQuack implements QuackBehavior {
  public void quack() {
    System.out.println("Silence...");
  }
}
```

### Delegation

- The Ducks should **delegate** flying and quacking behavior instead of defining it in the Duck super or sub classes
  - They should delegate the behavior to a behavior class
- Place a setter method in the super class69, top level type, that allows for setting which algorithm/behavior to use.

```java
public abstract class Duck {
  // assign a reference to a behavior interface (that is implemented by a behavior class)
  QuackBehavior quackBehavior;
  FlyBehavior flyBehavior;

  public void performQuack() {
    // delegate quacking to the reference to some sort/type of quack behavior object
    quackBehavior.quack();
  }
  public void performFly() {
    flyBehavior.fly();
  }

  // Add setters to be able to set behavior dynamically at runtime:
  public void setFlyBehavior(FlyBehavior fb) {
    flyBehavior = fb;
  }
  public void setQuackBehavior(QuackBehavior qb) {
    quackBehavior = qb;
  }
}

// The subtype references the interface properties and uses a specific behavior class that conforms to that interface
// When the subtype is instantiated the constructor uses a specific behavior class for performing actions delegated in the super class to it
public class MallardDuck extends Duck {
  public MallardDuck() {
    // assign the instance variables initialized in the super class to the specific behavior classes
    // the superclass calls the methods on these which is delegated to the methods on the specific behavior clases assigned below
    quackBehavior = new Quack(); // specific behavior class Quack
    flyBehavior = new FlyWithWings(); // specific fly behavior class
  }

  // other specific to MallardDuck instance methods
}

// USAGE
Duck mallard = new MallardDuck();
mallard.performQuack();
mallard.performFly();

// Change behavior at runtime with setters on the super class:
mallard.setQuackBehavior(new MuteQuack());
// because the implementation is NOT in the duck class, you can inject it into there and change it on the fly
mallard.performQuack(); // now the quack is muted
```

## Main points

- The interface oversees the encapsulation of a family of algorithms (in this case, Fly and Quack behaviors)
- Allows for swapping out of the algorithms (or behaviors) so they are interchangeable
  - Another use case: think of a set of classes to implement different state taxes by different states
- Think of the set of behaviors as a family of algorithms
