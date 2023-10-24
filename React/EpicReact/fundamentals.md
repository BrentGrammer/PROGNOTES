Components are functions that return something that is renderable - numbers, react elements, null, strings etc..

JSX:
- Babel takes our jsx and compiles it to React.createElement(...) calls.
Ex: ui = <Capitalized /> // React.createElement(Capitalized)

React useState runs every render

JSX when it's returned, called in the render() method just creates UI descriptor objects - (React.createElement(compEl))
Ultimately these React elements will be rendered to the page.

----

State Batching Updates

- They are batched if in a React Event Handler
- They are not batched if they are in an asynchronous callback. (this changes in React 18)

----

Phases:  *This cycle is triggered on initial render and on state changes.

Render Phase: creates react elements - with React.createElement

Reconciliation Phase: compares previous elements with the new ones

Commit Phase:  update the DOM if needed.

Reasons for Re-renders:
- Props change.
- Internal state changes
- Component is consuming context values which changed
- Component's parent re-renders

---

Be careful about unnecessarily lifting state - if state is not needed by any but one component, then move it there to prevent unnecessary re-renders triggered by the parent.

Note: React cannot batch updates in asynchronous callbacks (i.e. .then())
Ex:

const [status, setStatus] = useState('idle')
const [data, setData] = useState(null)

useEffect(() => {
  fetchSomething().then(res => {
    setStatus('resolved')
    setData(res)
  })
})

**React will re-render after setStatus is called and component trying to show data will try to show null until setData completes after. See full explanation in lesson 8 of React-Hooks, the video Store the State in an Object extra credit.

----

Errors:

If a render error is thrown and unhandled, then that causes the white screen of death - the application is removed from the page.

Use ErrorBoundaries to handle them.
**Use react-error-boundary package

Using a key prop on components to re-mount them:
you can use a key prop set to a piece of state that updates to re-mount the ErrorBoundary (or other component) to reset it's state. <ErrorBoundary key={pokemon} /> - Lesson 8 of React Hooks set, Re-mount Errorboundary 


-------


WARNING: Can't perform a React state update on an unmounted component...

This is usually caused by an asynchronous call (fetch data etc) that doesn't complete before a user navigates away to another component.  The call completes and then tries to update the state of the previous component.

Good full ex. with custom hook in Advanced Hooks set on section 3, useCallback, vid title: Make safeDispatch

You can solve this by using useRef to track whether the component is mounted or not and then conditionally make the asynchronous call if the component has not been unmounted.

Ex:
// useLayoutEffect does not wait for other events and fires before painting and as soon as component is unmounted
React.useLayoutEffect(() => {
  mountedRef.current= true;
  return () => {
    mountedRef.current = false; 
  } 
}, []}

// check mountedRef in your async func and only call if component is mounted.
const fetchStuff = async () => {
  if (mountedRef.current) fetch(data);
}
