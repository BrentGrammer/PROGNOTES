# HOOKS

- Hooks are State that is attached to each fiber node.

  - a linked list as one hook connects to another as you use them
  - hooks each have their own state as well.

- Hooks are POJOs, objects, that are linked to Fiber Nodes. i.e. throgh the next prop on a linked list node.
- A Hook can have a next prop that points to another hook (also a linked list setup)
- In other words, the nodes in a linked list can have a linked list of hooks attached to them.
  Hooks are like objects that are hooked and hanging off of branches in the tree - they are not actual nodes on the fiber tree, but attachments to a node/branch (like a bird feeder hanging on a branch of a tree).

- Each Fiber node has a state prop (i.e. memoizedState). and Each hook has state as well.

### FLUSH:

To emtpy a structure of it's data and deal with the data.

## HOOK QUEUES:

- Hooks also have a queue
- React uses queues to flush data and set it up in a queue to handle in an order.
  - allows for updating state with requests when it decides it is best to deal with them, i.e. it can batch them.

UPDATING STATE AND RECALCULATING (RE-RENDER):

- Where state lives (where the hook is attached) determines which part of the tree should be updated when it changes

  - React recalculates when state changes automatically - The function component is re-run to see the output and to see if the state is different from what is registered (in the current virtual DOM tree)

- When dispatch is called on a hook, a re-render will be scheduled for the fiber node it is attached to and the function component representing the fiber node will be re-run along with any other functions inside it or children.

Walk through of useReducer hook source code in react-dom development source: https://dontimitateunderstand.com/courses/understanding-react/lectures/46000850

\*\*Always return a new object or state - do not mutate and return the existing one to make things deterministic

## USESTATE HOOK:

- Really it is a specialized version of useReducer() hook.
- if state is complex, you should use useReducer hook instead.

### Initial state/mounting

- The initial value of a useState hook is always discarded on re-renders - it only has an effect when the component mounts.

### USING MULTIPLE HOOKS IN A COMPONENT:

- If using more than one hook (i.e. useState more than one time or a combination of hooks), each hook is added to the hook queue in the order they are called.
  - when the component renders it calls the hooks in the order they are in the queue/linked list created by the declaration of them in the component.

NOTE: \*\*The queue for the hooks is set up ONCE on the first mounting of the component! This is why you cannot use hooks in if conditions or loops as the behavior would be inconsistent (the next links wouild be different) on future re-renders

Ex:

```javascript
const [state1, setState1] = useState("something")
const [state2, setState2] = useState("something2")

// first hook call is added to the fiber node (under 'memoizedState')
// the second hook will be in the `next` prop of the first hook so that state1 hook points to state2 hook.

{
  ...fiberNodeprops,
  memoizedState: {
    ...otherprops...,
    next: state2hook object
  }
}
```

- Note: when the function component is called on a re-render, it will see that the hooks are already there and will not re-create them.

## CALLING HOOKS MULTIPLE TIMES:

- hooks reference a closure variable so calling them in the same handler will reference the value set when the component function is run, and not update state each time!
  from https://dontimitateunderstand.com/courses/understanding-react/lectures/47896716

```javascript
const [numClicks, setNumClicks] = useState(0);

const handleClick = () => {
  setNumClicks(numClicks + 1); // numClicks = 0, new state = 1
  setNumClicks(numClicks + 1); // numClicks still is 0!! new state will be set to 1 again!
  setNumClicks(numClicks + 1); // same as above..
};
// handler is called after the component function has run, the handler remembers the closure value of numClicks that was created when the component ran and the state was set to 0 at that time.
```

#### Correct way to do this:

- If you need to call the state update several times in a single handler, then you can pass it a function which will have latest state injected on each call instead of relying on the closure as above:

from https://dontimitateunderstand.com/courses/understanding-react/lectures/47896716 at timestamp 6:58

```javascript
const handleClick = () => {
  setNumClicks((n) => n + 1);
  setNumClicks((n) => n + 1);
  setNumClicks((n) => n + 1); // this will update the counter by 3 each time the handler is called
};
```

\*\*\*BATCHING: Note that react will batch the multiple state setting calls above in one batch after the handler finishes running, it will not update on each call (which would cause an entire re-render each time)
