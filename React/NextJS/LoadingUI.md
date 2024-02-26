# Loading UIs

- Can use `<Suspense>` which comes with React 18 to show a loader while the comopnent is rendering.
- alternative is to use the `loading.tsx` file and return a loading component that will show when all the components are rendering.
- Can use devtools Components (react dev tools) to search for "suspense" in the filter and then click the little timer icon in the top right to set the suspense to true to test loading screens.
- Note: the server sends back the loading content for server components using Suspense, but keeps the connection open to update with the content after it is done loading - this is called streaming.

### Adding Suspense to app wide components

- can wrap children of app wide layout.tsx with it:

```javascript
export default function RootLayout({
  children,
}: {
  children: React.ReactNode,
}) {
  return (
    <html lang="en" data-theme="winter">
      <body className={inter.className}>
        <NavBar />
        <main className="p-5">
          <Suspense fallback={<p>Loading...</p>}>{children}</Suspense>
        </main>
      </body>
    </html>
  );
}
```

### Use loading.tsx

- There is also a loading.tsx file you can add (i.e. in `app/loading.tsx`)
- When you make this file and return a loading component, it will show when any component is loading

```javascript
// in /app/loading.tsx
const Loading = () => {
  return <div>Loading...</div>;
};
```
