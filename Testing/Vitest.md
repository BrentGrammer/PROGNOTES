# Vitest

- Testing tool similar to Jest

## Setup

- To get globals like 'it', 'expect', 'describe' etc. go into your `vitest.config.js` (or .ts) and enable them:

```javascript
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
  },
});
```

## Usage

- looks for `.test.js/ts` by default
- Can place test files next to the file being tested if desired
