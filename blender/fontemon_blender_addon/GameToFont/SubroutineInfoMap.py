from .SubroutineInfo import SubroutineInfo
from typing import TypeVar, Dict

T = TypeVar("T", int, str)


SubroutineInfoMap = Dict[T, SubroutineInfo]