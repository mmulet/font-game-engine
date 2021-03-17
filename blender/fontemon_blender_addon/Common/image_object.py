import bpy


def image_object(o):
    # type: (bpy.Optional[bpy.AllObjectTypes]) -> bpy.Optional[bpy.EmptyImageObjectTypeWithData]
    if o is None:
        return None
    if o.type != "EMPTY":
        return None
    if o.empty_display_type != "IMAGE":
        return None
    if o.data is None:
        return None
    out = o # type: bpy.Any
    return out
