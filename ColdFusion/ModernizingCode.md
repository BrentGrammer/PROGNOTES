# Modernizing Legacy Code

- Tips including some from [Dan Card's talk on refactoring legacy applications](https://cfcasts.com/series/ortus-webinars-2022/videos/getting-started-with-the-legacy-migration-with-dan-card)
- [Sandi Metz Refactoring talk at Railconf 2014](https://www.youtube.com/watch?v=8bZh5LMaSmE)

## Extracting/Separation of Concerns

### Extract Queries

- Extract SQL queries into a function
- Can have related query functions in a separate file
- [\*Pass in scopes instead of using directly](https://cfcasts.com/series/ortus-webinars-2022/videos/getting-started-with-the-legacy-migration-with-dan-card) - see timestamp 38:40.
  - `<cfset bookData = coreFunctions.searchByTitle(form.searchTerm) />`
  - Placing this in the cfm file where you output it, you can then mock the query in your tests

### Extract loops (incl. for queries)

- Loops that don't depend on things all over the page can be extracted into functions
- [See demo](https://cfcasts.com/series/ortus-webinars-2022/videos/getting-started-with-the-legacy-migration-with-dan-card) at timestamp 43:00
  - [Component code](https://cfcasts.com/series/ortus-webinars-2022/videos/getting-started-with-the-legacy-migration-with-dan-card) at 46:10

```java
// cfm view
<cfset resultRows = coreFunctions.createRows(bookData) /> // function in separate cfc file

<table>
    ...
    <tbody>
        <cfoutput>
            #resultRows#
        </cfoutput>
    </tbody>
</table>
```

### Web Components

- see [Web Components in Your CFML Application](https://www.youtube.com/watch?v=O4nYyrj5rjw)
- Can use JavaScript classes and vanilla JS to make re-usable components
- Create custom html tags
- Better compatibility and plugin with jQuery and non-SPA applications if not using a library like React, etc.

### Using JavaScript Modules

- Use [importmap](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script/type/importmap) for creating module import capability in vanilla JS

```html
<!-- 
 Check for support if needed:
 if (HTMLScriptElement.supports?.("importmap")) {
  console.log("Browser supports import maps.");
} -->

<script type="importmap">
  {
    "imports": {
      "square": "./shapes/square.js"
    }
  }
</script>
```

[MDNs Js Modules docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)

## Tags to Script

- Avoid using tag syntax if possible and migrate to script syntax
- Even on cfm pages, don't be afraid to favor using the cfscript tags where appropriate
  - Makes it easier to move into a cfc if needed.
- Can use tools like [cfscript.me](https://cfscript.me/) to convert tag syntax pages to cfscript syntax accurately.

## Refactor Long Functions

- Good place to refactor is functions that are many lines long
- Start breaking those apart

## Adding Linters and Formatting

- Cfformat
- Cflint

## Use Application variables where necessary

- Application.cfc stores default app wide variables you can uses when appropriate (only use when necessary)
  - you can set default datasource so you don't have to specify it anywhere else in queries etc. (if your app is using one datasource)

## Tools

### Use Query Builder

- Can use Query Builder tool to write shorter queries in a functional style

### Use Hyper for HTTP Requests

- [Hyper](https://hyper.ortusbooks.com/)

## Add TestBox

### Installation

- Install commandbox if needed
- `box install testbox`
  - creates box.json
- gitignore `testbox` directory generated
- `box testbox generate harness` to generate scaffold for test runner

### Usage

- For legacy apps, good to test that cfc (components) can be initialized and compiled correctly:
  - see [video](https://cfcasts.com/series/cb-zero-to-hero/videos/creating-the-userservicecfc-tdd-style/) at timestamp 6:00

```javascript
function run() {
  describe("My Service", function () {
    it("can be created", function () {
      // ensures no syntax or compilation errors - test cfcs like models, etc.
      expect(myModel).toBeComponent();
    });
  });
}
```

- [Project with tests](https://github.com/ColdBox/coldbox-zero-to-hero/tree/v7.x)
- [Using Testbox with non-Coldbox legacy app](https://github.com/nolanerck/testbox-for-non-coldbox-cfml/tree/master)
  - [See demo of testing legacy code here](https://youtu.be/0bEfrWit_as?t=2689)

## Bundlers

- Parcel
  - See [video](https://frontendmasters.com/courses/web-development-v3/building-a-project-with-parcel/?w=parcel) adding parcel to a vanilla js project
  - see also [this](https://frontendmasters.com/courses/archive/complete-react-v7/parcel/)
- Webpack
- Vite
- [EsBuild](https://esbuild.github.io/) - recommended as alternative to Vite for some apps.

### Multi page app integration

- See [REPO](https://github.com/BrentGrammer/ModernizeJSApp) with examples of how to add vite or parcel to existing multi page vanilla js app.

Vite uses rollup under the hood so you can set an input object with multiple entry point. it's build.rollup...
https://vitejs.dev/config/build-options.html#build-rollupoptions
https://rollupjs.org/configuration-options/#input

those should do the trick, put the rollup config in the build config and you'll get multiple output js files

if vite is just compiling all those js files together into dist files, it's probably already going to be in the order of imports so you can follow the order of the script tags with your imports then replace them all with one dist file per page

## Adding Vitest

### ES Modules

- `import` and `export` syntax is now widely supported natively without the need for adding a bundler.
- use the `.mjs` extension on your files. This helps flag to various tooling (NodeJS, web servers, etc.) that this file uses ECMAScript Modules (ESM) syntax. With this, no module bundlers are needed when serving to a browser, as ESM Imports are now well-supported
  - see [article](https://pyodide-components.readthedocs.io/en/latest/vitest.html)
  - [In depth guide to ESM](https://gils-blog.tayar.org/posts/using-jsm-esm-in-nodejs-a-practical-guide-part-1/)
- You can name your test files simply with `.test.js`
  - These files are only executed in a node.js runtime environment and use it's native import/export module capability

### Using IIFEs to Confine Scope

- Try wrapping the javascript in the files in an IIFE to prevent variable collisions

```javascript
// js/script1.js
(function (globalApp) {
  // All your script1.js code goes here

  // can register globally available things for other scripts to see optionally
  globalApp.something = "available to other scripts";

  var localVariable1 = "value1";
  function myFunction1() {
    // ...
  }
  // No variables or functions are directly in the global scope anymore
})(globalApp);

// js/script2.js
(function (globalApp) {
  // All your script2.js code goes here

  console.log(globalApp.something);
  var localVariable2 = "value2";
  function myFunction2() {
    // ...
  }
})(globalApp);

// ... and so on for all your .js files
```

### Testing Legacy JS

- If your testing environment (Vitest) has access to the Node.js `fs` module (which it typically does), you can read the contents of your script files directly.

```javascript
import { test, expect, beforeEach } from "vitest";
import { JSDOM } from "jsdom";
import * as fs from "fs"; // Import the file system module
import * as path from "path";

let dom;
let window;

beforeEach(() => {
  dom = new JSDOM(`<!DOCTYPE html><html><body></body></html>`);
  window = dom.window;

  // Simulate the global variable from the HTML
  window.someGlobalVarUsedInScripts = "globalvalue";

  // Simulate script1.js
  const script1Path = path.join(__dirname, "js", "script1.js"); // Construct the path
  const script1Content = fs.readFileSync(script1Path, "utf8"); // Read the file
  new window.Function(script1Content)();

  // Simulate script2.js
  const script2Path = path.join(__dirname, "js", "script2.js");
  const script2Content = fs.readFileSync(script2Path, "utf8");
  new window.Function(script2Content)();
});

test("script1Func should return the correct string", () => {
  expect(window.script1Func()).toBe("Script1: script1value");
});

test("script2Func should return the correct string with global var", () => {
  expect(window.script2Func()).toBe("Script2: script2value and globalvalue");
});
```

- **Changes:**

  - Imported the `fs` module.
  - Used `path.join` to construct the correct file paths (important for portability). `__dirname` is the directory of the test file.
  - Used `fs.readFileSync` to read the file contents into a string.

- **Pros:** Avoids hardcoding the script content in the test file. More maintainable.
- **Cons:** Relies on Node.js `fs` module.

* Alternative example more closely simulating how the scripts load in the DOM:

```javascript
import { test, expect, beforeEach } from "vitest";
import { JSDOM } from "jsdom";
import * as fs from "fs";
import * as path from "path";

let dom;
let window;
let document;

beforeEach(async () => {
  // Make beforeEach async
  dom = new JSDOM(`<!DOCTYPE html><html><body></body></html>`, {
    runScripts: "dangerously", // Needed to execute scripts in JSDOM
    url: "http://localhost/", // Important for resolving relative paths
  });
  window = dom.window;
  document = dom.window.document;

  // Simulate the global variable from the HTML
  window.someGlobalVarUsedInScripts = "globalvalue";

  // Function to load and execute a script
  const loadScript = (filePath: string): Promise<void> => {
    return new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = filePath;
      script.onload = () => resolve();
      script.onerror = (err) => reject(err);
      document.body.appendChild(script);
    });
  };

  // Simulate loading script1.js and script2.js
  await loadScript(path.join(__dirname, "js", "script1.js"));
  await loadScript(path.join(__dirname, "js", "script2.js"));
});

test("script1Func should return the correct string", () => {
  expect(window.script1Func()).toBe("Script1: script1value");
});

test("script2Func should return the correct string with global var", () => {
  expect(window.script2Func()).toBe("Script2: script2value and globalvalue");
});
```

- **Changes:**

  - `runScripts: 'dangerously'` is added to the JSDOM constructor. This is _essential_ for JSDOM to execute the code in the `<script>` tags.
  - A `loadScript` function is created to dynamically add `<script>` tags to the JSDOM document. This function returns a Promise to handle the asynchronous nature of script loading.
  - `beforeEach` is made `async` to use `await` and ensure the scripts are loaded before the tests run.
  - Instead of `new window.Function()`, we're using `document.createElement('script')` and setting the `src`.

- **Pros:** More closely simulates how the browser loads and executes scripts, which can be important for testing complex scenarios or libraries.
- **Cons:** More complex code, especially with the asynchronous script loading. `runScripts: 'dangerously'` has security implications if you're not careful (but it's generally safe in a testing environment where you control the code).

### Using ES Modules natively

- The `type="module"` on the `<script></script>` tag tells the browser to treat the JavaScript file as an ES Module
- Using `.mjs` extension (as naming convention) and `<script type="module">` converts your file to an ES Module
  - note: The file extension alone (.mjs) is not enough to make a script be treated as a module by the browser. The browser's behavior is determined by the `<script>` tag's type attribute.
  - If you rename a file to script.mjs but do not use `<script type="module">` in your HTML, the browser will not treat it as an ES Module. It will likely try to execute it as a regular JavaScript script. This will lead to errors if you have import or export statements in your script.mjs file, because those are syntax that the browser only expects to find inside a module.

```
    .mjs + `<script type="module">` = ES Module (Correct)
    .mjs + `<script src="script.mjs">` = (no type="module") = NOT an ES Module (Error if using import/export)
    .js + `<script type="module">` = ES Module (Also correct)
    .js + `<script src="script.js">` = NOT an ES Module (Standard script)
```

### script defer

- why no “document.addEventListener” for DOMContentLoaded? As it turns out, in browsers, you can load with `<script defer>` and get the same effect.

### Example test

```javascript
import { expect, test } from "vitest";
import { myFunc } from "../src/myfunc.mjs";

test("myFunc works", async () => {
  const someDep = await someDep();
  expect(myFunc(someDep)).to.equal("something");
});
```
