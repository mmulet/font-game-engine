import bpy
from ..Common import text_object
from typing import overload



def get_end_prop(field):
    # type: (bpy.TextEndTypeFields) -> int
    o = text_object(bpy.context.active_object)
    if o is None:
        return 0
    return o['font_text_end'][field]


def set_end_prop(field, value):
    # type: (bpy.TextEndTypeFields, int) -> None
    o = text_object(bpy.context.active_object)
    if o is None:
        return
    o['font_text_end'][field] = value

@overload
def get_prop(field, default):
    # type: (bpy.EmptyTextTypeBoolFields, bool) -> bool
    ...
@overload
def get_prop(field, default):
    # type: (bpy.EmptyTextTypeStrFields, str) -> str
    ...
@overload
def get_prop(field, default):
    # type: (bpy.EmptyTextTypeIntFields, int) -> int
    ...
@overload
def get_prop(field, default):
    # type: (bpy.EmptyTextTypeFloatFields, float) -> float
    ...
def get_prop(field, default):
    # type: (bpy.EmptyTextTypeBoolFields, bool) -> bool
    o = text_object(bpy.context.active_object)
    if o is None:
        return default
    return o[field]


@overload
def set_prop(field, default):
    # type: (bpy.EmptyTextTypeBoolFields, bool) -> None
    ...
@overload
def set_prop(field, default):
    # type: (bpy.EmptyTextTypeStrFields, str) -> None
    ...
@overload
def set_prop(field, default):
    # type: (bpy.EmptyTextTypeIntFields, int) -> None
    ...
@overload
def set_prop(field, default):
    # type: (bpy.EmptyTextTypeFloatFields, float) -> None
    ...

def set_prop(field, value):
    # type: (bpy.EmptyTextTypeBoolFields, bool) -> None
    o = text_object(bpy.context.active_object)
    if o is None:
        return
    o[field] = value