# Handling async requests and http calls in React

## Uri encoding

- Can validate or clean user input put into URL by using encodeURIComponent
- helps if there are spaces etc. so they are encoded properly for sending in a url
- careful about user input in url - security risk

```javascript
fetch(`http://myendpoint?input=${encodeURIComponent(userinput)}`)
```
