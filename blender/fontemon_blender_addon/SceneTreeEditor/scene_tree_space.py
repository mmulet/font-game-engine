import bpy


def scene_tree_space(space):
    # type: (bpy.Optional[bpy.AllSpaceData]) -> bpy.Optional[bpy.SceneTreeSpaceDataType]
    if (space is None or
        space.type != "NODE_EDITOR" or
            space.tree_type != "SceneTreeType"):
        return None
    return space
