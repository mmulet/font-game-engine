from .SubroutineInfo import SubroutineInfo
from xml.etree.ElementTree import Element
from .CharStringInfo import CharStringInfo
from typing import Callable
from .AddSubroutineState import AddSubroutineState
from .addCharStringToTable import addCharStringToTable
from .SubroutineInfoMap import  T


def addCharStringToSubroutineTable(
    getCharStringInfo: Callable[[T],
                                CharStringInfo], out_subroutineTable: Element
) -> Callable[[AddSubroutineState[T], T], AddSubroutineState[T]]:
    def reducer(state: AddSubroutineState[T],
                assetId: T) -> AddSubroutineState[T]:
        charStringInfo = getCharStringInfo(assetId)
        addCharStringToTable(out_subroutineTable, charStringInfo.commands,
                             state.index)
        state.subroutineInfoMap[assetId] = SubroutineInfo(
            state.subroutineNumber, charStringInfo)
        state.index += 1
        state.subroutineNumber += 1
        return state

    return reducer
