from .PixelPosition import PixelPosition
from .SpritePosition import SpritePosition
from .SubroutineInfoMap import SubroutineInfoMap
from .CharStringInfo import CharStringInfo
from .findSpaceRuns import findSpaceRuns
from .addCharacterToCharString import addCharacterToCharString
from .MakeWordCharStringState import MakeWordCharStringState
from .constants import pixelWidth, pixelHeight
from functools import reduce


def wordToCharStringInfo(
        word: str, assetToInfo: SubroutineInfoMap[str]) -> CharStringInfo:
    characters = findSpaceRuns(word)
    out = reduce(
        addCharacterToCharString(assetToInfo), characters,
        MakeWordCharStringState(fileContent="",
                                currentPosition=SpritePosition(x=0, y=0),
                                characterStartPosition=SpritePosition(x=0,
                                                                      y=0)))
    return CharStringInfo(out.fileContent,
                          initialPosition=PixelPosition(0, 0),
                          endPosition=PixelPosition(
                              float(out.currentPosition.x) / pixelWidth - 1,
                              -float(out.currentPosition.y) / pixelHeight))
