# Lazy Loading

- Postpone loading of a component (I.e. until a user clicks on it etc.)
- Do NOT lazy load small components - this will result in overhead that does not optimize anything. Only use for large heavy components.
- By default components that are statically imported are included with the bundle build by NextJS
  ```javascript
  // since component is statically imported, NextJS adds this to the bundle for the page
  import HeavyComponent from "../components/HeavyComponent";
  ```
- We can defer loading components by using the dynamic function from next/dynamic

```javascript
"use client";

import dynamic from "next/dynamic";
// use the dynamic import to lazy load the component
const HeavyComponent = dynamic(() => import("../components/HeavyComponent"));

const HeavyPage = () => {
  const [isVisible, setIsVisible] = useState(false);

  // onClick to show the heavy component (will not load into bundle before the button is clicked with dynamic import)
  return (
    <main>
      <h1>Heavy Page</h1>
      <button onClick={() => setIsVisible(true)}>Show</button>
      {isVisible && <HeavyComponent />}
    </main>
  );
};
```

### Dynamic import options

- You can add options like a loading screen while the component is being fetched

```javascript
const HeavyComponent = dynamic(() => import("../components/HeavyComponent"), {
  loading: () => <p>Loading...</p>,
});
```

- you can use the `ssr` option to prevent NextJS from pre-rendering the component on the server (it does this for imported client components by default).

  - Use this when you use browser APIs or features that will throw an error on the server:

  ```javascript
  const HeavyComponent = dynamic(() => import("../components/HeavyComponent"), {
    loading: () => <p>Loading...</p>,
    ssr: false, // will not pre-render the imported client component
  });
  ```

  ### Lazy loading external libraries

```javascript
"use client";

const HeavyPage = () => {
  const [isVisible, setIsVisible] = useState(false);

  const sortUsers = async () => {
    // use the await import() and access default prop from the module to lazy load the lodash library.
    // The library will not load until the user clicks
    const _ = (await import("lodash")).default; // wrap the import in parens to get access to the module default prop
    const sorted = _.orderBy(users, ["name"]);
  };
  return (
    <main>
      <h1>Heavy Page</h1>
      <button onClick={sortUsers}>Show</button>
    </main>
  );
};
```

### Debugging

- To check if your components are lazy loaded you can open up dev tools and go to Network.
- Click the JS fetch for the page.tsx and do a filter/string search for text in the component. If it is there, then the component was loaded in the bundle, but if not then it hasn't loaded yet.
  - Ex: for HeavyComponent above, search the page.tsx response in devtools for the text "My Heavy Component"
