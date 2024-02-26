# Layouts

### Custom Layouts

- If you need layouts to cover parts of your app (separate from the main layout.tsx provided by NextJS)

- Create a new folder under the `app/` folder called `admin` and inside that a `layout.tsx` file (the name must match and is case sensitive)
- All pages in the folder that are siblings to the layout.tsx file will be children of it and be wrapped in that layout.
  - `/app/admin/page.tsx` becomes injected as a child into `app/admin/layout.tsx` and is rendered for all components under the /admin route.

```javascript
// /app/admin/layout.tsx
interface Props {
  children: React.ReactNode;
}
const AdminLayout = ({ children }: Props) => {
  return (
    <div className="flex">
      <aside className="bg-slate-200 p-5 mr-5">Admin Sidebar</aside>
      <div>{children}</div>
    </div>
  );
};
```

### Global Styles Overwriting
- In the global css file you have directives that you can overwrite (@base etc)
- To overwrite parts of the base layer (for example to update the styling of all h1s in the app), you can use another directive:
```css
/* overwrites the base layer to style all h1 elements in the app */
@layer base {
  h1 {
    @apply font-bold text-2xl mb-3;
  }
}
```
