Notes from Clean Code in the Browser Series from cleancoders.com


SINGLE RESPONSIBILITY PRINCIPLE

- The code should express the author's intent!

Best Practices vs. Leading Practices - Leading Practices are TDD and practices that are for nuanced situations requiring expertise.  Best Practices are for obvious problems that have known best solutions.

- SRP - modules should have only one reason to change, or one change agent who would ask for a change.
  - NOTE: Agents of change can include the Developers, PM/PO (changes to UI for ex.), copywriter, Designer, Users (changes to UI for ex.), business people from various departments etc.


- Command Query Separation: Functions should not have command side effects if they are querying and vice versa - this makes functions easier to use and understand.  Side effects should be separated into their own function scope or class.  Querying functions should simply make a get to query for data and not alter any state.

*Functions should only have side effects, or no side effects.

- Taco Bell Programming: using small ingredients to compose various items on the menu.  Functional Programming - making small functions that you can compose to build up into more complicated tasks.
  - Can compose functions with a helper:/]
  function compose(...funcs) {
    let result = null;
    funcs.forEach(fn => result = fn(result));
    return result;
  }

  function someTask() {
    return compose(
      myFunc1,
      () => myFunc2(withArg),
      myFunc3
    );
  }
You might need to use an anonymous func for the parameter arguments if you need to pass in args.


- SRP in CSS: use BEM

  - Block__element--modifier
  - Block is an element that is independent and can be moved around the html and retain it's meaning
  - an element is a child of a block that depends on the block for meaning
  - a modifier is some kind of alternate state that a block or element might get into.

  Ex: featureX-form__text-field--disabled

Example of hi level policy mixed with low level implementation:

thsi combines hi level policy about how the thermostat, heater and cooler relate to one another.  It also combines low level detail about communicating with these particular devices.

class House {
  changeThermostat(newTemp) {
    const temp = await fetch('http://thermostat.local/read');
    if (newTemp > temp) {
      fetch('http://gasHeater.local/engage', {
        method: 'POST',
        body: JSON.stringify({ run: true })
      });
    } else if (newTemp < temp) {
      fetch('http://electric-ac.local/engage', {
        method: 'POST',
        body: JSON.stringify({ run: true })
      });
    }
  }
}

These disparate parts of knowledge should be broken out to their own classes or functions:

class House {
  constructor() {
    this.thermostat = new Thermostat();
    this.heater = new GasHeater();
    this.cooler = new ElectricAC();
  }

  changeThermostat(newTemp) {
    const temp = await this.thermostat.read();
    if (newTemp > temp) {
      this.heater.run();
    } else if (newTemp < temp) {
      this.cooler.run();
    }
  }
}

If the thermostat machinery changes, the heater company or machine change, or the cooler manufacturer and device changes, those are three reasons for the house class to change.  With that implementation knowledge put into it's own modules/classes, the ChangeThermoststat method now does not have those reasons to change and each class would be updated for each change.
The classes encapsulate the knowledge of how each device is accessed.
The changeThermostat method now only contains the high level policy on how those devices relate to each other without having to know about their low level details.

**See Dependency Injection section for further refinement of this code.


-----

OPEN CLOSED Principle: ledft off at 1:07

- When you think you need to modify existing logic in a class or module (other than to fix incorrect code), stop and ask if there is a missing abstraction that would instead allow you to make the change through extension.

Extensions are cleaner than modification.

Watch out for logic junk drawers - for ex. a bunch of conditional logic in various methods is a smell.  When a change is asked for, you need to keep adding conditionals to cover new use cases.  You need to keep adding new conditionals and properties to the class to cover each new use case - this is modification and not extension.

If in this situation you need to look for a missing abstraction (i.e. you can move logic to a new class, or are able to create multiple classes to be responsible for pieces of the logic (each condition).

You can use subclasses or duck typing to fill in the missing abstractions (i.e. in javascript since we don't deal with types idiomatically as it's a dynamic language).

Note: a risk of Open/Close is making leaky abstractions or abstractions that are not meaningful or quite right.  i.e. subclasses that have methods that don't quite fit the idea of each subclass and are too general or applicable/appropriate to one of the subclasses but not as much the others.  These can overcomplicate things.

A solution can be to ditch the subclasses and parent classes and just have separate classes or functions that handle the differing ideas and behavior, or move the differing behavior to it's appropriate and made for subclass.


----------------------

Lyskov Substitution Principle: Wherever an instance of a base class is used, you should be able to substitute it with an instance of a subclass without anything breaking.  IOW, a subclass should not break a contract that a base class has with it's users.

- Cynefin framework:

Problems can be divided into four domains:

Obvious problems - use best practices, use known solutions to solve.
Complicated problems - have many moving parts and require coordination and specialized workers.  Success is dependent on execution of a deterministic plan.
Complex problems - do not have deterministic outputs because inputs are not deterministic.  variables can change - market changes, client did not know what they wanted, etc.  While doing work, that is when it is discovered to what needs to be done, i.e. exploration and experimentation.
Chaos problems - no target is known, the only chance of success involves novel practices.  Undesirable situation, only way to move forward is to try to get clarity.

Software development usually involves complex problems.

Scrum was an attempt to deal with complex problems by taking chunks of the problem and breaking them down to complicated problems and iterate on that.
The stories in sprints are complicated problems with clear deliverables and outcome targets - success depends on execution and is deterministic.

The risk with Scrum is that the sum of all the parts does not necessarily equate to a successful whole (the complex problem of software development).

Some ways to combat this risk is to learn as you work and experiment.  Centralized leadership is not good - the ones doing the work should be making the decisions.  Validate assumptions. Work in small increments with fast feedback loops.

Prototyping with user feedback is also useful.

--

Lyskov Substitution Principle: Wherever an instance of a base class is used, you should be able to substitute it with an instance of a subclass without anything breaking.  IOW, a subclass should not break a contract that a base class has with it's users.  It should have at least the methods and interface that it's base class has, even if it has more for it's specific purpose.

Ex of Lyskov Sub principle around 57:00 in Episode 4

Signs of violating the Lyskov Substitution principle:
  - Looks similar to violating the open/close principle in that a class becomes bloated (with conditionals for instance)
  - The key sign is that the conditionals are doing alot of type checking
   if (x instanceof Y) ...
   else if (x instanceof Z) ... 
   etc.

This is also a sign if implicit type checking is done in dynamic languages:
   if (x.prop === 'value1') ...
   else if (x.prop === 'value2') ...


  - you can have a violation of the open/close principle along with an underlying violation of the Lyskov Substitution principle at the same time.

***SOLUTION: A solution is to either create new base classes for each subclass that violates LSP and requires a new contract, or change the violating subclasses to conform to the base class contract.


Example fixing LSP violation at 1:04:20 in episode 4.

The solution in the example was to move the logic for each conditional based on the type of input to the separate input classes so that the top level class where the conditionals were is not responsible for calculating their value.  

Then a middle layer passed on the event and value to the top level generic onChange handler which simply updated the state with the passed value.

Similar to the solution to the Open/Close principle violation, we move the conditional logic to relevant subclasses to handle instead of in the single function or class.

--------

INTERFACE SEGREGATION PRINCIPLE

- Multiple Client specific Interfaces are better than having a single Generic Interface.

- Organize things by who uses them

- The interfaces only include the methods that their client cares about, no more no less.
This reduces the scope of knowledge that clients need to interact with their object.
* A key idea is to protect other users from knowledge of the generic interface by creating client specific interfaces from it that only contain relevant information to the client using it.

Works best when clients have very little in common with interests and overlapping functionality.

It is possible to share a popular method across client interfaces.

Ex:  Giant User DAO that can be split to interfaces
    GENERIC USER WITH ALL STUFF
ADMIN_USER  MEMBER_USER  TRIAL_USER

Hide information from clients who don't need it and offer a clean api for them to use. 

Can use the facade pattern to hide messy or complicated code and make the api clean.  

*The whole point is to reduce the amount of knowledge you need to interact with the system.

-----

DEPENDENCY INVERSION

- If you have a lot of mocking in your tests or you just have mocks that are complicated and not simple, this is a smell that you are not following the Dependency Inversion principle
- There needs to be a distinction between hi level policy and low level implementation.

**High level policies should not have dependencies on low level implentation details.
Those details should depend on the high level policy.
The high level policy classes should not know anything specific about the low level implementation classes it's using.

IOW, both sides should rely on an interface rather than an implentation

Implementing code in this way has benefits like easy testing with few mocks or very simple mocks when they are used.

example:
     WRONG:
                        class House
                              |
                             /|\                                       
      class Thermostat   class GasHeater   class ElectricAC

    CORRECT:
                         class House
                              |
                             /|\
Thermostat Interface  Heater Interface   Cooler Interface
      |                       |                |
class Thermostat      class GasHeater    class ElectricAC

**We want to favor abstractions (interfaces) over concretions (the classes/implementations) in high level policies.

Example passing in the low level classes as dependencies:

class House {
  constructor(thermostat, heater, cooler) {
    this.thermostat = thermostat;
    this.heater = heater;
    this.cooler = cooler;
  }

  changeThermostat(newTemp) {
    const temp = await this.thermostat.read();
    if (newTemp > temp) {
      this.heater.run();
    } else if (newTemp < temp) {
      this.cooler.run();
    }
  }
}

const house = new House(new Thermostat(), new GasHeater(), new ElectricAC());

**The house class (high level policy code) knows nothing about the concretions that might be passed in besides knowing that they will implement the defined interfaces.


We also want to worry about not giving knowledge of which abstraction to use in high level policies:


WRONG: 
class App extends Component {
  constructor(props) {
    super(props);
    this.state = {...};
    // this is knowledge about whether user is legacy to use legacy client
    if (user.legacy) {
      this.client = new PaintJSClient();
    } else {
      this.client = new BigBucksInvestorClient();
    }
  }
}

CORRECT:
class App extends Component {
  constructor(props) {
    super(props);
    this.state = {...};
    
    this.client = this.props.client;
  }
}
// we pass in the client to the app class
const client = new BigBucksInvestorClient();
<App client={client} />

