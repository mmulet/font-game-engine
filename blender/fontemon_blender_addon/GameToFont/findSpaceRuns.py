from .WordCharacter import WordCharacterSpace, WordCharacter, WordCharacterChar
import bpy

def findSpaceRuns(word: str):
    # type: (str) -> list[bpy.WordCharacter]
    characters = []  # type: list[WordCharacter]
    spaceRun = 0
    for char in word:
        if char == " ":
            spaceRun += 1
            continue
        if spaceRun != 0:
            characters.append(WordCharacterSpace('space', spaceRun))
            spaceRun = 0
        characters.append(WordCharacterChar('char', char))
    if spaceRun != 0:
        characters.append(WordCharacterSpace('space', spaceRun))
    out = characters # type: bpy.Any
    return out
