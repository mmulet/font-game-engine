import bpy



def get_shared_parent(objects):
    # type: (bpy.Sequence[bpy.HasParent]) -> bpy.Optional[bpy.AllObjectTypes]
    if len(objects) <= 0:
        return None
    shared_parent = objects[0].parent
    if shared_parent is None:
        return None
    for o in objects:
        if (o.parent is None or
                o.parent.name != shared_parent.name):
            return None
    return shared_parent
