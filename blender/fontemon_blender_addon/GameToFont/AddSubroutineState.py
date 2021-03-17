from .SubroutineInfoMap import SubroutineInfoMap, T
from typing import Generic


class AddSubroutineState(Generic[T]):
    def __init__(self, subroutineInfoMap: SubroutineInfoMap[T], index: int,
                 subroutineNumber: int) -> None:
        super().__init__()
        self.subroutineInfoMap = subroutineInfoMap
        self.index = index
        self.subroutineNumber = subroutineNumber
