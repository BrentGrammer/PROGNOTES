# Agentic A.I.

### Recommended Resources

- [A.I. Assisted Development by Anthony Alicea](https://dontimitate.dev/courses/ai-assisted-development/)
- [Clean Coders Agentic Discipline](https://cleancoders.com/episode/agentic-discipline-4)

## Tools

- Browser agents:
  - Browser-use: A Python library. Highly automated, but unpredictable.
  - Playwright with LangGraph. More granular control with Playwright. Leverages LangChain's LangGraph
- Ollama - local models you can download to run on your machine. Qwen models, etc.
- Coding agents:
  - Aider
  - OpenCode

## Principles

- Productivity can be gained by letting the agents do what they're good at (syntax, low level programming, writing the code) and can do faster than you can.
- Agents must be closely monitored and managed. They will make mistakes. Your job is to manage and guide the agent to follow good design, good architecture, good software principles.
- Agents should only be relied on to take care of low level detail syntax. High level software development is still required by people - the design, the components, how functions relate to each other, the names of functions, the arguments of functions, etc. etc.

## Good Practices and tendencies of A.I. agents

- Constraints and Physical Barriers must be put in place to protect against actions the agent will take that are not desired.
- Agents have poor long term memory and recency bias. What is at the beginning of the context window will be less important than what is at the end of the window.

### Implementation Plans

- Detailed implementation plans for complex features are needed.
- Store these plans in a file that the A.I. can read so it is retrieved for the context window every time. The plan can then be persisted across phase runs, put back into the context window and remain unaltered from the original.
- You must have checkpoints and run the plan in small phases. You need to stop and inspect and review at each checkpoint and phase.

### Testing

- Have the agent right tests, lots of them. These tests will change as the program is developed
  - The tests provide Constraints and back pressure to keep the A.I. agent from diverging wildly from the intent and desired behavior of the program
- Have the agent reach very high coverage (> 90%)

#### Acceptance Tests

- **Use Acceptance Tests as the source of truth**
  - Gherkin Syntax (GIVEN the system is in state X, WHEN I do action A, THEN the system will be in state Y)
  - Have the A.I. agent write a parser to turn the Acceptance Tests Gherkin syntax into actual unit-like tests (using your tool like Jest or JUnit etc)
  - Review the tests - the Acceptance Tests should not change unless you permit the change.
  - The distance from the text, parser to the unit-like tests prevents the A.I. from changing the Acceptance Tests too much

#### Mutation Tests

- Use Mutation Tests
- Build a mutation tester
- This tool reaches into the source code and makes changes in key spots, then runs the tests. If the tests pass, that means there are surviving Mutants. Tell the A.I. agent to then kill the surviving mutants.
- Note: this takes a lot of time and compute power because the entire suite of tests will be run for each mutation in a single source file, for example. You can run these on multiple cores in parallel to try to help speed up the process.
- Mutation tests increase coverage and test all assertions, all comparators, operators etc. - adds semantic stability and prevents A.I. agent from cheating more.
- Semantic Stability has a cost - if you want to make a change to the system, there is a high cost to redoing the tests. Do not do Mutation Testing if you are in the middle of development. Wait until you are more or less done with the module.

### Run a C.R.A.P. tool

- This tool measures cyclomatic complexity in the source code.
- This will identify functions with a high level of C.C. and you can ask the A.I. agents to reduce the "CRAP" in the system.
  - This will do things like take big functions with high number of branches and split them up into smaller, simpler functions.

### Run a Linter

- Use a linter to check code quality as well.
- This will correct parantheses or braces errors the A.I. might make mistakes on.
  - If the parens or braces is higher than a few of them, the A.I. cannot count them and loses track.
  - The linter tells the A.I. where to put the closing braces and parens.

### Dependency Checker

- tool inspects the source code, follows the depency import statements, etc. and builds a map of the dependency structure.
- Can be used to allow or disallow certain dependencies.
- The goal is to get it so that low level modules depend on high level modules, and high level modules do not depend on low level modules.
- This will help the agent how to identify how to partition and split modules based on the results of the dependency checker tool fed to the A.I. agent.
  - This will break apart big modules and break things down better, etc.

### Debugging

- Ask the A.I. agent questions about details.
  - state, internal details etc.
- The A.I. agent can produce stack traces, giving you information about the paths through code, make tables you ask it to, etc.
  - it can build tools and produce maps of components, structure and details of the software system for you
- The inevitable slog of debugging will not go away and can reduce the speed or productivity gains back to normal levels, negating any productivity gains.

### Performance Enhancements

- A.I. is very good at finding ways to improve performance and should be leveraged.
- Ask the Agent about profiling and measuring the system if it is slow.
- This can help guide you to the correct place the bottleneck is.

### Building tools

- Point A.I. at prototypes or other tools that exist as an example and ask it to build a tool like that for your specific use case.
