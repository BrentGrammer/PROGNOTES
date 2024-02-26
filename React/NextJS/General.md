# NextJS Course Part 1

- Github with starter project (finished): https://github.com/mosh-hamedani/next-course

- Forum for questions:https://forum.codewithmosh.com/
- Good youtube series: https://www.youtube.com/watch?v=E1HzFvXgrCs

## NextJS overview

- A Framework built on top of the React.js library
- comes bundled with builtin router, compiler, nodejs runtime to execute JavaScript on a server/non-browser
- With NextJS you can write both backend and frontend code.
  - no need to maintain two separate projects
- SSR: render components on the server and send the content to the client.
  - Faster
  - More SEO friendly
- Static Site Generation - pre-render static pages for fast serving

### Prereqs:

- Node (16+)
- Extensions:
- ES7+ React/Redux/React-Native
- JavaScript and TypeScript Nightly
- Tailwind CSS Intellisense by tailwind css

### Create a NextJS app:

- In a terminal run: `npx create-next-app@{version}`
  - '13.4' is the version for the course.
  - answer the questions prompted - **NextJS usually do NOT use `src` directory, so you usually want to select NO for that question.**
  - Router: there are two routers - the new App Router and legacy Pages Router, use the new router.
  - Select NO to not customize the default import alias.

### Start in Development:

- CD into the project folder created by npx create-next-app and run: `npm run dev`

### Production Build

- `npm run build`
  - Note: symbols next to the output represent which pages are static and which are dynamically rendered
  - circles represent static pages and lambda symbols mean it is a dynamically rendered page.
- `npm start` - starts app in production

## Project Structure

### App Folder

- The `app/` folder is the container for the routing system.
  - note all components in the app folder are server components by default
  - **NOTE**: a component is not publicly accessible via routing unless there is a `page.tsx` file in the folder!
    - This allows you to co-locate components with folders that are related and still keep them under the app folder.
- NextJS Router is based on the folder file structure
- `layout.tsx` file represents common layout for pages.
  - the children in this component are replaced dynamically at runtime based on user's location
- `page.tsx` represents the home page.
- `globals.css` has app wide styles
  - only place truly global styles in here
  - For component specific styles use CSS Modules
    - files must have `.module.css` extension
    - when importing the styles module into a component it is an object you can access the classes on.
    - You cannot use hyphens etc. in classnames with css modules. always use camel case.
    - when generating css, NextJS uses postcss with plugins to generate the css so classnames do not clash.
  - DaisyUI is a handy package for quick styling of components - bundled button classes etc. uses tailwind under the hood and can be used as a plugin in the tailwind config file.

### The Public Folder

- `public/` is where you put static assets like images svgs etc.

### Root folder

- configuration files for eslint, next, postcss, tailwind and typescript
