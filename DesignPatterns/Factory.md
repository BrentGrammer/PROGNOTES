# Factory Pattern

Based on examples from the book, [Head First Design Patterns](https://a.co/d/gc0p5dK)

### Why use a Factory Pattern?

- encapsulates object creation, i.e. the building of objects of different types
  - One of the main ideas is to move the `new()` instantiation of objects and encapsulate that since the new keyword makes a concrete class.
  - If implementation of the concrete objects change, then everywhere they are used may need to be updated - the code is not closed to modification (open/close principle)
- it's only responsibility and job is to build objects
- **provides one place to update what types of objects your clients consume**
  - Multiple clients needing to handle various types of objects should not have if/else or any logic for building the different types in their logic. You would then have to update that logic every time you need to handle new types of products etc. as requirements change.

## Implementation

- Pass in an instantiation of a factory as a dependency
  - Note on static factories: you don’t need
    to instantiate an object to make use of the
    create method. But remember it also has
    the disadvanage that you can’t subclass and
    change the behavior of the create method.
- **Make the objects returned by the factory all implement the same interface**

```java
// PizzaStore is a client that needs to use the factory to get a concrete type of pizza based on what type is passed in to the orderPizza method

public class PizzaStore {
    // the pizza factory is only responsible for building and returning different kinds of pizzas
    SimplePizzaFactory factory;

    public PizzaStore(SimplePizzaFactory factory) {
        this.factory = factory;
    }

    public Pizza orderPizza(String type) {
        Pizza pizza;

        // Do not instantiate concrete classes with new Pizza() etc. here. Instead we use the factory to create/get a pizza based on type and encapsulate the building logic in the factory class
        pizza = factory.createPizza(type);

        // ***The pizzas produced by the factory conform to an interface!
        pizza.prepare();
        pizza.bake();
        pizza.cut();
        pizza.box();
        return pizza;
    }
    // other methods here
}

public class SimplePizzaFactory {

    public SimplePizzaFactory() {

    }

    public Pizza createPizza(String type) {
        if (type == "cheese") {
            // return cheese pizza
        } else if (type == "pepperoni") {
            // return pepperoni pizza
        } else {
            return null;
        }
    }

}
```

## Factory Method Pattern

- encapsulate the object creation into an abstract method in a abstract base class
- Let subclasses made from this base class decide which specific type of product or object to create
- Again, the objects/products must conform to a stable public interface (with common methods that the base class can call to operate on the product)

```java
// Abstract base class that will call a factory method
public abstract class PizzaStore {
    public Pizza orderPizza(String type) {
        Pizza pizza;
        pizza = createPizza(type);
        pizza.prepare();
        pizza.bake();
        pizza.cut();
        pizza.box();
        return pizza;
    }

    // Factory Method that encapsulates product creation
      // Subclasses extend from this base class and implement this for the particular type of pizze product needed
    protected abstract Pizza createPizza(String type);

    // other methods here
}

// The abstract product class (stable interface for all subclasses of this product)
public abstract class Pizza {
    // properties common to all pizzas - part of the interface all pizzas must conform to
    String name;
    String dough;
    String sauce;
    ArrayList toppings = new ArrayList();

    // base methods that operate on the product. Can be overridden by subclasses if needed.
    void prepare() {
        System.out.println("Preparing " + name);
        System.out.println("Tossing dough...");
        System.out.println("Adding sauce...");
        System.out.println("Adding toppings: ");
        for (int i = 0; i < toppings.size(); i++) {
            System.out.println("   " + toppings.get(i));
        }
    }

    void bake() {
        System.out.println("Bake for 25 minutes at 350");
    }

    void cut() {
        System.out.println("Cutting the pizza into diagonal slices");
    }

    void box() {
        System.out.println("Place pizza in ofﬁcial PizzaStore box");
    }
}


// Concrete Creators - subclasses that decide what type of product to create
  // Used in base class factory method
  // Note how this subclass extends the abstract base class PizzaStore so that it gets methods common to all pizza stores, like orderPizza, but has control over which kind of product pizza to create.
public class NYPizzaStore extends PizzaStore {
    // implementation of the abstract factory method in the base class
    Pizza createPizza(String item) {
        if (item.equals("cheese")) {
            return new NYStyleCheesePizza();
        } else if (item.equals("veggie")) {
            return new NYStyleVeggiePizza();
        } else if (item.equals("clam")) {
            return new NYStyleClamPizza();
        } else if (item.equals("pepperoni")) {
            return new NYStylePepperoniPizza();
        } else return null;
    }
}

// Subclassed product using the stable public interface needed by all base types of this product:
public class NYStyleCheesePizza extends Pizza {
    public NYStyleCheesePizza() {
        name = "NY Style Sauce and Cheese Pizza";
        dough = "Thin Crust Dough";
        sauce = "Marinara Sauce";

        toppings.add("Grated Reggiano Cheese");
    }
}


// USAGE EXAMPLE

public class PizzaStoreExample {

    public static void main(String[] args) {
        // Instantiate the concrete creator subclass that knows how to make the specific types of products
        PizzaStore nyStore = new NYPizzaStore();
        PizzaStore chicagoStore = new ChicagoPizzaStore();

        // call the base class's orderPizza common to all subclass pizza stores
        // This will then call the factory method implemented by the subclass
        Pizza nypizza = nyStore.orderPizza("cheese");
        Pizza chicagopizza = chicagoStore.orderPizza("cheese");
    }
}
```

### Parallel class heirarchies

Note above that there are parrallel class heirarchies at play. The creator classes and the product classes both have abstract base classes that delegate implementation to subclasses.

### Dependency Inversion

- The factory pattern helps with following the Dependency Inversion Principle where we want high and low level components to depend on abstractions and not concrete implementations (i.e. the `new`ing up of concrete classes in the code)
- In the example, the PizzaStore abstract class (high level component)
- The low level Pizza component also depends on the Pizza abstract class
- Try not to use `new` for a class and assign it to a variable - this is coupling to a concrete implementation and Factory Pattern can be used to get around this.
- Classes should only derive from interfaces/abstractions, not other concrete classes
- Methods in the base class should ideally NOT be overriden by subclasses - they are meant to be common to all subclasses

## Abstract Factories

- Provides an interface for creating related objects without specifying their concrete classes
- Create an abstract factory class that you can derive one or more concrete factories from
- Used to create a family of objects/products with different implementations
  - i.e. think ingredients for a pizza as a family of objects (Sauce, Dough, Veggies, Meat, Cheese for example)
- You pass in the concrete factory (derived from the abstract factory so it conforms to an interface)

### Usage Example

```java
// Create an abstract factory, i.e. an interface that all derived factories will implement:
public interface PizzaIngredientFactory {

    public Dough createDough();
    public Sauce createSauce();
    public Cheese createCheese();
    public Veggies[] createVeggies();
    public Pepperoni createPepperoni();
    public Clams createClam();

}

// Now a concrete factory implements the abstract factory interface:
public class NYPizzaIngredientFactory implements PizzaIngredientFactory {

    public Dough createDough() {
        return new ThinCrustDough();
    }

    public Sauce createSauce() {
        return new MarinaraSauce();
    }

    public Cheese createCheese() {
        return new ReggianoCheese();
    }

    public Veggies[] createVeggies() {
        Veggies veggies[] = { new Garlic(), new Onion(), new Mushroom(), new RedPepper() };
        return veggies;
    }

    public Pepperoni createPepperoni() {
        return new SlicedPepperoni();
    }
    public Clams createClam() {
        return new FreshClams(); // fresh clams for coastal NYC as opposed to say Chicago that does not get fresh ones
    }
}

// Make an abstract method in your base Product class to delegate implementation of adding the family of ingredients to subclasses which will use the derived factory:
public abstract class Pizza {
    // Common props including the family of objects that are ingredients
    String name;
    // ingredients family
    Dough dough;
    Sauce sauce;
    Veggies veggies[];
    Cheese cheese;
    Pepperoni pepperoni;
    Clams clam;

    // Abstract method delegating to IngredientsFactory
    abstract void prepare();

    void bake() {
        System.out.println("Bake for 25 minutes at 350");
    }
    void cut() {
        System.out.println("Cutting the pizza into diagonal slices");
    }
    void box() {
        System.out.println("Place pizza in ofﬁcial PizzaStore box");
    }
    void setName(String name) {
        this.name = name;
    }
    String getName() {
        return name;
    }
    public String toString() {
        // code to print pizza here
    }
}

// Update the subclasses of Pizza to take in a Ingredients Factory (which will be derived from the abstract factory)
public class CheesePizza extends Pizza {
    // declare the factory as a property
    PizzaIngredientFactory ingredientFactory;

    // pass in the factory to the constructor
    public CheesePizza(PizzaIngredientFactory ingredientFactory) {
        this.ingredientFactory = ingredientFactory;
    }

    // Implement the abstract method in the base Pizza class to use the passed in factory
    void prepare() {
        System.out.println("Preparing " + name);
        // use the factory to create the family of products that are specific to the type of pizza
        dough = ingredientFactory.createDough();
        sauce = ingredientFactory.createSauce();
        cheese = ingredientFactory.createCheese();
    }
}


// In the pizza store that needs specific ingredients, create the derived factory from the abstract factory and pass it in to the pizza products
public class NYPizzaStore extends PizzaStore {

    protected Pizza createPizza(String item) {
        Pizza pizza = null;
        PizzaIngredientFactory ingredientFactory =
            new NYPizzaIngredientFactory();

        if (item.equals("cheese")) {

            pizza = new CheesePizza(ingredientFactory);
            pizza.setName("New York Style Cheese Pizza");

        } else if (item.equals("veggie")) {

            pizza = new VeggiePizza(ingredientFactory);
            pizza.setName("New York Style Veggie Pizza");

        } else if (item.equals("clam")) {

            pizza = new ClamPizza(ingredientFactory);
            pizza.setName("New York Style Clam Pizza");

        } else if (item.equals("pepperoni")) {
            pizza = new PepperoniPizza(ingredientFactory);
            pizza.setName("New York Style Pepperoni Pizza");

        }
        return pizza;
    }
}
```

**The main advantage gained here is that now pizzas can have specific implentations of ingredients that differ and are standardized according to the type of store and the original ordering logic in the client application does not change**:

```java

public class PizzaStoreExample {

    public static void main(String[] args) {
        PizzaStore nyStore = new NYPizzaStore();
        PizzaStore chicagoStore = new ChicagoPizzaStore();

        // The same orderPizza method is called with the same type etc., and under the hood the factories passed in to the pizza prepare abstract method in the pizza subclasses handles the different ingredient implementations as needed.
        Pizza nypizza = nyStore.orderPizza("cheese");
        Pizza chicagopizza = chicagoStore.orderPizza("cheese");
    }
}

```

### Differences between Abstract Factory and Factory Method patterns

- Factory Method uses inheritance/classes and Abstract Factory uses object composition
  - In Factory Method, you extend a class and override a method to create objects
  - In abstract factory, you instantiate a factory based on the abstract type and pass it in to code written against the abstract type.
- Abstract Factory is used when you need to group together related objects

### Considerations with Abstract Factory pattern

- Requires larger interface since dealing with a family of objects
- If you need to extend the family of objects, you need to update the interface in the abstract factory type and in all of the subclasses...
- use whenever you have families of products you need to create and you want to make sure your clients create products that belong together.
