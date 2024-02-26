# NestJS Routing

Routing in NextJS is based on the file system.
Based on convention, not configuration.

#### Note on difference between old/new router

- With the new router not all files placed in a route folder are accessible (old router - all files were accessible via the url). Instead you get a 404 page now.

### Special Files

- `page.tsx` - for making component publically accessible
- `layout.tsx` - defines common layout
- `loading.tsx` - showing loading UI components
- `route.tsx` - creating APIs
- `not-found.tsx` - show custom errors
- `error.tsx` - show general and custom error pages

### Creating a new route:

- Create a folder in the `app/` folder, for example `users/`
- Add a `page.tsx` file in the `app/users/` folder.
  - **You need to name the component in the folder `page.tsx`**
  - This will render a component that shows when the user is at the location: `/users`
  - can use `rafce` shortcut with the ES7+ extension to quickly make a component
- **NOTE**: a component is not publicly accessible via routing unless there is a `page.tsx` file in the folder!

### Nested Routes

- Add a subfolder to a route folder
- create another `page.tsx` in the subfolder and export a component that renders when the user is at that location: `routefolder/subfolder` ex: `users/new`

## Navigation

**Do not use <a> tags for navigating - this reloads a lot of assets**

### Client Side navigation using Link

- the Link component comes with NextJS from the next/link lib

#### Link Prefetches the content to the viewport

- to see this you can build the app in production: `npm run build; npm start;`
- Link will prefetch pages with the <Link> (including for each possible value of href if it parses multiple query params - see [video](https://members.codewithmosh.com/courses/mastering-next-js-13-with-typescript/lectures/49120320) at 2:30 for explanation)

#### As you navigate NextJS stores the payload of the pages in a client side cache

- When you go to a previously visited page, it is retrieved from the cache not the network.
  - Note: If you do a full page reload then the client cache is cleared.

```javascript
import Link from "next/link";

<Link href="/users">My Link</Link>;
```

- Clicking on a Link will only have requests for downloading the content of the page, not all repetitive parts of the app/assets again.

### Dynamic Routing

- use square brackets in a nested folder to create a route parameter
  - `[id]/` under `users/` would make a route parameter for users/:id
  - make the usual `page.tsx` file to export the component in the folder (`users/[id]`)
- The route parameter will be available in the component as a prop under the `params` property:

```javascript
// users/[id]/page.tsx
interface Props {
  params: { id: number };
}

const UserDetailPage = ({ params: { id } }: Props) => {
  return <div>UserDetailPage {id}</div>;
};
```

#### Double Nested Routes (dynamic params)

- If you need deeper nested dynamic routing, add another folder under the dynamic route folder with the same convention, but use a different parameter name
- All of the parameters in the heirarchy for the nested routes will be in the params property

```javascript
// users/[id]/photos/[photoId]/page.tsx
// this component renders for the route: /users/:id/photos/:id
interface Props {
  params: { id: number, photoId: number };
}
// note that we have both id and photoId (even though id is the dynamic param in the parent folder)
const PhotoPage = ({ params: { id, photoId } }: Props) => {
  return (
    <div>
      Photo Page
      {id} {photoId}
    </div>
  );
};
```

### Catch all routing

- add three dots before the param name to have catch a dynamic number of parameters
- `[products/[...slug]]`
- for a route `/products/grocery/dairy/eggs` you can extract from `params.slug`: ['grocery','dairy','eggs']
- **NOTE** using `[...params]` requires at least one parameter present in the url or you get a 404.
- to make the params optional use double brackets: `[[...param]]`

  - with this change you can navigate to `/products` without a param and not get the 404

  ```javascript
  interface Props {
    params: { slug: string[] }; //dynamic params with the [...slug] catch all route
  }

  const ProductPage = ({ params: { slug } }: Props) => {
    return <div>ProductPage {slug}</div>;
  };
  ```

### Query String Parameters

- use the builtin `searchParams` property in the component to access query params
- **You cannot access query params in components, only pages (page.tsx)**
  - When you need to access them in components they need to be passed down as props from the parent page.tsx component.

```javascript
interface Props {
  params: { slug: string[] }; //dynamic params with the [...slug] catch all route
  searchParams: { sortOrder: string }; // ?sortOrder= query param value
}
const ProductPage = ({
  params: { slug },
  searchParams: { sortOrder },
}: Props) => {
  return (
    <div>
      ProductPage {slug} {sortOrder}
    </div>
  );
};
```

#### Use query string params for sorting and filtering

- Since we have server rendered components no need for state and event handling - just use query params (`?sortOrder=name`)
- If sorting in a component (not a page.tsx) then you need to pass the query params to it

```javascript
// In the parent page.tsx component using the table access the query string params and pass down
const UsersPage = async ({ searchParams: { sortOrder } }: Props) => {
  return (
    <>
      <h1>Users</h1>
      <UserTable sortOrder={sortOrder} />
    </>
  );
};

// using link in `users/UsersTable.tsx` component, use links to set the query string params (extracted by parent page.tsx and passed down)
const UserTable = async ({ sortOrder }: Props) => {
  //...fetch users
  const sortedUsers = sort(users).asc(
    sortOrder === "email" ? (user) => user.email : (user) => user.name
  );

  return (
    <table>
      <th>
        <Link href="/users?sortOrder=name">Name</Link>
      </th>
      <th>
        <Link href="/users?sortOrder=email">Email</Link>
      </th>

      <tbody>
        {sortedUsers.map((user) => (
          <tr key={user.id}>
            <td>{user.name}</td>
            <td>{user.email}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};
```

### Programmatic Navigation

- use the `useRouter()` hook from `next/navigation` - DO NOT use the `next/router` import as that is the old router and will not work.
  - `router.push('/my-route')`
- You need to use 'use client' directive if handling in an event handler (server components cannot handle browser events)

```javascript
"use client";
import { useRouter } from "next/navigation";
import React from "react";

const NestedNewRoute = () => {
  const router = useRouter();
  return (
    <button className="btn btn-primary" onClick={() => router.push("/users")}>
      Create
    </button>
  );
};
```
