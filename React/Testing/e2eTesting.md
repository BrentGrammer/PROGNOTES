# End to End Testing

- The E2E tests aren't going to give you 100% use case coverage (and you should
  not even try), nor will they give you 100% code coverage (and you should not
  even record that for E2E tests anyway)

- Even one E2E test can give you a lot of confidence. There is also an approach
  you can use to test in production using feature flags
  ([see Kent C Dodds intro](https://epicreact.dev/modules/build-an-epic-react-app/e2e-testing-intro))

- You can use Cypress with a Testing Library implementation:
  - [Installation and setup](https://testing-library.com/docs/cypress-testing-library/intro/)
  - configuration in [cypress/support/e2e.js](/cypress/support/e2e.js)
  - the script that should be run in CI is `npm run test:e2e`:
    - `start-server-and-test start:cli http://localhost:3000/list cy:open`
