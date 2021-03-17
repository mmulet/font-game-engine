from typing import Callable, Type,TypeVar
from bpy.types import Scene
RT = TypeVar("RT")  # returnTYpe


def persistent(a: Callable[..., RT]) -> Callable[..., RT]: ...

HandlerCallbackListType : Type[list[Callable[[Scene], None]]]

frame_change_post: HandlerCallbackListType
load_post: HandlerCallbackListType

