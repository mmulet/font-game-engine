from .SubroutineInfoMap import SubroutineInfoMap
from .addSpriteMapToCharString import addSpriteMapToCharString
from .MakeCharStringState import MakeCharStringState
from .SpritePosition import SpritePosition
import bpy


def addFrameInfoSpriteMapToCharString(assetInfo):
    # type: (SubroutineInfoMap[str]) -> bpy.Callable[[MakeCharStringState, bpy.Tuple[str, list[bpy.FrameInfoPosition]]], MakeCharStringState]
    other_reducer = addSpriteMapToCharString(assetInfo)

    def reducer(state, info):
        # type: (MakeCharStringState, bpy.Tuple[str, list[bpy.FrameInfoPosition]]) -> MakeCharStringState
        return other_reducer(
            state,
            (info[0], [SpritePosition(p['x'], p['y']) for p in info[1]]))

    return reducer
