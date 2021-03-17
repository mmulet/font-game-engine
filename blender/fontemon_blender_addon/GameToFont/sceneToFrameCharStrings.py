from .SpritePosition import SpritePosition
import bpy
from .SubroutineInfoMap import SubroutineInfoMap
from .addRepeatedSceneFramesAsSubroutines import SceneNameToFrameSubroutines
from .frameToCharString import frameToCharString
from .callSubroutineCommand import callSubroutineCommand
from .slotsToCharString import slotsToCharString
from .MakeCharStringState import MakeCharStringState
from .relativeMoveToCommand import relativeMoveToCommand
from .endCharacterCommand import endCharacterCommand


class GlyphInfo:
    def __init__(self, glyphId: str, fileContent: str) -> None:
        self.glyphId = glyphId
        self.fileContent = fileContent


def getFrameContent(
    toCharString,
    frameSubroutineNumber,
    slots,
    frame,
    assetToInfo,
):
    # type: (bpy.Callable[[bpy.FrameInfo],str], bpy.Optional[int], list[str], bpy.FrameInfo, SubroutineInfoMap[str]) -> str
    if frameSubroutineNumber is None:
        return toCharString(frame)
    subroutineCommand = callSubroutineCommand(frameSubroutineNumber)
    if 'slots' not in frame:
        return subroutineCommand
    out = slotsToCharString(frameSlots=frame['slots'],
                            nodeSlots=slots,
                            state=MakeCharStringState('', SpritePosition(0,
                                                                         0)),
                            assetToInfo=assetToInfo)
    return f"{out.fileContent}\n{relativeMoveToCommand(-out.currentPosition.x, -out.currentPosition.y)}\n{subroutineCommand}"


def sceneToFrameCharStrings(nodeId_to_list_of_frame_blank_glyph_ID,
                            assetToInfo, wordToInfo,
                            sceneNameToFrameSubroutines, game):
    # type: (bpy.NodeId_to_list_of_frame_blank_glyph_ID, SubroutineInfoMap[str], SubroutineInfoMap[str], SceneNameToFrameSubroutines, bpy.SceneTreeOutputType ) -> bpy.Callable[[bpy.Tuple[str, bpy.SceneNodeInfoType]], list[GlyphInfo]]
    def reducer(info):
        # type: (bpy.Tuple[str, bpy.SceneNodeInfoType]) -> list[GlyphInfo]
        nodeId, node = info
        frameToBlankGlyphId = nodeId_to_list_of_frame_blank_glyph_ID[nodeId]
        scene_name = node['scene_name']
        slots = node['slots']
        frames = game['scenes'][scene_name]['frames']
        toCharString = frameToCharString(assetToInfo=assetToInfo,
                                         wordToInfo=wordToInfo,
                                         slots=slots)
        maybeSceneSubroutines = sceneNameToFrameSubroutines.get(
            node['scene_name'], None)

        return [
            GlyphInfo(glyphId=frameToBlankGlyphId[index],
                      fileContent="0 800 vmoveto\n" + getFrameContent(
                          toCharString=toCharString,
                          frame=frame,
                          frameSubroutineNumber=maybeSceneSubroutines[index]
                          if maybeSceneSubroutines is not None else None,
                          assetToInfo=assetToInfo,
                          slots=slots) + endCharacterCommand())
            for index, frame in enumerate(frames)
        ]

    return reducer
