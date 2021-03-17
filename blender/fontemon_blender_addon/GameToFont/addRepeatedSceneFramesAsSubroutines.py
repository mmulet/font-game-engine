from .SubroutineInfoMap import SubroutineInfoMap
from xml.etree.ElementTree import Element
import bpy
from .findRepeatedScenes import findRepeatedScenes
from .frameToCharString import frameToCharString
from .addCharStringToTable import addCharStringToTable
from functools import reduce
from typing import Dict, List


class FrameSubroutineState:
    def __init__(self, frameSubroutineNumbers: "list[int]", index: int,
                 subroutineNumber: int) -> None:
        self.frameSubroutineNumbers = frameSubroutineNumbers
        self.index = index
        self.subroutineNumber = subroutineNumber


SceneNameToFrameSubroutines = Dict[str, List[int]]


class RepeatedFrameSubroutineState:
    def __init__(self,
                 sceneNameToFrameSubroutines: SceneNameToFrameSubroutines,
                 index: int, subroutineNumber: int) -> None:
        self.sceneNameToFrameSubroutines = sceneNameToFrameSubroutines
        self.index = index
        self.subroutineNumber = subroutineNumber


def addRepeatedSceneFramesAsSubroutines(game, assetToInfo, wordToInfo,
                                        out_subroutineTable, subroutineIndex,
                                        subroutineNumber):
    # type: (bpy.SceneTreeOutputType, SubroutineInfoMap[str], SubroutineInfoMap[str], Element, int, int) -> SceneNameToFrameSubroutines
    repeatedScenes = findRepeatedScenes(game["nodes"])

    def reducer2(state, frame):
        # type: (FrameSubroutineState, bpy.FrameInfo) -> FrameSubroutineState
        charString = frameToCharString(assetToInfo, wordToInfo,
                                       slots=None)(frame)
        addCharStringToTable(out_subroutineTable, charString, state.index)
        state.frameSubroutineNumbers.append(state.subroutineNumber)
        state.index += 1
        state.subroutineNumber += 1
        return state

    def reducer(state: RepeatedFrameSubroutineState,
                scene_name: str) -> RepeatedFrameSubroutineState:
        frames = game['scenes'][scene_name]['frames']
        next_state = reduce(
            reducer2, frames,
            FrameSubroutineState([],
                                 index=state.index,
                                 subroutineNumber=state.subroutineNumber))
        state.sceneNameToFrameSubroutines[
            scene_name] = next_state.frameSubroutineNumbers
        state.index = next_state.index
        state.subroutineNumber = next_state.subroutineNumber
        return state

    return reduce(
        reducer, repeatedScenes,
        RepeatedFrameSubroutineState(
            {}, index=subroutineIndex,
            subroutineNumber=subroutineNumber)).sceneNameToFrameSubroutines
