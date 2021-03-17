Project structure. Included is a suite of tools to create font games.

# Tutorial:

For a quick tutorial about how to make your own game [go here](https://github.com/mmulet/code-relay/blob/main/markdown/Tutorial.md)

# For developers:

The project is structured around a blender addon called `fontemon-blender-addon`. The addon also s

- blender: Fontemon uses [blender](https://www.blender.org/) for level creation
  and game layout using a custom addon called fontemon-blender-addon.

Along with 3 other tools for development:

- imageToCharStringConverter: Convert an image to a charstring (a vector graphics format needed by the font.)
- textPreviewTool: A tool for writing text boxes with instant feedback.
- testFontInBrowser: A GUI for testing the font in the browser

These other tools are served by a simple HTTP server run by the blender addon

Each tool has it's own README.md in it's root directory.
# Getting started

Start with the README.md in the ./blender/README.md

