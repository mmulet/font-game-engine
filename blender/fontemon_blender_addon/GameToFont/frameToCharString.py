from functools import reduce
from .SpritePosition import SpritePosition
from .SubroutineInfoMap import SubroutineInfoMap
from .MakeCharStringState import MakeCharStringState
from .slotsToCharString import slotsToCharString
import bpy
from .addFrameInfoSpriteMapToCharString import addFrameInfoSpriteMapToCharString


def frameToCharString(assetToInfo, wordToInfo, slots):
    # type: (SubroutineInfoMap[str],  SubroutineInfoMap[str], bpy.Optional[list[str]]) -> bpy.Callable[[bpy.FrameInfo], str]
    def reducer(frameInfo):
        # type: (bpy.FrameInfo) -> str
        state = MakeCharStringState("", SpritePosition(0, 0))
        state2 = state if 'slots' not in frameInfo or slots is None else slotsToCharString(
            frameSlots=frameInfo['slots'],
            nodeSlots=slots,
            state=state,
            assetToInfo=assetToInfo)
        state3 = reduce(addFrameInfoSpriteMapToCharString(assetToInfo),
                        frameInfo['sprites'].items(), state2)
        state4 = state3 if 'words' not in frameInfo else reduce(
            addFrameInfoSpriteMapToCharString(wordToInfo),
            frameInfo['words'].items(), state3)
        return state4.fileContent

    return reducer
