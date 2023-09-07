**Software should be regularly changed otherwise it becomes rigid.**

The whole point of software and why it's valuable is that it can be changed easily.

Tests written thoroughly are how you can regularly change software. Merciless refactoring. Everytime you work on the code improve it a little bit. The tests give you confidence on constant changes.
Make small light weih

60 hours a week, 40 are for employer and 20 are for your development, studying whatever you want.

### Topics to review:

Nossi Schneider chart
Mele and Morris state machine
Quicksort algo from memory
Transform analysis term
Tramp data term
Parniss table
Kinasis term
Kinaisensce term

Writing bug free software is virtually impossible. The goal is to reach an asymptote of 0 bugs over time through experience.
Eventually you will make a mistake.

Professionals are not timid, but confident. They take calculated risks but understand that eventually they will make a mistake. The reaction to that should be to laugh.

Managers have a job to do just like you. You need to work with them towards a best outcome. They will demand unreasonable deadlines and you need to say no (agreeing to the impossible will just result in shipping broken software and hiring users and the business).
Compromise and negotiation is needed, and understanding you are both just doing your jobs (their job is just to demand deadlines etc)

### Ambiguous Requirements

Acceptance tests:
Best way to resolve ambiguity of requirements and communication is acceptance tests.
They are defined by the business and their audience is the business(as opposed to unit tests whose audience is developers).
They serve as a specification of how the system should behave and clearly formally define the definition of done and requirements.
The definition of done is when all acceptance tests pass. They should be automated, much cheaper than manual acceptance tests

Ex: given when then tests can describe a business use case thoroughly and formally and acceptance tests can come in this form. It's then the developers job to implement the test.

### Testing the GUI:

GUI is volatile and difficult to treat, it changes frequently. Should have minimal tests on GUI only if absolutely needed.
Should test an API layer just below the GUI that contains business logic that the GUI calls and uses.
If you need to test the GUI, stub out the business logic it calls so you only test the GUI.
Better to get buttons and c elements by name or id than position.
