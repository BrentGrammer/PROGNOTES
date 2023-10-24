USEEFFECT:



-----


Make sure to default a value you're passing in for initial state:

<Greeting initial={} />

const Greeting = ({ initial = '' }) => {
  <input value={initial} ... />
}

this solves the warning of a controlled input switching to controlled input.


Lesson 3:

Be careful about expensive calls passed as initial value into useState().

React.useState will run the argument function passed in as initial argument on every render, but it will ignore using it as the value since it is tracking state over time.
Primitives are cheap so setting those as initial values is no big deal.

Ex:
const [name, setName] = React.useState(window.localStorage.getItem('name'))
// runs local storage call on every render

getting local storage is expensive and run everytime.  If we want to prevent it from being re-run, pass it in wrapped as a function:

LAZY STATE INITIALIZERS:

React.useState(() => window.localStorage.getItem('name'));
// This only runs one time. this is Lazy State Initialization. React will not call this after it does not need the initial value anymore

*Don't do this unless your state initialization is expensive.  Primitives are cheap to re-create.

--------

USE EFFECT:
The whole point of the dependency array in useEffect is to sync the state of the world with the state of the app.

useEffect dependencies are compared shallowly, so do not use objects or complex types in the deps list - you could get a re-run of the effect every render. (Effect Dependencies vid)

Listing empty array (no dependencies listed) means you depend on nothing.
Leaving out the dependency array means you depend on everything.

*Careful about cleanup functions - you only might want them to run once so that what they're cleaning up isn't re-initialized unnecessarily on every render, so make sure the dependency array is empty: []


------

USEREF:
- Allows you to mutate a value (stored in the current property of ref) without triggering a re-render.
(if you want a re-render, then you use useState)

Note: you cannot use the ref={ref} prop on a functional component directly since they do not have instances.  You can only use ref prop on a DOM node (i.e. an input or div etc.)



LESSON 4: Hooks Flow:

- First Render: lazy initializers are run (functions passed into useState)
- React updates DOM (with our component html/css)
- Browser paints the screen with out component
 - component finishes rendering - 
- UseEffects are run

Phases are:
 MOUNT
 UPDATE
 UNMOUNT

*Re-rendering/state updates in a child component do not cause the parent component to re-render.
If the parent re-renders then the child component will re-render as well.


7:30 - React does not call a render for your components (children) immediately after running the parent component (<App>).  It just creates the element in memory.
*Children are rendered AFTER the parent component completes it's render.


----

USEREF:

1:50 lesson 7 of hooks, in the Solution video
- when your component returns that just creates a UI object descriptor which eventually gets rendered to the DOM as a DOM node.
- When it is rendered to the DOM, React sees the ref prop and useRef hook and assigns a "current" property to the node

(why devtools shows different values when expanding log: it logs before the value has been defined, but when you expand the logged obj, the updating of it's property has already happened. Devools updates the innards of that object to help out, so when you expand it, you see the updated vals.)


***Interact with useRef current props inside a useEffect hook - you need current to be set after the render occurs and the component is mounted, so you can only get it's populated value in the useEffect.
 
----


USEREDUCER:

returns the current state and a function you can call which you pass a value that is passed to the reducer function

NOTE: the dispatch we get back from useReducer is stable and does not change between renders - so if you abstract it and are asked by ESLint to put it in a dependencies hook list, then it's okay, you won't get a infinite loop.

const [state, dispatch] = useReducer(reducerFunc, initialState)

// this returns the updated state - it has injected the current state and whatever is passed into the dispatch function returned in the second parameter here.
const reducerFunc(state, action) => ({
  switch(action.type) {
    case 'INCREMENT':
      return {count: state.count + 1)
    default: {
      return state
    } 
})

// in component:

const myClickHandler = () => dispatch({ type: 'INCREMENT' })

------

USECALLBACK:

- solves the problem of a inner component function you need to call in a useEffect that is called every render in a dependency list - infinite loop.  Because it is in the component and not coming from an external module, it is possible it could change, so React wants it in the dependency list.

Example is fetching data that depends on setting state inside the functioncomponent body.

const fetchstuff = (forminput) => ...fetchdata(forminput);

useEffect(() => { data = fetchstuff(); setdata(data) }, [fetchstuff])
// fetchstuff is new everytime the component re-renders because it is defined in the component function body.  This will cause infinite loops.

Extract Logic into Hook video has a good example of using pending resolved rejected statuses for async requests to update state with a reducer.

Solution:

const memoized = useCallback(() => {
  return fetchData(dynamicParam)
}, [dynamicParam])

// this memoizes the function.  if the dynamic param does not change from the last render then the function will not be redefined triggering the infinite loop becuase of the deps list depending on it.

-------------


USECONTEXT:

Used to share implicit state between two components in a part of the component tree

Ex:

const CountContext = React.createContext()

// we encapsulate the context provider state so children components passed as props can hook into this context  
function CountProvider(props) {
  const [count, setCount] = React.useState(0);
  const value = [count,setCount]
  return <CountContext.Provider value={value} {...props} />
}

function CountDisplay(){
  const [count] = React.useContext(CountContext)
  return <p>{count}</p>
}

function Counter() {
  const [ ,setCount] = React.useContext(CountContext)
  // update the context state using it's setCount returned for you:
  const increment = () => setCount(c => c + 1)
  return <button onClick={increment}>Increment</button>
}

// wrap our components in the count provider abstraction
function App() {
  return {
    <CountProvider>
      <CountDisplay />
      <Counter />
    </CountProvider>
  }
}


Note: useful pattern to prevent errors if components are outside of a provider and trying to access a context is to wrap the context and null check in a custom hook:

function useCount() {
  const context = useContext(CountContext)
  if (!context)
    throw new Error('useCount Error: used outside of provider.)
 
  return context;
}

// now just use useCount in your components


-----
 
USELAYOUTEFFCT:

- Prevents janky UX when updating observable changes to the DOM with useEffect because that code runs after the browser has painted the screen and visually updated it.  
- use useLayoutEffect when you make changes to the DOM that will change how the browser paints the screen.
***It fires before the browser paints the screen whereas useEffect fires after the paint.

It can also be useful if you need some code to run before any other code or useEffects are run in the component.


----

USEMEMO:

- use this when you have a expensive calculation that returns the same result given the same inputs.

ex: 
- You have a large list of items to process based on user input:

const allItems = getItem(inputValue); // very expensive, list is 10,000 items big for ex.

return (
  <>
    {allItems.map(item => <Item item={item} />)}
  </>
)

// to prevent this calculation on every render if the input didn't change, use useMemo:

const allItems = useMemo(() => getItem(inputValue), [inputValue]) 
// will not rerun calc if inputValue didn't change.  If the component re-renders for some reason other than the inputValue change, then the calculation will not be re-run