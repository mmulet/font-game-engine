from .MakeWordCharStringState import MakeWordCharStringState
from .charToCode import charToCode
import bpy
from .SubroutineInfoMap import SubroutineInfoMap
from .addSpriteToCharString import addSpriteToCharString
from .constants import fontCharacterWidth, pixelWidth
from .horizontalMoveToCommand import horizontalMoveToCommand
from .charCodeToAssetName import charCodeToAssetName

def addCharacterToCharString(assetToInfo):
    # type: (SubroutineInfoMap[str]) -> bpy.Callable[[MakeWordCharStringState, bpy.WordCharacter],MakeWordCharStringState]
    def reducer(state, character):
        # type: (MakeWordCharStringState, bpy.WordCharacter) -> MakeWordCharStringState
        if character.type == "char":
            code = charToCode(character.char)
            subroutineInfo = assetToInfo[charCodeToAssetName(code)]
            state = addSpriteToCharString(
                position=state.characterStartPosition,
                state=state,
                subroutineInfo=subroutineInfo)
            state.characterStartPosition.x += fontCharacterWidth * pixelWidth
            state.characterStartPosition.y += 0
            return state
        distance = character.length*fontCharacterWidth*pixelWidth
        state.fileContent += horizontalMoveToCommand(distance)
        state.characterStartPosition.x += distance
        state.currentPosition.x += distance
        return state
    return reducer
