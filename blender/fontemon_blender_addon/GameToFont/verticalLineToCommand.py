class VerticalLineToPair:
    def __init__(self, dy: float, thenDx: float) -> None:
        self.dy = dy
        self.thenDx = thenDx


def verticalLineToCommand(pairs, lastDy):
    # type: (list[VerticalLineToPair], float) -> str
    return f"{' '.join([f'{p.dy} {p.thenDx}' for p in pairs])} {lastDy} vlineto\n"
