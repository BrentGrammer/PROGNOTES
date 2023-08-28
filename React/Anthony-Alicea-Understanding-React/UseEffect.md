# USE EFFECT

https://dontimitateunderstand.com/courses/understanding-react/lectures/48265470

- Side Effect: Something that works on variables or things outside of the function scope.
- The purpose is to deal with things that React does not have control over (keeping react state in sync with "the outside world")

### Mental Model:
- Components are not objects and useEffect is not something you want the object to do
- Components are functions being run over and over again (called on each render - the two renders are Current and Work In Progress)

***Purpose of useEffect: to keep things outside the context of React in sync.

- useEffect runs AFTER all react code has been committed and completed. 
  - It runs after rendering or re-renders and after all work has been completed.
*This is how it is safe to have side effects - because the side effect occurs after the entire function (i.e. component)  and react work has run.

- Effects are POJOs (just objects) that are added to a queue directly on the fiber node. (The hooks linked list queue has references to these effect objects in it's queue).

### useEffect with no dependencies:
```javascript
useEffect(() => {
  console.log('use effect ran.');
});
// Will run after the component has rendered or re-rendered
```

## DEPENDENCIES
https://dontimitateunderstand.com/courses/understanding-react/lectures/48265472

- If passing no array, it means run the useEffect everytime.
- If passing an empty array, no dependencies, so only run useEffect once.

NOTE: React compares the values of previous dependency (current) and future dependency (Work in Progress) to determine whether to run the effect. If they are the same the effect is not run.

### Gotchas - careful with objects:

```javascript

const [numOfClicks, setNumOfClicks] = useState({ total: 0 })

useEffect(() => {
    console.log('ran')
}, [numOfClicks]) // see below - really should use numOfClicks.total to get to primitive value

handleClick = () => {
    setNumOfClicks({...numOfClicks, total: numOfClicks.total + 0})
    // Even though the increment is 0, it is still a new object so the effect WILL run! since objs compared by reference.
}
```

**Get down to the primitive values in dependencies so they are compared more easily and it doesn't matter where they are in memory as with objects**
Ex:
```javascript
useEffect(() => {
    console.log('ran')
}, [numOfClicks.total]) // not just the state object numOfClicks for ex.
```

## Cleanup 
- You can return a function to run when the component:
  1. Unmounts
  2. Re-rerenders

ex:
```javascript
useEffect(() => {
   return () => console.log('unmounting or re-rendering')
})
```

During a re-render the Work In Progress will be set up with a new instance of the destroy/useEffect function

## FETCHING DATA

- React recommends using meta frameworks or other libraries to handle fetching data instead of writing manual Effects.
- Reasons to avoid data fetching in Effects:
   - Race Conditions caused by re-renders
   - Network Waterfalls where fetching triggers more fetching because different components are doing fetching, causes multiple requests for data which is slow
   - caching is not built in, so when component re-renders even if data didn't change, you'll re-fetch in the useEffect
- should use frameworks like React Query

### Preventing Race Conditions in Fetch calls
- 6:00 marker in https://dontimitateunderstand.com/courses/understanding-react/lectures/48491137

- React has a specific order that it does things:
  - If a component is executed multiple times, then previous effect's cleanup functions are run before the effects for subsequent component renders are run.
  - When a new render occurs, the destroy cleanup function for the previous Effect is run first.

Example:

*This prevents 'Bob' result from showing if you select a different person from the dropdown before the Bob promise finishes.

```javascript

async function fetchBio(person) {
    const delay = person === 'Bob' ? 2000 : 200;
    return new Promise(resolve => {
        setTimeout(() => {
            resolve('This is ' + person + 'bio')
        }, delay)
    })
}

function App() {
    const [person, setPerson] = useState('Alice')
    const [bio, setBio] = useState(null)

    useEffect(() => {
        let ignore = false;
        setBio(null)
        fetchBio(person).then(result => {
        // ignore is closed over from cleanup function/useEffect scope, so when promise resolves, 
        // it will be set to true by the cleanup if new person select causes re-render
            if (!ignore) { 
                setBio(result)
            }
        })

	return () => {
	    ignore = true 
            // even though promise is still awaiting (for Bob), 
            // this cleanup function is run if a new person is selected.
	}
    }, [person])

    
    /// ... dropdown to select 3 names: 'Alice' 'Taylor' or 'Bob'

}

```

Pattern: depend on updated prop and set a flag that is set in the cleanup useEffect function to prevent result from previous call from being set to state.

## DON'Ts with UseEffect
- Don't calculate or set state based on other state in useEffect (causes unnecessary re-render)
- Do not use effects for events, like a click event. Handle it in a click handler, not useEffect