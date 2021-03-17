from .SpritePosition import SpritePosition
from .SubroutineInfo import SubroutineInfo
from .MakeCharStringState import MakeCharStringState
from typing import TypeVar
from .relativeMoveToCommand import relativeMoveToCommand
from .callSubroutineCommand import callSubroutineCommand
from .constants import pixelWidth, pixelHeight

T = TypeVar('T', bound=MakeCharStringState)


def addSpriteToCharString(
    position: SpritePosition,
    state: T,
    subroutineInfo: SubroutineInfo,
) -> T:
    charStringInfo = subroutineInfo.charStringInfo
    initialPosition = charStringInfo.initialPosition
    endPosition = charStringInfo.endPosition
    state.fileContent += relativeMoveToCommand(
        dx=position.x - state.currentPosition.x +
        initialPosition.pixelX * pixelWidth,
        dy=position.y - state.currentPosition.y - initialPosition.pixelY *
        pixelHeight) + callSubroutineCommand(subroutineInfo.subroutineNumber)
    state.currentPosition.x = position.x + (endPosition.pixelX +
                                            1) * pixelWidth
    state.currentPosition.y = position.y - endPosition.pixelY * pixelHeight
    return state
