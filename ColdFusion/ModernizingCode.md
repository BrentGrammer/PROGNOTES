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

## Add Tests

- Use TestBox
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

## Bundlers

- Parcel
  - See [video](https://frontendmasters.com/courses/web-development-v3/building-a-project-with-parcel/?w=parcel) adding parcel to a vanilla js project
  - see also [this](https://frontendmasters.com/courses/archive/complete-react-v7/parcel/)
- Webpack
- Vite
- [EsBuild](https://esbuild.github.io/) - recommended as alternative to Vite for some apps.
