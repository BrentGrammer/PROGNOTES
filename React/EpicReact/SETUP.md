# SETUP AND CONFIGURATION TIPS

## Compiler Options
- Set baseUrl in a jsconfig.json file to allow for shorter imports without having to specify relative path.  i.e. import {mystuff} from 'utils/mystuff'
```json
{
  "compilerOptions": {
    "baseUrl": "./src" // point to path where your source code is
  },
  "include": ["src"]
}
```