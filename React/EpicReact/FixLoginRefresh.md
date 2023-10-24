To fix the login screen showing on refresh briefly:

from Epic React Kent C Dodds vid: https://epicreact.dev/modules/build-an-epic-react-app/authentication-extra-credit-solution-02

Need a loading state to key off of

- If Loading, show spinner

In the top level where you are getting user data if logged in:

ex maybe in app.jsx:

// log user in with existing token and set User state here

useEffect(() => {
 // define getuser if necessary
  getUser();  // this needs to set loading state and reset when it's finished
}, []);

// base this on the async status of the request to check if user is logged in
if (isLoading || isIdle) return <Loading />;

if (error) return <Error message={message} />;

if (success) {
  return user ? <AuthenticatedApp user={user} />
  : <UnauthenticatedApp />
}

// render authenticated app if there is a user or the unauthed app if not:
if (isSuccess)