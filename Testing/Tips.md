# Testing Tips

### TypeScript

#### Testing null or empty inputs

- TypeScript will complain about passing in empty inputs to functions that expect a type. You can override this by setting the value to unknown and then type casting:

```javascript
it("handles empty input", () => {
    // set to unknown
  const empty: unknown = undefined;
  // type cast arg to expected type
  doIt(empty as Security[]);
});
```
