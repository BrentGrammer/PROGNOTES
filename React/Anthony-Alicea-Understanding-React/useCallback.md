# useCallback

- Hook to memoize a function (not the result of a function like useMemo).

- Functions inside components are objects that are recreated with new memory addresses when the component re-renders.
- Memoizing with React.memo or useMemo will not prevent a recalculation/re-render because the functions are re-created on each component render/run with new addresses - they fail the Object.is() check React does under the hood. (i.e. in cases where the functions are passed down to a memoized child component as props)
- see [video](https://dontimitateunderstand.com/courses/understanding-react/lectures/50908158) at timestamp 4:40

## Use Case

- When passing a function as a prop to a memoized child component, when the parent re-renders that function is always going to be new (at a different location in memory when it's recreated in the parent's re-render).
- Usually used in conjunction with React.memo() for a memoized component (like useMemo is used in conjunction with React.memo as well)

```javascript
const Parent = () => {
  // stores function on a hook attached to this fiber node
  const myFunc = useCallback(() => {
    console.log("my memoized function does something");
  }, []); // empty dependencies array means same function will be used everytime. If your functions are dependent on some data, then add it to the array.

  return <Child myFunc={myFunc} />;
};

const Child = React.memo(({ myFunc }) => {
    // This child component will not re-render when parent holding myFunc re-renders because the function is memoized and will not be re-created in the parent everytime.

    // Otherwise React.memo would not work as expected because even though the function sig is the same, the underlying object in memory is at a different location when parent re-renders recreating it, so Object.is() comparison will fail.
    return (
        <button onClick={myFunc}>Click</button>;
    );
});
```
