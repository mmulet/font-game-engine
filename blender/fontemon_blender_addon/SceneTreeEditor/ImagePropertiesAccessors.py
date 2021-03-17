import bpy
from ..Common import image_object
from .get_or_make_animation_pattern import get_or_make_animation_pattern
from typing import overload


@overload
def get_prop(field, default):
    # type: (bpy.EmptyImageBoolFields, bool) -> bool
    ...


@overload
def get_prop(field, default):
    # type: (bpy.EmptyImageIntFields, int) -> int
    ...


@overload
def get_prop(field, default):
    # type: (bpy.EmptyImageStrFields, str) -> str
    ...


def get_prop(field, default):
    # type: (bpy.Any, str | int | bool) -> str | int | bool
    o = image_object(bpy.context.active_object)
    if (o is None or field not in o):
        return default
    fieldName2 = field  # type: bpy.EmptyImageStrFields
    return o[fieldName2]


@overload
def set_prop(field, default):
    # type: (bpy.EmptyImageBoolFields, bool) -> None
    ...


@overload
def set_prop(field, default):
    # type: (bpy.EmptyImageIntFields, int) -> None
    ...


@overload
def set_prop(field, default):
    # type: (bpy.EmptyImageStrFields, str) -> None
    ...


def set_prop(field, value):
    # type: (bpy.Any, str) -> None
    o = image_object(bpy.context.active_object)
    if o is None:
        return
    fieldName2 = field  # type: bpy.EmptyImageStrFields
    o[fieldName2] = value


@overload
def pattern_get_prop(field, default):
    # type: (bpy.AnimationPatternIntKeys, int) -> int
    ...


@overload
def pattern_get_prop(field, default):
    # type: (bpy.AnimationPatternStrKeys, str) -> str
    ...


@overload
def pattern_get_prop(field, default):
    # type: (bpy.AnimationPatternBoolKeys, bool) -> bool
    ...


@overload
def pattern_get_prop(field, default):
    # type: (bpy.AnimationPatternIntVectorKeys, bpy.Sequence[int]) -> bpy.Sequence[int]
    ...


def pattern_get_prop(field, default):
    # type: (bpy.AnimationPatternIntKeys, int) -> int
    o = image_object(bpy.context.active_object)
    if o is None or "font_animation_pattern_info" not in o:
        return default
    return o["font_animation_pattern_info"][field]




default_patterns = [list(range(i+1)) for i in range(14)]

def get_pattern_of_length(length):
    # type: (int) -> list[int]
    o = image_object(bpy.context.active_object)
    if o is None or "font_animation_pattern_info" not in o:
        return default_patterns[length - 1]
    return o["font_animation_pattern_info"]["pattern"][:length]

def set_pattern_of_length(value):
    # type: (bpy.Sequence[int]) -> None
    o = image_object(bpy.context.active_object)
    if o is None:
        return
    old_pattern = get_or_make_animation_pattern(o)["pattern"]
    for [index, new_value] in enumerate(value):
        old_pattern[index] = new_value
    

@overload
def pattern_set_prop(field, value):
    # type: (bpy.AnimationPatternIntKeys, int) -> None
    ...


@overload
def pattern_set_prop(field, value):
    # type: (bpy.AnimationPatternStrKeys, str) -> None
    ...


@overload
def pattern_set_prop(field, value):
    # type: (bpy.AnimationPatternBoolKeys, bool) -> None
    ...


@overload
def pattern_set_prop(field, value):
    # type: (bpy.AnimationPatternIntVectorKeys, bpy.Sequence[int]) -> None
    ...


def pattern_set_prop(field, default):
    # type: (bpy.AnimationPatternIntKeys, int) -> None
    o = image_object(bpy.context.active_object)
    if o is None:
        return
    get_or_make_animation_pattern(o)[field] = default
