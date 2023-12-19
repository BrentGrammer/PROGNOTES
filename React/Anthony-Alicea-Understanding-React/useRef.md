# useRef

- Stores a value, but does not trigger a re-render when the value is changed (unlike useState for ex.)
- Like other hooks is an object attached to a fiber node
- Should be used in instances where you don't need the UI to update when the value changes!

```javascript
// returns an object so it can be passed around by reference (as a place in memory)
const numClicksRef = React.useRef({ total: 0 });

function handleClick() {
  numOfClicksRef.current.total += 1;
  alert(numOfClicksRef.current); // will update on every click and show current number
}

return <p>{numOfClicksRef.current}</p>; // will stay at zero since changing ref does not queue a re-render
```

### Using useRef to access DOM elements

- Sometimes you may need to access the actual DOM nodes
  - For example, since React renders and re-renders, you may need to do something just one time on a DOM node on the first render
- Should be used with caution only if you can't find a builtin declarative way to do what you need.

```javascript
function Counter() {
  const buttonRef = React.useRef();

  React.useEffect(() => {
    // access the actual DOM node after rendering is complete and operate on it as in vanilla JS
    buttonRef.current.focus(); // focus the button only once after the initial render
  }, []);

  // pass in the ref object to the jsx element to get a reference to the actual DOM node after all reconciliation and rendering is complete.
  return <button ref={buttonRef}>Focused on render</button>;
}
```

## forwardRef

- Used when we want parent components to reference a DOM element within a child component

```javascript
function App() {
  const buttonRef = React.useRef();

  React.useEffect(() => {
    buttonRef.current.focus();
  }, []);

  // pass ref cretaed in parent to child component ref prop
  return (
    <>
      <Counter ref={buttonRef} />; // only focus the first one - control by
      parent
      <Counter />;
    </>
  );
}

//wrap the component in forwardRef which will allow the function to be called with an extra argument after props containing a ref passed in in the parent component
const Counter = React.forwardRef(function ChildComponent(props, buttonRef) {
  return <button ref={buttonRef}>Focused on render</button>;
});
```
