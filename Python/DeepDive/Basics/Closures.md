CLOSURES:

-A closure is the encapsulation of a free variable referenced inside a function that is outside of the local scope (scope inside a function).
IOW, it is a function and it's free variable(s) bound together.

- [Good explanation of how the pointers and call stack updates](https://app.pluralsight.com/ilx/video-courses/1bafc95c-ab4c-49d9-8189-953e42b7f0b9/bd6c38f2-283f-47de-ac99-e2da75ec83a0/4304ba88-dd6f-4ae1-bc1f-9cf9384b7e6d)

Closure = function + free variables (non local variables which are referenced in it's body definition) with an extended scope

Free Variable: a variable that is referenced which is not local to the scope

Note: you can see the free variables of a function with introspection:
fn.**code**.co_freevars # returns a tuple of free variables
fn.**closure** # returns an object with the memory addr of the cell and the addr of the value the cell points to

Key Point:
** The closure is created when the function is created (defined) - the cell is created and pointers set
** The free variables are evaluated at runtime (when the function runs)

## How Closures Work In Python:

- A closure consists of a function and it's free variable(s) - this means that the value of the variable that is nonlocal and the variable that is free in the closure is shared and has a shared scope (2 scopes).
  IOW, the label is in 2 scopes but references the same value

-Python creates a cell (an object) as an intermidiary object with a value that references the original value object in memory.
The outer variable points to the cell (instead of directly to the value object), and the free variable in another scope points to the same cell (the cell again is pointing to the original object)
(Normally, without a shared scope, the variable would simply point to the direct object value in memory)

Cell - { memAddr: 0x0511, value: 0xA22 } ----> Original Value - { memAddr: 0xA22, value: 'value' }

The variables point to the cell which has an indirect reference to the original value object (python double hops over these whenever the value for the variable is retrieved)

- The cell created has more than one variable pointing to it, so that when the outer scope is destroyed, the free variable in the closure is still pointing to the cell, so it is not garbage collected and remains as a reference to the original value.
  Note: The cell address remains the same, but what it points to can change.

Create vs. Run time:
-When a closure is created (the function with free variables in an extended scope), a cell is created which points to the original value.
-During runtime, when the closure is run(the function is called), Python does the double hop to retrieve/evaluate the variable by referencing the cell, which then references the original value it's pointing to.

### MODIFYING FREE VARS IN A CLOSURE:

-When you want to assign a value to an outer scoped variable

Ex:

def counter():
count = 0

def inc():
nonlocal count
count += 1
return count

return inc

fn = counter() # closure returned with nonlocal count pointing to cell and cell pointing to 0 object

fn() # indirect reference pointing to 0 object in the cell is changed to point to a 1 object.

NOTE: You can have different instances of closures - each time a closure is created, a new cell is created.

Ex:

```python
f1 = counter()
f2 = counter()

f1() # -> 1
f1() # -> 2

f2() # -> 1 (points to a new cell which points to a separately created 0 object)
```

### SHARING EXTENDED SCOPES:

- Multiple closures can share the same reference:

```python
def counter():
  count = 0

def inc1():
nonlocal count
  count += 1
  return count

def inc2():
  nonlocal count
    count += 1
    return count

    return inc1, inc2

f1, f2 = counter() # unpack returned tuple of function references

f1() # -> 1
f2() # -> 2 (scope is shared with f1 closure so the cell points to the same original value object
```

### COMMON GOTCHA WITH SHARED EXTENDED SCOPES AND CLOSURES:

-When returning closures in a for loop, the free variable is not evaluated until the closures are called after the for loop completes - this can create problems since the free variables indirect reference has already been modified multiple times by the loop

Ex:

adders = []

for n in range(1, 4):
adders.append(lambda x: x + n)

adders[0](10) # -> 13
adders[1](10) # -> 13
adders[2](10) # -> 13

\*\* n in the for loop and inside the lambda closure all point to the same cell. n is assigned a new value in each iteration changing where that cell points. When n is evaluated in the called closures at runtime, the value the cell points to has already been changed to reference 3 (the last assignment of n in the loop)

## SHARED SCOPES CAUTION WITH CLOSURES (AND FOR LOOPS):

-Be careful about having shared labels across shared scopes

-Can be particularly tricky when dealing with loops

Ex:

```python
def adder(n):
def inner(x):
return x + n
return inner

add_1 = adder(1) # closure with n as free var pointing to 1
add_2 = adder(2) # closure with n as free var pointing to 2
add_1(10) # -> 11
add_2(10) # -> 12

# Now you may want to reduce repition by using a loop:

adders = []
// add inner functions to the list

# n is shared between the two scopes here - the n in the for statement and the n in the append are the same, n is global and the lambda is NOT a closure:

for n in range(1,3):
adders.append(lambda x: x + n)

# n = 3 --> each lambda added to the array is pointing to the n in the for statment which is modified to point to 2.

adders[0](10) #-> returns 12, since n is pointing to 2 after the for loop completes using n when this is called.

IOW, What is being added to the array is a symbol/label that is pointing towards an object referenced by the global n in the for statement. This object gets modified to 2, and so all of the references added to the array are pointing to 2.

# the symbol `n` is not evaluated in Python until the lambda functions are run!
```

- lambda is created, a symbol `n` is stored
- Python will look up and derefrence `n` when the lambda is run

\*\*\*You can also get this bug even if you use closures:

-Create the loop inside a function to make the lambdas closures:

```python
def create_adders():
adders = []

# n is now a free variable in top level function scope

# the lambda is an inner function(closure) accessing free var n
```

for n in range(1,3):
adders.append(lambda x: x + n)
return adders # a list of closures

adders = create_adders();
adders[0](10) # -> still returns 12 because the loop updates n which cell in closure is pointing to when this is evaluated.

### SOLUTION:

DON'T USE A CLOSURE - assign a default accessing `n` in the loop:

-assign the `n` in the lambda as a default value to an extra argument and use that argument in the addition

-\*\*\* Defaults get evaluated at Creation Time instead of later at Run Time in Python, so the current value of y when the loop is run and the lambda is created which will be called later, the lambda is created with y pointing to the value of n in the current loop.
Note: This is actually not a closure since y is pointing to an object and not a cell. y is not a free variable in the lambda, since y is local and n is not metnioned in the body of the lambda

def create_adders():
adders = []
for n in range(1,3): # assign y to default `n` and use `y` in lambda
` adders.append(lambda x, y=n: x + y)
return adders

adders = create_adders()

adders[0](10) # -> returns 11 as desired

## USING CLOSURES TO REPLACE A CLASS:

-Often you can use a closure to replace a class:
Ex: - When you have a simple class, with one callable for instance, it's usually easier and cleaner to write it as a closure.

Ex with class to feed numbers to and get average of them at a point:

### this class stores numbers and returns the average every time they are requested

class Averager:
def **init**(self):
self.numbers = [] # instance variable

def add(self, number):
self.numbers.append(number)
total = sum(self.numbers)
count = len(self.numbers)
return total / count

- disadvantage here is that every time a number is added, the add must recalculate the total and count - this is inefficient

a = Averager()

a.add(10) # 10.0
a.add(20) # 15.0

### Alternative using a closure:

- simply store the total and increment it with the new number on each add
- simply store the count and increment it on each add
  - This eliminates the overhead of storing the numbers and calculating len and sum each time

def averager():
total = 0
count = 0

# create closure:

def add(number): # since there is an assignment make these nonlocal to keep total and count values around when calling inner closure:
nonlocal total
nonlocal count  
 total = total + number
count = count + 1
return total / count

return add

a = averager() # returns the add closure
a(10) # -> 10.0
a(20) # -> 15.0

### Another Example with a class counting time of elapsed seconds:

- When you have a simple class, with one callable for instance, it's usually easier and cleaner to write it as a closure.

from time import perf_counter

class Timer:
def **init**(self):
self.start = perf_counter()

# this tells python to just call this method when the instance is called

# this is done if you only have one callable you want to use and now you don't have to dot chain the method onto the object

def **call**(self):
return perf_counter() - self.start

t1 = Timer() # starts counter
t1() # returns time from start - calls the polling method defed by **call**

-- Alternative approach using a closure

def timer():
start = perf_counter()
def poll():
return perf_counter() - start
return poll

t1 = timer()
t1() # returns time difference from creation and this call

## CLOSURE APPLICATION PART 2:

-Useful for adding functionality to a function

- Ex of a counter function counting and printing how many times a fn has been called in addition to calling it:

- this returns a closure fn that calls the function passed in with args passed
  on calling the closure and also prints how many times it has been called using the stored count variable captured in the closure

def counter(fn):
cnt = 0
def inner(*arg, \*\*kwargs):
nonlocal cnt
cnt += 1
print('{0} has been called {1} times'.format(fn.**name**, cnt)) # call the fn passed in with whatever args passed:
return fn(*args, \*\*kwargs)
return inner

def add(a,b):
return a + b

# returns the closure that will call add with the count free var from the counter fn:

counter_add = counter(add)

result = counter_add(10,20) # prints 'add has been called 1 times'
result # -> 30

-- Example using global var to store the count:

# create global:

counters = dict()

def counter(fn):
cnt = 0
def inner(*args, \*\*kwargs):
nonlocal cnt
cnt += 1
counters[fn.__name__] = cnt
return fn(*args, \*\*kwargs)
return inner

counted_add = counter(add)
counted_mult = counter(mult)

counted_add(10,30)
counted_mult(10,2)

# both closures are referencing the same global variable and update it.

-- Modified so the dictionary is passed in so you don't have to define and remember the name of the global in the closure function:

def counter(fn, counters):
cnt = 0
def inner(*args, \*\*kwargs):
nonlocal cnt
cnt += 1 # uses local passed in variable
counters[fn.__name__] = cnt
return fn(*args, \*\*kwargs)
return inner

c = dict()

counted_add = counter(add, c)
counted_mult = counter(mult, c)

\***\* You can use the same label as the original function to keep the name and the extra functionality \*\***:

add = counter(add, c)

# now add has the extra functionality counter when it is called along with returning the original result!
