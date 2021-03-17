import bpy

def remove_all_children(o):
    # type: (bpy.types.Object) -> None
    override = bpy.context.copy()
    override['selected_objects'] = o.children
    bpy.ops.object.delete(override)