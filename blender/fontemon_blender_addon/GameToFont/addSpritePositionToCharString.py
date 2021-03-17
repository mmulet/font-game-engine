from .SubroutineInfo import SubroutineInfo
from .MakeCharStringState import MakeCharStringState
from .addSpriteToCharString import addSpriteToCharString
from .SpritePosition import SpritePosition
from typing import Callable


def addSpritePositionToCharString(
    subroutineInfo: SubroutineInfo
) -> Callable[[MakeCharStringState, SpritePosition], MakeCharStringState]:
    def reducer(state: MakeCharStringState,
                position: SpritePosition) -> MakeCharStringState:
        return addSpriteToCharString(state=state,
                                     position=position,
                                     subroutineInfo=subroutineInfo)

    return reducer
