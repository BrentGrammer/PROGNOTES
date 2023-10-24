Explanation of using Profiler in React.memo for Reducing re-renders section video titled Intro at 2:32.

Click record, press event etc., stop recording.
Flame graph shows commits - at the top there is a commit bar graph - colored means DOM changes were made on the commit, gray means no changes

In settings can set threshold to show components that rendered in certain time.
Can show ranking of components by most time to least as well.


----

CODE SPLITTING

- Download less code and only the code that is needed by the user at a given time.
- Use Lazy imports to only load your component when it is needed.
Note: the imported file needs to have a default export

NOTE: with lazy loads the browser or webpack if using it maintains a cache 

Use React.lazy to only import the component when it is needed on the page.
  - This automatically code splits for you without manual configuration


This is built on top of async dynamic imports which return a promise 
import('./async-script.js').then(
  moduleExports => {
    moduleExports.go()
  },
  error => {
    console.error('there was an error loading the script')
    throw error
  },
)

For ex, you have a checkbox to load a component using D3 which is a large download.  You only need to import the component using D3 after the check is checked

- note: wrap lazily loaded component in a Suspense with fallback to prevent white screen of death

const Globe = React.lazy(() => import('../globe'))

function App() {
  <Checkbox />
  <React.Suspense fallback={<Loading />}>
    {showGlobe && <Globe />}
  </React.Suspense>
}

--- 

EAGER LOADING:

- When a user makes an action that indicates they want to load a resource (i.e. mouse hover over a checkbox, etc.) start eager loading the resource so it's ready by or when they click).

ex:

function Comp() {
  <form>
    <label onMouseEnter={loadGlobe} onFocus={loadGlobe} /> 
    <input type="checkbox" ... />
  </form>
}

// kick off the lazy load of 
function loadGlobe()

----

REACT.MEMO

You can opt out of re-render phase in components by using React.PureComponent or React.memo.

Read article on fixing slow render before re-render fixes: https://kentcdodds.com/blog/fix-the-slow-render-before-you-fix-the-re-render

function MyComp() {
}
MyComp = React.memo(MyComp); // reassign to memoized version.

Second argument is a function that you use to look at previous props and next props for comparison.
- if you return true, then you will not re-render, if you return false a re-render will trigger

React.memo(MyComp, (prevProps, nextProps) => {
  // compare prevProp to a nextProp and return true or false:
  return nextProp.index !== nextProp.highlightedIndex; 
  // returns true if current list item is not highlighted, so it will not re-render
})


**Do calculations higher in the tree so you only pass primitives to memoized component
****Pass primitives to React.memo components so you don't need to write custom comparators.
If you pass an object and need to compare slices or parts of the state to determine whether to re-render then things get complicated.  Eliminate the complexity by moving your logic higher in the component tree to the parent for example and just pass a primitive result from it:

<Parent
  isSelected={selectedItem?.id === item.id}
  isHighlighted={highlightedIndex}
/>

function ListItem({ isSelected, isHighlighted }) {...}

React.memo(ListItem) 
// no need for comparator on object prop passed in, only if primitives change, component will re-render
	


-----

COLOCATE STATE:

Careful about what you keep in Global State. Only store what you truly need to share and it might be better to just use prop drilling if shared state is going to cause unnecessary re-renders.

- Put state as close to the component that needs it. 
- Minimized re-renders of other components 

If you can split the context holding state into logical parts and only wrap the comonents concerned with that state, then that is another way to colocate state.

**Remember to measure your performance with the Profiler tab in devtools.  Press record and perform an action to rerender, then stop recording.  Look at the time in ms the event took etc.
You can adjust the CPU slowdown (i.e. put it to 6x in the dropdown) to make it easier to compare measurements.
focus on the click or input key events for the number to look at

--

- Create a Implementation/Consumer Component to get a slice of state:
// create man in the middle consumer component that passes the slice of state to an implementation
let Cell = ({row, col}) => {
  const largeState = useAppState()
  const cell = state.grid[row][col]
  // by passing state slice and memoizing comp, it won't re-render when any piece of global state is changed.
  return <CellImpl cell={cell} row={row} column={col} />
}
Cell = React.memo(Cell)

let CellImpl = (props) => {
  ... implementation, logic etc.
  return <button>Click me</button>
}
CellImpl = React.memo(CellImpl)


**From the video Slice of App State from the Performance lectures, Fix Perf Death by a thousand cuts
- BETTER: make a generic consumer component for a slice of state:

- with this pattern, the component needing a slice of state will only re-render when it's slice of state is changed.

// slice is a function user passes in to get the slice of state they want
// the Wrapper also passes a state prop to the component passed in so the inner component can work with it.
function withStateSlice(Comp, slice) {
  const MemoComp = React.memo(Comp)
  function Wrapper(props) {
    const state = useAppState()
    return <MemoComp state={slice(state, props)} {...props} />
  }
  // helps with debugging showing name in REact devtools for component instead of just 'Wrapper'.
  // note this doesn't work with components wrapped in React.memo
  Wrapper.displayName = `withStateSlice(${Comp.displayName || Comp.name})`

  return React.memo(Wrapper)
}

// previously CellImpl
let Cell = ({state: cell, row, col}) => {
  ... implementation, logic etc. using row and cell, updating global piece of state etc.
  return <button>{cell}</button>
} 

Cell = withStateSlice(Cell, (state, props) => state.grid[props.row][props.col])



------


FPS: 60 fps 
You need your operations to run about in about 16 milliseconds (click events, etc.) in order not to drop frames at 60 fps


----


WEB WORKERS:

- You can use sometihng like Workerize library to make your expensive functions run in a web worker on another thread so it doens't block the UI thread in JavaScript.  

- The main strategy is to run an async operation on a web worker thread which frees the main browser thread to keep running.
- When the async operation finishes on the separate thread, the data returned can be caught in an async custom hook that you use in a useEffect having the data as a dependency.  When it updates the component re-renders with the new data fetched in the background thread and the main thread was not blocked.


------

OPTIMIZE CONTEXTS:

- Be careful about components that consume a context value or are children or parents that consume a context value.

Context value is compared with a SHALLOW comparison by React,(i.e. using Object.is or ===) so even if the elements of an object or array are identical, React sees this as a new obj or array and triggers a re-render.

- KCD explains what can happen in the Memoize context value video under part 6 of performance at 2:00.
https://epicreact.dev/modules/react-performance/optimize-context-value-solution

A solution is to memoize the state in the provider with useMemo:

// in this example state is an array of elements to show in a list.
function AppProvider({children}) {
  const [state, dispatch] = React.useReducer(appReducer, {});

  const value = React.useMemo(() => [state, dispatch], [state]); // state is a new array even if has same els.
  return (
    <AppStateContext.Provider value={value}>
      {children}
    </AppStateContext.Provider>
  )
}

// useMemo will check the value of state now and if the same elements, will not re-render.


SEPARATE CONTEXTS:

- If components do not need all the parts of a context value then split the context so that components can use only the parts of it's value that they need:

// create separate context and providers for pieces of original context value:
const AppStateContext = React.createContext();
const AppDispatchContext = React.createContext();

function AppProvider({children}) {
  const [state, dispatch] = React.useReducer(appReducer, {
    ..initial state
  });
  return (
    <AppStateContext.Provider value={state}>
      <AppDispatchContext.Provider value={dispatch}>
        {children}
      </AppDispatchContext.Provider>
    </AppStateContext.Provider>
  );
}

// create hooks for consuming the different contexts:
function useAppDispatch() {
  const context = React.useContext(AppDispatchContext);
  if (!context) {
	throw new Error();
  }
  return context;
}

function useAppState() {
  const context = React.useContext(AppStateContext);
  if (!context) {
	throw new Error();
  }
  return context;
}

// use either or the other or both in different components that need them so stop re-renders from state changes if the component only needs the dispatch part:

function Cell() {
  const state = useAppState()
  ...
}
// the grid only needs a dispatch to send something to update the state of cells.  not using state in here prevents Grid from re-rendering.  Since the context providers are referencing children prop, the wrapper with state will not update this component since props are not re-created (try reading KCDs article One Simple trick to optimize React re-renders for a crappy explanation).
function Grid() {
  const dispatch = useAppDispatch()
  ...
}