# stubs

This is where the python types go.
This is used only by [pyright](https://github.com/Microsoft/pyright) and
maybe your editor

## Pylance

If you are using [pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) in vscode:
set the stub path directory to ${projectRootDir}/python/stubs

```js
python.analysis.stubPath;
```

Also set typeChecking mode to "strict"

```js
python.analysis.typeCheckingMode;
```

--- Note
All of these types are done by hand and may not be entirely accurate.

# All type checking is done with pyright version 1.1.115

```
npm install -g pyright@1.1.115
```
or use without installing
```
npx pyright@1.1.115
```

Later versions don't work because of a regression that forcibly disallows call expressions in type annotations.
If you are editing with vscode use pylance version v2021.2.4 or earlier. v2021.2.4 includes the version without the regression.


