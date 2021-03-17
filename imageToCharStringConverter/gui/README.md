## GUI

Launch the GUI in three steps:

1. ```sh
   cd gui
   ```

2. ```sh
   npm install .
   ```

3. ```sh
   npm run gui
   ```

This should open up a webpage with the GUI.

# build
```
tsc && rollup --config rollup.config.js
```

### GUI Instructions

This GUI is a barebones editor for charstrings. Charstrings can only contain 4 colors:

1. Black
2. Light Gray
3. Dark Gray
4. Transparent (usually white)

5. Open an image file with the image picker

6. You should see, on the left hand side, a List:

- Output Colors:
- Black
- Transparent
- lightGray
- darkGray
- Input Colors:
- All of your input colors

Your job is to transform the input colors to the output colors:
Left click on an Input color and you will see a red border around that color. Now,
click on one of the output colors,
the input color will disappear and the image will transform all pixels with that input color, to the output color.

Keep going until there are no more input colors left.

You can also select the colors from the image itself. Position your cursor over the image, if you look to the left you should see a yellow box over then color of that pixel.
Left click, and that yellow box will turn red, that means the color has been selected.

- Click again to deselect your color.

Once you have eliminated all input colors, pres the Save CharString button to save your charstring.
You can also press the Save ModifiedImage button so save your new image (for preview in blender)

