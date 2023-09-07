https://cleancoders.com/episode/clean-code-episode-15

Designing System Components:
- Start with identifying Actors in the system
  - An object or class should be for each actor to separate responsibilities
  - the component should have one actor that would ask them to change how they are doing things

Example Coffee maker system:
3 actors:
  - The Brewer actor - responsible for controlling the UI class
  - the Hot Drinker actor - responsible for the Hot Water Source class
  - the Now Drinker actor - takes pot on and off - responsible for the Container Vessel class

*Note above the classes are generic and not implementation specific - i.e. not boiler pot, or on button,o or heat valve etc.
*The components that contain details depend on the components that contain policy (dependency inversion principle)

**Start with the high level policy design divorced from the low level details.

The high level policy classes together make up a component
  - you can derive many different coffee machines from the component
  - Derivatives can be plugged into it and the component knows nothing about them.
  - The derivatives themselves can each be a component - you can mix and couple them with other derivatives from the base high level policy component

---

Now implement the low level details (think Open Closed Principle)

- Make derivatives of the base classes (high policy level classes you started with) to handle low level implementation without making any policy decisions.

Ex: UI -> MarkIVUI (poll() -checks if ready to start and then calls Base class UI start())

------------------

COMPONENT COHESION

https://cleancoders.com/episode/clean-code-episode-16

Component: what defines a component is that it is ready to run and is independently deployable as part of a running system.
  - examples: a DLL or JAR file or a Gem (ruby)

What are the elements of a Component?
- Functions
  - the forces that bind functions together is called Cohesion

Classes are the first layer of cohesion for functions. 
  - The functions are the only thing that are public and visible from a class
  - the data is private

Common Mistakes:

Subsystem Error:
The most common error when trying to decide what classes belong together or cohere is the Subsystem Error.
 - That classes can work together to acheive a certain goal is not a good reason to put them in the same component (video ts 12:16)
  - Ex: Payment system: the class that formats a report should NOT be in the same component with the classes that calculate the values displayed within that report
  - **Unlikely that classes that QUERY data should be combined in the same component with classes that USE the data!

Bundling whole heirarchies together in a single component. (13:20)
  - dependencies shoule be inverted across inherited relationships - the flow of control should oppose the source code dependency

**A sign that you have bad component cohesion is if you find it difficult to independently deploy components due to tight coupling
 - The GOAL is INDEPENDENT DEPLOYABILITY


THE RELEASE/RE-USE EQUIVALENCE PRINCIPLE (19:35)

- The granule of re-use is the granule of release
  - The smallest thing you are willing to release is the smallest thing anyone else will be able to re-use
  - you cannot re-use a component unless it's author is willing to manage it through a release cycle (maintain old version while new is up or older versions for availability, release numbering, date record keeping, etc)

** Rule: A component has to be large enough (with enough classes in it) to justify managing the release cycle (otherwise you have too many components to manage and keep track of -this reduces the number of components to manage).
  - You want to shoot for a few strategic components and not a plethora of little tiny ones.
  - Remember that a component must be maintained through a release cycle when designing  the system and components.

THE COMMON CLOSURE PRINCIPLE (24:20)
- All of the classes that change for the same reason should be grouped in the same component (within a layer)
  - This means that all the classes in a component all have the same responsibility and serve the same actor. they are closed to all the needs of any other actor in the system
  - See timestamp 30:54 for a good graphic explanation of the end goal
  - When an actor requests a change, we will then know which components will need to change and which will not
- The classes we group together into components should be closed against the same kinds of changes. (26:33)
  - We gather together the classes that change for the same reasons and separate classes that change for different reasons.
  - Restatement of the Interface Segregation Principle

- The goal of this principle is to minimize the number of components that must change when requirements change.

- In a well designed system, if the requirements change, just one component should change. But this is not practical in reality since multiple layers of an application may need to change with updated reqs. 
- **Should strive for if a requirement changes, then one component PER LAYER changes.

- Components should not cross boundaries/layers (i.e the UI layer, the DATA layer, etc.)


THE COMMON RE-USE PRINCIPLE (31:52)

- Group together classes that are used together and separate classes that aren't used together (have/have no dependencies on one another)
- Construct your component so that you use all of the classes within that component (similar to the interface segregation principle)
  - i.e. the interface segregation principle says to make classes where if one method is used, they are all used
  - Avoid making components that depend on classes that they do not use. If one class in a component is used, then all of the others should be used as well.
- When you depend upon a component, you should depend upon ALL of the classes within that component.
  - The problem this addresses is that of exposing too much knowledge

If you have a component with a class that your users don't use or care about (i.e. Bob's example of a voice driver in the modem in his bad windows upgrade crash), then if that unused class changes, your users for that component will be affected.


* You cannot satisfy all of the principles and must choose how much of each to apply (44:25):

Release Re-use Equivalence Principle - tends to add classes to a component
  - Be careful about making components with this principle soley - you'll have a very re-usable component, but it will be a pain to maintain because it will be loaded with classes which are tightly coupled

Common Closure Principle - tends to limit the number of classes in a component
  - Be careful of adhering to much to this at the expense of the other priciples. You will have a component with a single responsibility, but it will be very difficult to re-use

Common Re-use Principle - tends to limit the number of classes in  a component

- The component partitioning you choose initially will likely not be the one you wind up with later in the project
  - early in project focus is on the common use and common closure principles (Developability)
  - as project matures, it moves more towards the release and re-use equivalence principle (Reusibility)

Systems are made up of layers, that are made up of components which contain classes that house functions.

Layer (isolated)
    Components (re-usable and independently deployable)
      Classes (single responsibility to single actor)
        Functions
