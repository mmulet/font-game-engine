import bpy


def shiftSpriteMapUpwards(out_map):
  # type: (bpy.FrameInfoPositionListable) -> None
  for positions in out_map.values():
    for position in positions:
      position['y'] += 1000


def parseGame(out_game, smaller):
  # type: (bpy.SceneTreeOutputType, bool) -> None
  if not smaller:
    return
  for scene in out_game['scenes'].values():
    for frame in scene['frames']:
      shiftSpriteMapUpwards(frame['sprites'])
      shiftSpriteMapUpwards(frame['words'])
      shiftSpriteMapUpwards(frame['slots'])
  