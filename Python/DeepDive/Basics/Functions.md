FUNCTIONS

-Arguments are passed by reference into functions (their memory address

Basic builtin functions:

print(<value>) <--always returns a string!
input(<value>) <--prints passed in string etc, to console or screen
len('string') <-prints number of length of string

CONVERT DATA TYPES:

int() <-- converts value to int
str() <--converts value to string
float() <--converts value to float (decimal point number)
bool() <-- converts passed in value to boolean value
list() <-- converts values to a list (it will put letters of string into an array)

Ex: str(int(20)) # evaluates to '20'

\*\*\*Variables are passed into functions by reference and not by value.
-This means that immutable data types are safe from side effects that could be caused by a functions code on them.

```python
def func(s):
  s = s + 'added content'
  return s
```

# the param in func stores the reference to the address of the var passed in and if it's a string, for instance, a new string will be created in a different memory address when the code on the right of the = is evaluated in the function and the s created in the function will point to the memory address of that new object.

The original string passed in will not be affected or mutated.

\*When passing in Mutable values/data types, this protection is not in place!
You need to be careful when passing in mutable data types to functions because you can get unintended side effects since all vars are passed by reference and a separate object is not created in the function scope.

---

NOTE: Variables inside of function bodies are not created until the function is called.

Every time a function is called it's own local scope is created

## Any variable assignments inside a function body will tell python to create locally scoped variables

KEYWORD ARGUMENTS:

-some builtin functions have a keyword arg which you can set to modify the behavior:

Ex:

```python
print('Hello ', end='')
print('World')

# prints Hello World on one line since end keyword arg sets the ending character on the string passed in to
# print from \ new line char to empty string

pass multiple args to print and it adds a space in between: print('cat', 'dog')
# prints 'cat dog'

you can use sep keyword arg to change the default space to whatever you want:
print('cat', 'dog', sep='--')
# prints 'cat--dog'
```

---

def hello():
return "hello"

\*\*\*\*If you write a function, and that function doesn't use an explicit return statement, The None object is returned instead

Set default value to none to make a parameter optional:

Another use is to give optional parameters to functions an 'empty' default:

```python
def spam(foo=None):
    if foo is not None:
        # foo was specified, do something clever!
```

--

USING A SENTINEL VALUE AS DEFAULT ARG INSTEAD OF NONE:

\*\*\*NOTE: If you want to set the default to a value that would accept None as an argument, use a sentinel value (use object() which generates a random memory address - this is something that the user is unlikely to enter and allows for the passing of None as an arg):

```python
# __defaults__ on the func stores an array of default vals for args to access:
def my_func(a=object(), kw=object()):
  default_a = my_func.__defaults__[0]
  default_kw = my_func.__kwdefaults__['kw']

  if a is not default_a:
    ...
  else:
    ...
  if kw is not kw_default:
    ...
  else:
    ...
```

---

DEFAULT PARAMS:

-WARNING:

Setting a default param in a module will create an object that the default param is set to.

1. Don't set a default param directly to a function - it will be called and the result will be created as an object that will remain atached to the default param

Ex:

in a module:

def log(a, time=datetime.utcnow()):
#...

The default param datetime will be run on module load (when the module is loaded into the program) and will be an object. When the log function is called later it will remain the return value of datetime.utcnow() and will not update!

Solve this by setting default params to None and making a conditional to check if it's falsey (None will be falsey) to set it:

```python
def log(a, time=None):
  # best to use or to set a default
  time=time or datetime.utcnow()
  ## as an if statement:
  if not time:
    time=datetime.utcnow()
    #... this function will be run when the func is called now and update as desired
```

2. Don't set a default param to a mutable data type without risking that the data will be mutated and change (i.e. setting it to a list)

mylist = [1,2,3]
def log(a, options=mylist):
#...

(If mylist is changed somewhere in the code elsewhere the default param will change since it is pointing to the mutable object in memory by it's memory address)

SOLUTION: Use a tuple instead of a list: mylist=(1,2,3)
(tuples are immutable)

---

\*\*\*\*You can leverage this when using a cache for functions:

(set the default param value to a empty dictionary which will point to the same memory address on all future calls using the cache)

```python
def func(a, cache={}):
 if a in cache:
   return cache[a]
 else:
   # do work on a
   cache[a] = result
   return result
```

NOTE: There is a better approach to caching using memoization and closures. You generally don't want to hard code the cache like this, because it is not as reusable.

---

SCOPE:

Scope for a function and the variables inside it are destroyed once the function returns/ends
Variables inside the local scope of a function are temporary

\*\*\*EXCEPTION: When passing in mutable data params like a List, since it is mutable and you are passing a reference, any changes
made to that data passed in will mutate the data since you are referencing the address of it and not dealing with a copy.

```python
spam = 42

def localfn(spam):
  spam = 43

# spam is still 42 in global scope -
```

\*\*Local variables cannot be used in the global scope.

---

ERROR HANDLING:

-Python program will crash if error encountered. Using try-except will tell Python how to handle the error
and the program will keep running:

```python
def divide42(divideBy):
  try:
    return 42 / divideBy
  except ZeroDivisionError:
    print('Error dividing by zero')

divide42(0)

# prints error message defined in except block
```

\*\*You can use except without specifying the error type and it will catch all errors:

def divide42(divideBy):
try:
return 42 / divideBy
except:
print('There was an error')

Useful for input validation errors:

print('How many cats do you have?)
numCats = input()

try:
print(numCats)
except ValueError:
print('You did not enter a number')

### Unpacking arguments with \*args:

\*args returns a tuple

```python
l = [10,20,30]

def func(a, b, c):
  # code

func(*l)

# this unpacks the passed in array to the 3 positional args in the func
```

- If you have a \*args place holder, and an argument is not passed in then an empty tuple will be returned:

```python
def func(a, b, *args):
  return [a, b, args]

func(10,20)

# returns [10,20,()]
```

---

### Named Parameters:

Note: once you start passing in named args you must continue with named args for the rest of the arguments:

```python
func(1, c=2, b=3, d=4) # func (1, c=2, 3, 4) will throw an error


def func (a,b,c,d):
  ...

func(1,2, d=5)
# a = 1 b = 2, c wll be unassigned and d = 5

def func(a, *args, b):
  ...

func(1, 2, 3, b = 4) # a=1 args=(2, 3) b=4
# will assign b properly since named, otherwise 4 would go into args as it unpacks all the rest of the unamed arguments
```

---

-You can omit any mandatory positional arguments as follows:

```python
def func (*args, d):
  ...

func(1,2,3, d=100) # args is tuple (1,2,3), d = 100

func(d=100) # args = (), d = 100 args positional is not required
```

---

-Force no positional arguments (only named allowed):

```python
# * indicates the end of positional arguments.
def func(*, d):
  ...
```

```python
func(d = 100) # must pass in a named argument only, passing any positional params will throw an error
```

====``========

KWARGS:

\*\*kwargs - stands for keyword arguments

-Scoops up named keyword arguments like \*args scoops up positional arguments

-stores the arguments in a dictionary

-The kwargs is a convential name, it could be any placeholder name - the \*\* is what tells python to scoop up keyword args as opposed to positional ones.

-No parameters can come after the \*\*kwargs parameter

Positional args must be specified first, and then kwargs last (
def func(\*args, \*\*kwargs):...)

Ex:

```python
# the following func has no positional paramters (* at the beginning delineates end of pos args), one rqeuired keyword argument d, and the remainder of keyword arguments are scooped into a dictionary:

def func(*, d, **kwargs):
  # ...code


func(d=1,a=2,b=3)
# d = 5 and kwargs holds { 'a': 2, 'b': 3 }


func (d=1) is also okay since **kwargs does not require that keyword args be set for it.

func() # -> kwargs will be {} (an empty dictionary)
```

-You can use both args and kwargs to scoop up positional and keyword args:

```python
def func(*args, **kwargs):
  # code

func (1,2,a=3,b=4)
# -> args is (1,2) and kwargs is { 'a': 3, 'b': 4 }

# This example is if you want to have a keyword argument after positional with kwargs at the end:

def func(1,b,*,d,**kwargs):
  # code

# The * indicates that the following d must be a keyword arg (you cannot just have **kwargs after a *)
```

### Using a wrapper around a function with args and kwargs:

```python
# * used in the parameters scoops up the arguments passed in to the named vars (args or kwargs)
def time_it(fn, *args, **kwargs):
  start = time.perf_counter()
  fn(*args, **kwargs)  ## --> This unpacks the arguments - The * and ** syntax unpacks when used as arguments (opposite of when they are used in parameters)

  end = time.perf_counter()
  return end - start

# You can now pass in a function (since functions are passable objects in python) by name with flexible arguments

time_it(print, 1,2,3, sep='-')

# print takes (*args, sep=' ')
```

---

FIRST CLASS FUNCTIONS:

\*All functions in Python are first class objects

First class objects:
-can be passed into a function
-can be returned from a function
-can be assigned to a variable
-can be stored in a data structure (list, dict, etc.)

Higher Order Functions:
-take a function as an argument
-return a function

---

ANNOTATIONS AND DOCSTRINGS:

Annotation:

-used to provide inline documentation i.e. to parameters
-Mainly used for modules and tools

def my_func(a: 'a string', b: 'positive int') -> 'string':
...

-Annotations can be any expression - a string, a type identifier, etc.

def my_func(a: str, b: 'int > 0') -> str:
...

Annotation for default value:

def my_func(a: str = 'value', b: int = 1, \*\*kwargs: 'additional args')

NOTE: The annotation is just metadata and does not affect code (i.e. you can assign a above to an integer and no error or warning will be thrown)

---

DOCSTRING:

-Strings that get compiled and can be used as documentation:
-They can be returned by calling the built in help function

In Functions:

-Can put a string in triple double quotes:

```python
def myFunc():
  """This is a docstring in a function"""
   ...code...

help(myFunc)
# returns name of function and the docstring provided

# These strings are stored in a __doc__ property on the object

def my_func(a:

```

---

INTROSPECTION:

-Getting info about your code through code

- built in dir() method - taks an object (including a function) and returns a list of valid attributes for it.

\*The dir() method can be cumbersome to get the right info you're looking for, so it is recommended to use the inspect module:

import inspect

-you can get info on an object/fucntion:

```python
inspect.getsource(obj) # prints the code including docstrings
inspect.getmodule(obj) # prints the module
```

```python
my_func.__code__.co_varnames
#->returns all variables for the function including those in the body,
```

---

Difference between functions and methods in python:

Attributes are objects (incl functions) that are bound to a class
-methods are callable attributes

```python
def Class:
  def func(self):
    pass

# this is an instance method - it is not bound to the class, but bound to the instance created from the class.
```

====================

CALLABLES:

-Any object that can be called using the () operator.

-\*\*All Callables return a value (even if it is just None)

-Functions and methods are callable

-Other objects in Python besides functions and methods are callable:

classes
generators
coroutines
asynchronous generators

-can check if an object is callable with builtin callable function which will return a boolean:
Ex: callable(obj)

---

REDUCING FUCTIONS:

-recombine iterables recursively ending up with a single return value

-Also called Folding Functions, Accumulators, Aggregators

-works with any iterable, sets, string, list, etc.

Ex:

```python
from functools import reduce

reduce(fn, iterable)

# ex with lambda:
reduce(lambda a, b: a + b, [1,2,3])
#-> returns 6

# ex with sequence, i.e. a string:
reduce(lambda a, b:
```

---

USING TRY FINALLY IN A FUNCTION:

-If you have a try finally block and return in the try or the except block before finally, Python will always run the finally. It will put the return statement on
hold and execute the finally block before returning.
(This can be useful for clean up)
