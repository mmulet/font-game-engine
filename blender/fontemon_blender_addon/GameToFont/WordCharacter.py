import bpy
from typing import Union

class WordCharacterSpace:
    def __init__(self, type, length) -> None:
        # type: (bpy.Literal["space"], int) -> None
        self.type = type
        self.length = length


class WordCharacterChar:
    def __init__(self, type, char) -> None:
        # type: (bpy.Literal["char"], str) -> None
        self.type = type
        self.char = char


WordCharacter = Union[WordCharacterSpace, WordCharacterChar]
