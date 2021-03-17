# Text Preview Tool

You can create text boxes in blender, but the interface is a bit clunky

- You have to use \n instead of newlines.
- Editing is a huge pain.
- No live update of your changes.

This is a tool to make editing text a breeze!

- Just type your text in the text box and the preview will update automatically
- You can use enter to go to the next line. instead of typing \n
- You can go backwards or forwards by dragging the red box over the frames
- You can jump to a specific frame by clicking on it.
- When you are done, click on Transform output to copy the output to your clipboard
- Paste the output into blender!

# Installing

```sh
npm install .
```

# Running

```sh
npm run host
```

# build

```
tsc && rollup --config rollup.config.js
```
