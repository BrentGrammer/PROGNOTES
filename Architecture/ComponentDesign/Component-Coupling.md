/component Coupling

https://cleancoders.com/episode/clean-code-episode-17


ACYCLIC DEPENDENCIES PRINCIPLE (17:40):
- A software system is composed of components and the dependencies between the components must not form a cycle.
  - If you start at a component and follow the dependencies you must not wind back up at the original component and is not circular
  - You can draw dependencies on a graph and make sure all the arrows point down (18:10)
- helps avoid the "morning after" syndrome - where everything keeps breaking the next morning when it worked yesterday because dependencies changed   

Example of creating a cycle to avoid: 
Error Management component that sits at the bottom of a dependency graph needs to put a message on the UI (at the top of the graph).
The UI had a method called display(). Error Management calling display() creates a cycle in the dependency since the arrow points up to the top from the bottom.

Ways to deal with cycles:
- Split the target dependency component (UI in the above example) into two components.
  - The display component would be split from the UI component
  - Problem with this is lots of small components if you keep doing it.
- Use the Dependency Inversion Principle - find the dependency that causes the cycle and invert it.
  - Ex: Take the display method and make an interface out of it. The interface would reside in the Eror Management component and then the UI would implement it. (instead of Error Management depending on UI, UI depends on the interface in Error Management). 


STABLE DEPENDENCIES PRINCIPLE (28:42)

- A component should only depend on other components that are MORE stable than it is.
  - All the dependencies in an arhcitecture should be pointing in the direction of increasing stability.

Stability: not binary - things can be partially stable, more stable, less stable etc. 27:40
  - Something that is hard to change is stable
  - Something that is easy to change is unstable

You want to depend on components that are hard to change and more stable. Make sure that changing it hurts those doing the changing more than it hurts you

Determining which components are stable:
- Look at the dependencies.
  - components with a lot of components that depend on it are stable since (assuming they are clean) having many components depend on you means you have to check that they aren't broken when you change - the more you have to check, the harder it is, so the component is more stable.
  - conversely, a component that depends on many other components is unstable, since there is nothing stopping it from changing as the components it depends on won't break. the outgoing dependencies will probably force it to change.

Independent components are stable (hard to change), dependent components are instable (easy to change).

**You want certain components to be instable - in those components you put code that you expect will change frequently.
You don't want stable components depending on instable components - all instable comopnents should be depending on more stable components

The I Metric (35:41):
- count the number of classes outside of a component that dependent on the classes inside the component
  - The fan in coupling of a component is this number
- count the number of classes outside of a component that classes within that component depend upon
  - The Fan Out coupling of a component is this number
- Take the ratio of the Fan Out to the sum of the Fan In and Fan Out couplings - this is I
  - I will be 0 when it is very stable
  - I will be 1 if very instable
  - IOW, If there is more Fan In(outer depends on inner classes) than Fan Out , then that is stable. if more fan out (inner depends on outer classes) but less or no fan in that is instable. 

component H with only incoming dependencies has an I metric of 0
component EZ with no dependencies has an I metric of 1

All dependencies should be pointing in the direction of decreasing I (more stability)
 
Fixes (39:46):
- Split the component
- Use Dependency Inversion
  - create an interface in component H and have EZ implement that interface


THE STABLE ABSTRACTIONS PRINCIPLE (43:17):

- The more stable a component is, the more abstract it should be
  - instable components at the top should be concrete
  - measures how well your component structure adheres to the Dependency Inversion Priciple

**NOTE: just because a component is hard to change, does not mean it is hard to Extend (open/closed principle)
- stable components at the bottom of a dependency graph in a system will happen, but if they are designed correctly, even though they are hard to modify, they should be open for extension.
  - can do this with abstraction - it is abstract classes that are open to extension even if closed to modification

Instable components easy to change at the top of a system, all the hard to change stuff at the bottom

Abstract components composed of many classes, some are abstract some are not. The components that are more stable at the bottom should have more abstract classes than not
  - interfaces and abstract classes are considered abstract

AVOID components with:
1. a bunch of concrete classes with incoming dependencies (instable that have others depending on it)
2. a bunch of Abstract classes with no incoming dependencies (stable components that are hard to change at the top of the system heirarchy, bad since dependencies should move in direction to stable components)

You don't want a bunch of abstract classes and interfaces that nobody depends upon or implements - that is useless.
You also don't want a lot of concrete components (i.e. database schemas) that lots of others depend upon - this is painful
  - Note: libraries that are not changing are okay here, it's components that we expect to and are changing that should not have a lot of incoming dependencies


the D metric to track components adherence to dependency inversion 51:58