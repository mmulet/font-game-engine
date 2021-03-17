# Fontemon game engine in blender!

Fontemon uses [blender](https://www.blender.org/) for level creation and game layout.

## Installation

I used blender 2.92.0. I cannot guarantee that the tools will work with any other version.

1. Install [blender 2.92](https://www.blender.org/download/releases/2-92/)
2. Install the fontemon_blender_addon (instructions below)
3. Open one of the blender files in ${projectRoot}/blender/blenderFiles/\*

All blender files included here need the fontemon_blender_addon
First you need to zip the source files into a .zip file

1. zip fontemon_blender_addon
2. Open blender
3. Open the Preferences Window: Edit > Preferences
4. On the left hand side click the Add-ons menu button: Add-ons
5. Near the top of the window, click the Install button: Install
6. Navigate to this directory and click on "fontemon_blender_addon.zip"
7. Near the bottom of the window, click the Install Add-on button
8. Wait
9. Once the fontemon addon appears, click the empty checkbox on the left hand side. Once you see a check in the checkbox, the add-on is installed and enabled!

- Guaranteed to work with blender 2.92. If you are having trouble, try using blender 2.92

## The anatomy of a font game.

### Definitions

A font game is divided into a network or "tree" of "scenes".
Each scene is a uninterrupted sequence of "frames".
Each scene will transition to the next scene based on "conditions".

Example:

- The font game starts.
- The player presses any key and the title appears. This is the first "frame" of the first "scene"
- The player presses any key and the title shifts to the right a bit. This is the second "frame" of the first "scene"
- If they player presses the "a" key we will show the picture of the sun, otherwise will will show a picture of the moon.
  Here we have two "conditions" each leading to two different "scenes".
  - The first condition is "a" key leading to first frame of the sun "scene"
  - The second condition is called the "default" condition, this is the condition we go to when no other conditions are met. This condition leads to the first frame of the moon "scene".



- Use Show in Orthographic to show/hide frames
- Only one asset can be used in frame at a time.
- Save all charstrings in ${projectRootDir}/images/charStrings

# FontTools

Included is a custom fork of fontTools modified for speed. On my machine, it is about 30-50x faster than normal font tools which means I can compile font games
in seconds rather than minutes.
## Note to future self
Look for changes by searching for the string "LFDS"
(without quotes)

