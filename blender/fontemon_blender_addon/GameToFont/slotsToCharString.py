import bpy
from .MakeCharStringState import MakeCharStringState
from .SubroutineInfoMap import SubroutineInfoMap
from functools import reduce
from .addFrameInfoSpriteMapToCharString import addFrameInfoSpriteMapToCharString


def slotsToCharString(frameSlots, nodeSlots, state, assetToInfo):
    # type: (bpy.SlotList, list[str], MakeCharStringState, SubroutineInfoMap[str]) -> MakeCharStringState
    return reduce(addFrameInfoSpriteMapToCharString(assetToInfo),
                  [(nodeSlots[int(slotNumber)], positions)
                   for slotNumber, positions in frameSlots.items()], state)
