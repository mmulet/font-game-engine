import bpy
from .has_all_text_attributes import has_all_text_attributes

def text_object(o):
    # type: (bpy.Optional[bpy.AllObjectTypes]) -> bpy.Optional[bpy.EmptyTextType]
    if o is None:
        return None
    if o.type != "EMPTY":
        return None
    if o.empty_display_type != "PLAIN_AXES":
        return None
    if not has_all_text_attributes(o):
        return None
    return o
