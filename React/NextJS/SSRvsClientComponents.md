# SSR vs. Client Side Rendering

- Client Rendering
  - Large bundles
  - more resource intensive
  - No builtin SEO (bots cannot execute javascript code to render contents)
  - less secure with API keys etc. in components exposed to the client.
- SSR
  - Smaller bundles - only send essential components to client
  - Server handles the rendering, less resources needed on client (better for mobile browser, for example that would take longer to load JavaScript or clients with less resources)
  - better SEO - bots can parse the content since it is sent from the server instead of just JS.
  - API keys etc. can be kept on the server.

### Server components vs. Client components

- **In NestJS apps we use a mix of client and server components**
- default to Server Components and use client components only when absolutely needed.
- Note: all components in the `app/` folder are server components by default.

- **Disadvantage** of Server components is they lose interactivity
  - they cannot listen to browser events like clickm change, submit etc.
  - cannot access browser APIs, ex.: local storage
  - cannot maintain state or use useEffects hooks etc.

#### Keep most standard components of the app on the server:

- NavBars
- SideBars
- Pagination
- Footer
- ProductList
- ProductCart

**EXTRACT the parts of the components that need interactivity and make only those client side components**
Ex: Extract the button to update the cart from the ProductCart component and only send that to the client, render the rest of the component on the server.

```javascript
<ProductCart /> // Server component
<AddToCart />  // Update cart button and functionality is client component
```

### Making a Client Component
- use the 'use client' directive at the top of the file
```javascript
'use client'
import React from 'react';

//...my component
```
- This tells the JS compiler to include this component in the JavaScript bundle
- **If this component is dependent on other components, then those will also be included as client components in the bundle automatically!**
  - i.e. you don't need to repeat the directive on every client component
