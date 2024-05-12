# Auth

- [OWASP Cheat Sheet Guide to Security](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

## TOKENS

### JWT

Can decode at https://jwt.io
format of a JWT: `{header}.{payload}.{signature}`

- The key value of JWTs is that they come with a security feature to ensure that they have not been tampered with in between exchanges (client/server). Can confirm that the information receieved is information that was sent when the tokens are validated.
  - If the JWT contents are modified, then the signature will be different than the originally hashed: `{header}.{payload}.{signature}`
- [SO Thread on Security and JWTs](https://stackoverflow.com/questions/38018469/how-exactly-does-json-web-token-jwt-reduce-the-man-in-the-loop-attack)
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
- **Main drawback is invalidation is difficult** - You cannot invalidate them manually before expiration time if needed. There are workarounds, but you wind up losing the advantages of cookie session based auth (and need a database and reintroduce state).

#### Example creating JWT:

Use the npm package `jsonwebtoken` to sign tokens on the backend.

```javascript
import * as jwt from 'jsonwebtoken';

const secret = 'some-long-ungeussable-string';

const payload = {
  sub: '123' // subject
  iss: 'example.com', // issuer, usually use your domain
  aud: 'api.example.com', // audience - who the token is intended for, i.e. your api
};

const token = jwt.sign(payload, secret, {
  expiresIn: '1h' // set this to something short
});
```

### JWT Best Practices

- Do not store JWTs in Local Storage - either keep them in a httpOnly cookie or in your React state/Browser Memory
  - Local storage is easily accessible by malicious JS code (localStorage.getItem('token'))
  - If you're site has no XSS vulnerabilities then local storage is okay, but to be safe it should be avoided.
  - For refreshing the page and maintaining signed in state, store the token in an httpOnly cookie, not local storage
  - Note: you can store things like `expiresIn` and some user info if it is not particulary sensitive in local storage. The important thing is not to store the token there, but in a httpOnly cookie instead.
- Do not keep any secret keys that are used to sign tokens in the browser. You should only have access to them on the backend server. If stored in browser someone could parse them to sign tokens.
- Do not decode the token in the client (to extract user info etc.). This is especially important if you are using OAuth.
  - Access tokens are meant to be opaque tokens only read at the API
  - Instead, you can have a user info endpoint that returns user info from the token or get the user info when they sign in/out.
  - If you want to check the expires at time on a token, don't decode it, just keep a expiresAt key
- Make your secrets used to decode/sign the token long and strong, ideally something generated by a computer and can't be guessed
- Keep the token payload small since they need to be sent over the network regularly - increases request time
- Only send tokens over HTTPS to prevent man in the middle attacks and snags

### JWT vs. Cookies

- Cookies with sessions require a session db to manage and keep track of sessions, JWTs do not require session db management.
- Cookies are appropriate for web browser to server communication. Mobile apps for ex. might have more difficulty dealing with cookies. JWTs are more versatile and flexible and more mobile friendly.
- With JWT you are not limited by the size of your data, with cookies you only have 4093 bytes per domain - for all cookies, not the one.
- JWTs better for microservices since multiple servers don't need to share a session DB (cookie session management). the user data is encoded in the JWT
- JWT tokens cannot be “invalidated” (without maintaining them in a shared db), in JWT approach the logout length precision is set by the expiration length of the access_token.
  - An invalidation alternative: A common approach for invalidating tokens when a user changes their password is to sign the token with a hash of their password. Thus if the password changes, any previous tokens automatically fail to verify. You can extend this to logout by including a last-logout-time in the user's record and using a combination of the last-logout-time and password hash to sign the token. This requires a DB lookup each time you need to verify the token signature, but presumably you're looking up the user anyway
  - But: approach is useful in monolithic apps, but in order to implement it in a microservices app you need all services to either store the user's password and last login or to make requests to fetch them and both are bad ideas.
- There is no clear advantage to combining cookies and jwts

## Salting and Hashing Passwords

- Good library to use for hashing and salting pws is [bcryptjs](https://www.npmjs.com/package/bcryptjs). This lib generates a random salt for you.
- Apply unique salt (random unpredictable string) to each password
  - A system-wide single salt is pointless to mitigate attacks; it would just make passwords longer.
  - should generate a unique salt upon creation of each stored credential (not just per user or system-wide). That includes passwords created during registration or as the result of a password reset.
- The salt doesn't need to be encrypted, for example. Salts are in place to prevent someone from cracking passwords at large and can be stored in cleartext in the database. However, do not make the salts readily accessible to the public
- A common practice is to simply append the salt to the hash of the pw.

### Third Party Auth

- The most common of these is OAuth2 (and its sibling OpenID Connect). These standards define a flow for authenticating with a third party and getting back an access token that can be used to make requests on behalf of the user.
- SSO - Single Sign On - used to be done using SAML (which is more difficult to implement) - now it is done more with OAuth2 and Open ID Connect methods.
