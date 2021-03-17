from typing import Literal
from bpy import ContextOverride


class object:
    @classmethod
    def delete(cls, context: ContextOverride = ...) -> None: ...
    @classmethod
    def empty_add(cls, *, type: Literal["IMAGE", "PLAIN_AXES"]) -> None: ...
    @classmethod
    def font_create_text(cls) -> None: ...

    @classmethod
    def parent_set(
        cls, context: ContextOverride = ..., *, type: Literal["OBJECT"], keep_transform: bool) -> None: ...

    @classmethod
    def parent_clear(
        cls, context: ContextOverride = ..., *, type: Literal["CLEAR_KEEP_TRANSFORM"]) -> None: ...

    @classmethod
    def select_hierarchy(
        cls, *, direction: Literal["CHILD"], extend: bool) -> None: ...

    @classmethod
    def duplicate(
        cls, *, linked: bool = ...) -> None: ...


class node:
    @classmethod
    def view_selected(cls) -> None: ...
    @classmethod
    def add_node(cls, *, type: str = ...) -> None: ...
    @classmethod
    def translate_attach_remove_on_cancel(cls, c:Literal['INVOKE_DEFAULT']=...) -> None:...


class outliner:
    @classmethod
    def show_active(cls) -> None: ...
