import bpy
from .CharStringInfo import CharStringInfo
from .PixelPosition import PixelPosition


def rawCharStringToPixelCharStringInfo(charStringInfo):
    # type: (bpy.CharStringWithoutInitialPosition) -> CharStringInfo
    return CharStringInfo(
        charStringInfo['commands'],
        initialPosition=PixelPosition(charStringInfo['initialPosition']['x'],
                                      charStringInfo['initialPosition']['y']),
        endPosition=PixelPosition(charStringInfo['endPosition']['x'],
                                  charStringInfo['endPosition']['y']))
