# imageToCharStringConverter

The font needs the image in a custom vector format that I'm calling charstring.

This utility will convert an image to this format.

## Warning

These tools are only meant to work with pixel art (Low resolution and small color palette (less than 50 colors)).
They may crash on or not work on modern images with millions of colors and huge resolutions.
If working with modern images, you will need to convert your images first.
In blender, you can do this by setting a low resolution in scene options, and use
a color-ramp node as a shader to squash the color space down to a low number of colors.
