# Testing with Python

- Some notes and examples are from Emily Bache's Testing in Python 3 course.

## unittest

- Built in library with Python
- name files with `test_` prefix: `test_classname.py`
  - The library will pick up this prefix for which files to run as tests.
- run tests with: `python -m unittest`

```python
import unittest

# Example unit test to test drive a phonebook.
# Good practice is to start outlining how the class is used and what it's interface looks like and not implement (insert pass for the concrete methods as they're created)
class PhonebookTest(unittest.TestCase):
    # use a setup method to eliminiate duplicate setup code for tests in the suite
    # setUp is a method inherited from unittest.TestCase so we override it here.
    def setUp(self) -> None:
        # setUp is special method because its called before every test case is executed.
        self.phonebook = Phonebook() # instantiate new class for each tests

    # tearDown is another builtin method with unittest - runs after every test case for cleanup etc.
    # Note that teardown is not run if setUp above fails, otherwise it always runs even on other errors.
    def tearDown(self):
        # useful to close a database connection or delete temp files
        # (classes created will be removed from memory automatically)
        pass

    # name tests with test_ in the name
    def test_lookup_by_name(self):
        self.phonebook.add("Bob", "12345")
        number = phonebook.lookup("Bob")

        self.assertEqual(number, "12345")

    # what happens when name does not exist:
    def test_missing_name(self):
        # use context manager to raise error in tests - will throw a key error and if method throws this then test will pass
        with self.assertRaises(KeyError):
            self.phonebook.lookup("missing")

    @unittest.skip("Work in progess") # example of how to skip a test
    def test_empty_phonebook_is_consistent(self):
        is_consistent = self.phonebook.is_consistent()
        self.assertTrue(is_consistent)
```

```python
# phonebook.py
class Phonebook:
  def __init__(self):
    self.numbers = {}

  def add(self, name, number):
    self.numbers[name] = number

  def lookup(self, name):
    return self.numbers[name]

  def is_consistent(self):
    return True
```

## Terms

- Test Fixture: supporting code for managing resources needed by your test cases. (i.e. `setUp` and `tearDown` are considered a test fixture)

## Troubleshooting

### Cannot find module in production code in test

- Set the Python PATH if your test cannot find the module to import it:
  - `$ PYTHONPATH=src python -m pytest`
  - This adds the `src` folder (replace with folder containing your source code) to the path so the test can see and import it.

# Pytest

- Install with pip

### Command Commands to run tests:

- Show print statements for debugging: `pytest -s`
  - run specific test: `pytest -k test_name`
  - run tests in a file: `pytest -vv ./tests/test_financial_parsers.py`
  - show full verbose test output: use `-vv` flag
- Coverage: `coverage run -m pytest arg1 arg2 arg3`
  - Omit tests from coverage report:
    - create .coveragerc in root and put:
    ```shell
    [run]
    omit =
        # ignore all test cases in tests/
        tests/*
    ```
  - Generate a report: `coverage html`

## raising errors in tests:

- use pytest.raises()

```python
import pytest

#...test case wrapper and test code...
    with pytest.raises(KeyError):
        phonebook.lookup("Bob")
```

## Pytest Fixtures

- The test case indicates the resource it needs specified in its arguments list
- Pytest looks for a function decorated with `pytest.fixture` and hooks it together at run time (a kind of dependency injection)
  - Test indicates what it requires
  - At runtime, pytest finds that and injects it into the test.

```python
import pytest

# use decorator and name the function same name as resource
@pytest.fixture
def phonebook():
  return Phonebook()

# add the dependency resource as an argument to the test:
def test_lookup_by_name(phonebook):
    phonebook.add('bob','12345')
    number = phonebook.lookup('bob')
    assert number == '12345'

## Further tests can use phonebook fixture and it works like setup does in unittest.
```

### Cleanup fixture in pytest

- Use a yield statement which will allow code afterwards to be run after the test case.

```python
@pytest.fixture
def phonebook():
  yield Phonebook() # use the yield statement.
  phonebook.clear() # this runs as cleanup (on the phonebook builtin to the class custom method) after every test.
```

### builtin fixture dependencies

- There are built in dependencies you can pass to the fixture, for example `tmpdir` which will create a temp directory unique to each test.

```python
@pytest.fixture
def phonebook(tmpdir): # tmpdir created temp directory for each test
  # provide a doc string to show in the test output for fixture registry
  "Provides an empty Phonebook"
  yield Phonebook(tmpdir)
  phonebook.clear()
```

### Viewing available fixtures:

- `python -m pytest --fixtures`

## Paramaterized Lists

- For tests with multiple cases use the paramtrize annotation.

```python
@pytest.mark.parametrize(
  "entry1,entry2,is_consistent", # the arguments in the test
  [
    (("Bob","12345"),("Anna","01234"), True),
    (("Bob","12345"),("Sue","12345"), False)
  ] # the data for the arguments - each case is a tuple list of the data
)
def test_is_consistent(phonebook, entry1,entry2,is_consistent):
  phonebook.add(*entry1)
  phonebook.add(*entry2)
  assert not phonebook.is_consistent() == is_consistent
```

# Organizing tests in a large project

- Source code is stored in a `src` folder
- Tests are stored in a `test` folder

```python
# my_proj
  # src
  # test
```

- Store Test fixtures in the `test/conftest.py` file
  - `test/conftest.py` is a special file that pytest will look for fixtures in.
  - it is a good central place to keep your test fixtures.

### pytest.ini

- An important file that stores options that apply to all of the tests in the project.
- This setup tells to run with strict markers that are only on the list
- We use this in conjuction with marking tests as slow with `@pytest.mark.slow` to skip tests that use the large csv file when the not slow option is passed to the command.

```
[pytest]
addopts = --strict-markers
markers =
  slow: Run tests that use sample data from file(deselect with'-m "not slow"')
```

## Pytest Markers

- Get a list of builtin markers with: `pytest --markers`
  - skip is built in for example: `@pytest.mark.skip("Comment on why this test is skipped")`
  - `@pytest.mark.skipif(sys.version_info < (3,6) reason="requires python3.6 or higher")`
- Some tests are slow and you might want to skip them

```python
# use the mark.slow annotation
@pytest.mark.slow
def test_slow_test(phonebook):
  with open('largefile.csv') as f:
    # expensive processing on large file
  # ...
```

- Now run the pytest command with the not slow flag to skip the marked slow tests:
  - `pytest -m "not slow"`

### Capturing Standard Out in Tests

- Built in fixture `capsys` in pytest can be used to capture what is printed to the console.

```python
def test_print_fizzbuzz(capsys):
    print_fizzbuzz(3)
    captured_stdout = capsys.readouterr().out # can read from std out or error - we choose out here
    assert captured_stdout == "1\n2\nFizz"
```

# Test Doubles

### Using a Stub

- Mock comes with the python standard library from unittest and can be used to create a stub.

```python
from unittest import Mock

def test_alarm_is_on_at_higher_threshold():
    # this constructs a stub using the Mock function:
    stub = Mock(Sensor) # pass the class to mock so it knows what methods it has
    # configure the mock to return what you want:
    stub.sample_pressure.return_value = 21.0 # control what is returned

    alarm = Alarm(stub) # pass in stub instead of real sensor impl
    alarm.check()
    assert alarm.is_alarm_on
```

### Using a fake

- Fakes have an implementation with logic and behavior (unlike stubs), but is not suitable for production.
  - Using a stub would be trickier than a fake - stubbing all the methods is complicated for the dependency.
  - For example, the File interface which has a lot of methods and is slow is bad to use in tests, but we can use StringIO instead which has the same methods as File, but is all in memory. It matches the File interface, but is faster and simpler for tests.

```python
import io
from html_pages import HtmlPagesConverter

def test_convert_second_page():
    # make a fake of a file to prevent using file system in the test
    # the fake has the same interface needed in the class as the file interface, so to the class it looks like a file
    fake_file = io.StringIO("""\
page one
PAGE_BREAK
page two
""")
    converter = HtmlPagesConverter(fake_file) # class accepts a file passed in, but we use the fake
    converted_text = converter.get_html_page(1) # get page 2 0-based index
    assert converted_text == "page two<br />"
```

### Example of a Mock

```python
class MockNotifier():
    def __init__(self):
        # add the expected users to be notified and init to empty list (this is not the original or real impl)
        self.expected_user_notifications = []

    # we need the same interface as the class that we're replacing
    def notify(self, user, message):
        # don't send real messages from this mock in the test, check all notifications are expected
        expected_user = self.expected_user_notifications.pop(0) # notification should be the user at the front of the list

        # if the user is not expected, raise an error
        if user != expected_user:
            raise RuntimeError(f'got notification for unexpected user {user}, was expecting {expected_user}')

    # keep a list of users we expect to be notified in this mock impl
    def expect_notification_to(self, user):
        self.expected_user_notifications.append(user)


# test:
def test_discount_for_users_with_mock():
    notifier = MockNotifier() # use the mock here to pass into main impl
    discount_manager = DiscountManager(notifier) # pass mock in
    product = Product("headphones")
    product.discounts = []
    discount_details = DiscountData("10% off")
    users = [User("user1", [product], User("user2",[product]))]
    # set some expectations on the Mock for the calls that it should recieve in the next part of the test (this is the difference between a Stub)
    # should expect a notification to both users
    notifier.expect_notification_to(users[0])
    notifier.expect_notification_to(users[1])

```

### Using a Mock to check methods were called with the right Arguments:

```python
def test_get_score():
    # ...testing code from a parent method that calls get_score_with_weather within its logic

    def mock_get_score_with_weather(sunny_today, flavour):
        # check that the arguments recieved are expected
        assert sunny_today == True # make sure arguments are what was passed in to the parent function
        assert flavour == IceCream.Vanillan
        return 0 # return this hard coded score from the mock

    assert scorer.get_score == 0
```

# Coverage

- use the `coverage` package
- `coverage run -m pytest`
  - runs tests and gathers coverage data
- Read the coverage report: `coverage report -m`
  - shows a list of files in project and which lines of code were covered.
  - Get an html report: `coverage html`
    - allows you to click into files to see which lines are not covered highlighted red.

### Branch Coverage

- More computationally expensive, but will provide better coverage with more information.
- Takes into account branches of if conditionals, etc.
  - if the true condition branch is tested, but not the false condition, then the line is marked as yellow or partially covered in test coverage reports. (yellow means covered but with only one outcome.)

# Mutation Testing

- Used to determine how good your tests are
- Start with passing tests, deliberately insert bugs (make a mutant of the code)
- If tests fail, then that is a good sign - your tests have killed the mutant
- If the tests pass, that indicates a problem as the mutant has survived and the tests could be better.
- Mutation testing is time and resource heavy - cannot afford to do it all of the time.

# Hard to Test Code

## Peel and Slice Method

- If you have code with mostly testable logic that has some small part that is hard to test, use the peel and slice methods.

### Peel: Take the outer part away that is untestable

- Hard to test code is at the start and/or end of the method
- Use the extract method refactor on the source code and add new arguments to the juicier inner part extracted into a new method removing the outer ends that are hard to test.
  - The extracted method will take in more arguments where you can pass in dependencies that were hard to test when bundled with it before.
- The new method will be easy to test and be a major improvement from the method before extracting.

### Slice: Take away the inner untestable part.

- Use when the hard to test code is in the middle of the method.
- Create a local function that does the hard to test code. Move the function declaration to the start of the method and call it in the original place in the code.
- Now you can use the Peel method to peel the hard to test function at the top of the method.
- [Example video](https://app.pluralsight.com/ilx/video-courses/5a80aa07-b192-4111-a612-473392f6bdf9/16f61426-ac39-40df-b688-15c557dc2d77/a320aecc-5198-4d62-9b5b-e1106ab25963)

```python
# Step 1: Slice
# original Code demoing the slice method (hard code to test in the middle of method):

def print_sales_forecasts(now=None):
    # create a new local function to encapsulate the hard to test code in middle below
    def update_selection():
        # call the line of code with global side effects
        scorer.update_selection()


    names = ["Steve","Julie"]
    # use this pattern to use a passed in (for testing) or global (for prod)
    now = now or datetime.datetime.now() # use optional arg if set or global

    print(f"Forecast at time {now}")

    for name in names:
        if name == "Steve":
            scorer.flavour = IceCream.Strawberry
        else:
            # HARD TO TEST IN MIDDLE - THIS HAS GLOBAL SIDE EFFECTS - hard to test
            # scorer.update_selection() # this is a method that mutates global variable
            # call the sliced method here instead:
            update_selection()
        score = scorer.get_sales_forecast()
        print(f"{name} score: {score}")
```

```python
# Step 2: Peel

import datetime
import scorer
from scorer import IceCream

# pass in now as an optional argument since the code depends on this global
def print_sales_forecasts(now=None):
    # sliced function moved to the top
    def update_selection():
        scorer.update_selection()

    # call extracted method using the peel strategy. One of the args is a reference to the sliced func above
    print_sales_forecasts_with_update_selection(now, update_selection)

# define the extracted easy to test code into extracted method and pass in the hard to test extracted method.
# this enables you to replace update_selection with a test double in the test.
def print_sales_forecasts_with_update_selection(now, update_selection):
    names = ["Steve","Julie"]
    # use this pattern to use a passed in (for testing) or global (for prod)
    now = now or datetime.datetime.now() # use optional arg if set or global

    print(f"Forecast at time {now}")

    for name in names:
        if name == "Steve":
            scorer.flavour = IceCream.Strawberry
        else:
            # call the sliced method here instead:
            update_selection()
        score = scorer.get_sales_forecast()
        print(f"{name} score: {score}")


### In Test:

# create a stub for the hard to test extracted part:
def stub_update_selection():
    scorer.flavour = IceCream.Vanilla # set to fixed value so behavior is predictable
    # before the test was calling the actual scorer.update_selection which produced random output

def test_sales_forecasts(capsys):
    # pass in the now argument so the method uses it in the test instead of the global
    now = datetime.datetime.fromisoformat('2023-05-08 15:12:32.825082')
    # pass in the stub to the extracted inner code method
    print_sales_forecasts_with_update_selection(now=now, update_selection=stub_update_selection)
    # use builtin capsys to verify std out for the print method
    output = capsys.readouterr().out
    assert output == expected_output
```

### Disadvantage of Peel and Slice:

- Coverage for the extracted hard to test code will not be covered
- The code extracted into those new methods is awkward and difficult to test
- The resulting design after applying these methods may be worse and refactoring will be needed.
  - Short term solution so you can get enough tests in place so you can begin refactoring and fix the design.

# Monkey Patching

- Meta programming: changing an attribute or piece of code at runtime, exchanging the code that was there when the program started with some other code.
- Can be a useful strategy for inserting a test double for hard to test code.
- Pytest has a `monkeypatch` fixture builtin that you can use in tests

```python
# this method is difficult to test since it reaches out to the internet and is not covered using the peel and slice method shown above.

# method impl from scorer.lookup_weather:
def lookup_weather(location=None):
    location = location or (59.2343,18.2343) # default coords
    days_forward = 0
    params = {"lat" location[0], "long": location[1], "days_forward": days_forward}
    weather_app = "http://weather.com"
    response = requests.get(weather_app + "/forecast", params=params)
    if response.status_code != 200:
        raise RuntimeError("Weather unavailable")
    forecast = response.json()
    return bool(forecast["weather"]["main"] == "Sunny")

# test for the difficult to test code above (without using a double):
def test_lookup_weather_default_location():
    assert scorer.lookup_weather() == True # unreliable as the service could be down or not return sunny

# Use a test double in the test
class StubWeatherServiceResponse:
    def __init__(self):
        self.status_code = 200 # the real service returns a response with a status code on it
    # return the minimal json in this stubbed method that the test needs
    def json(self):
        return {"weather": {"main": "Sunny"}}


# use the monkeypatch test fixture builtin to pytest
def test_lookup_weather_default_location(monkeypatch):
    #
    def stub_requests_get(*args, **kwargs):
        return StubWeatherServiceResponse()

    # use monkey patching to replace the requests module to not rely on the external service/internet request
    monkeypatch.setattr(requests, "get", stub_requests_get) # note how we're monkey patching a stable interface ("get" method name will not change on requests...)
    assert scorer.lookup_weather() == True

### This will improve the coverage on the lookup_weather method whereas before it was not covered.
```

### Warning with Monkey Patching:

- Do NOT use monkey patching to replace details that will change in the future (like method names)
  - In the above example, we monkey patch the "get" method in the requests module - this is likely to remain unchanged and is not an implementation detail specific to our source code.
- This can lead to fragile tests.

### Self Initializing Fakes

- If the System under test needs a remote service (i.e. making a request to the internet), you need to replace it with a Fake test double.
  - The first time you call this fake, it forwards your call to the remote service and records what happens in a file
  - The next time you call it, it provides the response from the file (the remote service does not need to be running)
  - Uses monkey patching under the hood
- Useful for reducing the amount of test double code you need to write.
- use `vcrpy` the python version of vcr and `pytest-recording` plugin for pytest that works well with the vcr package (`urllib` is a dependency you need to install as well).
  - you can use the annotation `@pytest.mark.vcr`
  - add a flag to the command to run pytest: `--record-mode=once` to tell vcr how to record
    - Once means that it will record new interactions the first time and then expect to be able to replay them. (i.e. can record what the server has done the first time you run the test marked with `mark.vcr)
    - Will create a `cassettes` directory with a yaml file containing details of the request made (using requests module for example)
    - Future test runs marked will use this recorded response from the server consistently
    - If the response changes in the future and you need to accomodate, you can delete the cassette file and re-record the response from the server to update.

```python
# use the vcr mark annotation to record the request made the first time (using record-mode=once)
@pytest.mark.vcr
def test_lookup_weather_not_sunny():
    location_ski_resort = (63.3990,13.0815)
    assert scorer.lookup_weather(location_ski_resort) == False # not sunny
```

- You'll need to update cassette files if they get out of date
- Can hinder refactoring if you want to rename the test (the cassette file is named after the test)
