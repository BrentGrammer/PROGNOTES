# Testing and Debugging in CFML

## Resources/Documentation

- [CFCasts videos](https://cfcasts.com/browse?q=testbox)
- [VS Code has a Testbox extension](https://cfcasts.com/series/2022-vs-code-hint-tip-and-trick-of-the-week/videos/testbox-vscode-testbox-vscode-hint-tip-and-trick-of-the-week-32222-episode-140)
- See [carehart.org for list of tools](https://www.carehart.org/cf411/#testing)
- See resources in [video](https://www.youtube.com/watch?v=0bEfrWit_as) at 49:30

## Example Repos with Tests

- [Example Project with Testing](https://github.com/coldbox-modules/cbq/tree/main/tests)
- [Another example project with tests](https://github.com/ColdBox/coldbox-zero-to-hero/tree/v7.x)
- [Example test setup with CI/Github Actions](https://github.com/foundeo/cfml-ci-examples/blob/master/.github/workflows/release.yml)
  - Also see [Dockerfile](https://github.com/foundeo/cfml-ci-examples/blob/master/Dockerfile)

### Using Testbox without Coldbox:

- [Using Testbox with non-Coldbox legacy app](https://github.com/nolanerck/testbox-for-non-coldbox-cfml/tree/master)
  - [See demo of testing legacy code here](https://youtu.be/0bEfrWit_as?t=2689)
  - [Testbox without Coldbox: CFCasts video 2020](https://cfcasts.com/series/itb-2020/videos/d2s7-ortus-testing-my-non-coldbox-site-with-testbox-nolan-erck)

## Debugging/logging

- `writeDump()` - useful for debugging complex values to the console.
  - Important: Adobe Engines have a very evil setting called Report Execution Times, make sure it is always turned OFF. If you use it with any application that leverages Components, it will slow down your application tremendously.
- Debugging Templates: CFML Engines also allow you to turn on/off a debugging template that shows up at the bottom of requests when running in server mode. You can activate this debugging by logging in to the appropriate engine administrator and looking for the debugging section. Turn it on and debug like a champ.

## TestBox

- [TestBox](https://testbox.ortusbooks.com/)
  - next-generation testing framework for ColdFusion (CFML). contains a testing framework, runner, assertions, and expectations library and ships with a mocking and stubbing library.

### Installation

- box install testbox
- when you do box install textbox it'll create a box.json file which tracks dependancies and versions etc, which is how the box install knows what to go and grab
- ask other developers to run box install after pulling the repo, which will get the latest and greatest packages (commandbox has a package manager similar to npm)

### Missing HTML Runner error:

- If you get an error about not being able to find system/runners/HTMLRunner.cfm,
  - check that the html runner file is present in testbox/system. If not, remove the testbox folder and reinstall with `box install`
  - You may need to kill docker containers running with bind mounds (volumes) running.
- Add a testbox mapping to the Application.cfc in /tests:

```java
component {

	this.name              = "A TestBox Runner Suite " & hash( getCurrentTemplatePath() );
	// any other application.cfc stuff goes below:
	this.sessionManagement = true;

	// any mappings go here, we create one that points to the root called test.
	this.mappings[ "/tests" ] = getDirectoryFromPath( getCurrentTemplatePath() );
	this.mappings[ "/testbox" ] = "testbox"; // resolves /testbox not found error

	// any orm definitions go here.

	// request start
	public boolean function onRequestStart( String targetPage ){
		return true;
	}

}
```

### Gitignore:

- gitignore the testbox directory.
  - don't have a node_modules folder in cfml and like in node
- box.json:

```json
"dependencies": {
  "testbox": "^2.1.1"
},
"installPaths":{
  "testbox": "testbox" // the folder where installed dep goes - gitignore this directory!
}
```

## Running Tests

- Easiest way for older apps is to use the browser runner:
  - `http://{domain}/testbox/tests/runner.cfm`
    - testbox/tests is the default folder where tests are expected (can be changed)
- [Sample XUnit style testing](https://cfcasts.com/series/itb-2020/videos/d2s7-ortus-testing-my-non-coldbox-site-with-testbox-nolan-erck/) at timestamp 18:00
- **Tests run in parallel and not necessarily in order from top to bottom of file**
- Command: `testbox run --noverbose`
  - only shows failing tests and top level stats.

### Specifying which directory to run

- http://localhost/.../runner.cfm?reporter=json
  - output in different format if needed
- http://localhost/.../runner.cfm?directory=/MyTests/1
  - specific nested folder - run tests there only
- /http://localhost/.../runner.cfm?directory=/MyTests/
  - run all tests nested in this folder
- http://localhost/MyTests/LoginTests.cfc?method=runremote
  - run a test file directly (without runner.cfc) by specifying runremote

### Example test

```javascript
component displayName="Some descriptive name" extends="testbox.system.BaseSpec" {

	/*********************************** LIFE CYCLE Methods ***********************************/

	// executes before all suites+specs in the run() method
	function beforeAll(){
	}

	// executes after all suites+specs in the run() method
	function afterAll(){
	}

	/*********************************** BDD SUITES ***********************************/

	function run(){
		feature( "Given-When-Then test language support", function(){
			scenario( "I want to be able to write tests using Given-When-Then language", function(){
				given( "I am using TestBox", function(){
					when( "I run this test suite", function(){
						then( "it should be supported", function(){
							expect( true ).toBe( true );
						} );
					} );
				} );
			} );
		} );
	}

}

// Non BDD - unit test style:
component displayName="Some descriptive name" extends="testbox.system.BaseSpec" {
  // executes before all suites+specs in the run() method
	function beforeAll(){
	}

	// executes after all suites+specs in the run() method
	function afterAll(){
	}

  function run( testResults, testBox ) {
    describe( "config bean", function() {
      it( "should do stuff", function() {
        var sut = new model.Config();
        expect( sut.stuff() ).toBe( true );
	  })
    })
  }
}
```

### Testing component compilation

- For legacy apps, good to test that cfc (components) can be initialized and compiled correctly:
  - see [video](https://cfcasts.com/series/cb-zero-to-hero/videos/creating-the-userservicecfc-tdd-style/) at timestamp 6:00

```javascript
function run() {
  describe("My Service", function () {
    it("can be created", function () {
      // ensures no syntax or compilation errors - test cfcs like models, etc.
      expect(myModel).toBeComponent();
    });
  });
}
```

- [Project with tests](https://github.com/ColdBox/coldbox-zero-to-hero/tree/v7.x)

## Render and save output in tests

- See [testing vid](https://cfcasts.com/series/itb-2020/videos/d2s7-ortus-testing-my-non-coldbox-site-with-testbox-nolan-erck/) at timestamp 41:40
- use `cfsavecontent` tag and set the output to a `variable` you can reference to make assertions.

```javascript
<cfcomponent displayName="Test rendered output" extends="testbox.system.BaseSpec">

  <cffunction name="testMyTagOutput">

    <cfsavecontent variable="myRenderedOutput">
      <cfmodule template="/views/MyView.cfm" />
    </cfsavecontent>

    <cfset $assert.isTrue( myRenderedOutput contains "something" ) />

  </cffunction>

</cfcomponent>

```

## Mockbox

- see [video](https://cfcasts.com/series/itb-2020/videos/d2s7-ortus-testing-my-non-coldbox-site-with-testbox-nolan-erck/) at 38:30

## Coverage

- Requires Fusion Reactor (paid license)
- Can turn code coverage off to make tests run faster in runner.cfm - set coverage param default="false"

## Integration Testing

### Tests that use the database

- Recommended to use a separate test database.
- [Wrap tests in Transactions using lifecycle annotations](https://testbox.ortusbooks.com/in-depth/life-cycle-methods/annotations)
  - This will automatically rollback changes made in the test (even if the test fails)

```java
component extends="coldbox.system.testing.BaseTestCase"{
// the annotation will run this method as if it were called in a aroundEach() lifecycle method
    /**
     * @aroundEach
     */
    function wrapInDBTransaction( spec, suite ){
        transaction action="begin" {
            try {
                arguments.spec.body();
            } catch (any e) {
                rethrow;
            } finally {
                transaction action="rollback"
            }
        }
     }
}
```

```java
// extend the test class you made above
component extends="DBTestCase"{

    function run() {
        given( "I have a two posts", function(){
            when( "I visit the home page", function(){
                then( "There should be two posts on the page", function(){
                    queryExecute( "INSERT INTO posts (body) VALUES ('Test Post One')" );
                    queryExecute( "INSERT INTO posts (body) VALUES ('Test Post Two')" );

                    var event = execute( event = "main.index", renderResults = true );

                    var content = event.getCollection().cbox_rendered_content;

                    expect(content).toMatch( "Test Post One" );
                    expect(content).toMatch( "Test Post Two" );
                });
            });
        });
    }
}
```

## Setup and Teardown

- `setUp()` and `tearDown()`: Use these methods within your test suites to set up the necessary context for your integration tests.
  - This might involve instantiating a subset of your application's object graph that is relevant to the integration boundary you are testing. You might still need to manually create some dependencies, but you can focus on the key collaborators.
- `beforeAll()` and `afterAll()`: If the setup for a group of integration tests is expensive (e.g., setting up database connections or external service stubs at a higher level), you can use `beforeAll()` and `afterAll()` to perform these actions once per test suite. Be cautious with `beforeAll()` as it can introduce state between tests if not managed carefully.

```java
component extends="testbox.system.BaseSpec" {

    variables.myObject = ""; // The thing we are testing

    /** Runs BEFORE EACH test (`it`). Setup fresh conditions. */
    function setUp() {
        variables.myObject = new path.to.MyComponent();
        // OR, setup test data:
        // variables.testData = { ... };
    }

    /** Runs AFTER EACH test (`it`). Clean up anything changed. */
    function tearDown() {
        variables.myObject = ""; // Reset the tested object
        // OR, clean up created files/data:
        // fileDelete(variables.tempFile);
    }

    function run() {
        describe("MyComponent", function() {
            it("should do something with initial state", function() {
                // 'variables.myObject' is fresh here
                variables.myObject.doAction(argument="initial");
                expect(variables.myObject.getResult()).toBeTrue();
            });

            it("should do something different after setup", function() {
                // 'variables.myObject' is a new, clean instance again
                variables.myObject.doAction(argument="different");
                expect(variables.myObject.getCount()).toBe(1);
            });
        });
    }

}
```

### Detailed Example

```java
component extends="testbox.system.BaseSpec" {

    variables.componentUnderTest = "";
    variables.testFilePath = getTempDirectory() & "/test_file.txt";
    variables.initialFileContent = "Initial content in the file.";

    /**
     * Runs before each individual 'it' block in this test suite.
     * Use this to set up the necessary conditions for each test.
     */
    function setUp() {
        // Create the test file with some initial content before each test
        fileWrite(variables.testFilePath, variables.initialFileContent);
        variables.componentUnderTest = new path.to.FileService(); // Instantiate the component under test
    }

    /**
     * Runs after each individual 'it' block in this test suite.
     * Use this to clean up any resources or state that might have been modified by the test.
     */
    function tearDown() {
        // Delete the test file after each test to ensure a clean state for the next test
        if (fileExists(variables.testFilePath)) {
            fileDelete(variables.testFilePath);
        }
        variables.componentUnderTest = ""; // Release the component instance
    }

    function run() {

        describe("FileService", function() {

            it("should read the initial content of the file", function() {
                // Arrange (setup is done in setUp())
                local.content = variables.componentUnderTest.readFile(variables.testFilePath);

                // Act & Assert
                expect(local.content).toBe(variables.initialFileContent);
            });

            it("should append new content to the file", function() {
                // Arrange (setup is done in setUp())
                local.newContent = "Appended content.";
                variables.componentUnderTest.appendToFile(variables.testFilePath, local.newContent);
                local.updatedContent = fileRead(variables.testFilePath);

                // Act & Assert
                expect(local.updatedContent).toBe(variables.initialFileContent & local.newContent);
            });

            it("should overwrite the existing content of the file", function() {
                // Arrange (setup is done in setUp())
                local.newContent = "Overwritten content.";
                variables.componentUnderTest.writeFile(variables.testFilePath, local.newContent);
                local.updatedContent = fileRead(variables.testFilePath);

                // Act & Assert
                expect(local.updatedContent).toBe(local.newContent);
            });

            it("should handle a non-existent file gracefully (example with mocking)", function() {
                // Arrange
                local.nonExistentPath = getTempDirectory() & "/non_existent_file.txt";
                variables.componentUnderTest = mock("path.to.FileService");
                variables.componentUnderTest.expects("readFile").withArgs(local.nonExistentPath).throws(new Exception("File not found"));

                // Act & Assert
                expect(function() { variables.componentUnderTest.readFile(local.nonExistentPath); }).toThrow("File not found");
            });

        });

    }

}
```
