FIBER TREE
- Another tree React creates to represent what the current state is and what work needs to be done to update the real DOM to match what you want.
- WORK IN PROGRESS NODES - A alternate slice of a tree that is set with the Fiber Tree current state. When work is done, the reference to the current and the alternate tree slices are switched so the alternate/'work in progress' becomes the current slice in the Fiber tree.

*There are three trees involved
- The react element tree (produced from your JSX)
- The Fiber Tree (current and alternate/future state representation)
  - There are two branches/versions of this tree - the Current and Work In Progress branches
  - more explanation around 1:00 here: https://dontimitateunderstand.com/courses/understanding-react/lectures/48480398
  - Think of tree management as a Ping Pong game of back and forth between the Current and Work In Progress branches (calling the function component over and over and comparing/updating the branches each time and cleaning up (i.e. useEffect destroy))
- The DOM Tree (actual rendered tree that gets updated on committing units of work/reconciliation).

Note on Reconciliation/Unmounting:
- Reconciliation is done in the most efficient way possible
- Unmounting a component does not necessarily mean that all of it's underlying elements are removed from the DOM or destroyed.
- If the replacement component or future/alternate Fiber tree is similar elements to what is already in the DOM, then reconciliation could work to reuse them or not remove them, for example.
  - One implication of this is that if you are swapping out components, try to make the replacement component similar in structure to what is already there.

TREE EDIT DISTANCE PROBLEM:
- What is the best algorithm with the shortest steps to compare and reconcile two trees.
- Reconcile: To compare two values and determine how to update one to match the other.

Examples of reconciliation:
- React might look at the work in progress in the Fiber tree to be used as the new current and determine what the most efficient way to update is - i.e. remove one <li> from a list or if the work is very complicated with nested elements, it may decide to delete the entire <ul> and replace it.

Looking at the work React does in the console.:
 - you can log out Fiber Nodes (look up how to do this or watch Tony's vids) - you need to find in the react dom development source code where to log.
 - A FiberNode will have a deletions property showing what React decides to delete with a flag (flags property) that corresponds to a action code (can see the source code for flags in React DOM source.

UNIT OF WORK:
- React has a Work loop that checks if there are units of work that need to be done.
- A Unit of Work is a Fiber Node (which will have flags and properties indicating what React needs to do for a particular slice of the Tree (DOM etc)).

React goes through the Fiber Tree and checks if there is work that needs to be done, if there is not it bails out, if there is then it performs a unit of work (actions specified by a FiberNode that requires updating the DOM).

LANES:
- React uses lanes (integers in the code) to determine the order and priority of units of work.

FLUSHING STATE:
- 3:56 of Beginning, Completing, Bailing Out and Pausing Work video in course.
- Flushed meaning everything has been processed (i.e. in the fiber tree/DOM updates)
- React has flags for beginning, pausing or bailing out work and also if work is completed.
  - One reason is it keeps track of the work cycle to allow the browser to run other events in the queue (i.e. an animation, timeout callback, etc) to keep things running smoothly and not block the UI or UX.