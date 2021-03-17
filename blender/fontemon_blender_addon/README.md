# Fontemon blender addon

This is the addon for creation of font games in blender.

## Note about Python types

### Problem

The my current version of blender (2.92) uses python 3.7.7.
There are some type features of python 3.8, that I don't
want to program without (like Literal and TypedDict). Furthermore,
typing_extensions is not included with blender, and it's
a pain to ask users to install it themselves.

### Solution

1. We are going to program all of the python types in python 3.8, but
   run the the actual addon in 3.7.
2. Keep the type files in a separate directory `${projectRoot}\python\stubs`
3. Use [python 2 style type comments](https://mypy.readthedocs.io/en/latest/cheat_sheet.html) instead of [python 3 type annotations](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html)
   , so that the interpreter doesn't complain about missing types.

When blender upgrades python to 3.8 or greater, we can merge everything
back in, and this problem will go away

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
