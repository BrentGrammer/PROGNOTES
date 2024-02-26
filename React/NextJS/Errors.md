# Error Handling

## Not Found pages

- You can add a `not-found.tsx` page at the `/app` level which will show automatically when an unknown route occurs
- You can use `notFound()` NextJS method from the `next/navigation` package to show not found page in components
  - By default this uses the not-found.tsx page defined in `/app/` folder, but if you want a custom not found page, just make a new `not-found.tsx` file in folder of the route you want to use `notFound()` in.

```javascript
import { notFound } from "next/navigation";

const UserDetailPage = ({ params: { id } }: Props) => {
  if (id > 10) notFound(); // will use app/not-found.tsx or not-found.tsx in same folder if present.

  return <div>content</div>;
};
```

## Unexpected Errors

- By default when the app is in production mode a generic error page will show if there is an uncaught or unexpected error in the app
- You can customize this error page by adding a `error.tsx` in the `/app/` folder
- You can have error.tsx pages at different levels of the app
  - Just place it under the folder/route that you want it to apply to.
  - Generally you only need one error page for the whole app to handle any unexpected errors.
- Errors are not caught for the main layout.tsx in the app folder. You need to create a separate error file to handle those if you have logic in the layout file etc.
  - in the `/app/` folder create a file called `global-error.tsx`
- NextJS also passes a reset function for retries after the error (user can click a button to retry)
  - use this with caution (will build up error logs as users retry - only use it in certain parts of the app where needed)
- If you are using a click event (for retries etc), then you need to use the 'use client' directive in the error.tsx page
- The Error object is passed to the error.tsx component by NextJS
- You generally will want to log the Error passed to the error page by NextJS using a logging service, for Example, Sentry is recommended, to log it somewhere permanent for debugging (otherwise it is only logged in the console).

```javascript
// app/error.tsx
"use client";
import React from "react";

interface Props {
  error: Error; // NextJS automatically passes Error obj to this component
  reset: () => void; // NextJS passes this automatically - used for retries
}

const ErrorPage = ({ error, reset }: Props) => {
  console.log("Error", error); // log to Sentry or logging service for persistence
  return (
    <>
      <button className="btn" onClick={() => reset()}>
        Retry
      </button>
      <div>An unexpected Error has occurred.</div>
    </>
  );
};
```
