# Authentication


## Loading user data and showing login/app based in login status on app load:
- Can split app into authenticated and unauthenticated parts and render either
  conditionally at the top level

```javascript
function App() {
  // login/register sets user state in redux or locally here, logout clears

  // on app load, get user information and check if there is a token/authenticated, set state to determine what part of app to render
  // this allows so user does not have to log in when loading the app if already logged in
  useEffect(() => {
    getUser().then(u => setUser(u))
  }, [])

  // show loading instead of home/login screen before user is fetched (from video Authentication => use UseAsync)
  if (isLoading) return <Loading />

  // handle error state and what to render etc.

  // async request finishes state is success
  if (isSuccess) {
    return user ? (
      <AuthenticatedApp user={user} logout={logout} />
    ) : (
      <UnauthenticatedApp login={login} register={register} />
    )
  }
}
```
