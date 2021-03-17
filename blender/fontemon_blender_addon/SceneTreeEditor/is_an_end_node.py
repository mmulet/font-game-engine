
import bpy


def is_an_end_node(node):
    # type: (bpy.AllSceneNodeTypes) -> bool
    return node.bl_idname == 'EndSceneNode'


def cast_to_not_an_end_node(node):
    # type: (bpy.AllSceneNodeTypes) -> bpy.Optional[bpy.AllOutputSceneNodeTypes]
    """None if it is an end node. Otherwise return the input"""
    # playing games with types
    if node.bl_idname == "EndSceneNode":
        return None
    return node
