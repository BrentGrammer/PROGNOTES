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
