from .CharStringInfo import CharStringInfo


class SubroutineInfo:
    def __init__(self, subroutineNumber: int,
                 charStringInfo: CharStringInfo) -> None:
        self.subroutineNumber = subroutineNumber
        self.charStringInfo = charStringInfo
