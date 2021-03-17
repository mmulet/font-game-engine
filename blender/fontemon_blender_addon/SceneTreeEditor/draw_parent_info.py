import bpy
from .get_shared_parent import get_shared_parent


def draw_parent_info(layout, o, image_objects):
    # type: (bpy.types.UILayout, bpy.HasParent, bpy.Optional[bpy.Sequence[bpy.HasParent]]) -> None
    parent = get_shared_parent(
        image_objects) if image_objects is not None else o.parent
    if parent is None:
        return
    _ = layout.label(text=f"Parent: {parent.name}")
    _ = layout.operator("font.selectparent")
