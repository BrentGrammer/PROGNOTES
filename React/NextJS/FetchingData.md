# Fetching Data

- on client side components you can use React Query or useEffect etc., but that could cost an extra trip to the backend (you request the JS bundle and then make another network call to get data)
- On server components you don't need useState necessarily and can use apis like fetch in the node runtime.

Ex:

```javascript
// make the component async to use await with fetch..
const UsersPage = async () => {
  // because we are in a server component, we can use fetch here
  const res = await fetch("https://jsonplaceholder.typicode.com/users");
  const users: User[] = await res.json();

  return (
    <>
      <h1>Users</h1>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </>
  );
};
```

### Fetching data in parallel

- It is recommended to fetch data in parallel to prevent waterfall

```javascript
import { Suspense } from "react";

export default async function UserPage({ params: { userId } }: Params) {
  // do not use await keyword, start both requests immediately
  const userData = getUser(userId);
  const userPostsData = getUserPosts(userId);

  // can use promise.all to await parallel requests
  const [user, userPosts] = await Promise.all([userData, userPostsData]);

  return (
    <>
      <h2>{user.name}</h2>
      <UserPosts posts={userPosts} />
    </>
  );
}
```

### Using Suspense

- another pattern is to load data with suspense
- you can show data incrementally while fetching it in parallel
- In this example we immediately show the user data while the posts continue fetching and will show when done.
  - We wrap the posts in a Suspense while they are fetching

```javascript
import { Suspense } from "react";

export default async function UserPage({ params: { userId } }: Params) {
  const userData = getUser(userId);
  const userPostsData = getUserPosts(userId);

  // await the user data to resolve, but don't await the userPostsData and let it continue fetching
  const user = await userData;

  return (
    <>
      <h2>{user.name}</h2>
      <Suspense fallback={<h2>Loading...</h2>}>
        {/* pass the promise to the posts component */}
        <UserPosts promise={userPostsData} />
      </Suspense>
    </>
  );
}

// Posts component
export default async function UserPosts({ promise }) {
  // await the passed in promise to fetch posts
  const posts = await promise;

  const content = posts.map(post => {
    return (
       <article key={post.id}>
          <p>{post.body}</p>
       </article>
    )
  })

  return content;
}
```
