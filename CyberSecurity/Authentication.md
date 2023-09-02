# Authentication

## TOKENS

### JWT

- https://stackoverflow.com/questions/38018469/how-exactly-does-json-web-token-jwt-reduce-the-man-in-the-loop-attack
- **The key concept of this stratagem is very much that of POSSESSION. "You have it or you don't," and anyone who DOES "have it" is going to be recognized. That's simply how the design was done.**
- Can be snatched in man in the middle attacks
  - at minimum you need SSL/HTTPS to encrypt tokens to reduce risk.
    - even then, they can be snatched: SSL traffic can still be sniffed and tokens can be stolen (though difficult to do so). There are no real solutions to that in JWT. Expiration doesn't help because the attacked can probably steal the fresh token. I've seen posts from auth0 or oauth.io about using AI to determine unusual token usage in APIs. The most promising solution to replay and mitm is a concept called "token binding", and it is already used in the industry where extra security is needed - like banking. It binds the token to the public/private key on the browser. PingIdentity is one provider.
    - Good thread on sniffing ssl: https://security.stackexchange.com/questions/83028/possibility-to-sniff-https-traffic-on-devices-without-installing-a-certificate
- JWT can be used for many things, among those are bearer tokens, i.e. a piece of information that you can present to some service that by virtue of you having it (you being the "bearer") grants you access to something.
  - Bearer Tokens: Bearer tokens can be included in an HTTP request in different ways, one of them (probably the preferred one) being the Authorization header. But you could also put it into a request parameter, a cookie or the request body. That is mostly between you and the server you are trying to access
- JWTs are digitally signed so if any one modifies it the server will know about it
- don't store the JWT access token in a cookie. It's best to store it in session storage since storing it in a cookie make it prone to XSS attacks, and an Httponly cookie is still vulnerable to CSRF attacks
- As long as a server has the same ACCESS_TOKEN_SECRET that was used to generate the JWT token, that server can decrypt the JWT token and get the userId.
- Sometimes additional and unnecessary information is stored in the JWT. The JWT token should primarily contain user information

### Cookies

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

  ### JWT vs. Cookies

- Cookies are appropriate for web browser to server communication. Mobile apps for ex. might have more difficulty dealing with cookies. JWTs are more versatile and flexible.
- With JWT you are not limited by the size of your data, with cookies you only have 4093 bytes per domain - for all cookies, not the one.
- JWTs better for microservices since multiple servers don't need to share a session DB (cookie session management). the user data is encoded in the JWT
- JWT tokens cannot be “invalidated” (without maintaining them in a shared db), in JWT approach the logout length precision is set by the expiration length of the access_token.
- There is no clear advantage to combining cookies and jwts
