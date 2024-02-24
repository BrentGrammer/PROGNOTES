# Cypress

## Installing

- npm i cypress --save-dev

## Running

- npx cypress open

### Running both app and cypress in one command:

- npm i concurrently (as this can used to run multiple commands concurrently).
- update the scripts section of your package.json to include a script like this: "cypress:open": "concurrently \"npm run dev\" \"cypress open\""
- run the one line npm run cypress:open command from a terminal and that should start both your app and cypress at the same time.

- Select E2E testing option (or component testing if using) if not setup (will generate basic config files)
- Select the browser (should detect what you have installed) to use.

### Creating a test

- by default tests go into `/cypress/e2e/my-test.cy.js`
  - note the .cy.js extension

### Running a test:

- On windows you may need to change `npm run dev` script in `package.json` to `"dev": "vite --host"`. This opens the hosting to your network so Cypress can access it reliably.
  - This should resolve not being able to open localhost in cypress with `cy.visit()` for example.
  - alternatively for angular: `ng serve --host 0.0.0.0`

## Common Config

### Setting a Global Base URL:

```javascript
// cypress.config.ts
import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
    baseUrl: "http://localhost:3000", // set your url here and then you can just use routes in the tests: cy.visit('/');
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
```

### Conditional assigning of base url for CI:

- See [video](https://epicreact.dev/modules/build-an-epic-react-app/e2e-testing-solution-01) at timestamp 0:16 for possible config.

### Using Testing Library with Cypress

- i.e. for `findByRole()` queries etc.
- `yarn add --dev @testing-library/cypress` or `npm i --save-dev @testing-library/cypress`

## Tips and Tricks

- If you need to add a name to an element (i.e. if using findByRole with name), you can add the `aria-label` attribute to the element and set a name that you can then use in the test query.
  - `<form aria-label="my form">`
