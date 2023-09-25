# Cookies

- Automatically sent with each request from browser to solve the problem of stateless HTTP (remembering who the user is on subsequent requests etc.)
  - Cookies are stored and associated with a domain/server
  - If the server sends a response with the `set-cookie` header (the value is the cookie and any options), then the web browser automatically sends that cookie with every request to the cookie's domain in a `Cookie` header
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

if Using express you can use `cookieParser` middleware package on the server.
Ex:

```javascript
//...other middleware in express server
app.use(cookieParser());

// Set the cookie on responses in auth endpoints:
res.cookie("token", signedJWTToken, {
  httpOnly: true,
});
res.send(...);

// now when parsing token from incoming requests in other routes:

// attach user info to request object from the token in request guard/middleware so it is accessible to other routes further down server pipeline
const token = request.cookies.token; // should be on requests send after setting it on response earlier
//...other code to decode token
req.user = decodedToken;

// can also use the token in express-jwt middleware: see https://courses.reactsecurity.io/view/courses/react-security-fundamentals/328811-switching-to-cookies/937491-verify-jwt-from-cookie
```

- Browser API is unintuitive, so recommended library is [js-cookie](https://www.npmjs.com/package/js-cookie) if working with cookies in the browser.
- For server cookies, use the library [cookie](https://www.npmjs.com/package/js-cookie)
- Set the cookie on the server usually - this is more secure. Send it as part of the response.

```javascript
// note - see ex further up using cookieparser middleware if using express
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
- Cookies need to set to `httpOnly` so that they cannot be accessed with JS
  - NOTE: certain XSS and Cross Site Request Forgery attacks can still get to the cookies
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

### Cross-Site Request Forgery Attacks

- Cookies are vulnerable to CSRF attacks:
  - Example: someone sends a email to a user of an application that has a clickable link which sends a request to the application domain with some query parameters set (i.e. `domain.com/transfer?amount=200`). When the email reader clicks the link, since cookies are automatically sent with requests to the app domain, this would trigger a request with the token stored in the browser cookie for that domain to be sent with it and execute the request without the user's intent
- You can use a CSRF token to protect against this. This is a token that is generated server side and retrieved from the application on startup so that requests will be blocked if not coming from the app with this token.
- example you can use a package like `csurf` on your backend API to protect against this.
  - **NOTE: csurf package is deprecated - you need to find an updated package or approach**

```javascript
const csrf = require("csurf");

// csurf is a middleware. get an instance and pass in an option to force the double submit cookie pattern for ccsrf protection
const csrfProtection = csrf({
  cookie: true,
});

// near your auth routes or after the jwt middleware make use of csrf protection
// this middleware will check future incoming requests on protected routes for the csrf token header and validate it against the one created below (generated when app starts and makes the get request)
app.use(csrfProtection);

// you'll need a new route to accept get requests to make use of this. You can fetch this from the client for example when the application starts up.
app.get("/api/csrf-token", (req, res) => {
  // the csurf middleware setup attacks a csrfToken method on the request object
  res.json({ csrfToken: req.csrfToken() });
});
```

Now in the React client for example, you need to get the csrf token when the app starts (for ex. in a Auth or Fetch context provider that wraps the app) and send it with requests that mutate or update data in the backend.

```javascript
const FetchProvider = ({ children }) => {
  const authAxios = axios.create({
    baseURL: process.env.APP_API_URL,
  });

  // use effect runs on mount - this provider runs at app startup and wraps the application/protected parts of the application.
  useEffect(() => {
    const getCsrfToken = async () => {
      const { data } = await authAxios.get("/csrf-token");
      // now set the default header on future axios requests to post/auth protected routes:
      authAxios.defaults.headers["X-CSRF-Token"] = data.csrfToken; // middleware on server expects this header. without it requests will fail.
    };

    getCsrfToken();
  }, []);

  return <Provider value={{ authAxios }}>{children}</Provider>;
};
```

### Logging Out a User/Ending a Session

- you should almost never perform mutations within a GET request, so rather than having a link to a /logout page which is too common, you should have a button that performs a POST request to /logout. This reduces the risk of CSRF attacks.
- **Expiration**: When a cookie expires, the browser will automatically delete it. So it won't show up in future requests.
  - Can set expiration time to far in the future for a "remember me" functionality". Note: Remember me may not log user in when they come back if they come back after the expiration has passed. All "remember me" is supposed to do is prevent the cookie from being automatically deleted when the browser is closed. Each app will have its own rules about how long a user can remain logged in after that point.
  - You can use `expires` (takes a date) or `max-age` (number of seconds the cookie is valid for) settings on a cookie to set it's expiration - it doesn't matter which one.
- Log out the user and expire the session automatically if the user account was deleted. Send them to the login page.

#### Automatic Logout (i.e. for bank apps after amount of inactivity):

- With client-side JavaScript, you simply create a timer and so long as the user is actively using the site, you reset the timer. If the timer expires, you log the user out. You can even provide them with a modal to notify them of the impending logout and give them the option to stay logged in.
- There are various ways you can determine activity. Depending on the type of app you have, you could track navigation, network requests, mouse movements, or keyboard activity.
  Ex tracking navigation:

```javascript
const location = useLocation();

useEffect(() => {
  console.log("location changed:", location.key);
}, [location.key]);
```

- When the user is prompted with a modal to remain signed in, reset the timer.

#### Automatic Redirect after Login

- Can use a `redirectTo=` query string param to tell the app where to direct the user (if for example coming from an email link that should lead the user to a particular page to do something).
- Security Warning: redirectTo query params can be abused by attackers. A baddy could use a redirectTo query param to redirect a user to a malicious site after logging in. So you should always validate the redirectTo query param to make sure it's a valid URL on your site. It's sufficient to just make sure the URL doesn't start with http or https and that it starts with /.
