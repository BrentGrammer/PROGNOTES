# Testing and Debugging in CFML

- [Example Project with Testing](https://github.com/coldbox-modules/cbq/tree/main/tests)
- [Example test setup with CI/Github Actions](https://github.com/foundeo/cfml-ci-examples/blob/master/.github/workflows/release.yml)
  - Also see [Dockerfile](https://github.com/foundeo/cfml-ci-examples/blob/master/Dockerfile)

## TestBox

- See resources in [video](https://www.youtube.com/watch?v=0bEfrWit_as) at 49:30
- See [resrouce for list of tools](https://www.carehart.org/cf411/#testing)
- [TestBox](https://testbox.ortusbooks.com/)
  - next-generation testing framework for ColdFusion (CFML) that is based on BDD (Behavior Driven Development) for providing a clean, obvious syntax for writing tests. It contains a testing framework, runner, assertions, and expectations library and ships with a mocking and stubbing library.
- `writeDump()` - useful for debugging complex values to the console.
  - Important: Adobe Engines have a very evil setting called Report Execution Times, make sure it is always turned OFF. If you use it with any application that leverages Components, it will slow down your application tremendously.
- Debugging Templates: CFML Engines also allow you to turn on/off a debugging template that shows up at the bottom of requests when running in server mode. You can activate this debugging by logging in to the appropriate engine administrator and looking for the debugging section. Turn it on and debug like a champ.

### Installation

- box install testbox
- when you do box install textbox it'll create a box.json file which tracks dependancies and versions etc, which is how the box install knows what to go and grab
- ask other developers to run box install after pulling the repo, which will get the latest and greatest packages (commandbox has a package manager similar to npm)

### Gitignore:

- gitignore the testbox directory.
  - don't have a node_modules folder in cfml and like in node

### Example test

```javascript
component extends="testbox.system.BaseSpec" {

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
component extends="testbox.system.BaseSpec" {
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
