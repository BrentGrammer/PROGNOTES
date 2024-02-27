# NPM

## npm ci

- Does not change the package-lock.json file and sticks to its versions.
- Useful in CI/CD

## npm i vs. npm ci

- npm install will update the lock file
  - should be used when adding dependencies or making changes to package.json file
- npm ci will not update the lock file but install what it specifies
  - should use in CI/CD
  - should use if you are not making any changes to package.json (i.e. first pull of project etc.). This way the lock file will not change.

## Reverting changes to package-lock.json

- `git checkout main -- package-lock.json`
  - Make sure main is up to date and pulled
  - will revert package-lock.json to what is on main branch
  - commit this new change to restore the lock file
