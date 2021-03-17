from functools import reduce
from .SubroutineInfoMap import SubroutineInfoMap
from .MakeCharStringState import MakeCharStringState
from typing import Callable, Tuple, List
from .SpritePosition import SpritePosition
from .addSpritePositionToCharString import addSpritePositionToCharString


def addSpriteMapToCharString(
    assetToInfo: SubroutineInfoMap[str]
) -> Callable[[MakeCharStringState, Tuple[str, List[SpritePosition]]],
              MakeCharStringState]:
    def reducer(state: MakeCharStringState,
                info: Tuple[str, List[SpritePosition]]) -> MakeCharStringState:
        spriteID, positions = info
        subroutineInfo = assetToInfo[spriteID]
        return reduce(addSpritePositionToCharString(subroutineInfo), positions, state)
    return reducer
