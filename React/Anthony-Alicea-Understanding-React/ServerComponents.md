# React Server Components

- Components run on the server
- The output is HTML and a Payload
  - The browser uses the HTML received to build the DOM

## Benefits

- Initial page load is faster since HTML is delivered and browsers are good at parsing and processing that faster than a JavaScript bundle (in a non server side React app)
- Data needed for the page can be fetched while HTML is generated on the server
- More work done on the server instead of the user's device
- Using async await and waiting for things while generating component on server is less complicated.

## Limitations of Server Components

- Cannot use hooks
  - There is no fiber tree for the individual user on the server
  - Example: cannot use `useState` on a server component
- Cannot store state (must be user specific on their machine)
- No stateful interaction

## When to use Server Components

- Where you don't need state interaction
  - example: static lists

## When to use client components

- When you need state individual to the user
- Recommendation from Next: Push client comopnents to the bottom of the tree
  - They are ancestors of each other
  - Makes it clear where to bundle JS and not maximizing benefit.
- Next.js will still generate what HTML it can from client components to serve initially such as the initial state.

## RSC Payload (aka "flight data")

- Server Components are served with a response containing two things:
  - The HTML that was rendered for the component (for the DOM tree)
  - A payload that allows the React Fiber Tree to be built.
- Used to enable reconciliation of the fiber tree when using server components
  - There needs to be a way to build the fiber tree for the portion of the DOM generated on the server. (no fiber tree was built for the part of the DOM for server components)
  - The server needs to send information to React on the client that it needs to build those parts of the fiber tree: The RSC payload or "flight data".
- Server components send the HTML to generate the DOM in the client, but the client also needs to make the React fiber tree that corresponds to that part of the DOM.
- The payload is what the nodes in the server component would look like (for use in React Fiber Tree etc) if the component was generated on the client. see [video](https://dontimitateunderstand.com/courses/understanding-react/lectures/52353974) at timestamp 6:37

### Sending the payload in the response:

- Next, for example, will build arrays and scripts and send that with the HTML generated from the server component to the client browser (in the same response with the HTML)
  - see [video](https://dontimitateunderstand.com/courses/understanding-react/lectures/52353970) at timestamp 3:20
  - This information is used to build the fiber tree on the client
- Because the HTML is sent and parsed immediately by the browser, the user will see content faster.
  - After the HTML is parsed to the DOM, JavaScript scripts will run Javascript to build up the matching React fiber tree.
  - Note that the content is duplicated from what is in the HTML since it is the information in a format React can use to build the Fiber Tree so it has it to compare to the DOM tree to continue to do work.

### Payload sizes will be larger with Server Components

- If you have a lot of data on the page, svgs, data etc., then when you send it as a server component, because of the RSC payload in addition to the HTML content, the response will be larger in size than otherwise - this is something to keep in mind.

### Hydration

- Running the downloaded RSC payload that came with the response from a server component to build the React Fiber Tree.
- Could be thought of as two ideas:
  - Tree Synchronization: creating the Fiber Tree to match the DOM
  - Hydration: We have synthetic events working now, because we have a fiber tree to know what should happen in the DOM whenever there is something is done that changes the DOM.
- Both Client and Server components create the Fiber Tree TOGETHER.

## Using Client and Server Components Together

- It is fine to import a client component into a server component
  - The import will bundle the javascript for the client component and send it to the client in the response to be run there on their browser.
- You CANNOT import a server component into a client component!
  - The code for a server component is HTML and the payload - you cannot say in the client to get some JavaScript code to import because it was never sent from the server (only the HTML and payload for building a fiber tree was).

### Using Children to use a Server Component inside a Client Component

- You can use server components in client components if you pass them as children using the children prop in a client component
- This works because the payload sent by a server component is information organized as the fiber tree is with a children array.
  - Attaches the payload array of elements from the server component as children to the fiber node of the client component in the fiber tree since passed as props.
  - The client component will have its representation in the Fiber Tree constructed and the payload array from the server component payload can be plugged into the fiber tree children node for the client component directly.
- Once the fiber tree is updated with the client component node data and the payload information sent from the server component, stateful updates in the client component will work and affect the server component as well (the DOM will be updated based on changes to the merged Fiber Tree)
  - For example if you have a click handler in the client component that transforms the text to uppercase for all text children of the client component, that will update in the server component since that part of the fiber tree has been built and will be used.
- Note that if you want any interactivity inside the server component itself, or state, then you have to make it a client component.

```javascript
"use client";

const ClientComponent = ({ children }) => {
  return <section>{children}</section>;
};

// server component:
const ServerComponent = () => {
  return (
    <ul>
      {data.map((d) => (
        <li key={d.id}>{d}</li>
      ))}
    </ul>
  );
};

// higher level component to compose the two:
import ServerComponent from "./components/ServerComponent";
// this will allow server component to be used in a client component
const App = () => {
  return (
    <ClientComponent>
      <ServerComponent />
    </ClientComponent>
  );
};
```
