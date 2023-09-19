# Cookies

- Automatically sent with each request from browser to solve the problem of stateless HTTP (remembering who the user is on subsequent requests etc.)
  - Cookies are stored and associated with a domain/server
  - web browser automatically sends cookies with every request to the cookie's domain.
  - the browser will automatically add HttpOnly cookies to the request before sending
- CSRF Attacks: malicious page uses auto sending browser behavior to make requests to your server with user's token

  - Modern browsers default a `same-site` attribute that defaults to LAX which means anything other than Top Level navigations (URL in the browser changes) do not auto send the cookie with a request. This mitigates CSRF Attacks.

  ```
  Set-Cookie: CookieName=CookieValue; SameSite=Lax;    // Only GET requests that happen due to top level navigation (URL change) are sent with cookies
  Set-Cookie: CookieName=CookieValue; SameSite=Strict; // no cookies at all are sent with any requests
  // Normal sends all cookies for all requests, but is not recommended
  ```

- GDPR Banner requirements: in general if you avoid the use of cookies for tracking and advertising purposes, you should be fine without a consent banner.

#### Do not store cookies in Local Storage

- localStorage can be read by any script and is insecure
- you have to wait for client side code to load before accessing local storage since it does not send cookies on every request.

### Setting a Cookie

- Browser API is unintuitive, so recommended library is [js-cookie](https://www.npmjs.com/package/js-cookie) if working with cookies in the browser.
- For server cookies, use the library [cookie](https://www.npmjs.com/package/js-cookie)
- Set the cookie on the server usually - this is more secure. Send it as part of the response.

```javascript
const res = new Response(body, {
  headers: {
    "set-cookie": "name=John",
  },
});
// The browser will parse this header and store it to send with all future requests to the server.
```

- the `path` property tells the browser which requests the cookie will be sent with. For ex, if `/admin` is set as the path, then cookies will only be sent on requests to /admin/\* and any subpaths under admin, but not other routes.

```javascript
import * as cookie from "cookie";
//...in response handler set the cookie, this ex sets a light or dark theme cookie:
function setTheme(theme) {
  return cookie.serialize(cookieName, theme, { path: "/" });
}
```

## Session Storage, Securing Cookies

- Make sure that client side JS cannot access or steal the cookie value and the cookie cannot be modified by the user.
- Cookies have a name, value and a set of optional attributes. Attributes can be used to configure the cookie's behavior.
  - Common Attrs:
    - `path`: route the cookie is sent with, defaults to / which means cookie sent for all requests on the domain.
    - `domain`: defaults to current domain. domain cookie is valid for.
    - `expires`: defaults when browser is closed. set data and time otherwise.
    - `max-age`: number of seconds until cookie expires, if not set expires when browser closed.
    - `secure`: if set, cookie is sent to server only over HTTPS. can set if in production (safari has problems in localhost for dev): `secure: process.env.NODE_ENV === 'production'`
    - `httpOnly`: if set to `true`, cookie is not accessible via JS, protects against XSS attacks.
    - `sameSite`: if set, cookie only sent to server if the request is from the same site origin. Prevents cross site forgery attacks. `lax` means cookie is only sent with safe methods like 'GET' methods, otherwise only sent with same site origin requests for POST etc.
- To prevent tampering use the `cookie` npm package to sign the cookie with a cryptographic hash function.
  - cookie package provides a sign and verify function for the cookie to confirm the user did not tamper with it.

### Cookie tips

- Do not store too much data in the cookie itself - this can slow down processing when it's sent to the server and cause problems if cookie is large.
- Most of the time only a ID is stored in the session cookie which can be used to look up the rest of the data in a db server side.
- Temp data sometimes is stored using a pattern called [Cookie Flash](https://remix.run/docs/en/main/utils/sessions#sessionflashkey-value).
