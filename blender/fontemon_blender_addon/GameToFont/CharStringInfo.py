from .PixelPosition import PixelPosition


class CharStringInfo:
    def __init__(self, commands: str, initialPosition: PixelPosition,
                 endPosition: PixelPosition) -> None:
        self.commands = commands
        self.initialPosition = initialPosition
        self.endPosition = endPosition
