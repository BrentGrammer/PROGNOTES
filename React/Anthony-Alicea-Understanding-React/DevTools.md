# React Dev Tools

- Extension for Chrome, Firefox or Edge

## Common actions

- [Finding matching DOM element for a component in devtools](https://dontimitateunderstand.com/courses/understanding-react/lectures/51624850) timestamp 1:40
  - Click on the eye icon in the bottom menu group items
- [Running a profiler](https://dontimitateunderstand.com/courses/understanding-react/lectures/51624850) at timestamp 1:56

### useDebugValue

- Custom hook to work with React DevTools
- When looking at custom hooks in Components in React Devtools you cannot get much information on it out of the box.

```javascript
import { useDebugValue } from "react";

const useCustomHook = (someProp) => {
  //...
  useDebugValue(someProp); // prop as it updates will show in devtools now for the custom hook
};
```
