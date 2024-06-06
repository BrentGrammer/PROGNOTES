# Testing jQuery/Vanilla JS apps

## QUnit

- Recommended testing tool for jquery.

### Preventing brittle DOM tests

- Use specific selectors instead of checking for element types like div or p or span for ex. etc.
  - For example if checking for an added list item in a html page, look for a class on that item instead of checking how many elements are in a div or list element.
  - Doing this allows you to change the html elements later from divs to spans etc.
  - Focus on checking for the existence of the node by class than what type of element or node it is.

### Testing HTML/Re-using HTML for tests

- See [video](https://app.pluralsight.com/ilx/video-courses/74d86142-f3dd-4607-8b33-d3dbe2f83ccb/ca39bbdb-0ff5-4b78-9fec-88e759ae9203/fb0a9d0d-3970-439e-ae75-0e6aba6924f0) at timestamp 3:30 for using QUnit's fixture to solve the problem of re-using html for different tests.

```html
<!-- in tests.html -->
<html>
    <head>
        <meta charset="UTF-8" />
        <title>QUnit Test Suite</title>
        <link rel="stylesheet" href="qunit.css">
        <script src="jquery.js"></script>
        <script src="qunit.js"></script>
        <script src="tests.js"></script>
        <scrip src="mycode.hs"></script>
    </head>
    <body>
        <div id="qunit"></div>
        <div id="qunit-fixture">{your test html here}</div>
    </body>
</html>
```

- The div with an id of qunit-fixture will take a snapshot of itself at the beginning of running tests
  - at the end of every test, it will reset itself to the original state it was in. So you don't have to reset the dom or cleanup after each test.

## Tests in Continuous Integration

- Run the JavaScript using PhantomJS and capture output.
  - PhantomJS wraps around the webkit engine and gives us a runtime environment to run JavaScript without all of the overhead of a real browser.
  - CAUTION: PhantomJS is made to simulate Chrome, so if you need to test for running under Firefox, IE or other browsers, it is not sufficient.

### Setting up CI with PhantomJS

- See [video] at timestamp 3:50

## Asynchronous Testing with QUnit

- see [video] at timestamp 1:45
- use `stop()` and `start()` functions in QUnit

```javascript
module("Asynchronous Tests");

test("broken synchronous timing test", function () {
  // call the stop function to pause running tests until notified
  stop();

  setTimeout(function () {
    ok(true);
    // tell QUnit to resume running the test with start()
    start(); // resume test running when this async callback is run
  }, 100);
});
```

### Multiple async operations

- You need to call stop multiple times if more than one async op in the test, otherwise you will get a false positive (passing test that is not reliable)

```javascript
module("Asynchronous Tests");

test("broken synchronous timing test", function () {
  // call the stop function to pause running tests until notified
  stop(2); // pass in param to tell how many starts to wait for before resuming the test.

  // call again for more async ops - QUnit knows it's waiting for two calls to start() before it can continue.
  //   stop();

  setTimeout(function () {
    ok(true);
    // tell QUnit to resume running the test with start()
    start(); // resume test running when this async callback is run
  }, 2000);
  // another async op
  setTimeout(function () {
    ok(true);
    // tell QUnit to resume running the test with start()
    start(); // resume test running when this async callback is run
  }, 100);
});
```

### Best way to write async tests

- use the builtin `asyncTest`

```javascript
module("Asynchronous Tests");

asyncTest("broken synchronous timing test", function () {
  // no need to use stop(), just retain calls to start()
  setTimeout(function () {
    ok(true);
    start();
  }, 2000);

  // another async op
  setTimeout(function () {
    ok(true);
    start();
  }, 100);
});
```

### Qunit settings
- Check the no trycatch option in the UI to get better errors on your test failures.
  - see [video](https://app.pluralsight.com/ilx/video-courses/74d86142-f3dd-4607-8b33-d3dbe2f83ccb/ca39bbdb-0ff5-4b78-9fec-88e759ae9203/7db88e1c-5677-492a-b11e-f8c0d8447d01) at timestamp 2:10
