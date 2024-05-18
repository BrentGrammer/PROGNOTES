# Testing and Debugging in CFML

## TestBox

- See resources in [video](https://www.youtube.com/watch?v=0bEfrWit_as) at 49:30
- See [resrouce for list of tools](https://www.carehart.org/cf411/#testing)
- [TestBox](https://testbox.ortusbooks.com/)
  - next-generation testing framework for ColdFusion (CFML) that is based on BDD (Behavior Driven Development) for providing a clean, obvious syntax for writing tests. It contains a testing framework, runner, assertions, and expectations library and ships with a mocking and stubbing library.
- `writeDump()` - useful for debugging complex values to the console.
  - Important: Adobe Engines have a very evil setting called Report Execution Times, make sure it is always turned OFF. If you use it with any application that leverages Components, it will slow down your application tremendously.
- Debugging Templates: CFML Engines also allow you to turn on/off a debugging template that shows up at the bottom of requests when running in server mode. You can activate this debugging by logging in to the appropriate engine administrator and looking for the debugging section. Turn it on and debug like a champ.
