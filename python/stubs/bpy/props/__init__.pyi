

from typing import Callable, Sequence, Type, TypeVar
from bpy import EnumPropertyItem, SceneTreeNodeInput, ContextType, Any, Sequence
from typing_extensions import Literal

I = TypeVar('I')


def IntProperty(name: str = ...,
                default: int = ...,
                description: str = ...,
                min: int = ...,
                max: int = ...,
                update: Callable[[
                    SceneTreeNodeInput, ContextType], None] = ...,
                get: Callable[[Any], int] = ...,
                set: Callable[[Any, int], None] = ...
                ) -> Type[int]: ...


def FloatProperty(name: str = ...,
                  default: float = ...,
                  description: str = ...,
                  min: float = ...,
                  max: float = ...,
                  update: Callable[[
                      SceneTreeNodeInput, ContextType], None] = ...,
                  get: Callable[[Any], float] = ...,
                  set: Callable[[Any, float], None] = ...
                  ) -> Type[float]: ...


def StringProperty(name: str = ...,
                   description: str = ...,
                   subtype: Literal["FILE_NAME", "DIR_PATH", "FILE_PATH"] = ...,
                   default: str = ...,
                   get: Callable[[Any], str] = ...,
                   set: Callable[[Any, str], None] = ...
                   ) -> Type[str]: ...


def BoolProperty(name: str = ...,
                 description: str = ...,
                 default: bool = ...,
                 get: Callable[[Any], bool] = ...,
                 set: Callable[[Any, bool], None] = ...
                 ) -> Type[bool]: ...


def FloatVectorProperty(name: str = ...,
                        description: str = ...,
                        default: Sequence[float] = ...,
                        size: int = ...,

                        ) -> Type[Sequence[float]]: ...


def BoolVectorProperty(name: str = ...,
                       description: str = ...,
                       default: Sequence[bool] = ...,
                       size: int = ...,

                       ) -> Type[Sequence[bool]]: ...


def IntVectorProperty(name: str = ...,
                      description: str = ...,
                      default: Sequence[int] = ...,
                      min: int = ...,
                      size: int = ...,
                      get: Callable[[Any], Sequence[int]] = ...,
                      set: Callable[[Any, Sequence[int]], None] = ...

                      ) -> Type[Sequence[int]]: ...


T = TypeVar('T')


def PointerProperty(
    name: str,
    type: Type[T],
    update: Callable[[
        Any, ContextType], None] = ...,
) -> Type[T]: ...


V = TypeVar('V')


def EnumProperty(items: list[EnumPropertyItem] | Callable[[Any, ContextType], list[EnumPropertyItem]],
                 name: str = ...,
                 description: str = ...,
                 get: Callable[[V], int] = ...,
                 set: Callable[[V, int], None] = ...) -> Type[str]: ...
