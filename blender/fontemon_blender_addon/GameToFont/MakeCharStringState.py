from .SpritePosition import SpritePosition


class MakeCharStringState:
    fileContent: str
    currentPosition: SpritePosition

    def __init__(self, fileContent: str,
                 currentPosition: SpritePosition) -> None:
        self.fileContent = fileContent
        self.currentPosition = currentPosition
