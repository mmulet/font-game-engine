from .MakeCharStringState import MakeCharStringState
from .SpritePosition import SpritePosition


class MakeWordCharStringState(MakeCharStringState):
    def __init__(self, fileContent: str, currentPosition: SpritePosition,
                 characterStartPosition: SpritePosition) -> None:
        super().__init__(fileContent, currentPosition)
        self.characterStartPosition = characterStartPosition
