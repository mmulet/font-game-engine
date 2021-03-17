# Test

This is a small web page to test your font.
Assumes you already built your font, and that it is saved in ${projectRoot}/output/out.otf

## Running:

```
node host.js
```

or 
```
npm run host

```

This should open web page to test at http://localhost:3533

## Build


```
tsc && rollup --config rollup.config.js
```

## Note about the cache

Host.js should set the cache control to "no-store", so the browser
*should* not cache the font.

If you keep reloading the page and nothing changes, try emptying the cache.
On chrome:

1.  Open dev tools (ctrl+shift+I). (Ignore the window that pops up, it just needs to be open)
2.  In the browser window, (not the devTools window). Hold left mouse on the reload icon (looks like ↻)
3.  In the menu that pops up select: Empty Cache and Hard Reload
