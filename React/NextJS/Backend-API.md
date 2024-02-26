# APIs with NextJS

- convention is to create a `/api/` folder to handle routes
- in the api folder you'll have subfolders per resource, i.e. `api/users`, and will have a `route.tsx` file for route handlers.
  - for returning content, we use `page.tsx`, for handling routes we use `route.tsx`
- In the route.tsx files you can create CRUD functions for GET POST PUT DELETE
- **IMPORTANT** If you do not include the request argument then NextJS will cache the response - if you always want fresh data from the network, include the request argument even if you don't use it (i.e. in a GET all resource route handler)

```javascript
// example GET handler
export function GET(request: NextRequest, { params }: Props) {
  if (params.id > 10)
    return NextResponse.json({ error: "User not found." }, { status: 404 });

  return NextResponse.json({ id: 1, name: "name" });
}

//...export async function POST(request) {}
```
